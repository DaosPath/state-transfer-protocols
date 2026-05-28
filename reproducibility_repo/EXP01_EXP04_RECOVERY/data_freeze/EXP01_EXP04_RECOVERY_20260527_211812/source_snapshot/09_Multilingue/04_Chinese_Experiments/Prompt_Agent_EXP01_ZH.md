# Prompt Agent EXP01 ZH

## 目的

为未来执行 EXP01_ZH 的智能体提供提示词。

## Prompt

```txt
你正在执行 EXP01_ZH 的中文复现实验。

不要生成虚假结果。
不要覆盖西班牙语结果。
不要保存 API key。

模式：
1. natural_zh
2. compressed_zh
3. proto_v1_core_zh
4. proto_v1_translated_zh，如适用

使用 EXP01_ES 的任务结构，翻译成中文时保留难度。
compressed_zh 不是“原始人说话”，而是中文操作性压缩。

只有真实执行实验时才写入 JSONL。
未执行时全部标记为 PENDING / 待执行。
```

## 状态

`待执行`.
