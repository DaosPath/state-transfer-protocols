from __future__ import annotations

import csv
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
# Keep output relative to the working directory to avoid Windows MAX_PATH issues
# with PIL's file writer on deeply nested research folders.
OUT = Path("paper_focused_handoff") / "figures"
OUT.mkdir(parents=True, exist_ok=True)


COLORS = {
    "natural": "#6b80bd",
    "compressed": "#dd8f55",
    "hybrid_min": "#8a83bd",
    "hybrid_state": "#8a7c70",
    "EXP05": "#77b7cf",
    "EXP06": "#d28d63",
    "EXP07": "#9b9b9b",
    "EXP08": "#8a7c70",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


FONT = font(28)
FONT_SM = font(22)
FONT_XS = font(18)
FONT_TITLE = font(30, bold=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def draw_line_chart(
    path: Path,
    title: str,
    subtitle: str,
    xlabels: list[str],
    series: dict[str, list[float]],
    y_label: str,
    y_min: float | None = None,
    y_max: float | None = None,
    dashed: set[str] | None = None,
    error: dict[str, tuple[list[float], list[float]]] | None = None,
    width: int = 980,
    height: int = 760,
) -> None:
    dashed = dashed or set()
    error = error or {}
    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)

    left, right, top, bottom = 115, 55, 110, 170
    plot = (left, top, width - right, height - bottom)
    x0, y0, x1, y1 = plot
    d.rectangle(plot, fill="#e9e9f2")

    values = [v for vals in series.values() for v in vals if not math.isnan(v)]
    if error:
        for lows, highs in error.values():
            values.extend(lows)
            values.extend(highs)
    if y_min is None:
        y_min = min(values)
    if y_max is None:
        y_max = max(values)
    pad = (y_max - y_min) * 0.12 if y_max > y_min else 1
    y_min -= pad
    y_max += pad

    def sx(i: int) -> float:
        if len(xlabels) == 1:
            return (x0 + x1) / 2
        return x0 + i * (x1 - x0) / (len(xlabels) - 1)

    def sy(v: float) -> float:
        return y1 - (v - y_min) * (y1 - y0) / (y_max - y_min)

    # grid and y ticks
    ticks = 5
    for t in range(ticks + 1):
        val = y_min + (y_max - y_min) * t / ticks
        yy = sy(val)
        d.line([(x0, yy), (x1, yy)], fill="white", width=3)
        label = f"{val:.2f}" if y_max - y_min < 5 else f"{val:.1f}"
        d.text((x0 - 12, yy), label, font=FONT_XS, anchor="rm", fill="#4d4d4d")

    for i, lab in enumerate(xlabels):
        xx = sx(i)
        d.line([(xx, y0), (xx, y1)], fill="white", width=2)
        d.text((xx, y1 + 18), lab, font=FONT_XS, anchor="mt", fill="#333333")

    d.text((width / 2, 45), title, font=FONT_TITLE, anchor="mm", fill="#222222")
    d.text((width / 2, 80), subtitle, font=FONT, anchor="mm", fill="#333333")
    d.text((42, (y0 + y1) / 2), y_label, font=FONT, anchor="mm", fill="#222222")

    # zero line if applicable
    if y_min < 0 < y_max:
        yy = sy(0)
        d.line([(x0, yy), (x1, yy)], fill="#7a7a7a", width=2)

    for name, vals in series.items():
        color = COLORS.get(name, "#555555")
        pts = [(sx(i), sy(v)) for i, v in enumerate(vals)]
        if name in error:
            lows, highs = error[name]
            for i, (lo, hi) in enumerate(zip(lows, highs)):
                xx = sx(i)
                d.line([(xx, sy(lo)), (xx, sy(hi))], fill=color, width=3)
                d.line([(xx - 8, sy(lo)), (xx + 8, sy(lo))], fill=color, width=3)
                d.line([(xx - 8, sy(hi)), (xx + 8, sy(hi))], fill=color, width=3)
        for a, b in zip(pts, pts[1:]):
            if name in dashed:
                draw_dashed(d, a, b, color)
            else:
                d.line([a, b], fill=color, width=5)
        for xx, yy in pts:
            d.ellipse((xx - 10, yy - 10, xx + 10, yy + 10), fill=color, outline="white", width=2)

    # legend
    lx, ly = left, height - 120
    items = list(series.keys())
    cols = min(3, len(items))
    cell_w = (width - left - right) / cols
    for idx, name in enumerate(items):
        cx = lx + (idx % cols) * cell_w
        cy = ly + (idx // cols) * 38
        color = COLORS.get(name, "#555555")
        d.line([(cx, cy), (cx + 34, cy)], fill=color, width=5)
        d.ellipse((cx + 12, cy - 8, cx + 28, cy + 8), fill=color, outline="white", width=2)
        d.text((cx + 46, cy), name, font=FONT_SM, anchor="lm", fill="#333333")

    img.save(path)


def draw_dashed(d: ImageDraw.ImageDraw, a: tuple[float, float], b: tuple[float, float], color: str) -> None:
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    step, dash = 18, 11
    t = 0.0
    while t < dist:
        t2 = min(t + dash, dist)
        d.line([(ax + ux * t, ay + uy * t), (ax + ux * t2, ay + uy * t2)], fill=color, width=5)
        t += step


def draw_grouped_bar_panels(
    path: Path,
    title: str,
    left_title: str,
    right_title: str,
    metrics: list[str],
    left_series: dict[str, list[float]],
    right_series: dict[str, list[float]],
    width: int = 1180,
    height: int = 620,
) -> None:
    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)
    d.text((width / 2, 42), title, font=FONT_TITLE, anchor="mm", fill="#222222")

    def draw_panel(x0: int, y0: int, x1: int, y1: int, panel_title: str, series: dict[str, list[float]]) -> None:
        d.rectangle((x0, y0, x1, y1), fill="#eeeeF5")
        d.text(((x0 + x1) / 2, y0 - 26), panel_title, font=FONT, anchor="mm", fill="#333333")
        for t in range(6):
            val = t / 5
            yy = y1 - val * (y1 - y0)
            d.line((x0, yy, x1, yy), fill="white", width=3)
            d.text((x0 - 10, yy), f"{val:.1f}", font=FONT_XS, anchor="rm", fill="#555555")
        names = list(series.keys())
        group_w = (x1 - x0) / len(metrics)
        bar_w = min(26, group_w / (len(names) + 1.8))
        for i, metric in enumerate(metrics):
            center = x0 + group_w * (i + 0.5)
            for j, name in enumerate(names):
                val = series[name][i]
                bx0 = center - (len(names) * bar_w) / 2 + j * bar_w
                bx1 = bx0 + bar_w * 0.78
                by = y1 - val * (y1 - y0)
                d.rectangle((bx0, by, bx1, y1), fill=COLORS.get(name, "#555555"))
            d.text((center, y1 + 16), metric, font=FONT_XS, anchor="mt", fill="#333333")
        d.text((x0 - 70, (y0 + y1) / 2), "Rate", font=FONT_SM, anchor="mm", fill="#222222")

    left_plot = (92, 120, 560, 465)
    right_plot = (680, 120, 1148, 465)
    draw_panel(*left_plot, left_title, left_series)
    draw_panel(*right_plot, right_title, right_series)

    legend_items = list(dict.fromkeys(list(left_series.keys()) + list(right_series.keys())))
    lx = 155
    ly = 560
    for idx, name in enumerate(legend_items):
        x = lx + idx * 250
        color = COLORS.get(name, "#555555")
        d.rectangle((x, ly - 12, x + 26, ly + 12), fill=color)
        d.text((x + 38, ly), name, font=FONT_SM, anchor="lm", fill="#333333")

    img.save(path)


def main() -> None:
    exp05 = read_csv(ROOT / "analysis" / "EXP05" / "principal_by_mode.csv")
    by_mode = {r["mode"]: r for r in exp05}
    metrics = [
        ("quality", "quality_index_mean"),
        ("fidelity", "semantic_fidelity_mean"),
        ("state", "state_preservation_mean"),
        ("continuity", "operational_continuity_mean"),
        ("compactness", "compactness_mean"),
    ]
    modes = ["natural", "compressed", "hybrid_min", "hybrid_state"]
    draw_line_chart(
        OUT / "fig_exp05_modes.png",
        "EXP05 Principal Results",
        "mode comparison across judge-scored metrics",
        [m[0] for m in metrics],
        {m: [f(by_mode[m], k) for _, k in metrics] for m in modes},
        "Score",
        y_min=3.3,
        y_max=5.0,
        dashed={"hybrid_min"},
    )

    exp06 = read_csv(ROOT / "analysis" / "EXP06" / "EXP06_ANALYSIS_20260526_151836" / "summary_by_mode.csv")
    by_mode6 = {r["mode"]: r for r in exp06}
    draw_line_chart(
        OUT / "fig_exp06_modes.png",
        "EXP06 Controlled Follow-Up",
        "compressed remains stronger globally; hybrid_state preserves more state",
        [m[0] for m in metrics],
        {
            "compressed": [f(by_mode6["compressed"], k) for _, k in metrics],
            "hybrid_state": [f(by_mode6["hybrid_state"], k) for _, k in metrics],
        },
        "Score",
        y_min=3.2,
        y_max=5.0,
    )

    lang = read_csv(ROOT / "analysis" / "EXP06" / "EXP06_ANALYSIS_20260526_151836" / "paired_effect_by_language.csv")
    order = ["EN", "ES", "ZH", "EN_LITERAL", "ES_LITERAL", "ZH_PINYIN"]
    rows = {r["language"]: r for r in lang}
    vals = [f(rows[x], "mean_delta") for x in order]
    lows = [f(rows[x], "ci95_low") for x in order]
    highs = [f(rows[x], "ci95_high") for x in order]
    draw_line_chart(
        OUT / "fig_exp06_language_delta.png",
        "EXP06 Paired Quality Delta",
        "hybrid_state minus compressed by language / variant",
        order,
        {"hybrid_state": vals},
        "Delta Q",
        y_min=-0.42,
        y_max=0.08,
        error={"hybrid_state": (lows, highs)},
    )

    exp07 = read_csv(ROOT / "analysis" / "EXP07" / "exp07_mode_summary.csv")
    by_mode7 = {r["mode"]: r for r in exp07}
    obj_metrics = [
        ("var rec.", "variable_recovery_rate_mean"),
        ("subtasks", "subtask_completion_rate_mean"),
        ("plan", "plan_continuity_rate_mean"),
        ("constraints", "constraint_retention_rate_mean"),
        ("handoff", "handoff_success_mean"),
    ]
    draw_line_chart(
        OUT / "fig_exp07_objective.png",
        "EXP07 Real-Agent Objective Metrics",
        "LangGraph/OpenFang handoff continuation, latest successful cells",
        [m[0] for m in obj_metrics],
        {m: [f(by_mode7[m], k) for _, k in obj_metrics] for m in ["natural", "compressed", "hybrid_state"]},
        "Rate",
        y_min=0.0,
        y_max=1.0,
    )

    exp08 = read_csv(ROOT / "data_freeze" / "EXP08_20260527_FINAL" / "analysis_final" / "exp08_operational_complete_mode_summary.csv")
    by_mode8 = {r["mode"]: r for r in exp08}
    obj_metrics8 = [
        ("var rec.", "variable_recovery_rate"),
        ("subtasks", "subtask_completion_rate"),
        ("plan", "plan_continuity_rate"),
        ("constraints", "constraint_retention_rate"),
        ("handoff", "handoff_success"),
    ]
    draw_line_chart(
        OUT / "fig_exp08_objective.png",
        "EXP08 Real-Agent Scale-Up",
        "900 operational executions, operational-complete view",
        [m[0] for m in obj_metrics8],
        {m: [f(by_mode8[m], k) for _, k in obj_metrics8] for m in ["compressed", "hybrid_state"]},
        "Rate",
        y_min=0.0,
        y_max=1.0,
    )

    draw_grouped_bar_panels(
        OUT / "fig_exp07_exp08_objective_compact.png",
        "Real-Agent Objective Metrics",
        "EXP07: cleaned executions",
        "EXP08: 900 operational executions",
        [m[0] for m in obj_metrics],
        {m: [f(by_mode7[m], k) for _, k in obj_metrics] for m in ["natural", "compressed", "hybrid_state"]},
        {m: [f(by_mode8[m], k) for _, k in obj_metrics8] for m in ["compressed", "hybrid_state"]},
    )


if __name__ == "__main__":
    main()
