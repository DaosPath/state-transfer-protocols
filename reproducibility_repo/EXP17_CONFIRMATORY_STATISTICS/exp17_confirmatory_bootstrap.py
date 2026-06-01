from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean


HERE = Path(__file__).resolve().parent
INVENTORY_CSV = HERE / "data_inventory_exp17.csv"
OUT_CSV = HERE / "exp17_bootstrap_candidate_results.csv"
OUT_MD = HERE / "EXP17_BOOTSTRAP_STATUS.md"

METRIC_CANDIDATES = [
    "metric_quality_index",
    "metric_semantic_fidelity",
    "metric_clarity",
    "metric_utility",
    "metric_completeness",
    "metric_state_preservation",
    "metric_operational_continuity",
    "metric_context_recoverability",
    "metric_handoff_quality",
    "metric_compactness",
    "metric_ambiguity",
    "metric_information_loss",
    "quality_index",
    "semantic_fidelity",
    "clarity",
    "utility",
    "completeness",
    "state_preservation",
    "operational_continuity",
    "context_recoverability",
    "handoff_quality",
    "compactness",
    "ambiguity",
    "information_loss",
    "constraint_preservation",
    "claim_drift_rate",
    "scope_drift_rate",
    "success_rate",
    "objective_success",
    "variable_recovery_rate",
    "subtask_completion_rate",
    "plan_continuity_rate",
    "constraint_retention_rate",
    "state_error_count",
    "json_valid",
    "handoff_success",
    "html_integrity_score",
    "dependency_preservation",
    "visual_quality_proxy",
    "visual_css_score",
    "visual_html_score",
    "visual_structure_score",
    "responsive_ok",
    "no_secret_leak",
    "no_local_paths",
    "regression_rate",
]


def load_inventory() -> list[dict[str, str]]:
    with INVENTORY_CSV.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def absolute_from_inventory(path_text: str) -> Path:
    root = Path(__file__).resolve().parents[2]
    return root / path_text


def read_table(path: Path) -> list[dict[str, object]]:
    suffix = path.suffix.lower()
    rows: list[dict[str, object]] = []
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
            rows.extend(csv.DictReader(handle))
    elif suffix == ".jsonl":
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if line.strip():
                    obj = json.loads(line)
                    if isinstance(obj, dict):
                        rows.append(obj)
    elif suffix == ".json":
        obj = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        if isinstance(obj, list):
            rows.extend(item for item in obj if isinstance(item, dict))
        elif isinstance(obj, dict):
            rows.append(obj)
    return [flatten_row(row) for row in rows]


def flatten_row(row: dict[str, object]) -> dict[str, object]:
    out = dict(row)
    for parent_key in ("evaluation", "validation", "pre_repair_validation", "metrics"):
        value = out.get(parent_key)
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except Exception:
                value = None
        if isinstance(value, dict):
            metrics = value.get("metrics") if isinstance(value.get("metrics"), dict) else value
            for key, metric_value in metrics.items():
                out.setdefault(key, metric_value)
    return out


def as_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def bootstrap_ci(values: list[float], seed_text: str, n: int = 2000) -> tuple[float, float, float]:
    if not values:
        return float("nan"), float("nan"), float("nan")
    seed = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest()[:12], 16)
    rng = random.Random(seed)
    samples = []
    for _ in range(n):
        samples.append(mean(rng.choice(values) for _ in values))
    samples.sort()
    lo = samples[int(0.025 * (n - 1))]
    hi = samples[int(0.975 * (n - 1))]
    return mean(values), lo, hi


def choose_group_cols(rows: list[dict[str, object]]) -> list[str]:
    preferred = ["task_id", "language", "generator", "model_key", "judge", "framework", "rep", "round"]
    available = set().union(*(row.keys() for row in rows[:200])) if rows else set()
    return [col for col in preferred if col in available]


def paired_deltas(rows: list[dict[str, object]], metric: str) -> list[float]:
    if not rows or "mode" not in rows[0]:
        return []
    group_cols = choose_group_cols(rows)
    if not group_cols:
        group_cols = ["__all__"]
        for row in rows:
            row["__all__"] = "all"

    grouped: dict[tuple[object, ...], dict[str, float]] = defaultdict(dict)
    for row in rows:
        mode = str(row.get("mode", ""))
        value = as_float(row.get(metric))
        if mode not in {"compressed", "hybrid_state"} or value is None:
            continue
        key = tuple(row.get(col, "") for col in group_cols)
        grouped[key][mode] = value
    return [pair["hybrid_state"] - pair["compressed"] for pair in grouped.values() if {"hybrid_state", "compressed"} <= pair.keys()]


def main() -> None:
    inventory = load_inventory()
    raw_candidates = [
        row for row in inventory
        if row.get("extension") in {".csv", ".jsonl", ".json"}
        and "clean_data" in row.get("role", "")
        and row.get("exp", "") in {f"EXP{i:02d}" for i in range(5, 17)}
    ]
    candidates = []
    seen_hashes: set[str] = set()
    for row in raw_candidates:
        path = absolute_from_inventory(row["path"])
        if not path.exists() or path.stat().st_size > 80_000_000:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in seen_hashes:
            continue
        seen_hashes.add(digest)
        candidates.append(row)

    results = []
    for item in candidates:
        path = absolute_from_inventory(item["path"])
        try:
            rows = read_table(path)
        except Exception as exc:
            results.append({
                "exp": item["exp"],
                "path": item["path"],
                "metric": "READ_ERROR",
                "pairs": 0,
                "mean_delta": "",
                "ci_low": "",
                "ci_high": "",
                "note": type(exc).__name__,
            })
            continue
        if not rows:
            continue
        keys = set().union(*(row.keys() for row in rows[:200]))
        for metric in METRIC_CANDIDATES:
            if metric not in keys:
                continue
            deltas = paired_deltas(rows, metric)
            if len(deltas) < 5:
                continue
            avg, lo, hi = bootstrap_ci(deltas, f"{item['path']}::{metric}")
            results.append({
                "exp": item["exp"],
                "path": item["path"],
                "metric": metric,
                "pairs": len(deltas),
                "mean_delta": f"{avg:.6f}",
                "ci_low": f"{lo:.6f}",
                "ci_high": f"{hi:.6f}",
                "note": "hybrid_state_minus_compressed",
            })

    fields = ["exp", "path", "metric", "pairs", "mean_delta", "ci_low", "ci_high", "note"]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    lines = [
        "# EXP17 Bootstrap Status",
        "",
        "This is the first confirmatory-pass bootstrap over already frozen clean datasets.",
        "",
        f"- Raw candidate clean datasets: `{len(raw_candidates)}`",
        f"- Unique candidate clean datasets scanned: `{len(candidates)}`",
        f"- Bootstrap result rows: `{len(results)}`",
        f"- Output CSV: `{OUT_CSV.name}`",
        "",
        "## Current Policy",
        "",
        "- Delta is `hybrid_state - compressed`.",
        "- Pairing uses available identifiers among task, language, generator/model, judge, framework, repetition and round.",
        "- Bootstrap uses deterministic seeded resampling per dataset/metric.",
        "- This script is intentionally conservative and skips files without clear paired cells.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"candidate_datasets": len(candidates), "bootstrap_rows": len(results), "output": str(OUT_CSV)}, indent=2))


if __name__ == "__main__":
    main()
