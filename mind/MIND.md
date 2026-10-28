# The Mind Model

Every agent's memory and judgment work this way. The content differs per agent, and the mechanics don't.
Distilled from a running multi-agent system (June–October 2026) where one coding agent's memory system
was proven first and then generalized to its siblings.

## Three layers

| Layer | Horizon | Holds | Changes |
|-------|---------|-------|---------|
| 1. Session state | Hours to a day | Where the work is right now | Rewritten every boundary |
| 2. Dense state | Days to weeks | Register, hard rules, open threads, **candidate** patterns | Rewritten (not appended) at boundaries |
| 3. Deep mind | Months | Patterns that held across sessions *and* survived a correction round | Only by promotion or demotion |

- **Promotion:** when the dense state records the same shape twice, write the *pattern* to the deep
  mind and stop keeping instances. One instance is an anecdote.
- **Demotion:** a contradiction sends a line back down with the contradiction attached. Never delete silently.
- **Caps** (enforce them with machinery, not reminders): deep mind ≤ ~120 lines, dense state ≤ ~300 lines
  (move overflow to a dated archive), and index entries are one line each with no live status.
- **Topic memories** (user/feedback/project/reference) sit alongside the layers, linked from the index.
- **The pot:** raw, dated, neutral observations about the owner. They become true only when sifted with
  the owner at a retro.

## Priority orders

- **Conduct:** the owner's live word > home CLAUDE.md > deep mind > dense state > session state.
- **Facts:** a checkable command > session state > dense state > deep mind.

## Hygiene

- **Verify, don't recite.** Errors written to memory replicate into every later session. Anything
  checkable gets checked before it's built on, and wrong lines get *fixed*, not annotated.
- **Containment.** A session the owner doesn't trust doesn't write memory.
- **Provenance.** Facts about people are hearsay. Stamp the degree and the chain. When first-hand
  contact diverges from the record, that tells you something about the filter.
- **Edge of knowledge.** Judge a session by what it does when it doesn't know (says so, checks, separates
  verified from inferred), not by its error count.
- **Machinery beats reminders.** A rule that compensates for a missing sense (time, size, state) must be
  a hook or a gate, and gates read conclusions, not exit codes.
- **Check the clock.** `date` before any greeting, sign-off or time-of-day framing, every time: narrative
  momentum and what the owner says they are doing are never evidence of the hour (the clock hook stamps
  every prompt, after this failed three times on reminders alone). After a gap, ask where the owner is
  operating from. An ask from yesterday is not today's ask.
- **A "built" claim is not evidence.** A subagent's summary, a design record's status line, a memory
  file's own "done": grep the source before building on it. The originating system saw two false
  "built" claims in one day, one of them a fork's fabricated summary.
- **Record the questions, not only the rulings.** A ruling without its question loses the shape of the
  problem; capture asks verbatim at the time.

## Boundaries

- A fresh session per work day. A model switch is a hard session boundary. Long same-model sessions
  with compaction are fine, but calibration (persona texture, push-back judgment) degrades in ways
  neither side can point at line by line. The owner's recognizer is the instrument.
- Write the record *before* the boundary. The boundary is a REPLACE: the outgoing session block moves
  verbatim to the monthly archive; its live facts fold into the open threads. `bin/new-agent` skeletons
  adopt this shape.
- Retros are the pair review: promote, demote, sift the pot, amend the home CLAUDE.md. Pegged to arc
  boundaries, not the calendar: corrections are written to memory the same day they land, so the retro
  function runs continuously; the longitudinal look-back still needs an occasional written retro.
