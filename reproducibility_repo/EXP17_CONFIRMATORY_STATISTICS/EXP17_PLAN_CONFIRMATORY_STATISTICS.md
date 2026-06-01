# EXP17 Confirmatory Statistics Plan

Status: planned / scaffolded

Date: 2026-05-31

## Purpose

EXP17 is the first follow-up after the EXP01-EXP16 technical report. It does not require new model calls. It reuses frozen data to test whether the main claims survive stronger statistical treatment.

## Main Question

Do the core claims survive dependence-aware statistics?

Core claims to test:

- `compressed` is the strongest general baseline.
- `hybrid_state` improves explicit state preservation in EXP05 and EXP06.
- real-agent and tool-agent results depend strongly on operational surface.

## Data Inputs

Primary inputs:

- EXP05 cleaned latest-cell evaluations.
- EXP06 cleaned valid generations and three-judge evaluations.
- EXP07 objective real-agent metrics.
- EXP08 operational-complete and strict-JSON-valid views.
- EXP09-EXP16 latest-cell clean datasets and failure datasets where applicable.

Public-release inputs:

- `13_Repo_Publico/GITHUB_RELEASE_state-transfer-protocols/reproducibility_repo/`
- `13_Repo_Publico/GITHUB_RELEASE_state-transfer-protocols/analysis/`

Internal full inputs, if needed:

- `05_Experimentos/EXP05_PREMIUM_MULTIMODEL_TRILINGUAL/`
- `05_Experimentos/EXP06_CAUSAL_PROTOCOL_TRANSFER/`
- `05_Experimentos/EXP07_REAL_AGENT_HANDOFF_OBJECTIVE_METRICS/`
- `05_Experimentos/EXP08_REAL_AGENT_SCALEUP/`
- later EXP folders.

## Planned Analyses

### 1. Clustered Bootstrap

Use clustered resampling rather than treating every row as independent.

Candidate cluster keys:

- task_id
- generator/model route
- language or variant
- judge route
- framework
- repetition

Primary bootstrap targets:

- EXP05 `hybrid_state - compressed` delta for state preservation.
- EXP05 `hybrid_state - compressed` delta for quality index.
- EXP06 `hybrid_state - compressed` delta for state preservation.
- EXP06 `hybrid_state - compressed` delta for quality index.
- EXP07/EXP08 objective deltas where paired cells exist.

### 2. Mixed-Effects Models

Fit models with random intercepts for repeated-measure structure.

Candidate fixed effects:

- protocol mode
- language / representation variant
- model route
- judge route
- framework
- interaction: mode x language
- interaction: mode x framework

Candidate random effects:

- task_id
- generator/model
- judge
- framework
- repetition

### 3. Robustness Tables

Create tables separating:

- core scientific results: EXP05-EXP08
- systems/interface results: EXP09-EXP16
- provider/platform failure classes
- saturated versus non-saturated experiments

## Expected Outputs

- `Informe_EXP17_ConfirmatoryStatistics.md`
- `exp17_bootstrap_results.csv`
- `exp17_mixed_effects_results.csv`
- `exp17_claim_strength_update.md`
- figures:
  - bootstrap intervals for state preservation
  - bootstrap intervals for quality index
  - variance component summary
  - protocol-by-surface interaction plot

## Success Criteria

EXP17 is successful if it can state, conservatively:

- which claims remain strong under clustered uncertainty;
- which claims become exploratory;
- which effects are dominated by task/model/judge/framework clustering;
- whether the current report's claim-strength table should be tightened.

## Non-Goals

EXP17 should not:

- run new model calls;
- change frozen data;
- repair old failures;
- make new model-intelligence rankings;
- treat provider failures as semantic failures.

## First Implementation Step

Build a data inventory script that lists available clean datasets, row counts, key columns, and candidate cluster identifiers across EXP05-EXP16.
