# 对照_Qwen两图关前缀缓存（指纹 09ee4f5dba）

状态：淘汰　　类别：出图　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：castsery/qwen_speed/speed_ab.py（E2）
带说明画布：未填
速查表条目：未填
样板任务：a0176fcc-1ca0-4f3d-b969-b896cddd4a52（8188，2026-11-17 14:54:31）

## 机器统计（2026-11-17 22:18 自动生成）

- 模型文件：qwen3vl_8b_bf16.safetensors、qwen_image_2.1_bf16.safetensors、qwen_image_2.1_vae_bf16.safetensors
- 主模型：qwen_image_2.1_bf16.safetensors；块补丁：无；步数：25
- 关键参数：`{"CLIPLoader.device": "default", "QwenImage21Cache.device": "off", "QwenImage21Cache.dtype": "default", "TextEncodeQwenImage21.resolution": 0, "KSampler.steps": 25, "KSampler.cfg": 1.0, "KSampler.sampler_name": "euler", "KSampler.scheduler": "simple", "KSampler.denoise": 1.0}`
- 跑过 1 次（失败 0、质量闸不过 0），提交者：未知（按前缀推断：castsery/qwen_speed/speed_ab.py 的 8188 改版（总督导））

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| 1536x864 | 1 | 47.9（47.9–47.9） | 1.9 | 没记 | 没记 |

审查记录：无

异常单：A261117-03（R2，已知原因）

<!-- 人写开始 -->
## 人写

用途：

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：

测试总结（测过什么、结论、局限、和别的工作流比）：
<!-- 人写结束 -->
