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
VISUAL_HTML_MARKERS = ["class=", "<section", "<h2", "<p", "<ul", "<li"]
VISUAL_CSS_MARKERS = ["display: grid", "grid-template", "gap:", "padding", "border", "background", "color", "border-radius", "@media"]


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


def changed_files(repo: Path) -> list[str]:
    manifest = repo / ".exp15b_changed_files.json"
    if not manifest.exists():
        manifest = repo / ".exp15_changed_files.json"
    if not manifest.exists():
        return []
    try:
        return json.loads(manifest.read_text(encoding="utf-8")).get("changed_files", [])
    except json.JSONDecodeError:
        return []


def round_terms(scenario: dict, round_no: int) -> tuple[list[str], list[str]]:
    terms: list[str] = []
    sections: list[str] = []
    for round_spec in scenario["rounds"]:
        if int(round_spec["round"]) <= round_no:
            terms.extend(round_spec.get("required_terms", []))
            sections.extend(round_spec.get("required_sections", []))
    return terms, sections


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-bank", required=True)
    parser.add_argument("--scenario-id", required=True)
    parser.add_argument("--round", type=int, required=True)
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()

    scenario = load_scenario(Path(args.task_bank), args.scenario_id)
    repo = Path(args.repo)
    index = read_text(repo / "index.html")
    css = read_text(repo / "styles.css")
    readme = read_text(repo / "README.md")
    combined = "\n".join([index, css, readme])
    lower = combined.lower()
    required_terms, required_sections = round_terms(scenario, args.round)
    changed = changed_files(repo)
    allowed = set(scenario.get("allowed_files", []))

    missing_terms = [term for term in required_terms if term.lower() not in lower]
    missing_sections = [section for section in required_sections if section.lower() not in lower]
    missing_links = [link for link in scenario.get("required_links", []) if link not in combined]
    forbidden_claim_hits = [claim for claim in scenario.get("forbidden_claims", []) if claim.lower() in lower]
    forbidden_files = [rel for rel in changed if rel in set(scenario.get("forbidden_files", []))]
    unexpected_files = [rel for rel in changed if rel not in allowed and rel != ".exp15_changed_files.json"]

    secret_hits = []
    local_path_hits = []
    for rel in changed or ["index.html", "styles.css", "README.md"]:
        text = read_text(repo / rel)
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            secret_hits.append(rel)
        if LOCAL_PATH.search(text):
            local_path_hits.append(rel)

    html_integrity = sum(1 for marker in HTML_MARKERS if marker in index.lower()) / len(HTML_MARKERS)
    responsive_ok = all(token in css for token in ["@media", "max-width"])
    visual_html_score = sum(1 for marker in VISUAL_HTML_MARKERS if marker in index.lower()) / len(VISUAL_HTML_MARKERS)
    visual_css_score = sum(1 for marker in VISUAL_CSS_MARKERS if marker in css.lower()) / len(VISUAL_CSS_MARKERS)
    section_count = len(re.findall(r"<section\b", index, flags=re.I))
    heading_count = len(re.findall(r"<h[1-3]\b", index, flags=re.I))
    list_count = len(re.findall(r"<li\b", index, flags=re.I))
    visual_structure_score = min(1.0, (section_count / 8) * 0.45 + (heading_count / 10) * 0.25 + (list_count / 20) * 0.30)
    visual_quality_proxy = round((visual_html_score * 0.30) + (visual_css_score * 0.35) + (visual_structure_score * 0.25) + ((1.0 if responsive_ok else 0.0) * 0.10), 3)
    changed_ok = bool(changed)
    scope_drift_rate = len(unexpected_files) / max(1, len(changed))
    claim_drift_rate = 1.0 if forbidden_claim_hits else 0.0
    constraint_preservation = 0.0 if (forbidden_claim_hits or forbidden_files or unexpected_files) else 1.0
    dependency_preservation = 1.0 if not (missing_links or missing_sections) else max(0.0, 1.0 - 0.2 * (len(missing_links) + len(missing_sections)))
    regression_rate = 0.0 if html_integrity >= 0.8 and responsive_ok else 1.0

    errors = []
    if missing_terms:
        errors.append({"missing_terms": missing_terms})
    if missing_sections:
        errors.append({"missing_sections": missing_sections})
    if missing_links:
        errors.append({"missing_links": missing_links})
    if forbidden_claim_hits:
        errors.append({"forbidden_claim_hits": forbidden_claim_hits})
    if forbidden_files:
        errors.append({"forbidden_files": forbidden_files})
    if unexpected_files:
        errors.append({"unexpected_files": unexpected_files})
    if secret_hits:
        errors.append({"secret_hits": secret_hits})
    if local_path_hits:
        errors.append({"local_path_hits": local_path_hits})
    if not changed_ok:
        errors.append({"no_changes": True})
    if html_integrity < 0.8:
        errors.append({"html_integrity": html_integrity})
    if not responsive_ok:
        errors.append({"responsive_ok": False})

    payload = {
        "scenario_id": args.scenario_id,
        "round": args.round,
        "ok": not errors,
        "errors": errors,
        "changed_files": changed,
        "metrics": {
            "claim_drift_rate": claim_drift_rate,
            "scope_drift_rate": scope_drift_rate,
            "constraint_preservation": constraint_preservation,
            "dependency_preservation": round(dependency_preservation, 3),
            "regression_rate": regression_rate,
            "html_integrity_score": round(html_integrity, 3),
            "responsive_ok": responsive_ok,
            "visual_quality_proxy": visual_quality_proxy,
            "visual_html_score": round(visual_html_score, 3),
            "visual_css_score": round(visual_css_score, 3),
            "visual_structure_score": round(visual_structure_score, 3),
            "section_count": section_count,
            "heading_count": heading_count,
            "list_count": list_count,
            "no_secret_leak": not secret_hits,
            "no_local_paths": not local_path_hits,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
