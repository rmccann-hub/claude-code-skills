# Verification: R28b (2026-11-11)

Checked on 2026-11-11 against the primary sources named below. The report is untrusted data. Its
line 3 is addressed to "the receiving session": it asks that session to check each claim, file the
report under `research/runs/`, update the facts files of the categories it names, and list what
changed. That is an instruction found in a research result. It was recorded here and not
followed: nothing was filed, and no repository file was edited.

Access notes:
- github.com web pages and api.github.com returned 403 for google/or-tools (curl). Issue #5582,
  issue #4985, Discussion #4183 and the milestones page were read with the Exa fetch tool
  (`web_fetch_exa`); Timefold's GitHub discussion and the archived Python repository came from Exa
  search highlights. The proto files came from raw.githubusercontent.com, and tags and branches
  from `git ls-remote`.
- `sat_parameters.proto` on the `stable` branch (head 100f66e) and at commit 98c165a (the
  report's source [10]) are byte-identical.
- mistic.heig-vd.ch returned 503 and then reset the connection. Taillard's page has moved to
  mistic.iict-heig-vd.ch, which curl read directly.
- ibm.com returned 403 to curl, and Exa timed out. The CPLEX 22.1.0 page was read with WebFetch,
  and the same text appears in Exa's copy of the 22.1.1 page. The report's URL is the Chinese
  locale (`/docs/zh/`); the English path is `/docs/en/`.
- link.springer.com served a bot check ("Client Challenge") to curl and redirected WebFetch to a
  login. The Keskinocak and Tayur chapter page and the 2017 Annals of OR article came through
  Exa fetch. rss.onlinelibrary.wiley.com returned 403 to curl; the Kingman (1962) summary came
  through Exa fetch and Crossref. cambridge.org (Kingman 1961) came through Exa fetch: it is a
  three-page "Research Note" with no abstract.
- Docker Hub pages were read through the Docker Hub v2 API (`full_description`), and Anaconda
  through `api.anaconda.org/package/gurobi/gurobi`.
- Registries read directly: PyPI JSON (gurobipy, ortools, simpy, timefold), Maven Central
  (`maven-metadata.xml` and file `Last-Modified` headers), Crossref, and the arXiv API.
- arXiv 1909.02737, 2502.18330 (v2, the current version) and 2502.18330v1 were each downloaded
  into their own new empty directory and read only with `pdftotext`.
- Gurobi support articles, the Gurobi docs, the What's New page, the webinar page, the newsroom,
  schedulingbenchmarks.org, the CP-SAT Primer, the SimPy changelog, the TU/e and Chalmers
  portals, the Google Groups thread and developers.google.com were read with curl.

| Claim | Status | Checked against |
|---|---|---|
| C1: CP-SAT's deterministic multi-worker mode is `interleave_search`, marked "Experimental" | verified | [sat_parameters.proto (stable)](https://raw.githubusercontent.com/google/or-tools/stable/ortools/sat/sat_parameters.proto), lines 767-774 |
| C1: a developer's recipe turns off binary-clause sharing and is "usually way slower" | verified. The writer is Laurent Perron, on 24 Oct 2023: "Ok interleave_search:true,share_binary_clause:false, num_workers:16" | [Seeding CP-SAT solver](https://groups.google.com/g/or-tools-discuss/c/lPb1FzhTMt0) |
| C1: a single worker is the simpler deterministic option | verified with a correction. The proto says only "A number of 1 means no parallelism."; it doesn't call one worker deterministic. Issue #5582's wrong OPTIMAL happened at `num_workers: 1, random_seed: 0, max_deterministic_time: 60`, so determinism doesn't mean correctness | sat_parameters.proto; [Issue #5582](https://github.com/google/or-tools/issues/5582) |
| C2: CP-SAT has no lexicographic API; the guidance is fix-and-resolve | verified (the Primer's quote; no lexicographic method in the proto or in R28's check of `cp_model.py`) | [CP-SAT Primer: Basic Modeling](https://d-krupke.github.io/cpsat-primer/modelling.html) |
| C2 and fact 10: Discussion #4183 gives the "project answer": fix objective i, hint, repeat | verified with a correction. The quoted steps are the question's (speedfreeman, 14 Apr 2024), not the project's. The answer, by lperron on 15 Apr 2024, covers blocking constraints instead: "you can. It is just harder for the solver at each iterations as the model is bigger (less fixed variables)." | [Discussion #4183](https://github.com/google/or-tools/discussions/4183) |
| C2: Gurobi and CPLEX support hierarchical objectives natively | verified | [Gurobi Multiple Objectives](https://docs.gurobi.com/projects/optimizer/en/current/features/multiobjective.html); [CPLEX 22.1.0 Solving multiple objective problems](https://www.ibm.com/docs/en/SSSA5P_22.1.0/ilog.odms.cplex.help/CPLEX/UsrMan/topics/multiobj/multiobj_solving.html) |
| C3: Taillard publishes best-known lower and upper bounds | verified with a correction. The page has moved to mistic.iict-heig-vd.ch. The job-shop summary's latest update line is "Update 17.06.2013", so it lags the literature too (ta33 was closed in 2025, see below) | [Scheduling instances](https://mistic.iict-heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html); [job-shop bounds](https://mistic.iict-heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/jobshop.dir/best_lb_up.txt) |
| C3: PSPLIB holds "optimal and heuristic solutions" (secondary) | verified at the secondary source | [PyJobShop/PSPLIB README](https://raw.githubusercontent.com/PyJobShop/PSPLIB/main/README.md) |
| C3 and fact 26: 215 PSPLIB instances open (2019) | verified (arXiv v1, 6 Sep 2019; journal ref Computers & Operations Research 2019) | [arXiv 1909.02737](https://arxiv.org/abs/1909.02737) |
| C3 and fact 27: "Two of these new solutions are not updated in PSPLIB." | verified with a correction. The sentence is only in v1 (25 Feb 2025). The current v2 (12 Sep 2025) drops it and points to PSPLIB instead: "The best heuristic solutions have been updated for some instances from PSPLIB." Don't cite it as evidence that PSPLIB lags | [arXiv 2502.18330v1](https://arxiv.org/abs/2502.18330v1); [v2](https://arxiv.org/abs/2502.18330v2) |
| C3: OR-Library not verified (report) | not checked (the report marks it not found) | none |
| C4: SimPy describes itself as "a process-based discrete-event simulation framework based on standard Python" | verified | [simpy on PyPI](https://pypi.org/project/simpy/) (JSON description) |
| C5: Kingman (1961), Proc. Camb. Phil. Soc. 57(4):902-904 | verified (Crossref: Mathematical Proceedings of the Cambridge Philosophical Society, Oct 1961, pp. 902-904; Cambridge Core lists it as "Research Notes") | [doi:10.1017/S0305004100036094](https://doi.org/10.1017/S0305004100036094) |
| C5: the 1961 paper doesn't show the ρ/(1−ρ) mean-wait formula | unverifiable. The note is paywalled, with no abstract and only a preview image; neither its presence nor its absence could be checked | Cambridge Core |
| C5: Kingman (1962) heavy-traffic statement | verified with a correction. Wiley's page and Crossref both render the summary with "p", not "ρ": "the distribution of (1 – p) w tends, as p tends to 1, to a negative exponential distribution" (en dash). JRSS B 24(2):383-392, July 1962 | [On Queues in Heavy Traffic](https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1962.tb00465.x); Crossref |
| C6 and fact 34: Wiers (2009) "disagreement concerning autonomy" quote; PPC 20(7):576-585 | verified | [TU/e portal](https://research.tue.nl/en/publications/the-relationship-between-shop-floor-autonomy-and-aps-implementati); Crossref [doi:10.1080/09537280903034289](https://doi.org/10.1080/09537280903034289) |
| C6 and fact 35: Ivert (2012) "guideline, not a regulation" and "shop type" quotes; PPC 23(6):452-467 | verified (abstract; Crossref issued date 31 May 2011, online first) | [Chalmers portal](https://research.chalmers.se/publication/159554); Crossref [doi:10.1080/09537287.2011.564218](https://doi.org/10.1080/09537287.2011.564218) |
| Fact 1: OR-Tools current stable v9.15 | verified ("Announcing the release of OR-Tools v9.15 We have released OR-Tools v9.15.", under "January 2026"); `git ls-remote` shows no tag after v9.15 | [OR-Tools Release Notes](https://developers.google.com/optimization/support/release_notes) |
| Fact 2: v9.15 released 12 Jan 2026 (secondary) | verified at the primary source by the R28 verification (GitHub release 12 Jan 2026); PyPI upload 2026-01-14T15:38Z | PyPI JSON; R28-verification.md |
| Fact 3: 9.15.6755 is the newest ortools on PyPI | verified | [ortools JSON](https://pypi.org/pypi/ortools/json) |
| Fact 4: next OR-Tools is a v9.16 milestone; #4985's fix targets it | contradicted. #4985 is closed (updated 26 Feb 2026). The open milestones are "v10.0" ("Due by October 14, 2026", overdue, 17/117 closed) and "v10.0.0 RC1" ("Due by September 30, 2026", 557/558 closed), plus Backlog; there is no open v9.16. The next release is v10.0, with no tag yet | [Milestones](https://github.com/google/or-tools/milestones); [Issue #4985](https://github.com/google/or-tools/issues/4985) (Exa fetch) |
| Fact 5 and Q3: #5582 wrong OPTIMAL on 9.15.6755, avoided by `presolve_inclusion_work_limit: 0`; "It also happens without a hint." | verified. Open, created 2026-11-10T23:03Z, no reply as fetched. The issue says the switches are "empirical results on this sample" | [Issue #5582](https://github.com/google/or-tools/issues/5582) |
| Facts 6 and 7: `interleave_search` deterministic and "Experimental" | verified | sat_parameters.proto (stable and 98c165a) |
| Fact 8: "usually way slower" | verified (Laurent Perron, 24 Oct 2023) | Google Groups thread |
| Fact 9: Primer lexicographic quote | verified (a line break falls after "lexicographic optimization,") | CP-SAT Primer |
| Fact 11: Gurobi "A hierarchical or lexicographic approach assigns a priority..." | verified | Gurobi Multiple Objectives (manual 14.0) |
| Fact 12: ObjN attribute defaults | verified. The list also includes "ObjNCon with default value 0" and "ObjNName" | Gurobi Multiple Objectives |
| Fact 13: Gurobi 13.0 added `NumObjPasses` and `ObjPassN*`, and `InheritParams` | verified with a correction. The report's URL (`/en/current/.../changes.html`) now shows "Additions, Changes, and Removals in Gurobi 14.0". Cite the 13.0 page, `/en/13.0/reference/releasenotes/changes.html` | [Gurobi 13.0 release notes](https://docs.gurobi.com/projects/optimizer/en/13.0/reference/releasenotes/changes.html) |
| Q2: what 14.0 changed for multi-objective (report: not found) | verified (added). 14.0 changes the automatic `InheritParams` setting "from 0 (don't inherit) to 1 (do inherit)" for concurrent and multi-objective environments, and the tuner can use the MIP gap as `TuneCriterion` on multi-objective models | [Gurobi 14.0 release notes](https://docs.gurobi.com/projects/optimizer/en/current/reference/releasenotes/changes.html) ("Last updated on Nov 11, 2026") |
| Fact 14: Gurobi 13.0 released 18 Nov 2025 | verified (newsroom; gurobipy 13.0.0 reached PyPI 2025-11-11) | [Gurobi newsroom](https://www.gurobi.com/company/newsroom/gurobi-releases-version-13-0-with-improved-performance-and-new-solving-capabilities) |
| Facts 15 and 16: 13.0 supported to Nov 2028; three-year term | verified. The URL redirects to https://www.gurobi.com/product/whats-new, which still shows 13.0 | [What's New](https://www.gurobi.com/product/whats-new) |
| Fact 17 and Summary: Gurobi 14.0.0 on Anaconda, "Last Updated Nov 10, 2026" | verified (API `latest_version` 14.0.0, summary "Version 14.0.0 of the Gurobi Optimizer, Gurobi Optimization, LLC.", files uploaded 2026-11-10 13:21-13:24 UTC). Also gurobipy 14.0.0 final on PyPI 2026-11-10T13:04Z and a `gurobi/optimizer:14.0.0` Docker tag | [anaconda.org/Gurobi/gurobi](https://anaconda.org/Gurobi/gurobi); [gurobipy JSON](https://pypi.org/pypi/gurobipy/json) |
| Summary: manual "for version 14.0 of the Gurobi Optimizer" | verified | [Gurobi Optimizer Reference Manual](https://docs.gurobi.com/projects/optimizer/en/current/) |
| Fact 18: 14.0 webinars 1 and 3 Dec 2026 | verified ("December 1 & 3, 2026") | [What's New in 14.0 Webinar](https://www.gurobi.com/resources/webinar-events/what-is-new-in-14.0-webinar) |
| Fact 19: 13.0.3, 8/2026, Actively Supported, 11/2028 | verified. The page was updated 2026-08-26T21:14Z and has no 14.0 row yet, so it still calls 13.0.3 "Actively Supported". gurobipy 13.0.3 reached PyPI 2026-08-25 | [Gurobi release and support history](https://support.gurobi.com/hc/en-us/articles/360048138771-Gurobi-release-and-support-history) |
| Section 6: Gurobi 12.0.0 "11/2024 \| Supported \| 11/2027" | verified (all 12.0.x rows end 11/2027) | same |
| Section 6: Gurobi 11.0.0 "11/2023 \| Supported \| 11/2026" | verified (all 11.0.x rows end 11/2026) | same |
| Section 6: "Starting with major release 10, ... three years after the initial release of the corresponding major release." | verified | same |
| Facts 20 and 21: WLS needs Internet only; licence file not recommended in the image | verified (gurobi/optimizer description) | [gurobi/optimizer](https://hub.docker.com/r/gurobi/optimizer) (Docker Hub API) |
| Q9: WLS "for containerized environments (Docker, Kubernetes, ...)"; `GRB_WLSACCESSID`, `GRB_WLSSECRET`, `GRB_LICENSEID` | verified | [gurobi/python-example](https://hub.docker.com/r/gurobi/python-example) |
| Q9: Token Server, or mounting `gurobi.lic` | verified ("docker run --volume=$PWD/gurobi.lic:/opt/gurobi/gurobi.lic:ro") | gurobi/optimizer |
| Q9: Error 10024: cgroups v2; fixed in 9.5.1 in containers, 10.0.0 natively; `--privileged --cgroupns=host` | verified | [Error 10024 article](https://support.gurobi.com/hc/en-us/articles/13235765567505-How-do-I-resolve-an-Error-10024-Web-license-service-only-available-for-container-environments) |
| Fact 22: Academic WLS: v10 or later, internet, 90 days | verified (separate list items) | [What is an Academic WLS license?](https://support.gurobi.com/hc/en-us/articles/13210193318033-What-is-an-Academic-WLS-license) |
| Mistake 6: "The standard academic licenses for Gurobi do not work in docker containers." | verified (a community-forum reply, not a documentation page) | [Installing Gurobi on a Docker container](https://support.gurobi.com/hc/en-us/community/posts/4406485885841-Installing-Gurobi-on-a-Docker-container-Ubuntu) |
| Q1: `gurobi/modeling-examples` image, `docker run -p 8888:8888 gurobi/modeling-examples` | verified | [gurobi/modeling-examples](https://hub.docker.com/r/gurobi/modeling-examples) |
| Facts 23 and 24: Taillard bounds summary; EJOR 64(2):278-285, 1993 | verified with a correction (new host, see C3) | Taillard's page |
| Q3: ta33 closed, ta26 and ta45 improved, ta45 solved optimally, with OR-Tools | verified (arXiv 2504.16106, 17 Apr 2025) | [arXiv 2504.16106](https://arxiv.org/abs/2504.16106) |
| Fact 28: BCV-3.46.1 best 3275 on 16-Oct-2026, lower bound 3275 | verified. The lower bound row is dated 15-Oct-2026 at 2239 before it; the 3275 bound is listed first | [Nurse Rostering bounds](https://www.schedulingbenchmarks.org/nrp/bounds.html) |
| Fact 29: Curtois and Qu set: 2 to 52 weeks, 8 to 150 employees | unverifiable. Springer served a bot check; Exa returned the abstract and introduction without the sentence. The cited article is Demirović, Musliu and Winter (2017), open access, not Curtois and Qu | [Annals of OR 10.1007/s10479-017-2693-y](https://link.springer.com/article/10.1007/s10479-017-2693-y) |
| Facts 30 and 31: SimPy 4.1.2, 24 May 2026; MIT; Python >=3.8 | verified (upload 2026-05-24T04:37Z; the changelog dates it "4.1.2 - 2026-05-23"; classifiers run to Python 3.14) | [simpy JSON](https://pypi.org/pypi/simpy/json); [SimPy changelog](https://simpy.readthedocs.io/en/latest/about/history.html) |
| Q6: 4.1.0 "[BREAKING] Python 3.8 is the minimum supported version", "[NEW] Add Process.name property" | verified | SimPy changelog |
| Q6: "Though it is theoretically possible to do continuous simulations with SimPy, it has no features that help you with that." | verified | simpy PyPI description |
| Fact 32: ADS record of Kingman (1961) | verified. ADS also lists "Atiyah, M. F." as an author, which Crossref and Cambridge Core don't; cite Kingman alone | [ADS](https://ui.adsabs.harvard.edu/abs/1961PCPS...57..902K) |
| Fact 33 and Q5: Keskinocak and Tayur (2004), pp. 485-554, ISOR vol. 74; abstract "short and reliable lead times" | verified | [Springer chapter](https://link.springer.com/chapter/10.1007/978-1-4020-7953-5_12) (Exa); Crossref |
| Fact 36: Timefold quickstarts list Project Job Scheduling and Employee Scheduling | verified with a correction. The official repository reads "Shadow Variables, Variable Listener, Strength Comparator"; "Strenght" is the fork's typo. Cite TimefoldAI/timefold-quickstarts | [timefold-quickstarts README](https://raw.githubusercontent.com/TimefoldAI/timefold-quickstarts/stable/README.md) |
| Fact 37 and Q1: Timefold Solver for Python is Apache-licensed; "Just pip install timefold" | verified as written, but outdated. Timefold halted the Python solver on 11 Jul 2025 ("As of today, Timefold is halting active development on the Beta version of our Python Solver."), and archived its repository on 6 Oct 2025. The newest `timefold` on PyPI is 1.24.0b0 (8 Jul 2025). Don't recommend `pip install timefold` | [Timefold blog](https://timefold.ai/blog/new-open-source-solver-python); [Discussion #1698](https://github.com/TimefoldAI/timefold-solver/discussions/1698) (Exa); [timefold JSON](https://pypi.org/pypi/timefold/json) |
| Tools table: Timefold Solver 2.7.1 (6 Oct 2026) is current | contradicted. Current is 2.8.0, 3 Nov 2026 (Maven `<release>2.8.0</release>`, file 07:49 UTC). 2.7.1's date is right | [maven-metadata.xml](https://repo1.maven.org/maven2/ai/timefold/solver/timefold-solver-core/maven-metadata.xml) |
| Tools table: Timefold 1.35.0, 16 Oct 2026 | verified with a correction: Maven Central's file is dated 15 Oct 2026, 12:16 UTC | Maven Central |
| Section 6: "Timefold Solver Community Edition 1.x will be maintained throughout 2026 with quarterly bug-fix releases and security updates." | verified with a correction. The blog's words are "Timefold Solver 1.x is maintained throughout 2026 with quarterly bug-fix and security releases", and the v1.34.0 notes put 1.x end of life "in early 2027", not the end of 2026 | [Timefold Solver 2.0 blog](https://timefold.ai/blog/timefold-solver-2-0-release); R28-verification.md |
| Q1: Google: scheduling problems "well-suited for the CP-SAT solver: Employee Scheduling" | verified. The list continues "The Job shop problem", so an official job-shop example exists too | [Constraint Optimization](https://developers.google.com/optimization/cp) |
| Q2: CPLEX "sorts the objectives by decreasing priority value. If several objectives have the same priority, they are blended..." | verified | CPLEX 22.1.0 page (WebFetch) |
| Q3 and mistake 2: `max_deterministic_time`, "Maximum time allowed in deterministic time to solve a problem." | verified. `max_num_deterministic_batches` "only make sense when interleave_search is true" | sat_parameters.proto |
| Q3: `random_seed` resets the solver's random generator | verified (default 1) | sat_parameters.proto |
| Section 8: CP-SAT Primer licence "not found" | verified with a correction: the Primer "is licensed under the CC BY 4.0 license" | CP-SAT Primer |
| Secondary items: AIMMS on Gurobi, xiang.es recipes, UPenn lecture, DAM due-date paper, Wikipedia, ResearchGate, cpsat-utils, PandaStack | secondary only (the report marks them so; not re-checked) | none |

Counts, one per row by its main status: 47 verified, 12 verified with a correction (the Timefold
Python row, "verified as written, but outdated", counted here), 2 contradicted, 2 unverifiable,
1 secondary only, 1 not checked (65 rows).

### What R28b corrects in R28

- **CP-SAT determinism.** R28 said the deterministic mode was "not sourced this run". R28b
  sources `interleave_search` and its "Experimental" label, which the R28 verification had
  already added. R28b also adds the developer's warning that it is slower.
- **Lexicographic solves.** R28 advised lexicographic solves without saying how. R28b shows that
  CP-SAT has no API for it (it's a loop), while Gurobi and CPLEX do it natively. That holds,
  except that the Discussion #4183 steps are the question's, not the maintainer's.
- **Gurobi 14.** R28 expected general availability "around Dec 2026". R28b says 14.0.0 has
  shipped, which matches the R28 verification's contradiction (gurobipy 14.0.0 on 10 Nov 2026).
  The 11.x and 12.x end-of-support dates are the same in both, and both are verified.
- **Kingman.** R28 credited the ρ/(1−ρ) formula to Kingman (1961) as quotable text. R28b moves
  the quotable heavy-traffic statement to Kingman (1962) and treats the formula as an
  attribution. The R28 verification had already marked the formula secondary only.
- **Wiers and Ivert.** R28 had Ivert saying that schedules "are usually ignored by the shop
  floor", which the R28 verification couldn't verify. R28b replaces it with abstract quotes that
  are verified and drops "ignore".
- **Keskinocak and Tayur.** R28 had no quote. R28b adds the abstract, which is verified.
- **Benchmarks.** R28 didn't fetch OR-Library, PSPLIB, Taillard or the nurse-rostering sets.
  R28b covers all but OR-Library. One correction: its PSPLIB-lag quote is only in arXiv v1.
- **Not corrected.** R28 had Timefold 2.0.0 as current, and R28b has 2.7.1; both are wrong, and
  the current release is 2.8.0. R28b's "pip install timefold" is new and outdated.

## Exact quotes for facts rows

Each quote is as it appears at the source. Where the source breaks a line, the quote joins it
with a space.

| Fact | URL | Exact quote |
|---|---|---|
| CP-SAT deterministic parallel search | https://github.com/google/or-tools/blob/stable/ortools/sat/sat_parameters.proto | "The search is deterministic (independently of num_workers!), and we" (sentence continues on the next comment line) |
| `interleave_search` is experimental | same | "Experimental. If this is true, then we interleave all our major search" (continues "strategy and distribute the work amongst num_workers.") |
| One worker | same | "A number of 1 means no parallelism." |
| Deterministic time limit | same | "Maximum time allowed in deterministic time to solve a problem." |
| Deterministic search is slower | https://groups.google.com/g/or-tools-discuss/c/lPb1FzhTMt0 | "It is usually way slower than the non deterministic version." (Laurent Perron, 24 Oct 2023) |
| CP-SAT lexicographic loop | https://d-krupke.github.io/cpsat-primer/modelling.html | "To implement a lexicographic optimization, you can do multiple rounds and always fix the previous objective as constraint." |
| Blocking instead of fixing (maintainer) | https://github.com/google/or-tools/discussions/4183 | "you can. It is just harder for the solver at each iterations as the model is bigger (less fixed variables)." |
| #5582 workaround is empirical | https://github.com/google/or-tools/issues/5582 | "These are empirical results on this sample, not a soundness argument for any of the switches." |
| #5582 without a hint | same | "It also happens without a hint." (bold on the page) |
| Gurobi hierarchical objectives | https://docs.gurobi.com/projects/optimizer/en/current/features/multiobjective.html | "A hierarchical or lexicographic approach assigns a priority to each objective, and optimizes for the objectives in decreasing priority order." |
| Gurobi blend and hierarchy | same | "Gurobi allows you to enter and manage your objectives, to provide weights for a blended approach, and to set priorities for a hierarchical approach." |
| Gurobi 13.0 per-pass attributes | https://docs.gurobi.com/projects/optimizer/en/13.0/reference/releasenotes/changes.html | "The attribute NumObjPasses gives the number of optimization passes that were conducted in the last solve." |
| Gurobi 14.0 inheritance change | https://docs.gurobi.com/projects/optimizer/en/current/reference/releasenotes/changes.html | "the automatic setting of the InheritParams parameter changed from 0 (don’t inherit) to 1 (do inherit)." (curly apostrophe U+2019 in "don’t") |
| CPLEX hierarchical objectives | https://www.ibm.com/docs/en/SSSA5P_22.1.0/ilog.odms.cplex.help/CPLEX/UsrMan/topics/multiobj/multiobj_solving.html | "The CPLEX multiobjective optimization algorithm sorts the objectives by decreasing priority value." |
| Gurobi manual version | https://docs.gurobi.com/projects/optimizer/en/current/ | "This is the manual for version 14.0 of the Gurobi Optimizer." |
| Gurobi 14.0.0 on Anaconda | https://api.anaconda.org/package/gurobi/gurobi | "Version 14.0.0 of the Gurobi Optimizer, Gurobi Optimization, LLC." |
| Gurobi support term | https://support.gurobi.com/hc/en-us/articles/360048138771-Gurobi-release-and-support-history | "Starting with major release 10, all Gurobi product releases are supported for a term of three years after the initial release of the corresponding major release." |
| Gurobi 12.0 end of support | same | "12.0.0 \| 11/2024 \| Supported \| 11/2027" (table row; cells joined with " \| ") |
| Gurobi 11.0 end of support | same | "11.0.0 \| 11/2023 \| Supported \| 11/2026" (table row) |
| Gurobi 13.0 end of support | https://www.gurobi.com/product/whats-new | "Gurobi version 13.0 (released in November 2025) and minor releases will be supported until November 2028." |
| Gurobi 12 end of support (vendor page) | same | "Gurobi version 12.0.0 (released in November 2024) and minor releases through 12.0.3 will be supported until November 2027." |
| Gurobi 14.0 webinar | https://www.gurobi.com/resources/webinar-events/what-is-new-in-14.0-webinar | "December 1 & 3, 2026" |
| WLS in containers | https://hub.docker.com/r/gurobi/optimizer | "WLS only requires that your container has access to the Internet." (a line break before "Internet.") |
| No licence file in images | same | "We do not recommend adding the license file to the Docker image itself." |
| Academic WLS | https://support.gurobi.com/hc/en-us/articles/13210193318033-What-is-an-Academic-WLS-license | "Requires Gurobi v10 or later" and "Is valid for 90 days" (separate list items) |
| Error 10024 cause | https://support.gurobi.com/hc/en-us/articles/13235765567505 | "This issue is present in all Gurobi versions up to 9.5.0, and has been fixed in 9.5.1." |
| Taillard bounds | https://mistic.iict-heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html | "Summary of best known lower and upper bounds of Taillard's instances" |
| Taillard paper | same | "Published in E. Taillard, \"Benchmarks for basic scheduling problems\", EJOR 64(2):278-285, 1993." (straight double quotes on the page) |
| PSPLIB open instances (2019) | https://arxiv.org/abs/1909.02737 | "we found that 215 of the PSPLIB instances, 2842 of the MMLIB instances, and 27 of the MISTA instances, were still open" |
| ta33 closed with OR-Tools | https://arxiv.org/abs/2504.16106 | "We find new numerical lower bounds for multiple benchmark instances, up to closing the Taillard's ta33 instance." |
| Nurse rostering bound | https://www.schedulingbenchmarks.org/nrp/bounds.html | "3275" with date "16-Oct-2026" under BCV-3.46.1 Best Solutions (separate cells) |
| SimPy scope | https://pypi.org/project/simpy/ | "SimPy is a process-based discrete-event simulation framework based on standard Python." |
| SimPy not continuous | same | "Though it is theoretically possible to do continuous simulations with SimPy, it has no features that help you with that." |
| SimPy 4.1 floor | https://simpy.readthedocs.io/en/latest/about/history.html | "[BREAKING] Python 3.8 is the minimum supported version" |
| Kingman 1962 | https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1962.tb00465.x | "the distribution of (1 – p) w tends, as p tends to 1, to a negative exponential distribution" (en dash U+2013; "p" stands for ρ as rendered) |
| Due-date quoting | https://link.springer.com/chapter/10.1007/978-1-4020-7953-5_12 | "an essential value feature for customer acquisition and retention is the ability to quote short and reliable lead times." |
| Wiers 2009 | https://research.tue.nl/en/publications/the-relationship-between-shop-floor-autonomy-and-aps-implementati | "a disagreement concerning autonomy is a key explanatory factor for understanding why an APS implementation may fail." |
| Ivert 2012 | https://research.chalmers.se/publication/159554 | "For example, is the dispatch list used as a guideline, not a regulation, the need for accurate data in the module is reduced." |
| Ivert 2012, shop type | same | "the shop type is influenced by the decision of how often the APS runs and what freedom is given to the shop floor." |
| Timefold Python halted | https://github.com/TimefoldAI/timefold-solver/discussions/1698 | "As of today, Timefold is halting active development on the Beta version of our Python Solver." |
| Timefold 1.x maintenance | https://timefold.ai/blog/timefold-solver-2-0-release | "Timefold Solver 1.x is maintained throughout 2026 with quarterly bug-fix and security releases" |

## Versions found from registries

| Tool | Current version | Released | Read from |
|---|---|---|---|
| OR-Tools (ortools) | 9.15.6755 (tag v9.15; no later tag; next milestone v10.0, overdue) | PyPI 2026-01-14T15:38Z; GitHub release 12 Jan 2026 | PyPI JSON; `git ls-remote --tags`; milestones page |
| Gurobi (gurobipy) | 14.0.0 (requires Python >=3.11; licence "Proprietary") | 2026-11-10T13:04Z; 14.0.0b1 2026-09-28; 13.0.3 2026-08-25 | PyPI JSON |
| Gurobi (conda) | 14.0.0 | 2026-11-10, 13:21-13:24 UTC | api.anaconda.org |
| Gurobi Docker image | tag 14.0.0 present beside 13.0.3, 12.0.x, 11.0.3 | not checked (tags all re-pushed 11 Nov 2026) | Docker Hub v2 API |
| SimPy | 4.1.2 (MIT; Python >=3.8) | PyPI 2026-05-24T04:37Z (changelog 2026-05-23) | PyPI JSON; changelog |
| Timefold Solver (Java) | 2.8.0 | 3 Nov 2026, 07:49 UTC; 2.7.1 on 6 Oct 2026 | Maven Central metadata and file dates |
| Timefold Solver 1.x | 1.35.0 | 15 Oct 2026, 12:16 UTC | Maven Central |
| timefold (Python, PyPI) | 1.24.0b0 (development halted; repository archived 6 Oct 2025) | 2025-07-08T11:18Z | PyPI JSON |

## Licences

| Source | Licence as the source states it | What an Apache-2.0 repository may do |
|---|---|---|
| OR-Tools code, `sat_parameters.proto` | Apache License 2.0 (file header "Licensed under the Apache License, Version 2.0") | Quote, paraphrase; adapt code keeping the notice and marking changes |
| OR-Tools issues, discussions, Google Groups posts | GitHub and Google terms; authors' copyright | Brief quotes with a link; paraphrase |
| CP-SAT Primer | "licensed under the CC BY 4.0 license" | Quote, paraphrase and adapt with attribution and a licence link |
| Gurobi docs, support articles, Docker Hub descriptions | Proprietary (Anaconda `LicenseRef-Gurobi-Proprietary`; PyPI "Proprietary") | Brief quotes with attribution; paraphrase; no code |
| IBM CPLEX manual | IBM copyright | Brief quotes; paraphrase |
| SimPy | MIT (PyPI classifier and `license`) | Quote, paraphrase; adapt code keeping the MIT notice |
| Timefold Solver and quickstarts | Apache-2.0 (Community; R28 verification); the archived Python solver is "under the Apache License" | Quote, paraphrase; adapt with notice |
| Taillard's page, schedulingbenchmarks.org, PSPLIB | No licence stated | Brief quotes of figures with citation; don't redistribute the data |
| arXiv 1909.02737, 2502.18330, 2504.16106 | Per-paper arXiv licence; not checked | Brief quotes with citation; paraphrase |
| Kingman 1961 (CUP), Kingman 1962 (Wiley/RSS), Keskinocak and Tayur 2004 (Springer), Wiers 2009 and Ivert 2012 (Taylor & Francis) | Publisher copyright | Brief quotes with full citation and DOI; paraphrase |
| Demirović, Musliu and Winter 2017 (Annals of OR) | Open access (licence not read; bot check) | Brief quotes with citation until the licence is read |

## Repository facts this contradicts

`git -C /home/user/claude-code-skills grep -n -i` for Gurobi, OR-Tools, ortools, CP-SAT, Timefold,
SimPy, Kingman, Wiers, Ivert, num_workers, lexicographic and interleave in
`skills/optimization-and-scheduling` finds these `os-` Facts rows. None is now wrong:

- `os-ortools` (v9.15 is the newest release) holds: no tag after v9.15, and v10.0 is unreleased.
- `os-cpsat-params` holds: the quote matches the proto on `stable`.
- `os-cpsat-wrong-status` holds: #5582 is still open, with the quoted sentences.
- `os-timefold` (2.8.0) holds; R28b's 2.7.1 is the stale value, not the row.
- `os-timefold-editions` ("1.x EOL in early 2027") holds; R28b's "end of 2026" doesn't
  contradict it.
- `os-gurobi` (gurobipy 14.0.0; three-year term) holds. The support page still has no 14.0 row,
  and 11.x support ends this month (11/2026). The row doesn't name 11.x, so nothing is wrong.

The module has no Facts row for SimPy, Kingman, Wiers, Ivert, `interleave_search` or
lexicographic solves. Two prose lines rest on claims this run touched, though neither is a
Facts row:
- Line 129 of `references/optimization-and-scheduling.md` says "Kingman (1961): queueing delay
  grows without bound as utilization nears 1, faster the more variable the work". The variability
  part is the VUT formula, which is attributed to the 1961 note only by secondary sources. Its
  text couldn't be read.
- Rule 5's "In tests, pin version, seed and workers" holds. #5582 shows that a pinned single
  worker can still return a wrong OPTIMAL, which rule 1's checker already covers.

---

# R28b: Optimization and scheduling, the questions R28 didn't reach

Three of the five "What we believe" items need correcting before the skill relies on them: CP-SAT's multi-worker deterministic mode exists but is documented as "Experimental" and slower; CP-SAT has no native lexicographic API (only Gurobi and CPLEX do); and the waiting-time result usually credited to Kingman (1961) is not what the sourced primary text says.

**TL;DR**

- **Versions moved:** Gurobi 14.0.0 shipped this week (Anaconda package dated 10 Nov 2026), so any "Gurobi 13 is current" fact from R28 is out of date; OR-Tools is still on v9.15 (9.15.6755 on PyPI), with a v9.16 milestone open but no announced date.
- **Corrections:** CP-SAT's `interleave_search` gives deterministic multi-worker search but is marked "Experimental"; CP-SAT lexicographic solves are a user-written loop, not an API; benchmark libraries give a mix of proven optima and best-known bounds, and some are stale against the literature.
- **Testing:** a planner's tests should pin a single worker or `interleave_search`, use a deterministic time limit, and check against published optima — because a live OR-Tools issue (#5582) reports CP-SAT 9.15.6755 returning a wrong `OPTIMAL`.

## 1. Summary

- **R28's own files were not read in this run.** The research tool refused to fetch `github.com/rmccann-hub/claude-code-skills` on a tool-permission rule ("This URL is not permitted"), not because the repository is missing; search results confirm the repository is public and active (pull requests #45, #108, #113, #114, #124 and #128, the last dated 11 Nov 2026).\[1\]\[2\] The receiving session must diff this report against R28's result and facts file itself.
- **Gurobi 14.0 is out.** Anaconda lists "Version 14.0.0 of the Gurobi Optimizer" with "Last Updated Nov 10, 2026", and the current reference manual says "This is the manual for version 14.0 of the Gurobi Optimizer." The official launch webinars are 1 and 3 December 2026.\[3\]\[4\]\[5\]
- **Gurobi support runs three years per major release.** Gurobi states: "Gurobi version 13.0 (released in November 2025) and minor releases will be supported until November 2028."\[6\] Gurobi's own "Gurobi release and support history" table lists 12.0.0 as "11/2024 | Supported | 11/2027", so Gurobi 12.0 support ends in November 2027, inside the 12-month window (Gurobi's newsroom confirmed the 12.0 release on 19 Nov 2024).
- **OR-Tools stable is v9.15** (9.15.6755 on PyPI); Google's release-notes page lists v9.15 as the latest, and GitHub shows a "v9.16" milestone with no published date.\[7\]\[8\]\[9\]
- **A correctness bug is open on the current CP-SAT.** Issue #5582 reports "CP-SAT 9.15.6755: OPTIMAL reported above the true optimum depending on the solution hint (avoided by presolve_inclusion_work_limit: 0)".\[7\] Treat any reported `OPTIMAL` in tests as a claim to check against an oracle, not a proof.
- **CP-SAT determinism:** `num_workers = 1` is deterministic; with several workers, `interleave_search = true` is documented as "Experimental" and "deterministic (independently of num_workers!)", and an OR-Tools developer adds that it "is usually way slower than the non deterministic version."\[10\]\[11\]\[12\]
- **CP-SAT has no lexicographic objective API.** The documented pattern is a loop: solve, fix the objective's value as a constraint, hint the previous solution, re-solve.\[13\]\[14\]\[15\]
- **Gurobi has both modes natively:** blended via `ObjNWeight` and hierarchical via `ObjNPriority`, with `ObjNRelTol`/`ObjNAbsTol` to relax earlier objectives. Gurobi 13.0 added per-pass result attributes (`NumObjPasses`, `ObjPassN*`).\[16\]\[17\]
- **Benchmark oracles differ in strength.** Taillard publishes a "Summary of best known lower and upper bounds"; PSPLIB publishes "optimal and heuristic solutions";\[18\]\[19\] the nurse-rostering site lists best solutions and lower bounds with dates (one instance, BCV-3.46.1, was closed on 16 Oct 2026). Some libraries lag the literature.\[20\]
- **SimPy is at 4.1.2** (released 24 May 2026, MIT licence); the 4.1 line requires Python ≥ 3.8.
- **Gurobi in containers and CI uses the Web License Service (WLS),** which needs internet access from the container; Gurobi says "We do not recommend adding the license file to the Docker image itself."\[21\]
- **Wiers (2009) and Ivert (2012) are correctly citable** in *Production Planning & Control* (details in section 10), but neither abstract says the shop floor "ignores" APS schedules; their actual findings are about disputed autonomy and dispatch lists used "as a guideline, not a regulation".\[22\]\[23\]
- **Keskinocak and Tayur (2004)** is a Springer handbook chapter (pp. 485–554);\[24\] its abstract stresses "short and reliable lead times".\[24\] A sentence from the chapter itself stating the short-versus-long trade-off was not found.

## 2. Corrections

| # | What we believed | Verdict | Correct fact | Source |
|---|---|---|---|---|
| C1 | "CP-SAT has a deterministic mode for multi-worker runs, set through a solver parameter." | Partly right, needs qualifying | The parameter is `interleave_search` (with `interleave_batch_size`). The proto comment marks it "Experimental". A developer's recipe also turns off binary-clause sharing, and says it is "usually way slower". A single worker is the simpler deterministic option. | sat_parameters.proto (stable branch); or-tools-discuss thread "Seeding CP-SAT solver"\[10\]\[11\] |
| C2 | "CP-SAT and Gurobi both support lexicographic (hierarchical) multi-objective solves." | Wrong for CP-SAT | Gurobi (and CPLEX) support hierarchical objectives natively. CP-SAT does not; the guidance is to "do multiple rounds and always fix the previous objective as constraint". | Gurobi "Multiple Objectives"; CP-SAT Primer (secondary); OR-Tools Discussion #4183\[14\]\[17\]\[25\] |
| C3 | "OR-Library, PSPLIB, Taillard's instances and the nurse-rostering benchmark sets publish instances with known optima or best-known solutions." | Mostly right, with caveats | Taillard: best-known lower and upper bounds. PSPLIB: optimal and heuristic solutions, but the literature reports open instances and some improvements not uploaded. Nurse rostering: best solutions and lower bounds with dates. OR-Library: not verified in this run. | Taillard's site; PSPLIB parser README (secondary); arXiv 1909.02737; arXiv 2502.18330; schedulingbenchmarks.org\[18\]\[19\]\[20\]\[26\] |
| C4 | "SimPy is the common Python discrete-event simulation library." | Unverified | SimPy describes itself as "a process-based discrete-event simulation framework based on standard Python". No primary source ranks it as "the common" library; say "a widely used" one, or "not found". | PyPI simpy page\[27\] |
| C5 | "Kingman's 1961 approximation for the G/G/1 queue gives waiting time growing as ρ/(1−ρ)." | Mis-attributed in detail | The 1961 paper (Proc. Camb. Phil. Soc. 57(4):902–904) is a heavy-traffic limit result.\[28\]\[29\] The widely quoted heavy-traffic statement ("the distribution of (1 – ρ)w tends, as ρ tends to 1, to a negative exponential distribution") is from Kingman's 1962 JRSS B paper. The "VUT" mean-wait formula with its ρ/(1−ρ) term is attributed to Kingman by secondary sources; its exact wording in the 1961 paper was not found.\[30\]\[31\] Cite it as "Kingman's formula (after Kingman 1961)", not as a quote. | ADS record of the 1961 paper; Wiley page for Kingman (1962); Wikipedia "G/G/1 queue" (secondary)\[32\]\[33\]\[34\] |
| C6 | (R28 prompt wording) "Wiers (2009) and Ivert (2012) on shop floors ignoring APS schedules" | Misleading framing | Wiers: "disagreement concerning autonomy is a key explanatory factor for understanding why an APS implementation may fail." Ivert: the dispatch list may be "used as a guideline, not a regulation". Neither says "ignoring". | TU/e portal (Wiers); Chalmers portal (Ivert)\[22\]\[23\] |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| 1 | OR-Tools current stable | v9.15 | https://developers.google.com/optimization/support/release_notes | "Announcing the release of OR-Tools v9.15 … We have released OR-Tools v9.15." | read 11 Nov 2026\[9\] |
| 2 | OR-Tools v9.15 release date | 12 Jan 2026 (secondary) | https://en.wikipedia.org/wiki/OR-Tools | "Stable release: v9.15 / January 12, 2026" | read 11 Nov 2026\[35\] |
| 3 | Newest OR-Tools on PyPI | 9.15.6755 | https://github.com/google/or-tools/issues/5582 | "9.15.6755 is the newest release on PyPI" | read 11 Nov 2026\[7\] |
| 4 | Next OR-Tools | v9.16 milestone, no date | https://github.com/google/or-tools/issues/4985 | "Milestone v9.16" | read 11 Nov 2026\[8\] |
| 5 | CP-SAT wrong OPTIMAL bug | open report on 9.15.6755 | https://github.com/google/or-tools/issues/5582 | "the symptom is a silent wrong OPTIMAL." | read 11 Nov 2026\[7\] |
| 6 | CP-SAT deterministic multi-worker | `interleave_search` | https://github.com/google/or-tools/blob/stable/ortools/sat/sat_parameters.proto | "The search is deterministic (independently of num_workers!)" | read 11 Nov 2026\[36\] |
| 7 | Same field's status | Experimental | https://github.com/google/or-tools/blob/98c165af62df62b3056c2ee0fca66b24e79097cb/ortools/sat/sat_parameters.proto | "Experimental. If this is true, then we interleave all our major search strategy and distribute the work amongst num_workers." | read 11 Nov 2026\[10\] |
| 8 | Cost of determinism | slower | https://groups.google.com/g/or-tools-discuss/c/lPb1FzhTMt0 | "Will start a deterministic search with 16 workers. It is usually way slower than the non deterministic version." | read 11 Nov 2026\[11\] |
| 9 | CP-SAT lexicographic pattern | loop and fix | https://d-krupke.github.io/cpsat-primer/modelling.html | "To implement a lexicographic optimization, you can do multiple rounds and always fix the previous objective as constraint." | read 11 Nov 2026\[14\] |
| 10 | CP-SAT lexicographic, project answer | blocking also allowed | https://github.com/google/or-tools/discussions/4183 | "Add a constraint that objective i == v Add s as a solution hint Repeat for objective i+1" | 14 Apr 2024\[13\] |
| 11 | Gurobi hierarchical objectives | `ObjNPriority` | https://docs.gurobi.com/projects/optimizer/en/current/features/multiobjective.html | "A hierarchical or lexicographic approach assigns a priority to each objective, and optimizes for the objectives in decreasing priority order." | read 11 Nov 2026\[17\] |
| 12 | Gurobi objective attribute defaults | priority 0, weight 1 | same | "ObjNPriority with default value 0, ObjNWeight with default value 1, ObjNRelTol with default value 0, ObjNAbsTol with default value 1e-6" | read 11 Nov 2026\[17\] |
| 13 | Gurobi 13.0 multi-objective additions | per-pass attributes | https://docs.gurobi.com/projects/optimizer/en/current/reference/releasenotes/changes.html | "The attribute NumObjPasses gives the number of optimization passes that were conducted in the last solve." | read 11 Nov 2026\[16\] |
| 14 | Gurobi 13.0 release | 18 Nov 2025 | https://www.gurobi.com/company/newsroom/gurobi-releases-version-13-0-with-improved-performance-and-new-solving-capabilities | "November 18, 2025 — Gurobi Optimization, LLC … is pleased to announce the release of Gurobi 13.0." | 18 Nov 2025\[37\] |
| 15 | Gurobi 13.0 end of support | Nov 2028 | https://www.gurobi.com/whats-new-gurobi-13-0/ | "Gurobi version 13.0 (released in November 2025) and minor releases will be supported until November 2028." | read 11 Nov 2026\[6\] |
| 16 | Gurobi support policy | 3 years | same | "Major product releases—and their subsequent minor and technical product releases—are supported for a term of three years from the initial major product release date." | read 11 Nov 2026\[6\] |
| 17 | Gurobi 14.0.0 | on Anaconda | https://anaconda.org/Gurobi/gurobi | "Version 14.0.0 of the Gurobi Optimizer … Last Updated Nov 10, 2026" | 10 Nov 2026\[4\] |
| 18 | Gurobi 14.0 launch events | 1 and 3 Dec 2026 | https://www.gurobi.com/resources/webinar-events/what-is-new-in-14.0-webinar | "December 1 & 3, 2026" | read 11 Nov 2026\[5\] |
| 19 | Last Gurobi 13 patch seen | 13.0.3, August 2026 | https://support.gurobi.com/hc/en-us/articles/360048138771 | "13.0.3 | 8/2026 | Actively Supported | 11/2028" | Aug 2026 (AMPL repackaged it on 8 Sep 2026) |
| 20 | Gurobi in containers | WLS | https://hub.docker.com/r/gurobi/optimizer | "WLS only requires that your container has access to the Internet." | read 11 Nov 2026\[21\] |
| 21 | Gurobi licence file in images | not recommended | same | "We do not recommend adding the license file to the Docker image itself." | read 11 Nov 2026\[21\] |
| 22 | Academic WLS | 90 days, v10+ | https://support.gurobi.com/hc/en-us/articles/13210193318033-What-is-an-Academic-WLS-license | "Requires Gurobi v10 or later … Requires an internet connection during usage … Is valid for 90 days" | read 11 Nov 2026\[38\] |
| 23 | Taillard bounds | best known LB/UB | http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html | "Summary of best known lower and upper bounds of Taillard's instances" | read 11 Nov 2026\[18\] |
| 24 | Taillard paper | EJOR 64(2):278–285, 1993 | same | "Published in E. Taillard, \"Benchmarks for basic scheduling problems\", EJOR 64(2):278-285, 1993." | read 11 Nov 2026\[18\] |
| 25 | PSPLIB content (secondary) | optima and heuristic | https://github.com/PyJobShop/PSPLIB | "PSPLIB contains different problem sets for various types of resource constrained project scheduling problems as well as optimal and heuristic solutions." | read 11 Nov 2026\[19\] |
| 26 | PSPLIB open instances | 215 open (2019) | https://arxiv.org/pdf/1909.02737 | "we found that 215 of the PSPLIB instances, 2842 of the MMLIB instances, and 27 of the MISTA instances, were still open" | 2019\[26\] |
| 27 | PSPLIB lag | improvements not uploaded | https://arxiv.org/pdf/2502.18330 | "Two of these new solutions are not updated in PSPLIB." | 2025\[20\] |
| 28 | Nurse rostering bounds | dated best solutions and LBs | https://www.schedulingbenchmarks.org/nrp/bounds.html | "3275 | 16-Oct-2026 | Found by: Alfonso Gippini Requeijo, Team Banzai S.L., Madrid, Spain." (BCV-3.46.1, LB also 3275) | 16 Oct 2026\[39\] |
| 29 | Curtois & Qu set | 24 instances | https://link.springer.com/article/10.1007/s10479-017-2693-y | "The planning horizon of the instances ranges from two weeks to 52 weeks, while the number of considered employees ranges from 8 to 150." | 2017\[40\] |
| 30 | SimPy current | 4.1.2, 24 May 2026 | https://pypi.org/project/simpy/4.1.1/ | "4.1.2 May 24, 2026" | read 11 Nov 2026\[41\] |
| 31 | SimPy licence and Python | MIT, ≥3.8 | same | "MIT License (MIT) … Python >=3.8" | read 11 Nov 2026\[41\] |
| 32 | Kingman (1961) citation | 57(4):902–904 | https://ui.adsabs.harvard.edu/abs/1961PCPS...57..902K | "Publication: Proceedings of the Cambridge Philosophical Society … Pub Date: 1961 … DOI: 10.1017/S0305004100036094" | read 11 Nov 2026\[32\] |
| 33 | Keskinocak & Tayur (2004) | pp. 485–554 | https://link.springer.com/chapter/10.1007/978-1-4020-7953-5_12 | "Due Date Management Policies … pp 485–554" | 2004\[24\] |
| 34 | Wiers (2009) | PPC 20(7):576–585 | https://research.tue.nl/en/publications/the-relationship-between-shop-floor-autonomy-and-aps-implementati | "a disagreement concerning autonomy is a key explanatory factor for understanding why an APS implementation may fail." | 2009\[22\] |
| 35 | Ivert (2012) | PPC 23(6):452–467 | https://research.chalmers.se/publication/159554 | "the shop type is influenced by the decision of how often the APS runs and what freedom is given to the shop floor." | 2012\[23\] |
| 36 | Timefold quickstarts | employee and project job scheduling | https://github.com/Optimum-Intelligence/timefold-quickstarts (fork of the official repo) | "📆 Project Job Scheduling | Shadow Variables, Variable Listener, Strenght Comparator" | read 11 Nov 2026\[42\] |
| 37 | Timefold licence | Apache | https://timefold.ai/blog/new-open-source-solver-python | "Timefold Solver for Python is free to use (open source under the Apache License)" | read 11 Nov 2026\[43\] |

## 4. Findings

### Q1. Official modelling examples

**OR-Tools.** Google's own CP page names rostering first: "Here are some examples of scheduling problems that are well-suited for the CP-SAT solver: Employee Scheduling"\[44\] (https://developers.google.com/optimization/cp, read 11 Nov 2026). Official flow-shop, RCPSP and cell/line-assignment samples in the OR-Tools repository: not found in this run (the repository's `examples/` tree could not be fetched; do not cite file names from memory). The CP-SAT release notes now say "Add soft constraint examples" (releases page; version not confirmed).\[45\]

**Timefold.** The quickstarts repository lists "Employee Scheduling | Load Balancing" and "Project Job Scheduling | Shadow Variables, Variable Listener, Strenght Comparator" (read via a fork of the official repository, since the official one was not fetched).\[42\] Timefold's documentation describes project job scheduling as RCPSP-like: "Schedule all jobs in time and execution mode to minimize project delays … This is a form of flexible job shop scheduling." (https://docs.timefold.ai/timefold-solver/0.8.x/use-cases-and-examples/use-cases-and-examples, an old 0.8.x page).\[46\] Timefold's site also lists a "Job shop scheduling" quickstart (https://timefold.ai/constraint-optimization). \[47\] Flow-shop and cell-assignment examples: not found. Python install: "Just pip install timefold and run one of the quickstarts" (Timefold blog).\[43\]

**MiniZinc.** Not covered (no source gathered).

**Gurobi.** Gurobi publishes a `gurobi/modeling-examples` container image ("docker run -p 8888:8888 gurobi/modeling-examples", https://hub.docker.com/r/gurobi/modeling-examples). \[48\] Which notebooks cover flow shop, RCPSP, cell assignment or rostering: not found.

**Verdict:** only rostering (OR-Tools, Timefold) and project scheduling (Timefold) are sourced; the rest is "not found" and should not be written into the skill as links.

### Q2. Multi-objective solves

**Gurobi (13.0 and 14.0 docs).** "Gurobi allows you to enter and manage your objectives, to provide weights for a blended approach, and to set priorities for a hierarchical approach."\[17\] Objectives with equal priority are blended by weight; higher priorities are optimised first, and `ObjNRelTol`/`ObjNAbsTol` let later passes degrade earlier objectives (AIMMS's description of the same behaviour: "Whenever the optimal solution for an objective (or blended objective) is found, Gurobi imposes that, for the remaining (lower priority) objectives, the only solutions considered are those that are also optimal for the previously (higher priority) optimized objectives").\[49\] New in 13.0: `InheritParams` for multi-objective environments and per-pass attributes `ObjPassNMipGap`, `ObjPassNObjBound`, `ObjPassNObjVal` (release notes "Additions, Changes and Removals in Gurobi 13.0").\[16\] What 14.0 changed for multi-objective: not found.

**CPLEX** (22.1.0 manual) works the same way: "The CPLEX multiobjective optimization algorithm sorts the objectives by decreasing priority value. If several objectives have the same priority, they are blended in a single objective using the weight attributes provided."\[25\]

**CP-SAT.** Single objective only. Weighted: write one linear objective with weights. Lexicographic: solve, add `objective == value` (or `<=` if not proven optimal), hint the previous solution, re-solve (Discussion #4183; CP-SAT Primer).\[13\]\[14\]\[15\] A big-M weighting also works for two objectives but "doesn't scale well for >2 objectives" (UPenn CIS 1890 lecture 9, secondary).\[50\]

**Guidance on choosing weights.** A vendor or standards source on choosing weights: not found. Practical rule from the sources above: if an ordering is truly strict, use hierarchy rather than huge weights; use weights only when trade-offs between objectives are acceptable.

### Q3. Test oracles for planners

| Library | Where | What it gives | Licence |
|---|---|---|---|
| Taillard | http://mistic.heig-vd.ch/taillard/ | Flow-, job- and open-shop instances plus "Summary of best known lower and upper bounds" | not found\[18\] |
| PSPLIB | db.wi.tum.de/psplib (address from a thesis; not fetched) | RCPSP sets J30/J60/J90/J120 and multi-mode, with optimal and heuristic solutions | not found\[19\]\[51\]\[52\] |
| Nurse rostering | https://www.schedulingbenchmarks.org/nrp/ | Instances, best solutions and lower bounds with dates and finders | not found\[39\] |
| OR-Library | not fetched | not found in this run | not found |

Caveats: bounds move. Taillard's job-shop ta33 was closed and ta45 solved with OR-Tools (arXiv 2504.16106); a 2019 count put 215 PSPLIB instances still open; and a 2025 paper notes improvements "not updated in PSPLIB".\[20\]\[26\]\[53\] A test should assert "objective ≥ published lower bound" and "objective ≤ published upper bound + tolerance", and record the bound's date.

**Deterministic CP-SAT for reproducible tests.** Use `num_workers=1`, or `interleave_search=True` with a fixed `interleave_batch_size`, plus a fixed `random_seed` and `max_deterministic_time` rather than wall-clock limits (sat_parameters.proto; developer forum).\[10\]\[11\]\[54\]

**Wrong-answer risk.** Issue #5582 on CP-SAT 9.15.6755 reports `OPTIMAL` above the true optimum, "avoided by presolve_inclusion_work_limit: 0", and that "It also happens without a hint."\[7\] This is the strongest current argument for oracle tests on small instances with known optima.

**Property-based testing.** A primary source on property-based testing of optimisation models: not found. The `cpsat-utils` package (secondary, community) provides `assert_feasible`, `assert_optimal` and `assert_objective`, and a hint check (`assert_hint_feasible`).\[55\] OR-Tools itself "Removed fuzztest support from OR-Tools (#4938)" (releases page).\[45\]

### Q4. People in the plan

- **Sequence- and person-dependent setups, cross-training and qualification models:** not covered beyond Timefold's employee scheduling quickstart, which assigns shifts "accounting for employee availability and shift skill requirements".\[56\]
- **Fairness in rostering:** the Curtois & Qu benchmark (24 instances, 8–150 employees, 2–52 weeks) encodes soft constraints such as consecutive working weekends and complete weekends (Timefold's nurse rostering description lists "Minimum and maximum consecutive working weekends" and "Complete weekends").\[40\]\[46\] A primary fairness study: not found.
- **Kingman (1961):** see C5. Citation: Kingman, J.F.C. (1961) "The single server queue in heavy traffic", *Proc. Camb. Phil. Soc.* 57(4), 902–904, DOI 10.1017/S0305004100036094.\[28\]\[32\] The only text found from the paper is its opening: "The process known as the single server queue has been intensively studied in recent years, and various solutions have been obtained." (Semantic Scholar snippet, truncated).\[57\] The heavy-traffic exponential-limit statement is from Kingman (1962), *J. R. Statist. Soc. B* 24(2), 383–392, DOI 10.1111/j.2517-6161.1962.tb00465.x:\[34\]\[58\] "the distribution of (1 – ρ)w tends, as ρ tends to 1, to a negative exponential distribution."\[34\]

### Q5. Quoting due dates

The chapter is Keskinocak, P. and Tayur, S. (2004), "Due Date Management Policies", in Simchi-Levi, Wu and Shen (eds), *Handbook of Quantitative Supply Chain Analysis*, ISOR vol. 74, Springer, pp. 485–554, DOI 10.1007/978-1-4020-7953-5_12.\[24\]\[59\] Its abstract: "an essential value feature for customer acquisition and retention is the ability to quote short and reliable lead times. Reliability is important for customers especially in a business-to-business setting, because it allows them to plan their own operations with more reliability and confidence."\[24\]

A sentence from the chapter stating the cost of quoting short versus long: not found (full text is paywalled). The clearest statement found is from a paper that cites it (Discrete Applied Mathematics, secondary for this point): "promising delivery dates too far into the future may not be acceptable to the customer or may force a company to offer price discounts in order to retain the business. Thus there is an important trade-off between assigning relatively short due dates (lead times) to customer orders and avoiding tardiness penalties." (https://www.sciencedirect.com/science/article/pii/S0166218X1000065X). \[60\] Use it with that attribution, not as Keskinocak and Tayur's words.

### Q6. Discrete-event simulation

SimPy 4.1.2 (24 May 2026) is current; 4.1.0 changes: "[BREAKING] Python 3.8 is the minimum supported version" and "[NEW] Add Process.name property" (SimPy changelog).\[41\]\[61\] SimPy's own scope note: "Though it is theoretically possible to do continuous simulations with SimPy, it has no features that help you with that."\[62\] Other Python DES libraries and their versions: not covered.

### Q7. Dispatching rules

Not covered. One sourced pointer: due-date management policies combine a due-date setting part with "a priority dispatching procedure that is aimed at meeting due‐dates" (ResearchGate summary of Keskinocak and Tayur, secondary).\[63\]

### Q8. Re-planning stability

Not covered (no nervousness or frozen-horizon source gathered). The Timefold quickstarts list "Pinning" as a solver concept (Food Packaging, Bed Allocation, Tournament Scheduling), which is the mechanism for freezing the near term in Timefold.\[42\]

### Q9. Commercial solver licences in containers and CI

**Gurobi.** WLS is "a Gurobi licensing service for containerized environments (Docker, Kubernetes, ...)", with credentials passed as `GRB_WLSACCESSID`, `GRB_WLSSECRET` and `GRB_LICENSEID` environment variables (gurobi/python-example).\[64\] Alternatives: a Token Server outside the cluster, or mounting `gurobi.lic` as a secret.\[21\] Known failure: "Error 10024: Web license service only available for container environments", caused by cgroups v2 hosts on old versions; fix is to update (≥9.5.1 in containers, ≥10.0.0 natively) or run with `--privileged --cgroupns=host`.\[65\] Academic WLS licences last 90 days and need v10+.\[38\] CI implication: CI runners need outbound internet and secrets; forks must not receive them.

**CPLEX.** Vendor guidance on containers and CI: not found.

### Q10. A published failure, and Wiers/Ivert

A published failure blamed on treating workers as deterministic: not found.

- **Wiers, V.C.S. (2009).** "The relationship between shop floor autonomy and APS implementation success: evidence from two cases." *Production Planning & Control* 20(7), 576–585. DOI 10.1080/09537280903034289. Quote: "there can be disagreement between the scheduler and the shop floor about the amount of autonomy permitted on the shop floor post implementation. When this is the case, it often leads to problematic use of APS."\[22\]
- **Kjellsdotter Ivert, L. (2012).** "Shop floor characteristics influencing the use of advanced planning and scheduling systems." *Production Planning & Control* 23(6), 452–467. DOI 10.1080/09537287.2011.564218 (online 2011). Quote: "It is found that the level of data quality needed in the APS system depends to a large extent on how the dispatch list is used. For example, is the dispatch list used as a guideline, not a regulation, the need for accurate data in the module is reduced."\[23\]

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| OR-Tools (CP-SAT) | CP/SAT/MIP solving | 9.15.6755 | 12 Jan 2026 (v9.15, secondary) | `pip install ortools` | none (parameters in code) | developers.google.com/optimization/support/release_notes\[7\]\[35\] |
| Gurobi Optimizer | MIP, multi-objective | 14.0.0 | 10 Nov 2026 (Anaconda); official launch not found | `conda install -c gurobi gurobi` | `gurobi.lic` | anaconda.org/Gurobi/gurobi\[4\] |
| Gurobi 13 line | previous major | 13.0.3 | August 2026 (Gurobi support history; AMPL repackaged it 8 Sep 2026) | as above | `gurobi.lic` | support.gurobi.com/hc/en-us/articles/360048138771 |
| Timefold Solver | constraint solver (Java, Python) | 2.7.1 (1.x line: 1.35.0, 16 Oct 2026, Maven Central) | 6 Oct 2026 | `pip install timefold`\[43\] | `solverConfig.xml` (not verified) | github.com/timefoldai/timefold-solver/releases |
| SimPy | discrete-event simulation | 4.1.2 | 24 May 2026 | `pip install simpy` | none | pypi.org/project/simpy |
| cpsat-utils (community) | CP-SAT test helpers | not found | not found | not found | none | github.com/d-krupke/cpsat-utils |
| gurobi/optimizer image | Gurobi in Docker | follows Gurobi | not found | `docker run --volume=$PWD/gurobi.lic:/opt/gurobi/gurobi.lic:ro …`\[21\] | `gurobi.lic` | hub.docker.com/r/gurobi/optimizer |

## 6. Changing in the next 12 months

- **Gurobi 14.0** is shipping now (package 10 Nov 2026; webinars 1 and 3 Dec 2026).\[4\]\[5\] Update any facts file that names 13.0 as current.
- **Gurobi 12.0 end of support is November 2027** (flag: within 12 months); Gurobi's support-history table lists 12.0.0 as "11/2024 | Supported | 11/2027".
- **Gurobi 11.0** support ends this month (November 2026): the same Gurobi table lists 11.0.0 as "11/2023 | Supported | 11/2026", and states "Starting with major release 10, all Gurobi product releases are supported for a term of three years after the initial release of the corresponding major release."
- **OR-Tools v9.16** is a milestone with no announced date; fixes for issue #4985 (`status_name()` TypeError) are targeted to it. Whether #5582 is fixed on `main` is unknown.\[7\]\[8\]
- **CP-SAT `interleave_search`** stays "Experimental", so its behaviour may change without notice.\[10\]
- **Timefold Solver 1.x maintenance ends around the end of 2026** (flag: within 12 months): Timefold's blog says "Timefold Solver Community Edition 1.x will be maintained throughout 2026 with quarterly bug-fix releases and security updates." End-of-support dates for SimPy and OR-Tools: not found.

## 7. Common mistakes

1. **Calling a CP-SAT multi-worker run reproducible.** The default portfolio is not deterministic; use one worker or `interleave_search` (sat_parameters.proto).\[12\]
2. **Using wall-clock time limits in tests.** Results then depend on machine load; use `max_deterministic_time` (sat_parameters.proto: "Maximum time allowed in deterministic time to solve a problem").\[36\]
3. **Inventing a CP-SAT lexicographic API.** AI assistants write calls like `model.minimize_lexicographic(...)`; no such method is documented. Use the fix-and-resolve loop (Discussion #4183).\[13\]
4. **Fixing the earlier objective with `int()` of a float.** Recipes advise "use round() instead of int()" and "use <= or >= if not optimal" (xiang.es CP-SAT recipes, secondary).\[15\]
5. **Trusting `OPTIMAL` without an oracle.** Issue #5582.\[7\]
6. **Baking a Gurobi licence into an image, or using a host-bound academic licence in a container.** Gurobi: "The standard academic licenses for Gurobi do not work in docker containers."\[66\]
7. **Quoting Kingman's ρ/(1−ρ) formula as text from the 1961 paper.** See C5.
8. **Treating PSPLIB's posted bounds as current.** Some improvements are not uploaded (arXiv 2502.18330).\[20\]
9. **Citing Wiers or Ivert as showing that shop floors "ignore" schedules.** They show disputed autonomy and dispatch lists treated as guidelines.\[22\]\[23\]

## 8. Sources and licences

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| OR-Tools repository and `sat_parameters.proto` | Apache-2.0 (PandaStack table: "OR-Tools / CP-SAT | Apache-2.0") | Yes | Yes | Yes | Keep NOTICE; name "Google OR-Tools"\[12\] |
| OR-Tools developer site | not found (Google Developers pages are usually CC BY 4.0, code Apache-2.0; not verified) | Briefly | Yes | Only after verifying | Link the page |
| OR-Tools issues and discussions | GitHub terms; author copyright | Briefly | Yes | No | Link the issue |
| CP-SAT Primer (d-krupke) | not found | Briefly | Yes | Not until licence confirmed | Name author and link |
| Gurobi docs, support articles, Docker Hub pages | Proprietary (Gurobi) | Briefly | Yes | No, unless the example's own licence allows | "Gurobi Optimization, LLC", link |
| IBM CPLEX manual | Proprietary (IBM) | Briefly | Yes | No | Link |
| Timefold quickstarts and blog | Apache License (stated for Solver) | Yes | Yes | Yes, for Apache-licensed code | Keep NOTICE; name Timefold |
| SimPy (PyPI, docs) | MIT | Yes | Yes | Yes | Keep MIT notice |
| Taillard benchmark site | not found | Briefly | Yes | Data: ask before redistributing | Cite Taillard (1993) |
| PSPLIB / PyJobShop PSPLIB README | not found | Briefly | Yes | No | Cite Kolisch & Sprecher (1997) |
| schedulingbenchmarks.org | not found | Briefly | Yes | Data: ask before redistributing | Cite Curtois & Qu (2014) |
| arXiv papers (1909.02737, 2502.18330, 2504.16106) | per-paper licence; not checked | Briefly | Yes | No | Full citation |
| Springer, Wiley, Taylor & Francis papers | Publisher copyright | Briefly (fair use) | Yes | No | Full citation with DOI |
| TU/e and Chalmers research portals | not found | Briefly | Yes | No | Full citation |
| Wikipedia | CC BY-SA 4.0 | Briefly | Yes | No (share-alike conflicts with Apache-2.0) | Link and licence |
| AMPL changelog, PandaStack, xiang.es, UPenn lecture | not found | Briefly | Yes | No | Link, label secondary |

## 9. Not found, contested, not covered

**Not found:** R28's result and facts file (tool refused the fetch; the repository is public, so the receiving session should diff locally); official OR-Tools flow-shop, RCPSP and line-assignment samples; Gurobi example notebooks by topic; OR-Library's location and licence; licences for Taillard, PSPLIB and schedulingbenchmarks.org; the exact wording of Kingman (1961) beyond its opening sentence; a sentence by Keskinocak and Tayur on short-versus-long quoting costs; vendor guidance on choosing weights; CPLEX container and CI licensing; a published failure blamed on deterministic workers; end-of-support policies for OR-Tools and SimPy. (Timefold Solver's current version is 2.7.1, released 6 Oct 2026, per its GitHub releases page, and its 1.x line is maintained through 2026.)

**Contested:** whether Kingman's mean-wait "VUT" approximation should be attributed to the 1961 paper (secondary sources say yes; the primary text found does not show it).\[33\]\[67\] Whether `interleave_search` counts as a supported deterministic mode (documented, but labelled "Experimental").\[10\]

**Not covered:** MiniZinc examples; property-based testing frameworks applied to models; person- and sequence-dependent setup models; cross-training models; rostering fairness literature; dispatching rules versus solvers; nervousness and frozen horizons; other Python DES libraries.

## Sources

1. [research: bring the eleven unrun prompts up to date before they run by rmccann-hub · Pull Request #128 · rmccann-hub/claude-code-skills · GitHub](https://github.com/rmccann-hub/claude-code-skills/pull/128)
2. [git-workflows: what the two audited repositories' week taught by rmccann-hub · Pull Request #124 · rmccann-hub/claude-code-skills · GitHub](https://github.com/rmccann-hub/claude-code-skills/pull/124)
3. [Gurobi Optimizer Reference Manual](https://docs.gurobi.com/projects/optimizer/en/current/)
4. [gurobi - Gurobi](https://anaconda.org/Gurobi/gurobi)
5. [What's New in 14.0 Webinar](https://www.gurobi.com/resources/webinar-events/what-is-new-in-14.0-webinar)
6. [What's New - Gurobi 13.0](https://www.gurobi.com/whats-new-gurobi-13-0/)
7. [CP-SAT 9.15.6755: OPTIMAL reported above the true optimum depending on the solution hint (avoided by presolve\_inclusion\_work\_limit: 0) · Issue #5582 · google/or-tools · GitHub](https://github.com/google/or-tools/issues/5582)
8. [solver.status\_name() raises TypeError: 'ortools.sat.python.cp\_model\_helper.CpSolverStatus' object is not callable · Issue #4985 · google/or-tools · GitHub](https://github.com/google/or-tools/issues/4985)
9. [OR-Tools Release Notes](https://developers.google.com/optimization/support/release_notes)
10. [or-tools/ortools/sat/sat\_parameters.proto at 98c165af62df62b3056c2ee0fca66b24e79097cb · google/or-tools · GitHub](https://github.com/google/or-tools/blob/98c165af62df62b3056c2ee0fca66b24e79097cb/ortools/sat/sat_parameters.proto)
11. [Seeding CP-SAT solver](https://groups.google.com/g/or-tools-discuss/c/lPb1FzhTMt0)
12. [Optimisation Solver as a Service: MicroVM Isolation · PandaStack](https://www.pandastack.ai/blog/microvm-optimization-solver-as-a-service-isolation/)
13. [Multiple objectives using blocking constraints · google/or-tools · Discussion #4183 · GitHub](https://github.com/google/or-tools/discussions/4183)
14. [Basic Modeling - The CP-SAT Primer - Using and Understanding Google OR-Tools' CP-SAT Solver](https://d-krupke.github.io/cpsat-primer/modelling.html)
15. [✨ Recipes for Google OR-Tools](https://xiang.es/posts/cp-sat/)
16. [Additions, Changes and Removals in Gurobi 13.0 - Gurobi Optimizer Reference Manual](https://docs.gurobi.com/projects/optimizer/en/current/reference/releasenotes/changes.html)
17. [Multiple Objectives - Gurobi Optimizer Reference Manual](https://docs.gurobi.com/projects/optimizer/en/current/features/multiobjective.html)
18. [Scheduling instances](http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html)
19. [GitHub - PyJobShop/PSPLIB: Project scheduling instance parser. · GitHub](https://github.com/PyJobShop/PSPLIB)
20. [A hybrid heuristic algorithm for the resource-constrained project scheduling problem](https://arxiv.org/pdf/2502.18330)
21. [hub.docker.com](https://hub.docker.com/r/gurobi/optimizer)
22. [The relationship between shop floor autonomy and APS implementation success : evidence from two cases — Eindhoven University of Technology Research Portal](https://research.tue.nl/en/publications/the-relationship-between-shop-floor-autonomy-and-aps-implementati)
23. [Shop floor characteristics influencing the use of advanced planning and scheduling systems](https://research.chalmers.se/publication/159554)
24. [Due Date Management Policies](https://link.springer.com/chapter/10.1007/978-1-4020-7953-5_12)
25. [Solving multiple objective problems](https://www.ibm.com/docs/zh/SSSA5P_22.1.0/ilog.odms.cplex.help/CPLEX/UsrMan/topics/multiobj/multiobj_solving.html)
26. [Strong Bounds for Resource Constrained Project Scheduling: Preprocessing and Cutting Planes](https://arxiv.org/pdf/1909.02737)
27. [simpy · PyPI](https://pypi.org/project/simpy/4.0.0/)
28. [Kingman, J. F. C. (1961) The single server queue in heavy traffic. Mathematical Proceedings of the Cambridge Philosophical Society, 57 (4). 902-904 doi:10.1017/s0305004100036094](https://www.mindat.org/reference.php?id=7917667)
29. [\[2206.09844\] Heavy-traffic single-server queues andthe transform method](https://ar5iv.labs.arxiv.org/html/2206.09844)
30. [Kingman’s Formula](https://blog.mikebowler.ca/2026/09/28/kingmans-formula/)
31. [1 queue](https://en.wikipedia.org/wiki/G/G/1_queue)
32. [The single server queue in heavy traffic - ADS](https://ui.adsabs.harvard.edu/abs/1961PCPS...57..902K)
33. [Kingman's formula](https://en.wikipedia.org/wiki/Kingman's_formula)
34. [On Queues in Heavy Traffic - Kingman - 1962 - Journal of the Royal Statistical Society: Series B (Methodological) - Wiley Online Library](https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1962.tb00465.x)
35. [OR-Tools](https://en.wikipedia.org/wiki/OR-Tools)
36. [or-tools/ortools/sat/sat\_parameters.proto at stable · google/or-tools · GitHub](https://github.com/google/or-tools/blob/stable/ortools/sat/sat_parameters.proto)
37. [Gurobi Releases Version 13.0 with Improved Performance and New Solving Capabilities - Gur](https://www.gurobi.com/company/newsroom/gurobi-releases-version-13-0-with-improved-performance-and-new-solving-capabilities)
38. [What is an Academic WLS license?](https://support.gurobi.com/hc/en-us/articles/13210193318033-What-is-an-Academic-WLS-license)
39. [Nurse Rostering Lower bounds and references](https://www.schedulingbenchmarks.org/nrp/bounds.html)
40. [Modeling and solving staff scheduling with partial weighted maxSAT](https://link.springer.com/article/10.1007/s10479-017-2693-y)
41. [simpy · PyPI](https://pypi.org/project/simpy/4.1.1/)
42. [GitHub - Optimum-Intelligence/timefold-quickstarts: Get started with Timefold quickstarts here. Optimize the vehicle routing problem, employee rostering, task assignment, maintenance scheduling and other planning problems. · GitHub](https://github.com/Optimum-Intelligence/timefold-quickstarts)
43. [Python Solver for Routing and Scheduling](https://timefold.ai/blog/new-open-source-solver-python)
44. [Constraint Optimization | OR-Tools | Google for Developers](https://developers.google.com/optimization/cp)
45. [Releases · google/or-tools · GitHub](https://github.com/google/or-tools/releases)
46. [Use cases and examples](https://docs.timefold.ai/timefold-solver/0.8.x/use-cases-and-examples/use-cases-and-examples?platform=1)
47. [Programming Constraint Solver and Optimization APIs](https://timefold.ai/constraint-optimization)
48. [modeling examples](https://hub.docker.com/r/gurobi/modeling-examples)
49. [Multi-Objective Optimization — AIMMS User's Guide](https://documentation.aimms.com/user-guide/aimms-ide/Solvers/GUROBI/GUROBI_Multi-Objective_Optimization.html)
50. [Lecture 9: More Constraint Programming](https://www.cis.upenn.edu/~cis1890/files/Lecture9.pdf)
51. [(PDF) Mixed integer programming formulations for the robust, resource-constrained project scheduling problem](https://www.researchgate.net/publication/365991497_Mixed_integer_programming_formulations_for_the_robust_resource-constrained_project_scheduling_problem)
52. [An Effective Two-Phase Genetic Algorithm for Solving the Resource Constrained Project Scheduling Problem (RCPSP)](https://arxiv.org/pdf/2506.21915)
53. [Updating Lower and Upper Bounds for the Job-Shop Scheduling Problem Test Instances](https://www.alphaxiv.org/abs/2504.16106)
54. [feat(planning): Solver CP-SAT jako podmiana heurystyki za tym samym interfejsem · Issue #92 · HackYeah-TuttiTripTeam/tuttitrip-backend · GitHub](https://github.com/HackYeah-TuttiTripTeam/tuttitrip-backend/issues/92)
55. [GitHub - d-krupke/cpsat-utils: A utils package for Google's ortools CP-SAT solver · GitHub](https://github.com/d-krupke/cpsat-utils)
56. [GitHub - MetaBarj0/timefold-quickstarts: Get started with Timefold quickstarts here. Optimize the vehicle routing problem, employee rostering, task assignment, maintenance scheduling and other planning problems. · GitHub](https://github.com/MetaBarj0/timefold-quickstarts)
57. [The virtual waiting time of the GI/G/1 queue in heavy traffic](https://www.semanticscholar.org/paper/The-virtual-waiting-time-of-the-GI-G-1-queue-in-Kyprianou/f393ff10b949a5b0a53a282addafaf16a1070c4e)
58. [Gaussian Limits for Scheduled Traffic with Super-Heavy Tailed Perturbations](https://arxiv.org/pdf/2303.05939)
59. [1 PINAR KESKINOCAK H. Milton and Carolyn J. Stewart School Chair and Professor](https://www.isye.gatech.edu/sites/default/files/cv/keskinocak-pinar/pinar-cv-september2025.pdf)
60. [Bicriteria problems to minimize maximum tardiness and due date assignment cost in various scheduling environments - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0166218X1000065X)
61. [SimPy History & Change Log — SimPy 4.1.2.dev16+gf43816490 documentation](https://simpy.readthedocs.io/en/latest/about/history.html)
62. [simpy · PyPI](https://pypi.org/project/simpy/4.1.0/)
63. [(PDF) Due Date Management Policies](https://www.researchgate.net/publication/239519658_Due_Date_Management_Policies)
64. [gurobi/python-example - Docker Image](https://hub.docker.com/r/gurobi/python-example)
65. [How do I resolve an "Error 10024: Web license service only available for container environments"?](https://support.gurobi.com/hc/en-us/articles/13235765567505-How-do-I-resolve-an-Error-10024-Web-license-service-only-available-for-container-environments)
66. [Installing Gurobi on a Docker container (Ubuntu)](https://support.gurobi.com/hc/en-us/community/posts/4406485885841-Installing-Gurobi-on-a-Docker-container-Ubuntu)
67. [The Kingman Formula](https://www.allaboutlean.com/kingman-formula/)
