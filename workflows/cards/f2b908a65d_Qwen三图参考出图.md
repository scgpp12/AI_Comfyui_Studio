# Qwen三图参考出图（指纹 f2b908a65d）

状态：可用　　类别：出图　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：ai-drama-pipeline/tools/qi21.py（gen_t0a、gen_r4–r8、gen_emo 等）
带说明画布：8188 AI天气/出图/主播定妆三视图_Qwen_带说明.json（内部代号 T0A）（人台＋服装＋脸那一类；同指纹也包括妆面三图等别的三图组合）
速查表条目：「定妆和场景」节 Qwen 2.1 固定参数（第 111 行）
样板任务：59eae015-bde7-43f8-8430-1e43b870e453（8188，2026-11-18 10:48:36）

## 机器统计（2026-11-18 12:40 自动生成）

- 模型文件：qwen3vl_8b_bf16.safetensors、qwen_image_2.1_bf16.safetensors、qwen_image_2.1_vae_bf16.safetensors
- 主模型：qwen_image_2.1_bf16.safetensors；块补丁：无；步数：25
- 关键参数：`{"CLIPLoader.device": "default", "QwenImage21Cache.device": "auto", "QwenImage21Cache.dtype": "default", "TextEncodeQwenImage21.resolution": 0, "KSampler.steps": 25, "KSampler.cfg": 1.0, "KSampler.sampler_name": "euler", "KSampler.scheduler": "simple", "KSampler.denoise": 1.0}`
- 跑过 53 次（失败 0、质量闸不过 0），提交者：未知（按前缀推断：None）、未知（按前缀推断：ai-drama-pipeline/tools/qi21.py（gen_t0a、gen_r4–r8、gen_emo、gen_v3、gen_hat、gen_studio 等共用，前缀分不出是哪个，审美频道））

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| 1104x1376 | 15 | 24.3（18.1–28.4） | 0.6 | 没记 | 没记 |
| 1056x1408 | 12 | 22.9（14.9–47.2） | 0.5 | 没记 | 没记 |
| 1376x768 | 12 | 17.6（11.6–24.4） | 0.4 | 50995.0 | 46062.0 |
| 1024x1280 | 7 | 22.1（21.8–22.3） | 0.5 | 没记 | 没记 |
| 1104x1216 | 4 | 15.6（12.9–28.5） | 0.5 | 没记 | 没记 |
| 864x1536 | 2 | 16.1（11.0–21.1） | 0.4 | 44279.0 | 39346.0 |
| 1536x864 | 1 | 21.3（21.3–21.3） | 0.5 | 没记 | 没记 |

审查记录：无

异常单：无

<!-- 人写开始 -->
## 人写

用途：

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：

测试总结（测过什么、结论、局限、和别的工作流比）：
<!-- 人写结束 -->
