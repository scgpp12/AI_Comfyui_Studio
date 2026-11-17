# -*- coding: utf-8 -*-
# 设计书试算：拿 8188 今天的 /history（只读导出的 json）按设计书的规则算一遍：指纹、分组中位耗时、异常。
# 用法：python trial.py history_8188.json 输出目录
import json, sys, hashlib, statistics as st, os, collections

H = json.load(open(sys.argv[1], encoding="utf-8")); OUTD = sys.argv[2]; os.makedirs(OUTD, exist_ok=True)
MODEL_EXT = (".safetensors", ".pth", ".ckpt", ".gguf", ".pt", ".bin", ".onnx")
# 指纹里不算的输入：每次都会变的内容（提示词、种子、文件名前缀、输入文件）
VOLATILE = {"prompt", "text", "negative_prompt", "seed", "noise_seed", "filename_prefix", "image", "audio", "video", "string", "value"}
SIZE_KEYS = {"width", "height", "length", "batch_size"}


def model_files(p):
    return sorted({v for n in p.values() for v in n["inputs"].values() if isinstance(v, str) and v.lower().endswith(MODEL_EXT)})


def fingerprint(p):
    """节点类型（按类型计数，不看节点编号）＋模型文件＋固定参数（数字、开关、采样器名等），连线只记上游节点类型。"""
    items = []
    for n in p.values():
        ins = []
        for k, v in sorted(n["inputs"].items()):
            if k in VOLATILE or k in SIZE_KEYS or k.startswith(("images.", "ref_images.", "ref_audios.")):
                continue
            if isinstance(v, list):
                ins.append((k, "<-" + p[v[0]]["class_type"]))
            elif isinstance(v, str) and len(v) > 200:
                continue                                    # 长文本当提示词看
            else:
                ins.append((k, v))
        items.append(json.dumps([n["class_type"], ins], ensure_ascii=False, sort_keys=True))
    return hashlib.sha1("\n".join(sorted(items)).encode()).hexdigest()[:10]


def size_of(p):
    for n in p.values():
        i = n["inputs"]
        if "width" in i and "height" in i and isinstance(i["width"], int):
            return "%dx%d%s" % (i["width"], i["height"], ("x%d" % i["length"]) if isinstance(i.get("length"), int) else "")
    return "-"


def steps_of(p):
    for n in p.values():
        if n["class_type"] in ("KSampler", "BasicScheduler") and isinstance(n["inputs"].get("steps"), int):
            return n["inputs"]["steps"]
        if n["class_type"] == "ManualSigmas":
            return len(n["inputs"]["sigmas"].split(",")) - 1
    return None


def prefix_of(p):
    for n in p.values():
        if "filename_prefix" in n["inputs"]:
            return n["inputs"]["filename_prefix"]
    return ""


rows = []
for pid, v in H.items():
    p = v["prompt"][2]; ex = v["prompt"][3]; msg = {m[0]: m[1] for m in v["status"]["messages"]}
    t_start = msg.get("execution_start", {}).get("timestamp"); t_end = (msg.get("execution_success") or msg.get("execution_error") or msg.get("execution_interrupted") or {}).get("timestamp")
    main = [n["inputs"]["unet_name"] for n in p.values() if n["class_type"] == "UNETLoader"]
    rows.append(dict(prompt_id=pid, 提交=ex.get("create_time"), 开始=t_start, 结束=t_end, 排队秒=round((t_start - ex["create_time"]) / 1000, 1) if t_start and ex.get("create_time") else None,
                     总耗时秒=round((t_end - t_start) / 1000, 1) if t_start and t_end else None, 状态=v["status"]["status_str"],
                     指纹=fingerprint(p), 主模型=main[0] if main else "-", 模型=model_files(p), 尺寸=size_of(p), 步数=steps_of(p),
                     节点数=len(p), 参考图数=sum(1 for n in p.values() if n["class_type"] == "LoadImage"),
                     有块补丁=any(n["class_type"] in ("QwenImageDiffsynthControlnet", "MiniMaxH3FunControlNetApply") for n in p.values()),
                     前缀=prefix_of(p)))
rows.sort(key=lambda r: r["开始"] or 0)
json.dump(rows, open(os.path.join(OUTD, "runs_trial.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- 异常规则 ----
# 规则 1（同指纹同尺寸）：总耗时 > 该组中位 × 2，且多出 ≥ 30 秒；组内至少 3 条才判。
# 规则 2（同主模型同尺寸，跨指纹）：每步秒数 > 同主模型同尺寸「不挂块补丁」那些任务每步中位 × 3 → 结构性慢（今天 103 对 14 那种）。
# 规则 3：状态不是 success。
grp = collections.defaultdict(list)
for r in rows:
    if r["总耗时秒"]:
        grp[(r["指纹"], r["尺寸"])].append(r["总耗时秒"])
fam = collections.defaultdict(list)
for r in rows:
    if r["总耗时秒"] and r["步数"] and not r["有块补丁"]:
        fam[(r["主模型"], r["尺寸"])].append(r["总耗时秒"] / r["步数"])
anom = []
for r in rows:
    if r["状态"] != "success":
        anom.append((r, "规则3 失败", r["状态"]))
        continue
    g = grp[(r["指纹"], r["尺寸"])]
    if len(g) >= 3 and r["总耗时秒"] > 2 * st.median(g) and r["总耗时秒"] - st.median(g) >= 30:
        anom.append((r, "规则1 同指纹慢", "%.1f 秒，组中位 %.1f 秒（%d 条）" % (r["总耗时秒"], st.median(g), len(g))))
    f = fam.get((r["主模型"], r["尺寸"]))
    if r["步数"] and f and len(f) >= 3:
        sps = r["总耗时秒"] / r["步数"]
        if sps > 3 * st.median(f):
            anom.append((r, "规则2 结构性慢", "每步约 %.2f 秒，同模型同尺寸不挂补丁的中位 %.2f 秒（%d 条），%.1f 倍" % (sps, st.median(f), len(f), sps / st.median(f))))

print("总条数", len(rows), "指纹数", len({r["指纹"] for r in rows}))
print("\n== 各指纹 ==")
for (fp, sz), g in sorted(grp.items(), key=lambda x: -len(x[1])):
    ex = next(r for r in rows if r["指纹"] == fp and r["尺寸"] == sz)
    print(fp, sz, "条数", len(g), "中位 %.1f" % st.median(g), "范围 %.1f–%.1f" % (min(g), max(g)), ex["主模型"][:40], "补丁" if ex["有块补丁"] else "", ex["前缀"])
print("\n== 异常 ==")
c = collections.Counter(a[1] for a in anom); print(c)
for r, rule, why in anom:
    print(r["prompt_id"][:8], rule, r["前缀"], r["尺寸"], why)
json.dump([dict(prompt_id=r["prompt_id"], 规则=rule, 说明=why, 前缀=r["前缀"], 指纹=r["指纹"]) for r, rule, why in anom],
          open(os.path.join(OUTD, "anomalies_trial.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
