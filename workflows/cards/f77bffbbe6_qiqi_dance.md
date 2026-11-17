# qiqi_dance（指纹 f77bffbbe6）

状态：待测　　类别：待定　　（这两项和下面三项在 index/指纹名.json 里改）
原件脚本：未填
带说明画布：未填
速查表条目：未填
样板任务：b3488adc-46bf-45a1-b085-aceeadeb8c42（8191，2026-11-17 18:33:18）

## 机器统计（2026-11-17 22:18 自动生成）

- 模型文件：minimax_h3_audio_vae_fp32.safetensors、minimax_h3_video_vae_fp16.safetensors、qwen3vl_32b_minimax_h3_int8_convrot.safetensors、viggle_remake_swap_pruned_int8_convrot.safetensors
- 主模型：viggle_remake_swap_pruned_int8_convrot.safetensors；块补丁：无；步数：6
- 关键参数：`{"KSamplerSelect.sampler_name": "euler", "ManualSigmas.sigmas": "1.0, 0.990476, 0.965243, 0.923077, 0.8, 0.631579, 0.0"}`
- 跑过 3 次（失败 0、质量闸不过 0），提交者：模型学习

| 尺寸 | 次数 | 执行秒中位（最小–最大） | 每步秒中位 | 整卡显存峰值中位 MiB | 进程显存峰值中位 MiB |
|---|---|---|---|---|---|
| - | 3 | 287.4（286.3–288.3） | — | 71308 | 65512 |

审查记录：无

异常单：无

<!-- 人写开始 -->
## 人写

用途：舞蹈换七七：整条 294 帧 viggle 换人，short_edge 480、竖屏 480×832。脚本 castsery/qiqi_dance/qd_vg.py（参数：重画帧 种子 short_edge）。

质量结论（写出处）：

用户评价（从幕布抄：分数、原话、日期）：

测试总结（测过什么、结论、局限、和别的工作流比）：11-17 三次（种子 0、1 等），执行约 287 秒、整卡峰值约 71GB，都能跑完。结论：全身景脸宽只有约 26 像素，嘴角拉到脸颊、鼻孔大、脸扁，修脸改不动；真人全身正面要看清脸的镜头不要用 480，改用 736 分段（3fd26fa7ce）。背面、没有脸的镜头可以用。

分辨率和帧数规则（viggle，详见 index/视频模型_分辨率和帧数规则.md「viggle 换人」一节）：short_edge 480–736（节点第 72 行）；24fps；17n+5、90–345 帧；736 下 192 帧能跑、294 帧 OOM，480 下 294 帧能跑；脸宽（原尺寸）736 全身约 41 像素正常、480 全身约 26 像素画坏，超分到 1080 后约 60 像素；真人全身正面要看清脸用 736、按切点分段每段约 192 帧以内（规范第 26 条）；交片 RIFE 插到 96 再按原片帧率取（qd_30.py）。
<!-- 人写结束 -->
