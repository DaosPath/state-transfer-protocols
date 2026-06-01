from __future__ import annotations

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent
INVENTORY_CSV = HERE / "data_inventory_exp17.csv"
OUT_MD = HERE / "REPRODUCIBILITY_MATRIX_EXP01_EXP16.md"
OUT_CSV = HERE / "reproducibility_matrix_exp01_exp16.csv"

REQUIRED_ROLES = [
    "prompts",
    "task_bank",
    "clean_data",
    "failures",
    "checksums",
    "report",
]


def load_inventory() -> list[dict[str, str]]:
    with INVENTORY_CSV.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def role_set(rows: list[dict[str, str]]) -> set[str]:
    roles: set[str] = set()
    for row in rows:
        roles.update(role for role in row.get("role", "").split("|") if role)
    return roles


def main() -> None:
    rows = load_inventory()
    experiments = [f"EXP{i:02d}" for i in range(1, 17)]
    grouped = {exp: [row for row in rows if row.get("exp") == exp] for exp in experiments}

    matrix = []
    for exp, exp_rows in grouped.items():
        roles = role_set(exp_rows)
        record = {"experiment": exp, "files_indexed": str(len(exp_rows))}
        for role in REQUIRED_ROLES:
            record[role] = "yes" if role in roles else "missing"
        record["extra_roles"] = ", ".join(sorted(roles - set(REQUIRED_ROLES)))
        record["audit_status"] = "complete" if all(record[role] == "yes" for role in REQUIRED_ROLES) else "needs_review"
        matrix.append(record)

    fields = ["experiment", "files_indexed", *REQUIRED_ROLES, "extra_roles", "audit_status"]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(matrix)

    lines = [
        "# EXP01--EXP16 Reproducibility Matrix",
        "",
        "Audit generated from `data_inventory_exp17.csv`.",
        "",
        "| EXP | Files | Prompts | Task bank | Clean data | Failures | Checksums | Report | Status |",
        "|---|---:|---|---|---|---|---|---|---|",
    ]
    for row in matrix:
        lines.append(
            "| {experiment} | {files_indexed} | {prompts} | {task_bank} | {clean_data} | "
            "{failures} | {checksums} | {report} | {audit_status} |".format(**row)
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- `yes` means at least one artifact with that role was detected by path/name.",
        "- `missing` means the artifact was not detected automatically and should be reviewed manually.",
        "- This matrix is conservative; older experiments may have evidence embedded in reports rather than separate frozen files.",
        "",
    ])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print({"matrix_csv": str(OUT_CSV), "matrix_md": str(OUT_MD)})


if __name__ == "__main__":
    main()
