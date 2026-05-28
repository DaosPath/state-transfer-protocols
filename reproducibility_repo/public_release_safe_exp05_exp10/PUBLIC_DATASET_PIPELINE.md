# Public Dataset Pipeline

## Goal

Create a dataset release that keeps useful structure and aggregate results while removing secret-like strings, local paths, and raw private artifacts.

## Build

From the package root:

```powershell
python .\scripts\build_public_redacted_dataset.py --root . --out PUBLIC_DATASET_REDACTED --sweep
```

Outputs:

- `PUBLIC_DATASET_REDACTED/jsonl_redacted/`
- `PUBLIC_DATASET_REDACTED/analysis_csv/`
- `PUBLIC_DATASET_REDACTED/PUBLIC_DATASET_MANIFEST.json`
- `PUBLIC_DATASET_REDACTED/SHA256SUMS.txt`
- `PUBLIC_DATASET_REDACTED/SECURITY_SWEEP_STDOUT.json`

## Redaction Rules

The redactor replaces:

- `sk-...` style keys
- `AIza...` Google API keys
- `Bearer ...` tokens
- known Azure key prefix patterns
- Windows absolute local paths

Replacement preserves JSON structure.

## Release Policy

Safe to publish only if:

1. `security_sweep_public_package.py` reports zero secret findings.
2. Manifest exists.
3. `SHA256SUMS.txt` exists.
4. No raw internal `data_freeze` folder is included.
5. No `.db`, `.wal`, `.shm`, `.env`, `.key`, `.pem`, `.p12`, `.pfx` files exist.

## Current Warning

The internal freeze contains secret-like strings inside generated model outputs. Therefore raw JSONL must not be published directly.
