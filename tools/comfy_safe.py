# -*- coding: utf-8 -*-
# ComfyUI 提交工具（11-17，模型学习频道，照规范 v1 改）。给 p0a_run_v2.py、h3i_kf_v2.py 等脚本 import 用。
# 管三件事（规范 v1）：
#   第 8 条  参考图、参考声走 /upload/image 上传，用服务器返回的 name；不再直接拷进 input 目录（同名会被静默复用）。
#   第 13 条 不在每条任务前后 /free；只在一批开始前、整批结束后各释放一次（batch_free）。
#   第 17 条 等结果的循环有总等待上限，超时记 FAIL、继续下一条（wait_result）。
# 11-17 晚补两件（总督导要求）：
#   第 15 条 起跑前量整卡空闲，不够就等、等满上限报错（wait_free）。门槛：一般 36000 MiB；独占整卡的作业另设（见各脚本）。
#   第 16 条 出完查灰图、黑帧（check_image / check_video）：取灰度算整张标准差，小于 3 判空图；
#            全黑也算失败（采样出 NaN 时解码出来通常是全黑或全灰，存成 png/mp4 后像素里不会有 NaN 这个值，所以靠「标准差太小」一起拦）；
#            视频抽首、中、尾三帧，任一帧不过就判失败。
# 只用标准库加系统里的 ffmpeg、ffprobe、nvidia-smi（sons02 系统 python 没有 numpy）。上传用 multipart/form-data，字段名照 ComfyUI server.py。
import json, os, sys, time, uuid, hashlib, subprocess, urllib.request, urllib.error

GENERAL_FREE_MIB = 36000          # 规矩：空闲不到 36000 MiB 就等（记忆 gpu-self-measure-35gb）
BLANK_STD = 3.0                   # 审查 B Q2：整张灰度标准差小于 3 判空图


# ---------- 第 15 条：起跑前量空闲 ----------
def gpu_free_mib(smi=None):
    """整卡空闲 MiB＝total − used（nvidia-smi）。smi 可传入假函数做离线测试。"""
    out = smi() if smi else subprocess.run(["nvidia-smi", "--query-gpu=memory.total,memory.used", "--format=csv,noheader,nounits"],
                                           capture_output=True, text=True, timeout=30).stdout
    total, used = [int(x) for x in out.strip().splitlines()[0].split(",")]
    return total - used


def wait_free(need_mib=GENERAL_FREE_MIB, max_wait_sec=1800, poll_sec=30, smi=None):
    """空闲够了就返回当时的空闲 MiB；不够就每 poll_sec 秒再量一次，等满 max_wait_sec 抛 RuntimeError（调用方记 FAIL 或停批）。"""
    t0 = time.time()
    while True:
        f = gpu_free_mib(smi)
        if f >= need_mib:
            print("VRAM_OK free=%d need=%d" % (f, need_mib), flush=True)
            return f
        if time.time() - t0 >= max_wait_sec:
            raise RuntimeError("vram_wait_timeout free=%d need=%d waited=%ds" % (f, need_mib, int(time.time() - t0)))
        print("VRAM_WAIT free=%d need=%d" % (f, need_mib), flush=True)
        time.sleep(poll_sec)


# ---------- 第 16 条：出完查灰图、黑帧 ----------
def _gray_std(raw):
    """8 位灰度字节串的均值和标准差（纯 Python，一张 1920×1088 约零点几秒）。"""
    n = len(raw)
    if n == 0:
        return 0.0, 0.0
    s = sum(raw); mean = s / n
    sq = sum(v * v for v in raw)
    return mean, max(sq / n - mean * mean, 0.0) ** 0.5


def _frame_gray(path, t=None):
    """用 ffmpeg 取一帧（图片就是那一张）转 8 位灰度原始像素。"""
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", "%.3f" % t] if t is not None else []) + ["-i", path, "-frames:v", "1", "-vf", "format=gray", "-f", "rawvideo", "-"]
    return subprocess.run(cmd, capture_output=True, timeout=120).stdout


def check_image(path):
    """返回 (是否通过, 说明)。不过：读不出像素、标准差 < 3（空图、全灰、全黑）。"""
    raw = _frame_gray(path)
    if not raw:
        return False, "读不出像素"
    mean, std = _gray_std(raw)
    if std < BLANK_STD:
        return False, "空图（灰度均值 %.1f、标准差 %.2f）" % (mean, std)
    return True, "灰度均值 %.1f、标准差 %.1f" % (mean, std)


def check_video(path):
    """抽首、中、尾三帧，每帧做 check_image 的判断；任一帧不过就不通过。"""
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, timeout=60).stdout.strip()
    try:
        dur = float(d)
    except ValueError:
        return False, "读不出时长"
    notes = []
    for name, t in (("首", 0.0), ("中", dur / 2), ("尾", max(dur - 0.1, 0.0))):
        raw = _frame_gray(path, t)
        if not raw:
            return False, "%s帧读不出像素" % name
        mean, std = _gray_std(raw)
        if std < BLANK_STD:
            return False, "%s帧是空帧（灰度均值 %.1f、标准差 %.2f）" % (name, mean, std)
        notes.append("%s %.1f" % (name, std))
    return True, "三帧标准差 " + "、".join(notes)


class Comfy:
    def __init__(self, base, timeout_sec=1200, poll_sec=2, submitter="未知", script=None):
        self.base = base.rstrip("/")          # 例："http://127.0.0.1:8188"
        # 谁提交的（ComfyUI 管理设计书 2.1）：写进 /prompt 的 extra_data，会原样存进 /history，收集器靠它认提交者
        self.submitter = submitter            # 频道名，例："模型学习"
        self.script = script or os.path.abspath(sys.argv[0])
        self.timeout_sec = timeout_sec        # 单条任务最长等多久（默认 20 分钟，审查 B 的建议值）
        self.poll_sec = poll_sec

    # ---------- 基础请求 ----------
    def post_json(self, path, data, timeout=120):
        r = urllib.request.Request(self.base + path, data=json.dumps(data).encode(), headers={"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(r, timeout=timeout).read() or b"{}")

    def get_json(self, path, timeout=60):
        return json.loads(urllib.request.urlopen(self.base + path, timeout=timeout).read() or b"{}")

    # ---------- 第 8 条：上传 ----------
    def upload(self, path, prefix="up"):
        """上传一张图或一段音频到 input/，返回服务器给的文件名（可能被改名，必须用它）。
        文件名先按内容 md5 前 12 位起，内容一样的重复上传服务器会认成同一张；内容不同同名时服务器会自动改名。"""
        data = open(path, "rb").read()
        name = "%s_%s%s" % (prefix, hashlib.md5(data).hexdigest()[:12], os.path.splitext(path)[1].lower())
        b = uuid.uuid4().hex
        body = (("--%s\r\nContent-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: application/octet-stream\r\n\r\n" % (b, name)).encode()
                + data + ("\r\n--%s\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\ninput\r\n"
                          "--%s\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\nfalse\r\n--%s--\r\n" % (b, b, b)).encode())
        r = urllib.request.Request(self.base + "/upload/image", data=body, headers={"Content-Type": "multipart/form-data; boundary=" + b})
        res = json.loads(urllib.request.urlopen(r, timeout=300).read())
        got = (res.get("subfolder") + "/" if res.get("subfolder") else "") + res["name"]
        return got

    # ---------- 第 13 条：一批只释放两次 ----------
    def batch_free(self, why=""):
        """只在一批开始前、整批结束后调用；批内条与条之间不要调。"""
        try:
            self.post_json("/free", {"unload_models": True, "free_memory": True})   # 两个键默认都是 false，必须写明
            time.sleep(3)
            print("FREE", why, flush=True)
        except Exception as e:
            print("FREE_FAIL", why, repr(e)[:200], flush=True)

    # ---------- 第 17 条：提交并等结果，有超时 ----------
    def run(self, graph):
        """提交 API 图，等它出结果。返回 (prompt_id, history 条目)；失败或超时抛 RuntimeError，由调用方记 FAIL。"""
        r = self.post_json("/prompt", {"prompt": graph, "client_id": str(uuid.uuid4()),
                                       "extra_data": {"submitter": self.submitter, "script": self.script}})
        if r.get("node_errors"):
            raise RuntimeError("node_errors " + json.dumps(r["node_errors"], ensure_ascii=False)[:1200])
        if "prompt_id" not in r:
            raise RuntimeError("submit_fail " + json.dumps(r, ensure_ascii=False)[:1200])
        pid = r["prompt_id"]
        h = self.wait_result(pid)
        if h["status"].get("status_str") != "success":
            raise RuntimeError("run_fail " + json.dumps(h["status"], ensure_ascii=False)[:1200])
        return pid, h

    def wait_result(self, pid):
        t0 = time.time()
        while True:
            if time.time() - t0 > self.timeout_sec:
                # 超时：只取消自己这一条（不发全局中断），再报错让调用方记 FAIL、继续下一条
                try:
                    self.post_json("/interrupt", {"prompt_id": pid})
                    self.post_json("/queue", {"delete": [pid]})
                except Exception:
                    pass
                raise RuntimeError("timeout %d s, prompt_id %s" % (self.timeout_sec, pid))
            try:
                h = self.get_json("/history/" + pid, timeout=30)
            except (urllib.error.URLError, OSError):
                h = {}                     # 服务一时连不上：继续等，由总上限兜底
            if pid in h:
                return h[pid]
            time.sleep(self.poll_sec)

    @staticmethod
    def outputs(h, exts=(".png", ".mp4")):
        """从 /history 条目里取输出文件（相对 output 目录的路径），不靠猜文件名。"""
        fs = []
        for o in h.get("outputs", {}).values():
            for k in ("images", "gifs", "videos"):
                for x in o.get(k, []):
                    if x["filename"].lower().endswith(exts):
                        fs.append(os.path.join(x.get("subfolder", ""), x["filename"]))
        return fs
