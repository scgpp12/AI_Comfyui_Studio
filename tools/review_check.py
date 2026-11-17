# -*- coding: utf-8 -*-
# 开跑前审查的机器部分（规范 v1.2）：读一份 API 格式的工作流 JSON（或一个脚本 dry-run 存下的 *_api.json），
# 算指纹、列模型和关键参数，并自动判几条能机器判的规则（4、5、7、10、11 的一部分）。其余条目由审查人对着脚本逐条打勾。
# 只读文件，不连 ComfyUI、不提交任务。
# 用法：python3 review_check.py 工作流_api.json [脚本.py]
import json, sys, os, re, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cm_common import fingerprint, size_key, model_files, main_model, steps_of, key_params, has_block_patch, BLOCK_PATCH

p = json.load(open(sys.argv[1], encoding="utf-8")); p.pop("_meta", None)
script = open(sys.argv[2], encoding="utf-8").read() if len(sys.argv) > 2 else ""
out = []
def add(rule, ok, note):
    out.append("| %s | %s | %s |" % (rule, {True: "过", False: "**不过**", None: "人工看"}[ok], note))

models = model_files(p); cls = [n["class_type"] for n in p.values()]
is_h3 = any("minimax_h3" in m.lower() or "minimax-h3" in m.lower() for m in models)
enc = [n["inputs"].get("clip_name") for n in p.values() if n["class_type"] == "CLIPLoader"]
if is_h3:
    add(4, all(e == "qwen3vl_32b_minimax_h3_int8_convrot.safetensors" for e in enc if e and "qwen3vl_32b" in e) and any(e and "int8_convrot" in e for e in enc),
        "文字编码器：%s" % "、".join(str(e) for e in enc))
else:
    add(4, None, "不是 H3；编码器 %s，对照模型配套表" % "、".join(str(e) for e in enc))
cfgs = [n["inputs"].get("cfg") for n in p.values() if isinstance(n["inputs"].get("cfg"), (int, float))]
add(5, all(abs(c - 1.0) < 1e-6 for c in cfgs) if cfgs else None, "cfg：%s" % (cfgs or "无 cfg 输入（BasicGuider 等于 1）"))
add(7, not any("test_" in m for m in models), "模型：%s" % "、".join(models))
lens = [n["inputs"].get("length") for n in p.values() if isinstance(n["inputs"].get("length"), int)]
wh = [(n["inputs"].get("width"), n["inputs"].get("height")) for n in p.values() if isinstance(n["inputs"].get("width"), int)]
ok10 = all(l % 17 == 5 and 124 <= l <= 362 for l in lens) and all(w % 16 == 0 and h % 16 == 0 for w, h in wh)
add(10, ok10 if (lens or wh) else None, "帧数 %s；画布 %s（H3 源码训练范围 124–362 帧；原生短边 768、最大 768×1344）" % (lens or "—", wh or "—"))
nref = sum(1 for c in cls if c == "LoadImage")
if has_block_patch(p):
    add(11, nref <= 2, "挂了块补丁插件（%s），LoadImage %d 个（含控制图）；照某人摆姿势首选 H3 Image，非用不可只喂 1 张参考图" % (
        "、".join(sorted(set(c for c in cls if c in BLOCK_PATCH))), nref))
else:
    add(11, True, "没挂块补丁插件")
if script:
    add(8, "/upload/image" in script or "comfy_safe" in script, "脚本里%s走 /upload/image 或 comfy_safe" % ("有" if ("/upload/image" in script or "comfy_safe" in script) else "没有"))
    per_free = bool(re.search(r"def run\(.*?\n(?:.*\n){0,60}?.*\"/free\"", script))
    add(13, ("batch_free" in script) or not per_free, "脚本里%s" % ("用 batch_free" if "batch_free" in script else ("在 run() 里调 /free（每条都释放）" if per_free else "没看到逐条 /free")))
    add(15, "wait_free" in script, "起跑前量显存：%s" % ("有 wait_free" if "wait_free" in script else "没看到"))
    add(16, ("check_image" in script) or ("check_video" in script), "质量闸：%s" % ("有" if ("check_image" in script or "check_video" in script) else "没看到"))
    add(17, "Comfy(" in script or "timeout" in script, "等结果超时：%s" % ("用 comfy_safe.Comfy.run" if "Comfy(" in script else "要人工看循环有没有上限"))
    add(23, "submitter" in script, "extra_data：%s" % ("写了 submitter" if "submitter" in script else "没看到 submitter"))
print("指纹：%s　尺寸键：%s　主模型：%s　步数：%s　块补丁：%s" % (fingerprint(p), size_key(p), main_model(p), steps_of(p), "有" if has_block_patch(p) else "无"))
print("关键参数：" + json.dumps(key_params(p), ensure_ascii=False)[:800])
print("\n| 条 | 机器判 | 说明 |\n|---|---|---|")
print("\n".join(out))
