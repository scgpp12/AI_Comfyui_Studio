# h3cmp（指纹 30dfe9f406）

状态：待测　　类别：待定　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：未填
带说明画布：未填
速查表条目：未填
样板任务：8b6aee21-df9c-4ba7-9bb5-23dea906e435（8188，2026-11-17 22:29:41）

## 机器统计（2026-11-18 12:40 自动生成）

- 模型文件：Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors、minimax_h3_audio_vae_fp32.safetensors、minimax_h3_latent_upscaler_3d_conv_v1_fp16.safetensors、minimax_h3_video_vae_fp16.safetensors、qwen3vl_32b_minimax_h3_int8_convrot.safetensors
- 主模型：Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors；块补丁：无；步数：8
- 关键参数：`{"MiniMaxH3ReferenceToVideo.ref_image_size": "match", "KSamplerSelect.sampler_name": "euler", "BasicScheduler.scheduler": "beta57", "BasicScheduler.steps": 8, "BasicScheduler.denoise": 1.0, "SelfLiftH3Sampler.cfg": 1.0, "SelfLiftH3Sampler.transition_step": 4, "SelfLiftH3Sampler.lowres_scale": 0.6}`
- 跑过 5 次（失败 0、质量闸不过 0），提交者：模型学习

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| 1376x768x124 | 5 | 122.3（111.4–123.9） | 18.0 | 65631 | 60698 |

审查记录：无

异常单：无

<!-- 人写开始 -->
## 人写

用途：

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：

测试总结（测过什么、结论、局限、和别的工作流比）：

分辨率和帧数规则（H3 Ref2V，详见 index/视频模型_分辨率和帧数规则.md「H3 Ref2V」一节）：原生短边 768、面积约 768×1344（节点不强制）；24fps；17k+5，训练范围约 124–362 帧；OOM 帧数未测；脸要多大未测；交片 RIFE 插到 96 再按原片帧率取。
调度器：本卡就是 Beta57 对照用的 beta57 版（h3cmp/run_b57.py）；11-18 用户定主播类镜头默认 beta57（ComfyUI 规范 v1.6 第 33 条）。
<!-- 人写结束 -->
