# Qwen深度控制_一参考图（指纹 f36be01b18）

状态：待测　　类别：出图　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：castsery/qwen_speed/speed_fix.py（a）
带说明画布：未填
速查表条目：规范 v1 第 11 条（非用深度控制不可时只喂 1 张参考图）
样板任务：9c50c2d8-72ed-43e6-a69e-d6e3ec05facb（8188，2026-11-17 14:56:09）

## 机器统计（2026-11-17 18:15 自动生成）

- 模型文件：qwen3vl_8b_bf16.safetensors、qwen_image_2.1_bf16.safetensors、qwen_image_2.1_fun_controlnet_union_int8_convrot.safetensors、qwen_image_2.1_vae_bf16.safetensors
- 主模型：qwen_image_2.1_bf16.safetensors；块补丁：有；步数：25
- 关键参数：`{"CLIPLoader.device": "default", "QwenImage21Cache.device": "auto", "QwenImage21Cache.dtype": "default", "TextEncodeQwenImage21.resolution": 0, "KSampler.steps": 25, "KSampler.cfg": 1.0, "KSampler.sampler_name": "euler", "KSampler.scheduler": "simple", "KSampler.denoise": 1.0, "QwenImageDiffsynthControlnet.strength": 1.0}`
- 跑过 1 次（失败 0、质量闸不过 0），提交者：未知（按前缀推断：castsery/qwen_speed/speed_fix.py（模型学习频道））

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| 1536x864 | 1 | 40.2（40.2–40.2） | 1.5 | 没记 | 没记 |

审查记录：无

异常单：A261117-04（R2，已知原因）

<!-- 人写开始 -->
## 人写

用途：

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：

测试总结（测过什么、结论、局限、和别的工作流比）：
<!-- 人写结束 -->
