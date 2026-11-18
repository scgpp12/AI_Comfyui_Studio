# qiqi_blender_v3（指纹 b45d7e2023）

状态：待测　　类别：待定　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：未填
带说明画布：未填
速查表条目：未填
样板任务：4f06198e-a2ad-476d-94ff-3d45f3844770（8188，2026-11-18 08:20:46）

## 机器统计（2026-11-18 12:55 自动生成）

- 模型文件：minimax_h3_audio_vae_fp32.safetensors、minimax_h3_fl2v_lightx2v_turbo_4step_v0.1_comfy_resized_avg_rank_21_bf16.safetensors、minimax_h3_fl2va_int8_convrot.safetensors、minimax_h3_video_vae_fp16.safetensors、qwen3vl_32b_minimax_h3_int8_convrot.safetensors
- 主模型：minimax_h3_fl2va_int8_convrot.safetensors；块补丁：无；步数：8
- 关键参数：`{"LoraLoaderModelOnly.strength_model": 0.65, "MiniMaxH3SigmaShift.shift_video": 12.0, "MiniMaxH3SigmaShift.shift_audio": 3.0, "CLIPLoader.device": "default", "BasicScheduler.scheduler": "simple", "BasicScheduler.steps": 8, "BasicScheduler.denoise": 1.0, "KSamplerSelect.sampler_name": "euler", "MiniMaxH3ReferenceToVideo.ref_image_size": "max"}`
- 跑过 2 次（失败 0、质量闸不过 0），提交者：模型学习

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| 1376x768x124 | 2 | 166.1（159.2–173.0） | 16.5 | 77231.0 | 72298.0 |

审查记录：无

异常单：无

<!-- 人写开始 -->
## 人写

用途：七七指屏 v3（攻击研究 11-18 按真人速度重做的 Blender：走三步到大屏前再指）路线 A：H3 首尾帧（fl2va int8 全量＋lightx2v turbo 0.65、SigmaShift 12/3、euler simple 8 步），钉首、中（下标 61）、尾三帧，关键帧是 Qwen 2.1 照 v3 深度出的（种子 457）。1376×768、124 帧。脚本 castsery/qiqi_blender_v3/qb3_vid.py A。

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：11-18 总督导把种子 999 和甲版北京、上海、广州三条地图合成挂上幕布，用户分数待填。

测试总结（测过什么、结论、局限、和别的工作流比）：11-18 种子 999、7 各一条，执行 159／173 秒，整卡峰值约 77GB。动作时间点和 Blender v3 一致（第 24–48 帧走三步、第 60–72 帧抬手、之后停住指大屏正中），v2 那种空站慢挪没有了。种子 999 自评 7.5：走路时自然转成侧脸，大屏干净；全景脸约 53 像素偏软。种子 7 自评 6.5：第 72–84 帧绿幕上冒出发光圆圈，后面还有零星光点，会坏抠像，不能用于合成。P0-D 用种子 999 合成：指尖停在大屏正中，甲「地图对准指尖」中国留在屏里 50–85%（北京最好），比 v2 的 36–53% 好。

分辨率和帧数规则（视频工作流照 index/视频模型_分辨率和帧数规则.md 对应模型一节写；出图写「不适用」）：
<!-- 人写结束 -->
