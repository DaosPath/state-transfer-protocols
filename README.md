# State-Transfer Protocols

Reproducibility package for the paper:

**State-Transfer Protocols for Multilingual Multi-Agent Handoff**

This repository contains the public paper package, long technical report, cleaned reproducibility artifacts, scripts, manifests, and checksums for the EXP01-EXP10 experimental trail.

## Citation

Archived release:

- GitHub: https://github.com/DaosPath/state-transfer-protocols
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
- later tool-agent experiments are controlled interface validations, not broad claims about general software-agent superiority.

## Repository Layout

- `paper_short/`: compact arXiv/workshop-oriented paper, including LaTeX source and compiled PDF.
- `technical_report/`: longer technical report with methodology, history, costs, errors, and extended evidence.
- `reproducibility_repo/`: prompts, task banks, schemas, cleaned data, analysis scripts, manifests, and checksums.
- `SHA256SUMS.txt`: checksums for public-release files.
- `release_manifest.json`: release metadata.

## Reproducibility Notes

The package is designed to support auditability without exposing provider credentials or private API keys. Cleaned/latest-cell datasets are included where available; raw internal logs with sensitive material are excluded.

Before public upload, the release package was scanned for common secret patterns including API keys, bearer tokens, and provider credentials.

## License

- Code and scripts: MIT License.
- Paper, reports, prompts, schemas, and cleaned data: Creative Commons Attribution 4.0 International (CC BY 4.0).

See `LICENSE` and `LICENSE-DATA` for details.
