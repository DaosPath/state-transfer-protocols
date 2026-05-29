from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SECRET_PATTERNS = [
    re.compile(r"sk-(proj-)?[A-Za-z0-9_\-]{10,}"),
    re.compile(r"AIza[0-9A-Za-z_\-]{10,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]{10,}", re.I),
    re.compile(r"CkOG[A-Za-z0-9]{20,}"),
]
LOCAL_PATH = re.compile(r"[A-Za-z]:\\[^\s\"'<>]+")
HTML_MARKERS = ["<!doctype html", "<html", "<head", "<body", "</html>"]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_scenario(path: Path, scenario_id: str) -> dict:
    for row in read_jsonl(path):
        if row["scenario_id"] == scenario_id:
            return row
    raise SystemExit(f"scenario_id not found: {scenario_id}")


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def count_hits(items: list[str], text: str) -> int:
    lower = text.lower()
    return sum(1 for item in items if item and item.lower() in lower)


def changed_files(repo: Path) -> list[str]:
    manifest = repo / ".exp13_changed_files.json"
    if not manifest.exists():
        return []
    try:
        return json.loads(manifest.read_text(encoding="utf-8")).get("changed_files", [])
    except json.JSONDecodeError:
        return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-bank", required=True)
    parser.add_argument("--scenario-id", required=True)
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()

    scenario = load_scenario(Path(args.task_bank), args.scenario_id)
    repo = Path(args.repo)
    index = read_text(repo / "index.html")
    css = read_text(repo / "styles.css")
    readme = read_text(repo / "README.md")
    combined = "\n".join([index, css, readme])
    required_terms = scenario.get("required_terms", [])
    required_sections = scenario.get("required_sections", [])
    allowed = set(scenario.get("allowed_files", []))
    changed = changed_files(repo)

    forbidden_claim_hits = [claim for claim in scenario.get("forbidden_claims", []) if claim.lower() in combined.lower()]
    missing_links = [link for link in scenario.get("required_links", []) if link not in combined]
    forbidden_files = [rel for rel in changed if rel in set(scenario.get("forbidden_files", []))]
    unexpected_files = [rel for rel in changed if rel not in allowed and rel != ".exp13_changed_files.json"]
    secret_hits = []
    local_path_hits = []
    for rel in changed or ["index.html", "styles.css", "README.md"]:
        text = read_text(repo / rel)
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            secret_hits.append(rel)
        if LOCAL_PATH.search(text):
            local_path_hits.append(rel)

    html_integrity = count_hits(HTML_MARKERS, index) / len(HTML_MARKERS)
    required_terms_present = count_hits(required_terms, combined)
    required_sections_present = count_hits(required_sections, combined)
    conflict_detection = count_hits(["conflict", "overlap", "merge", "regression", "controlled"], combined) > 0
    responsive_ok = "@media" in css and ("max-width" in css or "minmax" in css)
    max_files_touched = int(scenario.get("max_files_touched", max(1, len(allowed))))
    touched_for_scope = [rel for rel in changed if rel != ".exp13_changed_files.json"]

    result = {
        "scenario_id": args.scenario_id,
        "scenario_type": scenario["scenario_type"],
        "changed_files": changed,
        "required_terms_present": required_terms_present,
        "required_terms_expected": len(required_terms),
        "required_sections_present": required_sections_present,
        "required_sections_expected": len(required_sections),
        "conflict_detection": conflict_detection,
        "merge_safety": required_terms_present >= len(required_terms) and not forbidden_claim_hits,
        "constraint_preservation": not forbidden_claim_hits and not missing_links and not forbidden_files,
        "claim_drift_rate": len(forbidden_claim_hits) / max(1, len(scenario.get("forbidden_claims", []))),
        "scope_drift_rate": len(unexpected_files) / max(1, len(touched_for_scope)),
        "dependency_preservation": 1 - (len(missing_links) / max(1, len(scenario.get("required_links", [])))),
        "regression_rate": 0 if html_integrity >= 1 and responsive_ok else 1,
        "repair_success": conflict_detection and not forbidden_claim_hits and not unexpected_files,
        "html_integrity_score": html_integrity,
        "responsive_ok": responsive_ok,
        "missing_links": missing_links,
        "forbidden_claim_hits": forbidden_claim_hits,
        "forbidden_files_touched": forbidden_files,
        "unexpected_files_touched": unexpected_files,
        "max_files_touched_ok": len(touched_for_scope) <= max_files_touched,
        "no_secret_leak": not secret_hits,
        "secret_hits": secret_hits,
        "no_local_paths": not local_path_hits,
        "local_path_hits": local_path_hits,
    }
    result["task_success"] = (
        result["merge_safety"]
        and result["constraint_preservation"]
        and result["scope_drift_rate"] == 0
        and result["dependency_preservation"] >= 1
        and result["regression_rate"] == 0
        and result["max_files_touched_ok"]
        and result["no_secret_leak"]
        and result["no_local_paths"]
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["task_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
