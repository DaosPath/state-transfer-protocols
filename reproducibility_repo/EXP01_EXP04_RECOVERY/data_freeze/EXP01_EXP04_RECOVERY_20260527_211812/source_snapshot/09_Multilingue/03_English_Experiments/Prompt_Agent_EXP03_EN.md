# Prompt Agent EXP03 EN

## Purpose

Prompt for a future agent running the English reproduction of EXP03 Fusion.

## Prompt

```txt
You are running an English reproduction of EXP03 Fusion.

Do not invent results.
Do not modify Spanish results.
Do not overwrite existing files.
Use the same task structure as EXP03_ES, translated into English while preserving difficulty.

Modes:
1. natural_en
2. compressed_en
3. proto_v3_min_core_en
4. proto_v3_state_core_en
5. proto_v3_hybrid_en
6. translated variants if required

Mode definitions:

natural_en:
Answer in clear, complete English.

compressed_en:
Answer in compressed operational English.
Minimize tokens.
No politeness.
No filler.
No decorative language.
Preserve goal, facts, numbers, decisions, risks, and next step.
Output must allow another agent to continue the task.

proto_v3_min_core_en:
Use minimal symbolic protocol.
Prefer key=value, short operators, no long sentences.
Preserve only essential task information.

proto_v3_state_core_en:
Use symbolic protocol focused on state preservation.
Must include current state, decision, risk, missing info, next step when relevant.

proto_v3_hybrid_en:
Use compressed English plus minimal symbolic markers.
Balance readability and token efficiency.

Evaluation:
Use same metrics as EXP03_ES:
tokens, fidelity, clarity, completeness, utility, ambiguity, information loss, translation ease, state preservation, compactness.

Output:
Create JSONL rows only when experiment is actually executed.
Until execution, keep templates as PENDING.
```

## Status

`PENDING`.
