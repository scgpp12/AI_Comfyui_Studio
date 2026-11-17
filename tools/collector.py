# -*- coding: utf-8 -*-
# ComfyUI 管理：运行记录收集器（设计书第二节）。只读：GET /history、/system_stats；journalctl；读文件；ffmpeg。
# 不提交任务、不 /free、不中断。每条执行一行，追加写 runs/runs.jsonl，按 prompt_id 去重。
# 用法：python3 collector.py           收一次 8188、8191（没开的跳过），再重算异常（anomaly.py）
#       python3 collector.py --no-qc   不跑质量闸（补历史时也会跑，默认开）
import json, os, sys, time, datetime, subprocess, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/mnt/storage/model-lab/castsery")                 # comfy_safe.check_image / check_video
from cm_common import *

RUNS = os.path.join(BASE_DIR, "runs"); os.makedirs(RUNS, exist_ok=True)
RUNS_FILE = os.path.join(RUNS, "runs.jsonl")
GPU_DIR = os.path.join(BASE_DIR, "gpu_samples")
PREFIX_TABLE = os.path.join(BASE_DIR, "index", "前缀表.json")         # {"t0b/pose": "castsery/qiqi_anchor/t0b/gen_pose.py 或 gen_pair.py", ...}
QC = "--no-qc" not in sys.argv


def iso(ms):
    return datetime.datetime.fromtimestamp(ms / 1000).strftime("%Y-%m-%d %H:%M:%S") if ms else None


def seen_ids():
    s = set()
    if os.path.exists(RUNS_FILE):
        for l in open(RUNS_FILE, encoding="utf-8"):
            try:
                s.add(json.loads(l)["prompt_id"])
            except Exception:
                pass
    return s


# ---- 显存：按时间窗从 gpu_samples 取峰值；没有覆盖到就写「没记」，不估 ----
def vram_peak(port, t0, t1):
    if not (t0 and t1):
        return "没记", "没记"
    whole, proc, n = 0, 0, 0
    days = {datetime.datetime.fromtimestamp(t0 / 1000).strftime("%Y%m%d"), datetime.datetime.fromtimestamp(t1 / 1000).strftime("%Y%m%d")}
    first, last = None, None
    for d in sorted(days):
        f = os.path.join(GPU_DIR, d + ".jsonl")
        if not os.path.exists(f):
            continue
        for l in open(f):
            try:
                r = json.loads(l)
            except Exception:
                continue
            if t0 <= r["t"] <= t1:
                n += 1; whole = max(whole, r["used"]); first = first or r["t"]; last = r["t"]
                pid = r.get("ports", {}).get(port)
                if pid and pid in r.get("procs", {}):
                    proc = max(proc, r["procs"][pid])
    # 采样要覆盖这段执行的大部分（头尾各差不超过 10 秒）才算数
    if n == 0 or first - t0 > 10000 or t1 - last > 10000:
        return "没记", "没记"
    return whole, (proc if proc else "没记")


# ---- 日志：每步秒数、从盘上装了哪些模型 ----
STEP_RE = re.compile(r"(\d+)/(\d+) \[[\d:]+<[\d:]+,\s+([\d.]+)(s/it|it/s)\]")


def log_window(inst, t0, t1):
    src = INSTANCES[inst]["log"]
    if not (t0 and t1):
        return None, [], None
    if src.startswith("journal:"):
        a, b = "@%d" % (t0 // 1000 - 1), "@%d" % (t1 // 1000 + 2)
        txt = subprocess.run(["journalctl", "-u", src.split(":")[1], "-a", "--since", a, "--until", b, "--no-pager", "-o", "cat"],
                             capture_output=True, text=True, timeout=60).stdout.replace("\r", "\n")
    else:
        return None, [], "8191 日志没有时间戳，按时间窗对不上，没记"
    steps = [m for m in STEP_RE.finditer(txt) if m.group(1) == m.group(2)]
    sps = None
    if steps:
        v = float(steps[-1].group(3)); sps = round(v if steps[-1].group(4) == "s/it" else 1.0 / v, 3)
    loads = []
    for l in txt.splitlines():
        if "Model storage policy" in l and "paths=" in l:
            loads += re.findall(r"'([^']+)'", l.split("paths=", 1)[1])
    return sps, [os.path.basename(x) for x in loads], None


def submitter_of(extra, prefix):
    sub, scr = extra.get("submitter"), extra.get("script")
    if sub or scr:
        return dict(频道=sub or "未知", 脚本=scr or "未知", 来源="extra_data")
    guess = None
    if os.path.exists(PREFIX_TABLE):
        tbl = json.load(open(PREFIX_TABLE, encoding="utf-8"))
        for k in sorted(tbl, key=len, reverse=True):
            if prefix.startswith(k):
                guess = tbl[k]; break
    return dict(频道="未知", 脚本="未知", 来源="未写", 按前缀推断=guess)


def build(inst, pid, v):
    root = INSTANCES[inst]["root"]
    pr = v["prompt"]; p = pr[2]; extra = pr[3] if len(pr) > 3 and isinstance(pr[3], dict) else {}
    msg = {m[0]: m[1] for m in v.get("status", {}).get("messages", [])}
    t_sub = extra.get("create_time"); t0 = msg.get("execution_start", {}).get("timestamp")
    endm = msg.get("execution_success") or msg.get("execution_error") or msg.get("execution_interrupted") or {}
    t1 = endm.get("timestamp")
    err = None
    if "execution_error" in msg:
        e = msg["execution_error"]; err = dict(节点=e.get("node_type"), 类型=e.get("exception_type"), 消息=str(e.get("exception_message"))[:500])
    outs = []
    for o in v.get("outputs", {}).values():
        for k in ("images", "gifs", "videos", "audio"):
            for x in o.get(k, []):
                if not isinstance(x, dict) or x.get("type") != "output":
                    continue
                f = os.path.join(root, "output", x.get("subfolder", ""), x["filename"])
                rec = dict(文件=os.path.join(x.get("subfolder", ""), x["filename"]))
                if os.path.exists(f):
                    rec["大小"] = os.path.getsize(f); rec["md5"] = md5_file(f)
                    if QC and f.lower().endswith((".png", ".jpg", ".webp", ".mp4", ".webm", ".mov")):
                        from comfy_safe import check_image, check_video
                        ok, note = (check_video if f.lower().endswith((".mp4", ".webm", ".mov")) else check_image)(f)
                        rec["质量闸"] = dict(通过=ok, 说明=note)
                else:
                    rec["md5"] = "文件已不在"
                outs.append(rec)
    ins = []
    for name in inputs_of(p):
        f = os.path.join(root, "input", name)
        ins.append(dict(文件=name, md5=md5_file(f) if os.path.exists(f) else "文件已不在"))
    sps, loads, lognote = log_window(inst, t0, t1)
    whole, proc = vram_peak(inst, t0, t1)
    return dict(prompt_id=pid, 实例=inst, 提交时间=iso(t_sub), 开始=iso(t0), 结束=iso(t1),
                排队秒=round((t0 - t_sub) / 1000, 1) if t0 and t_sub else None,
                执行秒=round((t1 - t0) / 1000, 1) if t0 and t1 else None,
                状态=v.get("status", {}).get("status_str"), 错误=err,
                被缓存节点数=len(msg.get("execution_cached", {}).get("nodes", [])),
                指纹=fingerprint(p), 尺寸键=size_key(p), 主模型=main_model(p), 模型文件=model_files(p), 有块补丁=has_block_patch(p),
                步数=steps_of(p), 每步秒=sps, 从盘上装的模型=loads, 日志说明=lognote, 关键参数=key_params(p),
                参考输入=ins, 输出=outs, 文件名前缀=prefix_of(p), 提交者=submitter_of(extra, prefix_of(p)),
                整卡显存峰值MiB=whole, 进程显存峰值MiB=proc, 节点数=len(p), 收集时间=iso(int(time.time() * 1000)))


def collect():
    seen = seen_ids(); new = 0
    for inst, cfg in INSTANCES.items():
        try:
            http_get(cfg["url"], "/system_stats", timeout=5)
        except Exception:
            print("SKIP", inst, "没开", flush=True); continue
        h = http_get(cfg["url"], "/history?max_items=10000", timeout=120)
        items = sorted(h.items(), key=lambda kv: (kv[1]["prompt"][3] or {}).get("create_time", 0) if len(kv[1]["prompt"]) > 3 else 0)
        for pid, v in items:
            if pid in seen or not v.get("status", {}).get("completed", True) and not v.get("status", {}).get("messages"):
                continue
            try:
                rec = build(inst, pid, v)
            except Exception as e:
                rec = dict(prompt_id=pid, 实例=inst, 收集失败=repr(e)[:500])
            with open(RUNS_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            seen.add(pid); new += 1
    print("COLLECT_DONE new=%d total=%d at %s" % (new, len(seen), iso(int(time.time() * 1000))), flush=True)
    return new


if __name__ == "__main__":
    collect()
    import anomaly
    anomaly.main()
