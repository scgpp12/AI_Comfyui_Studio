# -*- coding: utf-8 -*-
# ComfyUI 管理：显存采样（设计书 2.1「显存峰值」）。只读：nvidia-smi --query-*、ss -ltnp。不碰 GPU 计算。
# 每 INTERVAL 秒一行，写 gpu_samples/YYYYMMDD.jsonl：{t: 毫秒时间戳, used: 整卡已用 MiB, total, procs: {pid: MiB}, ports: {"8188": pid, "8191": pid}}
# 用法：python3 gpu_sampler.py          （常驻；由 run_loop.sh 或以后的 cron @reboot 拉起）
import json, os, subprocess, time, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cm_common import BASE_DIR

INTERVAL = 3
OUT = os.path.join(BASE_DIR, "gpu_samples"); os.makedirs(OUT, exist_ok=True)


def q(args):
    return subprocess.run(args, capture_output=True, text=True, timeout=20).stdout


def ports():
    r = {}
    for l in q(["ss", "-ltnp"]).splitlines():
        for port in ("8188", "8191"):
            if (":%s " % port) in l and "pid=" in l:
                r[port] = l.split("pid=")[1].split(",")[0]
    return r


last_ports, last_pt = {}, 0
while True:
    try:
        t = int(time.time() * 1000)
        g = q(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"]).strip().splitlines()[0].split(",")
        procs = {}
        for l in q(["nvidia-smi", "--query-compute-apps=pid,used_memory", "--format=csv,noheader,nounits"]).splitlines():
            a = [x.strip() for x in l.split(",")]
            if len(a) == 2 and a[1].isdigit():
                procs[a[0]] = int(a[1])
        if time.time() - last_pt > 60:
            last_ports, last_pt = ports(), time.time()
        rec = dict(t=t, used=int(g[0]), total=int(g[1]), procs=procs, ports=last_ports)
        day = datetime.datetime.fromtimestamp(t / 1000).strftime("%Y%m%d")
        with open(os.path.join(OUT, day + ".jsonl"), "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        print("SAMPLE_ERR", repr(e)[:200], flush=True)
    time.sleep(INTERVAL)
