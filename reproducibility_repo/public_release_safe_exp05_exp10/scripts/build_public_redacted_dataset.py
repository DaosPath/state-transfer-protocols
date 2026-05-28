from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from redact_jsonl_for_public import redact_jsonl


DEFAULT_JSONL = [
    "analysis/EXP06/EXP06_ANALYSIS_20260526_151836/exp06_clean_ok.jsonl",
    "analysis/EXP06/EXP06_ANALYSIS_20260526_151836/exp06_clean_terminal.jsonl",
    "data_freeze/EXP07/exp07_clean_dedup.jsonl",
    "data_freeze/EXP07/exp07_operational_errors.jsonl",
]

DEFAULT_CSV_DIRS = [
    "analysis/EXP05",
    "analysis/EXP06/EXP06_ANALYSIS_20260526_151836",
    "analysis/EXP07",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_csvs(root: Path, out: Path) -> list[str]:
    copied = []
    target = out / "analysis_csv"
    target.mkdir(parents=True, exist_ok=True)
    for rel_dir in DEFAULT_CSV_DIRS:
        src_dir = root / rel_dir
        if not src_dir.exists():
            continue
        for src in src_dir.glob("*.csv"):
            name = src.relative_to(root).as_posix().replace("/", "__")
            shutil.copy2(src, target / name)
            copied.append(f"analysis_csv/{name}")
    return copied


def write_checksums(out: Path) -> None:
    rows = []
    for path in sorted(p for p in out.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt"):
        rows.append(f"{sha256(path)}  {path.relative_to(out).as_posix()}")
    (out / "SHA256SUMS.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default="PUBLIC_DATASET_REDACTED")
    parser.add_argument("--sweep", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out = (root / args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "jsonl_redacted").mkdir(exist_ok=True)

    reports = []
    for rel in DEFAULT_JSONL:
        src = root / rel
        if not src.exists():
            reports.append({"source": rel, "status": "missing"})
            continue
        dst = out / "jsonl_redacted" / rel.replace("/", "__")
        reports.append({"source": rel, "status": "redacted", **redact_jsonl(src, dst)})

    copied_csv = copy_csvs(root, out)
    manifest = {
        "name": "PUBLIC_DATASET_REDACTED",
        "policy": "Redacted JSONL plus aggregate CSV tables. Raw internal JSONL is not included.",
        "jsonl": reports,
        "csv_files": copied_csv,
        "license_recommendation": "CC BY 4.0 or CC BY-NC 4.0",
    }
    (out / "PUBLIC_DATASET_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_checksums(out)

    if args.sweep:
        sweep = root / "security_sweep_public_package.py"
        if sweep.exists():
            local_sweep = out / "security_sweep_public_package.py"
            shutil.copy2(sweep, local_sweep)
            proc = subprocess.run([sys.executable, str(local_sweep)], cwd=str(out), text=True, capture_output=True)
            (out / "SECURITY_SWEEP_STDOUT.json").write_text(proc.stdout, encoding="utf-8")
            if proc.returncode != 0:
                print(proc.stdout)
                print(proc.stderr)
                return proc.returncode

    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
