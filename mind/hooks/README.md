# Hook Templates

Merge these into each agent's `<home>/.claude/settings.json`.

- `clock.json`: injects the current time on every prompt and after every Bash call. Required for every agent.
- `startup-injection.sh <Display Name> <memory-dir> <deep-mind-file> <agent-prefix>`: SessionStart; injects
  the agent template (the synced copy beside it) and the agent's deep mind, with the loading order, before
  any tool call. Says when either is missing. Output stays under the harness's ~10 KB cap while the deep
  mind is ≤ ~7.7 KB.
- `memory-budget.py <memory-dir> [event] [agent-prefix]`: PostToolUse (Write|Edit|Bash) and SessionStart;
  the cap check — index size and integrity, frontmatter, deep-mind chars, dense-state lines. Speaks on change.
- `fortress-check.sh [fortress-dir]`: SessionStart; reads `FORTRESS_SYNC` beside it and says whether Fortress
  is missing (always), unsynced, moved, or in sync. Advisory, never blocks.

- `../../bin/whois --hook`: SessionStart, optional; lists the live sessions on this machine with the
  Fortress agent each belongs to. Not synced into the agent's copies (it reads Fortress's `agents/`),
  so it is the one hook that goes quiet, by saying so, when Fortress is absent.

Install with `bin/sync-agent <agent>`: it copies these and the template into `~/.claude/hooks/<agent>/`,
stamps them, and prints the settings block to merge by hand. The agent's settings call the agent's own
copies — never Fortress directly.
