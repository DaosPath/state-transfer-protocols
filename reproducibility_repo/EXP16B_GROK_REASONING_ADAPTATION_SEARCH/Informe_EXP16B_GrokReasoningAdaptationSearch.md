# EXP16B Freeze Report

Freeze timestamp: `20260530_225809`

## Scope

EXP16-B searches for a more stable Grok reasoning prompt contract after EXP16 showed poor operational success for the default Grok route.

Important caveat: most failures are platform/quota/auth failures, not JSON or semantic failures.

## Cell Counts

- Raw rows: `211`
- Latest cells: `160`
- Latest OK / OK repaired: `50`
- Latest failures: `110`
- Deprecated/misrouted latest cells: `0`

## Status By Model And Mode

| Model route | Mode | Status | Count |
|---|---|---:|---:|
| `grok_4_20_reasoning` | `grok_v1_final_json` | `error` | 28 |
| `grok_4_20_reasoning` | `grok_v1_final_json` | `ok` | 4 |
| `grok_4_20_reasoning` | `grok_v2_template_lock` | `error` | 27 |
| `grok_4_20_reasoning` | `grok_v2_template_lock` | `ok` | 5 |
| `grok_4_20_reasoning` | `grok_v3_patch_min` | `error` | 28 |
| `grok_4_20_reasoning` | `grok_v3_patch_min` | `ok` | 4 |
| `grok_4_20_reasoning` | `grok_v4_schema_echo` | `error` | 14 |
| `grok_4_20_reasoning` | `grok_v4_schema_echo` | `ok` | 18 |
| `grok_4_20_reasoning` | `grok_v5_two_phase_hidden` | `error` | 13 |
| `grok_4_20_reasoning` | `grok_v5_two_phase_hidden` | `ok` | 19 |

## Error Classes

| Error class | Count |
|---|---:|
| `401_auth` | 15 |
| `403_consumer_suspended` | 12 |
| `429_resource_exhausted` | 83 |

## Token Ledger

- Ledger calls: `50`
- Input tokens: `362074`
- Output tokens: `27626`
- Estimated total tokens: `389700`

| Model route | Calls | Input | Output | Estimated total |
|---|---:|---:|---:|---:|
| `grok_4_20_reasoning` | 50 | 362074 | 27626 | 389700 |

## Interpretation

- `grok_v5_two_phase_hidden` had the highest success count, followed closely by `grok_v4_schema_echo`.
- v1-v3 mostly failed through quota exhaustion and are not useful adaptations.
- Because most failures are 429/401/403 infrastructure failures, EXP16-B supports only a cautious operational claim: v4/v5 are better prompt contracts among successful attempts, while Grok via Vertex partner endpoint was unstable under this workload.

## Reproducibility Artifacts

- Freeze directory: `<LOCAL_RESEARCH_ROOT>/05_Experimentos/EXP16B_GROK_REASONING_ADAPTATION_SEARCH\data_freeze\freeze_20260530_225809`
- Clean latest OK: `exp16b_latest_cells_clean.jsonl`
- Latest failures: `exp16b_failures_latest.jsonl`
- Summary CSV: `exp16b_latest_cells_summary.csv`
- Checksums: `SHA256SUMS.txt` inside the freeze directory.

## Claim Strength

- Strong: platform failures must be separated from model/protocol failures.
- Strong: v4/v5 Grok prompt contracts outperformed v1-v3 in successful latest cells.
- Cautious: Grok adaptation conclusions are confounded by quota/auth/project suspension.
- Not claimed: complete Grok reasoning benchmark result. The experiment was interrupted by provider restriction.

