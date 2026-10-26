# Review loops

Read this for running two agent sessions, each in its own repository, that review each other's
work in rounds: setting the loop up, writing and reading its messages, closing a round, and
knowing where the agents must stop for a person.

It covers the loop between two repositories that depend on each other, such as an application
and a tool it drives. One agent reviewing a pull request alone, and a session's own context
files, are other modules' work. TODO(new-skill) Name those modules once they exist.

<!-- Skeleton, 2026-10-21. The rules below are drafts drawn from one loop's records, lessons
L26, L28, L30 and L35 to L38 in ROADMAP.md, and the coordinator's notes of 2026-10-20 and 21.
Each is checked against what shows up next before it's kept, and the other loops and the
published work on agent review are read before the Why section is written. -->

## Rules

Drafts, from one loop's records. Each holds until evidence says otherwise.

1. **Fix the close condition in the round's first message.** Name what has to be true for the
   round to close, and what proves it, before any work. A round with no fixed close drifts.
2. **Commit in advance to how the next verdict is decided:** "our next message says GO unless
   the run shows X". Rounds that did this closed in three messages; before it, one took 37.
3. **Name one writer for every next message.** A status line saying "yours, or ours first" has
   named no one, and both sides wrote the same message.
4. **Read the other side's committed files, not relayed copies.** Each side reads the other's
   default branch, every branch, at the start of a session and before it ends a turn. A relayed
   copy goes stale, and a fetch of one branch hides the rest.
5. **A message counts as sent only once it's marked released,** on a branch the other side
   reads. A draft isn't a message.
6. **Cite every claim as `owner/repo@commit:path:line`,** and paste every hash from a command's
   output, never retype it.
7. **Keep rules about evidence, cut rules about choreography.** Envelopes, digests, ledgers and
   deadlines that never fired cost more than they caught.
8. **Know what the agents can't supply:** time on hardware, a design both sides agree on, and
   acts only the owner can do, such as syncing a fork or giving a release its word. No number
   of messages stands in for them. Ask once, in writing, and say what waits on the answer.
9. **Write the owner's words down once, verbatim,** with who said them and when, and quote them
   where they apply. An answer from one side isn't a settlement.
10. **A change both sides must make is agreed word for word,** and each side checks it against
    the other's tree from a fresh clone.
11. **A new output line ships after the reader that parses it,** never before: the producer
    proposes the wording, the consumer ships its reader, then the producer releases.
12. **A session that stops with work outstanding says what it waits on, and from whom.** An idle
    session doesn't wake itself; the coordinator watches for one that has gone quiet.

TODO(new-skill) Settle the rules' order, merge the overlaps, and cut any the next evidence
doesn't support.

## Mistakes

- **Two sessions writing the same message.** Both read "yours, or ours first" as theirs. Name
  one writer.
- **Reading a relayed copy, or one fetched branch.** A coordinator reported a side idle for an
  hour while it had pushed twice, because its clone fetched only the default branch.
- **Retyping a hash.** One draft's hash had its first 16 characters right and the rest invented.
- **Taking an owner's question as a question.** "I thought we just needed X?" is the
  instruction; reading it as a question cost a round trip.
- **Summing up before taking in every released message.** A digest written before one released
  message was filed couldn't be reproduced by its reader.
- **Releasing a new output shape before the reader exists.** The consumer's completeness check
  fails on the first line it doesn't know.
- TODO(new-skill) The mistakes an AI assistant makes in a loop that these records don't show.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Close condition | The round's first message names what closes it and what proves it | GAP | Add it before any work |
| One writer | Each side's status names who writes the next message, and only one | DRIFT | Name one |
| Direct reading | Each side reads the other's committed files, every branch, at session start | GAP | Read them, not relayed copies |
| Citations | Claims cite `owner/repo@commit:path:line`; hashes pasted from output | DRIFT | Cite and paste |
| Owner's words | Each override is quoted once, with who and when | GAP | Record it verbatim |
| Stalled session | No side idle with work outstanding and nothing saying what it waits on | GAP | Say what it waits on, and from whom |
| TODO(new-skill) | | | |

## Why

### A close condition fixed at the first message

TODO(new-skill) Write this section from the evidence and the published work.

- **The advice:** fix the close condition, and what proves it, in the round's first message.
- **The reason:** rounds without one ran to dozens of messages; with one and a pre-committed
  verdict, three. TODO(new-skill) Cite the records by commit, with the repositories unnamed.
- **What others do, and why:** TODO(new-skill) from the published work on agent review loops.
- **What it costs:** TODO(new-skill)
- **When to choose differently:** TODO(new-skill)

TODO(new-skill) A section like this for each rule that matters.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked TODO(new-skill)
YYYY-MM-DD.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|

## Sources

Every source, with its license and how this module uses it: quoted, adapted with a notice, or
stated in our own words with a link.

| Source | Used for | License |
|---|---|---|
| TODO(new-skill) The loop's own records, by commit, with the repositories unnamed | The rules and mistakes | TODO(new-skill) |
