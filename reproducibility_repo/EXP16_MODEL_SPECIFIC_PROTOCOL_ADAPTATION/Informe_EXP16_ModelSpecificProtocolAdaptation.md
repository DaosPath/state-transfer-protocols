# EXP16 Freeze Report

Freeze timestamp: `20260530_225809`

## Scope

EXP16 tests whether model-specific protocol adaptations improve repository-maintenance handoff reliability versus general compressed and hybrid-state protocols.

Important caveat: Google Cloud / Vertex access was restricted on 2026-05-30 during the run. Platform errors are separated from model/protocol outcomes.

## Cell Counts

- Raw rows: `426`
- Latest cells: `421`
- Latest OK / OK repaired: `320`
- Latest failures: `101`
- Deprecated/misrouted latest cells: `37`

## Status By Model And Mode

| Model route | Mode | Status | Count |
|---|---|---:|---:|
| `gemini_3_5_flash` | `compressed_general` | `error` | 4 |
| `gemini_3_5_flash` | `compressed_general` | `ok` | 27 |
| `gemini_3_5_flash` | `compressed_general` | `ok_repaired` | 1 |
| `gemini_3_5_flash` | `hybrid_state_general` | `error` | 7 |
| `gemini_3_5_flash` | `hybrid_state_general` | `ok` | 25 |
| `gemini_3_5_flash` | `model_adapted` | `error` | 2 |
| `gemini_3_5_flash` | `model_adapted` | `ok` | 29 |
| `gemini_3_5_flash` | `model_adapted` | `ok_repaired` | 1 |
| `gemini_3_flash_preview` | `compressed_general` | `error` | 1 |
| `gemini_3_flash_preview` | `compressed_general` | `ok` | 12 |
| `gemini_3_flash_preview` | `hybrid_state_general` | `ok` | 12 |
| `gemini_3_flash_preview` | `model_adapted` | `error` | 1 |
| `gemini_3_flash_preview` | `model_adapted` | `ok` | 11 |
| `glm_5` | `compressed_general` | `ok` | 32 |
| `glm_5` | `hybrid_state_general` | `ok` | 32 |
| `glm_5` | `model_adapted` | `ok` | 32 |
| `grok_4_20_reasoning` | `compressed_general` | `error` | 23 |
| `grok_4_20_reasoning` | `compressed_general` | `ok` | 9 |
| `grok_4_20_reasoning` | `hybrid_state_general` | `error` | 27 |
| `grok_4_20_reasoning` | `hybrid_state_general` | `ok` | 5 |
| `grok_4_20_reasoning` | `model_adapted` | `error` | 28 |
| `grok_4_20_reasoning` | `model_adapted` | `ok` | 4 |
| `qwen3_next_80b_instruct` | `compressed_general` | `error` | 3 |
| `qwen3_next_80b_instruct` | `compressed_general` | `ok` | 23 |
| `qwen3_next_80b_instruct` | `compressed_general` | `ok_repaired` | 6 |
| `qwen3_next_80b_instruct` | `hybrid_state_general` | `error` | 5 |
| `qwen3_next_80b_instruct` | `hybrid_state_general` | `ok` | 25 |
| `qwen3_next_80b_instruct` | `hybrid_state_general` | `ok_repaired` | 2 |
| `qwen3_next_80b_instruct` | `model_adapted` | `ok` | 31 |
| `qwen3_next_80b_instruct` | `model_adapted` | `ok_repaired` | 1 |

## Error Classes

| Error class | Count |
|---|---:|
| `403_consumer_suspended` | 9 |
| `429_resource_exhausted` | 88 |
| `json_parse_or_contract` | 4 |

## Token Ledger

- Ledger calls: `320`
- Input tokens: `2390494`
- Output tokens: `334181`
- Estimated total tokens: `2724675`

| Model route | Calls | Input | Output | Estimated total |
|---|---:|---:|---:|---:|
| `gemini_3_5_flash` | 83 | 661438 | 85145 | 746583 |
| `gemini_3_flash_preview` | 35 | 278909 | 28037 | 306946 |
| `glm_5` | 96 | 673102 | 130629 | 803731 |
| `grok_4_20_reasoning` | 18 | 130092 | 12803 | 142895 |
| `qwen3_next_80b_instruct` | 88 | 646953 | 77567 | 724520 |

## Interpretation

- GLM 5 completed round 1 cleanly across all three protocols.
- Qwen3-Next showed strong success, especially under `model_adapted`.
- Gemini 3.5 Flash accepted the corrected model route and showed strongest success under `model_adapted` in the partial round.
- Grok reasoning default route remained operationally fragile.
- The old `gemini_3_flash_preview` route is preserved as a deprecated/misrouted exploratory artifact and should not be merged into official Gemini 3.5 Flash results.

## Reproducibility Artifacts

- Freeze directory: `<LOCAL_RESEARCH_ROOT>/05_Experimentos/EXP16_MODEL_SPECIFIC_PROTOCOL_ADAPTATION\data_freeze\freeze_20260530_225809`
- Clean latest OK: `exp16_latest_cells_clean.jsonl`
- Latest failures: `exp16_failures_latest.jsonl`
- Summary CSV: `exp16_latest_cells_summary.csv`
- Checksums: `SHA256SUMS.txt` inside the freeze directory.

## Claim Strength

- Strong: platform failures must be separated from model/protocol failures.
- Strong: model-adapted prompts improved success for Qwen and Gemini 3.5 Flash in the available round-1 data.
- Cautious: Grok default-route results are confounded by quota/auth/project suspension.
- Not claimed: complete EXP16 full-run result. The experiment was interrupted by provider restriction.

## Deprecated Routes

The following route keys are preserved for auditability but excluded from official real-model summaries:
- `gemini_3_flash_preview`

