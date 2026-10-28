#!/usr/bin/env python3
"""Memory budget and structure check for one agent's Claude memory directory.

Silent when healthy. When something would degrade a future session's load
(truncated index, oversized injection, broken frontmatter, dangling or
orphaned index entries), prints one hook-output block naming each problem.
If the check itself fails, it says so -- a silent gate is worse than none.

Usage: memory-budget.py <memory-dir> <hook-event-name> <agent-prefix>
  agent-prefix names the layer files: <prefix>_deep_mind.md,
  <prefix>_dense_state.md, <prefix>_dense_state_archive_YYYY-MM.md.
  Required: a missing prefix would silently skip the layer checks (a missing prefix was once silently skipped).
Designed for PostToolUse on Write|Edit|Bash: Bash matters because memory is
often edited with sed, which a Write|Edit matcher would never see.

Fortress canonical copy: mind/hooks/memory-budget.py. Each agent runs its
OWN synced copy (the replication factor, 2026-10-02); fix it here, then
bin/sync-agent carries the fix to every agent.
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # the line-shape check below still runs without it
    yaml = None

# The harness loads the index's first 200 lines OR 25 KB, whichever comes first.
INDEX_WARN_LINES, INDEX_HARD_LINES = 160, 200
INDEX_WARN_BYTES, INDEX_HARD_BYTES = 20_000, 25_000
INDEX_MAX_LINE_CHARS = 250
# SessionStart hook output caps at 10,000 chars. The startup injection
# carries a ~500-char prefix AND the agent template (~1,800 chars) alongside
# the deep mind, so the deep mind itself is lost past ~7,700.
DEEP_WARN_CHARS, DEEP_HARD_CHARS = 6_000, 7_700
DENSE_WARN_LINES, DENSE_HARD_LINES = 280, 300

STATE_DIR = Path.home() / ".claude" / "hooks" / "state"

INDEX = "MEMORY.md"


def layer_names(prefix: str) -> tuple[str, str, re.Pattern[str]]:
    return (
        f"{prefix}_deep_mind.md",
        f"{prefix}_dense_state.md",
        # Monthly day-log archives are grep-only by design and deliberately unindexed.
        re.compile(rf"^{re.escape(prefix)}_dense_state_archive_\d{{4}}-\d{{2}}\.md$"),
    )


def frontmatter_issues(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return [f"{path.name}: no frontmatter"]
    end = text.find("\n---", 4)
    if end == -1:
        return [f"{path.name}: frontmatter never closes"]
    block = text[4:end]
    issues: list[str] = []
    if yaml is not None:
        try:
            data = yaml.safe_load(block)
        except Exception as exc:  # noqa: BLE001 - report, never raise, inside a hook
            return [f"{path.name}: frontmatter is not valid YAML ({exc.__class__.__name__})"]
        if not isinstance(data, dict):
            return [f"{path.name}: frontmatter is not a mapping"]
        for key in ("name", "description"):
            if key not in data:
                issues.append(f"{path.name}: frontmatter lacks {key}")
    else:
        for key in ("name:", "description:"):
            if key not in block:
                issues.append(f"{path.name}: frontmatter lacks {key.rstrip(':')}")
    return issues


def check(d: Path, prefix: str) -> list[str]:
    deep, dense, unindexed_ok = layer_names(prefix)
    issues: list[str] = []
    index = d / INDEX
    if not index.exists():
        return [f"{INDEX} is missing from {d}"]
    index_text = index.read_text(encoding="utf-8", errors="replace")
    lines = index_text.splitlines()
    n_lines, n_bytes = len(lines), len(index_text.encode("utf-8"))
    if n_lines >= INDEX_HARD_LINES or n_bytes >= INDEX_HARD_BYTES:
        issues.append(f"{INDEX} {n_lines} lines / {n_bytes} bytes: the harness TRUNCATES past 200 lines or 25 KB")
    elif n_lines >= INDEX_WARN_LINES or n_bytes >= INDEX_WARN_BYTES:
        issues.append(f"{INDEX} {n_lines} lines / {n_bytes} bytes: nearing the 200-line / 25 KB load cap")
    for i, line in enumerate(lines, 1):
        if len(line) > INDEX_MAX_LINE_CHARS:
            issues.append(f"{INDEX} line {i} is {len(line)} chars: one line per memory, hooks only")

    linked = set(re.findall(r"\]\(([^)]+\.md)\)", index_text))
    for target in sorted(linked):
        if not (d / target).exists():
            issues.append(f"{INDEX} links to {target}, which does not exist")
    for path in sorted(d.glob("*.md")):
        if path.name == INDEX or unindexed_ok.match(path.name):
            continue
        if path.name not in linked:
            issues.append(f"{path.name} is not in {INDEX} (orphan: never recalled)")
        issues.extend(frontmatter_issues(path))

    deep_path = d / deep
    if deep_path.exists():
        n = len(deep_path.read_text(encoding="utf-8", errors="replace"))
        if n >= DEEP_HARD_CHARS:
            issues.append(f"{deep} {n} chars: PAST the SessionStart injection cap ({DEEP_HARD_CHARS}); the voice arrives truncated")
        elif n >= DEEP_WARN_CHARS:
            issues.append(f"{deep} {n} chars: nearing the injection cap ({DEEP_HARD_CHARS})")
    dense_path = d / dense
    if dense_path.exists():
        n = len(dense_path.read_text(encoding="utf-8", errors="replace").splitlines())
        if n > DENSE_HARD_LINES:
            issues.append(f"{dense} {n} lines: PAST its {DENSE_HARD_LINES}-line cap; boundary trim overdue")
        elif n >= DENSE_WARN_LINES:
            issues.append(f"{dense} {n}/{DENSE_HARD_LINES} lines: boundary trim due")
    return issues


def emit(event: str, text: str) -> None:
    if event == "SessionStart":
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text}}))
    elif event == "PostToolUse":
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": text}}))
    else:
        print(text)


def main() -> None:
    event = sys.argv[2] if len(sys.argv) > 2 else "PostToolUse"
    if len(sys.argv) < 4:
        emit(event, "[memory budget] usage: memory-budget.py <memory-dir> <hook-event-name> <agent-prefix> — prefix is required")
        return
    d = Path(sys.argv[1]).expanduser()
    prefix = sys.argv[3]
    try:
        if not d.is_dir():
            emit(event, f"[memory budget] memory dir missing: {d}")
            return
        issues = check(d, prefix)
        # Speak on change, not every call: a PostToolUse that repeats the same
        # warning after every Bash call is noise; SessionStart always speaks.
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        key = re.sub(r"[^A-Za-z0-9]+", "-", str(d)).strip("-")
        last = STATE_DIR / f"{key}.last"
        current = "\n".join(issues)
        previous = last.read_text(encoding="utf-8") if last.exists() else None
        last.write_text(current, encoding="utf-8")
        if not issues:
            if previous and event == "PostToolUse":
                emit(event, "[memory budget] clear")
            return
        if event == "PostToolUse" and previous == current:
            return
        emit(event, "[memory budget] " + "; ".join(issues))
    except Exception as exc:  # noqa: BLE001 - a silent gate is worse than none
        event = sys.argv[2] if len(sys.argv) > 2 else "PostToolUse"
        emit(event, f"[memory budget] check FAILED: {exc.__class__.__name__}: {exc}")


if __name__ == "__main__":
    main()
