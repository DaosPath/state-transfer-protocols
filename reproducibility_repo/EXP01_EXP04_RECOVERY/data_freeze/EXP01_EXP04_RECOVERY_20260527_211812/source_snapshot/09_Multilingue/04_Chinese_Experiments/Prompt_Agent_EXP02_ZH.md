# Prompt Agent EXP02 ZH

## 目的

为未来执行 EXP02_ZH 的智能体提供提示词。

## Prompt

```txt
你正在执行 EXP02_ZH，中文 Proto v2 复现实验。

不要生成虚假结果。
不要修改西班牙语结果。
不要覆盖已有文件。

模式：
1. natural_zh
2. compressed_zh
3. proto_v2_core_zh
4. proto_v2_translated_zh，如适用

目标：
- 比较 Proto v2 是否减少结构开销。
- 评估 compressed_zh 是否仍是强基线。
- 观察通用 proto 在中文 tokenization 下的表现。

只在真实执行时写 JSONL。
未执行结果保持 PENDING / 待执行。
```

## 状态

`待执行`.
