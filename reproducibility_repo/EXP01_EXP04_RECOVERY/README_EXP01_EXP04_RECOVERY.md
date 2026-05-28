# EXP01-EXP04 Recovery Freeze

Created UTC: 2026-05-27T21:18:14.540956+00:00

This folder recovers and freezes the early protocol-compression experiments before EXP05.
Original files were not modified.

## Clean policy

- Cell key: `experiment/language/task_id/mode/run/generator_model`
- Deduplication: last row wins
- OK row: no terminal `error` and no `evaluation_parse_error`
- Terminal errors are preserved separately, not deleted

## Counts

- Clean latest OK rows: 4419
- Terminal error rows: 0
- Secret sweep hits: 0

## Clean Outputs

- `clean_latest_ok/EXP01_EXP04_ALL.clean_latest_ok.jsonl`
- `clean_latest_ok/EXP01_EXP04_ALL.terminal_errors.jsonl`
- `analysis/EXP01_EXP04_summary_counts.csv`

## Frozen Snapshot

- `data_freeze/EXP01_EXP04_RECOVERY_20260527_211812/manifest.json`
- `data_freeze/EXP01_EXP04_RECOVERY_20260527_211812/SHA256SUMS.txt`
- `data_freeze/EXP01_EXP04_RECOVERY_20260527_211812/source_snapshot/`
