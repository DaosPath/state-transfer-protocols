# EXP02 ZH Reproduction

## 目的

复现 EXP02 的中文版本。

## 目标

测试 Proto v2 在中文中是否减少结构开销，并比较 `compressed_zh`、`natural_zh` 与通用 proto。

## 模式

- `natural_zh`
- `compressed_zh`
- `proto_v2_core_zh`
- `proto_v2_translated_zh`，如适用

## 要观察的问题

- Proto v2 是否在中文中减少 overhead？
- `compressed_zh` 是否比 `natural_zh` 更高效？
- 通用 proto 和中文压缩谁更强？

## 状态

`PENDIENTE_DE_EJECUCION / 待执行 / PENDING`.

## 下一步

在 EXP01_ZH 之后执行。
