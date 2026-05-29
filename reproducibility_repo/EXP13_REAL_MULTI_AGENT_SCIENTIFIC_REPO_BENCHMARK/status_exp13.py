from __future__ import annotations

import collections
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "exp13_runs.jsonl"
TASKS = ROOT / "task_bank_exp13_scientific_repo.jsonl"
MODELS = ROOT / "model_registry_exp13.json"


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    rows = read_jsonl(RUNS)
    scenarios = read_jsonl(TASKS)
    models = json.loads(MODELS.read_text(encoding="utf-8"))
    latest = {}
    for row in rows:
        latest[(row.get("scenario_id"), row.get("mode"), row.get("rep"), row.get("model_route"))] = row
    latest_counts = collections.Counter((r.get("model_route"), r.get("mode"), r.get("status")) for r in latest.values())
    historical_counts = collections.Counter((r.get("model_route"), r.get("mode"), r.get("status")) for r in rows)
    by_scenario = collections.Counter((r.get("scenario_type"), r.get("status")) for r in latest.values())
    real_latest = {k: r for k, r in latest.items() if r.get("model_route") in models}
    success_status = {"ok", "ok_repaired"}
    print(json.dumps({
        "experiment": "EXP13_REAL_MULTI_AGENT_SCIENTIFIC_REPO_BENCHMARK",
        "scenarios": len(scenarios),
        "models": list(models.keys()),
        "rows": len(rows),
        "latest_cells": len(latest),
        "ok_latest_cells": sum(1 for r in latest.values() if r.get("status") in success_status),
        "real_model_latest_cells": len(real_latest),
        "real_model_success_cells": sum(1 for r in real_latest.values() if r.get("status") in success_status),
        "expected_full_2reps": len(scenarios) * 2 * len(models) * 2,
        "latest_counts": {str(k): v for k, v in sorted(latest_counts.items())},
        "by_scenario_type": {str(k): v for k, v in sorted(by_scenario.items())},
        "historical_counts": {str(k): v for k, v in sorted(historical_counts.items())},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
