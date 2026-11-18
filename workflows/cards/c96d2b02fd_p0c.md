# p0c（指纹 c96d2b02fd）

状态：待测　　类别：待定　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：未填
带说明画布：未填
速查表条目：未填
样板任务：621e749d-b974-4ae6-a146-2533b445ffd4（8188，2026-11-18 09:51:30）

## 机器统计（2026-11-18 12:40 自动生成）

- 模型文件：minimax_h3_audio_vae_fp32.safetensors、minimax_h3_fl2v_lightx2v_turbo_4step_v0.1_comfy_resized_avg_rank_21_bf16.safetensors、minimax_h3_fl2va_int8_convrot.safetensors、minimax_h3_video_vae_fp16.safetensors、qwen3vl_32b_minimax_h3_int8_convrot.safetensors
- 主模型：minimax_h3_fl2va_int8_convrot.safetensors；块补丁：无；步数：8
- 关键参数：`{"LoraLoaderModelOnly.strength_model": 0.65, "MiniMaxH3SigmaShift.shift_video": 12.0, "MiniMaxH3SigmaShift.shift_audio": 3.0, "CLIPLoader.device": "default", "MiniMaxH3ReferenceToVideo.ref_image_size": "max", "BasicScheduler.scheduler": "simple", "BasicScheduler.steps": 8, "BasicScheduler.denoise": 1.0, "KSamplerSelect.sampler_name": "euler"}`
- 跑过 12 次（失败 0、质量闸不过 0），提交者：模型学习

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| 1376x768x107 | 4 | 133.2（131.5–133.5） | 13.4 | 75819.0 | 70886.0 |
| 1376x768x124 | 3 | 153.8（153.1–153.8） | 15.7 | 78072 | 71886 |
| 1376x768x175 | 3 | 221.9（221.9–222.1） | 23.7 | 81862 | 76374 |
| 768x960x73 | 2 | 69.0（68.8–69.2） | — | 72058.0 | 66262.0 |

审查记录：无

异常单：A261118-01（R5，待查）

<!-- 人写开始 -->
## 人写

用途：

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：

测试总结（测过什么、结论、局限、和别的工作流比）：

分辨率和帧数规则（视频工作流照 index/视频模型_分辨率和帧数规则.md 对应模型一节写；出图写「不适用」）：
<!-- 人写结束 -->
