# 配置分层规范

> 本文规范 Skill 的运行参数、默认配置、预设数据和 runtime 声明。

## 1. 职责

配置规范解决：

- 哪些参数每次运行都不同。
- 哪些参数是默认值。
- 哪些选项是静态预设。
- 参数如何合并。
- 什么不能写进配置。

配置不是运行状态，也不是凭据仓库。

## 2. 三层模型

```text
L1 运行时参数
  每次运行不同。
  存入 state/config.json。

L2 默认配置
  Skill 自带默认值。
  存入 config/default.json。

L3 预设数据
  可选项、枚举、模板变量。
  存入 references/presets/ 或 references/definitions/。
```

优先级：

```text
用户输入 > Agent 推断 > state/config.json > config/default.json > 脚本内置默认
```

## 3. L1 运行时参数

适合放入 `state/config.json`：

- 目标路径。
- 本次模式。
- 本次关键词。
- 用户选择的输出格式。
- Agent 推断出的输入类型。
- 本次运行目录。

示例：

```json
{
  "target": "/path/to/project",
  "mode": "release-review",
  "keyword": "project-review",
  "input_type": "directory",
  "run_dir": "runs/project-review-20260430-091500"
}
```

规则：

- 运行时参数不要写回 `config/default.json`。
- 推断参数建议记录来源。
- 本次路径可能是用户私人路径，不应进入公开示例。

## 4. L2 默认配置

适合放入 `config/default.json`：

- 超时时间。
- 重试次数。
- 默认输出语言。
- 批处理大小。
- 是否 dry-run。
- 最大文件数量。
- 默认报告格式。

示例：

```json
{
  "runtime": {
    "timeout_seconds": 60,
    "retry": 2,
    "dry_run": true
  },
  "limits": {
    "max_files": 200,
    "max_file_size_kb": 512
  },
  "output": {
    "language": "zh-CN",
    "format": "markdown",
    "write_report": true
  }
}
```

规则：

- 默认值应能让 Skill 直接运行。
- 嵌套不超过两层。
- 不写真实密钥。
- 不写运行产物。
- 不写用户本次输入。

## 5. L3 预设数据

适合放入 `references/presets/`：

- 模式列表。
- 输出类型。
- 平台枚举。
- 报告等级。
- 风格选项。

示例：

```json
{
  "modes": [
    {
      "id": "check",
      "label": "只检查",
      "description": "只输出问题，不修改文件。"
    },
    {
      "id": "fix",
      "label": "检查并修复",
      "description": "在用户明确授权后修改范围内文件。"
    }
  ]
}
```

## 6. 参数分类

```text
必须
  缺失后无法可靠执行。
  例：target 路径。

可推断
  可从输入、路径、文件扩展名推断。
  例：input_type。

可默认
  可从 config/default.json 获取。
  例：timeout_seconds。

可选
  不提供也不影响核心流程。
  例：report_title。
```

Agent 应先推断，再询问。

## 7. 参数询问

只询问缺失的必须参数。问题要说明用途。

推荐：

```text
我需要目标目录路径，用来扫描公开发布风险。
```

不推荐：

```text
给我参数。
```

如果需要多个参数，一次性问完。

## 8. Runtime Contract

当 Skill 需要特定运行时、系统二进制、本地模型、provider cache 或网络能力时，应使用 `config/runtime.json` 声明 Runtime Contract。

Runtime Contract 只保存“需求声明”，不保存实体环境。公开 Skill 不应把 `.venv`、`node_modules`、模型权重、大型缓存或作者本机路径放进仓库。

### 8.1 适用场景

需要 `config/runtime.json` 的情况：

- 有 Python、Node.js、Deno、Bun、Bash、Rust、Go 等脚本运行时要求。
- 需要 `ffmpeg`、`tesseract`、`poppler`、`imagemagick`、`gitleaks` 等系统二进制。
- 需要 OCR、ASR、VAD、embedding、rerank、vision 等本地模型资产。
- 需要 provider SDK 的大型 cache，并且 cache 位置会影响可复现性。
- 需要网络访问、固定 API host、代理或离线降级策略。

不需要 `config/runtime.json` 的情况：

- 只有 `SKILL.md`，不运行脚本。
- 不访问网络。
- 不需要本地模型或系统二进制。
- 所有能力都由 Agent 客户端内置工具提供，且没有额外环境要求。

### 8.2 标准结构

示例：

```json
{
  "schema_version": "1.0",
  "skill": "public-release-reviewing",
  "profiles": ["minimal", "standard", "full"],
  "envs": [
    {
      "id": "python-main",
      "kind": "python",
      "required": true,
      "version": ">=3.11",
      "manager": "uv",
      "lockfile": "scripts/python/uv.lock"
    }
  ],
  "binaries": [
    {
      "name": "gitleaks",
      "required": false,
      "purpose": "密钥扫描",
      "install_hint": "参考 gitleaks 官方安装文档。"
    }
  ],
  "models": [
    {
      "id": "example/asr-small",
      "role": "asr-default",
      "kind": "asr",
      "required": false,
      "size_mb": 142,
      "sha256": "填写公开可验证的 sha256",
      "license": "填写模型许可证",
      "source": {
        "type": "url",
        "url": "https://example.com/model.bin"
      }
    }
  ],
  "cache_policy": {
    "root": "runtime",
    "sync": false,
    "allow_provider_cache": true
  },
  "network": {
    "required": false,
    "hosts": [],
    "offline_behavior": "stop-or-degrade-with-record"
  }
}
```

### 8.3 字段说明

```text
schema_version
  Runtime Contract 版本。建议从 "1.0" 开始。

skill
  Skill 名称，应与目录名和 frontmatter name 一致。

profiles
  可选运行画像，例如 minimal、standard、full、gpu、offline。

envs
  脚本运行时声明。只声明语言、版本、包管理器和 lockfile，不存环境实体。

binaries
  系统二进制声明。写清 required、purpose、install_hint。

models
  本地模型资产声明。写清 role、kind、required、size、checksum、license、source。

cache_policy
  cache 是否允许、是否同步、由谁管理。公开仓默认 sync=false。

network
  网络需求、host 白名单、离线行为和降级策略。
```

`models[].kind` 建议使用：

```text
ocr
asr
vad
diarization
vision
segmentation
embedding
rerank
other
```

### 8.4 Runtime 实体边界

```text
可以进仓库
  config/runtime.json
  lockfile
  小型示例配置
  setup.md 中的准备说明

不进仓库
  .venv/
  node_modules/
  大型模型权重
  provider cache
  作者本机绝对路径
  真实凭据
```

运行环境、模型和 cache 应由目标客户端、runtime manager 或用户本机工具准备。公开规范只要求 Skill 说明需求和验证方式，不要求使用某个私有 Runtime 工具。

### 8.5 doctor / prepare / repair / resolve

如果 Skill 依赖 runtime manager，应把动作拆成四类，不把某个私有 CLI 写成通用要求：

```text
doctor
  只诊断，不创建环境，不下载模型，不修改系统。

prepare
  在用户明确执行后准备环境、依赖和模型资产。

repair
  修复损坏环境、checksum 不匹配或 cache 污染。

resolve
  返回 env、binary、model、cache 的实际路径，脚本不硬编码路径。
```

公开文档可以写占位命令：

```bash
<runtime-manager> skill doctor .
<runtime-manager> skill prepare . --profile standard
<runtime-manager> skill repair . --profile standard
<runtime-manager> resolve model --skill public-release-reviewing --role asr-default
```

如果没有 runtime manager，setup 文档必须给出等价的手动检查步骤。

## 9. 配置读取

脚本读取顺序：

```text
1. 读取 state/config.json。
2. 读取 config/default.json。
3. 合并参数。
4. 命令行参数覆盖配置。
5. 缺少必填参数则失败。
```

## 10. 禁止事项

- 把真实密钥写入配置。
- 把运行产物写入默认配置。
- 把用户本次输入写回仓库默认配置。
- 深层嵌套导致脚本难读。
- 用配置隐藏不可公开依赖。
- 配置默认执行破坏性动作。
- 把 Runtime 实体目录写入配置。
- 缺模型或环境时静默下载。
- 脚本绕过 Runtime Contract 直接硬编码模型/cache 路径。

## 11. 检查清单

```text
分层
  [ ] L1 写入 state/config.json。
  [ ] L2 写入 config/default.json。
  [ ] L3 写入 references/presets/ 或 definitions/。

安全
  [ ] 不含真实密钥。
  [ ] 不含私人路径。
  [ ] 不含客户数据。

可用
  [ ] 默认值可运行。
  [ ] 必填参数缺失时有明确停止条件。
  [ ] 推断参数记录来源。

Runtime
  [ ] 需要环境、二进制、模型或 cache 时存在 config/runtime.json。
  [ ] runtime.json 只保存声明，不保存实体资产。
  [ ] 模型声明包含 role、kind、required、checksum、license、source。
  [ ] cache_policy.sync 默认为 false。
  [ ] setup.md 说明 doctor、prepare、repair 或等价手动步骤。
```
