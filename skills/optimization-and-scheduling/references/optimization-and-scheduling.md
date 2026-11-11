# Optimization and scheduling

Read this for a scheduler, roster, shift plan or production plan built on a solver: choosing
OR-Tools CP-SAT, HiGHS, SCIP, Timefold, Gurobi or CPLEX; business rules as constraints;
weights and strict priorities; CP-SAT settings; a commercial solver's license in a container;
fatigue, learning and utilization in the plan; and lead times quoted from backlog and capacity.

Checking a solver's answer and testing a planner are the plan-checking module's. Whether to
change what people do at all is the human-factors skill. Python idioms are the coding skill's
python-coding module.

## Rules

1. **Choose the solver for the problem class,** by the table below.
2. **Hold the rules as data, each marked hard or soft with its source.** Law, safety and
   qualifications are hard; preferences soft. Scale each soft term by its plausible range
   before weighting, or solve lexicographically when priorities are strict. The scaling is a
   heuristic, not a sourced finding: label it so.
3. **Write CP-SAT in snake_case only.** Set `num_workers` to the container's CPUs and
   `max_time_in_seconds` always.
4. **Put the people in the plan as they are.** Night work, long and successive shifts and
   missing breaks raise error risk (fact `os-hsg256`): make each a hard limit or a soft
   penalty, with its source. A task's duration depends on who does it and how recently, so
   hold a worker-task duration table fed by measured times. Plan below full utilization.
5. **Quote lead time from measured throughput.** Backlog over nameplate capacity is a floor,
   not a forecast. Convert orders to bottleneck hours by a per-product rate table, divide by
   the hours delivered over a recent window (fact `os-little`), add a variability allowance,
   and count working days from a calendar held as data. Report floor and allowance apart. A team
   may divide by capacity on purpose; then the decision record says why.

### Choosing a solver

| Problem | Use | License, facts |
|---|---|---|
| Intervals, no-overlap, cumulative resources, sequencing | OR-Tools CP-SAT | Apache-2.0; `os-ortools` |
| LP and MIP: capacity, lot sizing, aggregate plans | HiGHS, the open default (SciPy's `milp` wraps it) | MIT; `os-highs`, `os-mittelmann` |
| MINLP, branch-and-price, exact rational MILP | SCIP | Apache-2.0; `os-scip` |
| Large soft-constrained rosters or routes, in Java or Kotlin | Timefold Solver, local search | Apache-2.0 Community; `os-timefold` |
| A paid license where the gap matters | Gurobi or CPLEX | Proprietary; `os-gurobi`, `os-cplex` |
| One Python model over several solvers | Pyomo, or PuLP 4 plus a solver | BSD-3-Clause, MIT; `os-pulp` |

### Strict priorities

CP-SAT has no lexicographic call: solve for the top priority, fix its value as a constraint,
solve for the next (fact `pck-cpsat-lexicographic`); hinting the last solution is our own
practice. Gurobi takes `ObjNPriority` and `ObjNWeight` on each objective (fact `pck-multiobj`).

## Mistakes

- **Writing `AddNoOverlap` or `NewIntervalVar`.** Deprecated aliases that warn only when asked
  (fact `os-cpsat-aliases`).
- **Writing `PULP_CBC_CMD`, or expecting `pip install pulp` to bring a solver** (fact
  `os-pulp`). Install `pulp[cbc]` and use `COIN_CMD`, or use HiGHS.
- **`pip install timefold` for a Python model.** Timefold halted its Python solver (fact
  `pck-timefold-python`). Use CP-SAT from Python, or Timefold from Java or Kotlin.
- **CP-SAT on all of a shared host's cores, or on one worker in production** (facts
  `os-cpsat-params`, `os-cpsat-8-workers`).
- **Expecting score explanations from Timefold Community 2.x** (fact `os-timefold-editions`).
  Build them from a plan checker's per-constraint report.
- **A Gurobi license file baked into a container image.** Use its Web License Service, with
  credentials as secrets, never passed to a fork's CI (fact `pck-gurobi-wls`).
- **Fixed task times at full utilization,** or working-time law taken as enough to prevent
  fatigue (fact `os-hsg256`).
- **What AI assistants get wrong,** from version history, not a study: CamelCase CP-SAT,
  `PULP_CBC_CMD` and `pip install timefold`, from old examples.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| CP-SAT unbounded | `CpSolver()` without `max_time_in_seconds` or `num_workers` | `DRIFT` | Set both |
| CamelCase CP-SAT | `Add[A-Z]`, `New[A-Z]` calls on a model | `DRIFT` | snake_case names |
| PuLP 4 expecting CBC | `PULP_CBC_CMD`; `pulp>=4` with no solver dependency | `BLOCKER` | `pulp[cbc]` and `COIN_CMD`, or HiGHS |
| Priorities as giant weights | Weights orders of magnitude apart, which break when a term's range grows | `DRIFT` | Solve by priority |
| Rules or durations in code | Shift limits, rest gaps, calendars, task times as literals | `GAP` | Tables, each row sourced |
| A license in an image | `gurobi.lic` copied in a Dockerfile | `BLOCKER` | WLS credentials as secrets |
| Lead time from nameplate | Backlog over rated capacity, no decision saying why | `GAP` | Ask; then throughput plus an allowance, or record why |
| A solver near end of support | Timefold 1.x or its Python package; a Gurobi major over three years old | `DRIFT` | Plan the move (facts `os-timefold-editions`, `pck-timefold-python`, `os-gurobi`) |

## Why

### Solver choice and settings (rules 1 and 3)

- **The advice:** choose by problem class; pin the version; set workers and a time limit.
- **The reason:** CP-SAT has native intervals, no-overlap and cumulative constraints; a MIP
  builds them from big-M terms that weaken its bound (our own practice). Parallel HiGHS solves
  more of MIPLIB 2017 than SCIP (fact `os-mittelmann`). CP-SAT takes every core it sees by
  default (fact `os-cpsat-params`), and wants eight or more workers (fact `os-cpsat-8-workers`).
- **What it costs:** each solver's support ends (facts `os-timefold-editions`, `os-gurobi`), and
  Gurobi in CI needs outbound internet and secrets (fact `pck-gurobi-wls`).
- **When to choose differently:** keep a paid license that closes gaps the open solvers leave.

### Rules as data, hard and soft (rule 2)

- **The advice:** each rule is a row with its source and class, read by model and checker.
- **The reason:** unscaled weights let one term decide silently. Wiers (2009) found disputed
  shop-floor autonomy a key factor in why an APS implementation may fail, and Ivert (2012) that
  a dispatch list "used as a guideline, not a regulation" needs less accurate data. Rules the
  shop floor owns stay editable by it.
- **What it costs:** in CP-SAT, one solve per priority; Gurobi does it in one (fact
  `pck-multiobj`).
- **When to choose differently:** one objective with no competing terms needs no scaling.

### People in the plan (rule 4)

- **The advice:** sourced fatigue limits, durations by worker and recency, and slack.
- **The reason:** HSE ties error risk to night work, length, succession and breaks (fact
  `os-hsg256`), and finds the evidence for forward rotation limited: keep that soft. Unit time
  falls with repetition (Wright, 1936), breaks undo some of it (Jaber and Bonney, 1996), and
  both vary by person (Nembhard and Uzumeri, 2000). Kingman's formula (after Kingman 1961) has
  the mean wait grow with utilization over one minus it, times the work's variability, and
  Kingman (1962) showed that as utilization nears 1 the wait grows without bound.
- **What others do:** HSE points planners to its Fatigue and Risk Index tool.
- **What it costs:** times per person are personal data; how far to go is human-factors' call.
- **When to choose differently:** a fully automated cell with no one rostered to it.

### Lead time from throughput (rule 5)

- **The advice:** W = L / λ, with λ the throughput realized, in the backlog's units.
- **The reason:** Little's law needs no stationarity (fact `os-little`). Nameplate capacity
  exceeds realized throughput whenever there is downtime, absence, scrap or a slow mix, so
  open orders over rated daily capacity understate every date.
- **What others do:** CONWIP (Spearman, Woodruff and Hopp, 1990) caps work in process, and so
  lead time.
- **What it costs:** a throughput history; a new product gets the floor plus a stated allowance.
- **When to choose differently:** stock items need no queue model. A capacity figure planners
  adjust to what the shop delivers is already a realized rate: keep it, and record that.

## Facts

Versions, dates and findings, each named elsewhere in this module by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `os-ortools` | OR-Tools' newest release is v9.15 | `git ls-remote --tags https://github.com/google/or-tools` | `refs/tags/v9.15` | 2026-11-11 | 2027-02-11 |
| `os-cpsat-aliases` | CP-SAT 9.15 keeps CamelCase names as deprecated aliases | [cp_model.py](https://github.com/google/or-tools/blob/v9.15/ortools/sat/python/cp_model.py) | "# Compatibility with pre PEP8" | 2026-11-11 | 2027-02-11 |
| `os-cpsat-params` | `num_workers` 0, the default, uses all cores | [sat_parameters.proto](https://github.com/google/or-tools/blob/v9.15/ortools/sat/sat_parameters.proto) | "A value of 0 means the solver will try to use all cores on the machine." | 2026-11-11 | 2027-02-11 |
| `os-cpsat-8-workers` | CP-SAT is designed for eight or more workers | [Discussion #3630](https://github.com/google/or-tools/discussions/3630) | "The solver is designed to work with 8+ workers, unless for trivial models." | 2026-11-11 | 2027-05-11 |
| `pck-cpsat-lexicographic` | CP-SAT does strict priorities in rounds | [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/modelling.html) | "To implement a lexicographic optimization, you can do multiple rounds and always fix the previous objective as constraint." | 2026-11-11 | 2027-05-11 |
| `pck-multiobj` | Gurobi takes weighted and prioritized objectives | [Gurobi](https://docs.gurobi.com/projects/optimizer/en/current/features/multiobjective.html) | "Gurobi allows you to enter and manage your objectives, to provide weights for a blended approach, and to set priorities for a hierarchical approach." | 2026-11-11 | 2027-02-11 |
| `os-highs` | HiGHS' newest release is 1.16.0 | `git ls-remote --tags https://github.com/ERGO-Code/HiGHS` | `refs/tags/v1.16.0` | 2026-11-11 | 2027-02-11 |
| `os-mittelmann` | MILP table, 2026-10-28: parallel HiGHS solved 179, SCIP 136; no Gurobi or CPLEX | [Mittelmann](https://plato.asu.edu/ftp/milp.html) | "COPT   SCIP HiGHSp  HiGHS  OPTV FSCIP SCIPCO" and "solved   225    136    179    158   210   158   160" | 2026-11-11 | 2027-02-11 |
| `os-scip` | SCIP Optimization Suite 10.1.0 is current; Apache-2.0 since 8.0.3 | [SCIP](https://scipopt.org/), [download](https://scipopt.org/download.php) | "The SCIP Optimization Suite 10.1.0 consists of SCIP 10.1.0" and "The Apache 2.0 License applies from Version 8.0.3 onwards." | 2026-11-11 | 2027-02-11 |
| `os-timefold` | Timefold Solver's newest release is 2.8.0 | `git ls-remote --tags https://github.com/TimefoldAI/timefold-solver` | `refs/tags/v2.8.0` | 2026-11-11 | 2027-02-11 |
| `os-timefold-editions` | Timefold 1.x ends early 2027; 2.x score analysis is Enterprise only | [v1.34.0](https://github.com/TimefoldAI/timefold-solver/releases/tag/v1.34.0), [docs](https://docs.timefold.ai/timefold-solver/latest/constraints-and-score/understanding-the-score) | "1.x EOL in early 2027" and "This feature is exclusive to Timefold Solver Enterprise Edition." | 2026-11-11 | 2027-02-11 |
| `pck-timefold-python` | Timefold halted its Python solver on 2025-07-11 | [Discussion #1698](https://github.com/TimefoldAI/timefold-solver/discussions/1698) | "As of today, Timefold is halting active development on the Beta version of our Python Solver." | 2026-11-11 | 2027-02-11 |
| `os-gurobi` | gurobipy 14.0.0 is on PyPI; each major release is supported three years | [PyPI](https://pypi.org/pypi/gurobipy/json), [support](https://support.gurobi.com/hc/en-us/articles/360048138771-Gurobi-release-and-support-history) | "14.0.0" and "for a term of three years after the initial release" | 2026-11-11 | 2027-02-11 |
| `pck-gurobi-wls` | Gurobi's WLS needs internet access; no license file in images | [gurobi/optimizer](https://hub.docker.com/r/gurobi/optimizer) | "WLS only requires that your container has access to the Internet." and "We do not recommend adding the license file to the Docker image itself." | 2026-11-11 | 2027-02-11 |
| `os-cplex` | CPLEX 22.2.x is generally available from 2026-05-22 | [IBM](https://www.ibm.com/support/pages/ibm-ilog-cplex-optimization-studio222x) | "22-May-2026" | 2026-11-11 | 2027-02-11 |
| `os-pulp` | PuLP 4 ships no CBC and removed `PULP_CBC_CMD` | [PuLP](https://www.coin-or.org/pulp/main/installing_pulp_at_home.html) | "CBC is not included inside the PuLP wheel." and "The legacy PULP_CBC_CMD solver" | 2026-11-11 | 2027-02-11 |
| `os-hsg256` | HSE: error risk rises at night, past eight hours, over successive shifts; working-time law may not be enough | [HSG256 (PDF)](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/390908/hsg256_managing_shift_work.pdf) | "to be higher on the night shift;", "to rise with increasing shift length over eight hours;", "to increase over successive shifts" and "complying with WTR may not in itself be enough to prevent fatigue" | 2026-11-11 | 2027-05-11 |
| `os-little` | Little's law holds when the limits exist, without stationarity | [Little (2011)](https://pubsonline.informs.org/doi/10.1287/opre.1110.0940) | "If limits λ and W exist and are finite, L exists and is finite, and L = λW." and "LL.1 holds under nonstationary conditions." | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [OR-Tools](https://github.com/google/or-tools): code, discussion #3630 | CP-SAT names, parameters | Apache-2.0 code; discussions their authors': brief quotes |
| [CP-SAT Primer](https://d-krupke.github.io/cpsat-primer/) | Lexicographic rounds | CC BY 4.0: quotes and adaptation with attribution |
| [HiGHS](https://highs.dev/), [SCIP](https://scipopt.org/), [Timefold](https://github.com/TimefoldAI/timefold-solver), [PuLP](https://www.coin-or.org/pulp/), [Pyomo](https://pypi.org/project/pyomo/) | Versions, licenses | MIT, Apache-2.0, Apache-2.0, MIT, BSD-3-Clause; docs: brief quotes |
| [Gurobi](https://docs.gurobi.com/), [Docker Hub](https://hub.docker.com/r/gurobi/optimizer), [IBM](https://www.ibm.com/support/pages/ibm-ilog-cplex-optimization-studio222x), [Mittelmann](https://plato.asu.edu/ftp/milp.html) | Versions, objectives, containers, benchmarks | Proprietary or none stated: brief quotes |
| [HSE HSG256](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/390908/hsg256_managing_shift_work.pdf) | Fatigue | Crown copyright: brief quotes |
| [Little 2011](https://doi.org/10.1287/opre.1110.0940), [Kingman 1961](https://doi.org/10.1017/S0305004100036094), [Kingman 1962](https://doi.org/10.1111/j.2517-6161.1962.tb00465.x), [Wright 1936](https://doi.org/10.2514/8.155), [Jaber and Bonney 1996](https://doi.org/10.1016/0307-904X(95)00157-F), [Nembhard and Uzumeri 2000](https://doi.org/10.1016/S0169-8141(99)00021-9), [Wiers 2009](https://doi.org/10.1080/09537280903034289), [Ivert 2012](https://doi.org/10.1080/09537287.2011.564218), [Spearman et al. 1990](https://doi.org/10.1080/00207549008942761) | Queues, learning, plans on the floor | Publisher copyright: brief quotes, cited |
