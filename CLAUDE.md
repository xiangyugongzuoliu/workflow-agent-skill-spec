# 翔宇工作流 Workflow Agent Skill 规范

> AI Agent 和维护者的项目总入口。
> 本文件是本仓库的项目上下文事实源。`AGENTS.md` 是另一个客户端入口，指回本文件，避免维护两套说明。

## 项目目的

本仓库定义一套面向公开发布的「翔宇工作流 Workflow Agent Skill 规范」。

它帮助维护者把可重复执行的 AI Agent 工作流沉淀成步骤化、可恢复、可验证、可审计的 Workflow Agent Skill，并确保这些 Skill：

- 触发边界清楚。
- 入口足够短，方便 Agent 加载。
- 可以安全公开分发。
- 可以用真实样例测试。
- 中断后可以恢复。
- 发布前可以审计。

本仓库不包含私有工作流、凭据、账号路由、客户数据或维护者本机专属路径。

## 事实源

```text
CLAUDE.md
  Agent 项目上下文事实源。

AGENTS.md
  支持 AGENTS.md 的 Agent 客户端入口。只指向本文件，不重复维护项目事实。

README.md
  面向公开读者的入口。

docs/specification.md
  完整总规范：16 模块框架、质量分级、场景选读和发布门禁。

docs/skill-file.md
  SKILL.md 入口、frontmatter、目录结构、分发边界和生命周期。

docs/workflow-steps.md
  workflow 步骤命名、执行者、输入输出、验证和调度。

docs/context-engineering.md
  上下文分层、直读、检索、隔离和输出结构。

docs/scripts.md
  scripts/、CLI、MCP、网络 API 和外部工具边界。

docs/platforms.md
  Agent 客户端能力差异和兼容写法。

docs/run-state.md
  runs/、state/、output/、progress.json 和恢复流程。

docs/configuration.md
  L1/L2/L3 配置分层、默认值、预设数据和 runtime 声明。

docs/prompts.md
  Agent 提示词、SubAgent 提示词、输出格式和失败处理。

docs/variables.md
  变量、占位符、来源标注和最新指针。

docs/credentials.md
  凭据占位、环境变量、权限范围和缺失行为。

docs/output-templates.md
  Markdown、JSON、HTML 输出模板和变量占位符。

docs/setup.md
  安装位置、依赖准备、运行时检查和环境修复。

docs/user-guide.md
  面向使用者的入门说明结构。

docs/troubleshooting.md
  错误分类、诊断顺序、重试策略和恢复检查。

docs/security.md
  公开发布安全边界。

docs/testing.md
  触发、功能、恢复、安全、回归、跨模型和发布测试。

docs/patterns.md
  设计模式、组合方式和反模式。

docs/quality-rubric.md
  百分制评分、等级裁决和阻塞项。

docs/glossary.md
  术语表。规定 Agent、Skill、Workflow Agent Skill、SubAgent、runtime 等专有名词边界。

docs/platform-adapters.md
  Claude Code、Codex、Cursor、OpenCode、Gemini CLI 等平台的条件式适配示例。

docs/release.md
  版本号、发布门禁、变更记录、迁移和废弃规则。

schemas/
  Skill metadata、progress、runtime、trigger eval 的 JSON Schema。

templates/
  可复用模板。

scripts/
  无第三方依赖的规范验证脚本。

examples/
  最小 Skill、多步工作流 Skill 和黄金样例。

evals/
  触发、功能、恢复、安全和 runtime 评估样例。

CHANGELOG.md
  版本变更记录。
```

## 编辑规则

- 公开安全优先：禁止真实凭据、私有路径、客户数据、私有 URL、付费内容。
- 不写维护者本机绝对路径。
- 不新增默认破坏性脚本；如确实需要，必须默认 `dry-run`，并写清审批边界。
- `README.md` 保持短入口，长规则放进 `docs/`。
- 示例里的 `SKILL.md` 要足够短，方便 Agent 加载。
- 优先写可验证示例，不写空泛概念。
- 修改模板时，同步更新或新增对应示例。
- 修改发布行为时，同步更新 `docs/security.md` 或 `docs/testing.md`。
- 修改仓库结构时，同步更新 `README.md` 和本文件。

## 质量标准

高质量 Skill 应该让未来的 Agent 能够：

1. 判断什么时候触发。
2. 判断什么时候不触发。
3. 解析必需输入。
4. 执行文档化工作流。
5. 长任务中持久化状态。
6. 中断后恢复。
7. 验证输出。
8. 发布前审计安全边界。

如果一个工作流不能测试、不能恢复、不能审计，就还不是生产级 Skill。

## 验证命令

在仓库根目录运行：

```bash
python3.12 scripts/validate-spec.py --root .
gitleaks detect --no-git --source . --redact --no-banner
find . -path ./.git -prune -o -name "*.json" -print0 | xargs -0 -n1 python3.12 -m json.tool >/dev/null
```

宽泛安全检索：

```bash
rg -n "token|secret|password|cookie|api_key|apikey|client|customer|/Users|~/Downloads|private" .
```

这条检索会故意命中文档里的示例命令。发布前需要人工复核每个命中项。

## Agent 读取顺序

维护仓库时：

1. 读 `CLAUDE.md`。
2. 读 `README.md`。
3. 按任务读取 `docs/`、`templates/`、`examples/` 或 `evals/` 下的具体文件。

处理 Skill 设计问题时：

1. 读 `README.md`。
2. 读 `docs/specification.md`。
3. 对照 `templates/SKILL.md` 和 `examples/`。

做发布检查时：

1. 读 `docs/security.md`。
2. 读 `docs/testing.md`。
3. 跑验证命令。

## 公开发布边界

只有满足以下条件，本仓库才可公开发布：

- 密钥扫描没有未处理发现。
- 示例数据是通用占位数据。
- 不依赖私有本机路径。
- README 没有承诺未经测试的能力。
- 根目录存在本仓库维护所需的 `CLAUDE.md` 和 `AGENTS.md`，且两者职责不冲突。
- 模板、示例和 README 中描述的结构一致。

## 维护者

翔宇工作流

- 官网：https://xiangyugongzuoliu.com
- GitHub：https://github.com/xiangyugongzuoliu
