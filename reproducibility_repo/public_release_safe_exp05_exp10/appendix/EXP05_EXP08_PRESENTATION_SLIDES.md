# Symbolic Compression Protocols for Multi-Agent Handoff

12-slide presentation draft for EXP05-EXP08.

---

## 1. Core Claim

Symbolic compression is not only prompt shortening.

It can be evaluated as an operational protocol for preserving state across agents, languages, models, and execution frameworks.

---

## 2. Problem

Agents fail at handoff when context is long, compressed, multilingual, or transferred across model families.

The practical question:

Can compact protocols preserve enough operational state for another agent to continue work?

---

## 3. Protocols

Four modes tested:

- natural: normal prose
- compressed: compact operational notes
- hybrid_min: extreme symbolic compression
- hybrid_state: compact structured state handoff

Key distinction: hybrid_state optimizes continuity, not only token reduction.

---

## 4. EXP05: Broad Discovery

Design:

- ES / EN / ZH
- multiple frontier and partner models
- natural, compressed, hybrid_min, hybrid_state
- LLM-judge metrics

Finding:

compressed was the strongest universal baseline; hybrid_state showed early continuity signal.

---

## 5. EXP05: Multilingual Signal

ZH did not collapse under compression and sometimes scored better.

Interpretation:

Promising evidence for language/tokenization effects, but exploratory because EXP05 was broad and partially stratified.

Claim discipline:

ZH result is signal, not proof.

---

## 6. EXP06: Controlled Test

EXP06 narrowed the question:

compressed vs hybrid_state under controlled causal transfer.

Variants:

- ES
- EN
- ZH
- ZH_PINYIN
- EN_LITERAL
- ES_LITERAL

Purpose: test whether hybrid_state itself improves continuity under stricter controls.

---

## 7. EXP06: Tradeoff

Result:

hybrid_state improved state-oriented transfer in selected conditions, but did not dominate global quality.

Interpretation:

compressed remains baseline; hybrid_state is specialized for operational state preservation.

---

## 8. EXP07: Real-Agent Handoff

EXP07 moved beyond LLM-as-judge:

- LangGraph-style execution
- OpenFang-style execution
- objective validators
- variable recovery
- subtask completion
- plan continuity
- constraint retention

This tests whether protocols survive actual agent workflows.

---

## 9. EXP07: Objective Metrics

Key result:

compressed remained operationally robust.

hybrid_state showed narrower advantages, especially around explicit constraint/state retention.

This prevents overclaiming and strengthens paper credibility.

---

## 10. EXP08: Scale-Up

EXP08 scales the real-agent setup:

- 30 tasks
- 5 repetitions
- 2 frameworks
- 2 Azure model routes for LangGraph
- 900 expected executions

Goal: determine whether EXP07 patterns survive larger real-agent sampling.

---

## 11. Reproducibility and Safety

Release package includes:

- paper source
- figures
- appendix
- task banks
- aggregate CSVs
- redacted public dataset
- manifests and checksums
- security sweep

Raw logs remain internal unless manually reviewed.

---

## 12. Final Takeaway

Strong claim:

compressed is a universal operational compression baseline.

Careful claim:

hybrid_state is a specialized protocol for preserving state and continuity, not a universal quality winner.

Research direction:

protocol design for interoperable multi-agent systems.
