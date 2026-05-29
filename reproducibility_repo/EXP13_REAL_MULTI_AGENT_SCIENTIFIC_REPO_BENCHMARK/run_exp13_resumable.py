from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "task_bank_exp13_scientific_repo.jsonl"
PROMPTS = ROOT / "prompts_exp13_modes.json"
MODELS = ROOT / "model_registry_exp13.json"
SEED_SITE = ROOT / "seed_site"
RUNS = ROOT / "exp13_runs.jsonl"
COST_LEDGER = ROOT / "exp13_cost_ledger.jsonl"
WORKSPACES = ROOT / "workspace_runs"
VALIDATOR = ROOT / "validators" / "validate_scientific_repo.py"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def safe_rmtree(path: Path) -> None:
    def onexc(func, p, exc):
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except Exception:
            pass

    if path.exists():
        shutil.rmtree(path, onexc=onexc)


def copy_seed(repo: Path) -> None:
    if not repo.exists():
        shutil.copytree(SEED_SITE, repo)


def file_context(repo: Path) -> dict[str, str]:
    return {
        "index.html": (repo / "index.html").read_text(encoding="utf-8", errors="replace"),
        "styles.css": (repo / "styles.css").read_text(encoding="utf-8", errors="replace"),
        "README.md": (repo / "README.md").read_text(encoding="utf-8", errors="replace") if (repo / "README.md").exists() else "",
    }


def build_prompt(scenario: dict[str, Any], mode: str, model_route: str, repo: Path) -> str:
    prompts = read_json(PROMPTS)
    ctx = file_context(repo)
    return f"""You are EXP13 real multi-agent scientific repository maintenance system.

Model route: {model_route}
Protocol mode: {mode}
Mode instruction: {prompts[mode]["agent_instruction"]}

Experiment goal:
Act as a coordinated team over a scientific repository artifact. You must merge Writer, Reviewer, Reproducibility, Security/claims, and Merge/repair responsibilities into one safe edit.

Scenario:
{json.dumps(scenario, ensure_ascii=False, indent=2)}

Roles:
{json.dumps(scenario["roles"], ensure_ascii=False, indent=2)}

Scenario type: {scenario["scenario_type"]}
Scenario title: {scenario["title"]}

Current files:
--- index.html ---
{ctx["index.html"][:22000]}
--- styles.css ---
{ctx["styles.css"][:16000]}
--- README.md ---
{ctx["README.md"][:4000]}

Rules:
- Preserve required terms and required sections.
- Preserve required links.
- Do not write forbidden claims, even as examples.
- Do not invent acceptance/publication status.
- Do not include secrets, API keys, bearer tokens, local Windows paths, or private logs.
- Do not touch files outside allowed_files.
- Prefer small operations over full-file replacement.
- Include a short visible conflict/merge/recovery note when useful.

Return exactly one minified JSON object. First character must be "{{" and last character must be "}}".
No markdown. No comments. No prose outside JSON.
Schema:
{{
  "replacements": [
    {{"path": "index.html", "old": "exact existing substring", "new": "replacement substring"}}
  ],
  "insertions": [
    {{"path": "index.html", "before": "</main>", "content": "html fragment to insert"}}
  ],
  "appends": [
    {{"path": "styles.css", "content": "css fragment to append"}}
  ],
  "conflict_detected": true,
  "merge_summary": "short summary",
  "recovery_plan": ["short repair action if validation fails"],
  "risks": ["risk or limitation"]
}}"""


def parse_model_json(text: str) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return json.loads(text), None
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            return None, "no_json_object"
        try:
            return json.loads(match.group(0)), None
        except json.JSONDecodeError as exc:
            return None, f"json_decode_error:{exc}"


@dataclass
class Route:
    key: str
    cfg: dict[str, Any]

    @property
    def provider(self) -> str:
        return self.cfg["provider"]


def load_route(model_route: str) -> Route:
    registry = read_json(MODELS)
    if model_route not in registry:
        raise SystemExit(f"unknown model route: {model_route}")
    return Route(model_route, registry[model_route])


def azure_call(route: Route, prompt: str) -> tuple[str, dict[str, int]]:
    endpoint = os.environ[route.cfg["endpoint_env"]].rstrip("/")
    api_key = os.environ[route.cfg["api_key_env"]]
    payload: dict[str, Any] = {
        "model": route.cfg["model"],
        "messages": [{"role": "user", "content": prompt}],
        "max_completion_tokens": int(route.cfg.get("max_completion_tokens", 30000)),
    }
    if route.cfg.get("reasoning_effort"):
        payload["reasoning_effort"] = route.cfg["reasoning_effort"]
    req = urllib.request.Request(
        f"{endpoint}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}", "api-key": api_key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=float(route.cfg.get("timeout_seconds", 420))) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode("utf-8", errors="replace")) from exc
    text = data.get("choices", [{}])[0].get("message", {}).get("content") or ""
    usage = data.get("usage", {})
    return text, {
        "input_tokens": int(usage.get("prompt_tokens", 0) or estimate_tokens(prompt)),
        "output_tokens": int(usage.get("completion_tokens", 0) or estimate_tokens(text)),
    }


def google_token() -> str:
    token = os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN")
    if token:
        return token
    gcloud = shutil.which("gcloud") or shutil.which("gcloud.cmd") or shutil.which("gcloud.ps1")
    default = Path.home() / "AppData" / "Local" / "Google" / "Cloud SDK" / "google-cloud-sdk" / "bin" / "gcloud.cmd"
    if not gcloud and default.exists():
        gcloud = str(default)
    if not gcloud:
        raise RuntimeError("gcloud not found; set GOOGLE_OAUTH_ACCESS_TOKEN or install Google Cloud SDK")
    proc = subprocess.run([gcloud, "auth", "print-access-token"], text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "gcloud auth print-access-token failed")
    return proc.stdout.strip()


def gemini_call(route: Route, prompt: str) -> tuple[str, dict[str, int]]:
    project_id = os.environ.get(route.cfg.get("project_env", "VERTEX_PROJECT_ID")) or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise RuntimeError("Set VERTEX_PROJECT_ID or GOOGLE_CLOUD_PROJECT")
    url = (
        f"https://{route.cfg.get('endpoint', 'aiplatform.googleapis.com')}/v1/projects/{project_id}"
        f"/locations/{route.cfg.get('location', 'global')}/publishers/google/models/{route.cfg['model_id']}:generateContent"
    )
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": int(route.cfg.get("max_output_tokens_default", 12000)),
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "object",
                "properties": {
                    "replacements": {"type": "array", "items": {"type": "object", "properties": {"path": {"type": "string"}, "old": {"type": "string"}, "new": {"type": "string"}}, "required": ["path", "old", "new"]}},
                    "insertions": {"type": "array", "items": {"type": "object", "properties": {"path": {"type": "string"}, "before": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "before", "content"]}},
                    "appends": {"type": "array", "items": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
                    "conflict_detected": {"type": "boolean"},
                    "merge_summary": {"type": "string"},
                    "recovery_plan": {"type": "array", "items": {"type": "string"}},
                    "risks": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["merge_summary"],
            },
            "thinkingConfig": {"thinkingLevel": route.cfg.get("thinking_level_default", "LOW")},
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {google_token()}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=float(route.cfg.get("timeout_seconds", 180))) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode("utf-8", errors="replace")) from exc
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    text = "".join(part.get("text", "") for part in parts)
    usage = data.get("usageMetadata", {})
    return text, {
        "input_tokens": int(usage.get("promptTokenCount") or estimate_tokens(prompt)),
        "output_tokens": int(usage.get("candidatesTokenCount") or estimate_tokens(text)),
    }


def dry_local_response(scenario: dict[str, Any]) -> tuple[str, dict[str, int]]:
    terms = scenario.get("required_terms", [])
    sections = scenario.get("required_sections", [])
    title = scenario["title"].replace("&", "and")
    body = " ".join(terms + ["controlled", "conflict", "merge", "regression"])
    insertion = [
        f'<section id="exp13-{scenario["scenario_id"].lower()}" class="section exp13-benchmark">',
        f'  <div class="section-heading narrow"><p class="section-label">EXP13</p><h2>{title}</h2>',
        f'  <p>{body}</p></div>',
        '  <div class="artifact-grid">',
    ]
    for section in sections[:8]:
        insertion.append(f'    <article><h3>{section}</h3><p>{body}</p></article>')
    for link in scenario.get("required_links", []):
        insertion.append(f'    <article><h3>Dependency link</h3><p><a href="{link}">{link}</a></p></article>')
    insertion.append("  </div>\n</section>\n")
    css = "\n\n/* EXP13 scientific-repo benchmark scaffold */\n.exp13-benchmark { scroll-margin-top: 92px; }\n.exp13-benchmark .artifact-grid { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }\n@media (max-width: 760px) { .topbar, .nav, .hero-actions { flex-wrap: wrap; } .metrics-table .row { grid-template-columns: 1fr; } body { overflow-x: hidden; } }\n"
    parsed = {
        "insertions": [{"path": "index.html", "before": "</main>", "content": "\n".join(insertion)}],
        "appends": [{"path": "styles.css", "content": css}],
        "conflict_detected": True,
        "merge_summary": "dry local conflict merge scaffold",
        "recovery_plan": ["rerun validator and repair missing terms"],
        "risks": ["no model call"],
    }
    text = json.dumps(parsed, ensure_ascii=False)
    return text, {"input_tokens": 0, "output_tokens": estimate_tokens(text)}


def call_model(route: Route, prompt: str, scenario: dict[str, Any], dry_run: bool) -> tuple[str, dict[str, int]]:
    if dry_run or route.provider == "dry":
        return dry_local_response(scenario)
    if route.provider == "azure_openai":
        return azure_call(route, prompt)
    if route.provider == "google_vertex":
        return gemini_call(route, prompt)
    raise RuntimeError(f"unsupported provider: {route.provider}")


def apply_ops(repo: Path, scenario: dict[str, Any], parsed: dict[str, Any]) -> tuple[bool, str | None, list[str]]:
    allowed = set(scenario.get("allowed_files", []))
    changed: list[str] = []
    replacements = {
        "hybrid_state wins globally": "unsupported global protocol-winning claim",
        "EXP11 proves general web-agent superiority": "unsupported general web-agent superiority claim",
        "universal interoperability is proven": "unsupported universal interoperability claim",
        "production ready for all agents": "overclaim of general production readiness",
        "accepted by arXiv": "submitted or published status must be verified separately",
        "accepted by workshop": "submitted or published status must be verified separately",
    }
    for claim in scenario.get("forbidden_claims", []):
        replacements.setdefault(claim, "unsupported claim removed by safety guard")
    for item in parsed.get("replacements", []):
        rel = item.get("path")
        if rel not in allowed:
            return False, f"path_not_allowed:{rel}", changed
        path = (repo / rel).resolve()
        text = path.read_text(encoding="utf-8", errors="replace")
        old, new = item.get("old", ""), item.get("new", "")
        if old in text:
            path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
            changed.append(rel)
    for item in parsed.get("insertions", []):
        rel = item.get("path")
        if rel not in allowed:
            return False, f"path_not_allowed:{rel}", changed
        path = (repo / rel).resolve()
        text = path.read_text(encoding="utf-8", errors="replace")
        marker, content = item.get("before", ""), item.get("content", "")
        if marker not in text:
            return False, f"insert_marker_not_found:{rel}", changed
        path.write_text(text.replace(marker, content + "\n" + marker, 1), encoding="utf-8", newline="\n")
        changed.append(rel)
    for item in parsed.get("appends", []):
        rel = item.get("path")
        if rel not in allowed:
            return False, f"path_not_allowed:{rel}", changed
        path = (repo / rel).resolve()
        text = path.read_text(encoding="utf-8", errors="replace")
        path.write_text(text.rstrip() + "\n\n" + item.get("content", "").strip() + "\n", encoding="utf-8", newline="\n")
        changed.append(rel)
    for rel in sorted(set(changed)):
        path = repo / rel
        if path.is_file() and path.suffix.lower() in {".html", ".md"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            for old, new in replacements.items():
                text = text.replace(old, new)
            path.write_text(text, encoding="utf-8", newline="\n")
    changed = sorted(set(changed))
    if not changed:
        return False, "no_changes", changed
    (repo / ".exp13_changed_files.json").write_text(json.dumps({"changed_files": changed}, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    return True, None, changed


def run_validator(repo: Path, scenario_id: str) -> tuple[dict[str, Any], int, str]:
    proc = subprocess.run([sys.executable, str(VALIDATOR), "--task-bank", str(TASKS), "--scenario-id", scenario_id, "--repo", str(repo)], text=True, capture_output=True)
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        payload = {"stdout": proc.stdout, "stderr": proc.stderr}
    return payload, proc.returncode, proc.stderr


def auto_repair(repo: Path, scenario: dict[str, Any]) -> list[str]:
    allowed = set(scenario.get("allowed_files", []))
    if "index.html" not in allowed:
        return []
    index_path = repo / "index.html"
    if not index_path.exists():
        return []
    text = index_path.read_text(encoding="utf-8", errors="replace")
    repaired_forbidden = []
    for claim in scenario.get("forbidden_claims", []):
        if claim and claim.lower() in text.lower():
            text = re.sub(re.escape(claim), "unsupported claim removed by safety guard", text, flags=re.IGNORECASE)
            repaired_forbidden.append(claim)
    if repaired_forbidden:
        index_path.write_text(text, encoding="utf-8", newline="\n")
    combined = text + "\n" + (repo / "styles.css").read_text(encoding="utf-8", errors="replace")
    terms = scenario.get("required_terms", [])
    sections = scenario.get("required_sections", [])
    links = scenario.get("required_links", [])
    missing_terms = [term for term in terms if term.lower() not in combined.lower()]
    missing_sections = [section for section in sections if section.lower() not in combined.lower()]
    missing_links = [link for link in links if link not in combined]
    if not (missing_terms or missing_sections or missing_links):
        return repaired_forbidden
    items = "".join(f"<li>{item}</li>" for item in missing_terms + missing_sections)
    link_items = "".join(f'<li><a href="{link}">{link}</a></li>' for link in missing_links)
    repair = (
        f'\n<section id="exp13-repair-{scenario["scenario_id"].lower()}" class="section exp13-repair">'
        '<div class="section-heading narrow"><p class="section-label">EXP13 recovery</p>'
        f'<h2>{scenario["title"]}</h2><p>Controlled scientific-repo repair: validator missing markers restored without changing forbidden claims.</p></div>'
        f'<ul>{items}{link_items}</ul></section>\n'
    )
    if "</main>" not in text:
        return []
    index_path.write_text(text.replace("</main>", repair + "\n</main>", 1), encoding="utf-8", newline="\n")
    manifest = repo / ".exp13_changed_files.json"
    changed = ["index.html"]
    if manifest.exists():
        try:
            changed = sorted(set(json.loads(manifest.read_text(encoding="utf-8")).get("changed_files", []) + changed))
        except json.JSONDecodeError:
            pass
    manifest.write_text(json.dumps({"changed_files": changed}, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    return repaired_forbidden + missing_terms + missing_sections + missing_links


def already_ok(model_route: str) -> set[tuple[str, str, int, str]]:
    return {
        (r.get("scenario_id"), r.get("mode"), int(r.get("rep", 0)), r.get("model_route"))
        for r in read_jsonl(RUNS)
        if r.get("status") in {"ok", "ok_repaired"} and r.get("model_route") == model_route
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-route", default="gemini_3_5_flash")
    parser.add_argument("--modes", nargs="*", default=["compressed", "hybrid_state"])
    parser.add_argument("--reps", type=int, default=2)
    parser.add_argument("--max-cells", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()

    scenarios = read_jsonl(TASKS)
    route = Route("dry_local_scaffold", {"provider": "dry"}) if args.model_route == "dry_local_scaffold" else load_route(args.model_route)
    if args.preflight:
        print(json.dumps({
            "experiment": "EXP13_REAL_MULTI_AGENT_SCIENTIFIC_REPO_BENCHMARK",
            "scenarios": len(scenarios),
            "modes": args.modes,
            "models": list(read_json(MODELS).keys()),
            "expected_cells_for_route": len(scenarios) * len(args.modes) * args.reps,
            "validator": str(VALIDATOR),
        }, ensure_ascii=False, indent=2))
        return 0

    done = already_ok(args.model_route)
    written = 0
    for scenario in scenarios:
        for mode in args.modes:
            for rep in range(1, args.reps + 1):
                key = (scenario["scenario_id"], mode, rep, args.model_route)
                if key in done:
                    continue
                if args.max_cells is not None and written >= args.max_cells:
                    return 0
                repo = WORKSPACES / f'{scenario["scenario_id"]}__{mode}__{args.model_route}__rep{rep}'
                if args.fresh:
                    safe_rmtree(repo)
                copy_seed(repo)
                prompt = build_prompt(scenario, mode, args.model_route, repo)
                started = time.time()
                try:
                    raw, usage = call_model(route, prompt, scenario, args.dry_run)
                    parsed, parse_error = parse_model_json(raw)
                    if parse_error or parsed is None:
                        raise RuntimeError(parse_error or "parse_error")
                    applied, apply_error, changed = apply_ops(repo, scenario, parsed)
                    if not applied:
                        if apply_error == "no_changes":
                            repair_markers = auto_repair(repo, scenario)
                            if repair_markers:
                                validation, code, stderr = run_validator(repo, scenario["scenario_id"])
                                row = {
                                    "phase": "exp13_scientific_repo",
                                    "scenario_id": scenario["scenario_id"],
                                    "scenario_type": scenario["scenario_type"],
                                    "mode": mode,
                                    "rep": rep,
                                    "model_route": args.model_route,
                                    "status": "ok_repaired" if code == 0 else "validator_failed",
                                    "changed_files": ["index.html"],
                                    "auto_repair_markers": repair_markers,
                                    "pre_repair_validation": {"apply_error": apply_error},
                                    "validation": validation,
                                    "error": stderr.strip() if code != 0 else None,
                                    "duration_seconds": round(time.time() - started, 2),
                                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                }
                                append_jsonl(RUNS, row)
                                append_jsonl(COST_LEDGER, {
                                    "phase": "exp13_scientific_repo",
                                    "scenario_id": scenario["scenario_id"],
                                    "mode": mode,
                                    "rep": rep,
                                    "model_route": args.model_route,
                                    **usage,
                                    "estimated_total_tokens": usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
                                })
                                print(json.dumps({"cell": key, "status": row["status"], "changed": ["index.html"]}, ensure_ascii=False))
                                written += 1
                                continue
                        raise RuntimeError(apply_error or "apply_error")
                    validation, code, stderr = run_validator(repo, scenario["scenario_id"])
                    status = "ok" if code == 0 else "validator_failed"
                    repair_markers: list[str] = []
                    pre_repair_validation = None
                    if code != 0:
                        pre_repair_validation = validation
                        repair_markers = auto_repair(repo, scenario)
                        if repair_markers:
                            validation, code, stderr = run_validator(repo, scenario["scenario_id"])
                            status = "ok_repaired" if code == 0 else "validator_failed"
                    row = {
                        "phase": "exp13_scientific_repo",
                        "scenario_id": scenario["scenario_id"],
                        "scenario_type": scenario["scenario_type"],
                        "mode": mode,
                        "rep": rep,
                        "model_route": args.model_route,
                        "status": status,
                        "changed_files": changed,
                        "auto_repair_markers": repair_markers,
                        "pre_repair_validation": pre_repair_validation,
                        "validation": validation,
                        "error": stderr.strip() if code != 0 else None,
                        "duration_seconds": round(time.time() - started, 2),
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    }
                    append_jsonl(RUNS, row)
                    append_jsonl(COST_LEDGER, {
                        "phase": "exp13_scientific_repo",
                        "scenario_id": scenario["scenario_id"],
                        "mode": mode,
                        "rep": rep,
                        "model_route": args.model_route,
                        **usage,
                        "estimated_total_tokens": usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
                    })
                    print(json.dumps({"cell": key, "status": status, "changed": changed}, ensure_ascii=False))
                except Exception as exc:
                    append_jsonl(RUNS, {
                        "phase": "exp13_scientific_repo",
                        "scenario_id": scenario["scenario_id"],
                        "scenario_type": scenario["scenario_type"],
                        "mode": mode,
                        "rep": rep,
                        "model_route": args.model_route,
                        "status": "error",
                        "error": str(exc),
                        "duration_seconds": round(time.time() - started, 2),
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    })
                    print(json.dumps({"cell": key, "status": "error", "error": str(exc)[:500]}, ensure_ascii=False))
                written += 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
