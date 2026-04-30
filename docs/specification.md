# 翔宇工作流 Workflow Agent Skill 完整规范

> 公开版跨平台工作流式 Agent Skill 全生命周期规范。
> 目标：让 Agent 可以参考本规范新建、审查、升级、测试和公开发布可复用 Skill。

本规范不是提示词合集，也不是某个私有知识库的内部操作手册，更不是 Claude Code、Codex 或任何单一客户端的私有格式说明。它定义的是一套可公开复用的 Workflow Agent Skill 工程体系：入口如何写、步骤如何拆、上下文如何装载、脚本如何隔离、状态如何恢复、配置如何分层、凭据如何声明、测试如何执行、发布前如何审计。

## 0. 公开版边界

本仓库由翔宇工作流维护，公开版遵循四条边界：

- 保留方法论、结构、模板和可复用工程规则。
- 删除真实账号、密钥、客户数据、私有路径和付费内容。
- 不绑定维护者本机目录、私有知识库或未公开服务。
- 平台特性只作为兼容说明，不伪装成所有 Agent 客户端都支持的标准。

因此，公开版会保留 `Agent`、`Skill`、`Workflow Agent Skill`、`SKILL.md`、`description`、`workflow/`、`runs/`、`progress.json` 等技术标识。`Claude Code`、`Codex`、`Cursor` 等具体客户端名称只在兼容性示例、参考来源或项目入口说明中出现，不作为通用要求。

## 1. 设计哲学

### 1.1 Skill 是工作流能力包

本规范中的 Skill 默认指 Workflow Agent Skill。一个成熟 Skill 至少要回答这些问题：

- 什么时候应该触发？
- 什么时候不应该触发？
- 需要哪些输入？
- 哪些输入可以推断，哪些必须询问？
- 读取哪些上下文？
- 哪些动作由 Agent 判断，哪些动作由脚本执行？
- 每一步输出写到哪里？
- 中断后怎样恢复？
- 最终产物怎样验证？
- 发布前怎样审计安全边界？

只有提示词而没有输入、输出、状态和验证的产物，只能算提示词片段，不算完整 Skill。

### 1.2 入口要短，细节要分层

`SKILL.md` 是入口，不是百科全书。入口文件只承载触发、边界、执行地图和必要约束。长规范、模板、示例、安装、排错和平台差异应放入 `docs/`、`workflow/`、`references/` 或 `assets/`。

入口越长，Agent 越难判断真正重要的规则。

### 1.3 能脚本化的不要交给模型猜

确定性动作优先交给脚本或工具：

- 文件扫描。
- JSON 校验。
- 格式转换。
- 批量重命名。
- 链接检查。
- 密钥扫描。
- 报告模板渲染。

Agent 负责理解、判断、取舍、解释和修复建议。脚本负责稳定、可复现、可测试。

### 1.4 状态必须落盘

长任务、批量任务、多步骤任务必须有运行目录。运行目录记录配置、进度、中间产物、最终输出和恢复提示。这样会话中断、上下文压缩、脚本失败后，另一个 Agent 仍能接手。

### 1.5 公开发布按软件包审计

Skill 会影响 Agent 行为，可能读写文件、访问网络、运行命令或接触凭据。公开发布前必须像审计一个小型软件包一样审查：

- 是否有真实密钥。
- 是否有私人路径。
- 是否有破坏性默认行为。
- 是否依赖隐藏服务。
- 是否有不可复现示例。
- 是否承诺了未测试能力。

## 2. 组织框架

公开版按内部全生命周期规范抽象为 16 个模块。核心模块是所有复杂 Skill 都应理解的基础；辅助模块按场景读取。

```text
核心模块
  01  SKILL.md 入口规范
  02  workflow 步骤规范
  03  上下文工程规范
  04  脚本与工具规范
  05  平台兼容规范
  06  运行状态规范
  07  配置分层规范
  08  提示词与 SubAgent 规范

辅助模块
  09  变量与占位符规范
  10  凭据声明规范
  11  输出模板规范
  12  环境初始化规范
  13  用户入门规范
  14  排错与恢复规范
  15  测试与发布规范
  16  设计模式与反模式
```

## 3. 文档路由

```text
docs/
  specification.md
    总规范。说明设计哲学、模块体系、质量分级和发布门禁。

  skill-file.md
    SKILL.md 入口、frontmatter、目录结构、分发边界和生命周期。

  workflow-steps.md
    workflow/step*.md 的命名、执行者、输入输出、验证和调度。

  context-engineering.md
    上下文分层、直读、检索、隔离、上下文预算和输出结构。

  scripts.md
    scripts/ 目录、脚本返回值、依赖、错误处理和工具调用边界。

  platforms.md
    不同 Agent 客户端的能力差异、frontmatter 差异和兼容写法。

  run-state.md
    runs/、state/、output/、progress.json、resume_hint 和恢复流程。

  configuration.md
    L1 运行时参数、L2 默认配置、L3 预设数据和 Runtime Contract。

  prompts.md
    Agent 提示词、SubAgent 提示词、输出格式和失败处理写法。

  variables.md
    变量命名、占位符、来源标注、禁止变量算术和最新指针。

  credentials.md
    凭据占位、环境变量、权限范围、缺失凭据行为和安全隔离。

  output-templates.md
    Markdown、JSON、HTML 等输出模板的结构和变量占位符。

  setup.md
    安装位置、依赖准备、运行时检查、模型资产和环境修复。

  user-guide.md
    面向普通使用者的入门说明结构。

  troubleshooting.md
    八层错误分类、诊断顺序、重试策略和恢复检查清单。

  testing.md
    触发、功能、恢复、安全、回归、跨模型和发布前测试。

  patterns.md
    常见设计模式、组合方式和反模式。

  security.md
    公开发布安全边界。

  quality-rubric.md
    百分制评分、等级裁决和阻塞项。

  glossary.md
    中英文术语边界，明确哪些专有名词不翻译。

  platform-adapters.md
    不同 Agent 客户端的条件式适配示例和降级路径。

  release.md
    版本、发布门禁、迁移和废弃规则。
```

## 4. 核心模块

### 4.1 `SKILL.md` 入口规范

详见 [skill-file.md](skill-file.md)。

入口规范解决这些问题：

- Skill 怎么命名。
- 目录怎么组织。
- frontmatter 字段怎么写。
- `description` 怎样避免误触发。
- `SKILL.md` 正文保留哪些内容。
- 长内容拆到哪里。
- 个人型和可分发型 Skill 如何区分。

最小合格入口必须包含：

```text
frontmatter
  name
  description
  license 或兼容说明

正文
  范围
  输入
  工作流
  文件边界
  工具边界
  输出
  验证
  失败处理
```

### 4.2 步骤规范

详见 [workflow-steps.md](workflow-steps.md)。

步骤文件解决这些问题：

- 步骤文件如何命名。
- 每步如何声明执行者。
- 输入文件和输出文件怎么写。
- 主 Agent、SubAgent、脚本和外部工具如何分工。
- 如何做前置检查和后验证。
- 如何处理分流、并行、同步点和跳过步骤。

步骤文件是合约，不是说明文。每个步骤至少写清：

- 为什么存在。
- 从哪里读取输入。
- 产物写到哪里。
- 失败时如何停止或恢复。
- 完成后如何验证。

### 4.3 上下文工程规范

详见 [context-engineering.md](context-engineering.md)。

上下文规范解决这些问题：

- 哪些资料应该由主 Agent 直读。
- 哪些资料适合由 SubAgent 或隔离上下文提炼。
- 哪些资料应该通过搜索或 MCP 获取。
- 如何把长资料压缩为执行指令。
- 如何避免把私有知识写死在 Skill 中。

公开 Skill 不应该硬编码私有知识。正确方式是声明“需要哪类资料”，并允许用户提供路径、URL、环境变量或参考目录。

### 4.4 脚本与工具规范

详见 [scripts.md](scripts.md)。

脚本规范解决这些问题：

- 什么动作适合脚本。
- 脚本如何声明依赖。
- 脚本如何读取输入和写输出。
- 返回值如何机器可解析。
- 错误如何分类。
- 网络请求如何超时、重试和失败关闭。
- 如何避免脚本读取真实凭据。

### 4.5 平台兼容规范

详见 [platforms.md](platforms.md)。

平台规范解决这些问题：

- 哪些规则属于通用 Agent Skill 原则。
- 哪些字段只适用于特定客户端。
- 不同 Agent 客户端在工具、hooks、SubAgent、上下文加载、项目入口文件和安装目录上的差异。
- 如何写不绑定单一平台的公开说明。

### 4.6 运行状态规范

详见 [run-state.md](run-state.md)。

运行规范解决这些问题：

- `runs/` 目录怎么命名。
- `keyword` 如何生成。
- `state/progress.json` 必须有哪些字段。
- `output/` 和步骤目录如何组织。
- 中断后如何根据 `resume_hint` 恢复。
- 多模式 Skill 如何避免产物混乱。

### 4.7 配置分层规范

详见 [configuration.md](configuration.md)。

配置规范解决这些问题：

- L1 运行时参数写到哪里。
- L2 默认参数写到哪里。
- L3 预设选项写到哪里。
- 配置优先级如何合并。
- 什么不能写入配置文件。
- runtime 环境、二进制、模型资产和缓存如何声明。

### 4.8 提示词与 SubAgent 规范

详见 [prompts.md](prompts.md)。

提示词规范解决这些问题：

- 提示词模板应该包含哪些部分。
- SubAgent 输出为什么应该是执行指令，而不是研究报告。
- 提示词文件何时放入 `references/prompts/`。
- 如何写失败处理、输出格式和质量标准。
- 如何避免主 Agent 读取过多原始材料。

## 5. 辅助模块

### 5.1 变量与占位符

详见 [variables.md](variables.md)。

变量规范定义：

- 变量命名。
- 变量来源。
- 默认值。
- 禁止变量算术。
- 最新指针文件。
- 路径占位符写法。

### 5.2 凭据声明

详见 [credentials.md](credentials.md) 和 [security.md](security.md)。

凭据规范定义：

- 环境变量名。
- 权限范围。
- dry-run 行为。
- 凭据缺失时的停止条件。
- 公开示例中如何使用占位值。

### 5.3 输出模板

详见 [output-templates.md](output-templates.md)。

输出模板规范定义：

- Markdown 模板。
- JSON 结构。
- HTML 模板。
- 变量占位符。
- 报告章节顺序。
- 机器可验证字段。

### 5.4 环境初始化

详见 [setup.md](setup.md)。

环境规范定义：

- 安装位置。
- 依赖检查。
- 运行时准备。
- 模型资产。
- 可选网络访问。
- 错误修复命令。

### 5.5 用户入门

详见 [user-guide.md](user-guide.md)。

入门规范定义：

- Skill 做什么。
- Skill 不做什么。
- 最小输入。
- 最小运行方式。
- 常见错误。
- 输出在哪里。

### 5.6 排错与恢复

详见 [troubleshooting.md](troubleshooting.md)。

排错规范定义：

- 入口层错误。
- 参数层错误。
- 依赖层错误。
- 凭据层错误。
- 网络层错误。
- 路径层错误。
- 进度层错误。
- 恢复顺序。

### 5.7 测试与发布

详见 [testing.md](testing.md)。

测试规范定义：

- 触发测试。
- 功能测试。
- 恢复测试。
- 脚本测试。
- 安全测试。
- 回归测试。
- 发布门禁。

### 5.8 设计模式与反模式

详见 [patterns.md](patterns.md)。

模式规范定义：

- 顺序编排。
- 多工具协调。
- 迭代精化。
- 上下文感知分流。
- 领域知识封装。
- 可视化输出。
- 定时执行。
- 链式组合。
- 常见反模式。

## 6. 质量分级

```text
等级 0  提示词片段
  只有提示词，没有输入、输出、状态和验证。
  不建议作为公开 Skill 发布。

等级 1  最小 Skill
  有 SKILL.md，包含 name、description、范围、输入、输出和验证。
  适合短任务、审查类任务、格式检查类任务。

等级 2  工作流式 Skill
  有 workflow/ 步骤文件，每步有输入、输出、执行者和完成标准。
  适合多步骤任务和可重复流程。

等级 3  脚本支撑型 Skill
  有 scripts/，确定性任务由脚本执行，脚本可独立运行。
  适合采集、转换、批处理、校验和报告生成。

等级 4  生产级 Skill
  有 runs/ 状态、progress.json、恢复能力、测试样例、安全边界和发布前审计。
  适合长任务、批量任务、跨工具任务和公开分发。
```

公开发布最低要求是等级 1。多步或批量任务应达到等级 2。含脚本、网络、凭据、删除、上传、发布等副作用时，应按等级 4 审计。

## 7. 场景选读

```text
只写最小 Skill
  必读：skill-file.md
  按需：testing.md

做多步工作流
  必读：skill-file.md、workflow-steps.md、run-state.md
  按需：configuration.md、testing.md

加入脚本
  必读：scripts.md、run-state.md、configuration.md
  按需：setup.md、troubleshooting.md

需要外部资料或知识库
  必读：context-engineering.md、variables.md
  按需：prompts.md、credentials.md

要公开发布
  必读：security.md、testing.md、user-guide.md
  按需：platforms.md、troubleshooting.md

做复杂系统或工具包
  必读：patterns.md、configuration.md、platforms.md
  按需：output-templates.md、setup.md
```

## 8. 开发流程

### 8.1 先定义边界

先写清：

- Skill 处理什么任务。
- 不处理什么任务。
- 用户应该怎样表达。
- 哪些输入必须提供。
- 哪些能力不能公开承诺。

如果边界写不清，不要进入脚本和模板设计。

### 8.2 再设计入口

`description` 是触发质量的核心。它必须同时包含：

- 任务类型。
- 触发场景。
- 排除场景。

示例：

```yaml
description: 当用户要求审查已有 Skill 的触发质量、工作流清晰度、安全边界和发布准备度时使用。本 Skill 不用于从零创建新 Skill。
```

### 8.3 再拆工作流

超过三步的流程应拆到 `workflow/`。每个步骤单独文件，不把全部流程塞进 `SKILL.md`。

步骤文件必须有：

- 目标。
- 输入。
- 动作。
- 输出。
- 完成标准。
- 失败处理。

### 8.4 再补状态

长任务一开始就建立运行目录，不要等复杂以后再补：

```text
runs/{keyword}-YYYYMMDD-HHMMSS/
  state/
    config.json
    progress.json
  step01-prepare/
  step02-execute/
  output/
```

### 8.5 再分离脚本

重复、确定、可测试的动作写脚本。脚本输出 JSON 或文件路径，不让 Agent 从大量终端日志中解析结果。

### 8.6 最后做测试和公开审计

发布前至少完成：

- 正向触发测试。
- 负向触发测试。
- 主路径功能测试。
- 恢复测试。
- 密钥扫描。
- README 与实际行为一致性检查。

## 9. 发布门禁

公开发布前必须通过：

```text
结构
  [ ] SKILL.md 存在。
  [ ] name 和 description 清晰。
  [ ] README 写清用途和边界。
  [ ] 多步任务有 workflow/。
  [ ] 长任务有 runs/ 和 progress.json。
  [ ] 需要环境、二进制、模型或 cache 时有 config/runtime.json。
  [ ] Runtime Contract 只声明需求，不包含环境实体。

安全
  [ ] 无真实密钥。
  [ ] 无私人路径。
  [ ] 无客户数据。
  [ ] 无私有服务 URL。
  [ ] 无默认破坏性动作。
  [ ] 网络行为已记录。

测试
  [ ] 触发评测包含正例和反例。
  [ ] 功能、恢复、安全和 runtime eval 有样例。
  [ ] 主路径跑通。
  [ ] 错误和中断可恢复。
  [ ] 脚本可独立运行。
  [ ] README 未承诺未测试能力。

质量
  [ ] 已按 docs/quality-rubric.md 给出评分。
  [ ] blocked 项为零。
  [ ] 术语符合 docs/glossary.md。
  [ ] 发布记录符合 docs/release.md。
```

## 10. 反模式

### 10.1 万能助手

名字叫 `assistant`、`helper`、`toolkit`，边界不清。Agent 无法判断什么时候用。

### 10.2 入口文件过大

把全部教程、背景、模板和排错都塞进 `SKILL.md`。这会污染上下文，降低执行稳定性。

### 10.3 只写提示词

没有输入、输出、验证和状态。它可能有用，但不能冒充生产级 Skill。

### 10.4 隐藏私有依赖

示例能在作者电脑跑，但离开私有路径、账号、知识库或内部服务就失效。

### 10.5 默认执行副作用

默认删除、覆盖、上传、发布、付款、发信或修改远端系统。公开 Skill 必须默认只读或 dry-run。

### 10.6 测试只看感觉

用“效果不错”“写得专业”当验收标准。公开 Skill 需要可验证断言。

## 11. 与内部规范的关系

内部规范服务维护者个人生产环境，允许绑定个人知识库、运行库、账号路由和本机工具。公开规范服务开源读者，默认读者没有这些资源。

因此公开版采用“结构同源、依赖脱敏”的原则：

- 保留 16 模块框架。
- 保留全生命周期约束。
- 保留自动化、恢复、测试、审计思想。
- 去掉私有目录、私有凭据、私有工具、真实业务提示词和客户数据。
- 将内部运行库能力改写为通用约定或可选实现。

## 12. 最小可执行样例

一个最小 Skill 可以只有：

```text
my-skill/
  SKILL.md
```

`SKILL.md`：

```markdown
---
name: markdown-release-check
description: 当用户要求检查已有 Markdown 文件是否适合发布时使用。本 Skill 不用于写新文章、上传内容或生成图片。
license: MIT
---

# Markdown 发布前检查

## 范围

检查一个已有 Markdown 文件是否适合发布。

## 输入

- Markdown 文件路径。

## 工作流

1. 确认文件存在。
2. 读取文件。
3. 检查标题、frontmatter、链接、图片引用、代码围栏和空章节。
4. 先报告阻塞问题。
5. 用户要求修复时，只修补目标文件。
6. 重新读取并验证。

## 输出

- 阻塞问题。
- 非阻塞建议。
- 已应用修复，如有。
- 剩余风险。

## 验证

- 每条发现引用目标文件路径。
- 代码围栏成对闭合。
- 未执行发布动作。
```

## 13. 生产级样例结构

```text
public-release-reviewing/
  SKILL.md
  docs/
    setup.md
    user-guide.md
  workflow/
    step01-prepare.md
    step02-scan.md
    step03-review.md
    step04-report.md
  scripts/
    scan-secrets.sh
    check-links.sh
  config/
    default.json
  references/
    templates/
      public-release-report.md
  evals/
    trigger-queries.json
  runs/
```

这个结构适合公开发布审查、源码包审查、内容发布前审查等长流程任务。

## 14. 维护原则

- 入口保持短。
- 规范按模块拆。
- 示例必须可运行。
- 安全边界单独写。
- 测试方法单独写。
- 公开声明不超过已验证能力。
- 版本历史交给 git，不写进 `SKILL.md`。

## 15. 结论

一个好的 Skill 应该让未来的 Agent 看得懂、跑得稳、断了能续、错了能查、发布前能审计。做到这些，Skill 才从提示词变成可复用的工作流能力包。
