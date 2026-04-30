# SKILL.md 入口规范

> 本文规范 `SKILL.md` 的命名、frontmatter、正文结构、目录边界和公开分发要求。

## 1. 职责

`SKILL.md` 是 Skill 的入口契约。它的职责不是解释所有背景，而是让 Agent 快速判断：

- 该不该使用这个 Skill。
- 怎么开始执行。
- 需要读哪些后续文件。
- 什么事情不允许做。
- 成功后应该产出什么。

入口文件应短、准、可执行。复杂细节拆到 `workflow/`、`references/`、`docs/`、`scripts/`。

## 2. 最小结构

```markdown
---
name: example-task-reviewing
description: 当用户要求审查已有任务产物的范围、安全性、完整性和发布准备度时使用。本 Skill 不用于从零创建产物。
license: MIT
compatibility: 面向跨平台 Workflow Agent Skill 客户端设计。
---

# 示例任务审查

## 范围

## 输入

## 工作流

## 文件

## 工具

## 输出

## 验证

## 失败处理
```

## 3. frontmatter

### 3.1 通用字段

```text
name
  必需。稳定、短小、小写、连字符分隔。

description
  必需。触发判断核心。写清何时用、做什么、何时不用。

license
  可选。公开仓库建议填写。

compatibility
  可选。说明运行环境或客户端兼容范围。

metadata
  可选。额外键值元数据。
```

### 3.2 平台扩展字段

不同 Agent 客户端可能支持额外字段，例如 `when_to_use`、`allowed-tools`、`hooks`、`model`、`effort`。公开规范应把这些字段写成平台扩展，而不是通用标准。

写法原则：

- 通用字段放前面。
- 平台扩展必须注明适用客户端。
- 不依赖扩展字段完成核心触发。
- 没有验证过的字段不要写入模板。

## 4. name 命名

推荐格式：

```text
{owner}-{domain}-{target}-{action}
```

说明：

- `owner`：维护者、组织或项目标识。
- `domain`：领域，例如 `content`、`dev`、`doc`、`skill`、`video`。
- `target`：对象，例如 `markdown`、`code`、`pdf`、`github`。
- `action`：动作，建议使用稳定动名词或明确动词。

公开示例可以使用：

```text
demo-markdown-release-check
example-task-reviewing
public-release-reviewing
```

避免：

```text
helper
assistant
toolkit
万能处理
```

## 5. description 写法

`description` 决定 Skill 是否会被 Agent 选中。它比正文更重要。

好的 `description` 包含三件事：

1. 任务类型。
2. 触发场景。
3. 排除场景。

推荐：

```yaml
description: 当用户要求审查已有 Skill 的触发质量、工作流清晰度、安全边界和发布准备度时使用。本 Skill 不用于从零创建新 Skill，也不执行发布操作。
```

不推荐：

```yaml
description: 一个强大的 Skill 助手。
```

问题：

- 没有任务边界。
- 没有触发场景。
- 没有排除场景。
- 容易误触发。

## 6. 正文结构

### 6.1 范围

写清 Skill 处理什么、不处理什么。

```markdown
## 范围

本 Skill 处理：

- 已有 Markdown 发布前检查。
- 链接、图片引用、frontmatter、代码围栏检查。

本 Skill 不处理：

- 从零写文章。
- 发布到外部平台。
- 生成图片。
```

### 6.2 输入

输入分三类：

```text
必填
  缺失会阻塞执行，必须询问或停止。

可选
  用户提供则使用，不提供也能运行。

可推断
  Agent 可从文件扩展名、目录结构或上下文推断。
```

原则：

- 能推断就不问。
- 不能可靠推断才问。
- 缺失必填输入时不要猜。

### 6.3 工作流

单步 Skill 可以在 `SKILL.md` 中写完整流程。超过三步，建议拆到 `workflow/`。

```markdown
## 工作流

1. 确认目标路径存在。
2. 读取必要文件。
3. 检查阻塞问题。
4. 输出报告。
5. 如用户要求修复，只修改范围内文件。
6. 重新验证。
```

### 6.4 文件

声明会读、会写、会改、不能读的文件。

```markdown
## 文件

可以读取：

- 目标文件。
- 同目录 README。
- 相关配置。

可以创建：

- 用户要求的审查报告。

可以修改：

- 只有用户明确指定的文件。

禁止读取：

- 凭据文件。
- 私人账号文件。
- 无关目录。
```

### 6.5 工具

声明会用的命令、脚本、网络访问和凭据。

工具章节可以这样写：

```text
## 工具

可运行只读检查：

  find <target> -maxdepth 3 -type f
  rg -n "token|secret|password|cookie|api_key|/Users|~/Downloads" <target>

不要运行破坏性命令。
```

### 6.6 输出

输出结构应稳定。

```markdown
## 输出

最终回复顺序：

1. 发布判断。
2. 阻塞问题。
3. 非阻塞问题。
4. 建议修复。
5. 已执行验证。
6. 剩余风险。
```

### 6.7 验证

验证必须具体。

```markdown
## 验证

- 目标路径存在。
- 每个阻塞问题都有证据。
- 未完整打印真实密钥。
- 修改后的文件已重新读取。
```

### 6.8 失败处理

失败处理要说明停止条件和恢复方式。

```markdown
## 失败处理

如果目标路径不存在，停止并要求用户提供有效路径。

如果疑似密钥被发现，脱敏值，只报告文件路径、键名和风险。
```

## 7. 目录结构

### 7.1 最小 Skill

```text
my-skill/
  SKILL.md
```

适合：

- 单文件检查。
- 小型审查。
- 简单格式转换。

### 7.2 工作流式 Skill

```text
my-skill/
  SKILL.md
  workflow/
    step01-prepare.md
    step02-execute.md
    step03-verify.md
  runs/
```

适合：

- 多步骤任务。
- 长任务。
- 可恢复任务。

### 7.3 脚本支撑型 Skill

```text
my-skill/
  SKILL.md
  workflow/
  scripts/
  config/
  references/
  examples/
  runs/
```

适合：

- 批处理。
- 文件扫描。
- 数据采集。
- 报告生成。

### 7.4 生产级 Skill

```text
my-skill/
  SKILL.md
  docs/
    setup.md
    user-guide.md
  workflow/
  scripts/
  config/
  references/
    templates/
    presets/
    definitions/
  evals/
  runs/
```

适合：

- 对外分发。
- 团队复用。
- 长期维护。

## 8. 独立性级别

公开 Skill 应区分两类：

```text
personal
  个人型。可以绑定个人知识库、目录习惯、账号路由。
  不适合直接公开分发。

portable
  可分发型。默认读者没有作者环境。
  必须自包含或显式声明依赖。
```

公开仓库中的示例默认按 `portable` 设计。

## 9. 生命周期

### 9.1 创建

先写最小 `SKILL.md`，只解决一个明确任务。

### 9.2 验证

用真实输入跑通主路径，记录失败点。

### 9.3 拆分

入口变长、步骤变多、产物变复杂时，拆出 `workflow/`、`references/`、`scripts/`。

### 9.4 发布

删除内部依赖，补 README、许可证、示例、安全边界和测试说明。

### 9.5 迭代

围绕失败案例改，不凭灵感重写全部。

### 9.6 废弃

废弃 Skill 时，在 README 或归档说明中写明替代方案。不要让废弃入口继续被 Agent 误触发。

## 10. 禁止事项

- 在 `SKILL.md` 中写真实密钥。
- 在 `SKILL.md` 中维护长版本历史。
- 在 `SKILL.md` 中堆全部教程。
- 用宽泛名称和宽泛 description。
- 默认执行破坏性操作。
- 公开示例依赖作者本机路径。
- 让 Skill 隐式读取私人账号或客户数据。

## 11. 检查清单

```text
入口
  [ ] name 稳定。
  [ ] description 写清触发和排除。
  [ ] 范围清楚。
  [ ] 输入分为必填、可选、可推断。

执行
  [ ] 工作流步骤明确。
  [ ] 文件边界明确。
  [ ] 工具边界明确。
  [ ] 输出结构稳定。

安全
  [ ] 无真实凭据。
  [ ] 无私人路径。
  [ ] 无客户数据。
  [ ] 无默认破坏性动作。

公开
  [ ] 示例可复现。
  [ ] README 不过度承诺。
  [ ] 安全和测试文档已同步。
```
