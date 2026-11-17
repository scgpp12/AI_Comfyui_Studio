# -*- coding: utf-8 -*-
# ComfyUI 管理：把 comfy_manage 的产物拷进 GitHub 工作副本并脱敏（公开仓库 scgpp12/AI_Comfyui_Studio）。只拷文本，不拷权重、图片、视频。
# 脱敏照 AI_Weather_Studio 的 redact.py 思路：内网地址、个人目录名、端口清单段落替换掉；拷完自查，查到疑似秘密就整个退出、不留文件。
# 用法：python3 sync_repo.py      （只同步和脱敏，不 git add、不 commit、不 push；那三步人工做）
import os, re, shutil, sys, json, glob

SRC = "/mnt/storage/model-lab/castsery/comfy_manage"
REPO = "/mnt/storage/model-lab/AI_Comfyui_Studio"
# (源相对路径或 glob, 仓库里的目标目录)
ITEMS = [("00_ComfyUI管理_设计书.md", ""), ("00_ComfyUI规范_v1.1.md", ""), ("00_ComfyUI规范_v1.2.md", ""), ("00_ComfyUI规范_v1.3.md", ""), ("README.md", ""),
         ("tools/*.py", "tools"), ("tools/*.sh", "tools"),
         ("workflows/总表.md", "workflows"), ("workflows/cards/*.md", "workflows/cards"),
         ("index/*.md", "index"), ("index/前缀表.json", "index"), ("index/指纹名.json", "index"), ("index/models.jsonl", "index"),
         ("reviews/*.md", "reviews"), ("anomalies/待查表.md", "anomalies"), ("anomalies/工单.json", "anomalies"), ("anomalies/调查/*.md", "anomalies/调查"),
         ("runs/runs.jsonl", "runs"), ("试算_1117/trial.py", "试算_1117"), ("试算_1117/runs_trial.json", "试算_1117"), ("试算_1117/anomalies_trial.json", "试算_1117")]
TEXT_EXT = (".md", ".py", ".sh", ".json", ".jsonl")
REDACT = [(re.compile(r"\b10\.32\.\d{1,3}\.\d{1,3}\b"), "<内网地址>"),
          (re.compile(r"\b192\.168\.\d{1,3}\.\d{1,3}\b"), "<内网地址>"),
          (re.compile(r"/home/<用户>\b"), "/home/<用户>"),
          (re.compile(r"\bC:\\\\?Users\\\\?sons\b"), r"C:\\Users\\<用户>"),
          (re.compile(r"[\w.+-]+@gmail\.com"), "<邮箱>"),
          # 设计书里列了一串内网服务端口，整句换掉
          (re.compile(r"内网端口和服务清单"), "内网端口和服务清单")]
SECRET = re.compile(r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|password\s*[:=]\s*\S+)", re.I)

copied, hits = [], []
for pat, dst in ITEMS:
    for src in sorted(glob.glob(os.path.join(SRC, pat))):
        rel = os.path.join(dst, os.path.basename(src)); out = os.path.join(REPO, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        t = open(src, encoding="utf-8").read()
        for rx, rp in REDACT:
            t = rx.sub(rp, t)
        for m in SECRET.finditer(t):
            hits.append((rel, m.group(0)[:12] + "…"))
        open(out, "w", encoding="utf-8").write(t); copied.append(rel)
if hits:
    for rel in copied:
        os.remove(os.path.join(REPO, rel))
    print("SECRET_FOUND，已撤回本次拷贝：", hits); sys.exit(2)
left = []
for rel in copied:
    t = open(os.path.join(REPO, rel), encoding="utf-8").read()
    if re.search(r"10\.32\.\d|/home/<用户>\b|@gmail\.com", t):
        left.append(rel)
print("SYNC_OK %d 个文件；脱敏后残留：%s" % (len(copied), left or "无"))
for rel in copied:
    print("  ", rel)
