# Prompt Agent EXP03 ZH

## 目的

为未来执行 EXP03_ZH Fusion 的智能体提供提示词。

## Prompt

```txt
你正在执行 EXP03 Fusion 的中文复现实验文档准备。

当前任务：
只创建实验文档、协议说明、模板和提示词。
不要执行实验。
不要生成虚假结果。
不要覆盖西班牙语实验结果。
所有未执行结果必须标记为 PENDING / 待执行。

实验模式：

1. natural_zh
使用清晰完整的中文自然语言。

2. compressed_zh
使用压缩中文。
规则：
- 使用简体中文。
- 尽量减少 token。
- 不要寒暄。
- 不要礼貌语。
- 不要修辞。
- 不要长解释。
- 保留目标、关键事实、数字、风险、决定、下一步。
- 可以省略主语。
- 可以使用短句。
- 不要使用完整 proto key=value 格式，除非任务需要。
- 输出必须让另一个智能体能够继续任务。

3. proto_v3_min_core_zh
使用通用 proto 核心格式。
尽量使用 key=value、短符号、操作符。
不要写完整中文解释。
只保留必要任务信息。

4. proto_v3_state_core_zh
使用通用 proto 核心格式，但重点保存状态。
需要保留：
state/current status
decision
risk
missing information
next step

5. proto_v3_hybrid_zh
使用压缩中文 + 最小状态标记。
格式可以类似：
"结：... 风：... 缺：... 下：..."

6. proto_v3_zh_native
使用中文本地化符号协议。
建议字典：
任=任务
目=目标
态=状态
结=结果
风=风险
缺=缺失
决=决定
数=指标
下=下一步
证=证据
错=错误
译=翻译
质=质量
损=损失
歧=歧义

示例：
"任=exp2复查; 结=v2较v1省token但输caveman; 质↓=清晰+实用; 风=信息损失; 下=测轻量v3"

评估指标：
tokens
semantic fidelity / 语义保真
clarity / 清晰度
completeness / 完整性
utility / 实用性
ambiguity / 歧义
information loss / 信息损失
translation ease / 翻译容易度
state preservation / 状态保存
compactness / 紧凑性

输出：
只创建文档和模板。
不执行实验。
不生成结果。
```

## 状态

`待执行`.
