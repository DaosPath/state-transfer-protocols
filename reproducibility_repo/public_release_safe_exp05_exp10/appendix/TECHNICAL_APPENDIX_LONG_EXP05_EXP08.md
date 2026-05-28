# Technical Appendix: EXP05-EXP08

This appendix records prompts, task banks, metrics, cleaning policy, failures, data security, and reproducibility artifacts for the symbolic compression protocol experiments.

## A. Experimental Path

- EXP05: broad multilingual multi-model discovery over natural, compressed, hybrid_min, and hybrid_state.

- EXP06: controlled causal transfer test for compressed vs hybrid_state under language and tokenizer ablations.

- EXP07: real-agent handoff evaluation with LangGraph/OpenFang-style execution and objective metrics.

- EXP08: scale-up run in progress at appendix build time; same real-agent design with larger task/repetition matrix.

## B. Exact Prompt Protocols

### EXP05 modes

```json
{
  "prompt_version": "exp05_modes_2026-05-18.1",
  "shared_prefix": "Use final answer only. Do not reveal hidden reasoning. Follow the target language exactly. Output plain text only unless a mode explicitly asks for fields. Do not invent data.",
  "modes": {
    "natural": {
      "max_tokens": 650,
      "template": "Language: {language}\nMode: natural\n\nWrite a clear natural-language answer for the task. Keep it concise but complete. Preserve objective, evidence, risk, decision, and next action when present. Avoid decorative prose.\n\nTask:\n{task_text}"
    },
    "compressed": {
      "max_tokens": 360,
      "template": "Language: {language}\nMode: compressed\n\nWrite a compressed operational answer. Short phrases. No filler. No long explanation. Preserve all critical entities, numbers, decisions, risks, and next actions. Use readable compact natural language, not obscure symbols.\n\nPreferred shape when useful:\nP: problem\nS: solution/decision\nR: risk\nN: next\n\nTask:\n{task_text}"
    },
    "hybrid_min": {
      "max_tokens": 260,
      "template": "Language: {language}\nMode: hybrid_min\n\nWrite the minimal hybrid protocol. One compact line if possible. Use only useful fields. Do not fill empty fields. Separate fields with semicolons. Preserve meaning over style.\n\nAllowed fields:\ng=goal; p=problem; c=context; e=evidence; d=decision; s=solution; r=risk; n=next; v=verify; m=metric; lim=limit; conf=confidence.\n\nRules:\n- Use 2 to 5 fields.\n- No Markdown.\n- No full paragraphs.\n- No invented data.\n- Must be understandable by another agent.\n\nTask:\n{task_text}"
    },
    "hybrid_state": {
      "max_tokens": 380,
      "template": "Language: {language}\nMode: hybrid_state\n\nWrite a compact state-preserving handoff. Use compact fields plus short natural fragments. Preserve operational continuity: objective, current state, evidence, decision, risk, verification, and next action.\n\nAllowed fields:\ng=goal; st=state; c=context; e=evidence; d=decision; r=risk; v=verify; n=next; mem=memory; lim=limit; conf=confidence.\n\nRules:\n- Use no more than 7 fields.\n- Each field must add information.\n- Prefer compact clarity over extreme compression.\n- No invented data.\n- Output must be directly usable by the next agent.\n\nTask:\n{task_text}"
    }
  }
}
```

### EXP06 modes

```json
{
  "prompt_version": "exp06_modes_2026-05-23.1",
  "shared_prefix": "Use final answer only. Do not reveal hidden reasoning. Follow the target language or variant exactly. Output plain text only. Do not invent data.",
  "modes": {
    "compressed": {
      "max_tokens": 360,
      "template": "Language/variant: {language}\nMode: compressed\n\nWrite a compressed operational answer. Short phrases. No filler. Preserve objective, current state, evidence, decision, risk, verification, and next action. Use readable compact natural language, not obscure symbols.\n\nPreferred shape when useful:\nP: problem\nS: state/solution\nR: risk\nV: verify\nN: next\n\nTask:\n{task_text}"
    },
    "hybrid_state": {
      "max_tokens": 380,
      "template": "Language/variant: {language}\nMode: hybrid_state\n\nWrite a compact state-preserving handoff. Use compact fields plus short natural fragments. Preserve operational continuity: objective, current state, evidence, decision, risk, verification, next action, and memory needed by the next agent.\n\nAllowed fields:\ng=goal; st=state; c=context; e=evidence; d=decision; r=risk; v=verify; n=next; mem=memory; lim=limit; conf=confidence.\n\nRules:\n- Use no more than 7 fields.\n- Each field must add information.\n- Prefer compact clarity over extreme compression.\n- No invented data.\n- Output must be directly usable by the next agent.\n\nTask:\n{task_text}"
    }
  }
}
```

### EXP07 modes

```json
{
  "natural": {
    "agent_a_instruction": "Work on the task until the interruption point. Write a handoff for the next agent in normal prose. Include all variables, constraints, completed subtasks, pending subtasks, plan steps, risks, and next action.",
    "handoff_style": "Plain natural-language operational summary."
  },
  "compressed": {
    "agent_a_instruction": "Work on the task until the interruption point. Write a compact handoff using dense operational notes. Preserve variables, constraints, completed subtasks, pending subtasks, plan steps, risks, and next action.",
    "handoff_style": "Dense compact notes with minimal prose."
  },
  "hybrid_state": {
    "agent_a_instruction": "Work on the task until the interruption point. Write a hybrid_state handoff using explicit state fields: G goal, VAR variables, C constraints, DONE completed subtasks, TODO pending subtasks, PLAN ordered steps, R risks, V checks, NEXT next action. Preserve operational continuity.",
    "handoff_style": "Structured symbolic state-transfer protocol."
  }
}
```

## C. Evaluator Prompting and Metrics

### EXP05 evaluator prompt

```json
{
  "prompt_version": "exp05_evaluator_2026-05-18.1",
  "max_tokens": 2200,
  "template": "You are a strict technical evaluator for EXP05_PREMIUM_MULTIMODEL_TRILINGUAL.\nUse final answer only. Return strict JSON only. No Markdown. No explanation outside JSON.\n\nEvaluate the generated answer against the original task.\n\nContext:\n- language: {language}\n- model: {generator_model}\n- mode: {mode}\n- task_id: {task_id}\n- task_group: {task_group}\n\nOriginal task:\n{task_text}\n\nGenerated answer:\n{output_text}\n\nScore 1 to 5. For positive metrics, 5 is best. For negative metrics, 1 is best.\n\nPositive metrics:\n- semantic_fidelity\n- clarity\n- utility\n- completeness\n- state_preservation\n- operational_continuity\n- context_recoverability\n- handoff_quality\n- compactness\n- inter_model_transferability\n- language_stability\n\nNegative metrics:\n- ambiguity\n- information_loss\n\nAlso provide:\n- critical_failure: true/false\n- winner_reading: short label\n- notes: one compact sentence\n\nReturn exactly this JSON schema:\n{\n  \"semantic_fidelity\": 0,\n  \"clarity\": 0,\n  \"utility\": 0,\n  \"completeness\": 0,\n  \"state_preservation\": 0,\n  \"operational_continuity\": 0,\n  \"context_recoverability\": 0,\n  \"handoff_quality\": 0,\n  \"compactness\": 0,\n  \"ambiguity\": 0,\n  \"information_loss\": 0,\n  \"inter_model_transferability\": 0,\n  \"language_stability\": 0,\n  \"critical_failure\": false,\n  \"winner_reading\": \"\",\n  \"notes\": \"\"\n}"
}
```

### EXP06 evaluator prompt

```json
{
  "prompt_version": "exp06_evaluator_2026-05-23.1",
  "max_tokens": 2200,
  "template": "You are a strict technical evaluator for EXP06_CAUSAL_PROTOCOL_TRANSFER.\nUse final answer only. Return strict JSON only. No Markdown. No explanation outside JSON.\n\nEvaluate the generated answer against the original task.\n\nContext:\n- experiment: {phase}\n- language_or_variant: {language}\n- generator_model: {generator_model}\n- mode: {mode}\n- task_id: {task_id}\n- task_group: {task_group}\n\nOriginal task:\n{task_text}\n\nGenerated answer:\n{output_text}\n\nScore 1 to 5. For positive metrics, 5 is best. For negative metrics, 1 is best.\n\nPositive metrics:\n- semantic_fidelity\n- clarity\n- utility\n- completeness\n- state_preservation\n- operational_continuity\n- context_recoverability\n- handoff_quality\n- compactness\n- protocol_transferability\n- language_or_variant_stability\n\nNegative metrics:\n- ambiguity\n- information_loss\n\nAlso provide:\n- critical_failure: true/false\n- winner_reading: short label\n- notes: one compact sentence\n\nReturn exactly this JSON schema:\n{{\n  \"semantic_fidelity\": 0,\n  \"clarity\": 0,\n  \"utility\": 0,\n  \"completeness\": 0,\n  \"state_preservation\": 0,\n  \"operational_continuity\": 0,\n  \"context_recoverability\": 0,\n  \"handoff_quality\": 0,\n  \"compactness\": 0,\n  \"ambiguity\": 0,\n  \"information_loss\": 0,\n  \"protocol_transferability\": 0,\n  \"language_or_variant_stability\": 0,\n  \"critical_failure\": false,\n  \"winner_reading\": \"\",\n  \"notes\": \"\"\n}}"
}
```

### Core LLM-judge metrics

- Positive: semantic_fidelity, clarity, utility, completeness, state_preservation, operational_continuity, context_recoverability, handoff_quality, compactness.

- Negative: ambiguity, information_loss.

- EXP05 additions: inter_model_consistency, judge_agreement, language_stability, protocol_transferability.

### Objective handoff metrics

- variable_recovery_rate: required variable values recovered by the receiving agent.

- subtask_completion_rate: target subtasks completed after handoff.

- plan_continuity_rate: plan steps preserved and continued.

- constraint_retention_rate: constraints preserved in execution.

- handoff_success: strict end-to-end success flag.

- state_error_count: count of missing, invented, or corrupted state elements.

## D. Task Banks

### EXP05 task bank sample

```jsonl
{"task_id":"T001","task_group":"A_context_summary","source":"EXP04_derived","task_es":"Resume el estado del proyecto despues de EXP04: hybrid_min gano costo en ES/EN/ZH, compressed fue mas estable en calidad y hybrid_state conservo mejor handoff. Conserva decision, evidencia, riesgo y siguiente paso.","task_en":"Summarize the project state after EXP04: hybrid_min won cost in ES/EN/ZH, compressed was more stable in quality, and hybrid_state preserved handoff better. Preserve decision, evidence, risk, and next step.","task_zh":"总结EXP04后的项目状态：hybrid_min在ES/EN/ZH中成本最低，compressed质量更稳定，hybrid_state更好地保留handoff。保留决策、证据、风险和下一步。"}
{"task_id":"T002","task_group":"A_context_summary","source":"EXP05_new","task_es":"Convierte una bitacora experimental larga en un resumen operativo para otro agente. Debe incluir objetivo, modelo usado, modo, metrica principal, anomalia y accion pendiente.","task_en":"Convert a long experiment log into an operational summary for another agent. Include objective, model used, mode, main metric, anomaly, and pending action.","task_zh":"把一段很长的实验日志转换成给另一个代理使用的操作性摘要。必须包含目标、使用的模型、模式、主要指标、异常和待执行动作。"}
{"task_id":"T003","task_group":"A_context_summary","source":"EXP05_new","task_es":"Resume un hallazgo parcial sin exagerar: un protocolo ahorra tokens en un modelo, pero pierde continuidad en otro. Conserva limite metodologico y recomendacion prudente.","task_en":"Summarize a partial finding without exaggeration: a protocol saves tokens in one model but loses continuity in another. Preserve methodological limitation and cautious recommendation.","task_zh":"不夸大地总结一个部分发现：某协议在一个模型中节省token，但在另一个模型中损失连续性。保留方法限制和谨慎建议。"}
{"task_id":"T004","task_group":"B_handoff","source":"EXP04_derived","task_es":"Agente A debe pasar a Agente B una comparacion entre compressed y hybrid_state. Incluye objetivo, contexto, evidencia minima, decision provisional, riesgo y verificacion.","task_en":"Agent A must pass Agent B a comparison between compressed and hybrid_state. Include objective, context, minimal evidence, provisional decision, risk, and verification.","task_zh":"代理A必须把compressed和hybrid_state的比较交接给代理B。包括目标、上下文、最小证据、临时决策、风险和验证。"}
{"task_id":"T005","task_group":"B_handoff","source":"EXP05_new","task_es":"Un supervisor entrega a un trabajador la tarea de validar un modelo nuevo en Vertex. Conserva region, nombre del modelo, prueba minima, criterio de exito y plan si hay cuota agotada.","task_en":"A supervisor gives a worker the task of validating a new model in Vertex. Preserve region, model name, minimal test, success criterion, and plan if quota is exhausted.","task_zh":"监督代理把在Vertex中验证新模型的任务交给工作代理。保留区域、模型名、最小测试、成功标准和配额耗尽时的计划。"}
{"task_id":"T006","task_group":"B_handoff","source":"EXP05_new","task_es":"Agente A detecto que el evaluador y el auditor discrepan. Prepara un handoff compacto para resolver el desacuerdo sin perder metricas ni salida original.","task_en":"Agent A found that the evaluator and auditor disagree. Prepare a compact handoff to resolve the disagreement without losing metrics or the original output.","task_zh":"代理A发现评估器和审计器意见不一致。准备一个紧凑交接，用于解决分歧，同时不能丢失指标或原始输出。"}
{"task_id":"T007","task_group":"C_planning","source":"EXP05_new","task_es":"Crea un plan de tres pasos para ejecutar EXP05 de forma resumible: manifest, cola de celdas, checkpoints y reportes parciales.","task_en":"Create a three-step plan to run EXP05 resumably: manifest, cell queue, checkpoints, and partial reports.","task_zh":"制定三步计划，以可恢复方式执行EXP05：manifest、单元队列、checkpoint和部分报告。"}
{"task_id":"T008","task_group":"C_planning","source":"EXP04_derived","task_es":"Ordena estas acciones para reducir riesgo experimental: validar modelos, congelar prompts, correr piloto, estimar costo, ejecutar FULL, auditar muestra, generar ELO.","task_en":"Order these actions to reduce experimental risk: validate models, freeze prompts, run pilot, estimate cost, execute FULL, audit sample, generate ELO.","task_zh":"为降低实验风险，对以下动作排序：验证模型、冻结提示、运行pilot、估算成本、执行FULL、审计样本、生成ELO。"}
{"task_id":"T009","task_group":"C_planning","source":"EXP05_new","task_es":"Propón una mitigacion para deriva semantica cuando cinco modelos interpretan el mismo marcador compacto de manera diferente.","task_en":"Propose a mitigation for semantic drift when five models interpret the same compact marker differently.","task_zh":"当五个模型对同一个紧凑标记有不同解释时，提出语义漂移缓解方案。"}
{"task_id":"T010","task_group":"D_persistent_state","source":"EXP05_new","task_es":"Diseña una memoria operativa minima para que un experimento interrumpido pueda continuar sin repetir celdas ya completadas.","task_en":"Design minimal operational memory so an interrupted experiment can continue without repeating already completed cells.","task_zh":"设计一种最小操作记忆，使中断的实验能够继续，而不重复已经完成的单元。"}
{"task_id":"T011","task_group":"D_persistent_state","source":"EXP05_new","task_es":"Comprime un estado de ejecucion con: presupuesto restante, modelos bloqueados por cuota, filas completadas, errores retryable y siguiente lote seguro.","task_en":"Compress 
```

### EXP06 task bank inventory

- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/evaluator_prompt_exp06.json`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/exp06_checkpoints.jsonl`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/exp06_cost_ledger.jsonl`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/exp06_cost_policy.json`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/exp06_errors.jsonl`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/exp06_manifest.json`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/exp06_runs.jsonl`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/freeze_exp06_policy_failures.py`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/PLAN_EXP06_CAUSAL_PROTOCOL_TRANSFER.md`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/prompts_exp06_modes.json`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/run_exp06_resumable.py`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/SHA256SUMS.txt`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/snapshot_manifest.json`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/status_exp06.py`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/task_bank_exp06_a.jsonl`
- `data_freeze/EXP06/EXP06_FREEZE_20260526_151836/task_bank_exp06_b.jsonl`

### EXP07 task bank sample

```jsonl
{"task_id":"H001","domain":"research_state","task":"Continue a research memo after interruption. Preserve dataset name, claim status, next analysis, and forbidden overclaim.","variables":{"dataset":"EXP06_clean_ok","claim":"hybrid_state improves state_preservation only","next_analysis":"paired deltas by generator","forbidden":"do not claim global quality win"},"constraints":["must separate state_preservation from global quality","must mention compressed as baseline"],"subtasks":["identify current claim","name next analysis","state limitation","produce next action"],"plan_steps":["read handoff","recover variables","continue memo","state next action"]}
{"task_id":"H002","domain":"csv_analysis","task":"Continue a CSV analysis workflow. Preserve file path, grouping variable, metric, filter, and output table name.","variables":{"file":"analysis/EXP06/paired_effect_by_phase_language.csv","group_by":"language","metric":"state_preservation_delta","filter":"phase == A","output":"table_phaseA_language_state"},"constraints":["no new data collection","report missing columns if absent"],"subtasks":["load file","filter phase A","group by language","summarize metric"],"plan_steps":["validate columns","apply filter","aggregate","write summary"]}
{"task_id":"H003","domain":"debugging","task":"Continue debugging a failed experiment runner. Preserve error class, suspected cause, attempted fix, and next diagnostic.","variables":{"error":"JSON parse failure","suspected_cause":"model returned markdown before JSON","attempted_fix":"strip code fences","next_diagnostic":"count failures by model and mode"},"constraints":["do not delete raw logs","keep failed rows as operational evidence"],"subtasks":["classify error","preserve raw row","apply parser repair","summarize failures"],"plan_steps":["inspect last error","repair parse","rerun only failed cell","update ledger"]}
{"task_id":"H004","domain":"document_editing","task":"Continue editing a paper section. Preserve section name, target claim, citation need, and reviewer risk.","variables":{"section":"Limitations","target_claim":"ZH effect is promising but not causal","citation_need":"tokenization/language disparity reference","reviewer_risk":"overstating tokenizer causality"},"constraints":["must use cautious language","must not call ZH result proven"],"subtasks":["revise limitation","add caution","preserve claim boundary","name future work"],"plan_steps":["read current section","edit paragraph","check claim strength","save revision"]}
{"task_id":"H005","domain":"tool_workflow","task":"Continue a tool-use workflow after Agent A created partial artifacts. Preserve artifact names, validation check, and remaining command.","variables":{"artifact":"exp07_summary.json","validation":"schema contains metrics and cell_id","remaining_command":"run status_exp07.py","risk":"duplicate cells on resume"},"constraints":["do not overwrite successful cells","append-only logs"],"subtasks":["verify artifact exists","validate schema","run status","report pending cells"],"plan_steps":["load manifest","check artifact","run status","resume missing cells"]}
{"task_id":"H006","domain":"planning","task":"Continue an implementation plan with budget and quota constraints. Preserve budget, rate limit, retry rule, and stop condition.","variables":{"budget_usd":"150","rate_limit":"4 calls/minute for expensive providers","retry_rule":"sleep 120 seconds on quota","stop_condition":"hard budget or unresolved provider auth"},"constraints":["must be resumable","must record per-call cost"],"subtasks":["state budget","state rate limit","state retry","state stop condition"],"plan_steps":["read quota policy","schedule cells","execute with retries","write ledger"]}
{"task_id":"H007","domain":"data_extraction","task":"Continue structured extraction from a short report. Preserve required fields, source label, confidence rule, and output format.","variables":{"source_label":"reviewer_note_07","required_fields":"claim, evidence, risk, action","confidence_rule":"low if evidence absent","output_format":"strict JSON array"},"constraints":["no prose outside JSON","missing fields must be null"],"subtasks":["extract claim","extract evidence","extract risk","extract action"],"plan_steps":["parse source","map fields","assign confidence","emit JSON"]}
{"task_id":"H008","domain":"handoff_long","task":"Continue a long multi-agent handoff. Preserve owner, dependency, blocker, active decision, and final deliverable.","variables":{"owner":"Agent B","dependency":"OpenFang daemon config","blocker":"provider credentials not injected","active_decision":"use objective metrics before LLM judges","deliverable":"EXP07 clean results and report"},"constraints":["do not ask LLM judge for primary score","keep credentials external"],"subtasks":["recover owner","recover dependency","recover blocker","continue decision","name deliverable"],"plan_steps":["read state","resolve blocker","execute objective run","write report"]}
{"task_id":"H009","domain":"qa",
```

## E. Cleaning and Deduplication

Policy: keep the last successful row per cell_id for analysis; keep policy_failure and operational_error as terminal evidence; ignore historical errors when later OK exists, but do not delete them from frozen raw logs.

### EXP06 cleaning report

```json
{
  "analysis_dir": "C:\\Hijosdelsol\\ia\\Investigacion_y_Produccion\\Investigaciones\\Protolenguaje_AgentesIA\\05_Experimentos\\EXP06_CAUSAL_PROTOCOL_TRANSFER\\analysis\\EXP06_ANALYSIS_20260526_151836",
  "clean_stage_status": {
    "evaluation_main:ok": 4689,
    "generation:ok": 1563,
    "generation:policy_failure": 21
  },
  "closure": {
    "clean_ok_rows": 6252,
    "estimated_cost_usd": 34.067306,
    "evaluation_ok": 4689,
    "generation_ok": 1563,
    "policy_failures": 21,
    "raw_rows": 6400,
    "unresolved_errors": 0
  },
  "created_local": "2026-05-26T15:18:37",
  "experiment_id": "EXP06_CAUSAL_PROTOCOL_TRANSFER",
  "policy_failure_by_task": {
    "A005": 9,
    "A008": 6,
    "A011": 3,
    "A012": 3
  },
  "raw_stage_status": {
    "evaluation_main:error": 22,
    "evaluation_main:ok": 4689,
    "generation:error": 105,
    "generation:ok": 1563,
    "generation:policy_failure": 21
  },
  "snapshot_dir": "C:\\Hijosdelsol\\ia\\Investigacion_y_Produccion\\Investigaciones\\Protolenguaje_AgentesIA\\05_Experimentos\\EXP06_CAUSAL_PROTOCOL_TRANSFER\\freezes\\EXP06_FREEZE_20260526_151836",
  "snapshot_files": [
    {
      "bytes": 13512281,
      "file": "exp06_runs.jsonl",
      "sha256": "3fc27cef269fd61c464a2543bb7e958e72dd936343a640cc7b0acc0f014b1e14"
    },
    {
      "bytes": 3323119,
      "file": "exp06_cost_ledger.jsonl",
      "sha256": "b0370016bff709e0eed316ca29baaf551dc6ac7869f4782c2c98186c149e0193"
    },
    {
      "bytes": 198565,
      "file": "exp06_errors.jsonl",
      "sha256": "7fff9c542edb049ef61e1883095bd91c69a997801320a1213f44309eadf7f793"
    },
    {
      "bytes": 2497,
      "file": "exp06_checkpoints.jsonl",
      "sha256": "3990974505389a5a3c4d6477d7fdb4575ba17647a5ed75c1cb8c39ee9b10f087"
    },
    {
      "bytes": 1758,
      "file": "exp06_manifest.json",
      "sha256": "7e2ff4a9075ac212ff5af62af7a4bc5ce2013ba18f936f918248bb1f2ff730ea"
    },
    {
      "bytes": 1418,
      "file": "prompts_exp06_modes.json",
      "sha256": "7f04d48b3298d3c3484fd505592b124d0b64eca6ebd6393a6f0876761c3dc828"
    },
    {
      "bytes": 1545,
      "file": "evaluator_prompt_exp06.json",
      "sha256": "c19bc56c71297467b40dbb0b954872dc493b1b39e818768b694d7484c3ceaefe"
    },
    {
      "bytes": 6667,
      "file": "task_bank_exp06_a.jsonl",
      "sha256": "867e32060e03f2bdfaeec6146f7d9432023c0c4c15fc790f4c69dd1cf6ae91ed"
    },
    {
      "bytes": 7145,
      "file": "task_bank_exp06_b.jsonl",
      "sha256": "ba6ae5b1ba5a93c1b9e5dd2a20aa0b18625b7dd93793f67a6612159ab514dc57"
    },
    {
      "bytes": 420,
      "file": "exp06_cost_policy.json",
      "sha256": "212daf325f80d6fe2775f019956a97f20e1c9656fe406ddde5e612cebb5f4e05"
    },
    {
      "bytes": 6819,
      "file": "PLAN_EXP06_CAUSAL_PROTOCOL_TRANSFER.md",
      "sha256": "f9115ce60e2f9f3314dfabbec86695c95d5609e9b9d5be6b3cd7bc3410fb52cb"
    },
    {
      "bytes": 17606,
      "file": "run_exp06_resumable.py",
      "sha256": "6cfa1e14e7d9d399dd901dc1d78300e55e91f5c7f5bd198a5ce6126262ca126e"
    },
    {
      "bytes": 1704,
      "file": "status_exp06.py",
      "sha256": "c14687be651a62c9efef30be7b61cd3e0097633199b98e05ac1154d6dcfff9d8"
    },
    {
      "bytes": 3045,
      "file": "freeze_exp06_policy_failures.py",
      "sha256": "295169c12a63132d3d38904dc771239226b592835ce4a52b4a61e6047820caf7"
    }
  ]
}
```

## F. Main Result Tables

### EXP05 by mode

| mode | n | semantic_fidelity_mean | semantic_fidelity_sd | semantic_fidelity_ci95_low | semantic_fidelity_ci95_high | utility_mean | utility_sd | utility_ci95_low | utility_ci95_high | state_preservation_mean | state_preservation_sd | state_preservation_ci95_low | state_preservation_ci95_high | operational_continuity_mean | operational_continuity_sd | operational_continuity_ci95_low | operational_continuity_ci95_high | handoff_quality_mean | handoff_quality_sd | handoff_quality_ci95_low | handoff_quality_ci95_high | compactness_mean | compactness_sd | compactness_ci95_low | compactness_ci95_high | ambiguity_mean | ambiguity_sd | ambiguity_ci95_low | ambiguity_ci95_high | information_loss_mean | information_loss_sd | information_loss_ci95_low | information_loss_ci95_high | quality_index_mean | quality_index_sd | quality_index_ci95_low | quality_index_ci95_high | token_efficiency_mean | token_efficiency_sd | token_efficiency_ci95_low | token_efficiency_ci95_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| compressed | 450 | 4.3511 | 1.0972 | 4.2497 | 4.4525 | 4.2556 | 1.1401 | 4.1502 | 4.3609 | 4.2333 | 1.1699 | 4.1252 | 4.3414 | 4.3267 | 1.1098 | 4.2241 | 4.4292 | 4.2511 | 1.1313 | 4.1466 | 4.3556 | 4.8333 | 0.609 | 4.7771 | 4.8896 | 1.6467 | 1.0197 | 1.5525 | 1.7409 | 1.9489 | 1.2644 | 1.8321 | 2.0657 | 4.3014 | 1.003 | 4.2087 | 4.3941 | 14.9586 | 7.8167 | 14.2364 | 15.6809 |
| hybrid_min | 450 | 3.8533 | 1.355 | 3.7281 | 3.9785 | 3.6244 | 1.4404 | 3.4914 | 3.7575 | 3.84 | 1.3876 | 3.7118 | 3.9682 | 3.7422 | 1.4174 | 3.6113 | 3.8732 | 3.6311 | 1.4628 | 3.496 | 3.7663 | 4.8489 | 0.6834 | 4.7857 | 4.912 | 2.2711 | 1.3239 | 2.1488 | 2.3934 | 2.4667 | 1.4819 | 2.3297 | 2.6036 | 3.7685 | 1.2393 | 3.654 | 3.883 | 11.6505 | 6.3863 | 11.0604 | 12.2405 |
| hybrid_state | 450 | 4.1889 | 1.2724 | 4.0713 | 4.3065 | 4.1333 | 1.3096 | 4.0123 | 4.2543 | 4.3689 | 1.1548 | 4.2622 | 4.4756 | 4.32 | 1.1938 | 4.2097 | 4.4303 | 4.1822 | 1.237 | 4.0679 | 4.2965 | 4.8067 | 0.63 | 4.7485 | 4.8649 | 1.8667 | 1.2234 | 1.7536 | 1.9797 | 2.0222 | 1.3627 | 1.8963 | 2.1481 | 4.18 | 1.1236 | 4.0762 | 4.2838 | 10.9386 | 5.6966 | 10.4122 | 11.4649 |
| natural | 450 | 4.1844 | 1.3511 | 4.0596 | 4.3093 | 4.02 | 1.4659 | 3.8846 | 4.1554 | 3.9911 | 1.5028 | 3.8523 | 4.13 | 4.0244 | 1.4779 | 3.8879 | 4.161 | 3.9356 | 1.5021 | 3.7968 | 4.0743 | 4.4089 | 1.0283 | 4.3139 | 4.5039 | 1.6956 | 1.2007 | 1.5846 | 1.8065 | 2.0333 | 1.5061 | 1.8942 | 2.1725 | 4.1612 | 1.243 | 4.0464 | 4.2761 | 15.4575 | 9.6453 | 14.5663 | 16.3486 |

### EXP06 by mode

| mode | n | quality_index_mean | quality_index_sd | semantic_fidelity_mean | clarity_mean | utility_mean | completeness_mean | state_preservation_mean | operational_continuity_mean | context_recoverability_mean | handoff_quality_mean | compactness_mean | protocol_transferability_mean | language_or_variant_stability_mean | ambiguity_mean | information_loss_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| compressed | 777 | 3.8547668547668548 | 1.3191091542236877 | 3.77992277992278 | 4.033676533676534 | 3.6713856713856714 | 3.539253539253539 | 3.7282282282282284 | 3.7614757614757615 | 3.5885885885885886 | 3.6799656799656804 | 4.704847704847705 | 3.7906477906477907 | 4.562419562419563 | 2.230802230802231 | 2.497640497640498 |
| hybrid_state | 786 | 3.6606641873817445 | 1.2725241063795787 | 3.6208651399491094 | 3.4355385920271417 | 3.4724342663273964 | 3.3969465648854964 | 3.8053435114503817 | 3.698897370653096 | 3.5127226463104324 | 3.4978795589482616 | 4.63782866836302 | 3.687871077184054 | 4.142493638676845 | 2.6776929601357082 | 2.6424936386768447 |

### EXP06 paired effect overall

| n_pairs | mean_delta | sd_delta | ci95_low | ci95_high | cohen_dz |
| --- | --- | --- | --- | --- | --- |
| 774 | -0.20764592857616115 | 0.43935788983878554 | -0.23859901930704416 | -0.17669283784527814 | -0.4726122675351365 |

### EXP06 judge agreement

| judge_a | judge_b | n_common | pearson_quality_index | mean_abs_delta | rmse |
| --- | --- | --- | --- | --- | --- |
| azure_gpt_5_4_high | gemini_3_5_flash | 1561 | 0.9011949669417862 | 0.5704922879810772 | 0.741599531122494 |
| azure_gpt_5_4_high | grok_4_20_reasoning | 1561 | 0.9132985618681273 | 0.39452027792834965 | 0.5437819251072934 |
| gemini_3_5_flash | grok_4_20_reasoning | 1563 | 0.8860520026502926 | 0.5118854274324524 | 0.7286063973319196 |

### EXP07 by mode

| mode | n | variable_recovery_rate_mean | variable_recovery_rate_sd | subtask_completion_rate_mean | subtask_completion_rate_sd | plan_continuity_rate_mean | plan_continuity_rate_sd | constraint_retention_rate_mean | constraint_retention_rate_sd | handoff_success_mean | handoff_success_sd | state_error_count_mean | state_error_count_sd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| compressed | 90 | 0.856111111111111 | 0.3155900286246238 | 0.4666666666666667 | 0.48168710996881825 | 0.5888888888888889 | 0.448642006991046 | 0.7388888888888889 | 0.4320566037730706 | 0.35555555555555557 | 0.4813630252184319 | 10.588888888888889 | 29.654146665886337 |
| hybrid_state | 90 | 0.75 | 0.41563542797596553 | 0.3638888888888889 | 0.481630410879696 | 0.44166666666666665 | 0.4605962184001236 | 0.7444444444444445 | 0.43216494747112655 | 0.34444444444444444 | 0.4778489044986781 | 10.811111111111112 | 29.60371007892345 |
| natural | 90 | 0.7388888888888889 | 0.39282738995915545 | 0.47277777777777774 | 0.4896204165571662 | 0.49722222222222223 | 0.4643081787927956 | 0.6833333333333333 | 0.45252102812894385 | 0.36666666666666664 | 0.48459411952081843 | 16.977777777777778 | 36.8982743050625 |

### EXP07 paired deltas

| framework | model_key | n | delta_variable_recovery_rate_mean | delta_variable_recovery_rate_sd | delta_subtask_completion_rate_mean | delta_subtask_completion_rate_sd | delta_plan_continuity_rate_mean | delta_plan_continuity_rate_sd | delta_constraint_retention_rate_mean | delta_constraint_retention_rate_sd | delta_handoff_success_mean | delta_handoff_success_sd | delta_state_error_count_mean | delta_state_error_count_sd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| langgraph | azure_gpt_5_4_high | 30 | -0.29333333333333333 | 0.604114246635937 | -0.125 | 0.3131458842577788 | -0.3416666666666667 | 0.42285632461199846 | -0.16666666666666666 | 0.6989318615762461 | -0.03333333333333333 | 0.18257418583505536 | 0.8 | 56.92245178522601 |
| langgraph | azure_gpt_chat_latest | 30 | -0.025 | 0.24870353490825592 | -0.18333333333333332 | 0.45454284220774926 | -0.1 | 0.4183300132670378 | 0.18333333333333332 | 0.5330998051949096 | 0.0 | 0.2626128657194451 | -0.13333333333333333 | 1.3829836145670416 |
| openfang | azure_gpt_chat_latest | 30 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## G. Failure Accounting

Failures are treated as operational evidence, not silently removed. Public release excludes raw logs that may contain secrets or local paths.

### EXP06 policy failures

| phase | task_id | language | mode | model_key | n |
| --- | --- | --- | --- | --- | --- |
| exp06_a_hybrid_state_causal_handoff | A005 | ES | compressed | azure_gpt_5_5_instant | 3 |
| exp06_a_hybrid_state_causal_handoff | A005 | ES | hybrid_state | azure_gpt_5_5_instant | 3 |
| exp06_a_hybrid_state_causal_handoff | A005 | ZH | hybrid_state | azure_gpt_5_5_instant | 3 |
| exp06_a_hybrid_state_causal_handoff | A008 | EN | compressed | azure_gpt_5_5_instant | 3 |
| exp06_a_hybrid_state_causal_handoff | A008 | ZH | compressed | azure_gpt_5_5_instant | 3 |
| exp06_a_hybrid_state_causal_handoff | A011 | ZH | compressed | azure_gpt_5_5_instant | 3 |
| exp06_a_hybrid_state_causal_handoff | A012 | ZH | compressed | azure_gpt_5_5_instant | 3 |

### EXP07 operational errors

```jsonl
{"_source_index": 0, "cell_id": "EXP07::openfang::natural::H001::r1::azure_gpt_chat_latest", "dry_run": false, "error": "Error code: 400 - {'error': {'message': \"Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.\", 'type': 'invalid_request_error', 'param': 'max_tokens', 'code': 'unsupported_parameter'}}", "framework": "openfang", "mode": "natural", "model": "gpt-chat-latest", "model_key": "azure_gpt_chat_latest", "phase": "full", "provider": "azure_openai", "rep": 1, "status": "error", "task_id": "H001", "timestamp_unix": 1779838899.6079657}
{"_source_index": 1, "cell_id": "EXP07::openfang::natural::H001::r1::azure_gpt_chat_latest", "dry_run": false, "error": "[Errno 22] Invalid argument: 'C:\\\\Hijosdelsol\\\\ia\\\\Investigacion_y_Produccion\\\\Investigaciones\\\\Protolenguaje_AgentesIA\\\\05_Experimentos\\\\EXP07_REAL_AGENT_HANDOFF_OBJECTIVE_METRICS\\\\generated_openfang_workflows\\\\EXP07::openfang::natural::H001::r1::azure_gpt_chat_latest.workflow.json'", "framework": "openfang", "mode": "natural", "model": "gpt-chat-latest", "model_key": "azure_gpt_chat_latest", "phase": "full", "provider": "azure_openai", "rep": 1, "status": "error", "task_id": "H001", "timestamp_unix": 1779838947.421067}
{"_source_index": 3, "cell_id": "EXP07::langgraph::natural::H001::r1::azure_gpt_chat_latest", "dry_run": false, "error": "Error code: 400 - {'error': {'message': \"Unsupported value: 'reasoning_effort' does not support 'minimal' with this model. Supported values are: 'medium'.\", 'type': 'invalid_request_error', 'param': 'reasoning_effort', 'code': 'unsupported_value'}}", "framework": "langgraph", "mode": "natural", "model": "gpt-chat-latest", "model_key": "azure_gpt_chat_latest", "phase": "full", "provider": "azure_openai", "rep": 1, "status": "error", "task_id": "H001", "timestamp_unix": 1779838998.1454597}
{"_source_index": 4, "cell_id": "EXP07::langgraph::natural::H001::r1::azure_gpt_chat_latest", "dry_run": false, "error": "Error code: 400 - {'error': {'message': \"Unsupported value: 'temperature' does not support 0.1 with this model. Only the default (1) value is supported.\", 'type': 'invalid_request_error', 'param': 'temperature', 'code': 'unsupported_value'}}", "framework": "langgraph", "mode": "natural", "model": "gpt-chat-latest", "model_key": "azure_gpt_chat_latest", "phase": "full", "provider": "azure_openai", "rep": 1, "status": "error", "task_id": "H001", "timestamp_unix": 1779839030.654772}

```

## H. Cost Ledger and Cost Policy

Costs use call-level estimated ledgers during execution. Final cloud billing may lag. The paper reports cost as operational estimate unless explicitly labeled as billed cost.

### EXP07 cost summary

| provider | model_key | calls | input_tokens_est | output_tokens_est | cost_estimated_usd |
| --- | --- | --- | --- | --- | --- |
| azure_openai | azure_gpt_5_4_high | 90 | 0 | 0 | 0.0 |
| azure_openai | azure_gpt_chat_latest | 181 | 89533 | 71644 | 0.23140484 |

## I. Data Security and Public Release

Public release uses a redaction pipeline. It removes API-key-like strings, bearer tokens, Azure-style key fragments, and local Windows paths from JSONL before publication.

### Redacted dataset manifest

```json
{
  "name": "PUBLIC_DATASET_REDACTED",
  "policy": "Redacted JSONL plus aggregate CSV tables. Raw internal JSONL is not included.",
  "jsonl": [
    {
      "source": "C:\\Hijosdelsol\\ia\\Investigacion_y_Produccion\\Investigaciones\\Protolenguaje_AgentesIA\\05_Experimentos\\EXP06_CAUSAL_PROTOCOL_TRANSFER\\delivery\\EXP05_EXP06_MAIN_PAPER_PACKAGE_20260526_FINAL\\analysis\\EXP06\\EXP06_ANALYSIS_20260526_151836\\exp06_clean_ok.jsonl",
      "status": "redacted",
      "target": "C:\\Hijosdelsol\\ia\\Investigacion_y_Produccion\\Investigaciones\\Protolenguaje_AgentesIA\\05_Experimentos\\EXP06_CAUSAL_PROTOCOL_TRANSFER\\delivery\\EXP05_EXP06_MAIN_PAPER_PACKAGE_20260526_FINAL\\PUBLIC_DATASET_REDACTED\\jsonl_redacted\\analysis__EXP06__EXP06_ANALYSIS_20260526_151836__exp06_clean_ok.jsonl",
      "rows": 6252,
      "rows_changed": 12
    },
    {
      "source": "C:\\Hijosdelsol\\ia\\Investigacion_y_Produccion\\Investigaciones\\Protolenguaje_AgentesIA\\05_Experimentos\\EXP06_CAUSAL_PROTOCOL_TRANSFER\\delivery\\EXP05_EXP06_MAIN_PAPER_PACKAGE_20260526_FINAL\\analysis\\EXP06\\EXP06_ANALYSIS_20260526_151836\\exp06_clean_terminal.jsonl",
      "status": "redacted",
      "target": "C:\\Hijosdelsol\\ia\\Investigacion_y_Produccion\\Investigaciones\\Protolenguaje_AgentesIA\\05_Experimentos\\EXP06_CAUSAL_PROTOCOL_TRANSFER\\delivery\\EXP05_EXP06_MAIN_PAPER_PACKAGE_20260526_FINAL\\PUBLIC_DATASET_REDACTED\\jsonl_redacted\\analysis__EXP06__EXP06_ANALYSIS_20260526_151836__exp06_clean_terminal.jsonl",
      "rows": 6273,
      "rows_changed": 12
    },
    {
      "source": "C:\\Hijosdelsol\\ia\\Investigacion_y_Produccion\\Investigaciones\\Protolenguaje_AgentesIA\\05_Experimentos\\EXP06_CAUSAL_PROTOCOL_TRANSFER\\delivery\\EXP05_EXP06_MAIN_PAPER_PACKAGE_20260526_FINAL\\data_freeze\\EXP07\\exp07_clean_dedup.jsonl",
      "status": "redacted",
      "target": "C:\\Hijosdelsol\\ia\\Investigacion_y_Produccion\\Investigaciones\\Protolenguaje_AgentesIA\\05_Experimentos\\EXP06_CAUSAL_PROTOCOL_TRANSFER\\delivery\\EXP05_EXP06_MAIN_PAPER_PACKAGE_20260526_FINAL\\PUBLIC_DATASET_REDACTED\\jsonl_redacted\\data_freeze__EXP07__exp07_clean_dedup.jsonl",
      "rows": 270,
      "rows_changed": 90
    },
    {
      "source": "C:\\Hijosdelsol\\ia\\Investigacion_y_Produccion\\Investigaciones\\Protolenguaje_AgentesIA\\05_Experimentos\\EXP06_CAUSAL_PROTOCOL_TRANSFER\\delivery\\EXP05_EXP06_MAIN_PAPER_PACKAGE_20260526_FINAL\\data_freeze\\EXP07\\exp07_operational_errors.jsonl",
      "status": "redacted",
      "target": "C:\\Hijosdelsol\\ia\\Investigacion_y_Produccion\\Investigaciones\\Protolenguaje_AgentesIA\\05_Experimentos\\EXP06_CAUSAL_PROTOCOL_TRANSFER\\delivery\\EXP05_EXP06_MAIN_PAPER_PACKAGE_20260526_FINAL\\PUBLIC_DATASET_REDACTED\\jsonl_redacted\\data_freeze__EXP07__exp07_operational_errors.jsonl",
      "rows": 4,
      "rows_changed": 0
    }
  ],
  "csv_files": [
    "analysis_csv/analysis__EXP05__miniexp_b_judge_drift.csv",
    "analysis_csv/analysis__EXP05__miniexp_c_success_by_budget.csv",
    "analysis_csv/analysis__EXP05__miniexp_e_by_model.csv",
    "analysis_csv/analysis__EXP05__miniexp_e_by_turn.csv",
    "analysis_csv/analysis__EXP05__mode_effects_vs_compressed.csv",
    "analysis_csv/analysis__EXP05__principal_by_generator.csv",
    "analysis_csv/analysis__EXP05__principal_by_language.csv",
    "analysis_csv/analysis__EXP05__principal_by_mode.csv",
    "analysis_csv/analysis__EXP05__principal_paired_mode_deltas.csv",
    "analysis_csv/analysis__EXP05__stats_by_generator.csv",
    "analysis_csv/analysis__EXP05__stats_by_judge.csv",
    "analysis_csv/analysis__EXP05__stats_by_language.csv",
    "analysis_csv/analysis__EXP05__stats_by_mode.csv",
    "analysis_csv/analysis__EXP05__stats_by_phase.csv",
    "analysis_csv/analysis__EXP05__stats_by_phase_mode.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__exp06_evaluation_scores_by_judge.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__exp06_generation_mean_scores.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__judge_agreement.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_effect_by_generator.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_effect_by_language.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_effect_by_phase.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_effect_by_phase_language.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_effect_overall.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_mode_differences.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__policy_failure_summary.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_generator.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_generator_mode.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_judge.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_language.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_language_mode.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_mode.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_phase.csv",
    "analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_phase_mode.csv",
    "analysis_csv/analysis__EXP07__exp07_cost_summary.csv",
    "analysis_csv/analysis__EXP07__exp07_cost_summary_char4_repaired_estimate.csv",
    "analysis_csv/analysis__EXP07__exp07_framework_model_mode_summary.csv",
    "analysis_csv/analysis__EXP07__exp07_framework_mode_summary.csv",
    "analysis_csv/analysis__EXP07__exp07_framework_summary.csv",
    "analysis_csv/analysis__EXP07__exp07_model_mode_summary.csv",
    "analysis_csv/analysis__EXP07__exp07_model_summary.csv",
    "analysis_csv/analysis__EXP07__exp07_mode_summary.csv",
    "analysis_csv/analysis__EXP07__exp07_paired_deltas_hybrid_state_minus_compressed.csv",
    "analysis_csv/analysis__EXP07__exp07_paired_delta_summary.csv"
  ],
  "license_recommendation": "CC BY 4.0 or CC BY-NC 4.0"
}
```

### Public-safe package policy

- arXiv package: TeX source and figures only.

- public repo: paper, appendix, scripts, task banks, aggregate CSVs.

- redacted dataset: JSONL after sanitizer, manifest, checksums, final sweep.

- raw JSONL: retained internally only unless manually reviewed.

## J. Reproducibility Inventory

- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__miniexp_b_judge_drift.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__miniexp_c_success_by_budget.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__miniexp_e_by_model.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__miniexp_e_by_turn.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__mode_effects_vs_compressed.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__principal_by_generator.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__principal_by_language.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__principal_by_mode.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__principal_paired_mode_deltas.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__stats_by_generator.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__stats_by_judge.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__stats_by_language.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__stats_by_mode.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__stats_by_phase.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP05__stats_by_phase_mode.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__exp06_evaluation_scores_by_judge.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__exp06_generation_mean_scores.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__judge_agreement.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_effect_by_generator.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_effect_by_language.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_effect_by_phase.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_effect_by_phase_language.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_effect_overall.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__paired_mode_differences.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__policy_failure_summary.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_generator.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_generator_mode.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_judge.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_language.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_language_mode.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_mode.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_phase.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP06__EXP06_ANALYSIS_20260526_151836__summary_by_phase_mode.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP07__exp07_cost_summary.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP07__exp07_cost_summary_char4_repaired_estimate.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP07__exp07_framework_mode_summary.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP07__exp07_framework_model_mode_summary.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP07__exp07_framework_summary.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP07__exp07_mode_summary.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP07__exp07_model_mode_summary.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP07__exp07_model_summary.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP07__exp07_paired_delta_summary.csv`
- `PUBLIC_RELEASE_SAFE/analysis_csv/analysis__EXP07__exp07_paired_deltas_hybrid_state_minus_compressed.csv`
- `PUBLIC_RELEASE_SAFE/ARXIV_METADATA.md`
- `PUBLIC_RELEASE_SAFE/DATASET_RELEASE_PLAN.md`
- `PUBLIC_RELEASE_SAFE/paper/main.tex`
- `PUBLIC_RELEASE_SAFE/paper/PAPER_PRINCIPAL_EXP05_EXP06_EXP07.pdf`
- `PUBLIC_RELEASE_SAFE/prompts/data_freeze__EXP05__prompts_exp05_modes.json`
- `PUBLIC_RELEASE_SAFE/prompts/data_freeze__EXP06__EXP06_FREEZE_20260526_151836__prompts_exp06_modes.json`
- `PUBLIC_RELEASE_SAFE/prompts/data_freeze__EXP07__prompts_exp07_modes.json`
- `PUBLIC_RELEASE_SAFE/PUBLIC_DATASET_PIPELINE.md`
- `PUBLIC_RELEASE_SAFE/README.md`
- `PUBLIC_RELEASE_SAFE/README_REPRODUCIBILITY.md`
- `PUBLIC_RELEASE_SAFE/REVIEWER_RESPONSE_NOTES.md`
- `PUBLIC_RELEASE_SAFE/scripts/build_public_redacted_dataset.py`
- `PUBLIC_RELEASE_SAFE/scripts/redact_jsonl_for_public.py`
- `PUBLIC_RELEASE_SAFE/scripts/security_sweep_public_package.py`
- `PUBLIC_RELEASE_SAFE/security_sweep_public_package.py`
- `PUBLIC_RELEASE_SAFE/SECURITY_SWEEP_REPORT.md`
- `PUBLIC_RELEASE_SAFE/task_banks/data_freeze__EXP05__task_bank_exp05.jsonl`
- `PUBLIC_RELEASE_SAFE/task_banks/data_freeze__EXP05__task_bank_miniexp_a_grok_reasoning.jsonl`
- `PUBLIC_RELEASE_SAFE/task_banks/data_freeze__EXP06__EXP06_FREEZE_20260526_151836__task_bank_exp06_a.jsonl`
- `PUBLIC_RELEASE_SAFE/task_banks/data_freeze__EXP06__EXP06_FREEZE_20260526_151836__task_bank_exp06_b.jsonl`
- `PUBLIC_RELEASE_SAFE/task_banks/data_freeze__EXP07__task_bank_exp07.jsonl`
- `PUBLIC_RELEASE_SAFE/task_banks/PUBLIC_RELEASE_SAFE__prompts__data_freeze__EXP05__prompts_exp05_modes.json`
- `PUBLIC_RELEASE_SAFE/task_banks/PUBLIC_RELEASE_SAFE__prompts__data_freeze__EXP06__EXP06_FREEZE_20260526_151836__prompts_exp06_modes.json`
- `PUBLIC_RELEASE_SAFE/task_banks/PUBLIC_RELEASE_SAFE__prompts__data_freeze__EXP07__prompts_exp07_modes.json`
- `PUBLIC_RELEASE_SAFE/task_banks/PUBLIC_RELEASE_SAFE__task_banks__data_freeze__EXP05__task_bank_exp05.jsonl`
- `PUBLIC_RELEASE_SAFE/task_banks/PUBLIC_RELEASE_SAFE__task_banks__data_freeze__EXP05__task_bank_miniexp_a_grok_reasoning.jsonl`
- `PUBLIC_RELEASE_SAFE/task_banks/PUBLIC_RELEASE_SAFE__task_banks__data_freeze__EXP06__EXP06_FREEZE_20260526_151836__task_bank_exp06_a.jsonl`
- `PUBLIC_RELEASE_SAFE/task_banks/PUBLIC_RELEASE_SAFE__task_banks__data_freeze__EXP06__EXP06_FREEZE_20260526_151836__task_bank_exp06_b.jsonl`
- `PUBLIC_RELEASE_SAFE/task_banks/PUBLIC_RELEASE_SAFE__task_banks__data_freeze__EXP07__task_bank_exp07.jsonl`
- `PUBLIC_RELEASE_SAFE/task_banks/PUBLIC_RELEASE_SAFE__task_banks__PUBLIC_RELEASE_SAFE__prompts__data_freeze__EXP05__prompts_exp05_modes.json`
- `PUBLIC_RELEASE_SAFE/task_banks/PUBLIC_RELEASE_SAFE__task_banks__PUBLIC_RELEASE_SAFE__prompts__data_freeze__EXP06__EXP06_FREEZE_20260526_151836__prompts_exp06_modes.json`
- `PUBLIC_RELEASE_SAFE/task_banks/PUBLIC_RELEASE_SAFE__task_banks__PUBLIC_RELEASE_SAFE__prompts__data_freeze__EXP07__prompts_exp07_modes.json`

## K. Figures Generated Automatically

- `paper/figures/extra_exp05_modes_vs_metrics.svg`

- `paper/figures/extra_paired_deltas.svg`

- `paper/figures/extra_framework_model_interaction.svg`

- `paper/figures/extra_cost_vs_quality.svg`

Regenerate with: `python scripts/generate_extra_figures.py --root . --out paper/figures`.
