# 术语表

> 本规范是中文规范，但保留必要英文专有名词。不要把专有名词翻译到失真。

## 1. 保留英文的术语

```text
Agent
  执行任务的大模型代理。不要翻译成“智能体”作为本规范主术语。

Skill
  Agent 可读取和执行的能力包。不要翻译成“技能”作为文件或规范名称。

Workflow Agent Skill
  工作流式 Agent Skill。本规范的核心对象。

SubAgent
  隔离上下文或并行处理的 Agent 执行单元。不要翻译。

runtime
  Skill 运行所需的环境、二进制、模型、cache 和网络能力集合。

Runtime Contract
  `config/runtime.json` 中声明的 runtime 需求契约。

doctor
  只诊断 runtime 或环境，不修改本机、不下载模型。

prepare
  用户明确执行后准备 runtime、依赖或模型资产。

repair
  修复损坏 runtime、checksum 不匹配或 cache 污染。

resolve
  返回 env、binary、model、cache 的实际路径，避免脚本硬编码。

frontmatter
  `SKILL.md` 顶部的 YAML 元信息。

description
  Agent 判断是否触发 Skill 的核心字段。

workflow/
  存放多步骤执行说明的目录。

runs/
  存放运行状态、中间产物和最终输出的目录。

progress.json
  记录执行状态、恢复提示、错误和产物路径的状态文件。

dry-run
  只生成计划或模拟动作，不执行真实副作用。
```

## 2. 中文可译术语

```text
trigger
  触发。

setup
  环境初始化。

configuration
  配置。

credential
  凭据。

output template
  输出模板。

release gate
  发布门禁。

quality rubric
  质量评分。

fallback
  降级路径。

checkpoint
  检查点。
```

## 3. 命名规则

- 文件名、目录名、frontmatter 字段和 JSON 字段保持英文。
- 文档正文默认中文，但技术标识不翻译。
- 平台名称保持原文，例如 Claude Code、Codex、Cursor、OpenCode、Gemini CLI。
- 不把平台名称写成通用要求。
- 不把内部品牌、课程或私有工具写进通用规范主体。

## 4. 禁止写法

```text
SubAgent 的中文直译
  不使用。应写 SubAgent。

Agent Skill 的中文直译
  不使用。应写 Agent Skill 或 Workflow Agent Skill。

运行环境目录必须是某个私有路径
  应写 Runtime Contract 声明，由目标 runtime manager 或用户工具解析。

所有平台都会读取 CLAUDE.md
  应写“支持 CLAUDE.md 的客户端可以读取”。
```

## 5. 检查清单

```text
[ ] Agent、Skill、Workflow Agent Skill、SubAgent 保持英文。
[ ] runtime、Runtime Contract、doctor、prepare、repair、resolve 含义一致。
[ ] 平台名只作为兼容示例出现。
[ ] 中文说明没有改变技术字段名称。
```
