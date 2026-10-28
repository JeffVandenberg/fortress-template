#!/usr/bin/env bash
# SessionStart injection for one agent: the agent template (defaults that
# override stock Claude behaviour) and the agent's deep mind, in that order,
# before any tool call — then the loading order the agent follows itself.
#
# Usage: startup-injection.sh <agent-display-name> <memory-dir> <deep-mind-file> <agent-prefix>
#   The template is read from THIS script's own directory (the agent's synced
#   copy), never from Fortress: the agent stands on its own.
#
# Output is capped by the harness near 10,000 chars; the template (~1.8 KB)
# and this prefix (~0.5 KB) leave the deep mind ~7.7 KB (memory-budget.py
# warns at 6 KB). Fails soft: anything missing is SAID, never fatal.
#
# Fortress canonical copy: mind/hooks/startup-injection.sh (replication
# factor, 2026-10-02). Each agent runs its own synced copy.
set -u
name="${1:-Agent}"
memdir="${2:?memory dir}"
deep="${3:?deep mind file}"
prefix="${4:-agent}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
template="$here/AGENT_TEMPLATE.md"
upper="$(printf '%s' "$name" | tr '[:lower:]' '[:upper:]')"

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
    printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"HOOK OUTPUT FAILED in %s: neither jq nor python3 could encode its output, so its content is missing from this session. Say so to the owner before anything else."}}\n' "startup-injection.sh"
  fi
}

{
  printf '%s STARTUP ORDER (hook-enforced). Two things arrive here before any tool call: the agent template (defaults the owner wants in every agent) and layer three, the deep mind. Read both as the voice, not as reference. THEN, before git, date, or anything checkable: Read the top of the dense state (register, hard rules, latest session) at %s/%s_dense_state.md in ONE call, by itself. THEN, if Fortress is present (its own hook says so; hooks run in no fixed order, so look for that line anywhere in your startup context), one cat of mind/MIND.md, OWNER.md and agents/<you>.md from it. If Fortress is missing, say so and go on without them. Facts come last. Persona before facts.\n\n' "$upper" "$memdir" "$prefix"
  if [ -r "$template" ]; then
    printf -- '----- AGENT TEMPLATE -----\n'
    cat "$template"
    printf '\n----- DEEP MIND -----\n'
  else
    printf 'AGENT TEMPLATE MISSING at %s (expected the synced copy beside this hook; run Fortress bin/sync-agent).\n\n----- DEEP MIND -----\n' "$template"
  fi
  if [ -r "$memdir/$deep" ]; then
    cat "$memdir/$deep"
  else
    printf 'DEEP MIND MISSING at %s/%s — this session starts without layer three. Say so to the owner before anything else.\n' "$memdir" "$deep"
  fi
} | emit
