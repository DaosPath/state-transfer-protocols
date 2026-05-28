# EXP03 ZH Fusion

## 目的

复现 EXP03 Fusion，并加入中文本地化变体。

## 目标

比较中文自然语言、压缩中文、通用 proto、中文本地 proto 和 hybrid_zh。

## 推荐模式

- `natural_zh`
- `compressed_zh`
- `proto_v3_min_core_zh`
- `proto_v3_state_core_zh`
- `proto_v3_hybrid_zh`
- `proto_v3_zh_native`
- `proto_v3_zh_native_translated`，可选

## 方法说明

- `proto_v3_core` 用于 ES/EN/ZH 公平比较。
- `proto_v3_zh_native` 测试中文本地化是否提高效率。
- `compressed_zh` 测试中文操作性压缩是否优于完整中文。
- `hybrid_zh` 测试压缩中文与状态符号之间的平衡。

## 状态

`PENDIENTE_DE_EJECUCION / 待执行 / PENDING`.

## 下一步

在 EXP01_ZH 和 EXP02_ZH 完成后执行。
