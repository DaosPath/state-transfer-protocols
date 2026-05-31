# Reproducibility README

## Package

This package contains the integrated EXP05-EXP16 paper/release trail, technical appendix, selected analysis outputs, frozen metadata, and checksum manifest.

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
- `EXP15_CROSS_CULTURAL_LONG_HORIZON_REPO_MAINTENANCE/Informe_EXP15_Final.md`
- `EXP15B_VISUAL_RESPONSIVE_SCALEUP/Informe_EXP15B_Final.md`
- `EXP15B_VISUAL_RESPONSIVE_SCALEUP/Informe_EXP15B_GrokReasoning_vs_NonReasoning.md`
- `EXP16_MODEL_SPECIFIC_PROTOCOL_ADAPTATION/Informe_EXP16_ModelSpecificProtocolAdaptation.md`
- `EXP16B_GROK_REASONING_ADAPTATION_SEARCH/Informe_EXP16B_GrokReasoningAdaptationSearch.md`
- `paper/REVIEWER_HOSTILE_CRITIQUE.md`

## Data Freeze

- `data_freeze/EXP05/`
- `data_freeze/EXP06/`
- `data_freeze/EXP07/`
- `data_freeze/EXP08_20260527_FINAL/`
- `data_freeze/EXP09_20260527_FINAL/`
- `data_freeze/EXP10_20260527_FINAL/`
- `EXP13_REAL_MULTI_AGENT_SCIENTIFIC_REPO_BENCHMARK/`
- `EXP15_CROSS_CULTURAL_LONG_HORIZON_REPO_MAINTENANCE/`
- `EXP15B_VISUAL_RESPONSIVE_SCALEUP/`
- `EXP16_MODEL_SPECIFIC_PROTOCOL_ADAPTATION/`
- `EXP16B_GROK_REASONING_ADAPTATION_SEARCH/`

Each freeze contains manifests, prompts or prompt-bearing runner snapshots, task banks, cleaned outputs where available, and checksum files. Raw logs are preserved for internal audit; public release should use redacted, latest-cell, or aggregated data.

EXP13 is included as a public latest-cell freeze:

- `exp13_latest_cells_clean.jsonl`
- `exp13_failures_latest.jsonl`
- `task_bank_exp13_scientific_repo.jsonl`
- `prompts_exp13_modes.json`
- `model_registry_exp13.json`
- `validators/validate_scientific_repo.py`
- `SHA256SUMS_EXP13.txt`

EXP15 is included as a public latest-cell freeze:

- `analysis_final/exp15_latest_cells_clean_ok.jsonl`
- `analysis_final/exp15_failures_latest.jsonl`
- `analysis_final/exp15_summary.json`
- `task_bank_exp15_cross_cultural_long_horizon.jsonl`
- `prompts_exp15_modes.json`
- `model_registry_exp15.json`
- `validators/validate_long_horizon_repo.py`
- `figures/fig_exp15_success_by_model.png`

EXP15-B is included as a public latest-cell freeze:

- `analysis_final/exp15b_latest_cells_clean_ok.jsonl`
- `analysis_final/exp15b_failures_latest.jsonl`
- `analysis_final/exp15b_summary.json`
- `analysis_final/exp15b_by_model.csv`
- `exp15b_grok_reasoning_vs_non_reasoning.json`
- `task_bank_exp15b_visual_responsive_scaleup.jsonl`
- `prompts_exp15b_modes.json`
- `model_registry_exp15b.json`
- `validators/validate_long_horizon_repo.py`
- `figures/fig_exp15b_success_by_model.png`

EXP16 is included as a public latest-cell freeze:

- `exp16_latest_cells_clean.jsonl`
- `exp16_failures_latest.jsonl`
- `exp16_latest_cells_summary.csv`
- `exp16_freeze_summary.json`
- `Informe_EXP16_ModelSpecificProtocolAdaptation.md`
- `SHA256SUMS_EXP16.txt`

EXP16-B is included as a public latest-cell freeze:

- `exp16b_latest_cells_clean.jsonl`
- `exp16b_failures_latest.jsonl`
- `exp16b_latest_cells_summary.csv`
- `exp16b_freeze_summary.json`
- `Informe_EXP16B_GrokReasoningAdaptationSearch.md`
- `SHA256SUMS_EXP16B.txt`

## Analysis

- `analysis/EXP05/`
- `analysis/EXP06/`
- `analysis/EXP07/`
- `analysis/EXP08/`
- `analysis/EXP09/`
- `analysis/EXP10/`

The analysis folders contain CSV/JSON/Markdown summaries used by the paper. EXP09 and EXP10 include deterministic validator summaries, repaired historical error counts, and latest-cell views.

## Supplemental Figures

Additional SVG figures are included in:

- `appendix_figures/fig_exp01_exp04_recovery_counts.svg`
- `appendix_figures/fig_exp09_success_by_route_mode.svg`
- `appendix_figures/fig_exp10_metric_means.svg`
- `appendix_figures/fig_exp11_success_by_model.svg`
- `appendix_figures/fig_exp12_success_by_mode.svg`
- `appendix_figures/fig_exp12_claim_drift_by_mode.svg`
- `appendix_figures/fig_exp13_success_by_model_mode.svg`
- `appendix_figures/fig_exp14_success_rate_by_round.svg`
- `appendix_figures/fig_exp14_success_rate_by_mode.svg`
- `appendix_figures/fig_exp16_success_by_model.svg`
- `appendix_figures/fig_exp16_success_by_mode.svg`
- `appendix_figures/fig_exp16b_success_rate_by_variant.svg`
- `appendix_figures/fig_exp16b_failure_classes.svg`
- `appendix_figures/fig_experiment_figure_coverage.svg`

They can be regenerated without external plotting dependencies:

```bash
python scripts/generate_appendix_figures.py
```

## Prompt, Task, Model, Freeze Index

The master index is:

- `appendix/APPENDIX_REPRODUCIBILITY_EXP05_EXP10.md`

It points to:

- exact communication modes: `natural`, `compressed`, `hybrid_min`, `hybrid_state`
- task banks and task templates by experiment
- observed provider/model routes
- freeze dates and route manifest files
- validators, schemas, tool-action contracts, and runner scripts
- repaired historical error logs for EXP09/EXP10 and latest failure evidence for EXP13/EXP15/EXP15-B/EXP16/EXP16-B
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
