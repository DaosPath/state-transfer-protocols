# State-Transfer Protocols

Reproducibility package for the paper:

**State-Transfer Protocols for Multilingual Multi-Agent Handoff**

This repository contains the public paper package, long technical report, cleaned reproducibility artifacts, scripts, manifests, and checksums for the EXP01-EXP15 experimental trail.

## Citation

Archived release:

- GitHub: https://github.com/DaosPath/state-transfer-protocols
- Project page: https://daospath.github.io/state-transfer-protocols/
- Zenodo DOI: https://doi.org/10.5281/zenodo.20425831

## What This Studies

The project treats compact prompting not only as token saving, but as a **state-transfer protocol** for LLM agents. The central comparison is between:

- `natural`: ordinary human-readable handoff text
- `compressed`: compact baseline
- `hybrid_min`: minimal hybrid compression
- `hybrid_state`: state-preserving protocol format

The main empirical conclusion is deliberately bounded:

- `compressed` is the most robust general baseline.
- `hybrid_state` is useful when operational state preservation matters.
- EXP10-EXP12 validate public-page and repository maintenance under deterministic validators.
- EXP13 is the main controlled multi-agent scientific-repository benchmark.
- EXP15 and EXP15-B extend the line into cross-cultural long-horizon visual/responsive repository maintenance.
- In EXP13, `compressed` was more operationally robust, while `hybrid_state` exposed contract fragility in longer role-conditioned tasks.
- In EXP15-B, Gemini 3.5 Flash and GLM 5 remained strong, Qwen was usable but weaker, and Grok Reasoning improved over Grok Non-Reasoning while still showing high contract fragility.

## Repository Layout

- `paper_short/`: compact arXiv/workshop-oriented paper, including LaTeX source and compiled PDF.
- `technical_report/`: longer technical report with methodology, history, costs, errors, and extended evidence, plus the historical EXP01-EXP15 report PDF.
- `reproducibility_repo/`: prompts, task banks, schemas, cleaned data, analysis scripts, manifests, and checksums.
- `reproducibility_repo/EXP13_REAL_MULTI_AGENT_SCIENTIFIC_REPO_BENCHMARK/`: EXP13 report, latest-cell data, failure log, prompts, task bank, validators, runner snapshot, and checksums.
- `reproducibility_repo/EXP15_CROSS_CULTURAL_LONG_HORIZON_REPO_MAINTENANCE/`: EXP15 report, latest-cell data, failure log, prompts, task bank, validators, summaries, and figures.
- `reproducibility_repo/EXP15B_VISUAL_RESPONSIVE_SCALEUP/`: EXP15-B scale-up report, latest-cell data, failure log, Grok Reasoning comparison, prompts, task bank, validators, summaries, and figures.
- `SHA256SUMS.txt`: checksums for public-release files.
- `release_manifest.json`: release metadata.

## Reproducibility Notes

The package is designed to support auditability without exposing provider credentials or private API keys. Cleaned/latest-cell datasets are included where available; raw internal logs with sensitive material are excluded.

EXP13 latest-cell view:

- real model cells: 128
- successful real model cells: 126
- `compressed`: 64/64
- `hybrid_state`: 62/64
- final failures retained as evidence: Gemini `no_json_object`, Azure `no_changes`

EXP15/EXP15-B latest-cell view:

- EXP15: 900 latest cells, 818 successful, 90.9% success, 141/180 complete chains.
- EXP15-B: 2000 latest cells, 1204 successful, 60.2% success, 71/200 complete chains.
- EXP15-B model success: Gemini 382/400, GLM 363/400, Qwen 318/400, Grok Reasoning 98/400, Grok Non-Reasoning 43/400.
- Grok Reasoning improved over Grok Non-Reasoning by 13.75 percentage points, but both remained fragile under strict visual/responsive contract validation.

Before public upload, the release package was scanned for common secret patterns including API keys, bearer tokens, and provider credentials.

## License

- Code and scripts: MIT License.
- Paper, reports, prompts, schemas, and cleaned data: Creative Commons Attribution 4.0 International (CC BY 4.0).

See `LICENSE` and `LICENSE-DATA` for details.
