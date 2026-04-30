# 翔宇工作流 Workflow Agent Skill 规范

> 💎 **跨平台工作流式 Agent Skill 规范** · 把重复任务沉淀成自动化、可恢复、可测试、可审计的 Workflow Agent Skill

<p>
  <img src="https://img.shields.io/badge/Workflow-Agent_Skill-FF6B35?style=for-the-badge&logo=githubactions&logoColor=white" alt="Workflow Agent Skill" />
  <img src="https://img.shields.io/badge/Agent-就绪-412991?style=for-the-badge&logo=openai&logoColor=white" alt="Agent 就绪" />
  <img src="https://img.shields.io/badge/跨平台-规范-2C3E50?style=for-the-badge" alt="跨平台规范" />
  <img src="https://img.shields.io/badge/Runtime-Contract-0E7C7B?style=for-the-badge" alt="Runtime Contract" />
  <img src="https://img.shields.io/badge/公开-安全-07C160?style=for-the-badge&logo=shield&logoColor=white" alt="公开安全" />
  <img src="https://img.shields.io/badge/MIT-许可-2C3E50?style=for-the-badge" alt="MIT 许可" />
</p>

你可以把这个仓库理解成一份“教 Agent 怎么做 Skill 的说明书”。

这里的 Workflow Agent Skill 不是一段提示词，而是一套可重复执行的工作流。比如你经常让 Agent 做深度调研、代码审查、内容发布、资料整理，就可以把这类流程做成一个 Skill，让下次执行更稳定。

本仓库不是某一个具体 Skill，也不绑定 Claude Code、Codex 或任何单一客户端。它的用途很简单：让你把这份规范交给 Agent，然后让 Agent 按规范帮你新建、审查、升级 Skill。

本仓库由翔宇工作流维护，从内部生产规范中提炼，只保留可复用、可解释、可审计、可分发的部分。它不依赖私有知识库、本机路径、真实账号、客户数据或未公开服务。

> 🎯 **不是把提示词存起来，而是把任务设计成会运行的工作流。**
> ⚡ **Agent 负责判断，脚本负责确定性，状态负责恢复，测试负责发布信心。**

---

## 🔥 解决什么问题

很多 Skill 做不好，不是因为模型不会，而是因为任务没有被设计成可执行系统：

- 触发条件太泛，Agent 不知道什么时候该用。
- `SKILL.md` 太长，真正关键的步骤被上下文淹没。
- 工作流只写愿望，没有输入、输出、完成标准和失败处理。
- 所有事情都靠提示词，确定性检查、文件扫描、格式转换没有脚本兜底。
- 长任务没有 `runs/` 和 `progress.json`，一中断就只能重来。
- 需要 runtime、模型、二进制或 cache，但没有可诊断的 Runtime Contract。
- 发布前没有触发评估、安全扫描和公开环境检查。

这套规范就是把这些问题拆清楚：什么时候触发、要问哪些输入、分几步执行、用哪些脚本、输出什么文件、失败后怎么继续、发布前怎么检查。

## 🧭 适合谁

```text
想做 Skill 的人
  把一个经常重复的任务做成稳定流程，例如深度调研、深度分析、发布检查、资料整理。

经常用 Agent 的人
  直接把本仓库发给 Agent，让它按规范帮你新建或检查 Skill。

开源维护者
  给公开仓补齐 README、Agent 项目入口、模板、示例、评测和安全边界。

团队负责人
  让团队里的 Agent 工作流有统一写法，不再每个人各写一套提示词。

课程学习者
  从“会让 Agent 做事”升级到“会把 Agent 工作流沉淀成资产”。
```

## 🤖 常用 Agent 指令

### 新建深度调研工作流

```text
我想新建一个“深度调研工作流”的 Skill。

请参考「翔宇工作流 Workflow Agent Skill 规范」来创建。

我希望这个 Skill 能做到：
- 输入一个主题。
- 自动拆解调研问题。
- 搜索和整理资料。
- 输出一份结构化调研报告。
- 记录每一步的进度，方便中断后继续。

请你按规范生成 SKILL.md、workflow/、config/runtime.json、evals/ 和必要的示例文件。
```

### 新建深度分析工作流

```text
我想新建一个“深度分析工作流”的 Skill。

请参考「翔宇工作流 Workflow Agent Skill 规范」来创建。

这个 Skill 用来分析一个项目、产品、行业或竞品。
我希望它能：
- 先确认分析目标。
- 收集必要背景。
- 分步骤输出分析结论。
- 明确证据、风险和建议。
- 最后生成一份可复用的分析报告。
```

### 检查一个已有 Skill

```text
这是一个我已经写好的 Skill。
请参考「翔宇工作流 Workflow Agent Skill 规范」帮我检查它能不能公开发布。

路径：{skill 路径}

请重点看：
- 什么时候会触发，什么时候不该触发。
- 工作流步骤是否清楚。
- 有没有隐藏的本机路径、账号、密钥或私有依赖。
- 是否支持中断恢复。
- 是否有测试样例。
- 最后给一个是否适合公开发布的结论。
```

### 把普通提示词升级成 Skill

```text
我现在只有一段提示词，想把它升级成一个可复用的 Skill。

请参考「翔宇工作流 Workflow Agent Skill 规范」帮我改。

提示词：{原提示词}

请不要只是把提示词保存起来。
请帮我补齐：
- 什么时候使用这个 Skill。
- 需要用户输入什么。
- 分几步执行。
- 输出什么结果。
- 怎么验证结果是对的。
- 如果中断了怎么继续。
```

## 📚 仓库导航

```text
workflow-agent-skill-spec/
  README.md                 公开介绍页。
  CLAUDE.md                 支持 CLAUDE.md 的 Agent 项目入口。
  AGENTS.md                 支持 AGENTS.md 的 Agent 项目入口。
  docs/                     完整规范正文。
  templates/                可复用模板。
  examples/                 最小样例和黄金样例。
  schemas/                  机器可验证契约。
  evals/                    触发、功能、恢复、安全、runtime 评测样例。
  scripts/validate-spec.py  本地验证器。
```

核心文档：

- [完整规范](docs/specification.md)
- [SKILL.md 入口规范](docs/skill-file.md)
- [workflow 步骤规范](docs/workflow-steps.md)
- [Runtime Contract 与配置](docs/configuration.md)
- [环境初始化](docs/setup.md)
- [测试与发布](docs/testing.md)
- [安全边界](docs/security.md)
- [质量评分](docs/quality-rubric.md)
- [术语表](docs/glossary.md)
- [平台适配](docs/platform-adapters.md)
- [发布与版本](docs/release.md)

## 🎓 更完整的学习路径

这份规范解决的是“怎么把 Skill 做成可执行的工作流”。如果你想系统学习从零用 AI Agent 做真实项目、搭工具链、写代码、封装工作流，可以继续看翔宇工作流的完整课程和内容。

<p>
  <a href="https://flowus.cn/xiangyugongzuoliu/share/d392dcad-b537-44ee-a3e2-56ff5af02bce">
    <img src="https://img.shields.io/badge/AI编程实操课-系统学习-FF6B35?style=for-the-badge&logo=bookstack&logoColor=white" alt="AI 编程实操课" />
  </a>
  <a href="https://xiangyugongzuoliu.com">
    <img src="https://img.shields.io/badge/官网长文-深度拆解-2C3E50?style=for-the-badge&logo=ghost&logoColor=white" alt="官网长文" />
  </a>
  <a href="https://www.youtube.com/@xiangyugongzuoliu">
    <img src="https://img.shields.io/badge/YouTube-实战演示-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube" />
  </a>
  <a href="https://github.com/xiangyugongzuoliu">
    <img src="https://img.shields.io/badge/GitHub-开源项目-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
</p>

- 🎓 **AI 编程实操课**：https://flowus.cn/xiangyugongzuoliu/share/d392dcad-b537-44ee-a3e2-56ff5af02bce
- 🌐 **翔宇工作流官网**：https://xiangyugongzuoliu.com
- ▶️ **YouTube「翔宇工作流」**：https://www.youtube.com/@xiangyugongzuoliu
- ✉️ **公众号「翔宇工作流」**：https://xiangyugongzuoliu.com/wechat/

## 📡 维护者

本规范由 **翔宇工作流** 维护。

```text
品牌：翔宇工作流
作者：翔宇
主题：AI Agent 工作流、AI 编程、自动化 Skill、开源实践
规范名：翔宇工作流 Workflow Agent Skill 规范
仓库：workflow-agent-skill-spec
```

## 📄 许可

本仓库使用 [MIT License](LICENSE)。
