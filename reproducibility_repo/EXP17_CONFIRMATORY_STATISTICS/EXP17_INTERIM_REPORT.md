# EXP17 Interim Report: Confirmatory Statistics and Reproducibility Audit

EXP17 uses already frozen EXP05--EXP16 data only. No model/API calls are required.

## Artifacts generated

- `data_inventory_exp17.csv`
- `DATA_INVENTORY_EXP17.md`
- `reproducibility_matrix_exp01_exp16.csv`
- `REPRODUCIBILITY_MATRIX_EXP01_EXP16.md`
- `exp17_bootstrap_candidate_results.csv`
- `EXP17_BOOTSTRAP_STATUS.md`

## Reproducibility status

- Complete by automatic artifact detection: `10/16` experiments.
- Needs manual review: `6/16` experiments.
- Manual review targets: EXP02, EXP03, EXP04, EXP07, EXP11, EXP12.

## Bootstrap coverage

- Unique clean datasets scanned: `32`.
- Bootstrap result rows: `147`.
- Current bootstrap computes `hybrid_state - compressed` with deterministic resampling.
- Pairing uses available identifiers among task, language, model/generator, judge, framework, repetition and round.

| Experiment | Bootstrap rows |
|---|---:|
| EXP05 | 44 |
| EXP06 | 44 |
| EXP07 | 14 |
| EXP08 | 7 |
| EXP10 | 3 |
| EXP14 | 9 |
| EXP15 | 26 |

## Early signal check

The following are machine-generated candidate intervals. They are useful for triage, not yet the final paper table.

| EXP | Metric | Pairs | Mean delta | 95% CI | Direction |
|---|---|---:|---:|---|---|
| EXP05 | `metric_state_preservation` | 83 | 0.289 | [0.084, 0.518] | hybrid_state higher |
| EXP05 | `metric_operational_continuity` | 83 | 0.253 | [0.060, 0.446] | hybrid_state higher |
| EXP05 | `metric_information_loss` | 83 | -0.265 | [-0.494, -0.048] | compressed higher / lower negative metric |
| EXP05 | `state_preservation` | 83 | 0.289 | [0.084, 0.518] | hybrid_state higher |
| EXP05 | `operational_continuity` | 83 | 0.253 | [0.072, 0.446] | hybrid_state higher |
| EXP05 | `information_loss` | 83 | -0.265 | [-0.506, -0.036] | compressed higher / lower negative metric |
| EXP05 | `metric_state_preservation` | 28 | 1.179 | [0.714, 1.679] | hybrid_state higher |
| EXP05 | `metric_operational_continuity` | 28 | 1.071 | [0.571, 1.643] | hybrid_state higher |
| EXP05 | `metric_information_loss` | 28 | -0.964 | [-1.429, -0.500] | compressed higher / lower negative metric |
| EXP05 | `state_preservation` | 28 | 1.179 | [0.750, 1.679] | hybrid_state higher |
| EXP05 | `operational_continuity` | 28 | 1.071 | [0.571, 1.643] | hybrid_state higher |
| EXP05 | `information_loss` | 28 | -0.964 | [-1.464, -0.500] | compressed higher / lower negative metric |
| EXP06 | `state_preservation` | 228 | 0.140 | [-0.079, 0.351] | uncertain |
| EXP06 | `operational_continuity` | 228 | 0.009 | [-0.215, 0.228] | uncertain |
| EXP06 | `information_loss` | 228 | 0.070 | [-0.167, 0.303] | uncertain |
| EXP06 | `state_preservation` | 228 | 0.140 | [-0.075, 0.364] | uncertain |
| EXP06 | `operational_continuity` | 228 | 0.009 | [-0.224, 0.241] | uncertain |
| EXP06 | `information_loss` | 228 | 0.070 | [-0.162, 0.311] | uncertain |
| EXP06 | `state_preservation` | 228 | 0.140 | [-0.070, 0.368] | uncertain |
| EXP06 | `operational_continuity` | 228 | 0.009 | [-0.219, 0.232] | uncertain |
| EXP06 | `information_loss` | 228 | 0.070 | [-0.167, 0.303] | uncertain |
| EXP06 | `state_preservation` | 228 | 0.140 | [-0.079, 0.364] | uncertain |
| EXP06 | `operational_continuity` | 228 | 0.009 | [-0.202, 0.237] | uncertain |
| EXP06 | `information_loss` | 228 | 0.070 | [-0.158, 0.294] | uncertain |
| EXP07 | `variable_recovery_rate` | 90 | -0.106 | [-0.194, -0.029] | compressed higher / lower negative metric |
| EXP07 | `constraint_retention_rate` | 90 | 0.006 | [-0.094, 0.111] | uncertain |
| EXP07 | `json_valid` | 90 | 0.000 | [-0.067, 0.067] | uncertain |
| EXP07 | `variable_recovery_rate` | 90 | -0.106 | [-0.192, -0.026] | compressed higher / lower negative metric |
| EXP07 | `constraint_retention_rate` | 90 | 0.006 | [-0.106, 0.111] | uncertain |
| EXP07 | `json_valid` | 90 | 0.000 | [-0.067, 0.067] | uncertain |
| EXP08 | `variable_recovery_rate` | 450 | -0.139 | [-0.176, -0.101] | compressed higher / lower negative metric |
| EXP08 | `constraint_retention_rate` | 450 | -0.063 | [-0.110, -0.018] | compressed higher / lower negative metric |
| EXP08 | `json_valid` | 450 | -0.089 | [-0.124, -0.056] | compressed higher / lower negative metric |
| EXP14 | `constraint_preservation` | 10 | 0.000 | [0.000, 0.000] | uncertain |
| EXP14 | `dependency_preservation` | 10 | 0.000 | [0.000, 0.000] | uncertain |
| EXP15 | `constraint_preservation` | 10 | 0.000 | [0.000, 0.000] | uncertain |
| EXP15 | `dependency_preservation` | 10 | 0.000 | [0.000, 0.000] | uncertain |
| EXP15 | `visual_quality_proxy` | 10 | 0.000 | [0.000, 0.000] | uncertain |
| EXP15 | `constraint_preservation` | 10 | 0.000 | [0.000, 0.000] | uncertain |
| EXP15 | `dependency_preservation` | 10 | 0.000 | [0.000, 0.000] | uncertain |
| EXP15 | `visual_quality_proxy` | 10 | 0.000 | [0.000, 0.000] | uncertain |

## Claims update policy

- Strong claims require repeated support across at least two independent surfaces or one controlled surface plus objective validation.
- Exploratory claims remain exploratory when they depend on one model family, one judge, one language variant, or saturated success rates.
- EXP09--EXP16 should be framed as operational/interface validation, not universal model ranking.
- The next EXP17 pass should add clustered bootstrap by task/model/language/framework where the schema permits it.
