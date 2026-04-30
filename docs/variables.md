# 变量与占位符规范

> 本文规范 Skill 中变量、占位符、路径引用、来源标注和最新指针的写法。

## 1. 职责

变量用于连接用户输入、配置、步骤产物和模板。变量规范解决：

- 变量叫什么。
- 变量从哪里来。
- 变量何时解析。
- 变量缺失怎么办。
- 变量如何避免歧义。

## 2. 变量来源

```text
用户输入
  由用户本次请求提供。

Agent 推断
  从路径、文件名、扩展名、上下文推断。

默认配置
  来自 config/default.json。

预设数据
  来自 references/presets/ 或 definitions/。

步骤产物
  来自 runs/{keyword}/stepNN-*/。
```

每个关键变量应能追踪来源。

## 3. 命名规则

推荐：

```text
target_path
target_dir
input_type
output_format
run_dir
current_step
keyword
mode
```

规则：

- 使用小写。
- 使用下划线。
- 避免缩写。
- 同一含义只用一个变量名。
- 路径变量以 `_path` 或 `_dir` 结尾。

## 4. 占位符写法

文档中可用：

```text
{target_path}
{run_dir}
{keyword}
{mode}
```

占位符必须在同一文档或相关配置中说明来源。

不推荐：

```text
{x}
{data}
{thing}
```

## 5. 禁止变量算术

不要写：

```text
{round_num-1}
{version+1}
{step-previous}
```

需要上一轮或最新产物时，使用指针文件：

```text
feedback_latest.md
draft_latest.md
report_latest.json
```

## 6. 路径变量

路径变量应明确相对谁。

```text
skill_dir
  Skill 根目录。

run_dir
  本次运行目录。

target_path
  用户指定目标。

output_dir
  最终输出目录，通常为 {run_dir}/output。
```

公开示例使用占位路径：

```text
/path/to/your/project
/path/to/input.md
```

不要使用作者真实路径。

## 7. 来源标注

推荐在 `state/config.json` 中记录来源：

```json
{
  "target_path": "/path/to/project",
  "target_path_source": "user",
  "input_type": "directory",
  "input_type_source": "inferred_from_path",
  "output_format": "markdown",
  "output_format_source": "default"
}
```

## 8. 缺失变量

处理规则：

```text
必需变量缺失
  停止并询问。

可推断变量缺失
  尝试从上下文推断。

可默认变量缺失
  使用 config/default.json。

可选变量缺失
  跳过，并记录默认行为。
```

## 9. 模板变量

模板变量应有默认或失败策略。

```text
{{ title }}
  必填。缺失时报错。

{{ summary }}
  可选。缺失时不渲染该段。

{{ generated_at }}
  默认当前运行时间。
```

## 10. 禁止事项

- 变量没有来源说明。
- 同一变量多种命名。
- 用变量算术表示上一轮。
- 在公开示例中使用真实路径。
- 把凭据值当变量传入模板。
- 把复杂逻辑藏在变量名里。

## 11. 检查清单

```text
命名
  [ ] 变量名清晰。
  [ ] 路径变量后缀明确。
  [ ] 同一含义没有重复名称。

来源
  [ ] 必需变量有来源。
  [ ] 推断变量有来源标注。
  [ ] 默认变量有默认配置。

安全
  [ ] 不含真实路径。
  [ ] 不含凭据值。
  [ ] 不使用变量算术。
```
