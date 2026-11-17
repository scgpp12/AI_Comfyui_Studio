# -*- coding: utf-8 -*-
# 8188 工作流改名（11-17，用户 18:07「命名没有规则 要求中文 说明他是什么」并同意对照表；总督导派活）。
# 规则：文件夹「项目 → 出图/出视频」；文件名「做什么_用什么模型_补充」；内部代号不进名字。只 mv，不删；先 cp -a 整目录备份；mv -n 不覆盖；逐条断言。
import os, shutil, subprocess, sys, hashlib, json, datetime
W = "/mnt/storage/ComfyUI/user/default/workflows/"
BK = "/mnt/storage/ComfyUI/user/default/workflows_备份_1117/"
MAP = [
    ("AI_Weather/出视频/P0A_甲_A1_半身播报.json", "AI天气/出视频/主播半身播报_H3_甲版式绿幕抠像.json", "P0A 甲 A1"),
    ("AI_Weather/出视频/P0A_甲_A1_半身播报_注释版.json", "AI天气/出视频/主播半身播报_H3_甲版式绿幕抠像_带说明.json", "P0A 甲 A1（注释版）"),
    ("AI_Weather/出视频/P0A_乙_B1_半身播报.json", "AI天气/出视频/主播半身播报_H3_乙版式演播室大屏同出.json", "P0A 乙 B1"),
    ("AI_Weather/出视频/P0A_乙_B1_半身播报_注释版.json", "AI天气/出视频/主播半身播报_H3_乙版式演播室大屏同出_带说明.json", "P0A 乙 B1（注释版）"),
    ("AI_Weather/出图/H3Image_参考图出关键帧_注释版.json", "AI天气/出图/参考图出关键帧_H3Image_带说明.json", "H3 Image 关键帧（注释版）"),
    ("AI_Weather/出图/T0A_Qwen三图定妆_注释版.json", "AI天气/出图/主播定妆三视图_Qwen_带说明.json", "T0A（注释版）"),
    ("AI_Weather/出图/T0B_Qwen深度控制摆姿势_注释版.json", "AI天气/出图/照深度图摆姿势_Qwen_带说明.json", "T0B（注释版）"),
    ("AI_Weather/出图/GPT出图说明.md", "AI天气/出图/GPT出图用法说明.md", "GPT 出图说明"),
    ("Ideogram4_写实_去审查.json", "通用/出图/写实文生图_Ideogram4_无审查.json", ""),
    ("Qwen2.1_文生图.json", "通用/出图/文生图_Qwen2.1.json", ""),
    ("Qwen2.1_改图_带参考图.json", "通用/出图/带参考图改图_Qwen2.1.json", ""),
    ("Sulphur2_t2v_distilled.json", "通用/出视频/文生视频_Sulphur2_蒸馏快速版.json", ""),
    ("Sulphur2_i2v_distilled.json", "通用/出视频/图生视频_Sulphur2_蒸馏快速版.json", ""),
    ("Sulphur2_Vantage_full.json", "通用/出视频/图加音频生视频_Sulphur2_完整版.json", ""),
    ("YZ_H3_ultimate.json", "通用/出视频/多参考图视频音频生视频_H3_YZ万能版.json", ""),
]
def md5(p): return hashlib.md5(open(p, "rb").read()).hexdigest()
dry = "--dry" in sys.argv
# 1) 断言：旧名都在、新名都不在、目录里没有对照表以外的文件
have = sorted(os.path.relpath(os.path.join(d, f), W) for d, _, fs in os.walk(W) for f in fs)
assert sorted(o for o, _, _ in MAP) == have, ("目录和对照表不一致", have)
for o, n, _ in MAP:
    assert os.path.isfile(W + o), o
    assert not os.path.exists(W + n), "新名已存在：" + n
before = {o: md5(W + o) for o, _, _ in MAP}
if dry: print("DRY OK", len(MAP)); sys.exit(0)
# 2) 备份
assert not os.path.exists(BK), "备份目录已存在：" + BK
subprocess.run(["cp", "-a", W, BK], check=True)
for o, _, _ in MAP: assert md5(BK + o) == before[o], "备份不一致：" + o
# 3) 逐条 mv -n
for o, n, _ in MAP:
    os.makedirs(os.path.dirname(W + n), exist_ok=True)
    subprocess.run(["mv", "-n", W + o, W + n], check=True)
    assert os.path.isfile(W + n) and not os.path.exists(W + o), "mv 没命中：" + o
    assert md5(W + n) == before[o], "内容变了：" + n
# 4) 删空掉的旧文件夹（只删空目录）
for d in ("AI_Weather/出视频", "AI_Weather/出图", "AI_Weather"):
    if os.path.isdir(W + d) and not os.listdir(W + d): os.rmdir(W + d)
# 5) 对照表
lines = ["# 8188 工作流 旧名→新名对照（11-17）", "",
         "依据：用户 11-17 18:07「命名没有规则 要求中文 说明他是什么」，同意本表。规则：文件夹「项目 → 出图/出视频」；文件名「做什么_用什么模型_补充」；内部代号（P0A、T0B、甲乙）不进名字，记在这里和说明卡里。",
         "目录：sons02 /mnt/storage/ComfyUI/user/default/workflows/；改名前整目录备份在 workflows_备份_1117/。只 mv，内容 md5 改名前后一致。", "",
         "| 旧名 | 新名 | 内部代号 | md5 |", "|---|---|---|---|"]
lines += ["| %s | %s | %s | %s |" % (o, n, c or "—", before[o]) for o, n, c in MAP]
open(W + "旧名→新名对照.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
json.dump([dict(旧=o, 新=n, 代号=c, md5=before[o]) for o, n, c in MAP], open("/mnt/storage/model-lab/castsery/comfy_manage/index/工作流改名_1117.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("RENAME OK", len(MAP), md5(W + "旧名→新名对照.md"))
