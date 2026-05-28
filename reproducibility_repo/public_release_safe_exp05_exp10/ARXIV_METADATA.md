# arXiv Metadata

## Title

Symbolic Compression Protocols for Multilingual Multi-Agent Handoff Across Frontier Models

## Authors

Jordy Hernandez Cruzado

Affiliation:

Hijos Del Sol Research / Independent Researcher

## Categories

Primary:

- `cs.CL` - Computation and Language

Cross-list:

- `cs.AI` - Artificial Intelligence
- `cs.LG` - Machine Learning

## Abstract

Large language model agents increasingly need to transfer operational state across models, providers, and languages without carrying full conversational histories. We study compact symbolic formats as state-transfer protocols, asking when they preserve semantic fidelity, operational continuity, and handoff quality across heterogeneous model families. EXP05 is a broad discovery experiment across multilingual and multi-model settings; EXP06 is a controlled follow-up comparing compressed against hybrid_state with tokenizer/variant ablations and three-judge calibration; EXP07 adds real-agent validation with LangGraph and OpenFang using objective handoff metrics. Across EXP05 and EXP06, compressed is the strongest general baseline, while hybrid_state improves judge-scored state preservation but does not win global quality. EXP07 shows that real-agent objective metrics are feasible and that compressed remains the strongest operational baseline, with hybrid_state showing only conditional benefits in selected strata. We argue that prompt compression should be reframed as interoperable state-transfer protocol design: compressed is the universal baseline, while hybrid_state is a specialized state-oriented protocol whose benefits depend on the target execution surface.

## Comments

Technical report. Includes EXP05 broad discovery, EXP06 controlled follow-up, and EXP07 real-agent handoff validation. Source package includes TeX and figures only; data and code release are staged separately after sanitization.

Repository:

- https://github.com/DaosPath/state-transfer-protocols

Archived release DOI:

- https://doi.org/10.5281/zenodo.20425831

## License

Recommended:

- arXiv paper license: CC BY 4.0 if available, otherwise arXiv default.
- Code: MIT.
- Clean data: CC BY 4.0 or CC BY-NC 4.0.

## Submission Files

Upload:

- `paper_short/arxiv_source_focused_handoff.zip`

Do not upload:

- internal `data_freeze/`
- raw JSONL
- clean JSONL before redaction
- local logs
- cost ledgers with local/provider artifacts

## Notes To Self

- arXiv account default category already set to `cs.CL`.
- Confirm author name appears as `Jordy Hernandez Cruzado`.
- Confirm affiliation as `Hijos Del Sol Research`.
- Check generated PDF after arXiv compiles source.
