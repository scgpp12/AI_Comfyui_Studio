# -*- coding: utf-8 -*-
# ComfyUI 管理：后台慢慢算模型文件 md5（设计书第六节）。只读模型文件；按（真实路径、大小、修改时间）缓存，算过的不再算。
# 用 nice -n 19 ionice -c3 跑，不占 GPU。全部约 650 GB，一次跑不完没关系，下次接着算。
# 用法：nice -n 19 ionice -c3 python3 model_md5.py [最多算多少 GB，默认不限]
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cm_common import BASE_DIR, MODEL_EXT, md5_file

CACHE = os.path.join(BASE_DIR, "index", "models_md5_cache.json")
ROOTS = ["/mnt/storage/ComfyUI/models", "/mnt/storage/model-lab/learn_nodes"]
LIMIT = float(sys.argv[1]) * 1e9 if len(sys.argv) > 1 else float("inf")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
todo, seen = [], set()
for root in ROOTS:
    for dp, dns, fns in os.walk(root, followlinks=True):
        for fn in fns:
            if fn.lower().endswith(MODEL_EXT):
                p = os.path.join(dp, fn)
                try:
                    real = os.path.realpath(p); s = os.stat(p)
                except FileNotFoundError:
                    continue
                key = "%s|%d|%d" % (real, s.st_size, int(s.st_mtime))
                if key not in cache and real not in seen:
                    todo.append((s.st_size, key, real)); seen.add(real)
todo.sort()                                            # 小的先算
done = 0
for size, key, real in todo:
    if done + size > LIMIT:
        break
    t = time.time(); cache[key] = md5_file(real); done += size
    json.dump(cache, open(CACHE + ".tmp", "w"), indent=0); os.replace(CACHE + ".tmp", CACHE)
    print("MD5 %.1f GB %.0fs %s" % (size / 1e9, time.time() - t, real), flush=True)
print("MD5_DONE %.1f GB, 剩 %d 个" % (done / 1e9, len([1 for s, k, r in todo if k not in cache])), flush=True)
