# 环境初始化规范

> 本文规范 Skill 如何说明安装位置、依赖准备、运行时检查、可选模型资产和修复流程。

## 1. 职责

setup 文档回答：

- Skill 放在哪里。
- 需要哪些运行时。
- 需要哪些命令。
- 需要哪些环境变量。
- 如何验证环境。
- 缺依赖时如何修复。

公开 Skill 不应默认修改系统环境。

## 2. 何时需要 setup 文档

需要 setup 文档：

- Skill 有脚本。
- Skill 有外部依赖。
- Skill 需要网络 API。
- Skill 需要本地二进制。
- Skill 需要模型资产。
- Skill 有可选凭据。

不一定需要：

- 只有一个 `SKILL.md`。
- 不运行脚本。
- 不访问网络。

## 3. 标准结构

```markdown
# 环境初始化

## 安装位置

## 运行时要求

## 依赖检查

## 依赖安装

## Runtime Contract

## Runtime doctor

## Runtime prepare

## 凭据配置

## 验证命令

## 常见错误
```

## 4. 安装位置

说明用户应把 Skill 放在哪里，但不要只写一个平台。

示例：

```text
将本目录放入你的 Agent 客户端支持的 Skill 目录。
不同客户端路径不同，以客户端文档为准。
```

如果是某个 Agent 客户端的特定说明，应标明适用范围，例如 Claude Code、Codex、Cursor 或其他客户端。

## 5. 运行时要求

如果 Skill 包含 `config/runtime.json`，setup 文档必须先说明 Runtime Contract 的位置和职责：

```text
Runtime Contract
  文件：config/runtime.json
  职责：声明运行时、二进制、模型、cache 和网络需求。
  边界：只保存声明，不保存 .venv、node_modules、模型权重或 provider cache。
```

示例：

```text
Python
  需要 Python 3.11 或更高。

Shell
  需要 bash 或 zsh。

可选命令
  gitleaks：用于密钥扫描。
```

## 6. Runtime doctor

doctor 只诊断，不修改环境、不下载模型、不写系统目录。

如果存在 runtime manager，setup 文档可以给占位命令：

```bash
<runtime-manager> skill doctor .
```

如果没有 runtime manager，给等价手动检查：

```bash
python3 --version
node --version
command -v rg
command -v gitleaks
```

doctor 输出应说明：

- 缺哪个 env。
- 缺哪个 binary。
- 缺哪个 model。
- 哪个 cache 不可写或被污染。
- 缺失项是否阻塞主流程。

## 7. Runtime prepare / repair

prepare 和 repair 必须由用户显式执行，不应在 Skill 执行中静默触发。

```bash
<runtime-manager> skill prepare . --profile standard
<runtime-manager> skill repair . --profile standard
```

没有 runtime manager 时，setup 文档应给分步手动准备方式，并写清哪些步骤会联网、下载模型或写入本机 cache。

禁止：

- 自动安装全局依赖。
- 自动下载大型模型。
- 自动修改 shell 配置。
- 自动写入系统目录。
- 在脚本里临时回退系统 Python 继续执行生产流程。

## 8. 依赖检查

只检查，不修改：

```bash
python3 --version
command -v rg
command -v gitleaks
```

检查结果应告诉用户：

- 缺什么。
- 是否必需。
- 缺失后哪些功能不可用。

## 9. 依赖安装

公开 Skill 可给安装建议，但不应默认自动安装。

示例：

```text
macOS 可通过 Homebrew 安装 gitleaks。
Linux 可参考 gitleaks 官方安装文档。
```

不要写只能在作者机器运行的命令。

## 10. 凭据配置

引用 [credentials.md](credentials.md)。

写清：

- 环境变量名。
- 权限范围。
- 缺失行为。
- dry-run 是否可用。

## 11. 模型资产

如果 Skill 需要本地模型或大型资产：

- 写清资产名称。
- 写清用途。
- 写清来源。
- 写清许可证限制。
- 不把大型资产提交到公开仓库。
- 缺失时给出明确错误。

公开仓库默认不自动下载大型模型。

如果 `config/runtime.json` 声明了模型，setup 文档应列出：

```text
模型 ID
  与 runtime.json 中 models[].id 一致。

角色 role
  例如 asr-default、ocr-default、embedding-default。

用途 kind
  例如 asr、ocr、embedding、vision。

是否必需
  required=true 时缺失必须停止。

校验
  sha256、license、source 必须可追溯。
```

## 12. cache 与网络

如果 Skill 使用 provider cache 或网络访问，setup 文档应写清：

- cache 是否允许。
- cache 是否同步。
- cache 损坏如何清理或修复。
- 需要访问哪些 host。
- 离线时停止还是降级。
- 降级后哪些输出不再保证完整。

公开 Skill 不应要求读者使用作者本机 cache。

## 13. 验证命令

每个 setup 文档都应给验证命令。

```bash
python3 -m json.tool templates/progress.json >/dev/null
gitleaks detect --no-git --source . --redact --no-banner
```

验证命令应只读。

## 14. 修复流程

推荐结构：

```text
问题：缺少 gitleaks
影响：无法运行专用密钥扫描
处理：继续使用文本搜索，或安装 gitleaks 后重试
```

Runtime 错误建议使用结构化写法：

```json
{
  "ok": false,
  "error_type": "runtime_missing",
  "message": "required model is not prepared",
  "fix": "运行 setup.md 中的 Runtime prepare 步骤。"
}
```

## 15. 禁止事项

- 默认安装全局依赖。
- 默认下载大型模型。
- 默认修改 shell 配置。
- 默认写入系统目录。
- 安装步骤需要作者私有账号。
- 把真实凭据写进 setup 文档。
- 把 Runtime 实体目录提交到 Skill 仓库。
- 缺 Runtime 时静默回退到系统环境。

## 16. 检查清单

```text
安装
  [ ] 安装位置说明清楚。
  [ ] 必需依赖和可选依赖分开。
  [ ] 依赖检查命令只读。

Runtime
  [ ] config/runtime.json 的职责已说明。
  [ ] doctor 只读。
  [ ] prepare/repair 需要用户显式执行。
  [ ] env、binary、model、cache、network 都有缺失行为。
  [ ] 不提交 .venv、node_modules、模型权重或 provider cache。

凭据
  [ ] 环境变量名明确。
  [ ] 缺失凭据行为明确。

安全
  [ ] 不自动修改系统。
  [ ] 不自动下载大型资产。
  [ ] 不包含真实密钥。
```
