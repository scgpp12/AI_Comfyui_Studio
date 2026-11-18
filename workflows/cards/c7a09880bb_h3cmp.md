# h3cmp（指纹 c7a09880bb）

状态：待测　　类别：待定　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：未填
带说明画布：未填
速查表条目：未填
样板任务：e5d7b9d4-4fba-4b16-be2e-343a25909282（8188，2026-11-17 17:47:32）

## 机器统计（2026-11-18 12:15 自动生成）

- 模型文件：Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors、minimax_h3_audio_vae_fp32.safetensors、minimax_h3_latent_upscaler_3d_conv_v1_fp16.safetensors、minimax_h3_video_vae_fp16.safetensors、qwen3vl_32b_minimax_h3_int8_convrot.safetensors
- 主模型：Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors；块补丁：无；步数：8
- 关键参数：`{"MiniMaxH3ReferenceToVideo.ref_image_size": "match", "KSamplerSelect.sampler_name": "euler", "BasicScheduler.scheduler": "beta57", "BasicScheduler.steps": 8, "BasicScheduler.denoise": 1.0, "SelfLiftH3Sampler.cfg": 1.0, "SelfLiftH3Sampler.transition_step": 4, "SelfLiftH3Sampler.lowres_scale": 0.6}`
- 跑过 1 次（失败 1、质量闸不过 0），提交者：模型学习

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| 1376x768x124 | 1 | 21.1（21.1–21.1） | — | 63975 | 59042 |

审查记录：无

异常单：A261117-08（R3，已知原因）

<!-- 人写开始 -->
## 人写

用途：

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：

测试总结（测过什么、结论、局限、和别的工作流比）：

分辨率和帧数规则（H3 Ref2V，详见 index/视频模型_分辨率和帧数规则.md「H3 Ref2V」一节）：原生短边 768、面积约 768×1344（节点不强制）；24fps；17k+5，训练范围约 124–362 帧；OOM 帧数未测；脸要多大未测；交片 RIFE 插到 96 再按原片帧率取。
<!-- 人写结束 -->
