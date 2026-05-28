from __future__ import annotations

import argparse
import csv
import html
from pathlib import Path


COLORS = ["#2f6f9f", "#7a9f35", "#b66a36", "#7f5ca3", "#3f8f83", "#b84a4a"]


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def num(row: dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default) or default)
    except ValueError:
        return default


def text(x: float, y: float, value: str, size: int = 12, anchor: str = "start", weight: str = "400") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="#222">{html.escape(value)}</text>'


def write_svg(path: Path, width: int, height: int, body: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        *body,
        "</svg>",
    ]
    path.write_text("\n".join(svg) + "\n", encoding="utf-8")


def grouped_bars(path: Path, title: str, groups: list[str], series: list[tuple[str, list[float]]], max_y: float = 5.0) -> None:
    width, height = 980, 520
    left, top, bottom, right = 70, 70, 105, 30
    plot_w, plot_h = width - left - right, height - top - bottom
    n_groups, n_series = len(groups), len(series)
    group_w = plot_w / max(n_groups, 1)
    bar_w = min(26, group_w / (n_series + 2))
    body = [text(width / 2, 32, title, 18, "middle", "700")]
    for tick in range(6):
        y = top + plot_h - (tick / 5) * plot_h
        body.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#ddd" stroke-width="1"/>')
        body.append(text(left - 12, y + 4, f"{tick}", 11, "end"))
    body.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="#333"/>')
    body.append(f'<line x1="{left}" y1="{top+plot_h}" x2="{width-right}" y2="{top+plot_h}" stroke="#333"/>')
    for gi, group in enumerate(groups):
        cx = left + gi * group_w + group_w / 2
        body.append(text(cx, top + plot_h + 32, group, 11, "middle"))
        for si, (_, vals) in enumerate(series):
            val = vals[gi]
            h = max(0, min(val / max_y, 1)) * plot_h
            x = cx - (n_series * bar_w) / 2 + si * bar_w
            y = top + plot_h - h
            body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w-2:.1f}" height="{h:.1f}" fill="{COLORS[si % len(COLORS)]}"/>')
    for si, (name, _) in enumerate(series):
        lx = left + si * 145
        body.append(f'<rect x="{lx}" y="{height-35}" width="14" height="14" fill="{COLORS[si % len(COLORS)]}"/>')
        body.append(text(lx + 20, height - 23, name, 11))
    write_svg(path, width, height, body)


def horizontal_deltas(path: Path, title: str, rows: list[tuple[str, float]]) -> None:
    rows = rows[:22]
    width, height = 980, max(360, 80 + len(rows) * 27)
    left, right, top = 330, 40, 55
    plot_w = width - left - right
    max_abs = max([abs(v) for _, v in rows] + [0.1])
    zero_x = left + plot_w / 2
    body = [text(width / 2, 30, title, 18, "middle", "700")]
    body.append(f'<line x1="{zero_x:.1f}" y1="{top-15}" x2="{zero_x:.1f}" y2="{height-35}" stroke="#333"/>')
    for i, (label, value) in enumerate(rows):
        y = top + i * 27
        x2 = zero_x + (value / max_abs) * (plot_w / 2)
        x = min(zero_x, x2)
        w = abs(x2 - zero_x)
        color = "#2f6f9f" if value >= 0 else "#b84a4a"
        body.append(text(left - 10, y + 12, label, 11, "end"))
        body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="17" fill="{color}"/>')
        body.append(text(x2 + (5 if value >= 0 else -5), y + 13, f"{value:.3f}", 10, "start" if value >= 0 else "end"))
    write_svg(path, width, height, body)


def line_chart(path: Path, title: str, xlabels: list[str], series: list[tuple[str, list[float]]], max_y: float = 1.0) -> None:
    width, height = 980, 520
    left, top, bottom, right = 80, 65, 120, 40
    plot_w, plot_h = width - left - right, height - top - bottom
    body = [text(width / 2, 30, title, 18, "middle", "700")]
    for tick in range(6):
        y = top + plot_h - (tick / 5) * plot_h
        body.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#ddd"/>')
        body.append(text(left - 12, y + 4, f"{tick/5:.1f}", 11, "end"))
    for si, (name, vals) in enumerate(series):
        pts = []
        for i, val in enumerate(vals):
            x = left + (i / max(len(xlabels) - 1, 1)) * plot_w
            y = top + plot_h - (val / max_y) * plot_h
            pts.append((x, y))
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        body.append(f'<polyline points="{d}" fill="none" stroke="{COLORS[si % len(COLORS)]}" stroke-width="3"/>')
        for x, y in pts:
            body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{COLORS[si % len(COLORS)]}"/>')
        lx = left + si * 160
        body.append(f'<rect x="{lx}" y="{height-35}" width="14" height="14" fill="{COLORS[si % len(COLORS)]}"/>')
        body.append(text(lx + 20, height - 23, name, 11))
    for i, label in enumerate(xlabels):
        x = left + (i / max(len(xlabels) - 1, 1)) * plot_w
        body.append(text(x, height - 70, label, 10, "middle"))
    write_svg(path, width, height, body)


def scatter(path: Path, title: str, points: list[tuple[str, float, float, float]]) -> None:
    width, height = 760, 520
    left, top, bottom, right = 80, 65, 80, 50
    plot_w, plot_h = width - left - right, height - top - bottom
    max_x = max([p[1] for p in points] + [0.1])
    body = [text(width / 2, 30, title, 18, "middle", "700")]
    body.append(f'<line x1="{left}" y1="{top+plot_h}" x2="{width-right}" y2="{top+plot_h}" stroke="#333"/>')
    body.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="#333"/>')
    body.append(text(width / 2, height - 25, "Estimated USD cost", 12, "middle"))
    body.append(text(20, top + plot_h / 2, "Variable recovery", 12, "middle"))
    for i, (label, xval, yval, size) in enumerate(points):
        x = left + (xval / max_x) * plot_w
        y = top + plot_h - yval * plot_h
        r = min(20, max(5, size))
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{COLORS[i % len(COLORS)]}" opacity="0.75"/>')
        body.append(text(x + 8, y - 8, label, 11))
    write_svg(path, width, height, body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default="paper/figures")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    out = (root / args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    exp05 = load_rows(root / "analysis/EXP05/principal_by_mode.csv")
    grouped_bars(
        out / "extra_exp05_modes_vs_metrics.svg",
        "EXP05: modes vs core metrics",
        [r["mode"] for r in exp05],
        [
            ("Fidelity", [num(r, "semantic_fidelity_mean") for r in exp05]),
            ("Utility", [num(r, "utility_mean") for r in exp05]),
            ("State", [num(r, "state_preservation_mean") for r in exp05]),
            ("Continuity", [num(r, "operational_continuity_mean") for r in exp05]),
            ("Compactness", [num(r, "compactness_mean") for r in exp05]),
        ],
        5.0,
    )

    deltas: list[tuple[str, float]] = []
    for r in load_rows(root / "analysis/EXP06/EXP06_ANALYSIS_20260526_151836/paired_effect_by_phase.csv"):
        deltas.append((f"EXP06 {r.get('phase', 'phase')}", num(r, "mean_delta")))
    for r in load_rows(root / "analysis/EXP07/exp07_paired_delta_summary.csv"):
        deltas.append((f"EXP07 {r.get('metric', 'objective')}", num(r, "mean_delta", num(r, "delta_mean"))))
    horizontal_deltas(out / "extra_paired_deltas.svg", "Paired deltas: hybrid_state minus comparator", deltas)

    rows = load_rows(root / "analysis/EXP07/exp07_framework_model_mode_summary.csv")
    keys = sorted({(r["framework"], r["model_key"]) for r in rows})
    modes = ["natural", "compressed", "hybrid_state"]
    data = {(r["framework"], r["model_key"], r["mode"]): num(r, "variable_recovery_rate_mean") for r in rows}
    line_chart(
        out / "extra_framework_model_interaction.svg",
        "EXP07: framework/model interaction",
        [f"{fw}\\n{model.replace('azure_', '')}" for fw, model in keys],
        [(mode, [data.get((fw, model, mode), 0.0) for fw, model in keys]) for mode in modes],
        1.0,
    )

    costs = {r["model_key"]: num(r, "cost_estimated_usd") for r in load_rows(root / "analysis/EXP07/exp07_cost_summary.csv")}
    quality = load_rows(root / "analysis/EXP07/exp07_model_summary.csv")
    scatter(
        out / "extra_cost_vs_quality.svg",
        "EXP07: cost vs objective quality",
        [(r["model_key"].replace("azure_", ""), costs.get(r["model_key"], 0.0), num(r, "variable_recovery_rate_mean"), num(r, "n") / 8) for r in quality],
    )
    print(f"wrote SVG figures to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
