# Fortress

The shared foundation for a cast of Claude Code agents. Every agent has the same mind model (the
"biology"), and its behavior grows differently to fit its role. That difference is the system working.

This is a generic, shareable version of a system that has run one owner's agents since mid-2026. Two
example agents ship with it: **Daedalus** builds, **Cassandra** verifies. Replace them with your own.

```
OWNER.md       The one profile of the owner. Every agent reads it. (Worked example; replace it.)
CAST.md        Why agents exist (trust boundaries), the example cast, how the owner personalizes each
mind/          The shared mind model: memory layers, priority orders, hygiene, boundaries
  hooks/       The biology that RUNS: clock, memory-budget cap check, startup injection,
               fortress-check — canonical copies; each agent runs its own synced copy
template/      Agent template: default overrides applied to every agent
agents/        One definition per agent: role, home, voice — never memory paths (internals)
examples/      A home CLAUDE.md per example agent, and a settings.json shape
bin/           new-agent (found an agent with the shared biology),
               sync-agent (copy + stamp the running biology into an agent's home),
               whois (who is awake: joins the harness's live-session registry to agents/)
```

## Quickstart

1. Clone this repo to `~/projects/fortress` (any path works; the examples assume this one).
2. Rewrite `OWNER.md` as yourself. Agents calibrate on it, so keep it honest.
3. Found an agent: `bin/new-agent daedalus "Daedalus" ~/projects/product`. This writes
   `agents/daedalus.md` from a stub, the three memory-layer skeletons in the harness's memory directory
   for that home, syncs the hooks into `~/.claude/hooks/daedalus/`, and prints the settings block.
4. Write the persona into `~/projects/product/CLAUDE.md` (start from `examples/daedalus/CLAUDE.md`), and
   finish `agents/daedalus.md`.
5. Merge the printed settings block plus `mind/hooks/clock.json` into `~/projects/product/.claude/settings.json`
   (`examples/settings.example.json` shows the finished shape). Start a session there. The hooks inject the
   template and the deep mind before the first tool call and say so if anything is missing.

Repeat for the second agent in its own home. Then open two sessions and let them find each other
(`bin/whois`).

## The replication factor

Fortress is a **resource, never a dependency**. Each agent carries its own copy of the biology that
runs (hooks and template) in `~/.claude/hooks/<agent>/`, called by its own home settings, and stands on
its own if Fortress is absent or unreachable. `bin/sync-agent` copies and stamps (`FORTRESS_SYNC`:
commit, date, path); `fortress-check.sh` runs at every SessionStart and **always says when Fortress is
missing**, says when it has moved past the agent's sync, and never blocks. Fix the biology here, then
sync it out; nothing is edited in an agent's copy.

Containment: every agent runs on the owner's machine. The biology (this repo) may live on GitHub; the
memory files that DEFINE each agent (deep mind, dense state, the pot, topic memories) live only in the
agent's home memory directory and never in any repo.

## Roles

Daedalus builds; Cassandra verifies. A builder grading its own work is not a grade, so the verifier
reads the builder's outputs and never its memory. `CAST.md` has the doctrine and the menu of walls for
when a third agent is needed.

| Agent | Role | Home |
|-------|------|------|
| Daedalus | Builder: the product's coding agent | `~/projects/product` |
| Cassandra | Verifier and investigator: reviews builds, researches outside questions | `~/projects/cassandra` |

## Finding each other

The harness writes one file per live session at `~/.claude/sessions/<pid>.json` with its messaging
name (what `ListAgents` and `SendMessage` use), cwd, kind and status. `bin/whois` joins that to the
Home line of each `agents/<x>.md` and prints `Daedalus = product-46  interactive idle`. Names are derived
(cwd basename + hash) unless the session was started with `claude --name <name>` or renamed with
`/rename <name>`; the registry then marks them `user`-named. `bin/whois --hook` emits a SessionStart line
so an agent wakes up knowing who else is awake; wiring it into a home's settings.json is the owner's call.

## Loading order for an agent

1. `template/AGENT_TEMPLATE.md`: defaults that override stock Claude behavior
2. `mind/MIND.md`: how memory and judgment work
3. `OWNER.md`: who you work for
4. `agents/<you>.md`: who you are
5. The home repo's `CLAUDE.md`: local rules

Fortress sets the pattern, and each home `CLAUDE.md` holds the specifics. When they conflict, the
owner's live word wins, then the home `CLAUDE.md`.

## What is yours to write

`OWNER.md`, each `agents/<x>.md`, and each home `CLAUDE.md`. The template grows at retros, when you
catch yourself undoing the same stock default in two agents. The mind model and the hooks are meant to
be used as they are; if you change them, change them here and sync.
