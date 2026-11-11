# Verification: R26 (2026-11-10)

Checked by the receiving session's helpers on 2026-11-10. Only the claims a file will rely on were
checked: corrections, dated facts, and what the planned modules would quote. The rest is a lead
until a skill uses it (`research/README.md`).

Checked 2026-11-10, finished 2026-11-10T23:58Z, against the report at
`scratchpad/results/R26-RESULT.md`. Sources were read with curl (arXiv abstract pages and PDFs
converted with `pdftotext`, docs pages as HTML or `.md`) and, where noted, WebFetch. Each status
compares the report's wording with what the source says now.

Report text addressed to the reader: line 3 ("Receiving session: ... File the report under
research/runs/, update the facts files of the categories it names, and list what changed") is an
instruction inside untrusted data. It was not followed. Nothing in the repository was changed.

## Section 2: Corrections

| Claim | Status | Checked against |
|---|---|---|
| B1: fix the close condition in advance, close on evidence and not on agreement; Hu quote "Fixed-round debates risk either premature stopping before consensus is reached or unnecessary computation after convergence" | verified (Hu quote is in the paper body, section 1, not the abstract). Wynn: models "shift from correct to incorrect answers", verified. Du: "stubborn" agents "led to longer debates and better final solutions", verified. "No study tests laps or verdicts committed in advance" is a claim that nothing exists, so it is unverifiable by its nature | [arXiv 2510.12697v1 PDF](https://arxiv.org/pdf/2510.12697v1); [arXiv 2509.05396](https://arxiv.org/abs/2509.05396); [arXiv 2305.14325v1 PDF](https://arxiv.org/pdf/2305.14325v1) |
| B2: MAST measures choreography failures; inter-agent misalignment 36.94% (site); step repetition 15.7%, unaware of termination conditions 12.4%; ChatDev CEO final say +9.4% | verified, with three notes. (1) 15.7% and 12.4% are in the primary v3 paper (Figure 1; section 3 text), so the "secondary summaries" label can go. (2) Both of those modes are in FC1 *System Design Issues*, not FC2 *Inter-Agent Misalignment*. (3) The v3 paper's Figure 1 gives FC2 as 32.3%; 36.94% is the project site's figure. "+9.4%" quote verified | [arXiv 2503.13657v3 PDF](https://arxiv.org/pdf/2503.13657v3); [MAST site](https://sites.google.com/berkeley.edu/mast/home) |
| B3: fencing token definition (Kleppmann); compare-and-set as the fix | Kleppmann quote verified on the primary blog (published 08 Feb 2016). "Fencing cannot order two writers when the lower token arrives first, with Kleppmann's agreement" (surfingcomplexity.blog): unverifiable, because the post was not found in two searches. Compare-and-set (a git push that must build on the latest commit) is the report's own reasoning, and no source is claimed for it | [martin.kleppmann.com](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html) |
| B4: Claude Code Review works "without building or running your code"; Anthropic: humans retain control "particularly before high-stakes decisions are made"; Copilot approvals count once an admin enables them | verified | [code.claude.com code-review](https://code.claude.com/docs/en/code-review); [Anthropic framework](https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents); [GitHub changelog 2026-10-28](https://github.blog/changelog/2026-10-28-copilot-code-review-merge-with-confidence-with-max-and-approvals/) |
| B5: Google: consensus, then escalate; "Don't let a CL sit around..."; writing the ruling down "not found as published practice", only a secondary source says so | first half verified. **Contradicted on the second half: Google's primary page says it: "(If you do this, though, make sure to record the results of the discussion as a comment on the CL, for future readers.)"** It says to record the outcome of a face-to-face resolution, though not "once, verbatim". The dev.to secondary source is not needed | [Google, The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html) |

## Section 3: Facts table

| Claim | Status | Checked against |
|---|---|---|
| #1 Du et al.: multiagent debate method quote; 2023-05-23 | verified (v1 23 May 2023). Venue ICML 2024 verified (PMLR 235:11733-11763) | [arXiv 2305.14325](https://arxiv.org/abs/2305.14325); [PMLR du24e](https://proceedings.mlr.press/v235/du24e.html) |
| #2 Du et al.: rounds plateau at about 4 | verified | [arXiv 2305.14325v1 PDF](https://arxiv.org/pdf/2305.14325v1) |
| #3 Du et al.: stubborn agents help | verified (the source has mismatched quote marks: “stubborn’) | [arXiv 2305.14325v1 PDF](https://arxiv.org/pdf/2305.14325v1) |
| Du et al. headline numbers: arithmetic 81.8 vs 67.0, GSM8K 85.0 vs 77.0 (section 4) | verified (Table 1) | [arXiv 2305.14325v1 PDF](https://arxiv.org/pdf/2305.14325v1) |
| #4 Choi, Zhu, Li: "Majority Voting alone accounts for most..."; NeurIPS 2025; v1 2025-08-24, v2 2025-10-23 | verified (comments: "NeurIPS 2025 Spotlight") | [arXiv 2508.17536](https://arxiv.org/abs/2508.17536) |
| #5 Choi et al.: debate is a martingale; "does not improve expected correctness" | verified | [arXiv 2508.17536](https://arxiv.org/abs/2508.17536) |
| #6 Choi et al. Qwen2.5-7B averages 0.7377 / 0.7112 / 0.7050, majority vote 0.7691; Llama 0.7242 | verified (Table: Decentralized MAD T=2/3/5; Majority Voting). These are Decentralized MAD rows only: Sparse MAD T=2 (0.7330) and Centralized MAD also lose to voting | [arXiv 2508.17536v2 PDF](https://arxiv.org/pdf/2508.17536v2) |
| #7 Wynn et al.: "debate can lead to a decrease in accuracy over time..." ; v2 2025-10-13 | verified (abstract uses a hyphen and the v2 PDF an em dash). Venue: ICML MAS Workshop 2025 | [arXiv 2509.05396](https://arxiv.org/abs/2509.05396) |
| #8 Wynn et al.: "...neither incentivized nor adequately equipped..." | verified in the v1 PDF ("incentivized"). The current v2 abstract spells it "incentivised" | [arXiv 2509.05396v1 PDF](https://arxiv.org/pdf/2509.05396v1); [arXiv 2509.05396](https://arxiv.org/abs/2509.05396) |
| Wynn et al.: 12-point MMLU drop 40.0 to 28.0; CommonSenseQA lowered in every configuration (sections 1, 4) | verified (Table 1, ↓12.0; text: "debate always harms performance" on CommonSenseQA). "One GPT plus two Mistral" is unverifiable as text, because the configuration column is icons that `pdftotext` drops | [arXiv 2509.05396v2 PDF](https://arxiv.org/pdf/2509.05396v2) |
| #9 Huang et al. ICLR 2024: "LLMs struggle to self-correct their responses without external feedback, and at times, their performance might even degrade post self-correction" | verified against the v1 abstract (2023-10-03). The current v2 abstract (2024-03-14) reads "...and at times, their performance even degrades after self-correction". Quote v2, or name v1. Cite arXiv, not the axi.lims.ac.uk mirror | [arXiv 2310.01798v1](https://arxiv.org/abs/2310.01798v1); [arXiv 2310.01798](https://arxiv.org/abs/2310.01798) |
| Huang et al.: multi-agent debate no better than self-consistency at equal cost (section 4) | verified ("its efficacy is no better than self-consistency ... when considering an equivalent number" of responses) | [arXiv 2310.01798v2 PDF](https://arxiv.org/pdf/2310.01798v2) |
| #10 Smit et al.: debate does not reliably outperform self-consistency and ensembling; ICML 2024 | verified (PMLR 235:45883-45905) | [arXiv 2311.17371](https://arxiv.org/abs/2311.17371); [PMLR smit24a](https://proceedings.mlr.press/v235/smit24a.html) |
| #11 MAST: 1,642 traces, 7 frameworks, 14 modes, 3 categories; v3 2025-10-26 | verified. The abstract says "1600+"; 1,642 is in the v3 body ("1642 annotated execution traces"). Failure rates "41% to 86.7%" verified | [arXiv 2503.13657](https://arxiv.org/abs/2503.13657); [arXiv 2503.13657v3 PDF](https://arxiv.org/pdf/2503.13657v3) |
| #12 MAST category shares 41.77 / 36.94 / 21.30 (project site) | verified on the site. The v3 paper's Figure 1 gives 44.2 / 32.3 / 23.5, so section 9's "contested" figures come from the primary v3, not only secondary summaries. Quote one source and name it | [MAST site](https://sites.google.com/berkeley.edu/mast/home); [arXiv 2503.13657v3 PDF](https://arxiv.org/pdf/2503.13657v3) |
| #13 Hu et al.: fixed rounds premature or wasteful; 2025-10-14 | verified (body text) | [arXiv 2510.12697v1 PDF](https://arxiv.org/pdf/2510.12697v1) |
| Hu et al.: stopped after 2–8 rounds instead of 10, losing 0.00 to 1.03 points; the "if all agents agree, the process terminates..." quote (section 4 Q6) | verified (Table 2: rounds 2–8, Diff 0.00 to −1.03, max 10 rounds; section 3 quote exact) | [arXiv 2510.12697v1 PDF](https://arxiv.org/pdf/2510.12697v1) |
| #14 ARMOR-MAD: PAR/EASE quote; 2026-06 preprint | verified (v1 2026-06-11) | [arXiv 2606.13197](https://arxiv.org/abs/2606.13197) |
| ARMOR-MAD skipped debate on 89.5% of GSM8K where 2 of 3 agreed (section 4) | verified (skip-rate table; τ = 0.67, "at least two out of three agents agreeing") | [arXiv 2606.13197v1 PDF](https://arxiv.org/pdf/2606.13197v1) |
| "agreement among agents is not evidence of correctness": who said it | verified as Wang et al., "From Debate to Decision: Conformal Social Choice for Safe Multi-Agent Deliberation", v1 (2026-04-09) abstract. A v2 appeared on 2026-10-20 (after the report's v1 citation), and its abstract shortens it to "agreement is not evidence of correctness". Quote the version named | [arXiv 2604.07667v1 PDF](https://arxiv.org/pdf/2604.07667v1); [arXiv 2604.07667](https://arxiv.org/abs/2604.07667) |
| Wang et al.: 81.9% of wrong-consensus cases at α=0.05; Claude Haiku, DeepSeek-R1, Qwen-3 32B; 8 MMLU-Pro domains | verified (v1: "81.9% of wrong-consensus cases are intercepted at α=0.05"; v2 says "flagged"). The Haiku model is Claude Haiku 4.5 | [arXiv 2604.07667v1 PDF](https://arxiv.org/pdf/2604.07667v1) |
| #15 Anthropic: pause at checkpoints; stopping conditions | verified (source apostrophe is curly: "it’s"); published Dec 19, 2024 | [Building effective agents](https://www.anthropic.com/research/building-effective-agents) |
| #16 Anthropic: "ground truth" from the environment | verified | [Building effective agents](https://www.anthropic.com/research/building-effective-agents) |
| #17 Anthropic: humans retain control before high-stakes decisions | verified. The page is dated Aug 4, 2025 (the report gives only a read date) | [Anthropic framework](https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents) |
| Anthropic: Claude Code "must ask for human approval before taking any actions that modify code or systems" (section 4 Q7) | verified | [Anthropic framework](https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents) |
| #18 Claude Code Review never approves or blocks | verified | [code.claude.com code-review](https://code.claude.com/docs/en/code-review) |
| #19 "A review with no findings doesn't mean your code is error-free or secure." | verified | [code.claude.com code-review](https://code.claude.com/docs/en/code-review) |
| #20 works "without building or running your code" | verified | [code.claude.com code-review](https://code.claude.com/docs/en/code-review) |
| #21 `REVIEW.md` from the base or default branch, never the PR's own changes | verified. Caveat from the customize page: which copy is read depends on branch protection, and with protection unconfirmed no `REVIEW.md` is read at all | [code.claude.com code-review](https://code.claude.com/docs/en/code-review); [code-review-customize](https://code.claude.com/docs/en/code-review-customize.md) |
| Section 4: "reads `REVIEW.md` and `CLAUDE.md` from the base branch only" | `REVIEW.md` part verified. **The `CLAUDE.md` part is not in the docs**: the customize page says a review reads the root `CLAUDE.md` and those in parent directories of each changed file, and names no branch. The report's cited source for it is a secondary changelog site (gradually.ai) | [code-review-customize](https://code.claude.com/docs/en/code-review-customize.md) |
| #22 Team and Enterprise; not with ZDR or HIPAA; not with customer-managed keys (section 4) | verified (CMEK: "isn't yet available") | [code.claude.com code-review](https://code.claude.com/docs/en/code-review) |
| Section 4: verification step "checks the candidate findings against the code and filters out false positives"; check run "doesn't conclude as a failure"; default focus "bugs that would break production" | verified on the rendered HTML page (the `.md` export words the verification step differently) | [code.claude.com code-review](https://code.claude.com/docs/en/code-review) |
| Section 4: `/code-review` (alias `/review`) runs on any plan; "Posting its findings to a pull request needs Claude Code v2.1.227 or later" | alias and any-plan verified. **Contradicted on the version: v2.1.227 is the minimum for posting *Ultrareview* findings (`/code-review ultra`, `--post`). The page gives no minimum version for `--comment`, which posts findings as inline comments** | [code-review-local](https://code.claude.com/docs/en/code-review-local.md) |
| #23 Copilot approvals GA 2026-10-28; count toward required approvals | verified (page dated October 28, 2026; "previously available in public preview, are now generally available") | [GitHub changelog 2026-10-28](https://github.blog/changelog/2026-10-28-copilot-code-review-merge-with-confidence-with-max-and-approvals/) |
| #24 approvals off by default; admin levels; file paths | verified | same |
| #25 approval dismissed on new commits | verified | same |
| #26 Max effort: public preview; aggregation agent quote | verified | same |
| Section 4: "Each review includes an approval assessment" | verified ("Every review includes an approval assessment in the pull request overview comment") | same |
| #27 GitHub: supplement with careful human review | verified | [GitHub responsible use](https://docs.github.com/en/copilot/responsible-use/code-review) |
| #28 "Copilot may not follow every instruction perfectly every time." | verified | [GitHub customize code review](https://docs.github.com/en/copilot/tutorials/customize-code-review) |
| Section 4: Copilot "may repeat the same comments again, even if they have been dismissed or downvoted" | behaviour verified; **contradicted on the wording, which is out of date: the current docs say "When re-reviewing, Copilot may repeat previous comments, even if you resolved or downvoted them."** | [GitHub use Copilot code review](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review) |
| Section 4: Copilot may miss problems in large or complex changes; may hallucinate | verified (responsible-use page: "especially where changes are large or complex"; hallucination is defined as a limitation there) | [GitHub responsible use](https://docs.github.com/en/copilot/responsible-use/code-review) |
| Section 4: Copilot "ignores instructions to block merges" | unverifiable: not on the three GitHub pages read | [GitHub customize code review](https://docs.github.com/en/copilot/tutorials/customize-code-review) |
| #29 Google: one business day maximum | verified on the primary page (the report quoted it through cubic.dev) | [Google, Speed of Code Reviews](https://google.github.io/eng-practices/review/reviewer/speed.html) |
| #30 Google: response time, not total time | verified | same |
| #31 Google: favor approving once a CL "definitely improves the overall code health" | verified | [Google, The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html) |
| #32 Google: escalation path quote | verified on the primary page (the report used a ctxs.ai copy) | same |
| Google: "Technical facts and data overrule opinions and personal preferences." (section 4) | verified on the primary page (the report used dev.to) | same |
| #33 Google: large changes, points "missed or dropped" | verified | [Google, Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) |
| #34 eng-practices repository archived 21 Nov 2025 | verified on the primary page: "This repository was archived by the owner on Nov 21, 2025. It is now read-only." (WebFetch) | [github.com/google/eng-practices](https://github.com/google/eng-practices) |
| #35 Pact: shared understanding quote | verified | [Pact, Writing Consumer tests](https://docs.pact.io/consumer) |
| #36 Pact: tests as loose as possible | verified | same |
| #37 Pact: `can-i-deploy` gives "a definitive answer" | verified | same |
| #38 oasdiff: exit code 0 or 1 for `oasdiff breaking` | verified | [oasdiff docs](https://oasdiff.com/docs) |
| #39 Kleppmann fencing token quote; 2016-02-08 | verified on the primary blog ("Published by Martin Kleppmann on 08 Feb 2016"). The wisc.edu copy is not needed | [martin.kleppmann.com](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html) |
| #40 Current Claude Code is 2.1.321 | **Contradicted: 2.1.322 was published to npm at 2026-11-10T01:58Z and is `latest` and `next`, and it heads CHANGELOG.md. `stable` is 2.1.311.** Accurate as written: Claude Desktop bundles 2.1.321, both in v4.23118.1 (2026-11-09) and in v5.1231.0 (2026-11-10) | [npm registry](https://registry.npmjs.org/@anthropic-ai/claude-code); [CHANGELOG.md](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md); [Claude Desktop changelog](https://claude.com/docs/cowork/changelog) |
| #41 Repository licence Apache-2.0, standard keeps CC0-1.0; release v0.1.0 dated 2025-09-23 | quote verified on the release page; Apache-2.0 `LICENSE` and the standard's `license: CC0-1.0` confirmed locally. **Contradicted on the date: v0.1.0 is 2026-09-23** (tag commit 2026-09-23 09:24 -0400; the release page shows "23 Sep" with no year) | [Release v0.1.0](https://github.com/rmccann-hub/claude-code-skills/releases/tag/v0.1.0) |

## Sections 6 and 7: dated facts, and section 8 licences

| Claim | Status | Checked against |
|---|---|---|
| Opus 4.8 fast mode ends 30 Nov 2026; Claude Code 2.1.316 deprecated it (secondary: claude-world.com) | verified on the primary source, so the secondary label can go: under 2.1.316, "Deprecated fast mode for Opus 4.8 as of October 30, 2026; it will be removed on November 30, 2026." | [CHANGELOG.md](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) |
| Copilot Max in public preview since 28 Oct 2026, "subject to change" | public preview since 2026-10-28 verified. "Subject to change" is not on the changelog page, so it is unverifiable there | [GitHub changelog 2026-10-28](https://github.blog/changelog/2026-10-28-copilot-code-review-merge-with-confidence-with-max-and-approvals/) |
| Copilot "Default" effort maps to Balanced from 28 Sep 2026 (secondary: dev.to) | verified on the primary source: "This change took effect September 28, 2026." | [GitHub changelog 2026-10-02](https://github.blog/changelog/2026-10-02-copilot-code-review-api-support-and-new-default-effort-level) |
| Google eng-practices archived; static site remains | verified (archived Nov 21, 2025; site pages load) | [github.com/google/eng-practices](https://github.com/google/eng-practices) |
| Section 8: arXiv licences "not checked individually", except MAST CC BY-NC-ND 4.0 | MAST CC BY-NC-ND 4.0 verified. Per abstract page: **2510.12697 (Hu) is also CC BY-NC-ND 4.0**; 2305.14325, 2508.17536, 2509.05396, 2310.01798, 2311.17371 and 2604.07667 are CC BY 4.0; 2606.13197 is arXiv's non-exclusive distribution licence | [arXiv 2510.12697](https://arxiv.org/abs/2510.12697) and each abstract page above |
| Everything else in the report | not yet checked | checked when a skill that relies on it is built (`research/README.md`) |

Not yet checked, as nothing above relies on them: arcusx.ai "rubber stamp", Copilot resolve-reasons (27 Aug 2026), Copilot skipping lockfiles and SVGs, quasa.io, smartscope.blog, surfingcomplexity.blog, the v0.1.25 release date, the GitHub "About" panel licence, and Du's ICML venue beyond PMLR.

## Exact quotes for facts rows

Copied from the sources as read on 2026-11-10. Curly quotes and dashes are kept as the source
has them.

1. Choi, Zhu, Li (NeurIPS 2025 Spotlight), voting: "Through extensive experiments across seven NLP benchmarks, we find that Majority Voting alone accounts for most of the performance gains typically attributed to MAD." [arXiv 2508.17536](https://arxiv.org/abs/2508.17536)
2. Choi et al., martingale: "We prove that it induces a martingale over agents' belief trajectories, implying that debate alone does not improve expected correctness." [arXiv 2508.17536](https://arxiv.org/abs/2508.17536)
3. Wynn et al., degradation: "Through a series of experiments, we demonstrate that debate can lead to a decrease in accuracy over time - even in settings where stronger (i.e., more capable) models outnumber their weaker counterparts." [arXiv 2509.05396](https://arxiv.org/abs/2509.05396)
4. Wynn et al., flips: "Our analysis reveals that models frequently shift from correct to incorrect answers in response to peer reasoning, favoring agreement over challenging flawed reasoning." [arXiv 2509.05396](https://arxiv.org/abs/2509.05396)
5. Wynn et al., cause (v2 spelling): "...naive applications of debate may cause performance degradation when agents are neither incentivised nor adequately equipped to resist persuasive but incorrect reasoning." [arXiv 2509.05396](https://arxiv.org/abs/2509.05396)
6. Huang et al. (ICLR 2024), current v2: "In the context of reasoning, our research indicates that LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction." [arXiv 2310.01798](https://arxiv.org/abs/2310.01798)
7. Smit et al. (ICML 2024): "Importantly, we find that multi-agent debating systems, in their current form, do not reliably outperform other proposed prompting strategies, such as self-consistency and ensembling using multiple reasoning paths." [arXiv 2311.17371](https://arxiv.org/abs/2311.17371)
8. MAST, categories: "This process identifies 14 unique modes, clustered into 3 categories: (i) system design issues, (ii) inter-agent misalignment, and (iii) task verification." [arXiv 2503.13657](https://arxiv.org/abs/2503.13657)
9. MAST, trace count (v3 body): "To address this question and systematically understand MAS failures, we introduce MAST-Data, a comprehensive, high-quality collection of 1642 annotated execution traces." [arXiv 2503.13657v3 PDF](https://arxiv.org/pdf/2503.13657v3)
10. MAST, failure rates: "...analysis reveals 41% to 86.7% failure rate on 7 state-of-the-art (SOTA) open-source MAS..." [arXiv 2503.13657v3 PDF](https://arxiv.org/pdf/2503.13657v3)
11. MAST, ChatDev: "We demonstrate that a straightforward system workflow adjustment ensuring the CEO had the final say contributed to a +9.4% increase in overall task success rate." [arXiv 2503.13657v3 PDF](https://arxiv.org/pdf/2503.13657v3)
12. MAST site, shares: "The distribution of failures across MAST’s categories is relatively balanced (FC1: 41.77%, FC2: 36.94%, FC3: 21.30%, Figure 2)." [MAST site](https://sites.google.com/berkeley.edu/mast/home)
13. Du et al., plateau: "However, we found that additional debate rounds above four led to a similar final performance to 4 rounds of debate." [arXiv 2305.14325v1 PDF](https://arxiv.org/pdf/2305.14325v1)
14. Du et al., stubborn: "In general, we found that prompts that encouraged models to be more “stubborn’ based on their own solutions led to longer debates and better final solutions." [arXiv 2305.14325v1 PDF](https://arxiv.org/pdf/2305.14325v1)
15. Hu et al., fixed rounds: "Fixed-round debates risk either premature stopping before consensus is reached or unnecessary computation after convergence." [arXiv 2510.12697v1 PDF](https://arxiv.org/pdf/2510.12697v1)
16. Hu et al., stop rule: "After each round, if all agents agree, the process terminates and returns the consensus; otherwise, it continues until a maximum of T rounds, after which the majority vote is returned." [arXiv 2510.12697v1 PDF](https://arxiv.org/pdf/2510.12697v1)
17. Wang et al., agreement (v1): "...yet agreement among agents is not evidence of correctness." (v2 abstract: "Multi-agent debate improves LLM reasoning, yet agreement is not evidence of correctness.") [arXiv 2604.07667v1 PDF](https://arxiv.org/pdf/2604.07667v1); [arXiv 2604.07667](https://arxiv.org/abs/2604.07667)
18. Anthropic, checkpoints and stop rules: "Agents can then pause for human feedback at checkpoints or when encountering blockers. The task often terminates upon completion, but it’s also common to include stopping conditions (such as a maximum number of iterations) to maintain control." [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
19. Anthropic, ground truth: "During execution, it's crucial for the agents to gain “ground truth” from the environment at each step (such as tool call results or code execution) to assess its progress." [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
20. Anthropic, human control: "But humans should retain control over how their goals are pursued, particularly before high-stakes decisions are made." [Anthropic framework](https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents)
21. Claude Code Review, never approves: "A review never approves or blocks the pull request, so the decision to merge stays with your team." [code.claude.com code-review](https://code.claude.com/docs/en/code-review)
22. Claude Code Review, no execution: "**How it examines your code**: a review works from reading the diff and the surrounding code, without building or running your code." [code.claude.com code-review](https://code.claude.com/docs/en/code-review)
23. Claude Code Review, instructions: "Code Review reads `REVIEW.md` from the pull request's base branch or from the default branch, never from the pull request's own changes." [code-review-customize](https://code.claude.com/docs/en/code-review-customize.md)
24. Claude Code Review, limits: "A review with no findings doesn't mean your code is error-free or secure." [code.claude.com code-review](https://code.claude.com/docs/en/code-review)
25. Copilot approvals count: "When approvals are turned on, Copilot can approve the pull request, and that approval counts toward your repository’s required approvals." [GitHub changelog 2026-10-28](https://github.blog/changelog/2026-10-28-copilot-code-review-merge-with-confidence-with-max-and-approvals/)
26. Copilot approvals default: "Approvals are off by default. Admins can turn them on at the enterprise, organization, or repository level, and repository admins can choose which file paths Copilot is allowed to approve." Same URL.
27. Copilot approval dismissed: "If new commits are pushed after Copilot approves, the approval is dismissed, and you can request a new review to get a fresh approval." Same URL.
28. GitHub, human review: "You should always review and verify the feedback generated by Copilot code review, and supplement Copilot's feedback with careful human review to ensure your code meets your requirements." [GitHub responsible use](https://docs.github.com/en/copilot/responsible-use/code-review)
29. GitHub, repeat comments: "When re-reviewing, Copilot may repeat previous comments, even if you resolved or downvoted them." [GitHub use Copilot code review](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review)
30. Google, response time: "One business day is the maximum time it should take to respond to a code review request (i.e., first thing the next morning)." [Google, Speed of Code Reviews](https://google.github.io/eng-practices/review/reviewer/speed.html)
31. Google, approval standard: "In general, reviewers should favor approving a CL once it is in a state where it definitely improves the overall code health of the system being worked on, even if the CL isn’t perfect." [Google, The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)
32. Google, record the resolution: "(If you do this, though, make sure to record the results of the discussion as a comment on the CL, for future readers.)" Same URL.
33. Google, escalation: "If that doesn’t resolve the situation, the most common way to resolve it would be to escalate. Often the escalation path is to a broader team discussion, having a Technical Lead weigh in, asking for a decision from a maintainer of the code, or asking an Eng Manager to help out." Same URL.
34. Google, no stalling: "Don’t let a CL sit around because the author and the reviewer can’t come to an agreement." Same URL.
35. Google, evidence: "Technical facts and data overrule opinions and personal preferences." Same URL.
36. Google, small CLs: "With large changes, reviewers and authors tend to get frustrated by large volumes of detailed commentary shifting back and forth—sometimes to the point where important points get missed or dropped." [Google, Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
37. Pact, can-i-deploy: "It will give you a definitive answer if the version of your consumer that is being deployed, is compatible with all of its providers." [Pact, Writing Consumer tests](https://docs.pact.io/consumer)
38. Pact, loose tests: "Your Pact tests should be as loose as they possibly can be, while still ensuring that the provider can't make changes that will break compatibility with the consumer." Same URL.
39. oasdiff: "Exit code is 0 when there are no breaking changes, 1 when breaking changes are found." [oasdiff docs](https://oasdiff.com/docs)
40. Kleppmann, fencing token: "In this context, a fencing token is simply a number that increases (e.g. incremented by the lock service) every time a client acquires the lock." [martin.kleppmann.com](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)
41. Claude Code, Opus 4.8 fast mode (2.1.316): "Deprecated fast mode for Opus 4.8 as of October 30, 2026; it will be removed on November 30, 2026." [CHANGELOG.md](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)
42. Copilot default effort: "This change took effect September 28, 2026." [GitHub changelog 2026-10-02](https://github.blog/changelog/2026-10-02-copilot-code-review-api-support-and-new-default-effort-level)
43. eng-practices archive: "This repository was archived by the owner on Nov 21, 2025. It is now read-only." [github.com/google/eng-practices](https://github.com/google/eng-practices)

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R26 · FORM: research-result v1
Save as: R26-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R26: Agents reviewing each other's work (for `agent-engineering` → `review-loops`)

Bottom line: published evidence from 2023 to 2026 says a loop of agents critiquing each other does not, by itself, make the answer more correct. Review works when it rests on outside evidence (tests, execution, citations, a named commit), has a stopping rule fixed in advance, and has a person who owns every decision the agents cannot make. Of the five beliefs, two are confirmed, two need correction, and one is unsupported by any study.

Categories whose facts files this run touches: agent-engineering (review-loops), AI code review products, human code review practice, contract testing, distributed coordination.

## 1. Summary

- Debate between agents mostly adds nothing beyond voting. Choi, Zhu and Li (NeurIPS 2025) find "Majority Voting alone accounts for most of the performance gains typically attributed to MAD". They also prove debate is a martingale (each agent's expected belief in the right answer stays the same from round to round), so it "does not improve expected correctness".
- Debate can make answers worse. Wynn, Satija and Hadfield (2025) show accuracy can fall over rounds, by 12 points on MMLU in one mixed-model setting, because agents switch from right answers to wrong ones under persuasive but incorrect reasoning.
- Agreement is not verification. Without outside feedback, models "struggle to self-correct" (Huang et al., ICLR 2024). The MAST study (a taxonomy of how multi-agent systems fail) covers 1,642 annotated execution traces from 7 frameworks. It measured failure rates of 41% to 86.7% and names "task verification" as one of three failure categories.
- More rounds have diminishing or negative returns. Du et al. (2023) saw gains level off at about 4 rounds; Choi et al. saw average accuracy fall from 2 to 3 to 5 rounds on 7B–8B models.
- Stopping when agents stabilise or agree loses little. Adaptive stopping halted after 2–8 rounds instead of 10, at a cost of 0 to about 1 accuracy point (Hu et al., 2025).
- Anthropic's own agent guidance: agents "pause for human feedback at checkpoints or when encountering blockers" and use "stopping conditions (such as a maximum number of iterations)".\[1\]
- Claude Code's managed Code Review never approves or blocks a pull request: "the decision to merge stays with your team". It reads the code but does not build or run it.\[2\]
- Change since most guidance was written: GitHub made Copilot code review approvals generally available on 28 October 2026. Approvals are off by default; when an admin turns them on, a Copilot approval "counts toward your repository's required approvals".
- GitHub's own documentation still tells users to "supplement Copilot's feedback with careful human review".\[3\]
- Google's review guide carries over almost unchanged: respond within one business day, keep changes small, approve once a change "definitely improves the overall code health", and escalate disagreements to a person instead of letting a change sit.\[4\]\[5\]\[6\]\[7\]\[8\]
- For two codebases that depend on each other, a machine-checked contract beats messages. Pact's `can-i-deploy` gives "a definitive answer" on compatibility for each version, and `oasdiff breaking` fails CI on a breaking OpenAPI change.
- Turn-taking: naming whose turn is next is only safe if the shared record rejects a stale writer. Distributed systems use a fencing token, a number that rises with each grant and is checked where the write lands (Kleppmann, 2016).
- Current Claude Code is 2.1.321 (bundled in Claude Desktop on 9 November 2026). Opus 4.8 fast mode ends 30 November 2026 (secondary source).\[9\]\[10\]
- No published study tests this repository's protocol (numbered "laps", verdicts committed in advance, a close condition in the first message). Treat those rules as house practice, not evidence-based findings.
- None of the five beliefs carries the "(the standard, date)" mark, so this run neither confirms nor refutes any dated fact in PROJECT-BOOTSTRAP-AND-AUDIT v0.49.0.

## 2. Corrections

| # | What we believe | Verdict | The right fact | Source |
|---|---|---|---|---|
| B1 | Two sessions reviewing each other converge faster when the close condition is fixed in the first message and each side commits in advance to its next verdict. | Partly unsupported; reframe. | No study tests "laps" or verdicts committed in advance (not found). Adjacent evidence supports fixing the stop rule in advance: "Fixed-round debates risk either premature stopping before consensus is reached or unnecessary computation after convergence" (Hu et al., arXiv 2510.12697).\[11\] But faster convergence is the wrong goal. Convergence is where agents flip to agree with each other (Wynn et al., arXiv 2509.05396), and Du et al. found agents prompted to be more "stubborn" debated longer and reached better answers (arXiv 2305.14325). The rule should say: fix the close condition in advance, and close on evidence, not on agreement. | arXiv 2510.12697; arXiv 2509.05396; arXiv 2305.14325 |
| B2 | Rules about evidence pay for themselves; rules about choreography cost more than they catch. | Half right; the second half is wrong as stated. | Evidence rules are well supported: models do not self-correct without outside feedback (Huang et al.), and verification failures are a top-level MAST category.\[12\]\[13\] But MAST also measures choreography failures. Inter-agent misalignment is one of its three categories (36.94% in the project site's figures), and "step repetition" (15.7%) and "unaware of termination conditions" (12.4%) are among the most common failure modes (secondary summaries of MAST). Rules on who has the final say and when to stop address measured failures. In MAST's ChatDev case, making the CEO agent have the final say "contributed to a +9.4% increase in overall task success rate" (arXiv 2503.13657v3). Envelopes and digests are not measured either way. Keep turn and stop rules; drop choreography that no failure mode justifies. | arXiv 2503.13657; https://sites.google.com/berkeley.edu/mast/home; secondary: taskade.com, easital.com |
| B3 | Two writers can collide on one message number even with per-side numbering, unless the last message names whose turn is next. | Incomplete. | Naming whose turn is next works only if both sides read the latest state before writing. A paused writer can still act on a stale view, like a client whose lease expired. Distributed systems fix this at the store: "a fencing token is simply a number that increases (e.g. incremented by the lock service) every time a client acquires the lock", and the store rejects a lower token (Kleppmann). Fencing still cannot order two writers when the lower token arrives first (secondary: surfingcomplexity.blog, with Kleppmann's agreement). For agent sessions: give each side its own message namespace, or use a compare-and-set on the shared file, for example a git push that fails unless it builds on the latest commit. | https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html (copy read at pages.cs.wisc.edu); surfingcomplexity.blog |
| B4 | Agents can't supply time on hardware, a design both sides agree on, or acts only a person can do; no number of messages stands in for them. | Confirmed, with one update. | Claude Code Review works "without building or running your code". Anthropic says humans should retain control "particularly before high-stakes decisions are made". Update: since 28 October 2026 a platform can let an agent supply a formal approval, since Copilot approvals count toward required approvals once an admin enables them. That is a person's policy choice, not something agents earn by exchanging messages. | code.claude.com/docs/en/code-review; anthropic.com framework; github.blog changelog 2026-10-28 |
| B5 | An answer from one side isn't a settlement; a person's ruling is written down once, verbatim. | First half confirmed; second half not found as published practice. | Google says the first step is consensus, and if that fails "the most common way to resolve it would be to escalate" to a tech lead, maintainer or manager. It adds: "Don't let a CL sit around because the author and the reviewer can't come to an agreement." Writing the ruling once, verbatim, is sound house practice, but no source states it. A secondary summary of Google's guide says notes from a face-to-face resolution should go on the review. | google.github.io/eng-practices/review/reviewer/standard.html; secondary: dev.to/codingblocks |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| 1 | Original multiagent debate method | Multiple instances propose and debate over rounds | https://arxiv.org/abs/2305.14325 | "multiple language model instances propose and debate their individual responses and reasoning processes over multiple rounds to arrive at a common final answer"\[14\] | 2023-05-23 |
| 2 | Debate rounds plateau | About 4 rounds on arithmetic | https://arxiv.org/html/2305.14325v1 | "additional debate rounds above four led to a similar final performance to 4 rounds of debate"\[15\] | 2023-05-23 |
| 3 | Stubborn agents help | Longer debates, better answers | https://arxiv.org/html/2305.14325v1 | "prompts that encouraged models to be more \"stubborn' based on their own solutions led to longer debates and better final solutions"\[15\] | 2023-05-23 |
| 4 | Voting explains most debate gains | Majority voting ≈ debate | https://arxiv.org/abs/2508.17536 | "we find that Majority Voting alone accounts for most of the performance gains typically attributed to MAD"\[16\] | 2025-08-24 (v2 2025-10-23) |
| 5 | Debate is a martingale | No expected gain from debate alone | https://arxiv.org/abs/2508.17536 | "We prove that it induces a martingale over agents' belief trajectories, implying that debate alone does not improve expected correctness."\[16\] | 2025-08-24 |
| 6 | More rounds lowered accuracy (Qwen2.5-7B, 7 benchmarks) | 0.7377 (T=2), 0.7112 (T=3), 0.7050 (T=5); majority vote 0.7691\[17\] | https://arxiv.org/abs/2508.17536 (PDF v2, table) | not found as a single sentence; values read from the paper's table | 2025-10-23 |
| 7 | Debate can degrade accuracy | Yes, over rounds | https://arxiv.org/pdf/2509.05396 | "debate can lead to a decrease in accuracy over time — even in settings where stronger (i.e., more capable) models outnumber their weaker counterparts"\[18\] | 2025-10-13 (v2)\[19\] |
| 8 | Why debate fails | Persuasive wrong reasoning | https://arxiv.org/html/2509.05396v1 | "naive applications of debate may cause performance degradation when agents are neither incentivized nor adequately equipped to resist persuasive but incorrect reasoning"\[18\] | 2025-09\[20\] |
| 9 | Self-correction without outside feedback | Fails, sometimes worse | https://axi.lims.ac.uk/paper/2310.01798 (abstract of arXiv 2310.01798) | "LLMs struggle to self-correct their responses without external feedback, and at times, their performance might even degrade post self-correction"\[13\] | 2023-10-03 |
| 10 | Debate vs other prompting | Not reliably better | https://arxiv.org/abs/2311.17371 | "multi-agent debating systems, in their current form, do not reliably outperform other proposed prompting strategies, such as self-consistency and ensembling using multiple reasoning paths"\[21\] | 2023-11 (ICML 2024) |
| 11 | MAST dataset | 1,642 traces, 7 frameworks, 14 modes, 3 categories | https://arxiv.org/abs/2503.13657 | "This process identifies 14 unique modes, clustered into 3 categories: (i) system design issues, (ii) inter-agent misalignment, and (iii) task verification." | 2025-10-26 (v3) |
| 12 | MAST category shares (project site) | 41.77% / 36.94% / 21.30% | https://sites.google.com/berkeley.edu/mast/home | "(FC1: 41.77%, FC2: 36.94%, FC3: 21.30%"\[12\] | read 2026-11-10 |
| 13 | Fixed rounds are wasteful or premature | Use adaptive stopping | https://arxiv.org/pdf/2510.12697 | "Fixed-round debates risk either premature stopping before consensus is reached or unnecessary computation after convergence."\[11\] | 2025-10-14 |
| 14 | Agreement-based routing and stopping | Skip or stop debate on agreement | https://arxiv.org/html/2606.13197v1 | "Pre-debate Agreement Routing (PAR) decides whether independently generated Round-0 answers require debate; Early Agreement Stopping Evaluator (EASE) stops debate after convergence"\[22\] | 2026-06 (preprint) |
| 15 | Anthropic: human checkpoints and stop rules | Pause at checkpoints; cap iterations | https://www.anthropic.com/research/building-effective-agents | "Agents can then pause for human feedback at checkpoints or when encountering blockers. The task often terminates upon completion, but it's also common to include stopping conditions (such as a maximum number of iterations) to maintain control." | 2024-12-19\[1\] |
| 16 | Anthropic: ground truth each step | Environment feedback | https://www.anthropic.com/research/building-effective-agents | "During execution, it's crucial for the agents to gain “ground truth” from the environment at each step (such as tool call results or code execution) to assess its progress." | 2024-12-19\[1\] |
| 17 | Anthropic: human control before high-stakes decisions | Required | https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents | "But humans should retain control over how their goals are pursued, particularly before high-stakes decisions are made." | read 2026-11-10\[23\] |
| 18 | Claude Code Review never approves | Merge decision stays with people | https://code.claude.com/docs/en/code-review | "A review never approves or blocks the pull request, so the decision to merge stays with your team."\[2\] | read 2026-11-10 |
| 19 | Claude Code Review limits | May miss bugs | https://code.claude.com/docs/en/code-review | "A review with no findings doesn't mean your code is error-free or secure."\[2\] | read 2026-11-10 |
| 20 | Claude Code Review does not execute code | Reads only | https://code.claude.com/docs/en/code-review | "a review works from reading the diff and the surrounding code, without building or running your code"\[2\] | read 2026-11-10 |
| 21 | Claude Code Review instructions source | Base or default branch only | https://code.claude.com/docs/en/code-review | "`REVIEW.md` from the base or default branch and never from the pull request's own changes"\[2\] | read 2026-11-10 |
| 22 | Claude Code Review availability | Team and Enterprise; not with ZDR or HIPAA config | https://code.claude.com/docs/en/code-review | "Code Review isn't available to organizations with Zero Data Retention enabled or with the HIPAA configuration applied"\[2\] | read 2026-11-10 |
| 23 | Copilot approvals GA | 28 Oct 2026; count toward required approvals | https://github.blog/changelog/2026-10-28-copilot-code-review-merge-with-confidence-with-max-and-approvals/ | "When approvals are turned on, Copilot can approve the pull request, and that approval counts toward your repository's required approvals."\[24\] | 2026-10-28 |
| 24 | Copilot approvals default | Off; admins enable; file-path scope | same as 23 | "Approvals are off by default. Admins can turn them on at the enterprise, organization, or repository level, and repository admins can choose which file paths Copilot is allowed to approve."\[24\] | 2026-10-28 |
| 25 | Copilot approval dismissed on new commits | Yes | same as 23 | "If new commits are pushed after Copilot approves, the approval is dismissed, and you can request a new review to get a fresh approval."\[24\] | 2026-10-28 |
| 26 | Copilot Max effort level | Public preview; several agents across providers plus aggregator | same as 23 | "An aggregation agent then reconciles their findings, resolves disagreements, and double-checks accuracy before combining everything into a single review."\[24\] | 2026-10-28 |
| 27 | GitHub: human review still needed | Supplement with human review | https://docs.github.com/en/copilot/responsible-use/code-review | "You should always review and verify the feedback generated by Copilot code review, and supplement Copilot's feedback with careful human review to ensure your code meets your requirements."\[3\] | read 2026-11-10 |
| 28 | Copilot instructions are not always followed | Non-deterministic | https://docs.github.com/en/copilot/tutorials/customize-code-review | "Copilot may not follow every instruction perfectly every time."\[25\] | read 2026-11-10 |
| 29 | Google: review response time | One business day maximum | https://google.github.io/eng-practices/review/reviewer/speed.html (quoted via secondary cubic.dev) | "One business day is the maximum time it should take to respond to a code review request (i.e., first thing the next morning)."\[6\] | read 2026-11-10 |
| 30 | Google: speed means response time | Not total time | https://google.github.io/eng-practices/review/reviewer/speed.html | "it is the *response* time that we are concerned with, as opposed to how long it takes a CL to get through the whole review and be submitted"\[26\] | read 2026-11-10 |
| 31 | Google: approval standard | Better, not perfect | https://google.github.io/eng-practices/review/reviewer/standard.html | "In general, reviewers should favor approving a CL once it is in a state where it definitely improves the overall code health of the system being worked on, even if the CL isn't perfect."\[8\] | read 2026-11-10\[4\] |
| 32 | Google: disagreements | Consensus, then escalate | https://google.github.io/eng-practices/review/reviewer/standard.html (copy at ctxs.ai) | "Often the escalation path is to a broader team discussion, having a Technical Lead weigh in, asking for a decision from a maintainer of the code, or asking an Eng Manager to help out."\[27\] | read 2026-11-10 |
| 33 | Google: small changes reviewed better | More thorough | https://google.github.io/eng-practices/review/developer/small-cls.html | "With large changes, reviewers and authors tend to get frustrated by large volumes of detailed commentary shifting back and forth—sometimes to the point where important points get missed or dropped." | read 2026-11-10\[5\] |
| 34 | Google eng-practices repository archived | 21 Nov 2025 (secondary) | https://pasqualepillitteri.it/en/news/3317/google-code-review-guidelines-internal-principles-industry-standard | "Repository archived on November 21, 2025, documentation still available on the static site google.github.io/eng-practices/."\[28\] | read 2026-11-10 |
| 35 | Pact: purpose of contract tests | Shared understanding of requests and responses | https://docs.pact.io/consumer | "Contract testing is about making sure your consumer team and provider team have a shared understanding of what the requests and responses will be in each possible scenario."\[29\] | read 2026-11-10 |
| 36 | Pact: keep tests loose | As loose as possible | https://docs.pact.io/consumer | "Your Pact tests should be as loose as they possibly can be, while still ensuring that the provider can't make changes that will break compatibility with the consumer."\[29\] | read 2026-11-10 |
| 37 | Pact: can-i-deploy | Definitive compatibility answer | https://docs.pact.io/consumer | "It will give you a definitive answer if the version of your consumer that is being deployed, is compatible with all of its providers."\[29\] | read 2026-11-10 |
| 38 | oasdiff exit codes | 0 none, 1 breaking | https://oasdiff.com/docs | "Exit code is 0 when there are no breaking changes, 1 when breaking changes are found." | read 2026-11-10\[30\] |
| 39 | Fencing token | Increasing number per lock grant | https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2018/Papers/leases-redis-problem.pdf (copy of Kleppmann 2016) | "In this context, a fencing token is simply a number that increases (e.g. incremented by the lock service) every time a client acquires the lock." | 2016-02-08\[31\] |
| 40 | Current Claude Code | 2.1.321 | https://claude.com/docs/cowork/changelog | "Bundled Claude Code version: 2.1.321." | 2026-11-09\[9\] |
| 41 | Repository licence | Apache-2.0 (standard keeps CC0-1.0) | https://github.com/rmccann-hub/claude-code-skills/releases/tag/v0.1.0 | "The licence is now Apache-2.0, replacing the original CC0-1.0 file. The standard keeps its own CC0-1.0 dedication." | 2025-09-23\[32\] |

## 4. Findings

### Q1. Published practice on multi-agent review and debate

**When it helps.** Du et al. (arXiv 2305.14325, May 2023; ICML 2024) had three ChatGPT (gpt-3.5) agents debate for two rounds on arithmetic, GSM8K, chess, biographies and MMLU. Debate beat a single agent (arithmetic 81.8 vs 67.0; GSM8K 85.0 vs 77.0) and beat majority vote on those tasks. Gains rose with rounds and levelled off at about four. Agents told to hold their own answers more firmly debated longer and did better.

**When it adds nothing.** Choi, Zhu and Li (arXiv 2508.17536, NeurIPS 2025) split debate into its voting part and its talking part. They ran 5 agents on Qwen2.5-7B and Llama3.1-8B across seven benchmarks. Majority vote averaged 0.7691 and 0.7242 and beat every debate setting. Decentralised debate fell as rounds rose (from 0.7377 at 2 rounds to 0.7050 at 5 on Qwen). Their theory explains why: if agents update their beliefs in the standard Bayesian way, each agent's expected belief in the right answer stays the same from round to round, so talking only moves it around. Debate helped only when they biased updates toward correction. Smit et al. (arXiv 2311.17371, ICML 2024) reached the same verdict when comparing debate with self-consistency and ensembling. Huang et al. (arXiv 2310.01798, ICLR 2024) found the same for one model checking itself. They also reported that multi-agent debate did no better than self-consistency on GSM8K at equal cost.

**When it amplifies errors.** Wynn, Satija and Hadfield (arXiv 2509.05396, 2025) ran 3-agent debates with GPT-4o-mini, Llama-3.1-8B and Mistral-7B on CommonSenseQA, MMLU and GSM8K.\[20\] On CommonSenseQA, debate lowered accuracy in every configuration. The worst drop was 12 points on MMLU (one GPT plus two Mistral, from 40.0 to 28.0). More answers flipped from right to wrong than the reverse, and telling agents they were rewarded for correctness did not stop it.\[19\]\[33\] A weak agent dragged a strong one down even when the strong agents outnumbered it.

**System-level failures.** MAST (Cemri et al., arXiv 2503.13657, v3 October 2025) annotated 1,642 execution traces from 7 frameworks. It found 14 failure modes in three groups: system design, inter-agent misalignment and task verification. A secondary write-up notes that "the reviewer agent so many frameworks include was, in practice, often a rubber stamp" (arcusx.ai, secondary).\[34\]

**What this means for `review-loops`.** A second agent is worth having as an independent sampler and as a source of checkable objections, not as a vote that settles a question. Every verdict should rest on something outside both agents: a test result, a cited line, a commit. Have each side give its first answer before seeing the other's, which is what voting gets right. Treat a switch to the other side's view without new evidence as a warning sign.

### Q2. AI code review in practice

**Anthropic Claude Code Review** (managed service, Team and Enterprise plans):
- Several agents read the diff and surrounding code in parallel. Then "a verification step checks the candidate findings against the code and filters out false positives".
- Findings are ranked by severity and posted as inline comments. A check run named Claude Code Review lists them and never concludes as a failure.
- By default it looks for "bugs that would break production, not formatting preferences or missing test coverage".
- It reads `REVIEW.md` and `CLAUDE.md` from the base branch only, so a pull request cannot rewrite its own review rules.\[35\]
- It does not build or run code.
- It is not available with Zero Data Retention, the HIPAA configuration, or customer-managed keys.
- The local command `/code-review` (alias `/review`) runs on any plan. Posting its findings to a pull request needs Claude Code v2.1.227 or later.

**GitHub Copilot code review:**
- Each review includes an approval assessment.
- Since 28 October 2026, approvals are generally available. They are off by default. When turned on, a Copilot approval counts toward required approvals, is dismissed by new commits, and can be limited to listed file paths.
- A new "Max" effort level (public preview) runs several review agents on models from different providers and reconciles their findings with an aggregation agent.
- GitHub's responsible-use page still says to supplement Copilot with careful human review.\[3\]
- Documented failure modes:
  - it may miss problems in large or complex changes;
  - it may hallucinate;
  - it may not follow every custom instruction;
  - it ignores instructions to block merges;
  - it "may repeat the same comments again, even if they have been dismissed or downvoted" (GitHub's usage docs, as quoted by a secondary source).

**What a person must still decide.** Both vendors leave the merge decision to people by default. Claude Code Review cannot approve at all. Copilot can, but only after a person turns approvals on, so letting an AI satisfy branch protection is a governance choice that should be written down. Treat "AI approved" and "AI found nothing" as inputs, not as evidence that code is correct or secure. Anthropic says a review with no findings "doesn't mean your code is error-free or secure".

### Q3. Human code review that carries over

From Google's engineering practices (the static site is still live; the repository was archived on 21 November 2025, secondary):

- **Latency:** respond within one business day at most. What matters is response time, not total time to submit. A reviewer can approve while leaving minor comments unresolved, which saves a round.
- **Small changes:** they are reviewed more quickly and more thoroughly; in large changes, important points get "missed or dropped".
- **What to check:** design, functionality, complexity, tests, naming, comments, style and documentation. Send comments on major design problems "immediately", before reviewing the rest.
- **Standard:** approve once the change definitely improves code health, even if it isn't perfect.
- **Disagreements:** try for consensus based on the guide, then talk directly, then escalate to a tech lead, maintainer or manager. Never let a change sit.
- **Emergencies:** only a real emergency justifies speeding up the whole process; a manager's soft deadline is not one.

**Which parts apply when both sides are agents:**
- **Small changes and "better, not perfect"** apply fully, and matter more, since agents lose detail in long contexts just as people do.
- **The one-business-day rule** becomes a turn deadline on the loop's own clock. Agents answer in minutes, so latency is rarely the bottleneck; the scarce resource is the person's attention.
- **Escalation** applies with one change: the escalation target must be a person. Two agents with the same training can share the same blind spot, as the martingale and sycophancy results above show.
- **Evidence over opinion:** Google's "technical facts and data overrule opinions" maps directly onto an evidence rule for agent verdicts.\[36\]

### Q4. Protocols between two codebases that depend on each other

In Pact, the consumer writes down what it needs, the provider verifies against it, and a broker records which versions are compatible. Pact's guidance:
- assert only what would break the consumer, and keep tests "as loose as they possibly can be";
- gate every deploy with `can-i-deploy`, which gives "a definitive answer" on compatibility.

For OpenAPI interfaces, `oasdiff breaking base.yaml revision.yaml` exits with code 1 on a breaking change, so CI can fail on it.

**When a shared written contract beats messages.** When both sides change independently, a machine-checked contract in version control catches drift every time. Messages catch it only if someone remembers to ask. Messages remain the right channel for intent and design ("why do you need this field?"); the contract is the record of what was agreed. For two agent sessions that each own a repository, the practical rule is: put the interface in a file both CIs check, and use messages to propose changes to that file rather than restate it.

### Q5. Turn-taking and ownership

A lease or a turn token alone does not stop two writers: a paused holder can wake after its lease expired and write anyway. Kleppmann's fix is a fencing token, a number that increases with each grant. The writer sends it with every write, and the store rejects any token lower than the highest it has seen. A later analysis (secondary, with Kleppmann's agreement) shows fencing still cannot order two writers when the lower token arrives first. So the store must also refuse writes that do not build on the latest state.

For agent sessions:
1. Give each session sole write access to its own message namespace, so numbers cannot collide.
2. Where both must write to one file, use a compare-and-set, such as a git push that fails unless it builds on the latest commit.
3. Put the turn owner and the base commit in each message, and have the reader reject a message whose base is stale.

This run did not research Claude Code's own coordination features for agent teams (see section 9).

### Q6. Stopping rules (Standard)

The evidence points to three rules:
1. **Cap rounds low.** Gains level off by about 4 rounds (Du et al.) and can reverse after 2 (Choi et al.; Wynn et al.).
2. **Stop early on stability or agreement; it costs almost nothing.**
   - Hu et al. use this rule: "if all agents agree, the process terminates and returns the consensus; otherwise, it continues until a maximum of T rounds, after which the majority vote is returned". They detect stability with a Beta-Binomial mixture and a Kolmogorov–Smirnov test.
   - That stopped debates after 2–8 rounds instead of 10, losing between 0.00 and 1.03 accuracy points.
   - ARMOR-MAD (a 2026 preprint, not peer reviewed) skipped debate entirely on 89.5% of GSM8K problems where 2 of 3 agents agreed at the start.
3. **Escalate to a person** when the cap is hit without agreement, as both Anthropic's guidance and Google's conflict rule say.

Agreement alone is not enough to close a loop. Wang et al., "From Debate to Decision: Conformal Social Choice for Safe Multi-Agent Deliberation" (arXiv 2604.07667v1, 9 April 2026), warn that "agreement among agents is not evidence of correctness". Their act-or-escalate layer sends wrong consensus to a person, catching "81.9% of wrong-consensus cases… at α=0.05" (Claude Haiku, DeepSeek-R1 and Qwen-3 32B on 8 MMLU-Pro domains). Require evidence, not just agreement, before closing.

### Q7. Where agents must stop for a person (Standard)

- **Anthropic:** agents should pause at checkpoints or blockers, and humans should keep control "particularly before high-stakes decisions are made". Claude Code asks for approval before actions that modify code or systems.
- **Claude Code Review** leaves the merge to people.
- **Copilot approvals** require an admin to opt in.
- **Physical tests** are outside any code reviewer's reach; Claude Code Review does not even build or run the code.
- **In every source found,** releases, authority over scope, approvals and anything needing hardware are left to people by design.

### Q8. Records (Standard)

No standard for auditing agent review loops was found. Existing patterns:
- MAST's annotated execution traces, which keep each message and action;
- Claude Code Review's check run, which lists its findings;
- reasons for resolving Copilot comments (Addressed, Won't fix, Incorrect), added on 27 August 2026 per a secondary source;
- the Pact Broker's matrix of which version pairs have been verified.

A loop should keep:
- each message, with its author, turn number and the commit it judged;
- each verdict, with the evidence it cites;
- the close condition as first stated;
- every escalation and the person's ruling;
- the final state of the shared contract.

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| Claude Code | Agent CLI; `/code-review` locally | 2.1.321 | 2026-11-09 (bundled in Claude Desktop) | `claude update` | `CLAUDE.md` | https://claude.com/docs/cowork/changelog \[9\] |
| Claude Code Review | Managed PR review | service, no version | not applicable | Owner enables in Claude admin settings; `@claude review` on a PR\[2\] | `REVIEW.md`, `CLAUDE.md` (base branch) | https://code.claude.com/docs/en/code-review |
| Copilot code review | PR review and optional approval | service; approvals GA, Max in preview | 2026-10-28 | request Copilot as reviewer, or ruleset "Automatically request Copilot code review" | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md` | github.blog changelog 2026-10-28; docs.github.com |
| Pact + Pact Broker CLI | Consumer-driven contracts, deploy gate | not found | not found | `pact-broker can-i-deploy` | pact files (JSON) | https://docs.pact.io/consumer |
| oasdiff | OpenAPI breaking-change check | not found | not found | `oasdiff breaking base.yaml revision.yaml` | optional config file | https://oasdiff.com/docs \[30\] |

## 6. Changing in the next 12 months

- **Opus 4.8 fast mode** ends 30 November 2026; Claude Code 2.1.316 deprecated it (secondary: claude-world.com). Flag: within 12 months.
- **Copilot's Max effort level** has been in public preview since 28 October 2026 and is "subject to change". Its pricing and behaviour may change before general availability (expected date not found).
- **Copilot's "Default" effort** maps to Balanced from 28 September 2026 (secondary: dev.to/pwd9000).\[37\]
- **Google eng-practices:** the repository is archived. The static site remains but will not be updated (secondary).
- **Pact and oasdiff:** end-of-support dates not found.

## 7. Common mistakes

- **Treating agreement as correctness.** Two agents converging proves nothing. Without an outside signal, debate leaves the expected chance of a right answer unchanged (Choi et al.), and it can flip right answers to wrong ones (Wynn et al.).
- **Letting the model that wrote the answer review it.** Self-correction without outside feedback does not work and can make answers worse (Huang et al.).
- **Adding rounds to fix disagreement.** Gains stop at about 4 rounds and can reverse earlier.\[15\]
- **Mixing a weak model into a strong one's review.** The weak agent drags the strong one down (Wynn et al.).\[18\]\[20\]
- **Reading "no findings" as "safe".** Anthropic says it isn't.\[2\]
- **Turning on Copilot approvals without a written policy.** Without one, the same product family can author and approve a change (secondary: quasa.io).
- **Putting review rules in the pull request.** Claude Code Review reads its rules from the base branch only, so a PR that edits them does not change its own review.
- **Assistant-specific mistakes:**
  - Copilot repeats comments that were dismissed.
  - It may not follow every instruction.
  - It skips some files, such as `package.json` lockfiles and SVGs (secondary).
  - Claude Code Review does not execute code.
- **Turn tokens without a check at the store.** A stale session can then write over a newer one (Kleppmann).
- **Over-strict contract tests.** Asserting the provider's business rules raises false alarms (Pact).

## 8. Sources and licences

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| arXiv papers (2305.14325, 2508.17536, 2509.05396, 2310.01798, 2503.13657, 2510.12697, 2311.17371, 2606.13197) | per paper. 2503.13657 (MAST) is CC BY-NC-ND 4.0 per its arXiv abstract page, which allows quoting with attribution but no adaptation. The others were not checked individually this run; arXiv's default licence is non-exclusive distribution. | brief quotes | yes | no, unless the paper's own licence allows | authors, title, arXiv ID |
| Anthropic docs and blog (code.claude.com, anthropic.com) | not found | brief quotes | yes | not without checking terms | "Anthropic", page title, URL |
| GitHub Docs and GitHub changelog | not verified this run | brief quotes | yes | not verified | "GitHub", page title, URL, date |
| Google eng-practices | not verified this run | brief quotes | yes | not applicable | "Google Engineering Practices", URL |
| Pact docs | not found | brief quotes | yes | not verified | "Pact Docs", URL |
| oasdiff docs | not verified this run (several oasdiff repositories are Apache-2.0) | brief quotes | yes | check the repository's own licence first | "oasdiff", URL |
| Kleppmann blog (and the copy at wisc.edu) | not found | brief quotes | yes | not applicable | Martin Kleppmann, "How to do distributed locking", 2016 |
| Secondary sources (cubic.dev, dev.to, taskade.com, easital.com, surfingcomplexity.blog, claude-world.com, quasa.io, arcusx.ai, pasqualepillitteri.it) | not found | brief quotes only, labelled secondary | yes | no | site, title, URL |
| This repository | Apache-2.0; the standard is CC0-1.0 | yes | yes | yes | per its own NOTICE and licence\[32\] |

Where a licence is "not found" or "not verified", the safe default for an Apache-2.0 repository is short quotation with attribution, paraphrase in its own words, and no copying of code.

## 9. Not found, contested, not covered

**Not found**
- Any study of two agent sessions in two repositories exchanging numbered "laps", committing to a verdict in advance, or writing a ruling once, verbatim.
- Current versions and release dates of the Pact Broker CLI and oasdiff, and end-of-support dates for both.
- Licences of Anthropic docs, GitHub Docs, Google eng-practices, Pact docs and Kleppmann's blog (not verified in this run).
- A published standard for audit records of agent review loops.
- Any statement on the 28 October 2026 Copilot changelog that a person must still review. It offers only approvals that are off by default, limits by file path, and dismissal on new commits.

**Contested**
- **MAST category shares.** The project site gives 41.77% / 36.94% / 21.30%; secondary summaries of the v3 paper give about 44.2% / 32.3% / 23.5%. The difference likely comes from different paper versions; check the v3 PDF before quoting a figure.
- **Whether debate helps at all.** Du et al. (2023, gpt-3.5) found clear gains over single agents and majority vote. Choi et al. (2025, 7B–32B open models) found majority vote matches or beats debate. The two differ in model strength, task and baseline.
- **Whether human review must stay.** OpenAI's internal experiments (reported secondhand by smartscope.blog) say human PR review is not strictly required. GitHub's guidance says to supplement Copilot with careful human review.

**Not covered**
- Claude Code agent teams and subagent coordination (task claiming, file locking): the search budget ran out.
- Versioned interface specifications beyond OpenAPI (protobuf/buf breaking checks, AsyncAPI).
- Other AI reviewers (CodeRabbit, Graphite, Gemini Code Assist) in primary sources.
- The dated-facts section of the repository's PROJECT-BOOTSTRAP-AND-AUDIT v0.49.0 was not read.
  - This run's fetch tool refused the GitHub URL as outside its permitted list. That is a tool restriction, not evidence that anything is missing.
  - The repository is public, and its releases page was readable through search (latest seen: v0.1.25, 3 November 2026).
  - A search snippet of its GitHub "About" panel still showed CC0-1.0, although v0.1.0 moved the repository to Apache-2.0. Check the licence file directly.

## Sources

1. [Building effective AI agents \\ Anthropic](https://www.anthropic.com/research/building-effective-agents)
2. <https://code.claude.com/docs/en/code-review>
3. [code review](https://docs.github.com/en/copilot/responsible-use/code-review)
4. [The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)
5. [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
6. [Code review best practices for authors and reviewers](https://www.cubic.dev/blog/code-review-best-practices)
7. [The Standard of Code Review - Google Engineering Practices Documentation](https://xcd0.github.io/eng-practices-ja-mdbook/review/reviewer/standard.html)
8. [The Standard of Code Review: Striking a Balance Between Quality and Progress - Software Engineering Blog](https://batalin.dev/posts/code-review-quality-vs-progress/)
9. [Changelog - Claude.ai Documentation](https://claude.com/docs/cowork/changelog)
10. [Claude Code Changelog Archive](https://claude-world.com/changelog/)
11. <https://arxiv.org/pdf/2510.12697>
12. [MAST](https://sites.google.com/berkeley.edu/mast/home)
13. [Large Language Models Cannot Self-Correc...](https://axi.lims.ac.uk/paper/2310.01798)
14. [\[2305.14325\] Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325)
15. [Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/html/2305.14325v1)
16. [\[2508.17536\] Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?](https://arxiv.org/abs/2508.17536)
17. <https://arxiv.org/pdf/2508.17536v2>
18. <https://arxiv.org/pdf/2509.05396>
19. [(PDF) Talk Isn't Always Cheap: Understanding Failure Modes in Multi-Agent Debate](https://www.researchgate.net/publication/395354595_Talk_Isn't_Always_Cheap_Understanding_Failure_Modes_in_Multi-Agent_Debate)
20. [Talk Isn’t Always Cheap: Understanding Failure Modes in Multi-Agent Debate](https://arxiv.org/html/2509.05396v1)
21. [\[2311.17371\] Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs](https://arxiv.org/abs/2311.17371)
22. [ARMOR-MAD: Adaptive Routing for Heterogeneous Multi-Agent Debate in Large Language Model Reasoning](https://arxiv.org/html/2606.13197v1)
23. [Our framework for safe and trustworthy agents \\ Anthropic](https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents)
24. [Copilot code review: Merge with confidence with Max and approvals - GitHub Changelog](https://github.blog/changelog/2026-10-28-copilot-code-review-merge-with-confidence-with-max-and-approvals/)
25. [Using custom instructions to unlock the power of Copilot code review - GitHub Docs](https://docs.github.com/en/copilot/tutorials/customize-code-review)
26. [Speed of Code Reviews](https://google.github.io/eng-practices/review/reviewer/speed.html)
27. [How to do code review - ctxs.ai](https://ctxs.ai/weekly/the-standard-of-code-review-4vqfbn)
28. [Google Code Review Guidelines: The Internal Principles That Set the Industry Standard](https://pasqualepillitteri.it/en/news/3317/google-code-review-guidelines-internal-principles-industry-standard)
29. [Writing Consumer tests](https://docs.pact.io/consumer)
30. [CLI Quick Start](https://oasdiff.com/docs)
31. [10/11/2017 How to do distributed locking — Martin Kleppmann’s blog](https://pages.cs.wisc.edu/~remzi/Classes/739/Fall2018/Papers/leases-redis-problem.pdf)
32. [Release v0.1.0 · rmccann-hub/claude-code-skills · GitHub](https://github.com/rmccann-hub/claude-code-skills/releases/tag/v0.1.0)
33. [Talk Isn't Always Cheap: Understanding Failure Modes in Multi-Agent Debate](https://www.alphaxiv.org/abs/2509.05396)
34. [Why Multi-Agent AI Systems Fail: A Field Guide to the MAST Taxonomy — Arcus](https://arcusx.ai/blog/2026-09-07-multi-agent-failures.html)
35. [Claude Code Changelog (November 2026)](https://www.gradually.ai/en/changelogs/claude-code/)
36. [Google’s Engineering Practices](https://dev.to/codingblocks/google-s-engineering-practices-code-review-standards)
37. [Copilot Can Now Approve Pull Requests. Should It Count Toward Your Branch Protection? - DEV Community](https://dev.to/pwd9000/copilot-can-now-approve-pull-requests-should-it-count-toward-your-branch-protection-2b78)
