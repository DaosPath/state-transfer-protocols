from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REPRO = ROOT / "reproducibility_repo"
INTERNAL_EXPS = ROOT.parent.parent / "05_Experimentos"
OUT = ROOT / "technical_report" / "figures_appendix"


def font(size=18, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_TITLE = font(24, True)
F_LABEL = font(16)
F_SMALL = font(13)
F_AXIS = font(14)


def save(img: Image.Image, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / name)


def short_source(name: str) -> str:
    base = Path(name).stem
    return (
        base.replace("experimento_", "EXP")
        .replace("_runs", "")
        .replace("exp", "EXP")
        .replace("_batch_decode_results", "_batch")
    )


def draw_horizontal(labels, values, title, filename, color=(76, 120, 168), xlabel="cells"):
    w = 1400
    row_h = 44
    ml, mr, mt, mb = 430, 100, 88, 70
    h = mt + mb + row_h * max(1, len(labels))
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    d.text((34, 28), title, font=F_TITLE, fill=(30, 30, 30))
    max_v = max(values) if values else 1
    plot_w = w - ml - mr
    for i in range(6):
        x = ml + int(plot_w * i / 5)
        tick = round(max_v * i / 5, 2 if max_v <= 1 else 0)
        d.line((x, mt - 12, x, h - mb + 8), fill=(225, 225, 225), width=1)
        d.text((x - 18, h - 42), str(tick), font=F_AXIS, fill=(80, 80, 80))
    for i, (label, value) in enumerate(zip(labels, values)):
        y = mt + i * row_h
        bar_w = int(plot_w * value / max_v) if max_v else 0
        d.text((20, y + 10), label[:50], font=F_LABEL, fill=(30, 30, 30))
        d.rounded_rectangle((ml, y + 8, ml + bar_w, y + 30), radius=4, fill=color)
        d.text((ml + bar_w + 8, y + 9), f"{value:.2f}" if isinstance(value, float) and value <= 1 else str(value), font=F_SMALL, fill=(80, 80, 80))
    d.text((ml + plot_w // 2 - 40, h - 24), xlabel, font=F_AXIS, fill=(80, 80, 80))
    save(img, filename)


def draw_stacked(labels, success, fail, title, filename, colors=((76, 120, 168), (225, 87, 89))):
    w, h = 1500, 780
    ml, mr, mt, mb = 90, 60, 92, 210
    plot_w = w - ml - mr
    plot_h = h - mt - mb
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    d.text((34, 28), title, font=F_TITLE, fill=(30, 30, 30))
    totals = [a + b for a, b in zip(success, fail)]
    max_v = max(totals) if totals else 1
    for i in range(6):
        y = mt + plot_h - int(plot_h * i / 5)
        tick = round(max_v * i / 5)
        d.line((ml, y, w - mr, y), fill=(225, 225, 225), width=1)
        d.text((20, y - 8), str(tick), font=F_AXIS, fill=(80, 80, 80))
    gap = 18
    bw = max(18, int((plot_w - gap * (len(labels) - 1)) / max(1, len(labels))))
    for idx, label in enumerate(labels):
        x = ml + idx * (bw + gap)
        s_h = int(plot_h * success[idx] / max_v) if max_v else 0
        f_h = int(plot_h * fail[idx] / max_v) if max_v else 0
        y0 = mt + plot_h
        d.rectangle((x, y0 - s_h, x + bw, y0), fill=colors[0])
        d.rectangle((x, y0 - s_h - f_h, x + bw, y0 - s_h), fill=colors[1])
        d.text((x - 50, h - 180 + (idx % 4) * 28), label[:28], font=F_SMALL, fill=(40, 40, 40))
    d.rectangle((ml, h - 45, ml + 16, h - 29), fill=colors[0])
    d.text((ml + 24, h - 48), "success", font=F_LABEL, fill=(50, 50, 50))
    d.rectangle((ml + 140, h - 45, ml + 156, h - 29), fill=colors[1])
    d.text((ml + 164, h - 48), "non-success", font=F_LABEL, fill=(50, 50, 50))
    save(img, filename)


def draw_rates(labels, rates, title, filename, color=(176, 122, 161)):
    w, h = 1500, 720
    ml, mr, mt, mb = 90, 60, 92, 190
    plot_w = w - ml - mr
    plot_h = h - mt - mb
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    d.text((34, 28), title, font=F_TITLE, fill=(30, 30, 30))
    for i in range(6):
        y = mt + plot_h - int(plot_h * i / 5)
        d.line((ml, y, w - mr, y), fill=(225, 225, 225), width=1)
        d.text((34, y - 8), f"{i/5:.1f}", font=F_AXIS, fill=(80, 80, 80))
    gap = 18
    bw = max(18, int((plot_w - gap * (len(labels) - 1)) / max(1, len(labels))))
    for idx, (label, rate) in enumerate(zip(labels, rates)):
        x = ml + idx * (bw + gap)
        bh = int(plot_h * max(0, min(1, rate)))
        y = mt + plot_h - bh
        d.rectangle((x, y, x + bw, mt + plot_h), fill=color)
        d.text((x, max(mt + 2, y - 20)), f"{rate:.2f}", font=F_SMALL, fill=(50, 50, 50))
        d.text((x - 40, h - 160 + (idx % 4) * 28), label[:28], font=F_SMALL, fill=(40, 40, 40))
    save(img, filename)


def latest_rows_jsonl(path: Path, key_fields):
    latest = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                latest[tuple(row.get(k) for k in key_fields)] = row
    return list(latest.values())


def exp01_04():
    path = REPRO / "EXP01_EXP04_RECOVERY" / "analysis" / "EXP01_EXP04_summary_counts.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    draw_horizontal([short_source(r["source_file"]) for r in rows], [int(r["clean_latest_ok"]) for r in rows], "EXP01-EXP04 recovered clean latest-ok cells", "fig_exp01_exp04_recovery_counts.png", (89, 161, 79))


def exp09():
    path = INTERNAL_EXPS / "EXP09_REAL_TOOL_USE_AGENT_TASKS" / "analysis_exp09" / "exp09_summary.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    labels, success, fail = [], [], []
    for key, row in sorted(data["success_by_route_mode"].items()):
        labels.append(key.strip("()").replace("'", "").replace(", ", " / "))
        success.append(int(row["ok"]))
        fail.append(int(row["total"]) - int(row["ok"]))
    draw_stacked(labels, success, fail, "EXP09 deterministic tool-use validation", "fig_exp09_success_by_route_mode.png")


def exp10():
    data = json.loads((INTERNAL_EXPS / "EXP10_PUBLIC_REPO_TOOL_AGENT" / "analysis_exp10" / "exp10_summary.json").read_text(encoding="utf-8"))
    metrics = data["metric_means_ok"]
    wanted = ["task_success", "state_preserved", "plan_preserved", "constraint_preservation_score", "dependency_preservation_score", "recovery_score", "scope_drift_rate", "claim_drift_rate"]
    labels = [m for m in wanted if m in metrics]
    vals = [float(metrics[m]) for m in labels]
    draw_horizontal(labels, vals, "EXP10 public repo tool-agent metric means", "fig_exp10_metric_means.png", (118, 183, 178), "mean value")


def exp11():
    rows = latest_rows_jsonl(INTERNAL_EXPS / "EXP11_PAGE_TASK_ASSIGNMENT" / "exp11_runs.jsonl", ["task_id", "mode", "model_route", "rep"])
    by_model = defaultdict(lambda: Counter(total=0, success=0))
    for row in rows:
        k = row.get("model_route", "unknown")
        by_model[k]["total"] += 1
        if row.get("status") == "ok" and row.get("validation", {}).get("task_success") is True:
            by_model[k]["success"] += 1
    labels = sorted(by_model)
    draw_stacked(labels, [by_model[k]["success"] for k in labels], [by_model[k]["total"] - by_model[k]["success"] for k in labels], "EXP11 page task assignment: latest-cell outcomes", "fig_exp11_success_by_model.png")


def exp12():
    rows = latest_rows_jsonl(INTERNAL_EXPS / "EXP12_CONFLICT_AWARE_REPO_MAINTENANCE" / "exp12_runs.jsonl", ["pair_id", "mode", "model_route", "rep"])
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
    draw_stacked(labels, [by_mode[k]["success"] for k in labels], [by_mode[k]["total"] - by_mode[k]["success"] for k in labels], "EXP12 conflict-aware maintenance: latest-cell outcomes", "fig_exp12_success_by_mode.png", ((89, 161, 79), (225, 87, 89)))
    draw_horizontal(sorted(drift), [sum(drift[k]) / len(drift[k]) for k in sorted(drift)], "EXP12 mean claim drift by mode", "fig_exp12_claim_drift_by_mode.png", (242, 142, 43), "mean claim drift")


def exp13():
    rows = [json.loads(l) for l in (REPRO / "EXP13_REAL_MULTI_AGENT_SCIENTIFIC_REPO_BENCHMARK" / "exp13_latest_cells_clean.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    totals, counts = Counter(), Counter()
    for row in rows:
        key = (row.get("model_route", "unknown"), row.get("mode", "unknown"))
        totals[key] += 1
        if row.get("status") == "ok" and row.get("validation", {}).get("task_success") is True:
            counts[key] += 1
    keys = sorted(totals)
    labels = [f"{a}/{b}" for a, b in keys]
    draw_stacked(labels, [counts[k] for k in keys], [totals[k] - counts[k] for k in keys], "EXP13 real multi-agent repo benchmark", "fig_exp13_success_by_model_mode.png")


def exp14():
    rows = [json.loads(l) for l in (INTERNAL_EXPS / "EXP14_LONG_HORIZON_REPO_MAINTENANCE" / "exp14_latest_cells_clean.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    by_round = defaultdict(lambda: Counter(total=0, success=0))
    by_mode = defaultdict(lambda: Counter(total=0, success=0))
    for row in rows:
        ok = row.get("status") == "ok" and row.get("validation", {}).get("ok") is True
        r = f"round_{row.get('round', 'unknown')}"
        m = row.get("mode", "unknown")
        by_round[r]["total"] += 1
        by_mode[m]["total"] += 1
        if ok:
            by_round[r]["success"] += 1
            by_mode[m]["success"] += 1
    labels = sorted(by_round, key=lambda s: int(s.split("_")[1]) if s.split("_")[1].isdigit() else 999)
    draw_rates(labels, [by_round[k]["success"] / by_round[k]["total"] for k in labels], "EXP14 success rate by round", "fig_exp14_success_rate_by_round.png", (76, 120, 168))
    labels = sorted(by_mode)
    draw_rates(labels, [by_mode[k]["success"] / by_mode[k]["total"] for k in labels], "EXP14 success rate by mode", "fig_exp14_success_rate_by_mode.png", (89, 161, 79))


def exp16():
    rows = list(csv.DictReader((REPRO / "EXP16_MODEL_SPECIFIC_PROTOCOL_ADAPTATION" / "exp16_latest_cells_summary.csv").open(encoding="utf-8")))
    by_model = defaultdict(lambda: Counter(total=0, success=0))
    by_mode = defaultdict(lambda: Counter(total=0, success=0))
    for row in rows:
        if row["model_route"] == "gemini_3_flash_preview":
            continue
        ok = row["status"].startswith("ok")
        by_model[row["model_route"]]["total"] += 1
        by_mode[row["mode"]]["total"] += 1
        if ok:
            by_model[row["model_route"]]["success"] += 1
            by_mode[row["mode"]]["success"] += 1
    labels = sorted(by_model)
    draw_stacked(labels, [by_model[k]["success"] for k in labels], [by_model[k]["total"] - by_model[k]["success"] for k in labels], "EXP16 outcome by model route", "fig_exp16_success_by_model.png", ((76, 120, 168), (242, 142, 43)))
    labels = sorted(by_mode)
    draw_stacked(labels, [by_mode[k]["success"] for k in labels], [by_mode[k]["total"] - by_mode[k]["success"] for k in labels], "EXP16 outcome by prompt adaptation mode", "fig_exp16_success_by_mode.png", ((89, 161, 79), (225, 87, 89)))


def exp16b():
    rows = list(csv.DictReader((REPRO / "EXP16B_GROK_REASONING_ADAPTATION_SEARCH" / "exp16b_latest_cells_summary.csv").open(encoding="utf-8")))
    by_mode = defaultdict(lambda: Counter(total=0, success=0))
    errors = Counter()
    for row in rows:
        by_mode[row["mode"]]["total"] += 1
        if row["status"].startswith("ok"):
            by_mode[row["mode"]]["success"] += 1
        elif row.get("error_class"):
            errors[row["error_class"]] += 1
    labels = sorted(by_mode)
    draw_rates(labels, [by_mode[k]["success"] / by_mode[k]["total"] for k in labels], "EXP16B Grok reasoning adaptation search", "fig_exp16b_success_rate_by_variant.png")
    draw_horizontal([k for k, _ in errors.most_common()], [v for _, v in errors.most_common()], "EXP16B terminal failure classes", "fig_exp16b_failure_classes.png", (225, 87, 89), "failure cells")


def coverage():
    labels = ["EXP01-04", "EXP05", "EXP06", "EXP07", "EXP08", "EXP09", "EXP10", "EXP11", "EXP12", "EXP13", "EXP14", "EXP15", "EXP15B", "EXP16", "EXP16B"]
    draw_rates(labels, [1.0] * len(labels), "Figure coverage across the experiment trail", "fig_experiment_figure_coverage.png", (118, 183, 178))


def main():
    for fn in [exp01_04, exp09, exp10, exp11, exp12, exp13, exp14, exp16, exp16b, coverage]:
        fn()
    print(f"Wrote PNG appendix figures to {OUT}")


if __name__ == "__main__":
    main()
