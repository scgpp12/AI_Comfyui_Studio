# -*- coding: utf-8 -*-
# ComfyUI 管理：异常检测和待查表（设计书第四节）。只读 runs/runs.jsonl，写 anomalies/。
# 规则（阈值写进设计书 4.1）：
#   R1 同指纹慢：同「指纹＋尺寸键」至少 3 条，执行秒 > 组中位 × 2 且多出 ≥ 30 秒
#   R2 结构性慢：同主模型同尺寸，每步秒 > 不挂块补丁那些任务每步中位 × 3（基准至少 3 条）
#   R3 失败：状态不是 success
#   R4 空图空帧：输出质量闸不过
#   R5 反复装模型：同一批（同指纹、前后相隔 < 10 分钟）里连续 ≥ 3 条都从盘上重装同一个模型文件
#   R6 排队长：排队 > 60 秒（只记，不开单）
# 工单 anomalies/工单.json：一个原因（规则＋指纹＋尺寸）一张；人写的字段（状态、负责人、结论、调查记录、关单）保留不覆盖。
import json, os, sys, statistics as st, collections, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cm_common import BASE_DIR

RUNS_FILE = os.path.join(BASE_DIR, "runs", "runs.jsonl")
AD = os.path.join(BASE_DIR, "anomalies"); os.makedirs(os.path.join(AD, "调查"), exist_ok=True)
TICKETS = os.path.join(AD, "工单.json")
R1_X, R1_MIN_EXTRA, R2_X, MIN_BASE, R5_GAP_MIN, R5_RUN, R6_SEC = 2.0, 30, 3.0, 3, 10, 3, 60


def ts(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S") if s else None


def per_step(r):
    if r.get("每步秒"):
        return r["每步秒"]
    if r.get("执行秒") and r.get("步数"):
        return r["执行秒"] / r["步数"]
    return None


def hits(rows):
    H = []
    grp = collections.defaultdict(list)
    for r in rows:
        if r.get("执行秒") and r.get("状态") == "success":
            grp[(r["实例"], r["指纹"], r["尺寸键"])].append(r["执行秒"])
    fam = collections.defaultdict(list)
    for r in rows:
        s = per_step(r)
        if s and r.get("状态") == "success" and not r.get("有块补丁"):
            fam[(r["实例"], r["主模型"], r["尺寸键"])].append(s)
    for r in rows:
        pid = r["prompt_id"]
        if r.get("状态") != "success":
            H.append(dict(规则="R3", key="R3|%s|%s" % (r["实例"], r.get("指纹")), pid=pid, 说明="状态 %s；%s" % (r.get("状态"), json.dumps(r.get("错误"), ensure_ascii=False)[:200])))
            continue
        g = grp[(r["实例"], r["指纹"], r["尺寸键"])]
        if len(g) >= MIN_BASE and r["执行秒"] > R1_X * st.median(g) and r["执行秒"] - st.median(g) >= R1_MIN_EXTRA:
            H.append(dict(规则="R1", key="R1|%s|%s|%s" % (r["实例"], r["指纹"], r["尺寸键"]), pid=pid,
                          说明="执行 %.1f 秒，同指纹同尺寸中位 %.1f 秒（%d 条），%.1f 倍" % (r["执行秒"], st.median(g), len(g), r["执行秒"] / st.median(g))))
        s = per_step(r); f = fam.get((r["实例"], r["主模型"], r["尺寸键"]), [])
        if s and len(f) >= MIN_BASE and s > R2_X * st.median(f):
            H.append(dict(规则="R2", key="R2|%s|%s|%s" % (r["实例"], r["指纹"], r["尺寸键"]), pid=pid,
                          说明="每步 %.2f 秒，同主模型同尺寸不挂块补丁的每步中位 %.2f 秒（%d 条），%.1f 倍" % (s, st.median(f), len(f), s / st.median(f))))
        bad = [o for o in r.get("输出", []) if o.get("质量闸") and not o["质量闸"]["通过"]]
        if bad:
            H.append(dict(规则="R4", key="R4|%s|%s" % (r["实例"], r["指纹"]), pid=pid, 说明="；".join("%s：%s" % (o["文件"], o["质量闸"]["说明"]) for o in bad)))
        if r.get("排队秒") and r["排队秒"] > R6_SEC:
            H.append(dict(规则="R6", key=None, pid=pid, 说明="排队 %.1f 秒" % r["排队秒"]))
    # R5：按实例、时间排序，同指纹、相隔 < 10 分钟的连续段算一批
    rs = sorted([r for r in rows if r.get("开始")], key=lambda r: (r["实例"], r["开始"]))
    batch = []
    def flush(b):
        if len(b) < R5_RUN:
            return
        cnt = collections.Counter(m for r in b for m in set(r.get("从盘上装的模型", [])))
        rel = [m for m, c in cnt.items() if c >= R5_RUN and c >= len(b) - 1]
        if rel:
            for r in b:
                H.append(dict(规则="R5", key="R5|%s|%s" % (b[0]["实例"], b[0]["指纹"]), pid=r["prompt_id"],
                              说明="同一批 %d 条，每条都从盘上重装：%s" % (len(b), "、".join(sorted(rel)))))
    for r in rs:
        if batch and (r["实例"] != batch[-1]["实例"] or r["指纹"] != batch[-1]["指纹"] or ts(r["开始"]) - ts(batch[-1]["结束"] or batch[-1]["开始"]) > datetime.timedelta(minutes=R5_GAP_MIN)):
            flush(batch); batch = []
        batch.append(r)
    flush(batch)
    return H


def main():
    rows = []
    if os.path.exists(RUNS_FILE):
        rows = [json.loads(l) for l in open(RUNS_FILE, encoding="utf-8") if l.strip()]
    rows = [r for r in rows if "收集失败" not in r]
    byid = {r["prompt_id"]: r for r in rows}
    H = hits(rows)
    json.dump(H, open(os.path.join(AD, "命中.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    T = json.load(open(TICKETS, encoding="utf-8")) if os.path.exists(TICKETS) else {}
    today = datetime.date.today().strftime("%y%m%d")
    n_today = sum(1 for t in T.values() if t["单号"].startswith("A" + today))
    for h in H:
        if not h["key"]:
            continue
        t = T.get(h["key"])
        if not t:
            n_today += 1
            r = byid[h["pid"]]
            t = T[h["key"]] = dict(单号="A%s-%02d" % (today, n_today), 规则=h["规则"], 实例=r["实例"], 指纹=r["指纹"], 尺寸键=r.get("尺寸键"),
                                   文件名前缀=r.get("文件名前缀"), 首次发现=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 涉及=[],
                                   状态="待查", 负责人="模型学习频道", 结论="", 调查记录="", 关单="")
        if h["pid"] not in t["涉及"]:
            t["涉及"].append(h["pid"])
        t["最新说明"] = h["说明"]
    json.dump(T, open(TICKETS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 待查表.md
    L = ["# 异常待查表（自动生成，人写字段在 工单.json 里改）", "",
         "更新：%s。规则见设计书 4.1。状态：待查／调查中／已知原因／已解决／不处理。" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "",
         "| 单号 | 规则 | 实例 | 前缀 | 指纹 | 尺寸 | 涉及条数 | 最新说明 | 状态 | 结论 | 调查记录 |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in sorted(T.values(), key=lambda t: t["单号"]):
        L.append("| %s | %s | %s | %s | %s | %s | %d | %s | %s | %s | %s |" % (t["单号"], t["规则"], t["实例"], t.get("文件名前缀", ""), t["指纹"], t.get("尺寸键", ""),
                 len(t["涉及"]), t.get("最新说明", "").replace("|", "／"), t["状态"], t["结论"].replace("|", "／"), t["调查记录"]))
    r6 = [h for h in H if h["规则"] == "R6"]
    L += ["", "## 只记不开单：排队超过 %d 秒（R6）" % R6_SEC, ""] + ["- %s（%s）：%s" % (h["pid"][:8], byid[h["pid"]].get("文件名前缀", ""), h["说明"]) for h in r6]
    open(os.path.join(AD, "待查表.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("ANOMALY hits=%d tickets=%d open=%d" % (len(H), len(T), sum(1 for t in T.values() if t["状态"] in ("待查", "调查中"))), flush=True)


if __name__ == "__main__":
    main()
