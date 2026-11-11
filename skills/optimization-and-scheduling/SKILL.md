---
name: optimization-and-scheduling
description: "Builds and checks schedulers, rosters and shift plans made by a solver: OR-Tools CP-SAT, HiGHS, Timefold, Gurobi; rules as constraints; fatigue and utilization; lead times from backlog and capacity. Use when an optimizer makes the plan."
license: Apache-2.0
metadata:
  reviewed: "2026-11-11"
---

# Optimization and scheduling

For plans a solver makes: production schedules, staff rosters, shift plans, routes and lead-time
quotes, written with OR-Tools CP-SAT, HiGHS, SCIP, Timefold, Gurobi, CPLEX, Pyomo or PuLP. It
covers choosing the solver, writing rules as constraints, checking what the solver returns, and
the people in the plan: fatigue, learning and utilization. Whether to change what people do at
all belongs to `human-factors`; checking results against independent references in general to
`testing`; language idioms to `coding`. Pinning and updating a solver follows the standard's
section 8, Dependencies.

## What applies to every module

These summarize the modules; they hold the cases, the facts and the reasons, so read the one
that fits before answering.

1. **A solver's status is a claim, not proof.** Check every plan with plain code that never
   imports the solver, and replay an infeasibility core with presolve off.
2. **A run stopped at a limit reports what it found:** status, incumbent, bound, gap, wall time,
   workers, seed and version.
3. **Rules are data,** each marked hard or soft with its source, read by the model and the
   checker alike.
4. **People are not machines in the model:** fatigue limits with sources, durations that depend
   on who and how recently, and utilization kept below full.
5. **A lead time is backlog over measured throughput,** plus a variability allowance; backlog
   over nameplate capacity is only a floor.

## Modules

Read the module that fits the request, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources.

| Module | Read it for |
|---|---|
| [`optimization-and-scheduling`](references/optimization-and-scheduling.md) | Building a solver's plan: choosing CP-SAT, HiGHS, SCIP, Timefold, Gurobi or CPLEX; hard and soft constraints, weights and strict priorities; CP-SAT settings; solver licenses in containers; fatigue, learning and utilization; lead-time quotes from backlog |
| [`plan-checking`](references/plan-checking.md) | Checking what a solver returns and testing a planner: an unconfirmed OPTIMAL or INFEASIBLE, an infeasibility core, a run stopped at its time limit, CP-SAT tests that repeat, and benchmark instances with published bounds |

## When something here is wrong

If the person says advice here is wrong, out of date, failed or doesn't fit, answer their
problem first. Then say in one sentence whether the fault looks like this skill's, and why: a
fact past its check-by date, an example that fails, two rules that disagree, or a case the skill
doesn't cover. If the fault is elsewhere, such as their setup, say that instead.

When the fault is the skill's own, draft a full report they can paste as a new issue at
https://github.com/rmccann-hub/claude-code-skills/issues.
Give the skill and module, the plugin's version or the skill's date in its frontmatter, their
request word for word, the line of the skill that misled, what happened, what's right with its
source, and the fix you'd suggest. Leave out their private data, company detail and repository
names. File it only if they ask you to.
