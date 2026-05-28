# Reviewer Response Notes

## Strong Claims

1. `compressed` is the strongest general-purpose baseline in this experimental family.
2. `hybrid_state` improves judge-scored state preservation in EXP05/EXP06 paired designs.
3. EXP06 confirms a tradeoff: `hybrid_state` improves state preservation but loses global quality.
4. EXP07 demonstrates real-agent objective evaluation with LangGraph and OpenFang.
5. Chinese/script representation effects are real enough to motivate further study, especially ZH vs ZH_PINYIN.

## Weak Or Exploratory Claims

1. The exact mechanism behind the ZH advantage.
2. Any general ranking of model intelligence.
3. Any universal framework ranking between LangGraph and OpenFang.
4. Any claim that `hybrid_state` wins all real-agent settings.
5. Any claim that LLM judges are ground truth.

## Limitations To State Clearly

- EXP05 is broad and exploratory.
- EXP06 is controlled but still judge-scored.
- EXP07 uses objective metrics but is smaller than EXP05/EXP06.
- Provider routing, quotas, policy filters, and hidden serving behavior are confounds.
- Some model names and prices are time-sensitive.
- Public data release requires redaction because generated outputs can contain secret-like strings.

## If Asked: Why LLM-as-Judge?

Answer:

LLM-as-judge was used for scale and multilingual coverage in EXP05/EXP06. We reduce the risk in three ways:

- three-judge calibration in EXP06
- judge agreement reporting
- EXP07 objective real-agent metrics that do not rely on judge preferences

We do not treat any judge as ground truth.

## If Asked: Why Not Human Evaluation?

Answer:

Human evaluation would be valuable, but this paper studies operational protocol behavior across thousands of model/language/framework cells. Human evaluation is reserved for a later validation layer. The current contribution is systems evidence plus controlled paired contrasts.

## If Asked: Why Not Release All Raw Data?

Answer:

The internal freeze is preserved, but raw model outputs may contain local paths or secret-like strings produced during experiments. Public release will use a sanitized dataset and aggregate tables. This is a safety/reproducibility tradeoff, not data hiding.

## If Asked: Does hybrid_state Actually Win?

Answer:

Not globally. The paper's point is the tradeoff:

- `compressed` wins as universal baseline.
- `hybrid_state` is useful for state preservation under judge-scored paired experiments.
- EXP07 shows real-agent benefits are conditional and metric-specific.

## If Asked: Why Include EXP07 If It Weakens hybrid_state?

Answer:

Because it makes the paper more honest and stronger. EXP07 shows that judge-scored gains do not automatically transfer to every real-agent objective metric. It reframes the contribution as protocol-surface interaction rather than a simplistic winner claim.

## If Asked: What Is The Main Contribution?

Answer:

The main contribution is reframing prompt compression as state-transfer protocol design, then showing across discovery, controlled, and real-agent experiments that protocol choice should depend on target function: quality, state preservation, continuity, cost, and execution surface.
