# RESEARCH RUN R28: Optimization and scheduling, with the people in the plan

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 11 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 11 November 2026.

This run informs these categories: optimization-and-scheduling, and human-factors where a plan
meets the people who carry it out.

## What this run is for

A skill that helps an agent write, review and audit code that plans work: solvers and their
models, schedules, lead-time quotes from backlog and capacity, line and cell assignment, shift and
crew rosters. The owner's own systems are of this kind: a manufacturer's lead-time board that
divides open orders by a line's daily capacity, and schedulers that assign work to cells and
people. The skill must make an agent good at three things: choosing and using a solver correctly,
checking that a plan is right without trusting the solver that made it, and keeping real people's
limits in the model rather than planning them as machines.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R28 · FORM: research-result v1
Save as: R28-RESULT.md
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

- Google OR-Tools (v9.x) CP-SAT is the leading open-source constraint solver for scheduling, and
  its Python API added PEP 8 (snake_case) method names alongside the old CamelCase ones.
- HiGHS is a leading open-source LP and MIP solver, and SciPy's `linprog` and `milp` use it.
- SCIP is now under the Apache 2.0 licence.
- Timefold Solver succeeds OptaPlanner, as a fork by its original team in 2023.
- Pyomo and PuLP are the common Python modelling layers, and PuLP ships the CBC solver.
- ISO 10075 (parts 1 to 3) covers mental workload, and the UK HSE's HSG256 covers shift work,
  with its Fatigue and Risk Index as a tool.
- Little's law (L = λW) holds for any stable system, and Kingman's approximation shows waiting
  time growing without bound as utilization approaches 100%.
- Wright's learning curve (1936) is the standard model of learning, and learning-forgetting
  models extend it to interrupted work.
- Hopp and Spearman's *Factory Physics* is the standard reference for lead time, WIP and
  capacity in manufacturing.

## Questions

### Priority

1. **Solvers today.** For each of OR-Tools (CP-SAT and its routing and linear wrappers), HiGHS,
   SCIP, CBC, Gurobi, CPLEX, Pyomo, PuLP, Timefold and MiniZinc: the current version and release
   date, the licence, the languages it supports, and what kind of problem it is for (LP, MIP,
   constraint programming, routing, scheduling). Which to choose for which problem, from the
   projects' own documentation and published benchmarks (for example Mittelmann's), with each
   benchmark's date.
2. **Modelling scheduling problems,** from the solvers' official documentation and examples:
   - job shop, flow shop, resource-constrained project scheduling, line and cell assignment, and
     crew or shift rostering (the official examples for each, with links);
   - interval variables, no-overlap and cumulative constraints, and time windows;
   - hard against soft constraints, penalties and weights, lexicographic and multi-objective
     models, and how to choose weights without one term silently dominating;
   - business rules as data rather than code;
   - diagnosing an infeasible model (CP-SAT's assumptions and sufficient sets, an LP or MIP's IIS);
   - time limits, the optimality gap, and what a result must report when it stops at a limit.
3. **People in the plan,** from peer-reviewed research and standards; label any unsourced
   heuristic as a heuristic:
   - fatigue and shift design: ISO 10075, HSE HSG256 and its Fatigue and Risk Index, rotation
     direction and speed, breaks, time-of-day effects on error;
   - learning and forgetting curves, and setup or changeover time that depends on who does it
     and in what order;
   - skills, cross-training and who is qualified for what;
   - preferences and fairness in rostering (the nurse-rostering literature and others);
   - planning below full utilization: Little's law, Kingman's approximation, variability buffers;
   - published cases of optimized plans that failed on the shop floor because they treated people
     as deterministic, and what fixed them.
4. **Quoting lead times from backlog and capacity:**
   - the factory-physics view of lead time, WIP and throughput; CONWIP;
   - the due-date quoting literature: quoting from workload, safety margins, and what quoting
     short costs against quoting long;
   - capacity that differs by product or is shared between products (equivalent units, shared
     resources), and how lead-time systems handle it;
   - holidays, shutdowns and calendars in date arithmetic.
5. **Checking a plan without trusting the solver,** from published practice:
   - validating a solution's feasibility with an independent checker;
   - standard instance libraries with known optima (OR-Library, PSPLIB, Taillard's instances,
     NRP and nurse-rostering sets) as test oracles;
   - property-based tests for models; determinism (seeds, worker counts) and regression on
     objective values;
   - simulation (discrete-event) to test a plan against variability before it ships;
   - explaining a schedule to the people who must follow it.

### Standard

6. **When a solver is too slow:** dispatching rules (EDD, SPT, critical ratio), local search and
   metaheuristics, Timefold's approach, and warm starts.
7. **Re-planning:** incremental re-solving, keeping a schedule stable when re-solved
   (nervousness), and freezing the near term.
8. **Running a solver in a service:** time limits, cancellation, memory, multi-threading defaults,
   and licences for commercial solvers in containers and CI.
9. **Common mistakes,** including those AI coding assistants make when writing optimization models
   and schedulers, with sources.
