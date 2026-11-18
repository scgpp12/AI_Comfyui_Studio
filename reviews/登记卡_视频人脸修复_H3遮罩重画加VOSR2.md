# 登记卡：视频人脸修复_H3遮罩重画加VOSR2（11-18，人工登记）

| 项 | 内容 |
|---|---|
| 类别 / 状态 | 出视频（后处理）/ 待用户看：测试通过，有已知副作用 |
| 来源 | AI老腊肉 YouTube sKM83V9og4Q；原文件 minimax_h3_r2v_perfect_face_refine.json，md5 f6c4681c |
| 工作流库 | 8188 `通用/出视频/视频人脸修复_H3遮罩重画加VOSR2.json`、`_带说明.json` |
| 运行实例 | 只在 :8191 跑（扩展装在 model-lab/learn_nodes） |
| 扩展 | Carasibana/ComfyUI-H3-FaceRefine d8521d1；drozbay/MaskVidExperiments c32ed8c（11-18 新装）；ylchen333/ComfyUI-VOSR2 6a21810 |
| 主模型 | Minimax-h3_Singularity_ref2va_Pruned_v1.3_int8，加 LoRA pika_h3_flex_turbo_8step_hd_ref2va，强度 1.0 |
| 其他模型 | qwen3vl_32b_minimax_h3_int8_convrot（8 位）、minimax_h3_video_vae_int8_convrot、minimax_h3_audio_vae_fp32、sam3.1_multiplex_fp16、face_yolov8n、VOSR2 |
| 关键参数 | 裁脸 768×768，crop_factor 2.5，平滑 21/51；SAM 提示词「face」；遮罩清理先收缩 12、再外扩 16；潜空间外扩 36；加 DifferentialDiffusion；euler 加 beta 8 步，denoise 0.5；VOSR2 倍率 1；贴回只贴脸，外扩 24、羽化 24，贴回遮罩用 SAM 的 |
| 脚本 | sons02 castsery/lr_fr/lr_run.py（API 版） |
| 帧数 / 尺寸 | 片段 17n+5 帧、24fps；裁脸画布 768，贴回原尺寸 |
| 用时 / 显存 | 124 帧 152–164 秒；整卡峰值 64–69 GB（自身约 58–63 GB） |
| 测试总结 | 模型学习/H3人脸修复_老腊肉_1118/测试总结.md |
| 已知副作用 | 会改表情和嘴型（0.5、0.35 都改），眼线、唇色变重，腮红变淡；说话和舞蹈镜头不要用 |
| 和旧 FaceRefine 比 | 两种都能修好糊脸。旧做法保住表情、嘴型，但不够像七七（0.36）；新做法更像七七（0.56），但会改表情（11-18 总督导复核更正） |
| 第 2 轮推荐 | 舞蹈、全身、糊脸用扣嘴 0.5（LR_MOUTH=1，像七七 0.58，嘴型保住）；说话镜头用 0.25（第 7 镜嘴声相关 0.52，嘴型没坏）；扣嘴 0.5 在第 7 镜第 16 帧改了眼睛 |
