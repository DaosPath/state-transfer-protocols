from __future__ import annotations

import csv
import html
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPRO = ROOT / "reproducibility_repo"
OUT = REPRO / "appendix_figures"
INTERNAL_EXPS = ROOT.parent.parent / "05_Experimentos"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def short_source(name: str) -> str:
    base = Path(name).stem
    return (
        base.replace("experimento_", "EXP")
        .replace("_runs", "")
        .replace("exp", "EXP")
        .replace("_batch_decode_results", "_batch")
    )


def write_svg(filename: str, body: str, width: int, height: int) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#ffffff"/>
<style>
text {{ font-family: Arial, Helvetica, sans-serif; fill: #222; }}
.title {{ font-size: 20px; font-weight: 700; }}
.axis {{ font-size: 12px; fill: #555; }}
.label {{ font-size: 12px; }}
.small {{ font-size: 11px; fill: #555; }}
.grid {{ stroke: #ddd; stroke-width: 1; }}
</style>
{body}
</svg>
"""
    (OUT / filename).write_text(svg, encoding="utf-8")


def horizontal_bar(labels, values, title, filename, color="#4c78a8", xlabel="cells"):
    width = 980
    row_h = 32
    margin_l, margin_r, margin_t, margin_b = 270, 70, 58, 50
    height = margin_t + margin_b + row_h * len(labels)
    max_v = max(values) if values else 1
    plot_w = width - margin_l - margin_r
    body = [f'<text class="title" x="28" y="34">{esc(title)}</text>']
    for i in range(6):
        x = margin_l + plot_w * i / 5
        tick = round(max_v * i / 5)
        body.append(f'<line class="grid" x1="{x:.1f}" y1="{margin_t-8}" x2="{x:.1f}" y2="{height-margin_b+6}"/>')
        body.append(f'<text class="axis" x="{x:.1f}" y="{height-18}" text-anchor="middle">{tick}</text>')
    for i, (label, value) in enumerate(zip(labels, values)):
        y = margin_t + i * row_h
        bar_w = plot_w * value / max_v if max_v else 0
        body.append(f'<text class="label" x="{margin_l-10}" y="{y+19}" text-anchor="end">{esc(label)}</text>')
        body.append(f'<rect x="{margin_l}" y="{y+5}" width="{bar_w:.1f}" height="20" rx="2" fill="{color}"/>')
        body.append(f'<text class="small" x="{margin_l + bar_w + 6:.1f}" y="{y+20}">{value}</text>')
    body.append(f'<text class="axis" x="{margin_l + plot_w/2:.1f}" y="{height-4}" text-anchor="middle">{esc(xlabel)}</text>')
    write_svg(filename, "\n".join(body), width, height)


def stacked_vertical(labels, series, title, filename, colors, ylabel="latest cells"):
    width, height = 980, 540
    margin_l, margin_r, margin_t, margin_b = 72, 28, 72, 130
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b
    totals = [sum(vals) for vals in zip(*series.values())] if series else [1]
    max_v = max(totals) or 1
    bar_gap = 18
    bar_w = max(14, (plot_w - bar_gap * (len(labels) - 1)) / max(len(labels), 1))
    body = [f'<text class="title" x="28" y="36">{esc(title)}</text>']
    for i in range(6):
        y = margin_t + plot_h - plot_h * i / 5
        tick = round(max_v * i / 5)
        body.append(f'<line class="grid" x1="{margin_l}" y1="{y:.1f}" x2="{width-margin_r}" y2="{y:.1f}"/>')
        body.append(f'<text class="axis" x="{margin_l-8}" y="{y+4:.1f}" text-anchor="end">{tick}</text>')
    for idx, label in enumerate(labels):
        x = margin_l + idx * (bar_w + bar_gap)
        y_bottom = margin_t + plot_h
        acc = 0
        for s_idx, (name, vals) in enumerate(series.items()):
            v = vals[idx]
            h = plot_h * v / max_v
            y = y_bottom - acc - h
            body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{colors[s_idx % len(colors)]}"/>')
            acc += h
        body.append(f'<text class="axis" transform="translate({x + bar_w/2:.1f},{height-72}) rotate(-35)" text-anchor="end">{esc(label)}</text>')
    lx = margin_l
    for s_idx, name in enumerate(series):
        body.append(f'<rect x="{lx}" y="{height-36}" width="12" height="12" fill="{colors[s_idx % len(colors)]}"/>')
        body.append(f'<text class="small" x="{lx+18}" y="{height-26}">{esc(name)}</text>')
        lx += 140
    body.append(f'<text class="axis" transform="translate(20,{margin_t + plot_h/2:.1f}) rotate(-90)" text-anchor="middle">{esc(ylabel)}</text>')
    write_svg(filename, "\n".join(body), width, height)


def vertical_rate(labels, rates, title, filename, color="#b07aa1"):
    width, height = 980, 500
    margin_l, margin_r, margin_t, margin_b = 70, 28, 68, 120
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b
    bar_gap = 18
    bar_w = max(16, (plot_w - bar_gap * (len(labels) - 1)) / max(len(labels), 1))
    body = [f'<text class="title" x="28" y="36">{esc(title)}</text>']
    for i in range(6):
        y = margin_t + plot_h - plot_h * i / 5
        tick = i / 5
        body.append(f'<line class="grid" x1="{margin_l}" y1="{y:.1f}" x2="{width-margin_r}" y2="{y:.1f}"/>')
        body.append(f'<text class="axis" x="{margin_l-8}" y="{y+4:.1f}" text-anchor="end">{tick:.1f}</text>')
    for idx, (label, rate) in enumerate(zip(labels, rates)):
        x = margin_l + idx * (bar_w + bar_gap)
        h = plot_h * max(0, min(1, rate))
        y = margin_t + plot_h - h
        body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{color}"/>')
        body.append(f'<text class="small" x="{x + bar_w/2:.1f}" y="{y-5:.1f}" text-anchor="middle">{rate:.2f}</text>')
        body.append(f'<text class="axis" transform="translate({x + bar_w/2:.1f},{height-62}) rotate(-35)" text-anchor="end">{esc(label)}</text>')
    write_svg(filename, "\n".join(body), width, height)


def fig_exp01_exp04_counts():
    path = REPRO / "EXP01_EXP04_RECOVERY" / "analysis" / "EXP01_EXP04_summary_counts.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    labels = [short_source(r["source_file"]) for r in rows]
    vals = [int(r["clean_latest_ok"]) for r in rows]
    horizontal_bar(labels, vals, "EXP01-EXP04 recovered clean latest-ok cells", "fig_exp01_exp04_recovery_counts.svg", "#59a14f")


def fig_exp13_mode_model_success():
    path = REPRO / "EXP13_REAL_MULTI_AGENT_SCIENTIFIC_REPO_BENCHMARK" / "exp13_latest_cells_clean.jsonl"
    counts = Counter()
    totals = Counter()
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            key = (row.get("model_route", "unknown"), row.get("mode", "unknown"))
            totals[key] += 1
            if row.get("status") == "ok" and row.get("validation", {}).get("task_success") is True:
                counts[key] += 1
    keys = sorted(totals)
    labels = [f"{m} / {mode}" for m, mode in keys]
    success = [counts[k] for k in keys]
    fail = [totals[k] - counts[k] for k in keys]
    stacked_vertical(labels, {"success": success, "non-success": fail}, "EXP13 real multi-agent repo benchmark", "fig_exp13_success_by_model_mode.svg", ["#4c78a8", "#e15759"])


def fig_exp16_by_model_and_mode():
    path = REPRO / "EXP16_MODEL_SPECIFIC_PROTOCOL_ADAPTATION" / "exp16_latest_cells_summary.csv"
    by_model = defaultdict(lambda: Counter(total=0, success=0))
    by_mode = defaultdict(lambda: Counter(total=0, success=0))
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            model = row["model_route"]
            if model == "gemini_3_flash_preview":
                continue
            success = row["status"].startswith("ok")
            by_model[model]["total"] += 1
            by_mode[row["mode"]]["total"] += 1
            if success:
                by_model[model]["success"] += 1
                by_mode[row["mode"]]["success"] += 1

    labels = sorted(by_model)
    success = [by_model[k]["success"] for k in labels]
    fail = [by_model[k]["total"] - by_model[k]["success"] for k in labels]
    stacked_vertical(labels, {"success/repaired": success, "failure": fail}, "EXP16 outcome by model route", "fig_exp16_success_by_model.svg", ["#4c78a8", "#f28e2b"])

    labels = sorted(by_mode)
    success = [by_mode[k]["success"] for k in labels]
    fail = [by_mode[k]["total"] - by_mode[k]["success"] for k in labels]
    stacked_vertical(labels, {"success/repaired": success, "failure": fail}, "EXP16 outcome by prompt adaptation mode", "fig_exp16_success_by_mode.svg", ["#59a14f", "#e15759"])


def fig_exp16b_adaptation_search():
    path = REPRO / "EXP16B_GROK_REASONING_ADAPTATION_SEARCH" / "exp16b_latest_cells_summary.csv"
    by_mode = defaultdict(lambda: Counter(total=0, success=0))
    errors = Counter()
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            by_mode[row["mode"]]["total"] += 1
            if row["status"].startswith("ok"):
                by_mode[row["mode"]]["success"] += 1
            elif row.get("error_class"):
                errors[row["error_class"]] += 1
    labels = sorted(by_mode)
    rates = [by_mode[k]["success"] / by_mode[k]["total"] for k in labels]
    vertical_rate(labels, rates, "EXP16B Grok reasoning adaptation search", "fig_exp16b_success_rate_by_variant.svg")
    if errors:
        labels, vals = zip(*errors.most_common())
        horizontal_bar(list(labels), list(vals), "EXP16B terminal failure classes", "fig_exp16b_failure_classes.svg", "#e15759", "failure cells")


def fig_exp09_summary():
    path = INTERNAL_EXPS / "EXP09_REAL_TOOL_USE_AGENT_TASKS" / "analysis_exp09" / "exp09_summary.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    labels, success, fail = [], [], []
    for key, row in sorted(data.get("success_by_route_mode", {}).items()):
        label = key.strip("()").replace("'", "").replace(", ", " / ")
        labels.append(label)
        success.append(int(row.get("ok", 0)))
        fail.append(int(row.get("total", 0)) - int(row.get("ok", 0)))
    stacked_vertical(labels, {"success": success, "non-success": fail}, "EXP09 deterministic tool-use validation", "fig_exp09_success_by_route_mode.svg", ["#4c78a8", "#e15759"])


def fig_exp10_summary():
    path = INTERNAL_EXPS / "EXP10_PUBLIC_REPO_TOOL_AGENT" / "analysis_exp10" / "exp10_summary.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    metrics = data.get("metric_means_ok", {})
    wanted = [
        "task_success",
        "state_preserved",
        "plan_preserved",
        "constraint_preservation_score",
        "dependency_preservation_score",
        "recovery_score",
        "scope_drift_rate",
        "claim_drift_rate",
    ]
    labels = [m for m in wanted if m in metrics]
    vals = [float(metrics[m]) for m in labels]
    horizontal_bar(labels, vals, "EXP10 public repo tool-agent metric means", "fig_exp10_metric_means.svg", "#76b7b2", "mean value")


def latest_rows_jsonl(path: Path, key_fields):
    latest = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            key = tuple(row.get(k) for k in key_fields)
            latest[key] = row
    return list(latest.values())


def fig_exp11_latest():
    path = INTERNAL_EXPS / "EXP11_PAGE_TASK_ASSIGNMENT" / "exp11_runs.jsonl"
    if not path.exists():
        return
    rows = latest_rows_jsonl(path, ["task_id", "mode", "model_route", "rep"])
    by_model = defaultdict(lambda: Counter(total=0, success=0))
    for row in rows:
        model = row.get("model_route", "unknown")
        by_model[model]["total"] += 1
        if row.get("status") == "ok" and row.get("validation", {}).get("task_success") is True:
            by_model[model]["success"] += 1
    labels = sorted(by_model)
    success = [by_model[k]["success"] for k in labels]
    fail = [by_model[k]["total"] - by_model[k]["success"] for k in labels]
    stacked_vertical(labels, {"success": success, "non-success": fail}, "EXP11 page task assignment: latest-cell outcomes", "fig_exp11_success_by_model.svg", ["#4c78a8", "#e15759"])


def fig_exp12_latest():
    path = INTERNAL_EXPS / "EXP12_CONFLICT_AWARE_REPO_MAINTENANCE" / "exp12_runs.jsonl"
    if not path.exists():
        return
    rows = latest_rows_jsonl(path, ["pair_id", "mode", "model_route", "rep"])
    by_mode = defaultdict(lambda: Counter(total=0, success=0))
    drift = defaultdict(list)
    for row in rows:
        mode = row.get("mode", "unknown")
        validation = row.get("validation", {})
        by_mode[mode]["total"] += 1
        if row.get("status") == "ok" and validation.get("task_success") is True:
            by_mode[mode]["success"] += 1
        if "claim_drift_rate" in validation:
            drift[mode].append(float(validation["claim_drift_rate"]))
    labels = sorted(by_mode)
    success = [by_mode[k]["success"] for k in labels]
    fail = [by_mode[k]["total"] - by_mode[k]["success"] for k in labels]
    stacked_vertical(labels, {"success": success, "non-success": fail}, "EXP12 conflict-aware maintenance: latest-cell outcomes", "fig_exp12_success_by_mode.svg", ["#59a14f", "#e15759"])
    labels = sorted(drift)
    vals = [sum(drift[k]) / len(drift[k]) if drift[k] else 0 for k in labels]
    horizontal_bar(labels, vals, "EXP12 mean claim drift by mode", "fig_exp12_claim_drift_by_mode.svg", "#f28e2b", "mean claim drift")


def fig_exp14_latest():
    path = INTERNAL_EXPS / "EXP14_LONG_HORIZON_REPO_MAINTENANCE" / "exp14_latest_cells_clean.jsonl"
    if not path.exists():
        return
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    by_round = defaultdict(lambda: Counter(total=0, success=0))
    by_mode = defaultdict(lambda: Counter(total=0, success=0))
    for row in rows:
        ok = row.get("status") == "ok" and row.get("validation", {}).get("ok") is True
        round_id = f"round_{row.get('round', 'unknown')}"
        mode = row.get("mode", "unknown")
        by_round[round_id]["total"] += 1
        by_mode[mode]["total"] += 1
        if ok:
            by_round[round_id]["success"] += 1
            by_mode[mode]["success"] += 1
    labels = sorted(by_round, key=lambda s: int(s.split("_")[1]) if s.split("_")[1].isdigit() else 999)
    rates = [by_round[k]["success"] / by_round[k]["total"] for k in labels]
    vertical_rate(labels, rates, "EXP14 long-horizon maintenance: success rate by round", "fig_exp14_success_rate_by_round.svg", "#4c78a8")
    labels = sorted(by_mode)
    rates = [by_mode[k]["success"] / by_mode[k]["total"] for k in labels]
    vertical_rate(labels, rates, "EXP14 long-horizon maintenance: success rate by mode", "fig_exp14_success_rate_by_mode.svg", "#59a14f")


def fig_coverage_index():
    experiments = [
        ("EXP01-04", 1),
        ("EXP05", 1),
        ("EXP06", 1),
        ("EXP07", 1),
        ("EXP08", 1),
        ("EXP09", 1),
        ("EXP10", 1),
        ("EXP11", 1),
        ("EXP12", 1),
        ("EXP13", 1),
        ("EXP14", 1),
        ("EXP15", 1),
        ("EXP15B", 1),
        ("EXP16", 1),
        ("EXP16B", 1),
    ]
    labels = [e for e, _ in experiments]
    rates = [float(v) for _, v in experiments]
    vertical_rate(labels, rates, "Figure coverage across the experiment trail", "fig_experiment_figure_coverage.svg", "#76b7b2")


def main():
    fig_exp01_exp04_counts()
    fig_exp13_mode_model_success()
    fig_exp09_summary()
    fig_exp10_summary()
    fig_exp11_latest()
    fig_exp12_latest()
    fig_exp14_latest()
    fig_exp16_by_model_and_mode()
    fig_exp16b_adaptation_search()
    fig_coverage_index()
    print(f"Wrote appendix figures to {OUT}")


if __name__ == "__main__":
    main()
