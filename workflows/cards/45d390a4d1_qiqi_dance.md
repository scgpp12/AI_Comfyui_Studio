# qiqi_dance（指纹 45d390a4d1）

状态：待测　　类别：待定　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：未填
带说明画布：未填
速查表条目：未填
样板任务：cb96abaf-4cf7-4031-86a3-2644913591cf（8191，2026-11-17 19:31:21）

## 机器统计（2026-11-18 12:40 自动生成）

- 模型文件：face_yolov8m.pt、minimax_h3_audio_vae_fp32.safetensors、minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors、minimax_h3_fl2va_pruned_int8_convrot.safetensors、minimax_h3_video_vae_fp16.safetensors、qwen3vl_32b_minimax_h3_int8_convrot.safetensors
- 主模型：minimax_h3_fl2va_pruned_int8_convrot.safetensors；块补丁：无；步数：8
- 关键参数：`{"KSamplerSelect.sampler_name": "er_sde", "BasicScheduler.scheduler": "simple", "BasicScheduler.steps": 8, "BasicScheduler.denoise": 0.55, "MiniMaxH3ReferenceToVideo.ref_image_size": "match", "LoraLoaderModelOnly.strength_model": 1.0, "CLIPLoader.device": "default"}`
- 跑过 1 次（失败 0、质量闸不过 0），提交者：模型学习

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| - | 1 | 39.6（39.6–39.6） | — | 64242 | 58446 |

审查记录：无

异常单：无

<!-- 人写开始 -->
## 人写

用途：

质量结论（写出处）：FaceRefine 只能改脸部细节，改不了嘴型和表情；结构画坏了回换人那步重做（规范第 27 条；舞蹈换七七 v2–v4 量过，嘴张开、嘴宽只差 1–3%）。

用户评价（从幕布抄：分数、原话、日期）：

测试总结（测过什么、结论、局限、和别的工作流比）：

分辨率和帧数规则（H3 fl2va，详见 index/视频模型_分辨率和帧数规则.md「H3 fl2va」一节）：原生短边 768、面积约 768×1344（节点不强制）；24fps；17k+5，训练范围约 124–362 帧；能跑 124、243 帧，FaceRefine 画布 768 每块 93 帧能跑；OOM 帧数未测；脸要多大未测；交片 RIFE 插到 96 再按原片帧率取。
<!-- 人写结束 -->
