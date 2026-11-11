# RESEARCH RUN R28b: Optimization and scheduling, the questions R28 didn’t reach

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 11 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 11 November 2026.

This run informs these categories: optimization-and-scheduling.

## What this run is for

A follow-up to R28 (filed 11 November 2026), which built the shipped
`optimization-and-scheduling` skill. That run listed what it couldn't cover; this one finds it.
Don't repeat R28's findings; where one has changed since (versions move fast here), say so.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R28b · FORM: research-result v1
Save as: R28b-RESULT.md
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

- CP-SAT has a deterministic mode for multi-worker runs, set through a solver parameter.
- CP-SAT and Gurobi both support lexicographic (hierarchical) multi-objective solves.
- OR-Library, PSPLIB, Taillard's instances and the nurse-rostering benchmark sets publish
  instances with known optima or best-known solutions.
- SimPy is the common Python discrete-event simulation library.
- Kingman's 1961 approximation for the G/G/1 queue gives waiting time growing as ρ/(1−ρ).

## Questions

### Priority

1. **Official modelling examples,** with links, for flow shop, resource-constrained project
   scheduling, cell or line assignment, and nurse or shift rostering, in OR-Tools, Timefold,
   MiniZinc and Gurobi.
2. **Multi-objective solves:** the lexicographic and weighted APIs in CP-SAT and Gurobi, with
   versions, and published guidance on choosing weights.
3. **Test oracles for planners:** OR-Library, PSPLIB, Taillard and the nurse-rostering sets
   (where each lives, its licence, and what it gives), property-based testing of models, and
   CP-SAT's deterministic mode for reproducible tests.
4. **People in the plan, the parts R28 didn't source:** setup times that depend on who and in
   what order, cross-training and qualification models, fairness in rostering (the
   nurse-rostering literature), and Kingman (1961) from the primary paper.
5. **Quoting due dates:** the costs of quoting short against long, from the due-date management
   literature (for example Keskinocak and Tayur, 2004), with exact quotes.

### Standard

6. **Discrete-event simulation** to test a plan against variability: SimPy and others, with
   versions.
7. **Dispatching rules** (EDD, SPT, critical ratio) and when they beat a solver.
8. **Re-planning stability:** the nervousness literature, and freezing the near term.
9. **Commercial solver licences** in containers and CI (Gurobi, CPLEX), from the vendors.
10. **A published failure** blamed on a plan that treated workers as deterministic; and the
    correct citations for Wiers (2009) and Ivert (2012) on shop floors ignoring APS schedules.
