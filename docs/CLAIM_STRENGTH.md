# Claim Strength Map

This document separates strong claims from exploratory claims so that reviewers can audit the project without over-reading the results.

## Stronger Claims

| Claim | Main Evidence | Boundary |
|---|---|---|
| `compressed` is a strong general baseline. | EXP05--EXP08 and repeated operational surfaces. | Baseline strength does not imply universal dominance in every metric. |
| `hybrid_state` improves state-oriented behavior in selected handoff settings. | EXP05 state-preservation gains and EXP06 controlled transfer analysis. | It does not consistently win global quality. |
| Real-agent and tool-use surfaces expose failures hidden by text-only evaluation. | EXP07--EXP16 parser, schema, blank-output, repair and scope-drift observations. | These are interface lessons, not universal rankings of models. |
| Reproducibility requires prompts, validators, schemas, cleaned cells and failure logs. | EXP17 inventory and reproducibility matrix. | Early experiments still need manual artifact review. |

## Exploratory Claims

| Claim | Why Exploratory |
|---|---|
| Chinese-language behavior may reflect tokenization or structural effects. | Promising but needs token-level causal controls. |
| Model-specific protocol adaptation can improve long-horizon behavior. | EXP16 is useful but not yet confirmatory across enough routes. |
| Later visual/repo-maintenance experiments show robust general software-agent performance. | EXP09--EXP16 are controlled interface validations, not full software-engineering benchmarks. |

## Recommended Framing

The safest central claim is:

> Protolanguages should be evaluated not only by compression or answer quality, but by their ability to preserve operational state across increasingly realistic agent surfaces.

The project should not claim that `hybrid_state` is a universal winner. The better claim is that different protolanguages occupy different operational roles: `compressed` as a robust baseline and `hybrid_state` as a state-transfer-oriented format with tradeoffs.
