# -*- coding: utf-8 -*-
# ComfyUI 管理：公用函数（指纹、取参数、只读 HTTP）。设计书：模型学习/ComfyUI管理/00_ComfyUI管理_设计书.md 第三节。
import json, hashlib, urllib.request, os

BASE_DIR = os.environ.get("CM_DIR", "/mnt/storage/model-lab/castsery/comfy_manage")
INSTANCES = {"8188": {"url": "http://127.0.0.1:8188", "root": "/mnt/storage/ComfyUI", "log": "journal:comfyui"},
             "8191": {"url": "http://127.0.0.1:8191", "root": "/mnt/storage/ComfyUI-test", "log": "file:/mnt/storage/model-lab/c8191.log"}}
MODEL_EXT = (".safetensors", ".pth", ".ckpt", ".gguf", ".pt", ".bin", ".onnx", ".sft")
VOLATILE = {"prompt", "text", "negative_prompt", "seed", "noise_seed", "filename_prefix", "image", "audio", "video", "string", "value"}
SIZE_KEYS = {"width", "height", "length", "batch_size"}
BLOCK_PATCH = {"QwenImageDiffsynthControlnet", "MiniMaxH3FunControlNetApply", "ControlNetApplyAdvanced", "ControlNetApply"}
PARAM_KEYS = {"steps", "cfg", "sampler_name", "scheduler", "denoise", "seed", "noise_seed", "strength", "strength_model", "start_percent",
              "end_percent", "transition_step", "lowres_scale", "resolution", "shift", "shift_video", "shift_audio", "sigmas", "width", "height",
              "length", "device", "dtype", "ref_image_size", "megapixels", "reference_latents_method", "conditioning_to_strength"}

# ---- 只读 HTTP：白名单之外的路径一律拒绝（设计书 9.3） ----
READ_ONLY_PATHS = ("/history", "/queue", "/system_stats", "/object_info")


def http_get(base, path, timeout=60):
    if not path.startswith(READ_ONLY_PATHS):
        raise RuntimeError("只读白名单之外的接口：" + path)
    return json.loads(urllib.request.urlopen(base + path, timeout=timeout).read() or b"{}")


# ---- 指纹 ----
def fingerprint(p):
    items = []
    for n in p.values():
        ins = []
        for k, v in sorted(n.get("inputs", {}).items()):
            if k in VOLATILE or k in SIZE_KEYS or k.startswith(("images.", "ref_images.", "ref_audios.")):
                continue
            if isinstance(v, list) and len(v) == 2 and str(v[0]) in p:
                ins.append((k, "<-%s#%s" % (p[str(v[0])]["class_type"], v[1])))
            elif isinstance(v, str) and len(v) > 200:
                continue
            else:
                ins.append((k, v))
        items.append(json.dumps([n["class_type"], ins], ensure_ascii=False, sort_keys=True, default=str))
    return hashlib.sha1("\n".join(sorted(items)).encode()).hexdigest()[:10]


def size_key(p):
    for n in p.values():
        i = n.get("inputs", {})
        if isinstance(i.get("width"), int) and isinstance(i.get("height"), int) and i["width"] > 0:
            return "%dx%d%s" % (i["width"], i["height"], ("x%d" % i["length"]) if isinstance(i.get("length"), int) else "")
    return "-"


def model_files(p):
    return sorted({v for n in p.values() for v in n.get("inputs", {}).values() if isinstance(v, str) and v.lower().endswith(MODEL_EXT)})


def main_model(p):
    for n in p.values():
        if n["class_type"] in ("UNETLoader", "CheckpointLoaderSimple") and n["class_type"] != "":
            v = n["inputs"].get("unet_name") or n["inputs"].get("ckpt_name")
            if isinstance(v, str):
                return v
    return "-"


def steps_of(p):
    for n in p.values():
        i = n.get("inputs", {})
        if n["class_type"] in ("KSampler", "KSamplerAdvanced", "BasicScheduler") and isinstance(i.get("steps"), int):
            return i["steps"]
        if n["class_type"] == "ManualSigmas" and isinstance(i.get("sigmas"), str):
            return len(i["sigmas"].split(",")) - 1
    return None


def key_params(p):
    out = {}
    for nid, n in p.items():
        for k, v in n.get("inputs", {}).items():
            if k in PARAM_KEYS and not isinstance(v, list):
                out.setdefault(n["class_type"] + "." + k, v)
    return out


def inputs_of(p):
    r = []
    for n in p.values():
        for k in ("image", "audio", "video"):
            v = n.get("inputs", {}).get(k)
            if n["class_type"].startswith("Load") and isinstance(v, str):
                r.append(v)
    return r


def prefix_of(p):
    for n in p.values():
        v = n.get("inputs", {}).get("filename_prefix")
        if isinstance(v, str):
            return v
    return ""


def has_block_patch(p):
    return any(n["class_type"] in BLOCK_PATCH for n in p.values())


def md5_file(path, chunk=1 << 22):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()
