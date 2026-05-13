# 数据字典

文件：`data/student_ai_tool_usage.csv`

## 字段说明

| 字段名 | 含义 | 说明 |
| --- | --- | --- |
| student_id | 学号后三位 | 应为 3 位数字 |
| name | 姓名 | 不应为空 |
| class_name | 班级 | 例如 信管2301 |
| assignment | 作业名称 | text_novel / image_prompt / video_generation |
| tool | 使用的 AI 工具 | 例如 豆包、DeepSeek、Kimi、MiniMax、ChatGPT |
| prompt_count | 提示词修改次数 | 应为非负整数 |
| output_quality_score | 作品质量评分 | 0 到 100 |
| submit_time | 提交时间 | 应为 YYYY-MM-DD HH:MM |
| duration_min | 完成作业耗时，分钟 | 应为正数 |
| video_seconds | 视频长度，秒 | 只有 video_generation 作业需要检查，至少 5 秒 |
| passed | 是否通过 | 应统一为 yes 或 no |

## 数据清洗原则

1. 不要直接删除异常数据。
2. 所有问题记录到 `output/data_quality_issues.csv`。
3. 可以生成一个清洗后的版本 `output/cleaned_student_ai_tool_usage.csv`。
4. 对明显可标准化的字段进行标准化，例如：
   - Chat GPT → ChatGPT
   - doubao / Doubao / 豆包 → 豆包
   - kimi → Kimi
   - minimax / MiniMax M2.7 → MiniMax
5. 对不能确定的异常值，保留原值，并在问题清单中说明。
