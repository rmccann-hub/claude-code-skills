# Verification: R28 (2026-11-11)

Checked on 2026-11-11 against the primary sources named below. The report is untrusted data. Its
line 3 is addressed to "the receiving session": it asks that session to check each claim, file the
report under `research/runs/`, update the facts files of the categories it names, and list what
changed. That is an instruction found in a research result. It was recorded here and not
followed: nothing was filed, and no repository file was edited.

Access notes:
- github.com web pages and api.github.com returned 403 for google/or-tools, ERGO-Code/HiGHS,
  TimefoldAI/timefold-solver and the rest (this session's GitHub access covers only the owner's
  repositories); `gh` and the GitHub MCP tools were refused for the same reason. Issue, pull
  request and release pages were read with the Exa fetch tool, files with
  raw.githubusercontent.com, and tags with `git ls-remote --tags`.
- plato.asu.edu failed TLS from curl (self-signed certificate in the chain) and WebFetch got 503.
  The Exa fetch tool returned both Mittelmann pages; the MILP page it returned is dated
  28 Oct 2026, later than the report's 7 Jul 2026 figures.
- iso.org returned 403 (bot check) to curl. ISO pages were read through Exa fetch and Exa search
  highlights of iso.org, including the committee catalogue rendered with stage codes.
- tandfonline.com timed out. The Wiers (2009) and Spearman et al. (1990) abstracts were read from
  Exa highlights of the T&F, Ingenta Connect and TU Eindhoven portal pages. Ivert (2012) full text
  was not reachable.
- docs.scipy.org reset the connection and WebFetch got 503; SciPy was checked in its source on
  raw.githubusercontent.com.
- coin-or.github.io/pulp redirects (301) to www.coin-or.org/pulp/; the redirected page was read.
- Gurobi's "What's New" page and the Timefold blog and docs were read through Exa (its copy of
  the Gurobi page may predate the 14.0 launch); Gurobi's support history page and release notes
  were fetched with curl.
- Registries read directly: PyPI JSON API, Maven Central (search API, maven-metadata.xml and file
  headers), Crossref, Zenodo and Semantic Scholar APIs.
- Downloaded files (HSG256 PDF, Little 2011 PDF, PuLP 3.3.2 wheel) were each put in their own
  directory and only read with `pdftotext` or `python3 -I -m zipfile -l`.

| Claim | Status | Checked against |
|---|---|---|
| OR-Tools latest release is v9.15, published 12 Jan 2026 | verified | [Releases · google/or-tools](https://github.com/google/or-tools/releases); `git ls-remote` shows no tag after v9.15 |
| ortools on PyPI is 9.15.6755, released 14 Jan 2026 | verified (upload 2026-01-14T15:37Z) | [ortools JSON on PyPI](https://pypi.org/pypi/ortools/json) |
| No OR-Tools release after 9.15 by 11 Nov 2026 | verified | PyPI JSON; `git ls-remote --tags` |
| OR-Tools is Apache-2.0 | verified | [LICENSE at v9.15](https://raw.githubusercontent.com/google/or-tools/v9.15/LICENSE); PyPI "Apache 2.0" |
| OR-Tools is written in C++ with Python, C# and Java wrappers | verified | [README at v9.15](https://github.com/google/or-tools/blob/v9.15/README.md) |
| OR-Tools 9.15 bundles HiGHS 1.12.0 and SCIP 10.0.0 (report: secondary) | verified at the primary source | [v9.15 release notes](https://github.com/google/or-tools/releases/tag/v9.15) |
| CP-SAT's Python API was renamed to snake_case in 9.9 (issue against 9.9.3963, milestone v9.10) | verified | [Issue #4143](https://github.com/google/or-tools/issues/4143) |
| Whether CamelCase names survive in 9.15 (report: not found) | verified with a correction | They survive as deprecated aliases: `cp_model.py` at v9.15 has "# Compatibility with pre PEP8" and `_add_pre_pep8_methods`, and `CpSolver.SufficientAssumptionsForInfeasibility` is kept. The warning is off by default (`enable_warnings = False`). The original belief ("alongside" the old names) holds for 9.15. [cp_model.py at v9.15](https://github.com/google/or-tools/blob/v9.15/ortools/sat/python/cp_model.py) |
| `add_no_overlap`, `add_no_overlap_2d`, `add_cumulative`, `new_optional_interval_var`, `sufficient_assumptions_for_infeasibility` are current names | verified | [ortools.sat.python.cp_model API documentation](https://or-tools.github.io/docs/pdoc/ortools/sat/python/cp_model.html); cp_model.py at v9.15 |
| `num_workers`, `random_seed`, `max_time_in_seconds` are current names | verified with a correction | They are `SatParameters` fields set through `solver.parameters`, not `cp_model` methods. `num_workers` default 0 (all cores); `random_seed` default 1; `max_time_in_seconds` default inf. [sat_parameters.proto at v9.15](https://github.com/google/or-tools/blob/v9.15/ortools/sat/sat_parameters.proto) |
| "A NoOverlap constraint ensures that all present intervals do not overlap in time" | verified (a line break falls before "in time") | [cp_model API documentation](https://or-tools.github.io/docs/pdoc/ortools/sat/python/cp_model.html) |
| `add_cumulative` takes intervals plus demands | verified ("Adds Cumulative(intervals, demands, capacity).") | [cp_model API documentation](https://or-tools.github.io/docs/pdoc/ortools/sat/python/cp_model.html) |
| CP-SAT default uses all cores, including hyperthreads (report: Primer, secondary) | verified at the primary source | sat_parameters.proto: "A value of 0 means the solver will try to use all cores on the machine." The hyperthreading phrase is the Primer's |
| CP-SAT deterministic mode "not sourced" | verified (added) | sat_parameters.proto: `interleave_search`, "Experimental", "The search is deterministic (independently of num_workers!)" |
| #5582: CP-SAT 9.15.6755 reports OPTIMAL above the true optimum depending on the hint; 7 of 207 at 1 worker | verified. Opened 10 Nov 2026 23:03 UTC, open, no maintainer reply yet | [Issue #5582](https://github.com/google/or-tools/issues/5582) |
| #5582: INFEASIBLE on a model with a known solution, without a hint | verified | [Issue #5582](https://github.com/google/or-tools/issues/5582) |
| #5582 workaround `presolve_inclusion_work_limit: 0` | verified; the issue also lists `keep_all_feasible_solutions_in_presolve: true`, `cp_model_probing_level: 0`, `cp_model_presolve: false`, and says these are "empirical results on this sample" | [Issue #5582](https://github.com/google/or-tools/issues/5582) |
| #5141: `sufficient_assumptions_for_infeasibility()` returns a non-assumption literal with presolve on | verified. Open since 20 Apr 2026, labelled Bug, assigned lperron; also reproduces on 9.14.6206 and `main`. A maintainer wrote that "presolve and assumptions are currently a best effort support" | [Issue #5141](https://github.com/google/or-tools/issues/5141) |
| PR #5539 opened 28 Oct 2026 proposes a fix; tests replay the core without presolve | verified. Opened 2026-10-28T21:18Z, open; the CLA bot flagged it at opening | [PR #5539](https://github.com/google/or-tools/pull/5539) |
| HiGHS 1.15.1 (2 Jul 2026) is the current release | contradicted | HiGHS 1.16.0 came out today: highspy 1.16.0 uploaded to PyPI 2026-11-11T15:12Z, and tag v1.16.0 exists. 1.15.1's date (2 Jul 2026) is right. [highspy JSON on PyPI](https://pypi.org/pypi/highspy/json); `git ls-remote` |
| HiGHS 1.15 shipped the first parallel MIP solver (1.15.0, 28 Jun 2026) | verified | [Releases · ERGO-Code/HiGHS](https://github.com/ERGO-Code/HiGHS/releases) |
| HiGHS 1.15 fixed IIS bugs (`Highs::getIis`) | verified at the primary source (report used newreleases.io) | [Releases · ERGO-Code/HiGHS](https://github.com/ERGO-Code/HiGHS/releases) |
| HiGHS is MIT; release binaries come as "-mit" and "-apache" builds, the Apache one with HiPO | verified; `highspy-extras` "is distributed under the Apache 2.0 license" | [LICENSE.txt](https://raw.githubusercontent.com/ERGO-Code/HiGHS/latest/LICENSE.txt); [highs.dev](https://highs.dev/); v1.15.1 release assets |
| SciPy's `linprog` and `milp` use HiGHS | verified at the primary source; the 1.6.0 and 1.9.0 version numbers remain secondary (Wikipedia) | [scipy/optimize/_milp.py](https://github.com/scipy/scipy/blob/main/scipy/optimize/_milp.py): "`milp` is a wrapper of the HiGHS linear optimization software"; `_linprog.py` default `method='highs'` |
| HiGHS is MATLAB's default from 2024a, per Mittelmann | unverifiable | Not on the milp.html page as fetched; no other source checked |
| Mittelmann MILP (7 Jul 2026): COPT 219, HiGHSp 179 (scaled 5.44), HiGHS 158, SCIP 136 of 240 | verified with a correction | The page is now dated 28 Oct 2026, with COPT-9.0.0 at 225 solved, HiGHSp 179 (scaled 7.69), HiGHS 158, SCIP 136, OPTV 210, FSCIP 158, SCIPCO 160. [Mittelmann MIPLIB2017 benchmark](https://plato.asu.edu/ftp/milp.html) |
| Mittelmann's MILP table omits Gurobi and CPLEX | verified | [Mittelmann MIPLIB2017 benchmark](https://plato.asu.edu/ftp/milp.html) |
| Mittelmann infeasibility (26 Jul 2026): CBC 20, HiGHS 25, SCIP 22 of 32 | verified; COPT 30; CBC is 2.10.5 | [Infeasibility Detection for MILP Problems](https://plato.asu.edu/ftp/infeas.html) |
| SCIP 10.0.0 released 24 Nov 2025 | verified (Zenodo publication_date 2025-11-24, licence apache2.0) | [scipopt/scip: v10.0.0](https://zenodo.org/records/17700258) |
| SCIP Optimization Suite 10.1.0 (Sep 2026) is current | verified | [SCIP news](https://scipopt.org/); tag v10.1.0; [download page](https://scipopt.org/download.php) lists SCIP 10.1.0 first |
| SCIP 10.0, SoPlex 8.0, PaPILO 3.0, GCG 4.0 Apache-2.0; Zimpl 3.7.0 and UG 1.0 LGPL | verified (for the 10.0 suite; 10.1.0 ships ZIMPL 3.8.0 and UG 1.1.0, whose licences were not checked) | [The SCIP Optimization Suite 10.0](https://arxiv.org/html/2511.18580v1) |
| "The Apache 2.0 License applies from Version 8.0.3 onwards." | verified | [SCIP download](https://scipopt.org/download.php) |
| SCIP 10 integrates IIS detection for MIPs (report: secondary) | verified at the primary source | arXiv 2511.18580 section 3.9 "IIS Finder"; the quoted wording is the [Pokutta blog](https://www.pokutta.com/blog/research/2025/12/02/scip-10.html)'s |
| SCIP 10 exact mode produces "verifiable certificates" | secondary only | [Pokutta blog](https://www.pokutta.com/blog/research/2025/12/02/scip-10.html); the arXiv abstract confirms only "a new solving mode for exactly solving rational mixed-integer linear programs" |
| PuLP latest is 4.2.0, 22 Oct 2026 | verified (upload 2026-10-22T10:40Z) | [pulp JSON on PyPI](https://pypi.org/pypi/pulp/json) |
| PuLP docs show 4.3.0 (report: contested) | verified with a correction | 4.3.0 is the unreleased version on `master` (`pyproject.toml` `version = "4.3.0"`); the docs build from it. No 4.3.0 tag or PyPI release |
| PuLP 4.0.0 released Sep 2026 | verified (25 Sep 2026) | PyPI JSON |
| PuLP 4.x does not include CBC; `PULP_CBC_CMD` removed | verified | [Installing PuLP at Home](https://www.coin-or.org/pulp/main/installing_pulp_at_home.html) |
| PuLP 4.x requires Python 3.12 or newer | verified (PyPI `requires_python` ">=3.12") | same page; PyPI JSON |
| Install with `pulp[cbc]`, solve with `COIN_CMD` | verified | same page; `pulp/apis/__init__.py` at 4.2.0 |
| PuLP 3.x (to 3.3.2, 25 May 2026) still bundled CBC | verified | The 3.3.2 wheel holds `pulp/solverdir/cbc/linux/arm64/cbc` and the other platforms' binaries. 3.3.2 requires Python >=3.10, so the report's "Python 3.9–3.11 users stay on PuLP 3.x" holds for 3.10 and 3.11 only |
| PuLP licence (report: not confirmed) | verified: MIT | PyPI `license_expression` "MIT"; `pyproject.toml` `license = "MIT"`; [LICENSE](https://github.com/coin-or/pulp/blob/master/LICENSE) |
| PuLP 4 has a Rust core `pulp._rustcore` | verified | Installing PuLP at Home |
| PuLP 4 adds a `TimeLimit` status (report: secondary) | verified at the primary source | [constants.py at 4.2.0](https://github.com/coin-or/pulp/blob/4.2.0/pulp/constants.py): `TimeLimit = -4` |
| Pyomo latest 6.10.1, 4 Jun 2026 | verified. The report's URL (pypi.org/project/pyomo/4.1.10505/) is an old release's page; use pypi.org/project/pyomo/ | [pyomo JSON on PyPI](https://pypi.org/pypi/pyomo/json); [CHANGELOG.md](https://github.com/Pyomo/pyomo/blob/main/CHANGELOG.md) "Pyomo 6.10.1 (04 Jun 2026)" |
| Pyomo 6.10 removed Python 3.9 support | verified (6.10.0, 20 Feb 2026; PyPI `requires_python` ">=3.10") | [RELEASE.md](https://github.com/Pyomo/pyomo/blob/main/RELEASE.md) |
| Pyomo "ongoing solver interface refactor" (v2) | verified ("v2: Ongoing solver interface refactor") | [RELEASE.md](https://github.com/Pyomo/pyomo/blob/main/RELEASE.md) |
| Pyomo is BSD-3-Clause | verified | PyPI `license_expression` "BSD-3-Clause" |
| Timefold Solver 2.0.0 released 22 Apr 2026 | verified | Maven Central file date 2026-04-22; [Timefold Solver 2.0 blog](https://timefold.ai/blog/timefold-solver-2-0-release) |
| Timefold Solver 2.0.0 is current | contradicted | Current is 2.8.0, released 3 Nov 2026 (Maven Central `<release>2.8.0</release>`; GitHub release 03 Nov). 2.1 to 2.7.1 came between. [maven-metadata.xml](https://repo1.maven.org/maven2/ai/timefold/solver/timefold-solver-core/maven-metadata.xml) |
| Timefold forked from OptaPlanner on 20 April 2023 | verified | [README](https://github.com/TimefoldAI/timefold-solver/blob/main/README.md) |
| Timefold 1.x end of life in early 2027 | verified. 1.35.0 (15 Oct 2026) says "This is the penultimate release before Timefold Solver 1.x reaches end of life." | [v1.34.0 release](https://github.com/TimefoldAI/timefold-solver/releases/tag/v1.34.0) (3 Aug 2026); [Releases](https://github.com/TimefoldAI/timefold-solver/releases) |
| Timefold 1.x gets quarterly maintenance releases through 2026 | verified | [Timefold Solver 2.0 blog](https://timefold.ai/blog/timefold-solver-2-0-release) |
| Timefold Community Edition stays Apache-2.0 | verified | README; Maven POM licence "The Apache Software License, Version 2.0" |
| Upgrade guide: ScoreExplanation removed, ScoreAnalysis "provided exclusively by Timefold Solver Enterprise Edition" | verified | [Upgrade from Timefold Solver 1.x to 2.x](https://docs.timefold.ai/timefold-solver/latest/upgrading-timefold-solver/upgrade-from-v1) |
| Release blog: "Explainability moves to Timefold Solver Plus, a new paid edition" | verified as written on 22 Apr 2026 | [Timefold Solver 2.0 blog](https://timefold.ai/blog/timefold-solver-2-0-release) |
| Which paid edition holds explainability (report: contested) | verified with a correction | Today Timefold names two editions, Community and Enterprise; "Plus" no longer appears. The README says "There are two editions of Timefold Solver", the licence page says "One Solver. Two editions." and lists Score Analysis under Solver Enterprise, and the 2.8.0 docs say "This feature is exclusive to Timefold Solver Enterprise Edition." [Timefold License Manager](https://licenses.timefold.ai/); [Understanding the score](https://docs.timefold.ai/timefold-solver/latest/constraints-and-score/understanding-the-score) |
| Timefold 2.x needs Java 21 | verified | Upgrade guide: "Timefold Solver 2.x requires Java 21 or later to run" |
| Timefold 2.0 removes all deprecated methods; adds the Neighborhoods API | verified | Timefold Solver 2.0 blog |
| Timefold 2.0 removed indictments (implied by the report's mistake 9) | verified with a correction | 2.8.0 (3 Nov 2026): "Indictments are back, and better than before!", as part of Score Analysis (still Enterprise). [Releases](https://github.com/TimefoldAI/timefold-solver/releases) |
| Timefold OpenRewrite migration recipe `timefold-solver-migration` | verified (now at 2.8.0) | Upgrade guide command `ai.timefold.solver:timefold-solver-migration:2.8.0` |
| Gurobi 13.0 supported until Nov 2028 | verified | [What's New](https://www.gurobi.com/product/whats-new); [Gurobi release and support history](https://support.gurobi.com/hc/en-us/articles/360048138771-Gurobi-release-and-support-history) |
| Gurobi 13.0.3, 8/2026, Actively Supported to 11/2028 | verified (page updated 26 Aug 2026) | Gurobi release and support history |
| Each major release supported for three years | verified | Gurobi release and support history |
| Gurobi 12.x end of support 11/2027; 11.x 11/2026 | verified | Gurobi release and support history |
| Gurobi 14.0.0b1 on PyPI 28 Sep 2026 | verified | [gurobipy JSON on PyPI](https://pypi.org/pypi/gurobipy/json) |
| Gurobi 14.0 GA "expected around Dec 2026" | contradicted | gurobipy 14.0.0 (final) was uploaded to PyPI 2026-11-10T13:04Z, and the Gurobi reference manual's `current` release notes are now "Additions, Changes, and Removals in Gurobi 14.0". The support history page has no 14.0 row yet. The 1 and 3 Dec 2026 webinar is verified. [What's New in 14.0 webinar](https://www.gurobi.com/resources/webinar-events/what-is-new-in-14.0-webinar) |
| Gurobi 13 "~16% faster solves on difficult MIP models" | verified (vendor claim) | What's New |
| Gurobi 13 resumed-MIP log shows "the total, accumulated time and work spent" | verified | [Gurobi 13.0 release notes](https://docs.gurobi.com/projects/optimizer/en/13.0/reference/releasenotes/changes.html) |
| Gurobi 13 "improves the NoRel heuristic by allowing it to use variable hints" | verified with a correction | The FAQ wording was not checked; the release notes say "The NoRel heuristic now takes user-provided variable hints (see the VarHintVal attribute) into account." |
| CPLEX 22.1.2 (Dec 2024) is current; 22.2 on PyPI only | contradicted | CPLEX Optimization Studio 22.2.x reached General Availability on 22 May 2026, with a 22.2.0.1 fix; PyPI `cplex` 22.2.0.1 uploaded 15 Jul 2026. [IBM ILOG CPLEX Optimization Studio 22.2.x](https://www.ibm.com/support/pages/ibm-ilog-cplex-optimization-studio222x) |
| CPLEX 22.1.x end of support (report: not found; at least Mar 2027) | verified with a correction | IBM's lifecycle page (updated 13 Oct 2026): "Transition to Extended/Sustained or End of Support: 30-Sep-2027", extended support to 30-Sep-2031. [IBM ILOG CPLEX Optimization Studio 22.1.x](https://www.ibm.com/support/pages/ibm-ilog-cplex-optimization-studio221x) |
| CPLEX 22.2.x lifecycle | verified (added) | "Support Cycle-3: 3 years of support with critical fix extension of 1 year and usage and existing fixes for 3 (3+1+3)" |
| CBC 2.10.13 is the latest release | unverifiable | Tag `releases/2.10.13` is the newest release tag, but Zenodo also lists "coin-or/Cbc: Release v2.933" (14 Aug 2026) whose tag is not in the repository. Release dates not checked |
| CBC is EPL-2.0 (report: secondary) | verified | [Cbc LICENSE](https://github.com/coin-or/Cbc/blob/master/LICENSE): "Eclipse Public License - v 2.0" |
| MiniZinc bundle is 2.10.1 | verified; 2.10.1 released 31 Aug 2026 | [MiniZinc Downloads](https://www.minizinc.org/downloads/); [changes.rst](https://github.com/MiniZinc/libminizinc/blob/master/changes.rst) |
| MiniZinc 2.10.0 released 23 Jul 2026 | verified | changes.rst |
| MiniZinc handbook shows 2.10.2 (report: contested) | verified with a correction | No 2.10.2 tag or changelog entry exists; the latest tags are 2.10.0 and 2.10.1. 2.10.1 is the current release |
| MiniZinc licence (report: not confirmed) | verified: MPL-2.0 | [LICENSE.txt](https://github.com/MiniZinc/libminizinc/blob/master/LICENSE.txt) |
| MiniZinc 2.9.6 added `--cleanup-time-limit` and removed SCIP 7 and earlier | verified (2.9.6 released 24 Apr 2026) | changes.rst |
| HSG256 (2006): error and accident risk higher at night, over 8 hours, over successive shifts, without enough breaks | verified. The report's ellipsis drops "especially if they are night shifts" | [HSG256 Managing shiftwork (PDF)](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/390908/hsg256_managing_shift_work.pdf), paragraph 31 |
| HSG256: "no single optimal shift system that suits everyone" | verified | HSG256 paragraph 66 |
| HSG256 recommends the Fatigue and Risk Index Tool | verified | HSG256 paragraph 64 |
| HSG256: limited evidence for forward rotation | verified | HSG256 table, "Forward versus backward rotation" |
| HSG256: concentration and productivity decline at end of shift, after lunch, at night | verified | HSG256 table, workload row |
| HSG256: WTR compliance "may not in itself be enough to prevent fatigue" | verified | HSG256 paragraph 67 |
| HSG256 is © Crown copyright 2006, "All rights reserved" | verified | HSG256 page 2 |
| ISO 10075-1:2017 and 10075-3:2004 current | verified (stages 90.93 and 90.92) | [ISO/TC 159/SC 1 catalogue](https://www.iso.org/committee/53352/x/catalogue/) |
| ISO 10075-2:2024 replaces the 1996 edition | verified (edition 2, 2024-07; 1996 withdrawn) | [ISO 10075-2:2024](https://www.iso.org/standard/76686.html) |
| ISO 10075-3 revision at working draft (stage 20.60) | contradicted | The catalogue lists "ISO/AWI 10075-3 [Under development]" at stage 10.99 (new project approved), not 20.60. ISO/TC 159/SC 1 catalogue |
| Little (2011): "If limits λ and W exist and are finite, L exists and is finite, and L = λW" | verified (the sample-path theorem) | [Little's Law as Viewed on Its 50th Anniversary](https://pubsonline.informs.org/doi/10.1287/opre.1110.0940), Operations Research 59(3):536–549; read from the [course-site PDF](https://people.cs.umass.edu/~emery/classes/cmpsci691st/readings/OS/Littles-Law-50-Years-Later.pdf) |
| Little: numerically exact over a finite window; no stationarity or queue discipline needed | verified | same paper, sections 1 and 2 |
| Kingman (1961) G/G/1 heavy-traffic result | verified (citation) | [The single server queue in heavy traffic](https://doi.org/10.1017/S0305004100036094), Math. Proc. Cambridge Philos. Soc. 57(4):902–904, Oct 1961 (Crossref) |
| Kingman formula Wq ≈ (ρ/(1−ρ))·((ca²+cs²)/2)·te and "generally very accurate" | secondary only | [Kingman's formula (Wikipedia)](https://en.wikipedia.org/wiki/Kingman%27s_formula); the paper itself was not read |
| Wright, "Factors Affecting the Cost of Airplanes", J. Aeronautical Sciences 3(4):122–128, Feb 1936 | verified | [doi:10.2514/8.155](https://doi.org/10.2514/8.155) (Crossref) |
| Jaber & Bonney (1996) learn–forget curve model | verified with a correction | The paper is "Production breaks and the learning curve: The forgetting phenomenon", Applied Mathematical Modelling 20(2):162–169 ([doi:10.1016/0307-904X(95)00157-F](https://doi.org/10.1016/0307-904X(95)00157-F)); the report's source [34] is a different, citing paper |
| Nembhard & Uzumeri (2000) individual learning and forgetting | verified (citation) | [Experiential learning and forgetting for manual and cognitive tasks](https://doi.org/10.1016/S0169-8141(99)00021-9), Int. J. Industrial Ergonomics 25(4):315–326 |
| Anzanello & Fogliatto (2011) "fast learners to short duration tasks" | secondary only | As quoted by a citing paper; not checked |
| Wiers (2009): "a disagreement concerning autonomy is a key explanatory factor for understanding why an APS implementation may fail" | verified with a correction | Quote is in the abstract of "The relationship between shop floor autonomy and APS implementation success: evidence from two cases", PPC 20(7):576–585 ([doi:10.1080/09537280903034289](https://doi.org/10.1080/09537280903034289)). The report's link [69] is a different paper (Kjellsdotter Ivert & Jonsson 2010, IMDS) |
| Ivert (2012) quotes on operation times and schedules being ignored | unverifiable | Full text paywalled and not reachable; the abstract has neither sentence. Citation verified: PPC 23(6):452–467 ([doi:10.1080/09537287.2011.564218](https://doi.org/10.1080/09537287.2011.564218)). The author's thesis has a similar sentence: "operation times in the schedule did not correspond to real operation times" |
| CONWIP: "This paper describes a new pull-based production system called CONWIP." (1990) | verified | [CONWIP: a pull alternative to kanban](https://www.tandfonline.com/doi/abs/10.1080/00207549008942761), IJPR 28(5):879–894 |
| Factory Physics 3rd ed., reissued by Waveland 2011, ISBN 9781577667391 | verified | [WorldCat OCLC 718450337](https://search.worldcat.org/title/718450337): "Reissue of 3rd ed. previously published: New York, NY : McGraw-Hill/Irwin/Irwin, 2008" |
| CP-SAT one worker runs no LNS (Primer) | secondary only, confirmed at the secondary source | [CP-SAT Primer: Parameters](https://d-krupke.github.io/cpsat-primer/parameters.html) |
| Perron: "The solver is designed to work with 8+ workers, unless for trivial models" | verified | [Discussion #3630](https://github.com/google/or-tools/discussions/3630) (10 Jan 2023) |
| Timefold 1.4.0 score analysis quote; `@PlanningPinToIndex` newsletter quote; Gurobi on Anaconda; GAMS MIPfeas; Mittelmann MIPfeas date; Timefold 1.0 July 2023 | unverifiable | Not checked in this run |

Counts, one per row by its main status: 81 verified, 11 verified with a correction, 5 contradicted,
4 unverifiable, 4 secondary only (105 rows).

## Exact quotes for facts rows

Each quote is as it appears at the source. Non-ASCII characters are noted.

| Fact | URL | Exact quote |
|---|---|---|
| OR-Tools languages | https://github.com/google/or-tools/blob/v9.15/README.md | "We wrote OR-Tools in C++, but provide wrappers in Python, C# and Java." |
| OR-Tools 9.15 bundled HiGHS | https://github.com/google/or-tools/releases/tag/v9.15 | "HiGHS=v1.12.0" |
| OR-Tools 9.15 bundled SCIP | https://github.com/google/or-tools/releases/tag/v9.15 | "SCIP=v10.0.0" |
| CP-SAT snake_case rename (9.9) | https://github.com/google/or-tools/issues/4143 | "It seems that the new version has renamed all the python methods from PascalCase to camel case." |
| CP-SAT CamelCase kept as aliases | https://github.com/google/or-tools/blob/v9.15/ortools/sat/python/cp_model.py | "# Compatibility with pre PEP8" |
| CP-SAT no-overlap | https://or-tools.github.io/docs/pdoc/ortools/sat/python/cp_model.html | "A NoOverlap constraint ensures that all present intervals do not overlap in time." (a line break before "in time") |
| CP-SAT cumulative | https://or-tools.github.io/docs/pdoc/ortools/sat/python/cp_model.html | "Adds Cumulative(intervals, demands, capacity)." |
| CP-SAT core method | https://github.com/google/or-tools/blob/v9.15/ortools/sat/python/cp_model.py | "Returns the indices of the infeasible assumptions." |
| CP-SAT default workers | https://github.com/google/or-tools/blob/v9.15/ortools/sat/sat_parameters.proto | "A value of 0 means the solver will try to use all cores on the machine." |
| CP-SAT one worker | https://github.com/google/or-tools/blob/v9.15/ortools/sat/sat_parameters.proto | "A number of 1 means no parallelism." |
| CP-SAT time limit | https://github.com/google/or-tools/blob/v9.15/ortools/sat/sat_parameters.proto | "Maximum time allowed in seconds to solve a problem." |
| CP-SAT deterministic parallel option | https://github.com/google/or-tools/blob/v9.15/ortools/sat/sat_parameters.proto | "The search is deterministic (independently of num_workers!), and we" (sentence continues on the next line) |
| CP-SAT wrong OPTIMAL (#5582) | https://github.com/google/or-tools/issues/5582 | "At 1 worker, 7 of the 207 reported OPTIMAL above a known feasible value, and 2 of 1,242 at 8 workers (6 passes)." |
| CP-SAT wrong INFEASIBLE (#5582) | https://github.com/google/or-tools/issues/5582 | "CP-SAT returns INFEASIBLE although a known solution, with every variable fixed to it, is OPTIMAL." |
| CP-SAT core bug (#5141) | https://github.com/google/or-tools/issues/5141 | "it returns a literal index that was never passed to CpModel.add_assumptions(...)" (the method name is in code formatting on the page) |
| CP-SAT assumptions under presolve (#5141) | https://github.com/google/or-tools/issues/5141 | "Yes, presolve and assumptions are currently a best effort support, we will need to improve that, but it might not happen soon." |
| PR #5539 tests | https://github.com/google/or-tools/pull/5539 | "Each case checks that the core is a subset of the original assumptions, is sufficient for infeasibility when replayed without presolve" (line breaks in the source) |
| CP-SAT workers (Perron) | https://github.com/google/or-tools/discussions/3630 | "The solver is designed to work with 8+ workers, unless for trivial models." |
| CP-SAT all cores (Primer) | https://d-krupke.github.io/cpsat-primer/parameters.html | "By default, CP-SAT leverages all available cores (including hyperthreading)." |
| CP-SAT LNS from two workers (Primer) | https://d-krupke.github.io/cpsat-primer/parameters.html | "With a single worker, only the default subsolver is used." |
| HiGHS parallel MIP | https://github.com/ERGO-Code/HiGHS/releases/tag/v1.15.0 | "This is the first release of the parallel MIP solver." |
| HiGHS IIS fixes | https://github.com/ERGO-Code/HiGHS/releases/tag/v1.15.0 | "several bugs in the computation of an Irreducible Infeasible Subsystem (IIS) via Highs::getIis were fixed" (`Highs::getIis` in code formatting) |
| HiGHS licence | https://highs.dev/ | "HiGHS is freely available under the MIT licence" |
| SciPy milp uses HiGHS | https://github.com/scipy/scipy/blob/main/scipy/optimize/_milp.py | "`milp` is a wrapper of the HiGHS linear optimization software" (backticks as in the docstring) |
| SCIP suite licences (10.0) | https://arxiv.org/html/2511.18580v1 | "SCIP 10.0, SoPlex 8.0, PaPILO 3.0, and GCG 4.0 are licensed under the Apache 2.0 license, whereas Zimpl 3.7.0 and UG 1.0 make use of the GNU Lesser General Public License." |
| SCIP Apache from 8.0.3 | https://scipopt.org/download.php | "The Apache 2.0 License applies from Version 8.0.3 onwards." |
| SCIP 10.1.0 suite | https://scipopt.org/ | "The SCIP Optimization Suite 10.1.0 consists of SCIP 10.1.0, GCG 4.1.0, SoPlex 8.1.0, ZIMPL 3.8.0, PaPILO 3.0.2 and UG 1.1.0." |
| Mittelmann MILP columns (28 Oct 2026) | https://plato.asu.edu/ftp/milp.html | "COPT   SCIP HiGHSp  HiGHS  OPTV FSCIP SCIPCO" (spacing as in the preformatted table) |
| Mittelmann MILP solved (28 Oct 2026) | https://plato.asu.edu/ftp/milp.html | "solved   225    136    179    158   210   158   160" |
| Mittelmann infeasibility solved (26 Jul 2026) | https://plato.asu.edu/ftp/infeas.html | "solved: 20 30 25 22 27 30 28" (columns CBC COPT HiGHS SCIP SCIPC XOPT XSMOO; spacing collapsed in the fetched copy) |
| PuLP drops CBC | https://www.coin-or.org/pulp/main/installing_pulp_at_home.html | "CBC is not included inside the PuLP wheel." |
| PuLP drops PULP_CBC_CMD | https://www.coin-or.org/pulp/main/installing_pulp_at_home.html | "The legacy PULP_CBC_CMD solver (which pointed at a CBC binary shipped inside the package) has been removed." |
| PuLP Python floor | https://www.coin-or.org/pulp/main/installing_pulp_at_home.html | "PuLP requires Python 3.12 or newer." |
| PuLP time-limit status | https://github.com/coin-or/pulp/blob/4.2.0/pulp/constants.py | "TimeLimit = -4" |
| Pyomo 6.10 drops 3.9 | https://github.com/Pyomo/pyomo/blob/main/RELEASE.md | "Removed support for Python 3.9" |
| Pyomo solver refactor | https://github.com/Pyomo/pyomo/blob/main/RELEASE.md | "v2: Ongoing solver interface refactor" |
| Timefold fork date | https://github.com/TimefoldAI/timefold-solver/blob/main/README.md | "Timefold Solver was forked on 20 April 2023 from OptaPlanner," |
| Timefold Community licence | https://github.com/TimefoldAI/timefold-solver/blob/main/README.md | "The Community Edition (this repo) is open-source and licensed under the Apache-2.0 license." |
| Timefold 1.x end of life | https://github.com/TimefoldAI/timefold-solver/releases/tag/v1.34.0 | "Only 2 more of these are planned before Timefold Solver 1.x EOL in early 2027." |
| Timefold 1.35.0 penultimate | https://github.com/TimefoldAI/timefold-solver/releases/tag/v1.35.0 | "This is the penultimate release before Timefold Solver 1.x reaches end of life." |
| Timefold score analysis paid | https://docs.timefold.ai/timefold-solver/latest/upgrading-timefold-solver/upgrade-from-v1 | "ScoreExplanation has been removed. Use ScoreAnalysis instead, which is now provided exclusively by Timefold Solver Enterprise Edition." (class names in code formatting) |
| Timefold score analysis edition (2.8.0 docs) | https://docs.timefold.ai/timefold-solver/latest/constraints-and-score/understanding-the-score | "This feature is exclusive to Timefold Solver Enterprise Edition." |
| Timefold 2.x Java floor | https://docs.timefold.ai/timefold-solver/latest/upgrading-timefold-solver/upgrade-from-v1 | "Timefold Solver 2.x requires Java 21 or later to run, whereas Timefold Solver 1.x supported Java 17 and later." |
| Timefold 1.x maintenance | https://timefold.ai/blog/timefold-solver-2-0-release | "Timefold Solver 1.x is maintained throughout 2026 with quarterly bug-fix and security releases" |
| Gurobi support term | https://support.gurobi.com/hc/en-us/articles/360048138771-Gurobi-release-and-support-history | "Starting with major release 10, all Gurobi product releases are supported for a term of three years after the initial release of the corresponding major release." |
| Gurobi 13 support end | https://www.gurobi.com/product/whats-new | "Gurobi version 13.0 (released in November 2025) and minor releases will be supported until November 2028." |
| Gurobi 11.x support end | https://support.gurobi.com/hc/en-us/articles/360048138771-Gurobi-release-and-support-history | "11.0.3 \| 07/2024 \| Supported \| 11/2026" (table row) |
| Gurobi 13 log change | https://docs.gurobi.com/projects/optimizer/en/13.0/reference/releasenotes/changes.html | "With Gurobi 13, this log line displays the total, accumulated time and work spent on solving the given MIP model" |
| CPLEX 22.1.x end of support | https://www.ibm.com/support/pages/ibm-ilog-cplex-optimization-studio221x | "Transition to Extended/Sustained or End of Support" with value "30-Sep-2027" (label and value are separate fields) |
| CPLEX 22.2.x GA | https://www.ibm.com/support/pages/ibm-ilog-cplex-optimization-studio222x | "General Availability" with value "22-May-2026 , AD26-0264" (separate fields; space before the comma as shown) |
| MiniZinc 2.10.1 date | https://github.com/MiniZinc/libminizinc/blob/master/changes.rst | "(released 31 August 2026)" |
| MiniZinc 2.10.0 date | https://github.com/MiniZinc/libminizinc/blob/master/changes.rst | "(released 23 July 2026)" |
| MiniZinc licence | https://github.com/MiniZinc/libminizinc/blob/master/LICENSE.txt | "released under the Mozilla Public License Version 2.0" |
| HSG256 error risk, night | HSG256 PDF (URL above), para. 31 | "The risk of errors, accidents and injuries has been found:" then the list item "to be higher on the night shift;" |
| HSG256 error risk, length | same, para. 31 | "to rise with increasing shift length over eight hours;" |
| HSG256 error risk, succession | same, para. 31 | "to increase over successive shifts, especially if they are night shifts;" |
| HSG256 error risk, breaks | same, para. 31 | "to increase when there are not enough breaks." (followed by reference numbers 18,22) |
| HSG256 no optimal system | same, para. 66 | "there is no single optimal shift system that suits everyone" |
| HSG256 FRI | same, para. 64 | "You may find it useful to use assessment tools such as HSE’s Fatigue and Risk Index Tool" (curly apostrophe U+2019 in HSE’s) |
| HSG256 forward rotation | same, Table, rotation row | "There is limited evidence that the internal body clock adapts more quickly to forward-rotating schedules" |
| HSG256 time of day | same, Table, workload row | "Concentration and productivity tend to decline towards the end of the shifts, following lunch and during the night and early hours of the morning." |
| HSG256 WTR not enough | same, para. 67 | "complying with WTR may not in itself be enough to prevent fatigue" |
| ISO 10075-2:2024 replaces 1996 | https://cdn.standards.iteh.ai/samples/76686/51d8c133dbc44726b47796bf352d5ea6/ISO-10075-2-2024.pdf (the standard's own foreword, in iTeh's preview of the ISO PDF) | "This second edition cancels and replaces the first edition (ISO 10075-2:1996), which has been technically revised." |
| Little's law conditions | https://pubsonline.informs.org/doi/10.1287/opre.1110.0940 | "If limits λ and W exist and are finite, L exists and is finite, and L = λW." (Greek λ, U+03BB) |
| Little's law, no stationarity | same | "LL.1 holds under nonstationary conditions." |
| Little's law, queue discipline | same | "LL.1 holds independent of queue discipline." |
| Little's law, finite window | same | "the finite time interval guarantees that the relationship L = λW is numerically exact" (Greek λ) |
| Wiers 2009 | https://doi.org/10.1080/09537280903034289 | "a disagreement concerning autonomy is a key explanatory factor for understanding why an APS implementation may fail" |
| CONWIP origin | https://doi.org/10.1080/00207549008942761 | "This paper describes a new pull-based production system called CONWIP." |

## Versions found from registries

| Tool | Current version | Released | Read from |
|---|---|---|---|
| OR-Tools (ortools) | 9.15.6755 (tag v9.15) | 14 Jan 2026 on PyPI; GitHub release 12 Jan 2026 | PyPI JSON; GitHub releases |
| HiGHS (highspy) | 1.16.0 | 11 Nov 2026 (15:12 UTC); before it 1.15.1, 2 Jul 2026 | PyPI JSON; tag v1.16.0 |
| SCIP Optimization Suite | 10.1.0 (SCIP 10.1.0, SoPlex 8.1.0, GCG 4.1.0) | Sep 2026 | scipopt.org news; tag v10.1.0 |
| PySCIPOpt | 6.3.0 | 11 Oct 2026 | PyPI JSON |
| PuLP | 4.2.0 (4.3.0 unreleased on master) | 22 Oct 2026 | PyPI JSON; tags |
| Pyomo | 6.10.1 | 4 Jun 2026 | PyPI JSON; CHANGELOG.md |
| gurobipy | 14.0.0 | 10 Nov 2026 (13:04 UTC); 13.0.3 on 25 Aug 2026 | PyPI JSON |
| CPLEX (cplex) | 22.2.0.1 | 15 Jul 2026; Optimization Studio 22.2.x GA 22 May 2026 | PyPI JSON; IBM lifecycle page |
| docplex | 2.32.264 | 1 Apr 2026 | PyPI JSON |
| Timefold Solver | 2.8.0 | 3 Nov 2026 | Maven Central metadata and file date |
| Timefold Solver 1.x | 1.35.0 | 15 Oct 2026 | Maven Central file date |
| MiniZinc | 2.10.1 | 31 Aug 2026 | changes.rst; tags; downloads page |
| CBC | releases/2.10.13 tag (date not checked) | not checked | `git ls-remote` |

## Licences

| Source | Licence as the source states it | What an Apache-2.0 repository may do |
|---|---|---|
| OR-Tools code, release notes, pdoc API docs | Apache License 2.0 (LICENSE at v9.15). The repository's own run 2026-09-23-A records the developers.google.com docs as CC BY 4.0; not re-checked today | Quote and paraphrase; adapt code keeping the licence and NOTICE, marking changes |
| HiGHS | MIT ("MIT License", LICENSE.txt); `highspy-extras` Apache 2.0 | Quote, paraphrase; adapt code keeping the MIT notice |
| SCIP 10.x and SoPlex, PaPILO, GCG | Apache 2.0 (LICENSE; download page; Zenodo `apache2.0`) | Quote, paraphrase; adapt code with notice |
| SCIP 10.0 report (arXiv 2511.18580) | arXiv non-exclusive distribution licence 1.0 | Brief quotes with citation; paraphrase |
| Zimpl, UG | GNU LGPL (per the 10.0 report) | Quote briefly; do not copy code into this repository |
| PuLP code | MIT (PyPI `license_expression`; LICENSE) | Quote, paraphrase; adapt code keeping the notice |
| PuLP docs | No licence stated beyond "© Copyright 2009-, pulp documentation team." | Brief quotes with a link; paraphrase |
| Pyomo | BSD-3-Clause (PyPI `license_expression`) | Quote, paraphrase; adapt code keeping the notice |
| Timefold Solver Community | Apache-2.0 (README; Maven POM) | Quote, paraphrase; adapt code with notice |
| Timefold docs and blog | No licence checked | Brief quotes with a link; paraphrase |
| MiniZinc (libminizinc) | Mozilla Public License 2.0 | Quote, paraphrase; MPL code may only come in as whole files that keep MPL-2.0 and their notices, so avoid copying it |
| CBC | Eclipse Public License 2.0 | Quote briefly; do not copy code |
| Gurobi docs and site | Proprietary (PyPI licence "Proprietary") | Brief quotes with attribution; paraphrase; no code |
| CPLEX | Proprietary, IBM International Program License Agreement; docplex is Apache 2.0 | Brief quotes; docplex code adaptable with notice |
| CP-SAT Primer | CC BY 4.0 ("licensed under the CC BY 4.0 license") | Quote, paraphrase and adapt with attribution and a link to the licence |
| Mittelmann benchmarks | None stated | Brief quotes of figures with author and date |
| HSE HSG256 | "© Crown copyright 2006", "All rights reserved" | Brief quotes with attribution; paraphrase |
| ISO 10075 parts | © ISO, paywalled | Titles, numbers and short abstract quotes only |
| Little 2011 (INFORMS), Kingman 1961 (CUP), Wright 1936 (AIAA), Spearman et al. 1990 (T&F), Wiers 2009 (T&F), Ivert 2012 (T&F) | Publisher copyright | Brief quotes with full citation; paraphrase |
| Wikipedia | CC BY-SA 4.0 | Quote and paraphrase with attribution; adapting brings share-alike, so avoid it |
| GitHub issues, PRs and discussions | GitHub terms; authors' copyright | Brief quotes with a link; do not copy reproduction scripts |

## Repository facts this contradicts

`git -C /home/user/claude-code-skills grep -n -i` for OR-Tools, ortools, HiGHS, highspy, SCIP,
PuLP, Pyomo, Timefold, OptaPlanner, Gurobi, CPLEX, MiniZinc, CP-SAT, Mittelmann, HSG256, 10075,
Little's law, Kingman, CONWIP and Factory Physics under `skills/` finds no Facts row on any of
them. The only hits are unrelated (`10075` inside a savannah.gnu.org URL in
`skills/coding/references/c-build.md` row `cb-fortify3`, and `100755` file modes in
`skills/git-workflows/references/git-hooks.md`). The `optimization-and-scheduling` skill is
still `planned` in `ROADMAP.md`. No Facts row in `skills/` is now wrong.

Outside `skills/`, `research/runs/2026-09-23-A-source-licences.md` row L9 records OR-Tools docs
as CC BY 4.0 and code as Apache 2.0; nothing found here contradicts it.

---

# R28: Optimization and scheduling, with the people in the plan

Five of the nine "What we believe" items need correcting. The biggest change is PuLP: from 4.0 it no longer ships CBC.\[1\] Others are wrong in detail: Little's law is not a "stable system" law;\[2\] HSE says the evidence for forward rotation is limited; ISO 10075-2 has a 2024 edition. Timefold 2.0 moved explainability out of the open-source edition.\[3\] Separately, two open OR-Tools 9.15 issues report CP-SAT returning a wrong "OPTIMAL" result or a wrong infeasibility core. Those reports are why the skill must check every plan with code that is independent of the solver.

**TL;DR**
- **Solver versions on 11 Nov 2026:** OR-Tools 9.15 (12 Jan 2026), HiGHS 1.15.1 (2 Jul 2026), SCIP 10.x (Apache-2.0; the SoPlex news page lists SCIP Optimization Suite 10.1.0 in Sep 2026), Gurobi 13.0.3 (Aug 2026, 14.0 arriving), Pyomo 6.10.1, PuLP 4.2.0 (CBC unbundled), Timefold Solver 2.0.0 (22 Apr 2026, 1.x end of life early 2027) and MiniZinc 2.10.x.
- **Never accept a solver's status as proof.** A filed CP-SAT 9.15 issue reports OPTIMAL above the true optimum and INFEASIBLE on a model with a known solution. Every plan needs an independent feasibility and objective checker, run against instance libraries with known optima.
- **People are not machines in the model.** HSE HSG256 says error risk rises on night shifts, with shift length over 8 hours, over successive shifts and without enough breaks. Kingman's heavy-traffic result says queues explode as utilisation nears 100%.\[4\] So a lead-time quote of "backlog ÷ daily capacity" is a floor, not a forecast.

## 1. Summary

- **OR-Tools v9.15** is the current release: tagged on GitHub 12 Jan 2026, on PyPI as 9.15.6755 on 14 Jan 2026, Apache-2.0.\[5\]\[6\] I found no newer release by 11 Nov 2026 and no announced date for one.
- **CP-SAT's Python API renamed its methods to snake_case in 9.9** (for example `add_no_overlap`, `new_interval_var`). Users reported confusion because the official examples and the prose disagreed.\[7\] Write new code in snake_case only.
- **Two open OR-Tools issues bear directly on "don't trust the solver".**
  - #5582 (CP-SAT 9.15.6755): "OPTIMAL reported above the true optimum depending on the solution hint".\[8\]
  - #5141: `sufficient_assumptions_for_infeasibility()` can return a literal that is not an assumption when presolve is on. PR #5539, opened 28 Oct 2026, proposes a fix.\[9\]\[10\]
- **HiGHS 1.15.1** (2 Jul 2026, MIT) is the current release. 1.15 shipped the first parallel MIP solver and fixed IIS bugs.\[11\]\[12\] On Mittelmann's MIPLIB2017 run of 7 Jul 2026, parallel HiGHS solved 179 of 240 instances, against SCIP 10's 136 and commercial COPT's 219.\[12\]\[13\]\[14\]\[15\]
- **SCIP 10.0** (24 Nov 2025) is Apache-2.0, as are SoPlex 8, PaPILO 3 and GCG 4; Zimpl and UG remain LGPL. SCIP 10 adds an exact rational MILP mode and IIS detection for MIPs.\[16\]\[17\]\[18\]
- **PuLP 4 (Sep–Oct 2026) is a breaking change.** It requires Python ≥ 3.12, no longer bundles CBC, and has removed `PULP_CBC_CMD`. Install with `pip install "pulp[cbc]"` and solve with `COIN_CMD`, or use HiGHS.\[1\]\[19\]\[20\]\[21\]
- **Timefold Solver 2.0.0** shipped on 22 Apr 2026 and Community Edition stays Apache-2.0.\[22\]\[23\] The 1.x line gets quarterly maintenance releases through 2026 and reaches end of life in early 2027.\[24\]\[25\] Timefold's own upgrade guide says "ScoreExplanation has been removed. Use ScoreAnalysis instead, which is now provided exclusively by Timefold Solver Enterprise Edition", while its 2.0 release blog says "Starting with 2.0, Explainability moves to Timefold Solver Plus, a new paid edition" — so explainability is now paid-only, though the two pages name the edition differently.
- **Gurobi 13.0.x** is supported until Nov 2028. Gurobi 14.0.0b1 reached PyPI on 28 Sep 2026, 14.0.0 is on Gurobi's Anaconda channel (updated 10 Nov 2026), and Gurobi has a "What's New in 14.0" webinar on 1 and 3 Dec 2026.\[26\]\[27\]\[28\]\[29\]
- **Mittelmann's benchmarks now omit Gurobi and CPLEX** from the MIPLIB2017 MILP table (7 Jul 2026). Use them to rank open-source solvers and COPT, not to compare against Gurobi.\[13\]
- **ISO 10075 is three parts with different dates:** Part 1:2017, Part 2:2024 (replacing 1996), Part 3:2004 (a revision is at working-draft stage).\[30\]
- **HSE HSG256 (2006)** says the risk of errors and accidents is higher on the night shift, rises with shift length over eight hours and over successive shifts, and rises when there are not enough breaks. It recommends the Fatigue and Risk Index tool, and states there is "no single optimal shift system".\[31\]
- **Little's law needs only that long-run averages exist and are finite.** It holds exactly over any finite window, and no stationarity or queue discipline is required.\[2\] In L = λW, λ is the realised throughput, not the nameplate capacity.
- **Kingman's 1961 G/G/1 heavy-traffic result** gives Wq ≈ (ρ/(1−ρ))·((ca²+cs²)/2)·te.\[32\] Waiting time grows without bound as ρ → 1, so plan below full utilisation.\[4\]
- **Wright (1936) is confirmed** as the origin of the learning curve. Learning–forgetting models for interrupted work include Jaber & Bonney (1996) and Nembhard & Uzumeri (2000).\[33\]\[34\]\[35\]
- **Factory Physics** is still the 3rd edition (2008, Waveland reissue 2011). CONWIP originates with Spearman, Woodruff & Hopp (1990).\[36\]\[37\]\[38\]

## 2. Corrections

| Belief | Verdict | Correct fact | Source |
|---|---|---|---|
| OR-Tools (v9.x) CP-SAT … Python API added PEP 8 names "alongside" the old CamelCase ones | **Partly corrected** | The snake_case rename happened in 9.9; a user reported "the new version has renamed all the python methods from PascalCase to camel case" (issue against 9.9.3963, milestone v9.10).\[7\] I did not confirm whether the CamelCase names survive as aliases in 9.15. Treat CamelCase as legacy and do not mix the two styles. Current version: 9.15 (12 Jan 2026). "Leading" is supported indirectly: CP-SAT "has been consistently winning gold medals in the MiniZinc Challenge" (secondary).\[39\] | github.com/google/or-tools/issues/4143; github.com/google/or-tools/releases; en.wikipedia.org/wiki/OR-Tools |
| HiGHS is a leading open-source LP/MIP solver; SciPy's `linprog` and `milp` use it | **Confirmed** (secondary for SciPy) | SciPy "uses HiGHS as its LP solver from release 1.6.0 and the HiGHS MIP solver … from release 1.9.0".\[40\] HiGHS is also MATLAB's default solver from 2024a, per Mittelmann.\[13\] | en.wikipedia.org/wiki/HiGHS_optimization_solver; plato.asu.edu/ftp/milp.html |
| SCIP is now Apache 2.0 | **Confirmed, with a nuance** | SCIP 10.0, SoPlex 8.0, PaPILO 3.0 and GCG 4.0 are Apache 2.0, but "Zimpl 3.7.0 and UG 1.0 make use of the GNU Lesser General Public License".\[16\] SCIP's own download page states: "The Apache 2.0 License applies from Version 8.0.3 onwards." | arxiv.org/html/2511.18580v1; scipopt.org/download.php |
| Timefold Solver succeeds OptaPlanner as a 2023 fork by the original team | **Confirmed; out of date** | "Forked on 20 April 2023 from OptaPlanner".\[22\] Timefold Solver 1.0 was announced in July 2023.\[41\]\[42\] Current: 2.0.0 (22 Apr 2026).\[23\] 1.x reaches end of life in early 2027.\[25\] | github.com/timefoldai/timefold-solver; optaplanner.io blog |
| Pyomo and PuLP are the common Python layers, and PuLP ships CBC | **Corrected** | PuLP 4.x: "CBC is not included inside the PuLP wheel. The legacy PULP_CBC_CMD solver … has been removed."\[1\] Python ≥ 3.12 is required.\[1\]\[20\] PuLP 3.x (≤ 3.3.2, 25 May 2026) still bundled CBC.\[43\]\[44\]\[45\] I did not source a ranking of "most common". | coin-or.github.io/pulp/main/installing_pulp_at_home.html |
| ISO 10075 parts 1–3 cover mental workload; HSE HSG256 covers shift work, with the FRI as a tool | **Confirmed; editions corrected** | The current parts are 10075-1:2017, 10075-2:2024 (1996 edition withdrawn) and 10075-3:2004, with a revision of Part 3 under development.\[30\] HSG256 (2006) recommends "assessment tools such as HSE's Fatigue and Risk Index Tool".\[31\] HSG256 also says the evidence for forward rotation is limited (see Q3).\[31\] | iso.org/committee/53352/x/catalogue/; HSG256 PDF |
| Little's law holds "for any stable system"; Kingman shows wait → ∞ as utilisation → 100% | **Little corrected; Kingman confirmed** | Little (2011): "If limits λ and W exist and are finite, L exists and is finite, and L = λW". It is also "numerically exact" over a finite window [0, T], and no stationarity is needed.\[2\] Kingman (1961) is a heavy-traffic limit result, not an exact formula.\[46\] | Little 2011, Operations Research 59(3); Kingman 1961, DOI 10.1017/S0305004100036094 |
| Wright's curve (1936) is the standard model; learning–forgetting models extend it | **Confirmed** | Wright, "Factors Affecting the Cost of Airplanes", J. Aeronautical Sciences 3(4):122–128, Feb 1936. Learn–forget curve model: Jaber & Bonney (1996). Individual learning and forgetting: Nembhard & Uzumeri (2000).\[34\]\[35\]\[47\] | arc.aiaa.org/toc/jans/3/4; sciencedirect S0169814199000219 |
| Hopp & Spearman's Factory Physics is the standard reference | **Confirmed (edition)** | 3rd edition, McGraw-Hill 2008, reissued by Waveland 2011 (ISBN 9781577667391).\[37\]\[38\] I found no 4th edition. "Standard" is a judgement and I found no source that ranks it. | worldcat.org OCLC 718450337 |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| 1 | OR-Tools latest release | v9.15 | https://github.com/google/or-tools/releases | "v9.15 Latest … 2026-01-12"\[5\] | 12 Jan 2026 |
| 2 | ortools PyPI version | 9.15.6755 | https://libraries.io/pypi/ortools | "**9.15.6755**: Jan 14, 2026"\[6\] | 14 Jan 2026 |
| 3 | OR-Tools components and languages | CP-SAT, CP*, Glop, PDLP, routing; C++/Python/C#/Java | https://github.com/google/or-tools/tree/v9.11 | "We wrote OR-Tools in C++, but provide wrappers in Python, C# and Java."\[48\] | read 11 Nov 2026 |
| 4 | OR-Tools 9.15 bundled solvers | HiGHS v1.12.0, SCIP v10.0.0 | https://data.safetycli.com/packages/pypi/ortools/changelog (secondary) | "HiGHS=v1.12.0 * SCIP=v10.0.0"\[49\] | Jan 2026 |
| 5 | CP-SAT snake_case rename | in 9.9 | https://github.com/google/or-tools/issues/4143 | "It seems that the new version has renamed all the python methods from PascalCase to camel case." | 2024 (milestone v9.10)\[7\] |
| 6 | CP-SAT wrong OPTIMAL (open issue) | 9.15.6755 | https://github.com/google/or-tools/issues/5582 | "At 1 worker, 7 of the 207 reported OPTIMAL above a known feasible value"\[8\] | read 11 Nov 2026 |
| 7 | CP-SAT core bug | presolve on | https://github.com/google/or-tools/issues/5141 | "it returns a literal index that was never passed to CpModel.add_assumptions(...)"\[9\] | 2026 |
| 8 | Fix proposed | PR #5539 | https://github.com/google/or-tools/pull/5539 | "Each case checks that the core is a subset of the original assumptions" | 28 Oct 2026\[10\] |
| 9 | HiGHS latest | 1.15.1 | https://github.com/ERGO-Code/HiGHS/releases/tag/v1.15.1 | "galabovaa released this 02 Jul" | 2 Jul 2026\[15\] |
| 10 | HiGHS parallel MIP | first in 1.15 | https://github.com/ERGO-Code/HiGHS/releases | "This is the first release of the parallel MIP solver."\[12\]\[15\] | 28 Jun 2026 |
| 11 | HiGHS IIS fixes | 1.15.0 | https://newreleases.io/project/github/ERGO-Code/HiGHS/release/v1.15.0 | "several bugs in the computation of an Irreducible Infeasible Subsystem (IIS) via Highs::getIis were fixed"\[14\] | Jun 2026 |
| 12 | SCIP 10.0.0 release | 24 Nov 2025 | https://zenodo.org/records/17700258 | "Published November 24, 2025 \| Version v10.0.0"\[18\] | 24 Nov 2025 |
| 13 | SCIP suite licences | Apache 2.0 / LGPL | https://arxiv.org/html/2511.18580v1 | "SCIP 10.0, SoPlex 8.0, PaPILO 3.0, and GCG 4.0 are licensed under the Apache 2.0 license, whereas Zimpl 3.7.0 and UG 1.0 make use of the GNU Lesser General Public License."\[16\] | Nov 2025 |
| 14 | SCIP 10 IIS | built in | https://www.pokutta.com/blog/research/2025/12/02/scip-10.html (secondary) | "IIS detection for MIPs is now integrated directly into SCIP"\[17\] | 2 Dec 2025 |
| 15 | Gurobi 13.0 support | to Nov 2028 | https://www.gurobi.com/product/whats-new | "Gurobi version 13.0 (released in November 2025) and minor releases will be supported until November 2028."\[26\] | read 11 Nov 2026 |
| 16 | Gurobi latest 13.x | 13.0.3, 8/2026 | https://support.gurobi.com/hc/en-us/articles/360048138771 | "13.0.3 \| 8/2026 \| Actively Supported \| 11/2028"\[50\] | 26 Aug 2026 |
| 17 | Gurobi 14 beta | 14.0.0b1 | https://pypi.org/project/gurobipy/ | "14.0.0b1 Sep 28, 2026"\[27\] | 28 Sep 2026 |
| 18 | PuLP latest on PyPI | 4.2.0 | https://pypi.org/project/PuLP/ | "Released: Oct 22, 2026" | 22 Oct 2026\[19\] |
| 19 | PuLP no longer bundles CBC | 4.x | https://coin-or.github.io/pulp/main/installing_pulp_at_home.html | "CBC is not included inside the PuLP wheel. The legacy PULP_CBC_CMD solver … has been removed." | read 11 Nov 2026 |
| 20 | PuLP Python floor | ≥ 3.12 | same | "PuLP requires Python 3.12 or newer."\[1\]\[20\] | read 11 Nov 2026 |
| 21 | Pyomo latest | 6.10.1\[51\] | https://pypi.org/project/pyomo/4.1.10505/ | "6.10.1 Jun 4, 2026"\[52\] | 4 Jun 2026 |
| 22 | Pyomo 6.10 changes | drops Py 3.9 | https://github.com/Pyomo/pyomo/blob/main/RELEASE.md | "Removed support for Python 3.9"\[53\] | 2026 |
| 23 | Timefold 2.0.0 | 22 Apr 2026 | https://mvnrepository.com/artifact/ai.timefold.solver/timefold-solver-core | "2.0.0 … Apr 22, 2026" | 22 Apr 2026\[23\] |
| 24 | Timefold fork date | 20 Apr 2023 | https://github.com/timefoldai/timefold-solver | "Timefold Solver was forked on 20 April 2023 from OptaPlanner"\[22\] | read 11 Nov 2026 |
| 25 | Timefold 1.x end of life | early 2027 | https://github.com/timefoldai/timefold-solver/releases | "Only 2 more of these are planned before Timefold Solver 1.x EOL in early 2027."\[25\] | 3 Aug 2026 |
| 26 | MiniZinc bundle | 2.10.1 | https://www.minizinc.org/downloads/ | "These contain MiniZinc 2.10.1, the MiniZinc IDE 2.10.1"\[54\] | read 11 Nov 2026 |
| 27 | MiniZinc 2.10.0 | 23 Jul 2026 | same (search snippet) | "MiniZinc 2.10.0 (released 23 July 2026"\[54\] | 23 Jul 2026 |
| 28 | Mittelmann MILP results | COPT 219, HiGHSp 179, HiGHS 158, SCIP 136 of 240 | https://plato.asu.edu/ftp/milp.html | "solved   219    136    179    158" | 7 Jul 2026\[13\] |
| 29 | Mittelmann MILP infeasibility | CBC 20, HiGHS 25, SCIP 22 of 32 | https://plato.asu.edu/ftp/infeas.html | "solved:   20    30     25       22" | 26 Jul 2026\[55\] |
| 30 | HSG256 error risk | night, >8 h, successive shifts, breaks | HSG256 PDF (assets.publishing.service.gov.uk) | "The risk of errors, accidents and injuries has been found: to be higher on the night shift; to rise with increasing shift length over eight hours; to increase over successive shifts … to increase when there are not enough breaks." | 2006\[31\] |
| 31 | HSG256: no one best system | — | same | "there is no single optimal shift system that suits everyone" | 2006\[31\] |
| 32 | ISO 10075 current parts | 1:2017, 2:2024, 3:2004 | https://www.iso.org/committee/53352/x/catalogue/ | "ISO 10075-2:2024 Ergonomic principles related to mental workload — Part 2: Design principles"\[30\] | read 11 Nov 2026 |
| 33 | Little's law conditions | limits exist | https://pubsonline.informs.org/doi/10.1287/opre.1110.0940 | "If limits λ and W exist and are finite, L exists and is finite, and L = λW."\[2\] | Jun 2011 |
| 34 | CONWIP origin | 1990 | https://www.semanticscholar.org/paper/77420401959120f8c9849bedd894c9dd90010439 | "This paper describes a new pull-based production system called CONWIP."\[36\] | 1990 |
| 35 | CP-SAT default threads | all cores | https://d-krupke.github.io/cpsat-primer/parameters.html (secondary) | "By default, CP-SAT leverages all available cores (including hyperthreading)."\[56\] | read 11 Nov 2026 |

## 4. Findings

### Q1. Solvers today

| Solver | Current version (date) | Licence | Languages | Problem class | Next release / end of support |
|---|---|---|---|---|---|
| OR-Tools: CP-SAT, routing, MPSolver/MathOpt wrappers, Glop, PDLP | 9.15 (12 Jan 2026) | Apache-2.0 | C++, Python, C#, Java | CP-SAT: constraint programming, SAT and integer scheduling. Routing: VRP and TSP. Glop/PDLP: LP. Wrappers call MIP solvers (bundled HiGHS 1.12, SCIP 10) | Next release not announced (not found). No published end-of-support policy (not found). |
| HiGHS | 1.15.1 (2 Jul 2026) | MIT. Release binaries ship as "-mit" and "-apache" builds; the Apache build includes HiPO\[12\]\[15\] | C++, C, Python (highspy), C#, Julia and others | LP, MIP, convex QP | Not found |
| SCIP | 10.0.0 (24 Nov 2025). The SoPlex news page lists "Apr/2026 · Version 8.0.2 released as part of the SCIP Optimization Suite 10.0.2", then Suite 10.0.3 (Jul 2026) and Suite 10.1.0 (Sep 2026), so 10.1.0 appears to be current | Apache-2.0 | C, C++ (PySCIPOpt, SCIP.jl, JSCIPOpt, russcip interfaces) | MIP, MINLP, constraint integer programming | Not found |
| CBC | 2.10.13, marked "Latest" on github.com/coin-or/Cbc/releases and "Published March 11, 2026" on Zenodo (Zenodo notes a newer record exists; check it). Mittelmann still benchmarks 2.10.5 | EPL-2.0 (secondary) | C++ (via PuLP, Pyomo, MiniZinc) | MIP | Not found. Note it trails HiGHS and SCIP on Mittelmann's infeasibility test\[55\] |
| Gurobi | 13.0.3 (Aug 2026). 14.0.0b1 on PyPI 28 Sep 2026; 14.0.0 on Anaconda 10 Nov 2026 | Proprietary | C, C++, Python, Java, .NET and others | LP, MIP, QP, MINLP | 13.x supported to Nov 2028. **14.0 GA expected around Dec 2026** (webinar 1 and 3 Dec 2026). Each major release is supported for three years\[50\] |
| CPLEX | 22.1.2 (December 2024, per IBM's Alex Fleischer: "Latest release #CPLEX @IBM version : 22.1.2 December 2024"). PyPI also lists cplex 22.2.0.0 (26 May 2026) and 22.2.0.1 (15 Jul 2026), so 22.1.2 may no longer be current | Proprietary | C, C++, Java, .NET, Python | LP, MIP, QP; CP Optimizer for scheduling | IBM's lifecycle page gives 22.1.x "General Availability 04-Mar-2022" under the "Enhanced (E): minimum 5 years support with extension of 3 years" policy, i.e. at least to Mar 2027 (flag: within 12 months unless extended); exact end date not found |
| Pyomo | 6.10.1 (4 Jun 2026) | BSD-3-Clause (from 6.9.3, per Snyk)\[57\] | Python | Modelling layer (LP, MIP, NLP, GDP) | Python 3.9 dropped in 6.10\[53\] |
| PuLP | 4.2.0 (22 Oct 2026). Docs show a 4.3.0 (contested: not on the PyPI snippet I saw) | Not confirmed in this run | Python ≥ 3.12. New Rust core (`pulp._rustcore`)\[19\]\[20\] | LP and MIP modelling. Calls CBC, HiGHS, SCIP, Gurobi, CPLEX, CP-SAT and others | 3.x is the last line to bundle CBC |
| Timefold Solver | 2.0.0 (22 Apr 2026) | Apache-2.0 (Community Edition); Plus and Enterprise are commercial | Java, Kotlin | Metaheuristic planning: scheduling, rostering, routing\[23\]\[58\] | **1.x end of life early 2027** (flag) |
| MiniZinc | 2.10.1 bundle.\[54\] 2.10.0 released 23 Jul 2026; the handbook titles "latest" as 2.10.2 (contested) | Not confirmed in this run | MiniZinc language, Python (minizinc-python) | Solver-independent CP modelling via FlatZinc.\[54\] Ships Gecode, HiGHS and others | Not found |

**Which to choose** (my synthesis, from the sources above):
- **Discrete scheduling with intervals, no-overlap, cumulative and sequencing.** Use CP-SAT. It wins the MiniZinc Challenge (secondary).\[39\] It has native interval and no-overlap constraints; see Q2.\[59\]
- **Pure LP and MIP** (capacity planning, aggregate production, lot sizing). Use HiGHS as the open-source default.
  - On 7 Jul 2026, Mittelmann's MIPLIB2017 run had parallel HiGHS solve 179 of 240 instances (scaled time 5.44), against 136 for SCIP and 219 for COPT. Gurobi and CPLEX were not in that table.\[13\]
  - Use SCIP when you need MINLP, branch-and-price (GCG), or the new exact rational mode.
  - Use Gurobi when the licence budget allows and the gap matters. Gurobi reports 13.0 is "~16% faster solves on difficult MIP models (>100s)" than 12.0; that is a vendor benchmark (gurobi.com FAQ).\[60\]
- **Large rostering or routing with many soft constraints, in Java or Kotlin.** Timefold's local search is the natural fit. Weigh the 2.0 edition split (see Q9).
- **Modelling layers.** Pyomo suits multi-solver, nonlinear or structured models. PuLP suits simple MILPs, but PuLP 4's packaging changes break old installs.
- **Benchmark dates.** MILP benchmark 7 Jul 2026. Infeasibility benchmark 26 Jul 2026. Mittelmann's index lists a MIPfeas benchmark dated 16 Sep 2026. GAMS introduced MIPfeas in Mar 2026 (gams.com blog).\[13\]\[55\]\[61\]\[62\]

### Q2. Modelling scheduling problems

- **Official examples.**
  - OR-Tools publishes a job-shop example at `developers.google.com/optimization/scheduling/job_shop`. Issue #4143 cites it, noting its code uses the new names while its prose used the old ones.\[7\]
  - Timefold's repository description lists "vehicle routing problem, employee rostering, task assignment, maintenance scheduling". Its 1.4.0 notes mention a "Project Job Scheduling" example.\[63\]
  - I did not fetch official flow-shop, RCPSP, cell-assignment or nurse-rostering example pages this run. They are listed under Not covered.
- **Intervals and resources.** In CP-SAT, `add_no_overlap` takes interval variables: "A NoOverlap constraint ensures that all present intervals do not overlap in time" (or-tools.github.io pdoc).\[64\]
  - `add_no_overlap_2d` packs rectangles.\[59\]\[65\]
  - `add_cumulative` takes intervals plus demands, for shared capacity such as crew size or a shared fixture.\[64\]
  - Optional intervals (`new_optional_interval_var`) model "this task runs on this cell or that person", and model time windows through start-variable domains (CP-SAT Primer, secondary).\[59\]
- **Hard against soft constraints and weights.**
  - No primary source fetched. Heuristic, labelled as such: make legal and safety rules (HSG256 limits, qualifications) hard. Make preferences soft. Normalise each soft term by its plausible range before weighting.
  - When you have a strict priority order, prefer lexicographic solves: optimise the first objective, fix it as a bound, then optimise the next. That stops one term silently dominating.
- **Diagnosing infeasibility.**
  - CP-SAT: add assumption literals that switch constraints on, then read `sufficient_assumptions_for_infeasibility()` (CP-SAT Primer). Re-check any core by re-solving with presolve off (issue #5141).\[9\]\[56\]
  - LP/MIP: HiGHS has `Highs::getIis`, with bugs fixed in 1.15.\[14\] SCIP 10 integrates IIS detection for MIPs.\[17\] Gurobi's reference manual has an "Infeasibility Analysis" section.\[66\]
- **Time limits and the gap.**
  - A result that stopped at a limit must report: the status (FEASIBLE, not OPTIMAL), the incumbent objective, the best bound, the relative gap, wall time, worker count and seed.
  - PuLP 4 adds distinct status codes such as `TimeLimit` (secondary: ceREEBerus PR #134).\[44\]
  - Gurobi 13 changed the resumed-MIP log to show "the total, accumulated time and work spent". Do not parse that log line for per-call runtime (Gurobi 13 release notes).\[66\]

### Q3. People in the plan

- **Fatigue and shift design (HSG256, 2006).**
  - The schedule factors are sourced in fact 30.
  - HSG256 points users to "HSE's Fatigue and Risk Index Tool, to identify whether any particular aspect of an existing or proposed working time pattern is likely to increase the risk of fatigue".\[31\]
  - On rotation, the HSG256 table text reads "Forward versus backward rotation There is limited evidence that…".\[31\] The guidance favours forward rotation, but on limited evidence. Encode it as a soft preference with a source note, not as a law.
  - On time of day, HSG256 says "Concentration and productivity tend to decline towards the end of the shifts, following lunch and during the night and early hours of the morning".\[31\] Reason enough to keep safety-critical or high-skill tasks out of those windows.
  - HSG256 lists vulnerable groups (young, older and new or expectant workers, and others), and says Working Time Regulations compliance "may not in itself be enough to prevent fatigue".\[31\]
- **Mental workload.** ISO 10075-2:2024 gives design principles; 10075-3:2004 gives measurement requirements.\[30\]\[67\] The texts are paywalled; I read only the scopes.
- **Learning and forgetting.**
  - Wright (1936) is the base model. Jaber & Bonney's (1996) learn–forget curve model covers production breaks. Nembhard & Uzumeri (2000) show learning and forgetting vary between individuals.\[33\]\[34\]\[68\]
  - Anzanello & Fogliatto (2011) review suggests "allocating fast learners to short duration tasks, while slow learners should perform tasks of long duration" (as quoted by a citing paper).\[35\]
  - Model implication: task duration is a function of the worker, their cumulative repetitions and the time since they last did the task. It is not a constant.
- **Who-dependent setup, skills, fairness.** I did not source these this run (see Not covered). Heuristic: keep the qualification matrix as data, and give each worker–task pair a duration and setup matrix.
- **Planning below full utilisation.** Little and Kingman are sourced in Q4. Kingman is why a rostered or line plan at around 100% load has unbounded expected queues once variability is above zero.\[4\]
- **Optimised plans that failed on the shop floor.**
  - Wiers (2009, Production Planning & Control 20(7)) found that "a disagreement concerning autonomy is a key explanatory factor for understanding why an APS implementation may fail".\[69\]
  - Ivert (2012) reports operators saying "the operation times in the dispatch list did not correspond with real operation times", and summarises Wiers: schedules "are usually ignored by the shop floor, which most likely happens for a good reason".\[70\]
  - The fix those papers point to is to give the shop floor matching autonomy, and to use real operation times rather than standards.
  - I found no case explicitly titled "failed because workers were treated as deterministic".

### Q4. Quoting lead times from backlog and capacity

- **Little's law** holds whenever the long-run throughput and time in system exist; no distributional or queue-discipline assumption is needed. It is "numerically exact" over a finite window (Little 2011).\[2\]
- **What that means for the owner's board.** "Open orders ÷ daily capacity" is Little's W = L/λ with λ set to capacity. The real λ is realised throughput, which is lower whenever there is downtime, absence, scrap or a product mix that is slower than the capacity unit. So the board understates lead time, systematically.
- **Fix:** divide by trailing measured throughput, in the same units as the backlog. Then add a queueing and variability allowance (Kingman), because orders do not arrive and complete evenly.
- **Kingman:** Wq ≈ (ρ/(1−ρ))·((ca²+cs²)/2)·te. It is a heavy-traffic approximation and is "generally very accurate, especially for a system operating close to saturation" (Wikipedia, secondary).\[32\]
- **CONWIP** (Spearman, Woodruff & Hopp 1990) caps WIP so that lead time is controlled through Little's law.
- **Due-date quoting.** Keskinocak & Tayur (2004), "Due Date Management Policies", is the standard survey. It is a handbook chapter\[71\] and I got no quote from it. I did not fetch the costs of quoting short against quoting long; see Not covered.
- **Capacity by product (equivalent units), shared resources, and holiday calendars.** Not sourced this run.
  - Heuristic: convert each order to hours on the bottleneck resource using a per-product rate table held as data, not code.
  - Do date arithmetic on a working-day calendar that the owner maintains, with shutdowns as data.

### Q5. Checking a plan without trusting the solver

- **Why it matters.** Issue #5582 reports CP-SAT 9.15 marking non-optimal solutions OPTIMAL: 7 of 207 runs at 1 worker. On another model it reports INFEASIBLE although "a known solution … is OPTIMAL". The reporter's workaround is `presolve_inclusion_work_limit: 0`.\[8\] The issue is open and the maintainers have not confirmed it.
- **Independent checker.**
  - Write a checker in plain code that never imports the solver. It re-checks every hard constraint (precedence, no overlap per resource, capacity per period, qualifications, rest rules) and recomputes the objective from the assignment.
  - Fail if the recomputed objective differs from the solver's.
  - For infeasibility cores, replay the core with presolve off, as PR #5539's tests do: "sufficient for infeasibility when replayed without presolve".\[10\]
- **Test oracles.**
  - MIPLIB2017 has known optima and is the basis of Mittelmann's runs.\[13\]
  - SCIP 10 adds an exact mode that produces "verifiable certificates" (secondary blog),\[17\] which is useful as an oracle for small MILPs.
  - OR-Library, PSPLIB, Taillard and NRP sets: not fetched this run.
- **Determinism.** CP-SAT parallelism is a portfolio. With one worker only the default subsolver runs, and from two upward it adds LNS (Primer).\[56\] Results with more than one worker are not reproducible run to run unless the solver's deterministic mode is used (that mode is not sourced this run). For regression tests, pin `num_workers`, `random_seed` and the version, and assert on objective bounds rather than exact assignments.
- **Simulation and explanation.** Discrete-event simulation was not sourced this run.
  - Explanation: Timefold's score analysis "can now break down the score all the way to individual constraint matches" (1.4.0).\[63\] In 2.0 it is outside the open-source edition: Timefold's upgrade guide says ScoreAnalysis "is now provided exclusively by Timefold Solver Enterprise Edition", and its release blog says "Explainability moves to Timefold Solver Plus, a new paid edition".
  - Heuristic: build explanations from the independent checker's per-constraint report instead.

### Q6–Q8. Standard questions (partial)

- **Slow solvers.** Timefold's 2.0 adds "a new API to escape local optima" (the Neighborhoods API).\[24\]\[41\] CP-SAT runs LNS when it has two or more workers.\[56\] CP-SAT and Gurobi both accept solution hints and warm starts: Gurobi 13 "improves the NoRel heuristic by allowing it to use variable hints".\[60\] Use hints with care given #5582. I did not source dispatching rules (EDD, SPT, critical ratio).
- **Re-planning.** Timefold supports pinning: `@PlanningPinToIndex` "tell[s] the solver that a certain portion of the list variable is pinned" (newsletter 2).\[72\] Use it to freeze the near term. I did not source the nervousness literature.
- **Running in a service.**
  - Threads: CP-SAT uses all cores, including hyperthreads, by default (Primer). Perron: "The solver is designed to work with 8+ workers, unless for trivial models" (GitHub discussion #3630, 2023).\[56\]\[73\] Set `num_workers` explicitly to the container's CPU quota.
  - Time limits: always set `max_time_in_seconds` or a deterministic time limit.
  - MiniZinc 2.9.6 added `--cleanup-time-limit` as a grace period before forced termination.\[74\]
  - Gurobi 13 adds Kubernetes autoscaling of Compute Server.\[75\] Commercial licences in containers and CI were not sourced this run.

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| OR-Tools (Python) | CP-SAT, routing, LP | 9.15.6755 | 14 Jan 2026 | `pip install ortools==9.15.6755` | None; parameters set in code (`solver.parameters`) | libraries.io/pypi/ortools |
| highspy | HiGHS LP/MIP | 1.15.1 | 2 Jul 2026\[11\] | `pip install highspy` (command not verified on the page) | Optional HiGHS options file (per release notes) | pypi.org/project/highspy |
| SCIP | MIP/MINLP | 10.0.0; Suite 10.0.2 (Apr 2026), 10.0.3 (Jul 2026) and 10.1.0 (Sep 2026) per the SoPlex news page | 24 Nov 2025 | Not verified this run | `scip.set` (not verified) | zenodo.org/records/17700258; soplex.zib.de |
| gurobipy | Commercial MIP | 13.0.3 (14.0.0 arriving) | Aug 2026 | `pip install gurobipy` (not verified) | Licence file (name not verified) | support.gurobi.com |
| Pyomo | Modelling | 6.10.1\[51\] | 4 Jun 2026 | `pip install pyomo` (not verified) | None | pypi.org/project/pyomo |
| PuLP | Modelling | 4.2.0 | 22 Oct 2026 | `python -m pip install pulp[cbc]`\[19\]\[20\] | None | coin-or.github.io/pulp |
| Timefold Solver | Java/Kotlin planning | 2.0.0 | 22 Apr 2026 | Maven `ai.timefold.solver:timefold-solver-core:2.0.0`\[23\] | `solverConfig.xml` (not verified) | mvnrepository.com |
| Timefold migration | 1.x → 2.0 upgrade | 2.0.0 | 2026 | OpenRewrite recipe `timefold-solver-migration`\[58\] | None | libraries.io (Maven) |
| MiniZinc | CP modelling | 2.10.1\[54\] | 2026 (2.10.0 on 23 Jul 2026) | Download the bundle from minizinc.org\[54\] | `.mzn` / `.dzn` / `.mpc` | minizinc.org/downloads |
| HSE FRI | Fatigue and risk index | Spreadsheet (rr446cal.xls)\[76\] | 2006 | Download from HSE | — | HSG256 / National Highways PDF |

## 6. Changing in the next 12 months

- **Timefold Solver 1.x end of life in early 2027 (flag: within 12 months).** Two more quarterly 1.x releases are planned. 2.0 removes all deprecated methods\[24\]\[25\] and needs Java 21 (per Timefold's upgrade page title).\[24\]
- **Gurobi 14.0** is in beta on PyPI (28 Sep 2026) and 14.0.0 is on the Anaconda channel (10 Nov 2026); launch webinars are on 1 and 3 Dec 2026.\[27\]\[28\]\[29\] Gurobi 13.x remains supported to Nov 2028.\[50\] Gurobi's "Gurobi release and support history" page lists "12.0.0 | 11/2024 | Supported | 11/2027" and "11.0.3 | 07/2024 | Supported | 11/2026", so Gurobi 11.x reaches end of support this month and 12.x in Nov 2027 (flag: both within 12 months).
- **PuLP 4** is already shipping and breaks old code: no bundled CBC, `PULP_CBC_CMD` removed, Python ≥ 3.12.\[20\] Python 3.9–3.11 users stay on PuLP 3.x.\[1\]\[44\]
- **Pyomo 6.10** dropped Python 3.9, and solver interface "v2" is described as an "ongoing solver interface refactor",\[53\] so expect API movement.
- **OR-Tools:** no release since 9.15 (Jan 2026). Fixes for #5141 (PR #5539) and #5582 would land in a future release with no announced date.\[10\]
- **ISO 10075-3** is under revision (working draft, stage 20.60).\[30\] I found no publication date.
- **MiniZinc** removed support for SCIP 7 and earlier (2.9.6).\[74\]

## 7. Common mistakes

1. **Trusting OPTIMAL or INFEASIBLE.** See #5582.\[8\] Always run the independent checker.
2. **Using an infeasibility core without re-checking it.** See #5141.\[9\]
3. **Writing `PULP_CBC_CMD`, or assuming `pip install pulp` brings a solver.** Removed in 4.x (PuLP docs).\[1\]\[20\] AI assistants trained on older code are likely to emit this; that is an inference, as I found no study of it.
4. **Mixing CamelCase and snake_case CP-SAT calls.** The official docs themselves mixed them (#4143).\[7\] Assistants trained on pre-9.9 examples will emit `AddNoOverlap` and `NewIntervalVar`.
5. **Lead time = backlog ÷ capacity.** Use measured throughput (Little 2011) and add a variability allowance (Kingman 1961).
6. **Planning people at 100% utilisation with fixed task times.** Wiers (2009) and Ivert (2012) show plans get ignored when planned times do not match real ones.\[70\]
7. **Treating Working Time Regulations limits as sufficient.** HSG256 says compliance may not be enough.\[31\]
8. **Leaving CP-SAT at all cores in a shared container, or at one worker in production.** One worker disables LNS (Primer); the default grabs every core.\[56\]
9. **Relying on Timefold score explanations after upgrading to Community 2.0.** Timefold's upgrade guide says "ScoreExplanation has been removed" and ScoreAnalysis "is now provided exclusively by Timefold Solver Enterprise Edition"; its release blog says explainability moves to the paid Plus edition.
10. **Comparing Gurobi with open-source solvers using current Mittelmann tables.** Gurobi is absent from the 7 Jul 2026 MILP table.\[13\]
11. **AI-assistant-specific mistakes.** I found no published primary study. Items 3 and 4 are inferred from the version history above.

## 8. Sources and licences

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| OR-Tools repo, release notes, API docs, issues | Apache-2.0 (repo) | Yes | Yes | Yes, keeping the Apache NOTICE and licence | "Google OR-Tools, Apache-2.0" plus link |
| HiGHS repo and release notes | MIT | Yes | Yes | Yes, keeping the MIT notice | Copyright notice plus link |
| SCIP suite / arXiv 2511.18580 | Software Apache-2.0; paper licence not checked | Brief | Yes | Software code yes (Apache) | Cite authors and arXiv ID |
| Timefold repo and blog | Code Apache-2.0; blog licence not stated\[22\] | Brief (blog) | Yes | Code yes (Apache) | Link and "Timefold" |
| PuLP docs | Licence not confirmed this run | Brief | Yes | Not until the licence is confirmed | Link |
| Pyomo repo | BSD-3-Clause | Yes | Yes | Yes, with the BSD notice | Notice plus link |
| MiniZinc site and handbook | Not confirmed | Brief | Yes | No, until confirmed | Link |
| Gurobi docs, site and support | Proprietary © Gurobi | Brief (fair use) | Yes | No | "Gurobi Optimization" plus link |
| Mittelmann benchmarks (plato.asu.edu) | None stated | Brief | Yes | n/a | "H. Mittelmann, ASU" plus date |
| CP-SAT Primer (d-krupke) | Not confirmed this run | Brief | Yes | No, until confirmed | Author plus link (secondary) |
| HSE HSG256 | © Crown copyright 2006, "All rights reserved"\[31\] | Brief only | Yes | n/a | "HSE, HSG256 (2006)" |
| ISO 10075 parts | © ISO, paywalled | Titles and scope only | Yes | n/a | Standard number and year |
| Little 2011 (INFORMS), Kingman 1961 (CUP), Wright 1936 (AIAA), Spearman et al. 1990 (T&F), Wiers 2009 (T&F), Nembhard & Uzumeri 2000 (Elsevier) | Publisher copyright | Brief | Yes | n/a | Full citation plus DOI |
| Wikipedia pages | CC BY-SA 4.0 | Yes | Yes | Share-alike would apply, so avoid adapting | Title, link, CC BY-SA |
| GitHub issue threads by third parties | GitHub terms; author copyright | Brief | Yes | Repro snippets: no, unless licensed | Issue number plus link |

## 9. Not found, contested, not covered

- **Not found.**
  - Any next OR-Tools release date.
  - The exact end-of-support date for CPLEX 22.1.x (IBM's policy gives a minimum of five years from GA on 4 Mar 2022).
  - Licences for PuLP and MiniZinc.
  - Whether CP-SAT's CamelCase aliases survive in 9.15.
  - A study of AI-assistant errors in optimisation code.
  - A published failure case explicitly blamed on deterministic worker models.
- **Contested.**
  - PuLP's latest version: PyPI shows 4.2.0 (22 Oct 2026) while the docs header shows 4.3.0.\[19\]\[20\]
  - MiniZinc's latest version: the downloads page shows 2.10.1 while the handbook shows 2.10.2.\[54\]
  - Gurobi 14.0.0: present on Anaconda (10 Nov 2026), but I found no general-availability announcement.
  - Timefold 2.0 explainability: Timefold's own pages disagree on which paid edition now holds it — the upgrade guide says Enterprise, the release blog says Plus.
- **Not covered (room).**
  - Official flow-shop, RCPSP, cell-assignment and rostering example links for each solver.
  - Lexicographic and multi-objective APIs (CP-SAT, Gurobi multi-objective).
  - Business rules as data.
  - OR-Library, PSPLIB, Taillard and NRP instance sets.
  - Property-based testing of models.
  - Discrete-event simulation tools.
  - Who-dependent setup times.
  - Cross-training and fairness (the nurse-rostering literature).
  - The costs of quoting due dates short against long.
  - Equivalent-unit capacity.
  - Calendar arithmetic.
  - Dispatching rules.
  - Nervousness and re-planning literature.
  - Commercial solver licences in containers and CI.

## Sources

1. [Installing PuLP at Home — PuLP 4.0.0 documentation](https://coin-or.github.io/pulp/main/installing_pulp_at_home.html)
2. <https://people.cs.umass.edu/~emery/classes/cmpsci691st/readings/OS/Littles-Law-50-Years-Later.pdf>
3. [Timefold Solver 2.0: Faster Solving, and the "Why" Now Costs Money](https://bytecode.news/posts/2026/04/timefold-solver-2-0-faster-solving-and-the-why-now-costs-money)
4. [The Single Server Queue in Heavy Traffic. - The Encyclopedia of Abstractions](https://abstractopedia.org/references/ref-ea99465f95a1/)
5. [Releases · google/or-tools · GitHub](https://github.com/google/or-tools/releases)
6. [ortools 9.15.6755 on PyPI - Libraries.io - security & maintenance data for open source software](https://libraries.io/pypi/ortools)
7. [Renaming of python methods leads to confusion · Issue #4143 · google/or-tools · GitHub](https://github.com/google/or-tools/issues/4143)
8. [CP-SAT 9.15.6755: OPTIMAL reported above the true optimum depending on the solution hint (avoided by presolve\_inclusion\_work\_limit: 0) · Issue #5582 · google/or-tools · GitHub](https://github.com/google/or-tools/issues/5582)
9. [CP-SAT: \`sufficient\_assumptions\_for\_infeasibility()\` returns a literal that is not in the assumption list (presolve only) · Issue #5141 · google/or-tools · GitHub](https://github.com/google/or-tools/issues/5141)
10. [#5141 :: Preserve assumption identity during CP-SAT presolve by ricardoleal20 · Pull Request #5539 · google/or-tools · GitHub](https://github.com/google/or-tools/pull/5539)
11. [highspy · PyPI](https://pypi.org/project/highspy/)
12. [Releases · ERGO-Code/HiGHS · GitHub](https://github.com/ERGO-Code/HiGHS/releases)
13. [https - Hans Mittelmann](https://plato.asu.edu/ftp/milp.html)
14. [ERGO-Code/HiGHS v1.15.0 on GitHub](https://newreleases.io/project/github/ERGO-Code/HiGHS/release/v1.15.0)
15. [Release v1.15.1 · ERGO-Code/HiGHS · GitHub](https://github.com/ERGO-Code/HiGHS/releases/tag/v1.15.1)
16. [The SCIP Optimization Suite 10.0](https://arxiv.org/html/2511.18580v1)
17. [SCIP Optimization Suite 10.0: Exact Solving, Better Decompositions, and a More Productive Ecosystem](https://www.pokutta.com/blog/research/2025/12/02/scip-10.html)
18. [scipopt/scip: v10.0.0](https://zenodo.org/records/17700258)
19. [PuLP · PyPI](https://pypi.org/project/PuLP/)
20. [pulp — PuLP 4.3.0 documentation](https://www.coin-or.org/pulp/main/includeme.html)
21. [Optimization with PuLP — PuLP 4.3.0 documentation](https://coin-or.github.io/pulp/)
22. [GitHub - TimefoldAI/timefold-solver: The open source Solver AI for Java and Kotlin to optimize scheduling and routing. Solve the vehicle routing problem, employee rostering, task assignment, maintenance scheduling and other planning problems. · GitHub](https://github.com/timefoldai/timefold-solver)
23. [Maven Repository: ai.timefold.solver » timefold-solver-core](https://mvnrepository.com/artifact/ai.timefold.solver/timefold-solver-core)
24. [Timefold Solver 2.0: Neighborhoods API and faster solving](https://timefold.ai/blog/timefold-solver-2-0-release)
25. [Releases · TimefoldAI/timefold-solver · GitHub](https://github.com/timefoldai/timefold-solver/releases)
26. [What's New - Gurobi 13.0](https://www.gurobi.com/product/whats-new)
27. [gurobipy · PyPI](https://pypi.org/project/gurobipy/)
28. [gurobi - Gurobi](https://anaconda.org/Gurobi/gurobi)
29. [What's New in 14.0 Webinar](https://www.gurobi.com/resources/webinar-events/what-is-new-in-14.0-webinar)
30. [ISO/TC 159/SC 1 - General ergonomics principles](https://www.iso.org/committee/53352/x/catalogue/)
31. [Page 1 of 45 Health and Safety Executive Managing shiftwork](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/390908/hsg256_managing_shift_work.pdf)
32. [Kingman's formula](https://en.wikipedia.org/wiki/Kingman's_formula)
33. [LEARNING CURVE ANALYSIS](https://link.springer.com/rwe/10.1007/1-4020-0612-8_504)
34. [Economic order quantity model for items with imperfect quality with learning in inspection - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0925527309003727)
35. [Experiential learning and forgetting for manual and cognitive tasks - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0169814199000219)
36. [CONWIP: a pull alternative to kanban](https://www.semanticscholar.org/paper/CONWIP:-a-pull-alternative-to-kanban-Spearman-Woodruff/77420401959120f8c9849bedd894c9dd90010439)
37. [Factory physics](https://search.worldcat.org/title/factory-physics/oclc/718450337)
38. [Factory Physics by Hopp, Wallace J./ Spearman, Mark L](https://www.biblio.com/book/factory-physics-hopp-wallace-j-spearman/d/1303087167)
39. [OR-Tools](https://en.wikipedia.org/wiki/OR-Tools)
40. [HiGHS optimization solver](https://en.wikipedia.org/wiki/HiGHS_optimization_solver)
41. [OptaPlanner - Timefold Solver 2 has been released](https://optaplanner.io/blog/2026/04/22/TimefoldSolver-2-released)
42. [OptaPlanner - Timefold Solver 1 has been released](https://optaplanner.io/blog/2023/07/03/TimefoldSolver-1-released)
43. [piwheels - PuLP](https://www.piwheels.org/project/pulp/)
44. [Support PuLP 4.0 while keeping PuLP 3.x fallback (#131) by ishikaghosh2201 · Pull Request #134 · MunchLab/ceREEBerus · GitHub](https://github.com/MunchLab/ceREEBerus/pull/134)
45. [PuLP 4.2.0 on PyPI - Libraries.io - security & maintenance data for open source software](https://libraries.io/pypi/PuLP)
46. [Heavy-traffic single-server queues andthe transform method](https://arxiv.org/html/2206.09844)
47. [Journal of the Aeronautical Sciences](https://arc.aiaa.org/toc/jans/3/4)
48. [GitHub - google/or-tools at v9.11 · GitHub](https://github.com/google/or-tools/tree/v9.11)
49. [ortools Changelog](https://data.safetycli.com/packages/pypi/ortools/changelog)
50. [Gurobi release and support history](https://support.gurobi.com/hc/en-us/articles/360048138771-Gurobi-release-and-support-history)
51. [python:pyomo package versions - Repology](https://repology.org/project/python:pyomo/versions)
52. [pyomo · PyPI](https://pypi.org/project/pyomo/4.1.10505/)
53. [pyomo/RELEASE.md at main · Pyomo/pyomo · GitHub](https://github.com/Pyomo/pyomo/blob/main/RELEASE.md)
54. [MiniZinc - Downloads](https://www.minizinc.org/downloads/)
55. [Asu](https://plato.asu.edu/ftp/infeas.html)
56. [Parameters - The CP-SAT Primer - Using and Understanding Google OR-Tools' CP-SAT Solver](https://d-krupke.github.io/cpsat-primer/parameters.html)
57. [pyomo vulnerabilities](https://security.snyk.io/package/pip/pyomo)
58. [ai.timefold.solver:timefold-solver-migration 2.0.0 on Maven - Libraries.io - security & maintenance data for open source software](https://libraries.io/maven/ai.timefold.solver:timefold-solver-migration)
59. [Advanced Modeling - The CP-SAT Primer - Using and Understanding Google OR-Tools' CP-SAT Solver](https://d-krupke.github.io/cpsat-primer/advanced_modelling.html)
60. [Gurobi 13.0](https://www.gurobi.com/resources/faq/gurobi-13-0)
61. [Expanding the Focus: Introducing the MIPfeas Benchmark](https://www.gams.com/blog/2026/03/expanding-the-focus-introducing-the-mipfeas-benchmark/)
62. [Decison Tree for Optimization Software](https://plato.la.asu.edu/bench.html)
63. [Release Timefold Solver Community Edition 1.4.0 · TimefoldAI/timefold-solver · GitHub](https://github.com/TimefoldAI/timefold-solver/releases/tag/v1.4.0)
64. [ortools.sat.python.cp\_model API documentation](https://or-tools.github.io/docs/pdoc/ortools/sat/python/cp_model.html)
65. [Google OR-Tools: build/python/ortools/sat/python/cp\_model.py Source File](https://or-tools.github.io/docs/python/cp__model_8py_source.html)
66. [Additions, Changes and Removals in Gurobi 13.0 - Gurobi Optimizer Reference Manual](https://docs.gurobi.com/projects/optimizer/en/current/reference/releasenotes/changes.html)
67. [ISO 10075-3:2004 - Ergonomic Principles for Mental Workload Assessment Methods](https://standards.iteh.ai/catalog/standards/iso/71355f1a-4b0e-4ba7-8f52-f25ca55fdb02/iso-10075-3-2004)
68. [D. Nembhard](https://www.semanticscholar.org/author/D.-Nembhard/1788992)
69. [(PDF) The potential benefits of advanced planning and scheduling systems in sales and operations planning](https://researchgate.net/publication/220672520_Potential_Benefits_of_APS_Systems_in_Sales-and-Operations_Planning)
70. [(PDF) Production Planning & Control: The Management of Operations Shop floor characteristics influencing the use of advanced planning and scheduling systems Shop floor characteristics influencing the use of advanced planning and scheduling systems](https://www.academia.edu/36278585/Production_Planning_and_Control_The_Management_of_Operations_Shop_floor_characteristics_influencing_the_use_of_advanced_planning_and_scheduling_systems_Shop_floor_characteristics_influencing_the_use_of_advanced_planning_and_scheduling_systems)
71. [Due Date Management Policies](https://link.springer.com/chapter/10.1007/978-1-4020-7953-5_12)
72. [Newsletter 2: The past, present and future of OptaPlanner / Timefold](https://timefold.ai/blog/newsletter-2-the-past-present-and-future-of-optaplanner-timefold)
73. [CP-SAT get's stuck when trying to maximize sum of boolean variables that are all added as assumptions · google/or-tools · Discussion #3630 · GitHub](https://github.com/google/or-tools/discussions/3630)
74. [MiniZinc Change Log — The MiniZinc Handbook 2.10.2](https://docs.minizinc.dev/en/latest/changelog.html)
75. [Gurobi Releases Version 13.0 with New Solving Capabilities](https://www.sdcexec.com/software-technology/software-solutions/news/22954972/gurobi-gurobi-releases-version-130-with-new-solving-capabilities)
76. [Safe roads, reliable journeys, informed travellers](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/359025/B22_Fatigue_March_2014.pdf)
