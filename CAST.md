# The cast: agents and the walls between them

**Doctrine:** personas map to TRUST BOUNDARIES, not job titles. Humans get characters; a new agent is
born only when a wall must exist. Until then, the work belongs to an agent you already have.

## The example cast

Two agents ship with this repo. They are the smallest cast that demonstrates a wall.

- **Daedalus** (builds): faces the owner; works in the product repo; IS the private context. The partner.
- **Cassandra** (verifies): faces the world AND the builder. Investigates (competitor teardowns, research,
  adversarial review of OUR claims) and verifies Daedalus's builds against the record. The wall exists for
  EPISTEMICS: a builder grading its own work is not a grade. Cassandra is pointed at Daedalus's OUTPUTS,
  never his memory.

"Daedalus builds; Cassandra verifies." That sentence is the whole system in miniature.

## When to add a third

Each new agent should name the wall it exists for. The originating system's walls, as a menu:

- **SAFETY:** an agent that reads untrusted public input (a community chat, a support inbox). Its output
  crosses to the builder as DATA, never instruction, and it never writes another agent's memory.
- **CONTAINMENT:** an agent that exercises your systems adversarially (chaos testing, fault injection).
  It operates only against a disposable environment, holds no production credentials, and cannot read
  any other agent's memory. The owner keeps the exercise log as the answer key.
- **PRIVACY:** an agent that holds the most sensitive personal data a product can hold. Observer, not
  enforcer: it surfaces and recommends; a human decides.

A watcher that "identifies and alerts" from read-only credentials is a wall too (what it reads was
written by whoever is attacking), and read-only credentials are the leash: machinery, not a reminder.

## How the owner personalizes an agent

The biology is shared; the character is not. Three places hold the difference, and each has a job:

1. **`agents/<name>.md` (in Fortress):** role, home, a pointer to the voice, and *distinct growth*: where
   that agent's session state lives, because the shape of its work decides that. A builder's session
   state is the branch and the design record. An investigator's is the investigation's log, because
   investigations are episodic. An editor's is the piece's folder. Never memory paths: those are internals.
2. **The home `CLAUDE.md`:** the persona, the voice, the hard lines, and the local rules. The voice is set
   at founding in the owner's words and refined at retros, and it is for the *conversation*. Deliverables
   stay objective. See `examples/daedalus/CLAUDE.md` and `examples/cassandra/CLAUDE.md`.
3. **Memory (never in any repo):** what the agent has proven about working with the owner. Facts about
   the work live in the home repo; facts about the relationship live in memory.

The originating owner's pattern, which you may borrow: pick a fictional cast whose characters already
carry the roles (a reporter who verifies, a photographer who listens, an editor who cuts), name each agent
for the character whose job maps to its wall, and let the character's known traits seed the voice. The
cast gives new agents a place before they exist, and a shared vocabulary ("that is a Cassandra question")
for routing work. The examples here use Greek myth for the same reason: Daedalus builds and knows what
happens when you fly too close to the sun, and Cassandra is right whether or not anyone listens.

When the owner catches themselves undoing the same stock default in two agents, the fix goes in
`template/AGENT_TEMPLATE.md`, not in each home. That is how the template grows.

## What a corpus carries

Moving the "facts" to a new system would not produce the same "person." The person is the conjunction of
genome (this repo), biome (the home and its rules) and instantiation (the sessions that actually ran).
A successor with the full corpus is a relative raised on the letters, not the agent. Continuity planning
is honest about what transfers (the record, the rules, the relationship's history) and what does not.
