# -*- coding: utf-8 -*-
# 规范 v1.5 第 32 条：给用到视频模型的工作流登记卡人写部分加「分辨率和帧数规则」一栏；viggle 卡顺带填用途和测试总结。
# 只改 <!-- 人写开始 --> 到 <!-- 人写结束 --> 之间；已有这一栏的卡不动；每张卡先备份到 cards_备份_1117v15/。
import os, glob, shutil, sys
D = "/mnt/storage/model-lab/castsery/comfy_manage/workflows/cards"
BK = "/mnt/storage/model-lab/castsery/comfy_manage/workflows/cards_备份_1117v15"
R = "index/视频模型_分辨率和帧数规则.md"
VIG = ("分辨率和帧数规则（viggle，详见 %s「viggle 换人」一节）：short_edge 480–736（节点第 72 行）；24fps；17n+5、90–345 帧；"
       "736 下 192 帧能跑、294 帧 OOM，480 下 294 帧能跑；脸宽（原尺寸）736 全身约 41 像素正常、480 全身约 26 像素画坏，超分到 1080 后约 60 像素；"
       "真人全身正面要看清脸用 736、按切点分段每段约 192 帧以内（规范第 26 条）；交片 RIFE 插到 96 再按原片帧率取（qd_30.py）。" % R)
FL = ("分辨率和帧数规则（H3 fl2va，详见 %s「H3 fl2va」一节）：原生短边 768、面积约 768×1344（节点不强制）；24fps；17k+5，训练范围约 124–362 帧；"
      "能跑 124、243 帧，FaceRefine 画布 768 每块 93 帧能跑；OOM 帧数未测；脸要多大未测；交片 RIFE 插到 96 再按原片帧率取。" % R)
RF = ("分辨率和帧数规则（H3 Ref2V，详见 %s「H3 Ref2V」一节）：原生短边 768、面积约 768×1344（节点不强制）；24fps；17k+5，训练范围约 124–362 帧；"
      "OOM 帧数未测；脸要多大未测；交片 RIFE 插到 96 再按原片帧率取。" % R)
FR_NOTE = "FaceRefine 只能改脸部细节，改不了嘴型和表情；结构画坏了回换人那步重做（规范第 27 条；舞蹈换七七 v2–v4 量过，嘴张开、嘴宽只差 1–3%）。"
CARDS = {
    "3fd26fa7ce": (VIG, "舞蹈换七七：正面段（4.23 秒切点到片尾）viggle 换人，short_edge 736、竖屏 736×1280、179 帧（跑 192 帧）。脚本 castsery/qiqi_dance/qd_vg_seg.py。",
                   "11-17 一次，执行 581 秒、整卡峰值约 83GB。对比 480 整条（f77bffbbe6）：嘴角拉到脸颊、鼻孔大、脸扁都好了，像七七 0.187→0.327（cmp_736.py，对照图 出片/对照_480对736_*.jpg）。用这段做成 v5 成片（自评 7.5）。局限：唱歌段嘴仍张开；刚转正面的一两帧侧脸偏糊。"),
    "f77bffbbe6": (VIG, "舞蹈换七七：整条 294 帧 viggle 换人，short_edge 480、竖屏 480×832。脚本 castsery/qiqi_dance/qd_vg.py（参数：重画帧 种子 short_edge）。",
                   "11-17 三次（种子 0、1 等），执行约 287 秒、整卡峰值约 71GB，都能跑完。结论：全身景脸宽只有约 26 像素，嘴角拉到脸颊、鼻孔大、脸扁，修脸改不动；真人全身正面要看清脸的镜头不要用 480，改用 736 分段（3fd26fa7ce）。背面、没有脸的镜头可以用。"),
    "3c640da60d": (VIG, "舞蹈换七七：整条 294 帧 short_edge 736 试跑。",
                   "11-17 一次，显存不够（prompt 773be809，工单 A261117-11：已占 33.8GB、还要约 9GB、CUDA 只剩 26.8GB）。结论：736 不要整条跑，按切点分段，每段约 192 帧以内。"),
    "ce371d4395": (VIG, "舞蹈换七七 viggle 换人的一次早期提交。", "11-17 一次，1.3 秒就失败（工单 A261117-09，已关单）。不是可用工作流，留作记录。"),
    "5c67ba3472": (FL, None, None), "d4dd97bd66": (FL, None, None), "45d390a4d1": (FL, None, None),
    "923fbd0250": (FL, None, None), "7b9e8c21a3": (FL, None, None),
    "aff1833d69": (RF, None, None), "113245bfad": (RF, None, None),
    "c131a344ac": (RF, None, None), "90b0f2d0bb": (RF, None, None), "30dfe9f406": (RF, None, None), "c7a09880bb": (RF, None, None),
}
FR_CARDS = {"5c67ba3472", "d4dd97bd66", "45d390a4d1"}
os.makedirs(BK, exist_ok=True); changed = []
for fp, (rule, use, summ) in CARDS.items():
    ps = glob.glob(os.path.join(D, fp + "_*.md")); assert len(ps) == 1, (fp, ps); p = ps[0]
    t = open(p, encoding="utf-8").read()
    a, rest = t.split("<!-- 人写开始 -->", 1); h, b = rest.split("<!-- 人写结束 -->", 1)
    if "分辨率和帧数规则" in h:
        print("SKIP", fp); continue
    if use:
        assert "\n用途：\n" in h, fp; h = h.replace("\n用途：\n", "\n用途：" + use + "\n", 1)
    if summ:
        k = "\n测试总结（测过什么、结论、局限、和别的工作流比）：\n"
        assert k in h, fp; h = h.replace(k, k.rstrip("\n") + summ + "\n", 1)
    if fp in FR_CARDS:
        k = "\n质量结论（写出处）：\n"
        assert k in h, fp; h = h.replace(k, k.rstrip("\n") + FR_NOTE + "\n", 1)
    h = h.rstrip("\n") + "\n\n" + rule + "\n"
    shutil.copy2(p, os.path.join(BK, os.path.basename(p)))
    open(p, "w", encoding="utf-8").write(a + "<!-- 人写开始 -->" + h + "<!-- 人写结束 -->" + b); changed.append(os.path.basename(p))
print("CHANGED", len(changed)); [print("  ", c) for c in changed]
