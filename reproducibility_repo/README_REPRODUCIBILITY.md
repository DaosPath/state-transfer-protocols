# Reproducibility README

## Package

This package contains the integrated EXP05-EXP13 paper/release trail, technical appendix, selected analysis outputs, frozen metadata, and checksum manifest.

No literal API keys or provider credential files are included. Runner snapshots may contain environment-variable names such as `API_KEY`, but not secret values.

## Main Paper

- `paper/main.tex`
- `paper/main.pdf`
- `paper/PAPER_PRINCIPAL_EXP05_EXP06_EXP07_EXP08_EXP09_EXP10.pdf`

## Appendix

- `appendix/TECHNICAL_APPENDIX_EXP05_EXP06.md`
- `appendix/TECHNICAL_APPENDIX_LONG_EXP05_EXP08.md`
- `appendix/APPENDIX_REPRODUCIBILITY_EXP05_EXP10.md`
- `appendix/Informe_EXP07_Real_Agent_Handoff_ObjectiveMetrics.md`
- `appendix/Informe_EXP08_Real_Agent_Scaleup.md`
- `appendix/Informe_EXP09_Real_Tool_Use_Agent_Tasks.md`
- `appendix/Informe_EXP10_Public_Repo_Tool_Agent.md`
- `EXP13_REAL_MULTI_AGENT_SCIENTIFIC_REPO_BENCHMARK/Informe_EXP13_RealMultiAgentScientificRepoBenchmark.md`
- `paper/REVIEWER_HOSTILE_CRITIQUE.md`

## Data Freeze

- `data_freeze/EXP05/`
- `data_freeze/EXP06/`
- `data_freeze/EXP07/`
- `data_freeze/EXP08_20260527_FINAL/`
- `data_freeze/EXP09_20260527_FINAL/`
- `data_freeze/EXP10_20260527_FINAL/`
- `EXP13_REAL_MULTI_AGENT_SCIENTIFIC_REPO_BENCHMARK/`

Each freeze contains manifests, prompts or prompt-bearing runner snapshots, task banks, cleaned outputs where available, and checksum files. Raw logs are preserved for internal audit; public release should use redacted, latest-cell, or aggregated data.

EXP13 is included as a public latest-cell freeze:

- `exp13_latest_cells_clean.jsonl`
- `exp13_failures_latest.jsonl`
- `task_bank_exp13_scientific_repo.jsonl`
- `prompts_exp13_modes.json`
- `model_registry_exp13.json`
- `validators/validate_scientific_repo.py`
- `SHA256SUMS_EXP13.txt`

## Analysis

- `analysis/EXP05/`
- `analysis/EXP06/`
- `analysis/EXP07/`
- `analysis/EXP08/`
- `analysis/EXP09/`
- `analysis/EXP10/`

The analysis folders contain CSV/JSON/Markdown summaries used by the paper. EXP09 and EXP10 include deterministic validator summaries, repaired historical error counts, and latest-cell views.

## Prompt, Task, Model, Freeze Index

The master index is:

- `appendix/APPENDIX_REPRODUCIBILITY_EXP05_EXP10.md`

It points to:

- exact communication modes: `natural`, `compressed`, `hybrid_min`, `hybrid_state`
- task banks and task templates by experiment
- observed provider/model routes
- freeze dates and route manifest files
- validators, schemas, tool-action contracts, and runner scripts
- repaired historical error logs for EXP09/EXP10 and latest failure evidence for EXP13
- cleaning and deduplication policy
- freeze/checksum locations
- auditable example rows and reports

## Rebuild

Preferred local rebuild from this package:

```powershell
python path\to\compile_latex.py .\paper\main.tex --json
```

Fallback from `paper/`:

```powershell
pdflatex main.tex
pdflatex main.tex
```

## Checksums

See `CHECKSUMS_SHA256.txt`.

## Public Release Boundary

Safe to publish after final sweep:

- paper source and PDF
- appendix
- aggregate CSV/JSON summaries
- task banks
- prompt definitions
- analysis scripts
- checksum manifests
- redacted JSONL samples

Do not publish:

- API keys
- credential files
- local auth caches
- raw provider logs before redaction
- cost ledgers containing private local/provider artifacts
- private local paths unless sanitized
