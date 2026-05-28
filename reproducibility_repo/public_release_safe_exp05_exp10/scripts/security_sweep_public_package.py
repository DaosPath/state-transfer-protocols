from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent

SECRET_PATTERNS = {
    "google_api_key": re.compile(r"AIza[0-9A-Za-z_\-]{20,}"),
    "azure_key_literal": re.compile(r"[A-Za-z0-9]{80,}"),
    "bearer_token": re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]{20,}", re.I),
    "openai_sk": re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    "generic_api_key_assignment": re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*[\"'][A-Za-z0-9_\-]{20,}[\"']"),
}

SUSPICIOUS_EXTENSIONS = {
    ".env",
    ".key",
    ".pem",
    ".p12",
    ".pfx",
    ".sqlite",
    ".db",
    ".wal",
    ".shm",
}

SKIP_DIRS = {
    ".git",
    ".venv",
    ".uv-cache",
    "__pycache__",
}


def is_binary(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:2048]
    except OSError:
        return True
    return b"\0" in chunk


def main() -> int:
    findings = []
    suspicious_files = []
    scanned = 0
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in SUSPICIOUS_EXTENSIONS:
            suspicious_files.append(rel)
        if is_binary(path):
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(text):
                snippet = match.group(0)
                redacted = snippet[:8] + "...REDACTED..." if len(snippet) > 8 else "...REDACTED..."
                findings.append(
                    {
                        "file": rel,
                        "pattern": name,
                        "line": text.count("\n", 0, match.start()) + 1,
                        "snippet": redacted,
                    }
                )

    report = {
        "root": str(ROOT),
        "files_scanned_text": scanned,
        "secret_findings": findings,
        "suspicious_files": suspicious_files,
        "pass": not findings,
        "note": "Suspicious files are not necessarily leaks; review before public release.",
    }
    out = ROOT / "SECURITY_SWEEP_REPORT.md"
    lines = [
        "# Security Sweep Report",
        "",
        f"- Text files scanned: {scanned}",
        f"- Secret findings: {len(findings)}",
        f"- Suspicious files: {len(suspicious_files)}",
        f"- Pass: {report['pass']}",
        "",
        "## Secret Findings",
        "",
    ]
    if findings:
        for item in findings:
            lines.append(f"- `{item['file']}` line {item['line']} pattern `{item['pattern']}`: `{item['snippet']}`")
    else:
        lines.append("None.")
    lines += ["", "## Suspicious Files", ""]
    if suspicious_files:
        for item in suspicious_files:
            lines.append(f"- `{item}`")
    else:
        lines.append("None.")
    lines += ["", "## JSON", "", "```json", json.dumps(report, indent=2, ensure_ascii=False), "```", ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

