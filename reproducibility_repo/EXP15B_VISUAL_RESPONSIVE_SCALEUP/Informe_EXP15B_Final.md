# EXP15B Final Freeze and Report

Generated: 2026-05-30T01:20:15.394431

## Scope

This report freezes the final observed experiment state, keeps repaired and failed
events auditable, and separates the latest-cell dataset from historical operational
noise. Raw artifacts remain internal until a separate public-release sanitizer runs.

## Final Status

- Raw rows: 2000
- Latest cells: 2000
- Latest successful cells: 1204
- Latest failed cells: 796
- Latest success rate: 60.2%
- Historical non-success events retained: 796
- Complete chains: 71 / 200

## By Model

| model_route | Total | Success | Rate | OK | Repaired | Error | Validator failed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| gemini_3_5_flash | 400 | 382 | 95.5% | 328 | 54 | 16 | 2 |
| glm_5 | 400 | 363 | 90.8% | 316 | 47 | 10 | 27 |
| grok_4_20_non_reasoning | 400 | 43 | 10.8% | 25 | 18 | 357 | 0 |
| grok_4_20_reasoning | 400 | 98 | 24.5% | 46 | 52 | 302 | 0 |
| qwen3_next_80b_instruct | 400 | 318 | 79.5% | 240 | 78 | 82 | 0 |

## By Mode

| mode | Total | Success | Rate | OK | Repaired | Error | Validator failed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| compressed | 1000 | 599 | 59.9% | 472 | 127 | 381 | 20 |
| hybrid_state | 1000 | 605 | 60.5% | 483 | 122 | 386 | 9 |

## Cost Ledger

- Ledger rows: 1233
- Input tokens recorded: 12903001
- Output tokens recorded: 1473720
- Reasoning tokens recorded: 0
- Estimated total tokens recorded: 14376721
- Estimated USD fields recorded: 0.000000

## Visual Proxy

The visual comparison script was rerun before freezing. The current visual proxy is
useful as an integrity threshold, but it saturated in prior runs. It must not be used
as a discriminative page-quality ranking without stronger screenshot-based evaluation.


## Grok Reasoning vs Non-Reasoning

| Route | Success | Total | Rate |
| --- | ---: | ---: | ---: |
| Non-Reasoning | 43 | 400 | 10.8% |
| Reasoning | 98 | 400 | 24.5% |

Reasoning improved success by 13.8% absolute
(2.279x relative). This is evidence about protocol and
interface compatibility, not a general model-quality ranking.

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
