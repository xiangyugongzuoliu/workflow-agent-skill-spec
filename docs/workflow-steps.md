# workflow 步骤规范

> 本文规范 `workflow/step*.md` 步骤文件的命名、结构、执行者、输入输出、验证和调度方式。

## 1. 职责

`workflow/` 存放步骤执行文档。每个步骤是一份独立合约，定义：

- 本步骤为什么存在。
- 由谁执行。
- 读取哪些输入。
- 写出哪些输出。
- 如何判断完成。
- 失败时如何处理。
- 下一步是什么。

步骤文件不是背景说明。它应让另一个 Agent 不读完整会话，也能继续执行。

## 2. 目录职责

```text
workflow/
  step01-prepare.md
  step02-execute.md
  step03-verify.md
```

可以放：

- 步骤执行说明。
- 输入输出约定。
- 验证检查点。
- 调度说明。

不要放：

- 长提示词模板。放 `references/prompts/`。
- 脚本代码。放 `scripts/`。
- 大量背景材料。放 `references/` 或 `docs/`。
- 运行产物。放 `runs/`。

## 3. 命名规范

```text
stepNN-{action}.md
```

规则：

- `NN` 使用两位数字，从 `01` 开始。
- `{action}` 使用短动作词，连字符分隔。
- 排序顺序就是执行顺序。
- 不使用 `step1`、`step02a`、`step02-1`。

推荐：

```text
step01-prepare.md
step02-collect.md
step03-review.md
step04-report.md
```

不推荐：

```text
step1.md
step02a-review.md
review-step.md
final.md
```

## 4. 标准结构

```markdown
# 步骤 02：执行审查

> 执行者：Agent / SubAgent / 脚本 / 外部工具
> 输入：`state/config.json`、`step01-prepare/file-index.txt`
> 输出：`step02-execute/findings.json`

## 目标

说明本步骤要完成什么。

## 输入

- 输入文件或目录。
- 上一步产物。
- 运行配置。

## 动作

1. 具体动作一。
2. 具体动作二。
3. 具体动作三。

## 输出

- 输出文件路径。
- 输出格式。
- 必需字段。

## 完成标准

- 文件存在。
- JSON 可解析。
- 每条发现包含证据。

## 失败处理

- 缺输入时停止。
- 权限不足时记录路径并继续可访问部分。
- 疑似密钥脱敏。

## 下一步

读取 `workflow/step03-verify.md`。
```

## 5. 执行者类型

```text
Agent
  当前对话中的主 Agent。
  适合编排、判断、读取配置、汇总结论。

SubAgent
  独立上下文中的 Agent。
  适合长材料分析、并行审查、隔离噪音。

脚本
  可执行程序。
  适合确定性操作、批处理、格式校验、转换。

外部工具
  MCP、CLI、API 或浏览器工具。
  适合网络查询、平台操作、系统能力调用。
```

选择规则：

- 确定性强，用脚本。
- 需要理解和判断，用 Agent 或 SubAgent。
- 需要大量上下文隔离，用 SubAgent。
- 需要实时外部数据，用外部工具。

## 6. 输入规范

输入必须写路径或来源，不写“上一步结果”这种会话依赖。

推荐：

```text
输入：
  - state/config.json
  - step01-prepare/file-index.txt
  - 用户指定的 target_dir
```

不推荐：

```text
输入：
  - 上一步分析结果
  - 刚才说的文件
```

## 7. 输出规范

输出路径必须稳定。

```text
步骤目录
  step{NN}-{action}/

最终输出
  output/

状态
  state/progress.json

无输出
  -
```

输出内容应机器可验证：

```json
{
  "status": "completed",
  "items_checked": 12,
  "blocking_issues": [],
  "notes": []
}
```

## 8. 验证检查点

每个步骤至少有一个验证检查点。

示例：

```text
2a  step02-execute/findings.json 存在。
2b  findings.json 可解析。
2c  每个阻塞问题包含 file、evidence、fix。
2d  progress.json 的 current_step 已更新。
```

检查点要具体，不能写“结果质量高”。

## 9. 参数收集

参数分三类：

```text
必须询问
  缺失后无法可靠执行。

可推断
  Agent 可从路径、文件名、上下文推断。

可默认
  从 config/default.json 或规范默认值读取。
```

规则：

- 能推断就不问。
- 问题一次性问完。
- 每个问题说明用途。
- 答案写入 `state/config.json`。

## 10. 前置检查

执行前检查：

- 输入路径存在。
- 必需文件可读。
- 输出目录可写。
- 必需命令存在。
- 必需凭据是否可选或已配置。

失败时不要继续猜。

## 11. 后验证

执行后检查：

- 输出文件存在。
- 输出格式正确。
- 状态文件更新。
- 错误已记录。
- 下一步能独立读取产物继续。

## 12. 分流

同一 Skill 支持多类型输入时，先做分流步骤。

```text
Step 01：识别输入类型
  Markdown → step02-markdown.md
  PDF      → step02-pdf.md
  目录     → step02-directory.md
```

分流结果写入 `state/config.json`：

```json
{
  "input_type": "markdown",
  "selected_path": "workflow/step02-markdown.md",
  "reason": "目标文件扩展名为 .md"
}
```

## 13. 并行与同步

只有任务相互独立时才并行。

适合并行：

- 多文件独立审查。
- 多来源独立采集。
- 多候选方案独立评估。

不适合并行：

- 后一步依赖前一步产物。
- 多个执行者会写同一文件。
- 共享同一外部资源且没有锁。

并行任务必须有同步点：

```text
step04-merge/
  inputs:
    step03-batch-a/result.json
    step03-batch-b/result.json
  output:
    step04-merge/merged.json
```

## 14. 跳过步骤

允许跳过步骤，但必须记录。

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

不要静默跳过。

## 15. 超时与错误

步骤文件应说明：

- 单步超时时间。
- 是否可重试。
- 最大重试次数。
- 失败是否阻塞后续步骤。
- 是否可降级。

示例：

```text
网络请求失败：
  重试 2 次。
  仍失败则记录 skipped_checks。
  不伪造结果。
```

## 16. 禁止事项

- 步骤依赖聊天记忆。
- 步骤没有输出路径。
- 步骤没有完成标准。
- 多个步骤重复做同一件事。
- 步骤里写长篇背景材料。
- 失败后继续执行不可验证动作。
- 并行执行者写同一文件。

## 17. 检查清单

```text
命名
  [ ] stepNN-{action}.md。
  [ ] 编号从 01 开始。
  [ ] action 与输出目录一致。

结构
  [ ] 有目标。
  [ ] 有输入。
  [ ] 有动作。
  [ ] 有输出。
  [ ] 有完成标准。
  [ ] 有失败处理。

执行
  [ ] 执行者明确。
  [ ] 输入路径稳定。
  [ ] 输出可验证。
  [ ] 状态会更新。

恢复
  [ ] 中断后可从文件恢复。
  [ ] 跳过步骤会记录原因。
  [ ] 下一步无需重读完整会话。
```
