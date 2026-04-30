# 步骤 03：验证

## 目标

确认审查完整、有证据支撑，并且可以安全报告。

## 输入

- `step02-execute/findings.json`
- `step02-execute/notes.md`
- `state/progress.json`

## 动作

1. 检查每个阻塞问题都有文件证据。
2. 检查没有完整打印疑似密钥值。
3. 检查建议修复都位于目标目录内。
4. 检查已列出跳过的检查。
5. 将最终发布审查报告写入 `output/public-release-report.md`。
6. 将 `state/progress.json` 更新为 `completed`。

## 输出

```text
output/public-release-report.md
state/progress.json
```

## 报告结构

```markdown
# 公开发布审查报告

## 判断

## 阻塞问题

## 非阻塞问题

## 建议修复

## 验证

## 跳过的检查

## 剩余风险
```

## 完成标准

- 最终报告存在。
- 判断值为 `ready`、`ready-with-notes` 或 `blocked` 之一。
- 阻塞问题都有证据。
- 验证章节说明已运行哪些检查。
- 剩余风险明确。

## 失败处理

如果发现项不完整，回到步骤 02，不要猜测。

如果报告无法写入，返回错误和预期报告路径。
