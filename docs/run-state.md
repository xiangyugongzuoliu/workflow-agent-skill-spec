# 运行状态规范

> 本文规范 `runs/`、`state/`、`output/`、`progress.json` 和中断恢复机制。

## 1. 职责

运行状态让 Skill 跨会话、跨上下文、跨 Agent 恢复执行。

适用场景：

- 多步骤任务。
- 批量任务。
- 运行时间较长的任务。
- 会生成多个中间产物的任务。
- 失败后需要继续的任务。

短任务可以不创建运行目录，但只要中断后重来会浪费明显时间，就应创建。

## 2. 目录结构

```text
runs/
  {keyword}-YYYYMMDD-HHMMSS/
    state/
      config.json
      progress.json
    step01-prepare/
    step02-execute/
    step03-verify/
    output/
```

固定目录：

```text
state/
  运行配置、进度、错误和恢复提示。

output/
  最终产物。
```

动态目录：

```text
stepNN-{action}/
  与 workflow/stepNN-{action}.md 对齐。
```

## 3. 运行目录命名

格式：

```text
{keyword}-YYYYMMDD-HHMMSS
```

多模式：

```text
{mode}-{keyword}-YYYYMMDD-HHMMSS
```

示例：

```text
markdown-release-20260430-091500
audit-agent-skill-20260430-101200
fix-readme-20260430-103000
```

不要只用时间戳。`keyword` 用于恢复时识别任务。

## 4. keyword 规则

`keyword` 来自本次任务的核心输入：

- 文章标题。
- 仓库名。
- 文件名。
- 搜索词。
- 用户名。
- 产品名。
- 模式名。

标准化：

- 转小写。
- 空格转连字符。
- 去掉特殊符号。
- 过长时截断。
- 中文可保留核心拼音或英文部分。

## 5. config.json

`state/config.json` 存本次运行参数。

```json
{
  "target": "/path/to/project",
  "mode": "release-review",
  "keyword": "project-review",
  "created_at": "2026-04-30T09:15:00Z",
  "run_dir": "runs/project-review-20260430-091500"
}
```

规则：

- 本次运行输入写这里。
- 不写真实密钥。
- 不写可公开文件外的私人路径，除非这是用户本次明确输入且不进入公开仓库。
- 每个推断值标注来源更好。

## 6. progress.json

最小字段：

```json
{
  "status": "processing",
  "current_step": "step02-execute",
  "completed_steps": ["step01-prepare"],
  "failed_steps": [],
  "skipped_steps": [],
  "outputs": {
    "config": "state/config.json",
    "file_index": "step01-prepare/file-index.txt"
  },
  "resume_hint": "继续执行 step02-execute，读取 state/config.json 和 step01-prepare/file-index.txt。"
}
```

推荐字段：

```text
status
current_step
completed_steps
failed_steps
skipped_steps
outputs
errors
resume_hint
created_at
updated_at
```

## 7. status

```text
pending
  已创建，尚未开始。

processing
  正在执行。

completed
  已完成。

failed
  失败且需要处理。
```

不要用模糊状态，例如 `done?`、`maybe_failed`。

## 8. 更新时机

必须更新：

- 运行目录创建后。
- 每个步骤开始前。
- 每个步骤完成后。
- 每个步骤失败后。
- 跳过步骤时。
- 最终完成时。

原则：

- 先写产物，再更新状态。
- 状态更新应尽量原子化。
- 失败时也要写入 `progress.json`。

## 9. 恢复流程

中断后恢复：

1. 找到最新或指定运行目录。
2. 读取 `state/progress.json`。
3. 检查 `status`。
4. 检查 `completed_steps` 的产物是否存在。
5. 从 `current_step` 继续。
6. 不重复执行已完成步骤，除非用户明确要求。

恢复时不要依赖聊天记录。

## 10. skipped_steps

跳过步骤必须记录原因。

```json
{
  "skipped_steps": [
    {
      "step": "step03-fix",
      "reason": "用户只要求审查，不要求修改"
    }
  ]
}
```

## 11. errors

错误记录应包含：

```json
{
  "errors": [
    {
      "step": "step02-execute",
      "type": "permission_denied",
      "path": "private-file.txt",
      "recoverable": true,
      "message": "文件不可读，已跳过。"
    }
  ]
}
```

不要记录真实密钥值。

## 12. output/

最终产物统一写入 `output/`。

推荐：

```text
output/
  final-report.md
  blockers.json
  summary.json
```

最终回复应引用这些产物，而不是只在对话中输出结果。

## 13. 最新指针

反复迭代时使用稳定指针：

```text
draft_latest.md
feedback_latest.md
report_latest.json
```

不要在提示词中写变量算术，例如 `{round_num-1}`。需要上一轮结果时，读取最新指针文件。

## 14. 多模式运行

多模式 Skill 用模式前缀区分：

```text
runs/
  check-article-a-20260430-091500/
  fix-article-a-20260430-093000/
  audit-project-b-20260430-100000/
```

不要让不同模式写同一个运行目录。

## 15. 清理策略

公开 Skill 可以建议：

- 保留最近若干次运行。
- 用户手动删除旧运行目录。
- 不自动删除用户数据。
- 清理前生成待删除清单。

不要默认清空 `runs/`。

## 16. 完成报告

完成时报告：

```text
状态：completed
运行目录：runs/project-review-20260430-091500
最终产物：output/final-report.md
验证：已运行 JSON 解析、链接检查、密钥扫描
剩余风险：未运行网络检查，因为用户关闭网络访问
```

## 17. 禁止事项

- 只在聊天里记录进度。
- 运行目录只有时间戳没有 keyword。
- 失败时不写 `progress.json`。
- 跳过步骤不记录原因。
- 最终输出散落在步骤目录。
- 自动删除旧运行数据。
- 把真实凭据写进运行状态。

## 18. 检查清单

```text
目录
  [ ] runs/ 存在或短任务明确不需要。
  [ ] state/ 存在。
  [ ] output/ 存在。
  [ ] 步骤目录与 workflow 文件对齐。

状态
  [ ] progress.json 可解析。
  [ ] status 合法。
  [ ] current_step 准确。
  [ ] completed_steps 与实际产物一致。
  [ ] resume_hint 可执行。

恢复
  [ ] 中断后不依赖聊天记录。
  [ ] 已完成步骤不重复执行。
  [ ] 错误和跳过项有记录。
```
