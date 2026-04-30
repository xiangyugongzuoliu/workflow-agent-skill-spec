# Agent Skill 测试与发布规范

Skill 测试有两个目标：

1. Skill 该触发时触发，不该触发时保持沉默。
2. Skill 带来的输出质量提升，足以抵消额外上下文、时间和复杂度。

测试应先于大规模实现。一个 Skill 如果没有可验证样例，就很难稳定维护。

## 1. 测试类型

```text
触发测试
  验证 name、description 和可选 when_to_use。

功能测试
  验证工作流、脚本、输出和恢复行为。

恢复测试
  验证中断后能读取 progress.json 继续。

安全测试
  验证 Skill 不泄漏密钥，也不执行不安全动作。

Runtime 测试
  验证 runtime 缺失、损坏、降级和修复路径。

回归测试
  将修改后的 Skill 与上一版本或无 Skill 基线对比。

跨模型测试
  验证不同模型能力下，关键步骤仍能执行。
```

## 2. 触发评测

创建真实用户提示词，并标注 Skill 是否应该触发。

建议准备约 20 条提示词：

- 8 到 10 条应该触发。
- 8 到 10 条不应该触发。

好的触发提示词应覆盖：

- 正式说法和口语说法。
- 错别字和缩写。
- 直接任务描述和间接任务描述。
- 短请求和长请求。
- 单步请求和多步请求。
- 相似但超出范围的任务。

将触发用例存入 `evals/trigger-queries.json`。

每条用例应包含：

```json
{
  "id": "should-trigger-001",
  "query": "检查这个已有 Skill，告诉我它能不能安全发布。",
  "should_trigger": true,
  "reason": "用户要求审查 Skill 的发布安全性。"
}
```

## 3. 功能评测

功能测试应使用真实输入，并验证具体输出。

最低检查：

```text
[ ] 必填输入已解析。
[ ] 缺失必填输入时有清晰停止条件。
[ ] 预期输出文件存在。
[ ] JSON 输出可以成功解析。
[ ] 报告章节符合文档模板。
[ ] 脚本失败时返回非零退出码。
[ ] 错误包含足够修复问题的细节。
```

避免空泛断言：

```text
输出很好。
结果很专业。
写作质量很高。
```

优先使用可验证断言：

```text
输出包含“阻塞问题”章节。
每条发现都引用文件路径。
生成的 JSON 包含 status、current_step、completed_steps 和 resume_hint。
输入文件不存在时，脚本以非零退出码退出。
```

## 4. 恢复评测

任何长时间运行的 Skill 都应证明自己能从中断中恢复。

测试顺序：

1. 启动一次运行。
2. 在中间步骤后停止。
3. 使用同一个运行目录重新进入。
4. 确认 Agent 读取 `state/progress.json`。
5. 确认已完成步骤不会重复，除非用户明确要求。
6. 确认新输出落在同一个运行目录。

必需恢复字段：

```text
status
current_step
completed_steps
failed_steps
outputs
resume_hint
```

## 5. 脚本评测

脚本应在 Agent 之外测试。

必需检查：

```text
[ ] 脚本有已记录的命令。
[ ] 脚本能处理缺失输入。
[ ] 脚本能处理格式错误的输入。
[ ] 脚本将输出写到指定路径。
[ ] 脚本打印有用错误。
[ ] 脚本不依赖维护者专属路径。
[ ] 脚本有副作用时可以 dry-run 运行。
```

## 6. 安全评测

发布前运行：

```bash
gitleaks detect --no-git --source . --redact --no-banner
rg -n "token|secret|password|cookie|api_key|apikey|client|customer|/Users|~/Downloads|private" .
```

然后人工审查每个命中。

只要存在以下任一情况，安全测试就应阻止发布：

- 真实凭据。
- 私人路径。
- 客户数据。
- 隐藏外部依赖。
- 破坏性默认行为。
- 没有超时或错误处理的网络调用。

## 7. Runtime 评测

Runtime 评测应覆盖 `config/runtime.json` 声明的 env、binary、model、cache 和 network。

最低检查：

```text
[ ] 必需 env 缺失时停止。
[ ] 必需 binary 缺失时停止。
[ ] 可选 binary 缺失时记录 skipped_checks。
[ ] 必需模型 checksum 不匹配时停止。
[ ] cache 不可写时给出 repair 建议。
[ ] 网络不可用时停止或记录降级。
```

Runtime 用例存入 `evals/runtime-cases.json`。

## 8. 回归评测

改进已有 Skill 时，与基线对比：

```text
基线
  Skill 的上一版本，或无 Skill。

候选
  当前修改后的版本。
```

记录：

```text
pass_rate
duration_ms
token_estimate
failed_assertions
human_feedback
```

只有质量收益值得新增复杂度时，Skill 才算更好。若质量提升很小但 token 用量明显升高，通常不值得改。

## 9. 跨模型评测

如果 Skill 面向多个模型或客户端，至少检查：

- 入口是否足够清晰。
- 步骤是否编号明确。
- 输出格式是否稳定。
- 复杂判断是否有示例。
- 失败处理是否可执行。

较弱模型需要更明确的步骤、示例和输出格式。较强模型仍然不应被迫读取冗余背景。

## 10. 评估驱动开发

推荐流程：

```text
1. 写触发评测。
2. 写最小 SKILL.md。
3. 跑主路径。
4. 记录失败。
5. 补步骤、脚本或上下文。
6. 再跑评测。
7. 通过后再扩能力。
```

不要先写一个庞大 Skill，再凭感觉补测试。

## 11. 发布门禁

以下清单通过前不要发布：

```text
触发
  [ ] 触发评测包含正例和反例。
  [ ] description 覆盖触发词。
  [ ] description 写明排除场景。

功能
  [ ] 主路径通过。
  [ ] 预期输出文件存在。
  [ ] JSON 输出可解析。
  [ ] 报告章节完整。

恢复
  [ ] 适用时已测试恢复行为。
  [ ] progress.json 可读。
  [ ] resume_hint 可执行。

脚本
  [ ] 适用时已直接测试脚本。
  [ ] 脚本失败返回非零退出码。
  [ ] 破坏性动作默认 dry-run。

安全
  [ ] 安全扫描无未解决发现。
  [ ] 无真实凭据。
  [ ] 无私人路径。
  [ ] 无客户数据。

Runtime
  [ ] 适用时 config/runtime.json 可解析。
  [ ] doctor / prepare / repair 或手动等价步骤已说明。
  [ ] runtime 缺失和损坏路径有 eval。

文档
  [ ] README 和示例匹配实际行为。
  [ ] 公开声明没有超出已测试能力。
  [ ] setup、security、testing 文档已同步。
```
