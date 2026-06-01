# EXP17 Bootstrap Status

This is the first confirmatory-pass bootstrap over already frozen clean datasets.

- Raw candidate clean datasets: `157`
- Unique candidate clean datasets scanned: `32`
- Bootstrap result rows: `147`
- Output CSV: `exp17_bootstrap_candidate_results.csv`

## Current Policy

- Delta is `hybrid_state - compressed`.
- Pairing uses available identifiers among task, language, generator/model, judge, framework, repetition and round.
- Bootstrap uses deterministic seeded resampling per dataset/metric.
- This script is intentionally conservative and skips files without clear paired cells.
