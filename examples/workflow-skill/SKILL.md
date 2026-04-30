---
name: public-release-reviewing
description: 当用户要求在公开发布前审查已有仓库或软件包时使用。本 Skill 不用于创建新软件包或发布版本。
license: MIT
compatibility: 需要 shell 访问权限执行只读文件检查。可选使用 gitleaks 提升密钥扫描能力。
---

# 公开发布审查

## 范围

审查已有仓库或软件包的公开发布准备度。

不要：

- 发布仓库。
- 删除文件。
- 重写整个项目。
- 读取目标目录外的凭据。
- 完整打印疑似密钥。

## 输入

必填：

- 目标目录。

可选：

- 发布渠道。
- 风险重点。
- 用户需要仅给修复建议，还是直接修复。

## 工作流

1. 读取 `workflow/step01-prepare.md`。
2. 读取 `workflow/step02-execute.md`。
3. 读取 `workflow/step03-verify.md`。

非平凡审查使用运行目录：

```text
runs/{keyword}-YYYYMMDD-HHMMSS/
  state/
    config.json
    progress.json
  step01-prepare/
  step02-execute/
  output/
```

## 输出

最终回复顺序：

1. 发布判断。
2. 阻塞问题。
3. 非阻塞问题。
4. 建议修复。
5. 已执行验证。
6. 剩余风险。

## 安全

如果发现疑似密钥，脱敏值，只报告文件路径、键名和风险。

如果发现破坏性脚本或命令，除非默认 dry-run 且需要显式批准，否则按阻塞问题报告。
