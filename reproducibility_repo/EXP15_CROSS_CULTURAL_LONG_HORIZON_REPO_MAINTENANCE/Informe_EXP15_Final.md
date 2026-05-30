# EXP15 Final Freeze and Report

Generated: 2026-05-30T01:20:11.369819

## Scope

This report freezes the final observed experiment state, keeps repaired and failed
events auditable, and separates the latest-cell dataset from historical operational
noise. Raw artifacts remain internal until a separate public-release sanitizer runs.

## Final Status

- Raw rows: 900
- Latest cells: 900
- Latest successful cells: 818
- Latest failed cells: 82
- Latest success rate: 90.9%
- Historical non-success events retained: 82
- Complete chains: 141 / 180

## By Model

| model_route | Total | Success | Rate | OK | Repaired | Error | Validator failed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| azure_gpt_5_4_high | 200 | 187 | 93.5% | 158 | 29 | 13 | 0 |
| dry_local_scaffold | 100 | 100 | 100.0% | 84 | 16 | 0 | 0 |
| gemini_3_5_flash | 200 | 191 | 95.5% | 166 | 25 | 9 | 0 |
| glm_5 | 200 | 195 | 97.5% | 176 | 19 | 1 | 4 |
| qwen3_next_80b_instruct | 200 | 145 | 72.5% | 118 | 27 | 55 | 0 |

## By Mode

| mode | Total | Success | Rate | OK | Repaired | Error | Validator failed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| compressed | 450 | 408 | 90.7% | 353 | 55 | 38 | 4 |
| hybrid_state | 450 | 410 | 91.1% | 349 | 61 | 40 | 0 |

## Cost Ledger

- Ledger rows: 822
- Input tokens recorded: 6259658
- Output tokens recorded: 1979450
- Reasoning tokens recorded: 0
- Estimated total tokens recorded: 8239108
- Estimated USD fields recorded: 0.000000

## Visual Proxy

The visual comparison script was rerun before freezing. The current visual proxy is
useful as an integrity threshold, but it saturated in prior runs. It must not be used
as a discriminative page-quality ranking without stronger screenshot-based evaluation.


## Safe Claims

- The freeze preserves latest-cell outcomes and historical repair evidence separately.
- Success rates can compare operational compatibility under this controlled contract.
- Repaired errors remain visible and are not silently deleted.

## Limitations

- This is a controlled repo-maintenance benchmark, not a general software-agent leaderboard.
- A successful validator pass does not imply superior visual design quality.
- Provider routing, quotas, and model availability are time-sensitive.
- Internal raw data still requires sanitization before public release.

## Reproducibility Artifacts

See `analysis/final/` for deduplicated datasets, failures, tables, workspace hashes,
security sweep counts, and the summary JSON. See `data_freeze/` for the immutable
snapshot and SHA-256 manifest.
