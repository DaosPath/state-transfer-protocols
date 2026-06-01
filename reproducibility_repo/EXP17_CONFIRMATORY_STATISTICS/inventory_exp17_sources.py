from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXP_ROOT = ROOT / "05_Experimentos"
PUBLIC_ROOT = ROOT / "13_Repo_Publico" / "GITHUB_RELEASE_state-transfer-protocols"
OUT_DIR = Path(__file__).resolve().parent

EXP_RE = re.compile(r"EXP\d{2}[A-Z]?", re.IGNORECASE)
EXTENSIONS = {".csv", ".jsonl", ".json", ".md", ".txt", ".py", ".yaml", ".yml"}


ROLE_PATTERNS = {
    "prompts": ("prompt", "prompts"),
    "task_bank": ("task", "tasks", "bank"),
    "clean_data": ("clean", "latest_ok", "latest_cells"),
    "failures": ("failure", "failures", "error", "errors"),
    "checksums": ("checksum", "hash", "sha256", "manifest"),
    "report": ("informe", "report", "paper", "appendix"),
    "validators": ("validator", "validators", "schema", "schemas"),
    "runs": ("runs.jsonl", "run.jsonl"),
    "cost_ledger": ("cost", "ledger"),
    "config": ("config", "registry", "model"),
    "analysis": ("analysis", "analyze", "bootstrap", "figure", "plot"),
}


def infer_exp(path: Path) -> str:
    matches = []
    for part in path.parts:
        matches.extend(match.group(0).upper() for match in EXP_RE.finditer(part))
    return matches[-1] if matches else ""


def infer_role(path: Path) -> str:
    text = str(path).lower()
    roles = []
    for role, patterns in ROLE_PATTERNS.items():
        if any(pattern in text for pattern in patterns):
            roles.append(role)
    return "|".join(sorted(set(roles)))


def count_jsonl(path: Path) -> tuple[int | str, str]:
    rows = 0
    keys: set[str] = set()
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if not line.strip():
                    continue
                rows += 1
                if len(keys) < 80:
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    if isinstance(obj, dict):
                        keys.update(obj.keys())
    except Exception as exc:
        return "ERR", type(exc).__name__
    return rows, ",".join(sorted(keys))


def count_csv(path: Path) -> tuple[int | str, str]:
    rows = 0
    header = ""
    try:
        with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
            reader = csv.reader(handle)
            for i, row in enumerate(reader):
                if i == 0:
                    header = ",".join(row)
                    continue
                rows += 1
    except Exception as exc:
        return "ERR", type(exc).__name__
    return rows, header


def summarize_file(path: Path, source: str) -> dict[str, str | int]:
    suffix = path.suffix.lower()
    rows: int | str = ""
    columns = ""
    if suffix == ".jsonl":
        rows, columns = count_jsonl(path)
    elif suffix == ".csv":
        rows, columns = count_csv(path)
    elif suffix == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
            if isinstance(data, list):
                rows = len(data)
                columns = ",".join(sorted(data[0].keys())) if data and isinstance(data[0], dict) else ""
            elif isinstance(data, dict):
                rows = 1
                columns = ",".join(sorted(data.keys()))
        except Exception as exc:
            rows = "ERR"
            columns = type(exc).__name__

    rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    return {
        "source": source,
        "exp": infer_exp(path),
        "role": infer_role(path),
        "path": str(rel),
        "extension": suffix,
        "size_bytes": path.stat().st_size,
        "rows": rows,
        "columns_or_keys": columns[:1200],
    }


def iter_files(base: Path, source: str):
    if not base.exists():
        return
    for path in base.rglob("*"):
        if path.is_file() and path.suffix.lower() in EXTENSIONS:
            if ".git" in path.parts or "node_modules" in path.parts:
                continue
            yield summarize_file(path, source)


def write_csv(rows: list[dict[str, str | int]], path: Path) -> None:
    fields = ["source", "exp", "role", "path", "extension", "size_bytes", "rows", "columns_or_keys"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str | int]], path: Path) -> None:
    by_exp: dict[str, dict[str, int]] = {}
    for row in rows:
        exp = str(row["exp"] or "NO_EXP")
        by_exp.setdefault(exp, {})
        for role in str(row["role"]).split("|"):
            if not role:
                continue
            by_exp[exp][role] = by_exp[exp].get(role, 0) + 1

    lines = [
        "# EXP17 Data Inventory",
        "",
        "Compact inventory of frozen/local/public artifacts used for confirmatory analysis.",
        "",
        f"- Experiment root: `{EXP_ROOT}`",
        f"- Public repo root: `{PUBLIC_ROOT}`",
        f"- Files indexed: `{len(rows)}`",
        "",
        "## Role Counts by Experiment",
        "",
        "| Experiment | Roles detected |",
        "|---|---|",
    ]
    for exp in sorted(by_exp):
        roles = ", ".join(f"{role}:{count}" for role, count in sorted(by_exp[exp].items()))
        lines.append(f"| {exp} | {roles or '-'} |")

    lines.extend([
        "",
        "## Notes",
        "",
        "- Row counts are computed for CSV, JSON and JSONL files only.",
        "- Role detection is filename/path based; it is an audit guide, not a semantic proof.",
        "- This inventory intentionally avoids raw content previews to reduce accidental leakage.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = []
    rows.extend(iter_files(EXP_ROOT, "local_experiments"))
    rows.extend(iter_files(PUBLIC_ROOT, "public_repo"))
    rows = sorted(rows, key=lambda r: (str(r["exp"]), str(r["source"]), str(r["path"])))

    csv_path = OUT_DIR / "data_inventory_exp17.csv"
    md_path = OUT_DIR / "DATA_INVENTORY_EXP17.md"
    write_csv(rows, csv_path)
    write_markdown(rows, md_path)

    exp_count = len({str(row["exp"]) for row in rows if row["exp"]})
    print(json.dumps({
        "files_indexed": len(rows),
        "experiments_detected": exp_count,
        "csv": str(csv_path),
        "markdown": str(md_path),
    }, indent=2))


if __name__ == "__main__":
    main()
