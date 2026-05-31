# External Submission and Feedback Plan

Status: prepared

Date: 2026-05-31

## Current Public Package

Repository:

- https://github.com/DaosPath/state-transfer-protocols

Zenodo DOI:

- https://doi.org/10.5281/zenodo.20425831

Core artifacts:

- short paper in `paper_short/`
- full EXP01-EXP16 technical report in `technical_report/`
- reproducibility package in `reproducibility_repo/`
- future roadmap in `reproducibility_repo/FUTURE_EXPERIMENTS_EXP17_EXP23/`

## Recommended Submission Track

Primary target:

- workshop or technical report venue focused on agents, efficient reasoning, prompt compression, model evaluation, or AI systems.

Secondary target:

- TMLR/OpenReview after EXP17 strengthens the statistical analysis.

Not recommended as first target:

- top-tier full conference submission without EXP17, human calibration, and a tighter short-paper version.

## Message Framing

Use this framing:

> We study compact symbolic communication formats as protolanguages for operational state transfer between LLM agents. Across EXP01-EXP16, compressed remains the strongest general baseline, while hybrid_state is a specialized state-transfer format whose benefits appear under explicit state-preservation metrics rather than global quality.

## Materials to Send

Attach or link:

- short paper PDF;
- technical report PDF;
- GitHub repository;
- Zenodo DOI;
- README_REPRODUCIBILITY.md;
- claim/evidence/limitation table;
- future experiments roadmap.

## Outreach Targets

Potential feedback groups:

- prompt compression / LLMLingua researchers;
- agent memory and state summarization researchers;
- LLM-as-judge and evaluation researchers;
- tool-use and software-agent benchmark groups;
- multi-agent workflow researchers;
- AI systems workshops.

## Short Outreach Email

Subject:

Feedback request: Protolanguages for state transfer in multi-agent LLM systems

Body:

Hello,

I am sharing a technical report and reproducibility package on compact symbolic protolanguages for state transfer between LLM agents.

The core result is deliberately bounded: `compressed` is the strongest general baseline, while `hybrid_state` improves explicit state preservation in paired EXP05/EXP06 analyses but does not win global quality. Later experiments test the same protocols across real-agent handoff, deterministic tool use, repository maintenance, long-horizon visual/responsive tasks, and model-specific adaptation.

Repository: https://github.com/DaosPath/state-transfer-protocols

Zenodo DOI: https://doi.org/10.5281/zenodo.20425831

I would appreciate feedback on framing, methodology, related work, and whether this is a better fit for a workshop, TMLR/OpenReview, or another venue.

Best,

Jordy Hernandez Cruzado

## Next Before Formal Submission

1. Run EXP17 confirmatory statistics.
2. Produce a shorter 8-12 page version if the target is a workshop.
3. Decide whether EXP09-EXP16 remain in the main paper or become systems appendix.
4. Add any missing references requested by reviewers or collaborators.
