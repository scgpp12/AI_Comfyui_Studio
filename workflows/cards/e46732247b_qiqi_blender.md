# qiqi_blender（指纹 e46732247b）

状态：待测　　类别：待定　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：未填
带说明画布：未填
速查表条目：未填
样板任务：a1875e03-0d34-4592-98b4-68cf0020f2a6（8188，2026-11-17 23:08:53）

## 机器统计（2026-11-18 12:55 自动生成）

- 模型文件：minimax_h3_audio_vae_fp32.safetensors、minimax_h3_fl2v_lightx2v_turbo_4step_v0.1_comfy_resized_avg_rank_21_bf16.safetensors、minimax_h3_fl2va_pruned_int8_convrot.safetensors、minimax_h3_fun_controlnet_union_2.0_pruned_int8_convrot.safetensors、minimax_h3_video_vae_fp16.safetensors、qwen3vl_32b_minimax_h3_int8_convrot.safetensors
- 主模型：minimax_h3_fl2va_pruned_int8_convrot.safetensors；块补丁：有；步数：8
- 关键参数：`{"LoraLoaderModelOnly.strength_model": 0.65, "MiniMaxH3SigmaShift.shift_video": 12.0, "MiniMaxH3SigmaShift.shift_audio": 3.0, "CLIPLoader.device": "default", "BasicScheduler.scheduler": "simple", "BasicScheduler.steps": 8, "BasicScheduler.denoise": 1.0, "KSamplerSelect.sampler_name": "euler", "MiniMaxH3ReferenceToVideo.ref_image_size": "max", "MiniMaxH3FunControlNetApply.strength": 1.0, "MiniMaxH3FunControlNetApply.start_percent": 0.0, "MiniMaxH3FunControlNetApply.end_percent": 1.0}`
- 跑过 2 次（失败 0、质量闸不过 0），提交者：模型学习

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| 1376x768x124 | 2 | 195.6（195.6–195.6） | 19.2 | 80023.0 | 75090.0 |

审查记录：无

异常单：无

<!-- 人写开始 -->
## 人写

用途：七七指屏路线 B1：H3 剪枝底模＋ControlNet 2.0（fun_controlnet_union 2.0 pruned int8），控制视频＝Blender 深度，首尾帧钉。1376×768、124 帧。脚本 castsery/qiqi_blender/qb_vid.py B1。

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：11-18 07:01–07:04 幕布打分：路线 A 8 分；B1 6 分、B2 6 分，B1、B2 的意见原话「人物动作僵硬 动作很缓慢的」。用户选路线 A。

测试总结（测过什么、结论、局限、和别的工作流比）：11-17 种子 999、7 各一条，执行约 196 秒、整卡峰值约 81GB；动作时间点跟 Blender 一致，第 1–3 帧没有跳变，量数上比 A 稳。但用户看片嫌「人物动作僵硬 动作很缓慢」，6 分。结论：Blender 驱动的动作照搬了假人动画的匀速和慢节奏，量数稳不等于看着自然；以后用 Blender 当控制，要先把动画本身调快、加缓入缓出，再喂。

分辨率和帧数规则（视频工作流照 index/视频模型_分辨率和帧数规则.md 对应模型一节写；出图写「不适用」）：
<!-- 人写结束 -->
