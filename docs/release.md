# 发布与版本规范

> 本文定义 Workflow Agent Skill 规范仓库和具体 Skill 的版本、发布门禁、迁移和废弃规则。

## 1. 版本号

推荐使用语义化版本：

```text
MAJOR.MINOR.PATCH
```

含义：

```text
MAJOR
  破坏性规范变更，例如目录结构、必需字段或 runtime schema 不兼容。

MINOR
  向后兼容新增能力，例如新增模板、评测类型或可选字段。

PATCH
  文档修正、示例修复、validator bugfix。
```

## 2. 发布门禁

发布前必须通过：

```text
结构
  [ ] README、SKILL.md、docs、templates、examples、evals 一致。
  [ ] schema 可解析。
  [ ] validator 通过。

安全
  [ ] gitleaks 通过。
  [ ] 私有路径和凭据关键词已人工复核。
  [ ] 公开示例不含客户数据。

运行
  [ ] 黄金样例脚本可运行。
  [ ] runtime 模板可解析。
  [ ] progress.json 符合 schema。

评测
  [ ] trigger eval 正负例齐全。
  [ ] function / recovery / security / runtime eval 有样例。
  [ ] README 没有承诺未验证能力。
```

## 3. 变更记录

每次发布应记录：

```text
Added
  新增规范、模板、schema、示例。

Changed
  改动已有规范行为。

Fixed
  修复错误、歧义或示例问题。

Security
  与安全边界、凭据、公开审计相关的改动。

Migration
  用户从旧版本迁移到新版本需要做的事。
```

## 4. 破坏性变更

破坏性变更必须：

- 提升 MAJOR 版本。
- 在 CHANGELOG 标明。
- 给迁移步骤。
- 保留旧字段说明至少一个小版本周期。
- validator 输出可理解的错误。

## 5. 废弃规则

废弃一个字段、文件或目录时：

```text
Deprecated
  标明从哪个版本开始废弃。

Replacement
  给替代方案。

Removal
  标明最早移除版本。
```

不要直接删除仍被示例或模板引用的内容。

## 6. 检查清单

```text
[ ] 版本号符合变更类型。
[ ] CHANGELOG 已更新。
[ ] 发布门禁全部通过。
[ ] 破坏性变更有迁移说明。
[ ] 废弃项有替代方案。
```
