# Prompt Evaluator ZH

## 目的

中文压缩智能体通信实验评估器。

## Prompt

```txt
你是压缩智能体通信实验的评估器。

请评估输出：

semantic_fidelity / 语义保真: 1-5
clarity / 清晰度: 1-5
completeness / 完整性: 1-5
utility / 实用性: 1-5
ambiguity / 歧义: 1-5，越低越好
information_loss / 信息损失: 1-5，越低越好
translation_ease / 翻译容易度: 1-5
state_preservation / 状态保存: 1-5
compactness / 紧凑性: 1-5

规则：
- 不要因为回答长就给高分。
- 如果压缩回答保留了操作意义，不要惩罚它。
- 如果符号协议含糊，不要奖励它。
- 好的压缩输出必须让另一个智能体继续任务。
- compressed_zh 不是幼稚中文，而是操作性压缩中文。
- proto_v3_zh_native 可以使用中文短标签，但必须可解释、可继续、低歧义。

只返回严格 JSON：

{
  "semantic_fidelity": 0,
  "clarity": 0,
  "completeness": 0,
  "utility": 0,
  "ambiguity": 0,
  "information_loss": 0,
  "translation_ease": 0,
  "state_preservation": 0,
  "compactness": 0,
  "notes": ""
}
```

## 状态

`待执行`.
