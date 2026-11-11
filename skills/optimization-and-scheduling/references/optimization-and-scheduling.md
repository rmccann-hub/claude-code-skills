# Optimization and scheduling

Read this for a scheduler, roster, shift plan or production plan built on a solver: choosing
OR-Tools CP-SAT, HiGHS, SCIP, Timefold, Gurobi or CPLEX; business rules as constraints; checking
a solver's answer or a run stopped at its limit; fatigue, learning and utilization in the plan;
and lead times quoted from backlog and capacity.

Whether to change what people do at all is the human-factors skill. Independent references in
general are the testing skill's test-oracles module; Python idioms, the coding skill's
python-coding module.

## Rules

1. **Never accept a solver's OPTIMAL or INFEASIBLE as proof.** A checker in plain code that
   never imports the solver re-checks every hard constraint (precedence, overlap, capacity,
   qualifications, rest), recomputes the objective from the assignment, and fails on any
   difference. Replay an infeasibility core with presolve off before reporting it (facts
   `os-cpsat-wrong-status`, `os-cpsat-core`).
2. **Report what a run that stopped at a limit found:** status (FEASIBLE, not OPTIMAL),
   incumbent, best bound, gap, wall time, workers, seed and solver version.
3. **Choose the solver for the problem class,** by the table below.
4. **Hold the rules as data, each marked hard or soft with its source.** Law, safety and
   qualifications are hard; preferences soft. Scale each soft term by its plausible range
   before weighting, or solve lexicographically when priorities are strict. This is a
   heuristic, not a sourced finding: label it so.
5. **Write CP-SAT in snake_case only.** Set `num_workers` to the container's CPUs and
   `max_time_in_seconds` always. In tests, pin version, seed and workers, and assert on bounds
   and the checker's verdict, never on an exact assignment.
6. **Put the people in the plan as they are.** Night work, shifts over eight hours, successive
   shifts and missing breaks raise error risk (fact `os-hsg256`): make each a hard limit or a
   soft penalty, with its source. A task's duration depends on who does it and how recently, so
   hold a worker-task duration table fed by measured times. Plan below full utilization.
7. **Quote lead time from measured throughput.** Backlog over nameplate capacity is a floor,
   not a forecast. Convert orders to bottleneck hours with a per-product rate table, divide by
   the hours delivered over a recent window (fact `os-little`), add a variability allowance,
   and count on a working-day calendar held as data. Report floor and allowance apart.

### Choosing a solver

| Problem | Use | License, facts |
|---|---|---|
| Intervals, no-overlap, cumulative resources, sequencing | OR-Tools CP-SAT | Apache-2.0; `os-ortools` |
| LP and MIP: capacity, lot sizing, aggregate plans | HiGHS, the open default (SciPy's `milp` wraps it) | MIT; `os-highs`, `os-mittelmann` |
| MINLP, branch-and-price, exact rational MILP | SCIP | Apache-2.0; `os-scip` |
| Large soft-constrained rosters or routes, in Java or Kotlin | Timefold Solver, local search | Apache-2.0 Community; `os-timefold` |
| A paid license where the gap matters | Gurobi or CPLEX | Proprietary; `os-gurobi`, `os-cplex` |
| One Python model over several solvers | Pyomo, or PuLP 4 plus a solver | BSD-3-Clause, MIT; `os-pulp` |

## Mistakes

- **Trusting OPTIMAL from a hinted run, or INFEASIBLE on a model a person can solve.** Run the
  checker, and solve again without the hint (fact `os-cpsat-wrong-status`).
- **Reporting a core from `sufficient_assumptions_for_infeasibility()` with presolve on.** It can
  name a literal that was never an assumption (fact `os-cpsat-core`).
- **Writing `AddNoOverlap` or `NewIntervalVar`.** Deprecated aliases that warn only when asked
  (fact `os-cpsat-aliases`).
- **Writing `PULP_CBC_CMD`, or expecting `pip install pulp` to bring a solver** (fact
  `os-pulp`). Install `pulp[cbc]` and use `COIN_CMD`, or use HiGHS.
- **CP-SAT on all of a shared host's cores, or on one worker in production** (facts
  `os-cpsat-params`, `os-cpsat-8-workers`).
- **Expecting score explanations from Timefold Community 2.x** (fact `os-timefold-editions`).
  Build them from the checker's per-constraint report.
- **Fixed task times at full utilization,** or working-time law taken as enough to prevent
  fatigue (fact `os-hsg256`).
- **What AI assistants get wrong,** inferred from version history, not a study: CamelCase CP-SAT
  and `PULP_CBC_CMD` from old examples, and OPTIMAL reported unchecked.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A plan ships on the solver's status | No checker, or one that imports the solver | `BLOCKER` | A plain-code checker |
| A core reported unchecked | Cores taken with presolve on, not replayed | `GAP` | Replay with presolve off |
| A limit-stopped run reads as optimal | Reports without status, bound, gap, workers, seed, version | `GAP` | Report all of them |
| CP-SAT unbounded | `CpSolver()` without `max_time_in_seconds` or `num_workers` | `DRIFT` | Set both |
| CamelCase CP-SAT | `Add[A-Z]`, `New[A-Z]` calls on a model | `DRIFT` | snake_case names |
| PuLP 4 expecting CBC | `PULP_CBC_CMD`; `pulp>=4` with no solver dependency | `BLOCKER` | `pulp[cbc]` and `COIN_CMD`, or HiGHS |
| Exact-assignment tests | Golden schedules compared field by field | `GAP` | Pin version, seed, workers; assert bounds |
| Rules or durations in code | Shift limits, rest gaps, calendars, task times as literals | `GAP` | Tables, each row sourced |
| Lead time from nameplate | Backlog divided by rated capacity | `BLOCKER` where customers get the date | Measured throughput plus an allowance |
| A solver near end of support | Timefold 1.x; a Gurobi major over three years old | `DRIFT` | Plan the move (facts `os-timefold-editions`, `os-gurobi`) |

## Why

### The independent checker (rules 1 and 2)

- **The advice:** a status is the solver's claim about itself; check it with code that shares
  nothing with the solver.
- **The reason:** an open CP-SAT 9.15 issue reports OPTIMAL above a known feasible value in 7 of
  207 runs at one worker, and INFEASIBLE on a model with a known solution (fact
  `os-cpsat-wrong-status`). Another returns a core literal never passed as an assumption, and a
  maintainer calls presolve with assumptions "best effort" (fact `os-cpsat-core`).
- **What others do:** the proposed fix for the core bug tests each core by replaying it without
  presolve. SCIP 10's exact rational mode is an oracle for small MILPs.
- **What it costs:** a second encoding of each constraint, which can drift: have both read one
  rules table.
- **When to choose differently:** an exploratory solve nobody acts on; never a published plan.

### Solver choice and settings (rules 3 and 5)

- **The advice:** choose by problem class, pin the version, set workers and a time limit.
- **The reason:** CP-SAT has native intervals, no-overlap and cumulative constraints, which a
  MIP builds from big-M terms that weaken its bound (our own practice). Parallel HiGHS solves
  more of MIPLIB 2017 than SCIP (fact `os-mittelmann`). CP-SAT takes every core it sees by
  default (fact `os-cpsat-params`), and wants eight or more workers (fact `os-cpsat-8-workers`).
- **What it costs:** pinned tests miss other worker counts, and each solver's support ends
  (facts `os-timefold-editions`, `os-gurobi`).
- **When to choose differently:** keep a paid license that closes gaps the open solvers leave.

### Rules as data, hard and soft (rule 4)

- **The advice:** each rule is a row with its source and class, read by model and checker.
- **The reason:** unscaled weights let one term decide silently. Wiers (2009) found "a
  disagreement concerning autonomy is a key explanatory factor for understanding why an APS
  implementation may fail", so rules the shop floor owns stay editable by it.
- **What it costs:** a lexicographic solve takes one solve per priority level.
- **When to choose differently:** one objective with no competing terms needs no scaling.

### People in the plan (rule 6)

- **The advice:** sourced fatigue limits, durations by worker and recency, and slack.
- **The reason:** HSE ties error risk to night work, length, succession and breaks, and says
  working-time law may not prevent fatigue (fact `os-hsg256`); it finds the evidence for
  forward rotation limited, so that stays a soft preference. Unit time falls with repetition
  (Wright, 1936), breaks undo some of it (Jaber and Bonney, 1996), and both vary by person
  (Nembhard and Uzumeri, 2000). Kingman (1961): queueing delay grows without bound as
  utilization nears 1, faster the more variable the work.
- **What others do:** HSE points planners to its Fatigue and Risk Index tool.
- **What it costs:** times per person are personal data; how far to go is human-factors' call.
- **When to choose differently:** a fully automated cell with no one rostered to it.

### Lead time from throughput (rule 7)

- **The advice:** W = L / λ, with λ the throughput realized, in the backlog's units.
- **The reason:** Little's law needs no stationarity (fact `os-little`). Nameplate capacity
  exceeds realized throughput whenever there is downtime, absence, scrap or a slow mix, so a
  manufacturer's lead-time board dividing open orders by daily capacity understates every date.
- **What others do:** CONWIP (Spearman, Woodruff and Hopp, 1990) caps work in process, and so
  lead time.
- **What it costs:** a throughput history. For a new product, quote the floor plus a stated
  allowance.
- **When to choose differently:** an item shipped from stock needs no queue model.

## Facts

Versions, dates and findings, each named elsewhere in this module by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `os-cpsat-wrong-status` | Open issue: CP-SAT 9.15.6755 reports wrong OPTIMAL and INFEASIBLE results | [#5582](https://github.com/google/or-tools/issues/5582) | "At 1 worker, 7 of the 207 reported OPTIMAL above a known feasible value" and "CP-SAT returns INFEASIBLE although a known solution" | 2026-11-11 | 2027-02-11 |
| `os-cpsat-core` | Open issue: with presolve on, a core can hold a non-assumption literal | [#5141](https://github.com/google/or-tools/issues/5141) | "it returns a literal index that was never passed to" and "presolve and assumptions are currently a best effort support" | 2026-11-11 | 2027-02-11 |
| `os-ortools` | OR-Tools' newest release is v9.15 | `git ls-remote --tags https://github.com/google/or-tools` | `refs/tags/v9.15` | 2026-11-11 | 2027-02-11 |
| `os-cpsat-aliases` | CP-SAT 9.15 keeps CamelCase names as deprecated aliases | [cp_model.py](https://github.com/google/or-tools/blob/v9.15/ortools/sat/python/cp_model.py) | "# Compatibility with pre PEP8" | 2026-11-11 | 2027-02-11 |
| `os-cpsat-params` | `num_workers` 0, the default, uses all cores | [sat_parameters.proto](https://github.com/google/or-tools/blob/v9.15/ortools/sat/sat_parameters.proto) | "A value of 0 means the solver will try to use all cores on the machine." | 2026-11-11 | 2027-02-11 |
| `os-cpsat-8-workers` | CP-SAT is designed for eight or more workers | [Discussion #3630](https://github.com/google/or-tools/discussions/3630) | "The solver is designed to work with 8+ workers, unless for trivial models." | 2026-11-11 | 2027-05-11 |
| `os-highs` | HiGHS' newest release is 1.16.0 | `git ls-remote --tags https://github.com/ERGO-Code/HiGHS` | `refs/tags/v1.16.0` | 2026-11-11 | 2027-02-11 |
| `os-mittelmann` | MILP table, 2026-10-28: parallel HiGHS solved 179, SCIP 136; no Gurobi or CPLEX | [Mittelmann](https://plato.asu.edu/ftp/milp.html) | "COPT   SCIP HiGHSp  HiGHS  OPTV FSCIP SCIPCO" and "solved   225    136    179    158   210   158   160" | 2026-11-11 | 2027-02-11 |
| `os-scip` | SCIP Optimization Suite 10.1.0 is current; Apache-2.0 since 8.0.3 | [SCIP](https://scipopt.org/), [download](https://scipopt.org/download.php) | "The SCIP Optimization Suite 10.1.0 consists of SCIP 10.1.0" and "The Apache 2.0 License applies from Version 8.0.3 onwards." | 2026-11-11 | 2027-02-11 |
| `os-timefold` | Timefold Solver's newest release is 2.8.0 | `git ls-remote --tags https://github.com/TimefoldAI/timefold-solver` | `refs/tags/v2.8.0` | 2026-11-11 | 2027-02-11 |
| `os-timefold-editions` | Timefold 1.x ends early 2027; 2.x score analysis is Enterprise only | [v1.34.0](https://github.com/TimefoldAI/timefold-solver/releases/tag/v1.34.0), [docs](https://docs.timefold.ai/timefold-solver/latest/constraints-and-score/understanding-the-score) | "1.x EOL in early 2027" and "This feature is exclusive to Timefold Solver Enterprise Edition." | 2026-11-11 | 2027-02-11 |
| `os-gurobi` | gurobipy 14.0.0 is on PyPI; each major release is supported three years | [PyPI](https://pypi.org/pypi/gurobipy/json), [support](https://support.gurobi.com/hc/en-us/articles/360048138771-Gurobi-release-and-support-history) | "14.0.0" and "for a term of three years after the initial release" | 2026-11-11 | 2027-02-11 |
| `os-cplex` | CPLEX 22.2.x is generally available from 2026-05-22 | [IBM](https://www.ibm.com/support/pages/ibm-ilog-cplex-optimization-studio222x) | "22-May-2026" | 2026-11-11 | 2027-02-11 |
| `os-pulp` | PuLP 4 ships no CBC and removed `PULP_CBC_CMD` | [PuLP](https://www.coin-or.org/pulp/main/installing_pulp_at_home.html) | "CBC is not included inside the PuLP wheel." and "The legacy PULP_CBC_CMD solver" | 2026-11-11 | 2027-02-11 |
| `os-hsg256` | HSE: error risk rises at night, past eight hours, over successive shifts; working-time law may not be enough | [HSG256 (PDF)](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/390908/hsg256_managing_shift_work.pdf) | "to be higher on the night shift;", "to rise with increasing shift length over eight hours;", "to increase over successive shifts" and "complying with WTR may not in itself be enough to prevent fatigue" | 2026-11-11 | 2027-05-11 |
| `os-little` | Little's law holds when the limits exist, without stationarity | [Little (2011)](https://pubsonline.informs.org/doi/10.1287/opre.1110.0940) | "If limits λ and W exist and are finite, L exists and is finite, and L = λW." and "LL.1 holds under nonstationary conditions." | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [OR-Tools](https://github.com/google/or-tools): code, issues, PR #5539, discussion #3630 | CP-SAT names, parameters, defects | Apache-2.0 code; issues their authors': brief quotes |
| [HiGHS](https://highs.dev/), [SCIP](https://scipopt.org/), [Timefold](https://github.com/TimefoldAI/timefold-solver), [PuLP](https://www.coin-or.org/pulp/), [Pyomo](https://pypi.org/project/pyomo/) | Versions, licenses | MIT, Apache-2.0, Apache-2.0, MIT, BSD-3-Clause; docs: brief quotes |
| [Gurobi](https://support.gurobi.com/), [IBM](https://www.ibm.com/support/pages/ibm-ilog-cplex-optimization-studio222x), [Mittelmann](https://plato.asu.edu/ftp/milp.html) | Versions, benchmarks | Proprietary or none stated: brief quotes |
| [HSE HSG256](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/390908/hsg256_managing_shift_work.pdf) | Fatigue | Crown copyright: brief quotes |
| [Little 2011](https://doi.org/10.1287/opre.1110.0940), [Kingman 1961](https://doi.org/10.1017/S0305004100036094), [Wright 1936](https://doi.org/10.2514/8.155), [Jaber and Bonney 1996](https://doi.org/10.1016/0307-904X(95)00157-F), [Nembhard and Uzumeri 2000](https://doi.org/10.1016/S0169-8141(99)00021-9), [Wiers 2009](https://doi.org/10.1080/09537280903034289), [Spearman et al. 1990](https://doi.org/10.1080/00207549008942761) | Queues, learning, plans on the floor | Publisher copyright: brief quotes, cited |
