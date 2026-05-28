# Symbolic State-Transfer Protocols for AI Agent Handoff

This repository/package contains the public research artifacts for a sequence of experiments on compact symbolic protocols for multi-agent handoff.

## What This Studies

Large language model agents often need to continue work after context loss, provider changes, quota failures, or handoff to another agent. Instead of preserving full conversation history, this project studies compact communication formats as **state-transfer protocols**.

The main protocols are:

- `natural`: ordinary prose handoff.
- `compressed`: dense compact operational notes.
- `hybrid_min`: extremely compact hybrid symbolic form.
- `hybrid_state`: explicit state-transfer form with fields for goal, variables, constraints, completed work, pending work, plan, risks, checks, and next action.

## Experiments

### EXP05: Broad Discovery

`EXP05_PREMIUM_MULTIMODEL_TRILINGUAL`

Broad multilingual and multi-model experiment across Spanish, English, and Chinese. It compares `natural`, `compressed`, `hybrid_min`, and `hybrid_state` across multiple generator families and judge setups.

Main role:

- discover broad protocol behavior
- test multilingual transfer
- test judge drift
- test token-budget stress
- compare Chinese compactness behavior

### EXP06: Controlled Follow-Up

`EXP06_CAUSAL_PROTOCOL_TRANSFER`

Controlled experiment focusing on the strongest EXP05 claim: whether `hybrid_state` improves state preservation compared with `compressed`.

Main role:

- paired `compressed` vs `hybrid_state`
- Chinese tokenizer/variant ablation
- three-judge calibration
- policy-failure accounting

### EXP07: Real-Agent Handoff Objective Metrics

`EXP07_REAL_AGENT_HANDOFF_OBJECTIVE_METRICS`

Small/medium real-agent validation using LangGraph and OpenFang. Unlike EXP05/EXP06, this experiment uses objective schema metrics rather than only LLM judges.

Main role:

- test real-agent handoff feasibility
- measure variable recovery, constraints, subtasks, plan continuity, state errors
- check whether judge-based conclusions survive in real agent surfaces

### EXP08: Real-Agent Scale-Up

`EXP08_REAL_AGENT_SCALEUP`

Larger real-agent scale-up. It expands EXP07 from 270 executions to 900 operational executions.

Main role:

- confirm or revise EXP07 with larger sample
- focus only on `compressed` vs `hybrid_state`
- compare LangGraph/OpenFang and model-route effects
- report two views: 900/900 operational-complete cells and 824/900 strict JSON-valid cells
- preserve 76 Azure GPT 5.4 High blank-output cells as a model/serving failure mode

## Current Claims

Strong claims:

- `compressed` is the strongest general-purpose baseline in this experimental family.
- `hybrid_state` improves judge-scored state preservation in EXP05/EXP06 paired designs.
- Real-agent handoff can be measured with objective schema metrics.
- Language/script representation matters, especially in ZH vs romanized variants, but the mechanism is not fully isolated.

Careful claims:

- `hybrid_state` is a specialized state-oriented protocol, not a universal winner.
- EXP07/EXP08 do not show global `hybrid_state` dominance in real-agent objective metrics.
- Framework and provider surfaces affect outcomes.

Claims not made:

- This is not a general intelligence ranking of models.
- This does not prove tokenization alone causes the ZH result.
- This does not prove one agent framework is universally better than another.

## Reproducing Analysis

Each experiment directory contains:

- raw JSONL runs
- cleaned/deduplicated outputs
- cost ledgers or estimates
- prompt/mode definitions
- task banks
- analysis scripts
- summary tables

Run analysis scripts from the relevant experiment directory, for example:

```powershell
uv run python .\analyze_exp08.py
```

For the integrated paper package, see:

- `paper/main.tex`
- `paper/PAPER_PRINCIPAL_EXP05_EXP06_EXP07_EXP08.pdf`
- `appendix/TECHNICAL_APPENDIX_EXP05_EXP06.md`
- `appendix/Informe_EXP07_Real_Agent_Handoff_ObjectiveMetrics.md`
- `appendix/Informe_EXP08_Real_Agent_Scaleup.md`
- `README_REPRODUCIBILITY.md`

## Public Release Policy

Recommended public release:

- paper source and PDF
- appendix
- clean/deduplicated datasets
- task banks
- prompt definitions
- analysis scripts
- checksum manifests

Do not release:

- API keys
- credential files
- local virtual environments
- provider cache folders
- local database WAL/SHM files
- logs containing private local paths unless sanitized

## License Recommendation

- Paper text: CC BY 4.0
- Code/scripts: MIT
- Clean data: CC BY 4.0 or CC BY-NC 4.0, depending on desired reuse policy

## Author

Jordy Hernandez Cruzado  
Hijos Del Sol Research / Independent Researcher
