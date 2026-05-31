# Future Experiments Roadmap: EXP17-EXP23

Project: Protolanguages for State Transfer in Multilingual Multi-Agent Systems

Status: planned, not executed

Date: 2026-05-31

This roadmap records the next experimental agenda after the EXP01-EXP16 technical report. The current report should be treated as the foundational experimental program. The items below are follow-up experiments, not missing requirements for the current paper.

## Framing

The current conclusion is:

- `compressed` is the strongest general baseline.
- `hybrid_state` is a specialized state-transfer protocol.
- Protocol performance depends on the operational surface: judge, model route, tool contract, parser, validator, repository task, visual/responsive constraint, and provider stability.

The next phase should test the same idea under stronger statistical, causal, human, and real-agent conditions.

## EXP17: Confirmatory Statistics

Purpose:

Run a stronger statistical analysis over EXP05-EXP16.

Core questions:

- Do the paired effects survive clustered bootstrap?
- Do they survive mixed-effects models?
- Which variance components dominate: task, language, generator, judge, framework, route, or repetition?

Planned methods:

- Clustered bootstrap by task and generator.
- Mixed-effects models with random intercepts for task, language or variant, generator, judge, framework, and repetition.
- Separate confirmatory analysis for EXP05/EXP06 and systems analysis for EXP07-EXP16.

Expected output:

- Statistical appendix.
- Updated confidence intervals.
- Stronger claim-strength table.

## EXP18: Tokenization and Representation Ablation

Purpose:

Isolate the ZH/tokenization signal more cleanly.

Core questions:

- Is the ZH advantage caused by tokenization, script density, training distribution, or prompt-format interaction?
- Does ZH_PINYIN degrade because of token length, unfamiliar distribution, or semantic distortion?

Planned methods:

- Compare ZH, ZH_PINYIN, EN_LITERAL, ES_LITERAL, synthetic symbolic strings, and controlled token-equivalent variants.
- Record tokenizer counts per provider/model.
- Report cost, input tokens, output tokens, and metric deltas.

Expected output:

- Tokenization/representation report.
- Causal caution table.
- Token count appendix.

## EXP19: Human Evaluation Calibration

Purpose:

Calibrate LLM judges and objective validators against human review.

Core questions:

- Do humans agree that `hybrid_state` preserves operational state better?
- Do LLM judges over-penalize symbolic formats?
- Which metrics best predict human-perceived continuation usefulness?

Planned methods:

- Sample outputs from EXP05/EXP06/EXP07/EXP13.
- Blind human review on fidelity, state preservation, constraint preservation, handoff usefulness, and overclaiming.
- Compare human labels with Gemini/GPT/Grok judge scores and deterministic validator outcomes.

Expected output:

- Human calibration report.
- Judge alignment matrix.
- Revised metric weighting recommendation.

## EXP20: Formal Protocol Grammar

Purpose:

Convert the experimental formats into more formal schemas or grammars.

Core questions:

- Can `compressed`, `hybrid_min`, and `hybrid_state` be defined as parseable grammars?
- Does grammar strictness improve state preservation or harm semantic flexibility?
- Which fields are essential for state transfer?

Planned methods:

- Define schema versions for each protocol.
- Measure parseability, repair rate, information loss, and handoff quality.
- Test optional fields: constraints, dependencies, claims, next actions, risks, validation conditions.

Expected output:

- Protocol grammar specification.
- Parser/validator suite.
- Field ablation table.

## EXP21: Long-Horizon Real Repository Maintenance

Purpose:

Move beyond controlled cells into longer chained repo maintenance.

Core questions:

- How does state degrade over 5-10 sequential handoffs?
- Does `hybrid_state` reduce claim drift, scope drift, and dependency loss over long chains?
- Which protocol best survives real editing, validation, and repair loops?

Planned methods:

- Use one or more live but sandboxed repositories.
- Run chained tasks: edit, validate, repair, summarize, hand off, continue.
- Measure accumulated drift, unexpected files touched, dependency preservation, validator success, and recovery after failure.

Expected output:

- Long-horizon degradation curves.
- Repo-maintenance benchmark.
- Drift and recovery report.

## EXP22: Model-Specific Protocol Adapters

Purpose:

Complete and strengthen the EXP16 line.

Core questions:

- Which models need custom protocol contracts?
- Can route-specific adapters improve parseability and state transfer without overfitting?
- Which failures are model failures and which are provider-surface failures?

Planned methods:

- Compare generic and model-adapted prompts across stable model routes.
- Keep provider failures separate: quota, auth, suspension, policy, routing, truncation.
- Test compact JSON-first, schema echo, two-phase hidden reasoning, and low-ambiguity contracts.

Expected output:

- Adapter comparison report.
- Provider-surface failure taxonomy.
- Model route compatibility matrix.

## EXP23: Cost-Quality-State Frontier

Purpose:

Turn the cost ledger into a formal decision analysis.

Core questions:

- When is `compressed` the best choice?
- When is `hybrid_state` worth extra tokens or lower aggregate quality?
- What is the efficient frontier across cost, quality, state preservation, and failure rate?

Planned methods:

- Use cost ledgers from EXP05-EXP16.
- Compute cost per successful cell, cost per state-preservation point, and cost per validator pass.
- Compare protocols under budget constraints.

Expected output:

- Cost-quality-state frontier plots.
- Budget-aware protocol selection guide.
- Practical deployment recommendations.

## Priority Recommendation

Recommended order:

1. EXP17, because it strengthens every existing claim.
2. EXP18, because the ZH/tokenization result is promising but not closed.
3. EXP22, because EXP16 was truncated and model-specific adapters are directly actionable.
4. EXP21, because it is the strongest next systems experiment.
5. EXP19, because human calibration improves credibility.
6. EXP20, because formal grammar turns the project from empirical formats into a more reusable protocol family.
7. EXP23, because cost-quality-state analysis is most useful once the above evidence is stronger.

## Non-Goals

These future experiments should not claim:

- that `hybrid_state` is globally superior;
- that ZH results prove tokenization causality without stronger controls;
- that provider-route behavior equals model intelligence;
- that saturated controlled tool tasks prove general software-agent competence.

## One-Sentence Agenda

The next phase should test whether compact symbolic protolanguages can preserve operational state under stronger statistics, controlled representation ablations, human calibration, formal schemas, longer repository chains, model-specific adapters, and explicit cost-quality tradeoffs.
