# 排错与恢复规范

> 本文规范 Skill 的错误分类、诊断顺序、重试策略和中断恢复流程。

## 1. 职责

排错规范解决：

- 错误属于哪一层。
- 是否可恢复。
- 是否应该重试。
- 如何记录错误。
- 如何继续执行。

不要用宽泛提示词掩盖结构问题。

## 2. 八层错误分类

```text
L0 Runtime 资产层
  Runtime env、本地模型、provider cache、系统二进制缺失或损坏。

L1 入口层
  Skill 未触发、误触发、description 不清。

L2 参数层
  必填输入缺失、路径不合法、模式无法判断。

L3 依赖层
  命令不存在、包缺失、运行时版本不对。

L4 凭据层
  环境变量缺失、权限不足、凭据失效。

L5 网络层
  超时、限流、服务错误、离线。

L6 文件层
  文件不存在、权限不足、输出不可写。

L7 进度层
  progress.json 损坏、状态不一致、产物缺失。
```

## 3. 诊断顺序

```text
1. 如果存在 config/runtime.json，先检查 Runtime Contract。
2. Runtime env、binary、model、cache 是否准备好。
3. 是否触发了正确 Skill。
4. 必填输入是否完整。
5. 目标路径是否存在。
6. 依赖命令是否可用。
7. 凭据是否需要且已配置。
8. 网络是否可用。
9. progress.json 是否可解析。
10. 上一步产物是否存在。
```

按顺序查，不要直接重跑全部。

## 3.1 Runtime 资产层

Runtime 资产层错误应先于脚本依赖错误排查。典型错误：

```text
runtime_missing
  config/runtime.json 声明的 env、binary、model 或 cache 未准备。

runtime_corrupt
  模型 checksum 不匹配、环境损坏、cache 污染。

binary_missing
  系统二进制缺失，例如 ffmpeg、tesseract、gitleaks。

model_license_required
  模型许可证要求用户手动下载或确认。

cache_not_writable
  provider cache 不可写或落到了错误目录。
```

结构化错误示例：

```json
{
  "type": "runtime_missing",
  "message": "required model asr-default is not prepared",
  "recoverable": true,
  "suggested_fix": "按 docs/setup.md 的 Runtime prepare 步骤准备模型资产。"
}
```

禁止用这些方式处理 Runtime 错误：

- 脚本内静默下载大型模型。
- 临时切换系统 Python 继续跑生产流程。
- 写死作者本机 runtime/cache 路径。
- 把 provider cache 复制进 Skill 仓库。
- 不校验 checksum 就使用本地模型。

## 4. 错误记录

写入 `state/progress.json`：

```json
{
  "status": "failed",
  "current_step": "step02-execute",
  "failed_steps": ["step02-execute"],
  "errors": [
    {
      "type": "runtime_missing",
      "message": "gitleaks not found",
      "recoverable": true,
      "suggested_fix": "安装 gitleaks 或继续使用文本搜索。"
    }
  ],
  "resume_hint": "安装 gitleaks 后从 step02-execute 继续；也可跳过专用密钥扫描。"
}
```

## 5. 重试策略

可重试：

- 网络超时。
- 5xx 服务错误。
- 临时限流。
- 可恢复文件锁。

不应盲目重试：

- 4xx 权限错误。
- 目标路径不存在。
- JSON 格式错误。
- 凭据缺失。
- 输出目录不可写。
- Runtime checksum 不匹配。
- 模型许可证需要用户确认。

## 6. 降级策略

允许降级，但必须记录。

示例：

```text
gitleaks 不可用
  降级为 rg 文本搜索。
  在 skipped_checks 中记录未运行专用扫描器。
```

不要静默降级。

Runtime 降级也必须记录：

```text
asr-default 模型缺失
  如果该模型是 required=true，停止。
  如果 required=false，跳过 ASR 分析，并在 skipped_checks 中记录。
```

## 7. 中断恢复

恢复步骤：

1. 读取 `state/progress.json`。
2. 检查 `completed_steps`。
3. 验证已完成步骤产物存在。
4. 从 `current_step` 继续。
5. 不重复已完成步骤。
6. 写入新的 `updated_at` 和恢复记录。

## 8. progress.json 损坏

处理：

1. 检查运行目录结构。
2. 根据已有步骤产物重建状态。
3. 如果无法判断，停止并要求用户确认从哪一步继续。
4. 不猜测执行破坏性动作。

## 9. 失败报告

失败时最终回复应包含：

- 失败步骤。
- 错误类型。
- 可恢复性。
- 已保留产物。
- 建议下一步。
- 是否需要用户输入。

## 10. 禁止事项

- 报错后直接跳过测试。
- 用 try/except 把所有错误变成“失败”。
- 不更新 `progress.json`。
- 重跑全部导致覆盖产物。
- 网络失败后伪造结果。
- 凭据缺失后继续执行真实请求。

## 11. 检查清单

```text
分类
  [ ] 错误有层级。
  [ ] 错误有类型。
  [ ] 可恢复性明确。

Runtime
  [ ] 存在 config/runtime.json 时先做 Runtime 检查。
  [ ] runtime_missing、runtime_corrupt、binary_missing 有明确修复路径。
  [ ] 缺必需模型或 env 时停止，不静默回退。
  [ ] cache、模型和环境路径不硬编码。

记录
  [ ] progress.json 已更新。
  [ ] resume_hint 可执行。
  [ ] 不打印敏感值。

恢复
  [ ] 已完成步骤不重复。
  [ ] 缺失产物会停止。
  [ ] 降级会记录原因。
```
