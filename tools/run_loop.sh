#!/bin/bash
# ComfyUI 管理：临时常驻（不写 crontab、不建 systemd 服务，机器一重启就没了）。
# 用户在聊天里同意持久配置之前先这样跑；同意后换成用户 crontab：*/5 收集器、@reboot 显存采样。
# 用法：nohup setsid bash run_loop.sh > logs/run_loop.log 2>&1 &     停：kill $(cat run_loop.pid) $(cat gpu_sampler.pid)
D=/mnt/storage/model-lab/castsery/comfy_manage
cd $D/tools || exit 1
mkdir -p $D/logs
echo $$ > $D/run_loop.pid
# 显存采样：没在跑就拉起来
if ! { [ -f $D/gpu_sampler.pid ] && kill -0 "$(cat $D/gpu_sampler.pid)" 2>/dev/null; }; then
  nohup nice -n 19 python3 gpu_sampler.py >> $D/logs/gpu_sampler.log 2>&1 &
  echo $! > $D/gpu_sampler.pid
fi
while true; do
  date '+%F %T START'
  nice -n 19 ionice -c3 timeout 1200 python3 collector.py
  sleep 300
done
