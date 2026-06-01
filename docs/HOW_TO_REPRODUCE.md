# How to Reproduce the Analysis

This repository is organized as a public reproducibility package for the state-transfer protolanguage experiments.

## Core Artifacts

- `paper_short/`: compact paper version for external review.
- `technical_report/`: long technical report covering EXP01--EXP16.
- `reproducibility_repo/`: prompts, task banks, validators, cleaned data, reports and experiment-specific artifacts.
- `reproducibility_repo/EXP17_CONFIRMATORY_STATISTICS/`: no-model statistical audit over frozen data.

## Recommended Reproduction Path

1. Read `README.md` for the project-level claim boundaries.
2. Inspect `technical_report/` for the complete experimental ladder.
3. Inspect each experiment folder under `reproducibility_repo/`.
4. Run the EXP17 inventory and audit scripts:

```powershell
cd reproducibility_repo\EXP17_CONFIRMATORY_STATISTICS
python .\inventory_exp17_sources.py
python .\audit_reproducibility_exp01_exp16.py
python .\exp17_confirmatory_bootstrap.py
```

## What EXP17 Does

EXP17 does not call models. It reuses frozen data and generates:

- `data_inventory_exp17.csv`
- `REPRODUCIBILITY_MATRIX_EXP01_EXP16.md`
- `exp17_bootstrap_candidate_results.csv`
- `EXP17_INTERIM_REPORT.md`

The bootstrap pass estimates `hybrid_state - compressed` deltas where paired cells are available.

## Current Limitations

- Older experiments may store reproducibility evidence inside reports rather than as separate frozen files.
- Some later experiments are saturated interface validations, not broad model-comparison benchmarks.
- Confirmatory mixed-effects modeling remains future work.
