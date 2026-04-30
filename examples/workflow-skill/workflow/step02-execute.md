# 步骤 02：执行审查

## 目标

检查目标目录的公开发布风险。

## 输入

- `state/config.json`
- `step01-prepare/file-index.txt`

## 动作

1. 在存在时读取 README、许可证、软件包配置、脚本、示例和安装文件。
2. 搜索疑似密钥和私人路径。
3. 检查安装和使用说明是否可复现。
4. 检查示例是否使用占位数据。
5. 检查脚本是否存在破坏性默认行为。
6. 检查必需依赖是否已声明。
7. 将发现写入 `step02-execute/findings.json`。

建议使用的只读命令：

```bash
find <target> -maxdepth 3 -type f
rg -n "token|secret|password|cookie|api_key|apikey|/Users|~/Downloads|client|customer" <target>
```

可选密钥扫描：

```bash
gitleaks detect --no-git --source <target> --redact --no-banner
```

## 输出

```text
step02-execute/findings.json
step02-execute/notes.md
state/progress.json
```

## 完成标准

- 发现项区分阻塞问题和非阻塞问题。
- 每个阻塞问题都有证据和具体修复方式。
- 疑似密钥已脱敏。
- 进度状态中的 `current_step` 为 `step03-verify`。

## 失败处理

如果 `gitleaks` 不可用，继续使用文本搜索，并记录未运行专用密钥扫描器。

如果命令因权限失败，记录路径，并只继续检查可访问文件。
