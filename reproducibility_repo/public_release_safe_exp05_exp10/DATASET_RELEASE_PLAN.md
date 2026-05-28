# Dataset Release Plan

## Decision

Do not publish the current full internal package as-is.

Reason: the security sweep found secret-like strings inside frozen EXP06 generated outputs. These appear inside model/task outputs, not in source code, but public release must treat them as sensitive until sanitized.

## Public Release Levels

### Level 1: arXiv Source Only

Safe now.

Include:

- `submission/ARXIV_SOURCE_EXP05_EXP06_EXP07_20260526.zip`

Contents:

- `main.tex`
- `figures/*.pdf`

Exclude:

- raw JSONL
- clean JSONL
- logs
- ledgers
- local configs
- credentials

Security status:

- arXiv source checked for key patterns: no hits.

### Level 2: Public Repo Without Data

Safe after review.

Include:

- `paper/`
- `appendix/`
- `README_PUBLIC.md`
- `README_REPRODUCIBILITY.md`
- analysis scripts
- task banks
- prompt definitions
- checksum manifests for published files

Exclude:

- raw runs
- clean outputs
- local DB files
- WAL/SHM files
- venv/cache
- logs with local paths
- any JSONL containing generated outputs until sanitized

### Level 3: Public Clean Data

Allowed only after redaction.

Include:

- clean deduplicated rows
- operational error summaries
- aggregate CSV tables
- cost summaries
- task banks
- prompts

Required redaction:

- replace key-like strings with `[REDACTED_SECRET_PATTERN]`
- remove or hash local absolute paths if needed
- remove provider account identifiers if present
- rerun security sweep after redaction

### Level 4: Raw Data

Not recommended for initial release.

Raw data may contain:

- model-emitted secret-like strings
- local paths
- provider errors
- operational logs

If raw data is needed later, release a separately sanitized archive with a clear note that raw text has been redacted.

## Licenses

Recommended:

- Paper: CC BY 4.0
- Code/scripts: MIT
- Clean data: CC BY 4.0
- Raw/sanitized generated outputs: CC BY-NC 4.0 if you want to restrict commercial reuse

## Immediate Publication Package

Use:

- `submission/ARXIV_SOURCE_EXP05_EXP06_EXP07_20260526.zip`

Do not upload:

- `data_freeze/`
- `analysis/*/*.jsonl`
- `exp*_runs.jsonl`
- `exp*_cost_ledger.jsonl`

## Required Before Public Repo

1. Create `PUBLIC_RELEASE_SAFE/`.
2. Copy only approved files.
3. Redact generated JSONL if including data.
4. Run `security_sweep_public_package.py` on the public folder.
5. Confirm zero secret findings.
6. Zip/tag release.

## Security Finding Summary

The internal package sweep found secret-like `sk-...` strings in:

- `data_freeze/EXP06/.../exp06_runs.jsonl`
- `analysis/EXP06/.../exp06_clean_ok.jsonl`
- `analysis/EXP06/.../exp06_clean_terminal.jsonl`

Therefore, these files must not be published unless redacted.
