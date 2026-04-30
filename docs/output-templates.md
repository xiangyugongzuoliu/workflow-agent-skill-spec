# 输出模板规范

> 本文规范 Skill 的 Markdown、JSON、HTML 等输出模板结构和变量占位符。

## 1. 职责

输出模板用于稳定产物结构，让结果可读、可验证、可复用。

适合模板化：

- 审查报告。
- 发布前检查报告。
- JSON 结果。
- HTML 报告。
- 用户说明。
- 修复计划。

## 2. 模板位置

```text
references/templates/
  report.md
  findings.schema.json
  dashboard.html
```

或者简单项目：

```text
templates/
  report.md
```

同一仓库应保持一致，并在 README 或 `SKILL.md` 中说明。

## 3. Markdown 报告模板

```markdown
# {title}

## 判断

{decision}

## 阻塞问题

{blocking_issues}

## 非阻塞问题

{non_blocking_issues}

## 建议修复

{suggested_fixes}

## 已执行验证

{verification}

## 跳过的检查

{skipped_checks}

## 剩余风险

{remaining_risk}
```

规则：

- 章节顺序稳定。
- 空章节也要写明“无”或“未检查”。
- 审查类报告先写阻塞问题。
- 证据写文件路径，不打印敏感值。

## 4. JSON 输出模板

```json
{
  "decision": "blocked",
  "blocking_issues": [],
  "non_blocking_issues": [],
  "suggested_fixes": [],
  "verification": [],
  "skipped_checks": [],
  "remaining_risk": []
}
```

规则：

- 字段稳定。
- 类型稳定。
- 空数组用 `[]`。
- 缺失信息用 `null` 或明确状态，不省略关键字段。

## 5. HTML 模板

HTML 模板适合可视化报告。

规则：

- 模板放 `references/templates/`。
- 数据从 JSON 注入。
- 样式自包含或明确引用。
- 不内嵌远端追踪脚本。
- 不泄漏本地路径。

基础结构：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
  </head>
  <body>
    <main>
      <h1>{{ title }}</h1>
      <section>{{ summary }}</section>
    </main>
  </body>
</html>
```

## 6. 变量占位符

推荐：

```text
{{ title }}
{{ decision }}
{{ generated_at }}
{{ blocking_issues }}
```

规则：

- 占位符有来源。
- 缺失时有默认或报错。
- 不把凭据作为模板变量。
- 不在模板中执行任意代码。

## 7. 列表渲染

如果模板引擎支持循环，应写清字段结构。

```text
blocking_issues[]
  severity
  file
  evidence
  impact
  fix
```

如果不使用模板引擎，由 Agent 或脚本生成完整 Markdown。

## 8. 机器可验证

输出应支持自动检查：

- JSON 可解析。
- 必需字段存在。
- 报告章节齐全。
- 文件路径存在或注明无法访问。
- 密钥值已脱敏。

## 9. 禁止事项

- 输出结构每次变化。
- 空章节直接删除。
- 把完整密钥渲染进报告。
- 把作者本机路径渲染进公开示例。
- HTML 模板默认加载未知远端脚本。
- 模板逻辑复杂到无法测试。

## 10. 检查清单

```text
结构
  [ ] 模板位置清晰。
  [ ] 章节顺序稳定。
  [ ] JSON 字段稳定。

变量
  [ ] 占位符有来源。
  [ ] 缺失值有处理策略。
  [ ] 不包含凭据变量。

验证
  [ ] JSON 可解析。
  [ ] 报告章节齐全。
  [ ] 敏感值已脱敏。
```
