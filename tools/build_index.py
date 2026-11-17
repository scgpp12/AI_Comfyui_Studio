# -*- coding: utf-8 -*-
# ComfyUI 管理：登记卡、总表、三张索引、模型清单（设计书第五、六节）。只读 runs/、模型目录、workflows 目录；写 workflows/、index/。
# 登记卡里「人写」那一段（<!-- 人写开始 --> 到 <!-- 人写结束 -->）保留不覆盖；机器那一段每次重写。
# 模型 md5：读 index/models_md5_cache.json（由 model_md5.py 后台慢慢算），没算到的写「待算」。
# 用法：python3 build_index.py
import json, os, sys, glob, statistics as st, collections, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cm_common import BASE_DIR, MODEL_EXT

RUNS_FILE = os.path.join(BASE_DIR, "runs", "runs.jsonl")
IDX = os.path.join(BASE_DIR, "index"); CARDS = os.path.join(BASE_DIR, "workflows", "cards")
os.makedirs(IDX, exist_ok=True); os.makedirs(CARDS, exist_ok=True)
NAMES = os.path.join(IDX, "指纹名.json")            # 人写：{指纹: {"短名":..,"类别":"出图/出视频","状态":"推荐/可用/待测/淘汰","注释版":..,"原件脚本":..,"速查表":..}}
MD5C = os.path.join(IDX, "models_md5_cache.json")
MODEL_ROOTS = ["/mnt/storage/ComfyUI/models", "/mnt/storage/model-lab/learn_nodes"]
WF_ROOTS = {"8188": "/mnt/storage/ComfyUI/user/default/workflows", "8191": "/mnt/storage/ComfyUI-test/user/default/workflows"}
NOW = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def load_runs():
    if not os.path.exists(RUNS_FILE):
        return []
    return [r for r in (json.loads(l) for l in open(RUNS_FILE, encoding="utf-8") if l.strip()) if "收集失败" not in r]


def med(v):
    v = [x for x in v if isinstance(x, (int, float))]
    return (round(st.median(v), 1), round(min(v), 1), round(max(v), 1)) if v else None


def scan_models():
    """模型目录清单：相对路径、大小、修改时间、是不是软链和指向。follow 软链目录，但同一个真实文件只记一次。"""
    cache = json.load(open(MD5C, encoding="utf-8")) if os.path.exists(MD5C) else {}
    out, seen_real = [], set()
    for root in MODEL_ROOTS:
        for dp, dns, fns in os.walk(root, followlinks=True):
            for fn in fns:
                if not fn.lower().endswith(MODEL_EXT):
                    continue
                p = os.path.join(dp, fn)
                try:
                    real = os.path.realpath(p); stt = os.stat(p)
                except FileNotFoundError:
                    out.append(dict(路径=p, 断链=True)); continue
                key = "%s|%d|%d" % (real, stt.st_size, int(stt.st_mtime))
                rec = dict(路径=p, 文件名=fn, 大小=stt.st_size, 修改=datetime.datetime.fromtimestamp(stt.st_mtime).strftime("%Y-%m-%d"),
                           软链=os.path.islink(p), 指向=real if real != p else None, md5=cache.get(key, "待算"), 重复真实文件=real in seen_real)
                seen_real.add(real); out.append(rec)
    return out


def main():
    R = load_runs()
    names = json.load(open(NAMES, encoding="utf-8")) if os.path.exists(NAMES) else {}
    T = json.load(open(os.path.join(BASE_DIR, "anomalies", "工单.json"), encoding="utf-8")) if os.path.exists(os.path.join(BASE_DIR, "anomalies", "工单.json")) else {}
    byfp = collections.defaultdict(list)
    for r in R:
        byfp[r["指纹"]].append(r)
    # ---- 新指纹自动登记「待测」 ----
    for fp, rs in byfp.items():
        if fp not in names:
            names[fp] = dict(短名=(rs[0].get("文件名前缀") or "未命名").split("/")[0], 类别="待定", 状态="待测", 注释版="", 原件脚本="", 速查表="")
    json.dump(names, open(NAMES, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # ---- 登记卡 ----
    for fp, rs in byfp.items():
        nm = names[fp]; path = os.path.join(CARDS, "%s_%s.md" % (fp, nm["短名"].replace("/", "_")))
        human = "## 人写\n\n用途：\n\n质量结论（写出处）：\n\n用户评价（从幕布抄：分数、原话、日期）：\n\n测试总结（测过什么、结论、局限、和别的工作流比）：\n"
        olds = glob.glob(os.path.join(CARDS, fp + "_*.md"))
        if olds:
            t = open(olds[0], encoding="utf-8").read()
            if "<!-- 人写开始 -->" in t:
                human = t.split("<!-- 人写开始 -->", 1)[1].split("<!-- 人写结束 -->", 1)[0].strip("\n")
            for o in olds:
                if o != path:
                    os.replace(o, path)                    # 短名改了就改文件名，人写内容带过去
        r0 = rs[-1]
        sizes = collections.defaultdict(list)
        for r in rs:
            sizes[r.get("尺寸键")].append(r)
        L = ["# %s（指纹 %s）" % (nm["短名"], fp), "",
             "状态：%s　　类别：%s　　（这两项和下面三项在 index/指纹名.json 里改）" % (nm["状态"], nm["类别"]),
             "原件脚本：%s" % (nm.get("原件脚本") or "未填"), "注释版画布：%s" % (nm.get("注释版") or "未填"), "速查表条目：%s" % (nm.get("速查表") or "未填"),
             "样板任务：%s（%s，%s）" % (r0["prompt_id"], r0["实例"], r0["开始"]), "",
             "## 机器统计（%s 自动生成）" % NOW, "",
             "- 模型文件：" + "、".join(r0.get("模型文件", [])),
             "- 主模型：%s；块补丁：%s；步数：%s" % (r0.get("主模型"), "有" if r0.get("有块补丁") else "无", r0.get("步数")),
             "- 关键参数：`%s`" % json.dumps({k: v for k, v in r0.get("关键参数", {}).items() if not k.endswith((".seed", ".noise_seed", ".width", ".height", ".length"))}, ensure_ascii=False)[:600],
             "- 跑过 %d 次（失败 %d、质量闸不过 %d），提交者：%s" % (len(rs), sum(1 for r in rs if r["状态"] != "success"),
                 sum(1 for r in rs for o in r.get("输出", []) if o.get("质量闸") and not o["质量闸"]["通过"]),
                 "、".join(sorted({(r["提交者"].get("频道") if r["提交者"].get("频道") != "未知" else "未知（按前缀推断：%s）" % r["提交者"].get("按前缀推断")) for r in rs}))),
             "", "| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |", "|---|---|---|---|---|---|"]
        for sz, g in sorted(sizes.items(), key=lambda x: -len(x[1])):
            m = med([r.get("执行秒") for r in g]); s = med([r.get("每步秒") for r in g])
            w = med([r.get("整卡显存峰值MiB") for r in g]); pp = med([r.get("进程显存峰值MiB") for r in g])
            L.append("| %s | %d | %s | %s | %s | %s |" % (sz, len(g), "%s（%s–%s）" % m if m else "—", s[0] if s else "—", w[0] if w else "没记", pp[0] if pp else "没记"))
        tk = [t for t in T.values() if t["指纹"] == fp]
        rv = sorted(os.path.basename(f) for f in glob.glob(os.path.join(BASE_DIR, "reviews", "*.md"))
                    if not os.path.basename(f).startswith("00_") and fp in open(f, encoding="utf-8").read())
        L += ["", "审查记录：" + ("、".join("[%s](../../reviews/%s)" % (x, x) for x in rv) if rv else "无")]
        L += ["", "异常单：" + ("、".join("%s（%s，%s）" % (t["单号"], t["规则"], t["状态"]) for t in tk) if tk else "无"), "",
              "<!-- 人写开始 -->", human, "<!-- 人写结束 -->", ""]
        open(path, "w", encoding="utf-8").write("\n".join(L))
    # ---- 总表 ----
    L = ["# 工作流总表（%s 自动生成）" % NOW, "", "按类别、状态排。点开登记卡看详情。", "",
         "| 类别 | 状态 | 短名 | 指纹 | 次数 | 执行秒中位 | 主模型 | 块补丁 | 异常单 |", "|---|---|---|---|---|---|---|---|---|"]
    order = {"推荐": 0, "可用": 1, "待测": 2, "淘汰": 3}
    for fp, rs in sorted(byfp.items(), key=lambda x: (names[x[0]]["类别"], order.get(names[x[0]]["状态"], 9), -len(x[1]))):
        nm = names[fp]; m = med([r.get("执行秒") for r in rs])
        L.append("| %s | %s | [%s](cards/%s_%s.md) | %s | %d | %s | %s | %s | %s |" % (nm["类别"], nm["状态"], nm["短名"], fp, nm["短名"].replace("/", "_"), fp, len(rs),
                 m[0] if m else "—", rs[-1].get("主模型"), "有" if rs[-1].get("有块补丁") else "无", "、".join(t["单号"] for t in T.values() if t["指纹"] == fp) or "无"))
    open(os.path.join(BASE_DIR, "workflows", "总表.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    # ---- 三张索引 ----
    m2w = collections.defaultdict(lambda: collections.defaultdict(int)); last = {}
    for r in R:
        for m in r.get("模型文件", []):
            m2w[m][r["指纹"]] += 1; last[m] = max(last.get(m, ""), r.get("开始") or "")
    L = ["# 模型→工作流（%s 自动生成）" % NOW, "", "| 模型文件 | 用到它的工作流（指纹：次数） | 最近一次 |", "|---|---|---|"]
    for m in sorted(m2w):
        L.append("| %s | %s | %s |" % (m, "、".join("%s %s：%d" % (names[f]["短名"], f, c) for f, c in m2w[m].items()), last[m]))
    open(os.path.join(IDX, "模型→工作流.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    L = ["# 工作流→模型（%s 自动生成）" % NOW, "", "| 工作流 | 指纹 | 模型文件 |", "|---|---|---|"]
    for fp, rs in byfp.items():
        L.append("| %s | %s | %s |" % (names[fp]["短名"], fp, "、".join(rs[-1].get("模型文件", []))))
    open(os.path.join(IDX, "工作流→模型.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    s2w = collections.defaultdict(lambda: collections.defaultdict(int))
    for r in R:
        sub = r["提交者"]
        key = sub.get("脚本") if sub.get("脚本") not in (None, "未知") else "未知（按前缀推断：%s）" % sub.get("按前缀推断")
        s2w[key][r["指纹"]] += 1
    L = ["# 脚本→工作流（%s 自动生成）" % NOW, "", "11-17 晚以前的任务没写提交脚本，按文件名前缀推断（index/前缀表.json）。", "", "| 提交脚本 | 工作流（指纹：次数） |", "|---|---|"]
    for s in sorted(s2w):
        L.append("| %s | %s |" % (s, "、".join("%s %s：%d" % (names[f]["短名"], f, c) for f, c in s2w[s].items())))
    open(os.path.join(IDX, "脚本→工作流.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    # ---- 模型清单 ----
    M = scan_models()
    used = set(m2w)
    with open(os.path.join(IDX, "models.jsonl"), "w", encoding="utf-8") as f:
        for m in M:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    byname = collections.defaultdict(set)
    for m in M:
        if not m.get("断链"):
            byname[m["文件名"]].add(m["大小"])
    tot = sum(m.get("大小", 0) for m in M if not m.get("断链") and not m.get("重复真实文件"))
    L = ["# 模型清单（%s 自动生成）" % NOW, "",
         "范围：%s。共 %d 个文件（同一个真实文件被软链指到多处的只算一次大小），合计 %.0f GB；断链 %d 个；md5 由后台慢慢算，没算到的写「待算」。" % (
             "、".join(MODEL_ROOTS), len(M), tot / 1e9, sum(1 for m in M if m.get("断链"))), "",
         "标记：「同名不同大小」「断链」「test_ 目录」「今天以来没用过」（只按收集器的运行记录判断，收集器 11-17 才开始，所以大多数都是没用过）。", "",
         "| 路径 | 大小 GB | 修改 | md5 | 软链 | 用过 | 标记 |", "|---|---|---|---|---|---|---|"]
    for m in sorted(M, key=lambda m: m["路径"]):
        if m.get("断链"):
            L.append("| %s | — | — | — | 断链 | — | 断链 |" % m["路径"]); continue
        tags = []
        if len(byname[m["文件名"]]) > 1: tags.append("同名不同大小")
        if "/test_" in m["路径"]: tags.append("test_ 目录")
        L.append("| %s | %.2f | %s | %s | %s | %s | %s |" % (m["路径"].replace("/mnt/storage/", ""), m["大小"] / 1e9, m["修改"], m["md5"] if m["md5"] == "待算" else m["md5"][:12],
                 ("→ " + m["指向"].replace("/mnt/storage/", "")) if m["软链"] or m["指向"] else "", "用过" if m["文件名"] in used else "—", "、".join(tags)))
    open(os.path.join(IDX, "模型清单.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("INDEX fps=%d cards=%d models=%d" % (len(byfp), len(glob.glob(os.path.join(CARDS, "*.md"))), len(M)), flush=True)


if __name__ == "__main__":
    main()
