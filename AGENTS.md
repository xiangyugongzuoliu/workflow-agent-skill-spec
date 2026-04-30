# 翔宇工作流 Workflow Agent Skill 规范

本文件是支持 `AGENTS.md` 的 Agent 客户端入口。

进入本仓库后，先读 `CLAUDE.md`。`CLAUDE.md` 是本仓库的项目上下文事实源。

## 必要上下文

- 项目目的：公开版「翔宇工作流 Workflow Agent Skill 规范」。
- 核心用途：让 Agent 参考本仓库新建、审查、升级跨平台工作流式 Skill。
- 公开安全边界：禁止密钥、私有路径、客户数据、私有 URL、维护者专属依赖。
- 公开读者入口：`README.md`。
- 完整规范：`docs/specification.md`。
- 核心模块：`docs/skill-file.md`、`docs/workflow-steps.md`、`docs/context-engineering.md`、`docs/scripts.md`、`docs/run-state.md`、`docs/configuration.md`。
- 辅助模块：`docs/variables.md`、`docs/credentials.md`、`docs/output-templates.md`、`docs/setup.md`、`docs/user-guide.md`、`docs/troubleshooting.md`、`docs/patterns.md`。
- 治理模块：`docs/quality-rubric.md`、`docs/glossary.md`、`docs/platform-adapters.md`、`docs/release.md`。
- 安全规则：`docs/security.md`。
- 测试规则：`docs/testing.md`。
- 机器契约：`schemas/`。
- 本地验证：`scripts/validate-spec.py`。
- 可复用模板：`templates/`。
- 示例：`examples/`。
- 评估样例：`evals/`。

## 维护规则

- 以 `CLAUDE.md` 为事实源。
- 不在本文件重复维护长项目说明。
- 仓库结构变化时，同步更新 `CLAUDE.md` 和 `README.md`。
- 发布行为变化时，同步更新 `docs/security.md` 或 `docs/testing.md`。
- 模板变化时，同步更新或新增对应示例。
- 发布前运行 `CLAUDE.md` 中列出的验证命令。
