# Qwen文生图（指纹 a4ef3a662c）

状态：可用　　类别：出图　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：ai-drama-pipeline/tools/qi21.py（gen_hat 帽子参考、gen_studio）
带说明画布：未填
速查表条目：第 111 行
样板任务：24c334f5-8155-473b-9924-942fe3c7070f（8188，2026-11-17 14:28:31）

## 机器统计（2026-11-17 18:15 自动生成）

- 模型文件：qwen3vl_8b_bf16.safetensors、qwen_image_2.1_bf16.safetensors、qwen_image_2.1_vae_bf16.safetensors
- 主模型：qwen_image_2.1_bf16.safetensors；块补丁：无；步数：25
- 关键参数：`{"CLIPLoader.device": "default", "QwenImage21Cache.device": "auto", "QwenImage21Cache.dtype": "default", "TextEncodeQwenImage21.resolution": 0, "KSampler.steps": 25, "KSampler.cfg": 1.0, "KSampler.sampler_name": "euler", "KSampler.scheduler": "simple", "KSampler.denoise": 1.0}`
- 跑过 5 次（失败 0、质量闸不过 0），提交者：未知（按前缀推断：ai-drama-pipeline/tools/qi21.py（gen_t0a、gen_r4–r8、gen_emo、gen_v3、gen_hat、gen_studio 等共用，前缀分不出是哪个，审美频道））

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| 1536x864 | 4 | 7.5（7.2–14.7） | 0.3 | 没记 | 没记 |
| 1024x1024 | 1 | 13.3（13.3–13.3） | 0.2 | 没记 | 没记 |

审查记录：无

异常单：无

<!-- 人写开始 -->
## 人写

用途：

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：

测试总结（测过什么、结论、局限、和别的工作流比）：
<!-- 人写结束 -->
