# 平台适配示例

> 本文给出跨平台适配示例。示例不是通用标准，具体能力以目标 Agent 客户端为准。

## 1. 适配原则

同一个 Workflow Agent Skill 应先满足通用结构：

- `SKILL.md` 写清触发和边界。
- `workflow/` 写清步骤。
- `config/runtime.json` 声明 runtime。
- `docs/setup.md` 写清准备和验证方式。
- `evals/` 提供评测样例。

然后再按客户端能力加适配层。

## 2. Claude Code 示例

适合使用：

```text
CLAUDE.md
  项目级导航和维护规则。

SKILL.md
  Skill 入口。

SubAgent
  用于隔离长材料分析或并行审查。
```

降级：

```text
如果 SubAgent 不可用，主 Agent 按批次串行处理，并在 progress.json 记录批次状态。
如果 hooks 不可用，把 hooks 行为改成手动验证命令。
```

## 3. Codex 示例

适合使用：

```text
AGENTS.md
  项目级规则入口。

SKILL.md
  Skill 入口或规范入口。

scripts/
  承接确定性检查。
```

降级：

```text
如果客户端没有自动 Skill 发现，把 README 或 SKILL.md 路径直接交给 Agent。
如果没有 SubAgent，保持 workflow 步骤串行执行。
```

## 4. Cursor / OpenCode / Gemini CLI 示例

适合使用：

```text
README.md
  面向人类和通用 Agent 的入口。

项目 rules
  只放项目长期约束，不替代 Skill。

workflow/
  由 Agent 按需读取。
```

降级：

```text
如果客户端不识别 SKILL.md，把 SKILL.md 当普通 Markdown 规范读取。
如果客户端不支持工具预授权，setup 文档列出用户应手动确认的命令。
```

## 5. 通用适配记录格式

```text
功能：SubAgent 并行审查
通用能力：隔离上下文分析多个批次
平台增强：支持 SubAgent 的客户端可并行执行
降级路径：主 Agent 串行处理批次
结果影响：速度变慢，输出结构不变
```

```text
功能：hooks 自动检查
通用能力：发布前运行验证命令
平台增强：支持 hooks 的客户端可自动触发
降级路径：README 和 docs/testing.md 中列出手动命令
结果影响：需要人工执行验证命令
```

## 6. 禁止事项

- 不写“所有客户端都支持某字段”。
- 不把 Claude Code、Codex 或其他客户端私有字段写成必需项。
- 不要求读者安装作者使用的私有 CLI。
- 不把项目规则文件当作 Skill 触发机制。
- 不把平台示例写进最小模板。

## 7. 检查清单

```text
[ ] 通用能力和平台增强已分开。
[ ] 每个增强能力都有降级路径。
[ ] README 没有过度承诺平台兼容性。
[ ] 示例中没有把单一客户端写成唯一入口。
```
