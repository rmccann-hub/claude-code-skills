# Plan checking

Read this for checking what a solver returns before anyone acts on it, and for testing a
planner: an OPTIMAL or INFEASIBLE nobody has confirmed, an infeasibility core to report, a run
stopped at its time limit, CP-SAT tests that give the same answer twice, and benchmark
instances with published bounds as the expected answer.

Choosing the solver, the rules as data, CP-SAT settings in production, the people in the plan
and lead-time quotes are the optimization-and-scheduling module's. Independent references in
general are the testing skill's test-oracles module, and flaky tests in general its
flaky-tests module.

## Rules

1. **Never accept a solver's OPTIMAL or INFEASIBLE as proof.** A checker in plain code that
   never imports the solver re-checks every hard constraint (precedence, overlap, capacity,
   qualifications, rest), recomputes the objective from the assignment, and fails on any
   difference. Replay an infeasibility core with presolve off before reporting it (facts
   `os-cpsat-wrong-status`, `pck-cpsat-5582`, `os-cpsat-core`).
2. **Report what a run that stopped at a limit found:** status (FEASIBLE, not OPTIMAL),
   incumbent, best bound, gap, time used, workers, seed and solver version.
3. **Make a planner's tests repeatable, and still check them.** Pin the solver version. Run
   CP-SAT on one worker, or set `interleave_search` for several, with a fixed `random_seed`
   and `max_deterministic_time` in place of `max_time_in_seconds` (facts
   `pck-cpsat-one-worker`, `pck-cpsat-interleave`, `pck-cpsat-det-time`). Assert on the
   checker's verdict and on bounds, never on an exact assignment.
4. **Use benchmark instances with published bounds as the expected answer.** Assert that the
   objective lies between the published lower and upper bounds, plus a stated tolerance, and
   record each bound's source and date: bounds move (facts `pck-taillard`, `pck-taillard-ta33`,
   `pck-psplib-open`, `pck-nrp-bounds`). Cite the figures; copy no instance file into the
   repository until someone has asked the owner and recorded the answer.

### What the checker reports

One line per hard constraint broken, naming the tasks, people and times; the objective it
recomputed beside the solver's; and a per-constraint total for each soft term. That report is
also the score explanation a planner shows its users. Model and checker read one rules table,
so a rule added to one reaches the other.

### A result outside the published bounds

For a minimizing objective, a value below the published lower bound is a defect in the model
or the checker, never a discovery, until the checker passes and the run is repeated. A value
above the upper bound plus tolerance is a regression. A value below the upper bound is either
a new best or a missed constraint: run the checker before celebrating.

## Mistakes

- **Trusting OPTIMAL from a hinted run, or INFEASIBLE on a model a person can solve.** Run the
  checker, and solve again without the hint; #5582 also happens without one (facts
  `os-cpsat-wrong-status`, `pck-cpsat-5582`).
- **Taking `presolve_inclusion_work_limit: 0` as the fix for #5582.** Its reporter calls the
  switches empirical results on one sample (fact `pck-cpsat-5582`). Keep the checker.
- **Reporting a core from `sufficient_assumptions_for_infeasibility()` with presolve on.** It can
  name a literal that was never an assumption (fact `os-cpsat-core`).
- **A checker that imports the solver or calls the model's constraint code.** It repeats the
  model's mistakes. Write it from the rules table alone.
- **Calling a default multi-worker CP-SAT run reproducible, or limiting tests by wall clock.**
  The answer then depends on the machine's load. Use the settings in rule 3.
- **Taking a repeatable run as a correct one.** #5582's wrong OPTIMAL came at one worker
  (fact `os-cpsat-wrong-status`).
- **Golden schedules compared field by field.** Any equal-cost answer fails them.
- **A best-known value asserted as the optimum, with no date.** It goes stale when the
  literature improves it (fact `pck-taillard-ta33`).
- **What AI assistants get wrong,** inferred from version history, not a study: OPTIMAL
  reported unchecked, and `max_time_in_seconds` in tests.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A plan ships on the solver's status | No checker, or one that imports the solver | `BLOCKER` | A plain-code checker |
| A core reported unchecked | Cores taken with presolve on, not replayed | `GAP` | Replay with presolve off |
| A limit-stopped run reads as optimal | Reports without status, bound, gap, workers, seed, version | `GAP` | Report all of them |
| Tests that can't repeat | Several workers without `interleave_search`; `max_time_in_seconds` in tests | `DRIFT` | One worker or interleaved, seed, deterministic time |
| Exact-assignment tests | Golden schedules compared field by field | `GAP` | Assert the checker's verdict and bounds |
| A bound without its date | Expected objectives with no source or date | `GAP` | Record both; recheck on the check-by date |
| Benchmark files copied in | Instance files committed with no license recorded | `GAP` | Ask the owner; fetch at test time meanwhile |

## Why

### The independent checker (rules 1 and 2)

- **The advice:** a status is the solver's claim about itself; check it with code that shares
  nothing with the solver.
- **The reason:** an open CP-SAT 9.15 issue reports OPTIMAL above a known feasible value in 7 of
  207 runs at one worker, and INFEASIBLE on a model with a known solution (fact
  `os-cpsat-wrong-status`). It happens with and without a hint, and its reporter's workaround is
  empirical (fact `pck-cpsat-5582`). Another issue returns a core literal never passed as an
  assumption, and a maintainer calls presolve with assumptions "best effort" (fact
  `os-cpsat-core`). A run stopped at a limit has a bound and a gap; reporting it as optimal
  hides how far the plan might be from the best.
- **What others do:** the proposed fix for the core bug tests each core by replaying it without
  presolve. SCIP 10's exact rational mode is a second opinion for small MILPs.
- **What it costs:** a second encoding of each constraint, which can drift: have both read one
  rules table.
- **When to choose differently:** an exploratory solve nobody acts on; never a published plan.

### Repeatable tests (rule 3)

- **The advice:** one worker or `interleave_search`, a fixed seed, a deterministic time limit,
  and assertions on the verdict and bounds.
- **The reason:** one worker means no parallelism, and `interleave_search` makes several
  workers search deterministically (facts `pck-cpsat-one-worker`, `pck-cpsat-interleave`).
  A wall-clock limit stops at a different point under a different load; a deterministic one
  doesn't (fact `pck-cpsat-det-time`). An exact assignment fails on any equal-cost answer.
- **What others do:** production runs use eight or more workers and a wall-clock limit (fact
  `os-cpsat-8-workers`), so tests and production differ on purpose.
- **What it costs:** `interleave_search` is marked Experimental, and a CP-SAT developer calls
  it "usually way slower" (fact `pck-cpsat-interleave`). One worker misses defects that only
  parallel search shows: keep one unpinned run that asserts only the checker's verdict.
- **When to choose differently:** a solver with a documented deterministic parallel mode needs
  no single-worker pin.

### Benchmark instances (rule 4)

- **The advice:** published bounds as the expected answer, each with its source and date.
- **The reason:** Taillard publishes best-known lower and upper bounds, and his job-shop summary
  was last updated in 2013; ta33 was closed with OR-Tools in 2025 (facts `pck-taillard`,
  `pck-taillard-ta33`). In 2019, 215 PSPLIB instances were still open (fact `pck-psplib-open`).
  The nurse-rostering site dates each bound, and one closed on 2026-10-16 (fact
  `pck-nrp-bounds`). An open instance has a gap, so assert a range, not a value.
- **What others do:** the literature reports new bounds before the libraries post them.
- **What it costs:** fetching instances at test time needs the network and a cache; asking
  for permission takes time. None of these sites states a license.
- **When to choose differently:** a problem no benchmark resembles: use small instances solved
  by hand or by exhaustive search instead.

## Facts

Versions, dates and findings, each named elsewhere in this module by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `os-cpsat-wrong-status` | Open issue: CP-SAT 9.15.6755 reports wrong OPTIMAL and INFEASIBLE results | [#5582](https://github.com/google/or-tools/issues/5582) | "At 1 worker, 7 of the 207 reported OPTIMAL above a known feasible value" and "CP-SAT returns INFEASIBLE although a known solution" | 2026-11-11 | 2027-02-11 |
| `pck-cpsat-5582` | #5582 occurs without a hint too; its workaround switches are empirical | [#5582](https://github.com/google/or-tools/issues/5582) | "It also happens without a hint." and "These are empirical results on this sample, not a soundness argument for any of the switches." | 2026-11-11 | 2027-02-11 |
| `os-cpsat-core` | Open issue: with presolve on, a core can hold a non-assumption literal | [#5141](https://github.com/google/or-tools/issues/5141) | "it returns a literal index that was never passed to" and "presolve and assumptions are currently a best effort support" | 2026-11-11 | 2027-02-11 |
| `pck-cpsat-one-worker` | `num_workers` 1 runs CP-SAT without parallelism | [sat_parameters.proto](https://github.com/google/or-tools/blob/stable/ortools/sat/sat_parameters.proto) | "A number of 1 means no parallelism." | 2026-11-11 | 2027-02-11 |
| `pck-cpsat-interleave` | `interleave_search` is deterministic for any worker count, Experimental, and slower | [sat_parameters.proto](https://github.com/google/or-tools/blob/stable/ortools/sat/sat_parameters.proto), [or-tools-discuss](https://groups.google.com/g/or-tools-discuss/c/lPb1FzhTMt0) | "The search is deterministic (independently of num_workers!), and we", "Experimental. If this is true, then we interleave all our major search" and "It is usually way slower than the non deterministic version." | 2026-11-11 | 2027-02-11 |
| `pck-cpsat-det-time` | CP-SAT takes a time limit in deterministic time | [sat_parameters.proto](https://github.com/google/or-tools/blob/stable/ortools/sat/sat_parameters.proto) | "Maximum time allowed in deterministic time to solve a problem." | 2026-11-11 | 2027-02-11 |
| `pck-taillard` | Taillard publishes best-known bounds; the job-shop summary's last update is 2013-06-17 | [Taillard](https://mistic.iict-heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html), [job-shop bounds](https://mistic.iict-heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/jobshop.dir/best_lb_up.txt) | "Summary of best known lower and upper bounds of Taillard's instances" and "Update 17.06.2013" | 2026-11-11 | 2027-05-11 |
| `pck-taillard-ta33` | Taillard's ta33 was closed in 2025, with OR-Tools | [arXiv 2504.16106](https://arxiv.org/abs/2504.16106) | "We find new numerical lower bounds for multiple benchmark instances, up to closing the Taillard's ta33 instance." | 2026-11-11 | 2027-05-11 |
| `pck-psplib-open` | In 2019, 215 PSPLIB instances were still open | [arXiv 1909.02737](https://arxiv.org/abs/1909.02737) | "we found that 215 of the PSPLIB instances, 2842 of the MMLIB instances, and 27 of the MISTA instances, were still open" | 2026-11-11 | 2027-05-11 |
| `pck-nrp-bounds` | The nurse-rostering site dates its bounds: BCV-3.46.1's best, 3275, on 2026-10-16 | [Bounds](https://www.schedulingbenchmarks.org/nrp/bounds.html) | "3275" and "16-Oct-2026" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [OR-Tools](https://github.com/google/or-tools): `sat_parameters.proto`, issues #5582 and #5141 | Parameters, defects | Apache-2.0 code; issues their authors': brief quotes |
| [or-tools-discuss](https://groups.google.com/g/or-tools-discuss/c/lPb1FzhTMt0) | Cost of deterministic search | Authors' copyright: brief quotes with a link |
| [Taillard](https://mistic.iict-heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html), [schedulingbenchmarks.org](https://www.schedulingbenchmarks.org/nrp/), PSPLIB | Benchmark bounds | None stated: cite figures; don't copy the data |
| [arXiv 2504.16106](https://arxiv.org/abs/2504.16106), [arXiv 1909.02737](https://arxiv.org/abs/1909.02737) | Bounds that moved | Per-paper arXiv license, not checked: brief quotes, cited |
