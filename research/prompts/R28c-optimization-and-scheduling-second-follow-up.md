# RESEARCH RUN R28c: Optimization and scheduling, what R28 and R28b didn’t reach

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 11 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 11 November 2026.

This run informs these categories: optimization-and-scheduling (both modules).

## What this run is for

A second follow-up. R28 built the `optimization-and-scheduling` skill and R28b its
`plan-checking` module (CP-SAT determinism, lexicographic solves, Gurobi 14, benchmark bounds,
Kingman's attribution). Both are filed and checked. This run takes what R28b couldn't find.
Don't repeat their findings; where one has changed since, say so.

## Rules

1. **Primary sources first:** official documentation, specifications and standards bodies, and
   each project's own release notes, changelogs and security advisories. Use secondary sources
   (respected books, well-known engineering blogs, surveys) only where no primary source covers
   the point, and label them "secondary".
2. **Cite every fact:** the URL, the exact sentence you relied on in quotation marks, and a date
   (the source's own date, otherwise the date you read it).
3. **Never guess.** Write "not found" when you can't source something. Write "contested" when good
   sources disagree, and give each side with its source.
4. **Versions:** for every product, give
   - the current stable version and its release date;
   - its end-of-support date;
   - any release due within 6 months, with the expected date and its source.

   Flag anything that reaches end of support within 12 months.
5. **"What we believe" is my current understanding and may be wrong or out of date.** Confirm or
   correct every item, each with a source. The corrections are the most valuable part of this run.
6. **Licences:** for each source, name its licence and say what an Apache-2.0 repository may do
   with it: quote briefly, paraphrase, or adapt its code examples, and with what attribution.
7. **Depth over breadth.** Finish the Priority questions fully. If you run out of room, list the
   rest under "Not covered".

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R28c · FORM: research-result v1
Save as: R28c-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.
```

Then these sections, in this order:

1. **Summary:** at most 15 bullets a professional must know today.
2. **Corrections:** every "What we believe" item that was wrong or out of date, with the right
   fact and its source.
3. **Facts table:** `| # | Fact | Value | Source URL | Exact quote | Date |`
4. **Findings:** one section per question below, numbered to match.
5. **Tools:** `| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |`
6. **Changing in the next 12 months:** deprecations, end-of-support dates, announced breaking
   changes.
7. **Common mistakes,** including those AI coding assistants make in this area, with sources.
8. **Sources and licences:** `| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |`
9. **Not found, contested, not covered.**

## What we believe (confirm or correct each)

- The OR-Tools repository ships official examples for job shop, flexible job shop, RCPSP and
  shift scheduling.
- MiniZinc's Handbook and its benchmark library include scheduling and rostering models.
- OR-Library (J. E. Beasley) is still hosted and free to use for research.
- Due-date quoting trades a longer promise (lost orders, price discounts) against tardiness
  penalties.
- Production-planning "nervousness" is reduced by freezing the near-term schedule.

## Questions

### Priority

1. **Official modelling examples,** with links to the exact files: OR-Tools (`examples/`
   directories for job shop, flow shop, RCPSP, assignment, shift and nurse scheduling),
   MiniZinc (Handbook and MiniZinc Benchmarks), Gurobi's modeling-examples notebooks by topic,
   and Timefold's quickstarts, each with its licence.
2. **People in the plan:** published models of setup times that depend on the sequence and on
   who does the work, cross-training and qualification matrices, and fairness in rostering
   (the nurse-rostering literature), each with the paper's own words.
3. **Re-planning stability:** the nervousness literature, frozen horizons and rolling
   horizons, and how CP-SAT, Gurobi and Timefold support keeping a previous plan (hints,
   pinning, penalties for change).
4. **Benchmark sets:** OR-Library's current location and terms, and the licences or terms of
   use for Taillard's instances, PSPLIB and schedulingbenchmarks.org.

### Standard

5. **Dispatching rules** (EDD, SPT, critical ratio, ATC): sources on when a rule beats a solver
   and when it doesn't.
6. **Due-date quoting:** a sentence from Keskinocak and Tayur (2004) or another primary source
   on the cost of quoting short against long.
7. **Property-based testing of optimisation models:** any published practice (Hypothesis,
   QuickCheck or similar applied to models or planners).
8. **Discrete-event simulation in Python beyond SimPy,** with versions, and CPLEX's guidance on
   containers and CI licences.
9. **A published failure** blamed on a plan that treated workers as deterministic, and
   published guidance on choosing objective weights.
