# Reproducibility README

## Package

This package contains the integrated EXP05/EXP06/EXP07 paper, technical appendix, selected analysis outputs, data-freeze metadata, and checksum manifest.

No literal API keys or provider credential files are included. Runner snapshots may contain environment-variable names such as `API_KEY`.

## Main paper

- `paper/main.pdf`
- `paper/main.tex`
- `paper/PAPER_PRINCIPAL_EXP05_EXP06_EXP07.pdf`
- `paper/PAPER_PRINCIPAL_EXP05_EXP06_EXP07.tex`
- `paper/PAPER_PRINCIPAL_EXP05_EXP06.pdf`
- `paper/PAPER_PRINCIPAL_EXP05_EXP06.tex`
- `paper/main.tex` now includes EXP07 real-agent handoff validation.

## Appendix

- `appendix/TECHNICAL_APPENDIX_EXP05_EXP06.md`
- `appendix/Informe_EXP07_Real_Agent_Handoff_ObjectiveMetrics.md`
- `paper/REVIEWER_HOSTILE_CRITIQUE.md`

## Data freeze

- EXP05 freeze manifest and cleaned outputs are under `data_freeze/EXP05/`.
- EXP06 freeze metadata and frozen raw ledgers are under `data_freeze/EXP06/`.
- EXP07 freeze metadata, raw runs, clean deduplicated runs, operational errors, prompts, task bank, OpenFang config, and checksums are under `data_freeze/EXP07/`.

## Analysis

- EXP05 statistical CSV/Markdown outputs are under `analysis/EXP05/`.
- EXP06 statistical CSV/Markdown outputs are under `analysis/EXP06/`.
- EXP07 objective real-agent handoff CSV/Markdown outputs are under `analysis/EXP07/`.

## Rebuild

From `paper/`, compile twice:

```powershell
pdflatex main.tex
pdflatex main.tex
```

On this machine the working MiKTeX path was:

```powershell
& 'C:\Users\jampi\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe' -interaction=nonstopmode -halt-on-error main.tex
```

## Checksums

See `CHECKSUMS_SHA256.txt`.
