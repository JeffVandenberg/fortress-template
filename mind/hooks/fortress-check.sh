#!/usr/bin/env bash
# SessionStart: is Fortress here, and has it moved since this agent's copies
# were synced? Advisory only; never blocks, never errors. ALWAYS says when
# Fortress is missing (2026-10-02): the agent then runs on its own
# copies — the replication factor — and the owner should know it is.
#
# Usage: fortress-check.sh [fortress-dir]
#   The stamp FORTRESS_SYNC sits beside this script (written by bin/sync-agent):
#   line 1 = Fortress commit hash, line 2 = sync date, line 3 = Fortress path.
set -u
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
stamp="$here/FORTRESS_SYNC"
fortress="${1:-}"
synced_hash=""; synced_at="never"
if [ -r "$stamp" ]; then
  synced_hash="$(sed -n 1p "$stamp")"
  synced_at="$(sed -n 2p "$stamp")"
  [ -z "$fortress" ] && fortress="$(sed -n 3p "$stamp")"
fi
[ -z "$fortress" ] && fortress="$HOME/projects/fortress"

# One SessionStart hook line from stdin, NEVER silent (2026-10-03: a jq
# failure used to exit 0 with 0 bytes, under the settings guard's radar). jq
# first, python3 second (memory-budget.py already needs it), and if both fail a
# hand-built line that names the failure so the session says so.
emit() {
  local text out
  text="$(cat)"
  if out="$(printf '%s' "$text" | jq -Rs '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:.}}' 2>/dev/null)" && [ -n "$out" ]; then
    printf '%s\n' "$out"
  elif out="$(printf '%s' "$text" | python3 -c 'import json,sys; print(json.dumps({"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":sys.stdin.read()}}))' 2>/dev/null)" && [ -n "$out" ]; then
    printf '%s\n' "$out"
  else
    printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"HOOK OUTPUT FAILED in %s: neither jq nor python3 could encode its output, so its content is missing from this session. Say so to the owner before anything else."}}\n' "fortress-check.sh"
  fi
}
say() { printf -- '----- FORTRESS -----\n%s' "$1" | emit; }

if [ ! -d "$fortress" ]; then
  say "FORTRESS MISSING at $fortress. This agent is running on its own synced copies (synced $synced_at from ${synced_hash:-unknown}). Say so to the owner in your first message."
  exit 0
fi
head="$(git -C "$fortress" rev-parse HEAD 2>/dev/null || true)"
if [ -z "$head" ]; then
  say "FORTRESS PRESENT at $fortress but not a git checkout; cannot tell whether this agent's copies (synced $synced_at) are current."
  exit 0
fi
if [ -z "$synced_hash" ]; then
  say "FORTRESS PRESENT at $fortress (HEAD ${head:0:7}); this agent has NEVER been synced from it — run bin/sync-agent."
  exit 0
fi
case "$synced_hash" in *-dirty)
  say "FORTRESS COPIES ARE FROM A DIRTY TREE: synced $synced_at from ${synced_hash:0:7} with uncommitted changes in Fortress. Commit there, then re-sync."
  exit 0;;
esac
if [ "$head" != "$synced_hash" ]; then
  behind="$(git -C "$fortress" rev-list --count "$synced_hash..$head" 2>/dev/null || echo '?')"
  say "FORTRESS HAS MOVED: $behind commit(s) since this agent's sync ($synced_at, ${synced_hash:0:7} → ${head:0:7}). Run bin/sync-agent when convenient; the copies here still work."
  exit 0
fi
say "Fortress in sync (${head:0:7}, synced $synced_at)."
