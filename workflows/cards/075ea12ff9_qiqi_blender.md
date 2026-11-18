# qiqi_blender（指纹 075ea12ff9）

状态：待测　　类别：待定　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：未填
带说明画布：未填
速查表条目：未填
样板任务：388e7b5d-6d47-47c3-9fa6-e5af89eabf43（8188，2026-11-17 22:58:54）

## 机器统计（2026-11-18 12:40 自动生成）

- 模型文件：minimax_h3_audio_vae_fp32.safetensors、minimax_h3_fl2v_lightx2v_turbo_4step_v0.1_comfy_resized_avg_rank_21_bf16.safetensors、minimax_h3_fl2va_int8_convrot.safetensors、minimax_h3_video_vae_fp16.safetensors、qwen3vl_32b_minimax_h3_int8_convrot.safetensors
- 主模型：minimax_h3_fl2va_int8_convrot.safetensors；块补丁：无；步数：8
- 关键参数：`{"LoraLoaderModelOnly.strength_model": 0.65, "MiniMaxH3SigmaShift.shift_video": 12.0, "MiniMaxH3SigmaShift.shift_audio": 3.0, "CLIPLoader.device": "default", "BasicScheduler.scheduler": "simple", "BasicScheduler.steps": 8, "BasicScheduler.denoise": 1.0, "KSamplerSelect.sampler_name": "euler", "MiniMaxH3ReferenceToVideo.ref_image_size": "max"}`
- 跑过 2 次（失败 0、质量闸不过 0），提交者：模型学习

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| 1376x768x124 | 2 | 159.2（158.8–159.7） | 16.4 | 77231.0 | 72298.0 |

审查记录：无

异常单：无

<!-- 人写开始 -->
## 人写

用途：七七指屏路线 A：H3 首尾帧（fl2va int8 全量＋lightx2v turbo 0.65、SigmaShift 12/3、euler simple 8 步），钉首、中（62）、尾三帧，关键帧是 Qwen 2.1 照 Blender 深度出的。1376×768、124 帧。脚本 castsery/qiqi_blender/qb_vid.py A。

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：11-18 07:01–07:04 幕布打分：路线 A 8 分；B1 6 分、B2 6 分，B1、B2 的意见原话「人物动作僵硬 动作很缓慢的」。用户选路线 A。A 是三条里用户唯一给 8 分的。

测试总结（测过什么、结论、局限、和别的工作流比）：11-17 种子 999、7 各一条，执行约 159 秒、整卡峰值约 77GB。动作中间段是模型自己补的，抬手比 Blender 早、转头那几帧脸偏糊，但用户觉得动作自然，给 8 分（B1、B2 照 Blender 时间走反而被嫌僵、慢）。11-18 P0-D 用它合成地图：指尖只伸到大屏左边约 100 像素，地图对不上城市，已挂幕布让用户定改法。

分辨率和帧数规则（视频工作流照 index/视频模型_分辨率和帧数规则.md 对应模型一节写；出图写「不适用」）：
<!-- 人写结束 -->
