# lr_fr（指纹 b6aecb3008）

状态：待测　　类别：待定　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：未填
带说明画布：未填
速查表条目：未填
样板任务：7850fb00-84d4-468e-833f-faa670924034（8191，2026-11-18 12:35:12）

## 机器统计（2026-11-18 12:40 自动生成）

- 模型文件：Minimax-h3_Singularity_ref2va_Pruned_v1.3_int8.safetensors、face_yolov8n.pt、minimax_h3_audio_vae_fp32.safetensors、pika_h3_flex_turbo_8step_hd_ref2va.safetensors、qwen3vl_32b_minimax_h3_int8_convrot.safetensors、sam3.1_multiplex_fp16.safetensors、test_yz1114/minimax_h3_video_vae_int8_convrot.safetensors
- 主模型：Minimax-h3_Singularity_ref2va_Pruned_v1.3_int8.safetensors；块补丁：无；步数：8
- 关键参数：`{"BlockSparseAttention.start_percent": 0.2, "BlockSparseAttention.end_percent": 1.0, "LoraLoaderModelOnly.strength_model": 1.0, "CLIPLoader.device": "default", "MiniMaxH3ReferenceToVideo.ref_image_size": "match", "DifferentialDiffusion.strength": 1.0, "KSamplerSelect.sampler_name": "euler", "BasicScheduler.scheduler": "beta", "BasicScheduler.steps": 8, "BasicScheduler.denoise": 0.25, "VOSR2ModelLoader.dtype": "default"}`
- 跑过 2 次（失败 0、质量闸不过 0），提交者：模型学习

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| 768x768 | 2 | 140.2（129.2–151.3） | — | 63678.0 | 57942.0 |

审查记录：无

异常单：无

<!-- 人写开始 -->
## 人写

用途：

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：

测试总结（测过什么、结论、局限、和别的工作流比）：

分辨率和帧数规则（视频工作流照 index/视频模型_分辨率和帧数规则.md 对应模型一节写；出图写「不适用」）：
<!-- 人写结束 -->
