# 脚本与工具规范

> 本文规范 Skill 中 `scripts/`、CLI、MCP、网络 API 和外部工具的使用边界。

## 1. 职责

脚本负责确定性、可重复、可测试的工作。Agent 负责理解、判断和修复建议。

适合脚本：

- 扫描文件。
- 校验 JSON。
- 检查链接。
- 解析输入。
- 批量转换。
- 生成报告。
- 合并结果。
- 执行密钥扫描。

不适合脚本：

- 判断文章好不好。
- 解释需求意图。
- 选择创作策略。
- 生成需要语义判断的结论。

## 2. 目录结构

```text
scripts/
  python/
    *.py
    pyproject.toml
  node/
    *.mjs
    package.json
  shell/
    *.sh
```

按需创建，不为了完整而创建空目录。

## 3. 运行原则

- 脚本可独立运行。
- 输入通过参数或配置文件传入。
- 输出写到运行目录。
- 终端只打印摘要。
- 返回值机器可解析。
- 失败时退出码非零。

## 4. 返回格式

推荐 JSON：

```json
{
  "ok": true,
  "output": "step02-execute/findings.json",
  "count": 12
}
```

失败：

```json
{
  "ok": false,
  "err": "target directory does not exist",
  "recoverable": true
}
```

规则：

- `ok: true` 对应退出码 0。
- `ok: false` 对应非零退出码。
- `err` 不打印密钥或敏感值。
- 输出文件路径相对运行目录或 Skill 根目录。

## 5. Python 脚本

推荐结构：

```python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def run(target: Path, output: Path) -> dict[str, object]:
    if not target.exists():
        return {"ok": False, "err": "target does not exist", "recoverable": True}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("{}", encoding="utf-8")
    return {"ok": True, "output": str(output)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = run(Path(args.target), Path(args.output))
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

## 6. Shell 脚本

Shell 脚本必须：

- 首行使用 shebang。
- 第二行使用 `set -euo pipefail`。
- 参数缺失时报错。
- 默认只读或 dry-run。
- 输出明确路径。

模板：

```bash
#!/usr/bin/env bash
set -euo pipefail

target="${1:?target required}"
output="${2:?output required}"

find "$target" -maxdepth 3 -type f > "$output"
```

## 7. 依赖声明

依赖必须显式声明。

```text
Python
  pyproject.toml 或脚本内联依赖声明。

Node.js
  package.json。

Shell
  setup 文档列出必需命令。
```

不要让脚本隐式依赖维护者机器上的全局包。

## 8. 网络请求

任何网络访问都必须记录：

- 访问哪个主机。
- 是否发送用户数据。
- 超时时间。
- 重试次数。
- 频率限制。
- 离线或 dry-run 行为。

默认规则：

```text
timeout
  必须设置。

retry
  只重试可恢复错误。

4xx
  不盲目重试，输出明确原因。

5xx
  可有限重试。

rate limit
  按服务返回等待，或停止并记录。
```

## 9. 凭据读取

脚本不直接写真实密钥。

推荐：

```text
从环境变量读取。
从用户提供的配置路径读取。
从客户端安全凭据系统读取。
```

示例配置：

```json
{
  "provider": "example",
  "api_key_env": "EXAMPLE_API_KEY"
}
```

缺失凭据时：

- 如果任务可 dry-run，进入 dry-run。
- 如果任务必须凭据，停止并说明缺哪个环境变量。
- 不提示用户在公开文件里写 key。

## 10. 脚本与 Agent 分工

```text
脚本做
  - 扫描。
  - 解析。
  - 转换。
  - 校验。
  - 合并。
  - 渲染。

Agent 做
  - 判断严重程度。
  - 解释影响。
  - 选择修复方案。
  - 写审查报告。
  - 处理无法结构化的例外。
```

## 11. 幂等性

脚本应尽量幂等：

- 同样输入多次运行，输出一致。
- 不依赖当前工作目录。
- 不覆盖无关文件。
- 输出写到指定路径。
- 临时文件写入运行目录。

## 12. 破坏性操作

删除、覆盖、上传、发布、发信、修改远端系统都属于破坏性操作。

规则：

- 默认 `dry_run: true`。
- 执行前生成计划。
- 需要用户明确批准。
- 实际动作写入运行目录。
- 失败后能回滚或说明无法回滚。

公开示例不要默认包含破坏性脚本。

## 13. 调用方式

步骤文件中只写调用命令和输入输出，不粘贴完整脚本代码。

```text
## 脚本执行

python scripts/python/scan.py --target "$TARGET" --output step02-scan/result.json

## 输出

- step02-scan/result.json
```

## 14. 禁止事项

- 脚本硬编码真实密钥。
- 脚本硬编码作者绝对路径。
- 脚本默认删除或上传。
- 脚本失败后返回成功。
- 脚本打印完整密钥。
- 脚本把大量日志当作唯一产物。
- 脚本依赖未声明的全局环境。

## 15. 检查清单

```text
结构
  [ ] scripts/ 只包含实际使用脚本。
  [ ] 依赖已声明。
  [ ] 脚本可独立运行。

输入输出
  [ ] 参数明确。
  [ ] 输出写入指定路径。
  [ ] 返回 JSON 或明确状态。

安全
  [ ] 无硬编码密钥。
  [ ] 无私人路径。
  [ ] 网络请求有超时。
  [ ] 破坏性动作默认 dry-run。

错误
  [ ] 失败退出码非零。
  [ ] 错误信息可修复。
  [ ] 不打印敏感值。
```
