from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT_ROOT = ROOT / "05_Experimentos" / "EXP01_EXP04_RECOVERY"

RUN_FILES = [
    ROOT / "06_Resultados" / "experimento_01_runs.jsonl",
    ROOT / "06_Resultados" / "experimento_02_runs.jsonl",
    ROOT / "06_Resultados" / "experimento_03_fusion_runs.jsonl",
    ROOT / "09_Multilingue" / "08_Combined_Runs" / "exp01_exp02_en_zh_runs.jsonl",
    ROOT / "09_Multilingue" / "08_Combined_Runs" / "EXP03_EN" / "exp03_en_runs.jsonl",
    ROOT / "09_Multilingue" / "08_Combined_Runs" / "EXP03_ZH" / "exp03_zh_runs.jsonl",
    ROOT / "05_Experimentos" / "EXP04_TRI" / "exp04_tri_runs.jsonl",
    ROOT / "05_Experimentos" / "EXP04_TRI" / "exp04b_batch_decode_results.jsonl",
]

SUPPORT_PATTERNS = [
    ROOT / "05_Experimentos" / "Experimento_01_Comparacion_Token_Natural_vs_Cavernicola_vs_Proto.md",
    ROOT / "05_Experimentos" / "Experimento_02_ProtoV2_vs_Caveman.md",
    ROOT / "05_Experimentos" / "Experimento_03_Proto_v3_Minimalista.md",
    ROOT / "05_Experimentos" / "Prompts_de_Prueba.md",
    ROOT / "05_Experimentos" / "Metricas_de_Evaluacion.md",
    ROOT / "05_Experimentos" / "run_experimento_01_opencode_go.py",
    ROOT / "05_Experimentos" / "run_experimento_01_opencode_go_local.py",
    ROOT / "05_Experimentos" / "run_experimento_02_proto_v2_opencode_go.py",
    ROOT / "05_Experimentos" / "run_experimento_03_proto_v3_fusion_opencode_go.py",
    ROOT / "05_Experimentos" / "run_experimento_03_proto_v3_fusion_local.py",
    ROOT / "05_Experimentos" / "EXP04_TRI" / "run_exp04_tri_opencode_go.py",
    ROOT / "05_Experimentos" / "EXP04_TRI" / "task_bank_exp04_tri.jsonl",
    ROOT / "09_Multilingue" / "08_Combined_Runs" / "run_exp01_exp02_en_zh_combined_opencode_go.py",
    ROOT / "09_Multilingue" / "08_Combined_Runs" / "exp03_language_common.py",
    ROOT / "09_Multilingue" / "08_Combined_Runs" / "EXP03_EN" / "run_exp03_en_opencode_go.py",
    ROOT / "09_Multilingue" / "08_Combined_Runs" / "EXP03_ZH" / "run_exp03_zh_opencode_go.py",
]

REPORT_GLOBS = [
    ROOT / "06_Resultados",
    ROOT / "09_Multilingue" / "08_Combined_Runs",
    ROOT / "09_Multilingue" / "08_Combined_Runs" / "EXP03_EN",
    ROOT / "09_Multilingue" / "08_Combined_Runs" / "EXP03_ZH",
    ROOT / "05_Experimentos" / "EXP04_TRI",
    ROOT / "09_Multilingue" / "03_English_Experiments",
    ROOT / "09_Multilingue" / "04_Chinese_Experiments",
]

SECRET_PATTERNS = [
    re.compile(r"sk-(?:proj-)?[A-Za-z0-9_\-]{32,}"),
    re.compile(r"AIza[0-9A-Za-z_\-]{20,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9_\-.]{30,}"),
    re.compile(r"[A-Za-z0-9]{48,}"),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_jsonl(path: Path) -> tuple[list[dict], int]:
    rows: list[dict] = []
    bad = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            bad += 1
    return rows, bad


def exp_id_for(path: Path, row: dict) -> str:
    if row.get("experiment_id"):
        return str(row["experiment_id"])
    name = path.name.lower()
    if "experimento_01" in name:
        return "EXP01"
    if "experimento_02" in name:
        return "EXP02"
    if "experimento_03" in name:
        return "EXP03"
    return "UNKNOWN"


def model_for(row: dict) -> str:
    return str(row.get("generator_model") or row.get("model") or "unknown")


def canonical_cell_id(path: Path, row: dict) -> str:
    exp = exp_id_for(path, row)
    language = row.get("language") or "ES"
    task_id = row.get("task_id") or "NA"
    mode = row.get("mode") or row.get("base_family") or "NA"
    run = row.get("run") if row.get("run") is not None else "NA"
    model = model_for(row)
    if exp == "EXP04B_BATCH_FINAL_DECODE":
        task_id = "+".join(row.get("source_task_ids") or ["batch"])
        mode = row.get("base_family") or "batch_decode"
    return "__".join(str(x).replace("/", "-") for x in [exp, language, task_id, mode, model, f"r{run}"])


def is_ok(row: dict) -> bool:
    err = row.get("error")
    parse_err = row.get("evaluation_parse_error")
    if err not in (None, "", False):
        return False
    if parse_err not in (None, "", False):
        return False
    return True


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def copy_snapshot(src: Path, freeze_dir: Path) -> dict:
    target = freeze_dir / "source_snapshot" / rel(src)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, target)
    return {
        "source": rel(src),
        "snapshot": target.relative_to(freeze_dir).as_posix(),
        "bytes": src.stat().st_size,
        "sha256": sha256_file(src),
        "modified_utc": datetime.fromtimestamp(src.stat().st_mtime, timezone.utc).isoformat(),
    }


def collect_support_files() -> list[Path]:
    files = [p for p in SUPPORT_PATTERNS if p.exists()]
    for folder in REPORT_GLOBS:
        if not folder.exists():
            continue
        for p in folder.glob("*.md"):
            files.append(p)
        for p in folder.glob("*.json"):
            files.append(p)
        for p in folder.glob("*.log"):
            files.append(p)
    return sorted(set(files))


def secret_sweep(paths: list[Path]) -> list[dict]:
    hits = []
    for path in paths:
        if not path.exists() or path.suffix.lower() not in {".md", ".py", ".json", ".jsonl", ".txt", ".log"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                hits.append({"path": rel(path), "pattern": pat.pattern})
    return hits


def main() -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    freeze_dir = OUT_ROOT / "data_freeze" / f"EXP01_EXP04_RECOVERY_{stamp}"
    clean_dir = OUT_ROOT / "clean_latest_ok"
    analysis_dir = OUT_ROOT / "analysis"
    freeze_dir.mkdir(parents=True, exist_ok=True)
    clean_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)

    source_files = [p for p in RUN_FILES if p.exists()] + collect_support_files()
    snapshot_manifest = [copy_snapshot(p, freeze_dir) for p in source_files]

    summaries = []
    all_clean_rows = []
    all_terminal_errors = []
    for path in [p for p in RUN_FILES if p.exists()]:
        rows, bad = read_jsonl(path)
        latest: OrderedDict[str, dict] = OrderedDict()
        duplicates = 0
        for idx, row in enumerate(rows):
            enriched = dict(row)
            enriched["_source_file"] = rel(path)
            enriched["_source_index"] = idx
            enriched["_recovered_experiment_id"] = exp_id_for(path, row)
            enriched["_cell_id"] = canonical_cell_id(path, row)
            enriched["_status_normalized"] = "ok" if is_ok(row) else "terminal_error"
            if enriched["_cell_id"] in latest:
                duplicates += 1
            latest[enriched["_cell_id"]] = enriched

        clean_rows = [r for r in latest.values() if r["_status_normalized"] == "ok"]
        error_rows = [r for r in latest.values() if r["_status_normalized"] != "ok"]
        out_name = path.stem.replace(".jsonl", "") + ".clean_latest_ok.jsonl"
        err_name = path.stem.replace(".jsonl", "") + ".terminal_errors.jsonl"
        write_jsonl(clean_dir / out_name, clean_rows)
        write_jsonl(clean_dir / err_name, error_rows)
        all_clean_rows.extend(clean_rows)
        all_terminal_errors.extend(error_rows)

        exp_counts = Counter(exp_id_for(path, r) for r in rows)
        lang_counts = Counter(str(r.get("language") or "ES") for r in rows)
        mode_counts = Counter(str(r.get("mode") or r.get("base_family") or "NA") for r in rows)
        model_counts = Counter(model_for(r) for r in rows)
        summaries.append(
            {
                "file": rel(path),
                "rows_raw": len(rows),
                "json_parse_errors": bad,
                "unique_cells": len(latest),
                "duplicate_cells_removed": duplicates,
                "clean_latest_ok": len(clean_rows),
                "terminal_errors": len(error_rows),
                "experiments": dict(exp_counts),
                "languages": dict(lang_counts),
                "modes_top": dict(mode_counts.most_common(20)),
                "models": dict(model_counts),
            }
        )

    write_jsonl(clean_dir / "EXP01_EXP04_ALL.clean_latest_ok.jsonl", all_clean_rows)
    write_jsonl(clean_dir / "EXP01_EXP04_ALL.terminal_errors.jsonl", all_terminal_errors)

    totals_by_exp = Counter(r["_recovered_experiment_id"] for r in all_clean_rows)
    totals_by_lang = Counter(str(r.get("language") or "ES") for r in all_clean_rows)
    totals_by_model = Counter(model_for(r) for r in all_clean_rows)
    totals_by_mode = Counter(str(r.get("mode") or r.get("base_family") or "NA") for r in all_clean_rows)

    with (analysis_dir / "EXP01_EXP04_summary_counts.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "source_file",
                "rows_raw",
                "unique_cells",
                "duplicate_cells_removed",
                "clean_latest_ok",
                "terminal_errors",
                "json_parse_errors",
            ],
        )
        writer.writeheader()
        for s in summaries:
            writer.writerow(
                {
                    "source_file": s["file"],
                    "rows_raw": s["rows_raw"],
                    "unique_cells": s["unique_cells"],
                    "duplicate_cells_removed": s["duplicate_cells_removed"],
                    "clean_latest_ok": s["clean_latest_ok"],
                    "terminal_errors": s["terminal_errors"],
                    "json_parse_errors": s["json_parse_errors"],
                }
            )

    checksum_lines = [f"{m['sha256']}  {m['source']}" for m in snapshot_manifest]
    (freeze_dir / "SHA256SUMS.txt").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    sweep_hits = secret_sweep(source_files)
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(ROOT),
        "freeze_dir": str(freeze_dir),
        "clean_dir": str(clean_dir),
        "policy": {
            "deduplication_key": "experiment/language/task_id/mode/run/generator_model",
            "latest_cell_policy": "last row wins",
            "ok_policy": "error empty/null and evaluation_parse_error empty/null/false",
            "terminal_errors_kept_separately": True,
        },
        "summaries": summaries,
        "global_clean_counts": {
            "clean_latest_ok_total": len(all_clean_rows),
            "terminal_errors_total": len(all_terminal_errors),
            "by_experiment": dict(totals_by_exp),
            "by_language": dict(totals_by_lang),
            "by_model": dict(totals_by_model),
            "modes_top": dict(totals_by_mode.most_common(40)),
        },
        "snapshot_files": snapshot_manifest,
        "secret_sweep_hits": sweep_hits,
    }
    (freeze_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    readme = f"""# EXP01-EXP04 Recovery Freeze

Created UTC: {manifest['created_utc']}

This folder recovers and freezes the early protocol-compression experiments before EXP05.
Original files were not modified.

## Clean policy

- Cell key: `experiment/language/task_id/mode/run/generator_model`
- Deduplication: last row wins
- OK row: no terminal `error` and no `evaluation_parse_error`
- Terminal errors are preserved separately, not deleted

## Counts

- Clean latest OK rows: {len(all_clean_rows)}
- Terminal error rows: {len(all_terminal_errors)}
- Secret sweep hits: {len(sweep_hits)}

## Clean Outputs

- `{clean_dir.relative_to(OUT_ROOT).as_posix()}/EXP01_EXP04_ALL.clean_latest_ok.jsonl`
- `{clean_dir.relative_to(OUT_ROOT).as_posix()}/EXP01_EXP04_ALL.terminal_errors.jsonl`
- `{analysis_dir.relative_to(OUT_ROOT).as_posix()}/EXP01_EXP04_summary_counts.csv`

## Frozen Snapshot

- `{freeze_dir.relative_to(OUT_ROOT).as_posix()}/manifest.json`
- `{freeze_dir.relative_to(OUT_ROOT).as_posix()}/SHA256SUMS.txt`
- `{freeze_dir.relative_to(OUT_ROOT).as_posix()}/source_snapshot/`
"""
    (OUT_ROOT / "README_EXP01_EXP04_RECOVERY.md").write_text(readme, encoding="utf-8")

    print(json.dumps({
        "freeze_dir": str(freeze_dir),
        "clean_latest_ok_total": len(all_clean_rows),
        "terminal_errors_total": len(all_terminal_errors),
        "secret_sweep_hits": len(sweep_hits),
        "summary_csv": str(analysis_dir / "EXP01_EXP04_summary_counts.csv"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
