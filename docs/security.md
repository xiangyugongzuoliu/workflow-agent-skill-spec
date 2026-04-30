# 安全边界

本文定义公开 Agent Skill 仓库可以包含什么、不能包含什么。

默认规则很简单：公开 Skill 应该在不访问维护者私人机器、私人知识库、客户数据或账号的情况下，也能被理解、安装和审计。

## 允许

公开 Skill 可以包含：

- 通用工作流。
- 公开文档链接。
- 占位配置。
- 环境变量名。
- 最小示例数据。
- 模板和 schema。
- 可在干净环境运行的脚本。
- 对用户输入路径的引用。

示例：

```json
{
  "api_key_env": "EXAMPLE_API_KEY",
  "source_dir": "/path/to/your/project",
  "dry_run": true
}
```

## 不允许

公开 Skill 不能包含：

- 真实 API key、token、cookie、密码或会话数据。
- 客户名称、客户文件、委托方数据集或私人截图。
- `/Users/name/...` 这类个人绝对路径或私人工作区路径。
- 内部服务 URL、私有端点或非公开 CLI 名称。
- 账号路由、凭据位置或付费内容副本。
- 默认删除、覆盖、上传、发布或发送数据的脚本。
- 依赖未公开私人知识的提示词。

## 凭据规则

使用环境变量或占位 JSON 文件。

推荐：

```json
{
  "provider": "example",
  "api_key_env": "EXAMPLE_API_KEY"
}
```

不推荐：

```json
{
  "api_key": "sk-real-key"
}
```

如果 Skill 需要凭据，应记录：

1. 需要哪个环境变量。
2. 需要什么权限范围。
3. 凭据缺失时会发生什么。
4. 是否可以在无凭据的 dry-run 模式下运行。

## 文件系统规则

示例只能使用占位路径：

```text
/path/to/your/project
/path/to/input.md
```

不要包含：

```text
/Users/example/private-client
~/Downloads/private-workspace
```

如果脚本需要 Skill 目录，使用运行时变量或脚本相对路径，不使用维护者专属绝对路径。

## 网络规则

任何执行网络访问的 Skill 都必须记录：

- 访问哪个主机或 API。
- 请求是否发送用户数据。
- 超时行为。
- 重试行为。
- 频率限制行为。
- 离线或 dry-run 兜底方式。

网络脚本应失败即关闭。请求失败时应产生清晰错误和可恢复状态，不能静默跳过步骤。

## 破坏性操作

破坏性操作包括：

- 删除文件。
- 覆盖用户文件。
- 移动大型目录。
- 上传文件。
- 发布内容。
- 发送邮件或消息。
- 修改远端基础设施。

规则：

1. 默认 `dry_run: true`。
2. 执行前生成计划。
3. 根据真值源验证计划。
4. 在 Agent 客户端支持时要求用户明确批准。
5. 将实际发生的动作写入运行目录。

## 发布前扫描

发布前从仓库根目录运行：

```bash
python3.12 scripts/validate-spec.py --root .
gitleaks detect --no-git --source . --redact --no-banner
rg -n "token|secret|password|cookie|api_key|apikey|client|customer|/Users|~/Downloads|private" .
find . -name ".env*" -o -name "*cookie*" -o -name "*token*"
```

搜索范围故意较宽。命中不一定就是泄漏，但发布前必须逐条审查。

## 人工审查清单

```text
[ ] 无真实凭据。
[ ] 无私人路径。
[ ] 无客户或委托方数据。
[ ] 无私有服务 URL。
[ ] 基础使用不依赖未发布的内部命令。
[ ] 破坏性操作默认 dry-run。
[ ] 已记录网络行为。
[ ] 示例使用占位数据。
[ ] 脚本可在干净环境运行，或清楚记录依赖。
[ ] README 未承诺不支持的行为。
```

## 报告安全问题

如果你在本仓库发现安全问题，优先通过 GitHub 安全公告提交私密报告。若不可用，请创建 GitHub Issue，只描述受影响文件和风险，不粘贴仍然有效的密钥。
