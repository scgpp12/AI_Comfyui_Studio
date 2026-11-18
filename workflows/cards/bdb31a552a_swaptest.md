# swaptest（指纹 bdb31a552a）

状态：待测　　类别：待定　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：未填
带说明画布：未填
速查表条目：未填
样板任务：21381308-31cc-4304-bebd-795501534b02（8191，2026-11-18 12:31:58）

## 机器统计（2026-11-18 12:55 自动生成）

- 模型文件：face_yolov8m.pt、minimax_h3_audio_vae_fp32.safetensors、minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors、minimax_h3_fl2va_pruned_int8_convrot.safetensors、minimax_h3_video_vae_fp16.safetensors、qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
- 主模型：minimax_h3_fl2va_pruned_int8_convrot.safetensors；块补丁：无；步数：8
- 关键参数：`{"KSamplerSelect.sampler_name": "er_sde", "BasicScheduler.scheduler": "simple", "BasicScheduler.steps": 8, "BasicScheduler.denoise": 0.4, "MiniMaxH3ReferenceToVideo.ref_image_size": "match", "LoraLoaderModelOnly.strength_model": 1.0, "CLIPLoader.device": "default"}`
- 跑过 2 次（失败 0、质量闸不过 0），提交者：未知（按前缀推断：None）

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| - | 2 | 77.5（48.0–107.1） | — | 49693.0 | 43957.0 |

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
