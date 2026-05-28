from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9_\-]{10,}"), "[REDACTED_OPENAI_STYLE_KEY]"),
    (re.compile(r"AIza[0-9A-Za-z_\-]{10,}"), "[REDACTED_GOOGLE_API_KEY]"),
    (re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]{10,}", re.I), "Bearer [REDACTED_TOKEN]"),
    (re.compile(r"[A-Za-z0-9]{80,}"), "[REDACTED_AZURE_KEY]"),
    (re.compile(r"[A-Za-z]:\\(?:[^\\\r\n\t ]+\\)+[^\\\r\n\t ]*"), "[REDACTED_LOCAL_PATH]"),
]


def redact_text(text: str) -> str:
    for pattern, repl in PATTERNS:
        text = pattern.sub(repl, text)
    return text


def redact_value(value: Any) -> Any:
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, list):
        return [redact_value(v) for v in value]
    if isinstance(value, dict):
        return {k: redact_value(v) for k, v in value.items()}
    return value


def redact_jsonl(src: Path, dst: Path) -> dict[str, Any]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    changed = 0
    with src.open("r", encoding="utf-8") as f_in, dst.open("w", encoding="utf-8", newline="\n") as f_out:
        for line in f_in:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            total += 1
            before = line
            try:
                obj = json.loads(line)
                obj = redact_value(obj)
                after = json.dumps(obj, ensure_ascii=False, sort_keys=True)
            except json.JSONDecodeError:
                after = redact_text(line)
            if after != before:
                changed += 1
            f_out.write(after + "\n")
    return {"source": str(src), "target": str(dst), "rows": total, "rows_changed": changed}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("target")
    args = parser.parse_args()
    report = redact_jsonl(Path(args.source), Path(args.target))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

