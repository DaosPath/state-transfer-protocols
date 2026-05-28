from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "appendix" / "TECHNICAL_APPENDIX_LONG_EXP05_EXP08.md"


def read(path: Path, max_chars: int | None = None) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    return text if max_chars is None else text[:max_chars]


def csv_table(path: Path, max_rows: int = 12) -> str:
    if not path.exists():
        return "_Missing._\n"
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        return "_Empty._\n"
    rows = rows[: max_rows + 1]
    widths = [max(len(str(row[i])) if i < len(row) else 0 for row in rows) for i in range(len(rows[0]))]
    lines = []
    header = rows[0]
    lines.append("| " + " | ".join(str(header[i]).strip() for i in range(len(header))) + " |")
    lines.append("| " + " | ".join("---" for _ in header) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join((str(row[i]).strip() if i < len(row) else "") for i in range(len(header))) + " |")
    return "\n".join(lines) + "\n"


def json_block(path: Path) -> str:
    obj = json.loads(path.read_text(encoding="utf-8"))
    return "```json\n" + json.dumps(obj, ensure_ascii=False, indent=2) + "\n```\n"


def file_inventory(base: Path, limit: int = 80) -> str:
    rows = []
    for p in sorted(base.rglob("*")):
        if p.is_file():
            rows.append(f"- `{p.relative_to(ROOT).as_posix()}`")
        if len(rows) >= limit:
            rows.append("- ...")
            break
    return "\n".join(rows) + "\n"


def main() -> int:
    exp06_analysis = ROOT / "analysis/EXP06/EXP06_ANALYSIS_20260526_151836"
    parts = [
        "# Technical Appendix: EXP05-EXP08\n",
        "This appendix records prompts, task banks, metrics, cleaning policy, failures, data security, and reproducibility artifacts for the symbolic compression protocol experiments.\n",
        "## A. Experimental Path\n",
        "- EXP05: broad multilingual multi-model discovery over natural, compressed, hybrid_min, and hybrid_state.\n",
        "- EXP06: controlled causal transfer test for compressed vs hybrid_state under language and tokenizer ablations.\n",
        "- EXP07: real-agent handoff evaluation with LangGraph/OpenFang-style execution and objective metrics.\n",
        "- EXP08: scale-up run in progress at appendix build time; same real-agent design with larger task/repetition matrix.\n",
        "## B. Exact Prompt Protocols\n",
        "### EXP05 modes\n",
        json_block(ROOT / "data_freeze/EXP05/prompts_exp05_modes.json"),
        "### EXP06 modes\n",
        json_block(ROOT / "data_freeze/EXP06/EXP06_FREEZE_20260526_151836/prompts_exp06_modes.json"),
        "### EXP07 modes\n",
        json_block(ROOT / "data_freeze/EXP07/prompts_exp07_modes.json"),
        "## C. Evaluator Prompting and Metrics\n",
        "### EXP05 evaluator prompt\n",
        json_block(ROOT / "data_freeze/EXP05/evaluator_prompt_exp05.json"),
        "### EXP06 evaluator prompt\n",
        json_block(ROOT / "data_freeze/EXP06/EXP06_FREEZE_20260526_151836/evaluator_prompt_exp06.json"),
        "### Core LLM-judge metrics\n",
        "- Positive: semantic_fidelity, clarity, utility, completeness, state_preservation, operational_continuity, context_recoverability, handoff_quality, compactness.\n",
        "- Negative: ambiguity, information_loss.\n",
        "- EXP05 additions: inter_model_consistency, judge_agreement, language_stability, protocol_transferability.\n",
        "### Objective handoff metrics\n",
        "- variable_recovery_rate: required variable values recovered by the receiving agent.\n",
        "- subtask_completion_rate: target subtasks completed after handoff.\n",
        "- plan_continuity_rate: plan steps preserved and continued.\n",
        "- constraint_retention_rate: constraints preserved in execution.\n",
        "- handoff_success: strict end-to-end success flag.\n",
        "- state_error_count: count of missing, invented, or corrupted state elements.\n",
        "## D. Task Banks\n",
        "### EXP05 task bank sample\n",
        "```jsonl\n" + read(ROOT / "data_freeze/EXP05/task_bank_exp05.jsonl", 5000) + "\n```\n",
        "### EXP06 task bank inventory\n",
        file_inventory(ROOT / "data_freeze/EXP06/EXP06_FREEZE_20260526_151836", 40),
        "### EXP07 task bank sample\n",
        "```jsonl\n" + read(ROOT / "data_freeze/EXP07/task_bank_exp07.jsonl", 5000) + "\n```\n",
        "## E. Cleaning and Deduplication\n",
        "Policy: keep the last successful row per cell_id for analysis; keep policy_failure and operational_error as terminal evidence; ignore historical errors when later OK exists, but do not delete them from frozen raw logs.\n",
        "### EXP06 cleaning report\n",
        json_block(exp06_analysis / "cleaning_report.json"),
        "## F. Main Result Tables\n",
        "### EXP05 by mode\n",
        csv_table(ROOT / "analysis/EXP05/principal_by_mode.csv", 8),
        "### EXP06 by mode\n",
        csv_table(exp06_analysis / "summary_by_mode.csv", 8),
        "### EXP06 paired effect overall\n",
        csv_table(exp06_analysis / "paired_effect_overall.csv", 4),
        "### EXP06 judge agreement\n",
        csv_table(exp06_analysis / "judge_agreement.csv", 12),
        "### EXP07 by mode\n",
        csv_table(ROOT / "analysis/EXP07/exp07_mode_summary.csv", 8),
        "### EXP07 paired deltas\n",
        csv_table(ROOT / "analysis/EXP07/exp07_paired_delta_summary.csv", 12),
        "## G. Failure Accounting\n",
        "Failures are treated as operational evidence, not silently removed. Public release excludes raw logs that may contain secrets or local paths.\n",
        "### EXP06 policy failures\n",
        csv_table(exp06_analysis / "policy_failure_summary.csv", 12),
        "### EXP07 operational errors\n",
        "```jsonl\n" + read(ROOT / "data_freeze/EXP07/exp07_operational_errors.jsonl", 5000) + "\n```\n",
        "## H. Cost Ledger and Cost Policy\n",
        "Costs use call-level estimated ledgers during execution. Final cloud billing may lag. The paper reports cost as operational estimate unless explicitly labeled as billed cost.\n",
        "### EXP07 cost summary\n",
        csv_table(ROOT / "analysis/EXP07/exp07_cost_summary.csv", 10),
        "## I. Data Security and Public Release\n",
        "Public release uses a redaction pipeline. It removes API-key-like strings, bearer tokens, Azure-style key fragments, and local Windows paths from JSONL before publication.\n",
        "### Redacted dataset manifest\n",
        json_block(ROOT / "PUBLIC_DATASET_REDACTED/PUBLIC_DATASET_MANIFEST.json"),
        "### Public-safe package policy\n",
        "- arXiv package: TeX source and figures only.\n",
        "- public repo: paper, appendix, scripts, task banks, aggregate CSVs.\n",
        "- redacted dataset: JSONL after sanitizer, manifest, checksums, final sweep.\n",
        "- raw JSONL: retained internally only unless manually reviewed.\n",
        "## J. Reproducibility Inventory\n",
        file_inventory(ROOT / "PUBLIC_RELEASE_SAFE", 120),
        "## K. Figures Generated Automatically\n",
        "- `paper/figures/extra_exp05_modes_vs_metrics.svg`\n",
        "- `paper/figures/extra_paired_deltas.svg`\n",
        "- `paper/figures/extra_framework_model_interaction.svg`\n",
        "- `paper/figures/extra_cost_vs_quality.svg`\n",
        "Regenerate with: `python scripts/generate_extra_figures.py --root . --out paper/figures`.\n",
    ]
    OUT.write_text("\n".join(parts), encoding="utf-8", newline="\n")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
