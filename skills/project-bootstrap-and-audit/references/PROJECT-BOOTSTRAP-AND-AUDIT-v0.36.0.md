---
name: project-bootstrap-and-audit
description: "Re-runnable configuration standard for one maintainer. One file, read in ranges rather than end to end, that proposes changes to itself at the approval gate. Chooses a language and a shape for something new, sets up the repository, retrofits an existing one, or audits configuration that already exists — against a two-axis stakes model and ten dimensions, then sequences what is left. Emits a fixed schema so two runs on the same repository produce comparable output. Folds in file governance, the release and deploy currency gate, secret handling, licensing, and cross-repository contracts. Stops at a hard approval gate before changing anything."
metadata:
  version: "0.36.0"
  updated: "2026-09-23"
  supersedes: "0.35.0"
  reading: "One file, read in ranges. Start at How to Read This File; take only the sections your job names."
  absorbs: "REPO-RECON.md, TEST-PROCEDURE.md, the standalone test procedure for this file — all deleted, their content is below"
  standards_repo: "<asked at Phase 0 — none is a valid answer>"
  license: "CC0-1.0"
---

# Project Bootstrap and Audit

**Licence: CC0 1.0 Universal.** Dedicated to the public domain — copy it, change it, sell it,
publish it, no attribution needed. If a jurisdiction does not permit dedication, treat it as a
licence to do all of the above unconditionally. No warranty of any kind.

---

# How to Read This File

<constraints>

**Do not read this file end to end.** It is a reference, not a document, and no job needs all of
it. Read this section, then only the ranges your job calls for. **A run that reads everything has
paid for attention it did not use and diluted the rules it did.**

**Line numbers below are generated and go stale the moment anything is edited. Build your own
index first** — one command, and it is authoritative where this table is only a hint:

```
grep -n '^# \|^## ' <this file>
```

Four of those matches — `# <project name>` twice, `# Decisions`, `# Test Verification
Checklist` — are **inside template code blocks, not sections.** The table below names every
real section; anything the grep shows that is not in it is template content.

**Then read by range**, not by scrolling: `sed -n '<start>,<end>p'`, or your tool's read with an
offset and a limit. Where a section turns out to continue past the range you took, take the next
range — do not guess at what was cut off.

</constraints>

## What to read, by job

**Always, first:** *How to Read This File*, *Scope*, *How to Read a Finding*, *Standing Rules*,
*Environment*, *Vocabularies* — all of which are under **Before You Start**, one H1, so the
heading index finds it in one match. **Everything else is on demand.**

| Job | Then read |
|---|---|
| **Survey** — look, change nothing | The Run, phases 0–5 |
| **Audit or retrofit** | The Run, all phases. The ten dimensions are inside phase 4 |
| **Set up something new** | The Run, plus *Choosing a Language and Runtime* and *Choosing the Shape*, plus *Starter File Contents* |
| **Write a missing config file** | *Starter File Contents* and *The Configuration File Map* |
| **Cut a release or a deploy** | *The Release and Deploy Currency Gate* |
| **Two repositories are involved, or more** | *Cross-Repository Contracts* — including the fleet case, and the copied-file trade |
| **Running on a tool that is not Claude Code** | *Any Agent, Any Tool*, then your job's row |
| **Test this standard** | *Validating a Change to This Standard*. Nothing else |
| **Plan what happens next** | The Run, phase 9 |

**Every job ends with the *Conformance Self-Check*.** It is short and it is the only part of this
file that asks the run to report on itself.

## What not to read during a run

| Section | Why |
|---|---|
| *Provenance* | The incident behind every rule. Read it when a rule looks arbitrary and you want to know what produced it — **never to be thorough** |
| *Validating a Change to This Standard* | For testing this file, not for running it |
| *Proposing a Change to This Standard* | Read it only when you have found this file wrong |

**If your tool gave you this whole file in context and you cannot read selectively, that is
fine** — the routing above still tells you which parts to attend to, and which to skip.

---

# Before You Start

**Everything in this section is read on every job, whatever the job is.** It is the shortest
part of the file that cannot be skipped: what this covers and does not, how to read a finding,
the rules that hold in every phase, what the environment decides rather than assumes, and the
closed set of words a report may use.

Run this to set up a repository, retrofit one, or check whether existing configuration
still matches reality. It is re-runnable by design. Running it twice on an unchanged
repository must produce the same statuses and the same schema.

**Two cadences, one file.** This standard runs at inception, before a release or deploy, and
when something feels stale. `TEST-VERIFICATION-CHECKLIST.md` runs per task, before claiming
work complete — it lives in the repository rather than beside this file, and **Starter File
Contents** specifies what goes in it.

**To run it:** attach this file to an agent session on a repository and say *"Run the attached
PROJECT-BOOTSTRAP-AND-AUDIT standard against this repository"* plus the job. It stops and waits
twice; nothing is written before you approve. **Sending Results Back** has the full prompt
and what to return.

**For something that does not exist yet**, attach it to an empty repository — or none — and say
what you want to build and who runs it. It will choose a language and a shape with you before
it writes anything.

**It runs on any agent tool**, not only the one whose paths it names. **Any Agent, Any Tool**
translates them, and every run closes with a **conformance self-check** so a run on an
unfamiliar model reports its own weak points rather than leaving you to find them.

## What this is for

Set up a new repository, or check an existing one against a baseline, **without a second
reviewer and without a platform team.** It replaces the judgement a colleague would apply at
inception and at release, with the reasoning written down so a later run can disagree with it.

**Goals.** Make inception decisions explicit, especially the irreversible ones. Make drift
findable rather than discovered. Keep configuration proportionate to what the project can
actually break. Leave a record that survives the session, so the next run starts from what was
decided rather than from scratch.

**Not a goal.** Judging whether the code is good. This reads configuration, structure and
process — never program logic, algorithms or correctness.

## Assumptions

These are beliefs the design rests on. Each could be wrong, and saying so is cheaper than
discovering it.

- **Instruction files are weak, and the evidence is specific about how.** A controlled study
  (Gloaguen et al., ETH Zurich / LogicStar, 2026, `arXiv:2602.11988`) tested four agents on 438
  tasks and found repository-level context files produced **no significant task-success gain
  while raising inference cost over 20% on average** — and that this held for developer-written
  files as much as generated ones. A follow-up (Lulla et al., 2026, `arXiv:2601.20404`)
  compared agents with and without an `AGENTS.md` on 124 pull requests in 10 repositories: the
  file went with **lower median runtime (28.64%) and fewer output tokens (16.58%)**, and task
  completion stayed comparable. One measures success and the other efficiency, so the two do
  not conflict. **What survives both results:** keep the context file short, hand-written, and
  limited to what a reader cannot discover from the codebase — tool commands being the one
  content type measurably used, by two orders of magnitude when the file names a non-standard
  tool, while repository overviews earned nothing. Two later measurements point the same way,
  the first only tentatively. First, **adherence to written instructions may decay within a
  session** — about 5.6% lower odds of compliance for each additional function generated
  (`arXiv:2605.10039`), an exploratory and non-monotonic finding in a study whose main result
  was that file size, position, structure and conflicts made no detectable difference — which
  is why this file uses hard gates and puts its self-check last, where any decay is worst,
  rather than trusting one instruction stated once. Second, **the same guidance file measurably
  helped one model while hurting another**, which is why every budget rule here says minimal
  rather than complete. Everything here treats written rules as guidance, and only deny rules,
  hooks and server-side checks as enforcement.
- **Accretion is the failure mode**, not absence. A solo project dies of configuration nobody
  maintains more often than of configuration nobody wrote. Hence `OVER` as a first-class finding.
- **Declines are worth recording** — a written "no" with a reopen trigger prevents the same
  question being re-litigated every run.
- **Stakes are two axes, not one.** Blast radius and audience diverge; an internal tool three
  people use can break a production floor.
- **The human decides.** Where a choice has a real trade, it goes to them with both
  consequences rather than being applied on the agent's judgement.

## Limitations

- **It enforces nothing by itself.** It is a document an agent reads. Everything real is a
  deny rule, a hook, or a server-side check that this can only propose.
- **No code review.** Structure, wiring and configuration only. Logic, correctness and
  performance are out of scope.
- **Tier is a heuristic.** Two axes and four levels is a rough instrument; it is meant to stop
  gross mismatch, not to be precise.
- **Budgets are unmeasured.** The line counts are working heuristics, stated as smells rather
  than thresholds, because no measurement supports a specific number.
- **Git and a hosted remote are assumed.** Nothing here covers other version control.
- **Named tools and platform capabilities go stale.** Every version number, price and plan
  limit in this file is dated in **Facts with an Expiry Date** and was true on that date
  only. A run that relies on one without checking it is reporting last year's platform.
- **Shapes not yet exercised** carry more risk: PowerShell, C#, C with meson, shell tools,
  and repositories with cross-repository contracts. The audit path has far more runs behind it
  than the scaffolding path.
- **It was built from one maintainer's estate, and it shows.** Every rule since 0.17.0 came
  from Python web applications and a C fork, all single-committer, all with tests, a build
  and a lockfile. **Adversarial probing found the shapes it handles badly**, and they share
  one property: the rule's premise about the repository is false. A proof-assistant
  repository with no test suite, a content-addressed build where pinning is meaningless, a
  documents or dataset repository with nothing to build, a monorepo with per-package
  versions, generative tests with no stable count. The premise rule above is the general
  answer; **it is not a substitute for knowing that this file has never been run on any of
  them.**
- **Three cases have no rule at all, and are named here rather than left to be discovered.**
  A fork whose upstream is dead or deleted — the contract rules assume a live provider. A
  prior decision record written by a *different* standard, which re-check mode will read as
  its own. And a repository that contains this file, where the audit and its subject are the
  same artifact. **Each produces no opinion rather than a wrong one**, which is why they are
  tolerable, and each is a gap someone will eventually hit.
- **The choosing part has no runs behind it at all.** Language and shape selection arrived in
  0.18.0 and has never been exercised on a real project. Treat its recommendations as a
  starting argument to disagree with, and report what it got wrong.
- **Planning is deliberately shallow.** Phase 9 sequences the work this run proposed and
  nothing else. It is not a substitute for project management and will look thin to anyone
  expecting one — that is the intent, not an omission.

## Versioning — loose guidance

`0.x` on purpose: **anything may change.**

**The version has one job: telling a reader whether two run reports are comparable.** Nothing
pins to a version range and no code depends on it, so the number promises that and nothing else.

| Bump | When |
|---|---|
| **Major** | The emission schema changed such that two reports no longer diff cleanly |
| **Minor** | New rules, new optional fields, anything leaving older reports readable |
| **Patch** | Wording, examples, a fix that changes no output |

**1.0.0 arrives when the schema stops changing** — that is the promise `1.x` makes, and until
then breaking changes are expected without ceremony.

**Do not bump per edit.** Batch changes and bump once. A fast-climbing number carries less
information, not more.

**The filename carries the version:** `PROJECT-BOOTSTRAP-AND-AUDIT-v<version>.md`, so copies
of different versions coexist and an attached file identifies itself before anything reads it.
**The frontmatter stays authoritative** — where the two disagree, `metadata.version` wins and
**the mismatch is itself a finding**, meaning a copy was renamed without being edited or the
reverse. Phase 8 records the frontmatter value. Prompts name the standard, not the file.

## Start here — read only what the job needs

This file covers five jobs. **Find yours, read those sections, skip the rest.** Reading a
section that does not apply costs context and dilutes attention on the ones that do.

| You were asked to | Read | Skip |
|---|---|---|
| **Survey** a repository — look, change nothing | Phases 0–5, then stop and report | Phases 6–9, release gate, validation |
| **Set up** a new repository | Phases 0–9, **all of Part II**, starter file contents, the ten dimensions, file governance | Release gate, validation |
| **Retrofit or audit** a repository | Phases 0–9, the ten dimensions, file governance | Release gate, validation, Part II (unless a choice is a finding) |
| **Choose a language** for something new | Choosing a language and runtime, then choosing the shape | Everything else, until a repository exists |
| **Write a missing config file** | Starter file contents, the configuration file map | Everything else |
| **Plan what happens next** | Phase 9 | Everything else, if the audit is already done |
| **Release or deploy** | Release and deploy gate, plus version reconciliation in dimension 10 | Phases 1–9 |
| **Prune files** | File governance | Everything else |
| **Validate a change to this standard** | Validating a change | Everything else |
| **Run it on a tool that is not Claude Code** | *Any Agent, Any Tool* — then your job's row above | Nothing extra |
| **Contribute a run to whoever maintains this** | *Sending Results Back* | Nothing extra |

**Every job ends with the conformance self-check.** It is short, it sits at the end, and it
is the only thing in this file that asks the run to report on itself.

**Testing the standard rather than a repository?** Read *Validating a Change to This Standard* and nothing else —
it carries the whole procedure: corpus, order, prompts, what to record, and how to triage a
failure. Its mechanical checks need no repository at all.

**This is one file, read in ranges.** *How to Read This File*, at the top, says which
sections each job needs and which to skip. Where a run finds this standard itself wrong,
*Proposing a Change to This Standard* says how that reaches the gate.

***Provenance* carries the version history and the incident behind every rule. It is never
read during a run** — only when a rule looks arbitrary and you want to know what produced it. It is the record of why rules exist, for
whoever maintains this file. Skip it unless you are changing the standard.
Within a run, skip further:

- ***The Release Gate*, *Cross-Repository Contracts*, *Standards Distribution*** — only when
  cutting a release or a deploy, where this repository provides to
  or consumes from another, or when proposing how a standard reaches many repositories. Most
  runs need none of the three.
- **A dimension that is `N/A` at this tier** — record it and move on. Do not argue it.

**Survey mode is the whole of the old reconnaissance pass.** Phases 0–5 are read-only and
produce more than a separate survey tool did. If you were asked only to look, run them, emit
their blocks, and stop before Phase 6.

**Whatever the job, it ends with one file.** Survey ends with phases 0–5 in it; a run stopped
at the gate ends with 0–6 and the decisions to answer; a full run ends with 0–9. Same name,
same shape, one attachment.

## Scope

This covers **the repository**: how it is set up, configured, gated, reviewed, documented and
released. It does not cover how the work is run.

**In scope.** Bootstrap and setup files, agent configuration, enforcement and CI, review and
merge discipline, secrets handling, dependencies, licensing, packaging, versioning,
documentation currency, file governance, cross-repository contracts.

**Also in scope, and narrowly:** sequencing and milestones **for the repository's own
configuration work** — the order the amendments land in, what constitutes done, and where
that record lives. Phase 9 covers it. This is a deliberate reversal of the earlier position
that all planning was out of scope, made because a run that produces sixteen amendments and
no order of operations has handed over a pile, not a plan.

**Out of scope.** What the business should depend on, what is worth building, which features
come first, staffing, process. The line: **this file may sequence work it proposed; it may
never sequence the product.** Where a finding needs one of those as an input — who depends
on this, does it touch production — **it is asked, never assumed**, and the answer is recorded
as given rather than argued with.

## How to read a finding

**A status describes the repository. It does not issue an instruction.**

Every recommendation carries what happens if it is taken **and what happens if it is not**.
Declining is a first-class answer, recorded with a reopen trigger and honoured until that
trigger fires. Nothing here is mandatory. **An audit that reads as a list of orders has been
written wrong.**

Where the baseline has a strong opinion it says so and gives the reason. Where practice is
genuinely split it gives both options and the trade, and asks. The ranking exists so the
consequences can be sorted, not so anything can be demanded.

<constraints>

**Standing rules. These hold in every phase.**

**The gates — what stops a run.**

- **Stop at Phase 6.** Nothing is written to the repository before explicit human
  approval. Reporting is not permission.
<!-- WHY exactly two waits: adherence decays measurably within a session, so gates counter
     drift — but each extra wait costs a round trip and invites the human to answer what the
     file could answer itself. Two is the floor, not a default to extend. -->
- **Phases 0–5 run in one pass**, each emitting its schema block before the next begins.
  **There are exactly two waits: Phase 3 and Phase 6.** Do not invent others.
- **Every run produces exactly one file.** Written outside the repository, named
  `RUN-REPORT-<repo>-<YYYY-MM-DD>.md`, containing everything the run produced — decisions to
  answer first, then every emission block. **The human must never have to assemble a report
  by copying pieces out of the conversation.** Emission blocks still appear in the reply as
  the run proceeds; the file is the durable copy and the only thing that has to travel.
- **Emit the schema, and only its fields.** Every phase has a required field set and every
  phase has `notes` for anything the fields cannot hold. Fill every field. **Do not add
  fields.**
**Evidence — what counts as knowing something.**

- **Evidence, not assertion.** Any field whose name ends `_proof` carries literal command
  output. Never a summary, never a paraphrase, never "verified".
- **An absolute negative is inverted by a single counterexample, and it is the claim shape a
  reader is least likely to doubt.** *There is no X anywhere in Y* reads as thoroughness
  while resting on one command having been run once, over a tree that may since have
  changed — including by this run's own amendments. **State what you searched, with what
  command, and when.** Prefer *this search found none* over *there are none*: the first is a
  result and can be re-run, the second is a claim about the world. Where an absolute negative
  is load-bearing — it makes a question unanswerable, or it justifies a decision — **re-run
  it immediately before writing it down.**
- **Never read an exit status through a pipe.** `pytest … | tail -25` reports **tail's**
  status, not pytest's, and tail succeeds at truncating failed output. A live run recorded
  `exit 0` that way; unpiped it was `exit 1` with four collection errors, and that run's
  largest finding would have been lost. **This voids every other evidence rule on this
  list**, because the output looks literal and the status is fabricated by the pipeline.
  Run the command unpiped and truncate afterwards, or use `set -o pipefail`, or read
  `${PIPESTATUS[0]}`. **The tell is output that was shortened for readability** — `tail`,
  `head`, `grep`, `less`, `| jq`. Where a `_proof` field holds trimmed output, the status
  beside it was taken unpiped or the field says how it was obtained.
- **Local green is not remote green.** A locally passing gate says nothing about the
  repository's actual CI conclusion. Where a remote exists, read it.
- **Enabling a feature is not the same as satisfying what it needs, and the gap is silent.** A
  configuration option whose precondition is unmet does not fail — it does nothing, reports
  nothing, and reads as coverage. The preconditions are the usual ones: a permission the token
  was not granted, a credential never set, a platform feature switched off at the repository, a
  plan tier the account does not hold. **A feature that cannot run has nothing to report, which
  is why this never surfaces on its own.** A live review caught a dependency tool configured to
  bypass its own schedule for security advisories, against a token scoped without the permission
  that reads them — the block was deliberate, correct in intent, and inert. **So read each
  enabled option against what it requires, and say which preconditions you verified and which
  you could not.** Where a precondition cannot be satisfied, the honest fix is removing the
  option, not leaving it as decoration.
- **Read a new configuration against its preconditions before it ships, not after.** The same
  defect in an older workflow had been green for a year before anyone read the log. **The cost of
  this check falls entirely on when you run it**, and a configuration not yet landed is the
  cheapest moment there will ever be.
- **A step configured not to fail reports success unconditionally, so its conclusion is not
  evidence at any depth.** `continue-on-error`, `|| true`, and a step's own
  fail-if-error switch set false each convert a gate into a log line, silently, with no
  signal at the level anyone checks. A live run found a coverage upload green at the rollup,
  green at the job, **green at the step** — while its log read `Token length: 0` and
  `Upload ... failed`. It had never once uploaded anything, across every run in its history,
  and the documentation described it as a live capability of the pipeline. **Read the `on:`
  and the suppression switches together at Phase 2**: for any step that cannot fail, read
  its output or record it as unrun. Never count it as a gate.
- **Read it at job and log level, not from the rollup — and read the skip list.** At run
  level **a job or a test that silently did not run looks exactly like one that passed**, and
  a green tick is the sum of both. A skipped test is not a passing test; a conditional job
  whose condition went false reports nothing and subtracts nothing from the conclusion. This
  matters most for the gates an amendment just changed, which is precisely when the rollup is
  least informative: a live run read a green conclusion at job and log level and confirmed
  three things the tick could not have told it — that the downloaded scanner really was
  checksum-verified before execution, that a newly added guard ran rather than skipping, and
  that a widened gate reached all three workflows. **Name the skip count and what skipped**,
  and where an amendment touched a gate, quote the log line proving it fired.
- **And check the workflow will run on the branch before you promise to read it.** A
  workflow triggering only on the default branch and on pull requests produces **nothing** on
  a feature branch — not a pending run, an absent one. A live apply pushed five commits and
  found zero workflow runs, so every gate on that work stayed local-only, with no way to
  discharge the rule above. **Read the `on:` block at Phase 2 and say so at the gate**, where
  the human is deciding whether to approve, rather than in the completion report where the
  answer is already fixed. Absent is recorded as absent; **calling it pending is a false
  statement about a run that will never arrive.**
**Honesty — what you may not do to make a report look better.**

- **Never invent a value.** Unknown is `unknown`. Absent is `none`. Never leave blank.
- **Never invent a status.** The vocabularies are closed. If nothing fits, use `secondary`,
  `strength` or `notes` — never coin a new term.
- **Never fill a placeholder with a real credential, and never ask the human for one.**
- **Never delete a file, a test, or a rule to make a check pass.** The remedies for a
  scanner or gate finding are: fix the real problem, narrow the check, or record an
  exemption. Removing the thing that failed is the forbidden resolution.
- **Record every override** — what you saw, what you did, why.
- **Correct, never silently edit.** A wrong claim gets a dated correction pointing at what it
  replaces. A pushed commit message cannot be amended, so the correction lives in the record.
- **Verify a stated problem before acting on it.** A premise in the prompt — "CI is
  failing", "this dependency is broken" — is a report, not a finding. Reproduce it, or read
  the current state. **It may already be fixed**, and proposing a repair for something
  already repaired wastes a run and adds churn to a repository that did not need it. Say what
  you found either way.
**Posture — how a finding is raised.**

- **Do not fix while inventorying.** Findings are Phase 4; fixes are Phase 7, after approval.
- **Two surfaces answering one question must be shown to agree, and only one may route.**
  Where a check, a router, a config value or a claim exists in two places, **they are one
  surface with one implementation, or they are a defect waiting for the day they disagree.**
  Observed three times in one project: a log sniffer reading only the first line while the
  parser it guarded found the marker anywhere — so a valid file routed to the wrong parser
  and returned **zero records from a fourteen-record input, silently**; an update offer and
  an approval check keyed differently, so the tool would have installed a build its own
  reports called unapproved; and two call sites spelling one output path. **Where merging is
  impossible, name both, say which one routes, and have the test assert the relation between
  them** so neither can drift alone.
- **Check a dimension's premise before rating it, and name the premise you checked.** Every
  dimension assumes something about the repository: that tests exist and are countable, that
  dependencies are pinned by version, that there is one version, that there is source at all.
  **Those assumptions are usually true and are not always true**, and where one is false the
  rule does not become lenient — **it becomes wrong, confidently.** A repository whose
  correctness argument is a machine-checked proof rather than a test suite is not missing
  tests. A build whose dependencies are content-addressed is not unpinned; it is pinned more
  strongly than a lockfile manages. A repository of documents, data or infrastructure has no
  build to gate. A monorepo with independent per-package versions has nothing to reconcile
  against a single tag. **Record `N/A` with the false premise named as the reason** — the
  same discipline as marking a fact `UNVERIFIABLE-HERE` rather than guessing at it. **A `GAP`
  raised against a premise that does not hold is the worst output this file can produce**,
  because it is specific, confident, and asks the human to break something that was right.
- **The deployment is a premise, and the most expensive one to get wrong.** Every dimension
  that rates exposure, reachability or blast radius assumes the audit knows where the software
  runs. **That knowledge comes from Phase 3's sixth question, never from a runbook**, and a
  finding built on a deployment the human has not confirmed is `UNVERIFIABLE-HERE` rather than
  rated.
- **Unfamiliar is not wrong.** These ten dimensions encode practice that is known to work;
  they do not encode everything that works. **An approach, tool, algorithm or layout you do
  not recognise is not evidence of a defect**, and the absence of a rule covering it is a
  fact about this file rather than about the repository. Where something is unusual and you
  cannot establish that it is wrong, **say that it is unusual and unverified, rate on what
  you could establish, and put the question to the human** — who may well have chosen it
  deliberately and be the only person who knows why. Rating a defect from unfamiliarity alone
  is how a standard degrades a repository towards its author's habits.
- **Where a repository's own recorded convention contradicts this file, the repository wins
  inside it — and the conflict is recorded, never silently resolved.** This file is guidance
  a maintainer chose to run; it is not authority over a decision they already made and wrote
  down. **A convention with its reasoning in the decision record outranks a rule here**, and
  the amendment is to record the divergence so no future run re-raises it. A convention with
  no reasoning anywhere is a different thing and may be raised normally. **Where the conflict
  is genuine and unrecorded, raise it as a question rather than an amendment** — the run does
  not get to settle which of two standards the repository follows.
- **An identifier that answers half a question while appearing to answer all of it is worse
  than one that answers none**, because it stops the reader asking. **And the name a human
  actually sees is part of the interface** — metadata inside a file does not help someone
  looking at a directory listing. A live protocol stamped artefacts with their sender and
  nothing else, which read as complete while leaving the recipient unstated; the fix put both
  in the envelope **and in the filename**, because a file manager shows the filename. Where
  an artefact moves between parties, its name places it in both directions.
- **Report over-configuration as loudly as under-configuration.** `OVER` is a real finding,
  **and it applies to enforcement this file itself installed.**

</constraints>

## Environment — detected, not assumed

<constraints>

**None of this is universal. Detect it, or ask.** The table below is what the standard was
built against; another maintainer, tool or plan will differ, and **a constraint assumed wrong
produces advice that cannot be followed.** Phase 0 establishes the real answers and records
them. Where a capability cannot be determined, it is `unknown` and becomes a human question —
never a guess.

</constraints>

| Fact | How it is established | If it holds |
|---|---|---|
| **Ephemerality** — only the repository is present | Assume true unless the tool says otherwise | Anything uncommitted does not exist |
| **Shell available** | Try one harmless command | **Without it, Phase 2 cannot execute documented commands.** Record them unrun; everything becomes `UNVERIFIABLE-HERE` and the run says so in its headline |
| **Writes outside the repository** | Try writing to a scratch path | **Without it, greenfield cannot build-then-copy and the run report has nowhere to live.** Emit the report in the reply and say why |
| **Remote CI readable** | Try reading a conclusion | Without it, "local green is not remote green" cannot be discharged. Record `unverifiable` |
| **Tag creation** | Try, or read the tool list | Where refused, tagging is a human action via the host UI or a dispatch job — **never "tag locally"** |
| **Local working copy exists** | **Ask. It cannot be detected** | Without one: no local tagging, no desktop tooling, and **client-side hooks gate nothing**, because every commit comes from an ephemeral container |
| **Enforced layer** | See *Any Agent, Any Tool* | Where the tool has none, dimension 6 is `N/A`, never `GAP`, and the guarantee moves server-side |
| **Branch protection available** | Read the plan, or ask | Unavailable on private repositories on free plans — **and rulesets carry the same gating**, so the newer mechanism is not an escape. Where unavailable, `N/A` with the reason — never a `GAP` re-proposed every run |
| **Third-party repositories readable** | Try one | Often scoped to the maintainer's own. An upstream fix status is then `unverifiable`, **never "no fix coming"** |
| **Clock agreement** | Compare `date -u` with `git log` | They can differ by days. Record both; anything written takes the session date |

## Vocabularies

**Closed sets, with precedence, and both are counted.**

### Agent-layer terms

The body uses these names; *Any Agent, Any Tool* maps each to a filename per tool. Shell
blocks below name Claude Code paths because a command must be concrete — substitute your
tool's and record the substitution.

| Term | What it is |
|---|---|
| **context file** | The canonical, portable project context. `AGENTS.md` |
| **tool shim** | A per-tool file that imports the context file and holds only what cannot be portable |
| **scoped rules** | Rules loaded per file or per path rather than every session |
| **enforced layer** | Permission configuration the tool obeys mechanically. **Not available on every tool** |
| **tool-server config** | Committed external-tool configuration, where the tool supports it |

### Dimension status

Exactly one `status` per dimension, plus any `secondary` entries and an optional `strength`.

<!-- WHY OVER is first-class: a solo project fails from configuration nobody maintains far
     more often than from configuration nobody wrote. Removing OVER makes this a ratchet that
     only ever adds. It applies to rules this file installed, too. -->
| Precedence | Status | Meaning |
|---|---|---|
| 1 | `BLOCKER` | A live exposure, or a check reporting success while measuring nothing. Ranked first for what it risks — the ranking is information, never an order |
| 2 | `DRIFT` | Configured, but no longer matches reality. Actively misleading |
| 3 | `GAP` | Missing something this tier warrants |
| 4 | `OVER` | Heavier than this tier warrants |
| 5 | `MIRROR` | Source of truth is outside the repository; unverifiable by design |
| 6 | `UNVERIFIABLE-HERE` | Cannot be established from this environment |
| 7 | `OK` | Present, correct, proven by output |
| 8 | `N/A` | Does not apply — by tier, by plan, **or because the rule's premise is false for this repository** |

<!-- WHY the closure rule: two early runs emitted 12 and 11 statuses for 10 dimensions, one
     by inventing `OK-with-gap` for a dimension that was partly fine. A count that need not
     balance hides both. Do not relax this to "roughly one per dimension". -->
**Closure rule.** Phase 4 emits exactly ten primary statuses, numbered 1–10. **If the tally
does not sum to ten, the phase failed — recount.** Secondaries and strengths are never counted.

<!-- WHY strength exists: precedence carries only the worst finding, so a repository with an
     excellent suite and one missing file reported as ten bare GAPs, and the run had to write
     a paragraph arguing against its own table. This field replaces that paragraph. -->
**`strength` is required wherever a dimension is materially better than its status implies.**
Precedence carries only the worst finding; without `strength` a report misrepresents the
repository and forces prose apologia the schema exists to remove.

### Command result

| Result | Meaning |
|---|---|
| `PASS` | Ran, exit 0 |
| `FAIL` | Ran, non-zero exit |
| `UNVERIFIABLE-HERE` | **Cannot** run here — no network, no daemon, needs a credential, wrong host OS, or a side effect outside the container |
| `NOT-RUN-HERE` | **Could** run, but was time-boxed out |

### Amendment severity

`recommended` or `optional`. **Nothing else.** Severity records how strongly the baseline
argues for something — it is never an instruction, and it is not a dimension status. An
amendment on a `BLOCKER` dimension is `recommended`; it does not have severity `BLOCKER`.

**Every amendment carries `if_accepted` and `if_declined`.** A recommendation without the
consequence of refusing it is an order wearing a suggestion's clothes.

<constraints>

**The setup carve-out.** Installing the **project's own declared dependencies** into the
ephemeral container — `pip install -e ".[test,dev]"`, `npm ci`, `meson setup build` — is
**setup, not a side effect.** Record it in `setup`. **Do not count it in `command_tally`.**
A dependency environment that already existed at session start goes in
`environment_preexisting`, not `setup` — the distinction is material to reproducibility.

Still `UNVERIFIABLE-HERE`: hand-patching an installed package, installing anything the
project does not declare, or writing outside the container.

</constraints>

## Facts with an Expiry Date

<constraints>

**Every fact below was true on the date beside it and is not self-renewing.** A standard that
names versions, prices and plan limits starts rotting the day it is written, and the failure is
not that a number is stale — it is that **advice built on a stale number cannot be followed**,
which reads to the human as the standard being wrong about everything.

**The rule: check it, or mark it.** Where a fact matters to a finding, verify it in this run and
say how. Where it cannot be verified from this environment, the finding built on it is
`UNVERIFIABLE-HERE` and the report says which fact it was waiting on. **Never report a plan
limit, a price or a tool capability from this table as though it were observed.**

**Nothing here is a dependency.** If the whole table were deleted the standard still runs; the
phases, dimensions and vocabularies name no version. It exists so a wrong number is findable
in one place rather than scattered through ten dimensions.
**A probe is only as good as its source, and this has already cost a real finding.** Checking
beats assuming — but a package index inside a sandbox, a mirror, a cache or a proxy can be
months behind and will answer with total confidence. On the first live audit run, the session
queried its own index, read Python 3.14 as a release candidate with 3.13 as newest stable,
and **withdrew a correct finding on that basis** — 3.14 had been stable for close to a year.
The index was roughly twelve months stale. Nothing in the report was fabricated; the evidence
was real and the source was wrong, which is the harder failure to see because the withdrawal
reads as diligence.

**So a probe that contradicts this table is checked before it is believed:**

- **Date the answer, not just the version.** An index that gives a version without a release
  date has told you what it holds, not what exists. Where the probe cannot produce a date,
  it has not verified anything.
- **Ask whether the source is in a position to know.** This is the crux, and it is a stronger
  test than comparing answers. **A pinned tool's bundled index is frozen at that tool's own
  release date and can never be current by construction** — it will answer instantly,
  authoritatively, and be arbitrarily old. That is precisely what happened: a pinned resolver
  was asked what Python exists, and it reported what its bundled download index shipped with,
  thirteen months earlier. The same holds for a container image's package lists, a vendored
  catalogue, an offline mirror, and any resolver's view of what it can install, which is a
  statement about reachability rather than about existence.
- **Sanity-check against upstream.** A vendor's own release history is the source of truth for
  its versions. Where the environment cannot reach upstream, **say so and mark the finding
  `UNVERIFIABLE-HERE`** — that is the status's whole purpose.
- **Corroborate from inside the repository where you can.** The strongest evidence in that run
  came from neither API: wheels for the newer interpreter were already sitting in the
  committed lockfile, which proved the dependency graph had moved while the gate had not. **A
  lockfile, a manifest or a vendored artefact is a dated fact the repository is carrying
  already**, and it needs no network at all.
- **A stale source is itself a finding.** A build environment resolving a year-old index is a
  dimension 2 concern in its own right and gets recorded, not silently worked around.
- **Withdrawing a finding needs the same evidence as raising one.** A withdrawal removes a
  real problem from the report and nobody audits an absence. **Where a probe cancels a finding
  this table would have produced, the report says which source answered and as of when.**

</constraints>

### Platform capability

| Fact | As of | Why a run cares |
|---|---|---|
| Classic branch protection **and** rulesets: public repositories on a free plan, or public and private on a paid one — **GitHub Pro suffices for a personal account**. Push rulesets need an organisation plan and apply only to private and internal repositories | 2026-09 | Dimension 6. Decides `GAP` against `N/A`, and whether the public-or-pay decision is raised at all |
| Secret scanning and push protection: free and default-on for public repositories; a paid per-committer add-on for private | 2026-09 | Dimension 7. Decides whether the free remedy exists |
| Immutable releases are a **repository or organisation setting**, not a default. When on: tag and assets frozen at publish, title and notes still editable, and assets must be uploaded while the release is a draft | 2026-09 | The release gate. Read the setting; do not assume either way |
| Dependency-update pull requests wait three days after a release by default, with no configuration; security updates are exempt. The period is set with `default-days` under `cooldown:`, with per-semver keys alongside; a bare `cooldown: 0` is not a documented form | 2026-09 | Dimension 8. A config matching the default is `OVER`; a longer one is not |
| A tag can be created in the browser at publish time, with no clone | 2026-09 | The only reason the release gate is reachable at all without a working copy |

### Agent tooling

| Fact | As of | Why a run cares |
|---|---|---|
| Claude Code reads `AGENTS.md` natively from v2.1.277, **but only when no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists** in the working directory or above it, and not in sessions without feature flags (Bedrock, other third-party providers, telemetry off), in the first session after an install or upgrade, or with the built-in `agents-md` plugin disabled. Keeping `@AGENTS.md` in `CLAUDE.md` works in all of them and "never makes Claude read `AGENTS.md` twice" | 2026-09 | Dimension 4 and *Any Agent, Any Tool*. Why the shim stays although native reading shipped |
| `AGENTS.md` is read directly by most other major agent tools; Gemini CLI and Aider need one config line | 2026-09 | Whether a shim is warranted per tool |
| Anthropic's target is under 200 lines per `CLAUDE.md`; Claude Code loads one of up to 4 MiB in full and skips a larger one | 2026-09 | The budget table. The one published number behind it; the others are this file's heuristics |
| Codex stops adding instruction files once their combined size reaches `project_doc_max_bytes`, 32 KiB by default | 2026-09 | The budget table. Truncation reads exactly like being ignored |
| Deny rules are evaluated ahead of allow at every scope and survive permissive modes — but govern the agent's own tools, not a script it writes | 2026-09 | Dimension 4. Bounds what the enforced layer can honestly claim |
| Adherence to written instructions may decay within a session — about 5.6% lower odds of compliance per additional function generated, an exploratory, non-monotonic finding; the same study found no detectable effect of file size, position, structure or conflicts (`arXiv:2605.10039`) | 2026-09 | Why the gates exist, and why the conformance block sits last |
| Audits of public skill marketplaces found between a quarter and a third of published skills flawed (Snyk: 36.82% of 3,984; `arXiv:2601.10338`: 26.1% of 42,447), with confirmed coordinated malicious campaigns | 2026-09 | Dimension 4's inventory of hooks, skills and plugins |

### Language toolchains

**Used by Part II and dimension 2. Check the current release before pinning anything — and
check what answered you, per the probe rule above.**

| Stack | Current at 2026-09 | Lockfile | Notes |
|---|---|---|---|
| **Python** | 3.14.x, stable since 2025-10; 3.13.x still maintained; `uv` carries the momentum, Poetry fully supported, pip-tools for minimalists | `uv.lock` / `poetry.lock` | `ruff` for lint and format, `pytest`, `src/` layout. Dependency groups are standardised |
| **PowerShell** | 7.6.x | none exists | Pester 5.7.x is the safe pin — 6 exists and breaks things. `PSScriptAnalyzer` for lint |
| **.NET / C#** | 10, LTS | `packages.lock.json`, opt-in | `Directory.Build.props` for shared properties, `Directory.Packages.props` for central versions |
| **JS / TS** | Node 22 and 24 both LTS | `package-lock.json` / `pnpm-lock.yaml` | Biome 2.x for a new project; ESLint plus Prettier where plugins already exist. Vitest for new tests |
| **Go** | 1.27 | `go.mod` + `go.sum`, both committed | `go vet`, `go test -race`, `gofmt`. Pin `golangci-lint` by version in CI |
| **Rust** | 1.98.x, edition 2024 | `Cargo.lock`, **committed for libraries too** | `cargo fmt --check`, `clippy -D warnings`. That lockfile guidance reversed in 2023 — old advice says otherwise |
| **C with meson** | `meson.options` is the current filename; `meson_options.txt` still works | none | Every building directory carries its own `meson.build` |
| **Shell** | — | none | `shellcheck`, `shfmt`, `bats` |

### Published standards worth citing instead of reinventing

| Standard | What it already covers | Where this file defers to it |
|---|---|---|
| **OpenSSF Scorecard** | Nineteen automated supply-chain and process checks, runnable as a workflow | Dimension 8, and parts of 6 and 7 |
| **OpenSSF Best Practices Badge** | Self-attested practices a scanner cannot detect | A T3 project with external users |
| **MADR** (4.x) | A published decision-record format, minimal and full variants | Dimension 10 |
| **Keep a Changelog**, **Semantic Versioning**, **Conventional Commits** | Changelog shape, version meaning, commit grammar | Dimension 10 |
| **C4 model** | Context, container, component and code views | Part II, where structure needs a diagram |

**Where one of these already specifies something, cite it and move on.** A finding that
re-derives a published check by hand costs the reader the chance to use the tooling that
already implements it.

---

# The Run

## Phase 0 — Preflight

```bash
git status --porcelain          # must be empty
git fetch --tags --prune        # BEFORE any tag or branch claim
git remote -v
git rev-parse --abbrev-ref HEAD
git rev-parse --is-shallow-repository
date -u
git log -1 --format='%H %ad' --date=short
```

Refuse to continue unless the working tree is clean and it is a git repository with a remote
(or the human confirms it is deliberately local).

**Read the default branch name; never assume `main`.** It can be anything — a fork often
keeps a branch named for its purpose. Every rule below that reasons about "the default branch"
means the one this repository actually has, and a finding that names `main` on a repository
whose default is something else is reading the wrong branch.

**Fetch before you read refs.** Tag counts, branch positions and "N commits behind" are all
wrong from an unfetched clone, and a wrong one has already been written into a decision
record as fact.

**Branch.** Use `chore/config-audit` unless the harness pins one, in which case use that and
record it. Not a question — a recorded override.

**Probe capability before relying on it.** Try a harmless command, a scratch write, a remote
CI read, and a tag listing. **Record each as yes / no / unknown.** A capability assumed and
absent produces advice the human cannot follow; a capability present and unused wastes the run.

**Three things cannot be detected. Ask them once — and ask them at the Phase 3 wait, not
here:**

1. **Is there a local working copy of this repository?** Decides tagging, hooks and desktop
   tooling. **Default if unanswered: no**, which is the more restrictive assumption.
2. **Is there a standards repository these projects share?** Name it, or "none".
3. **Who holds copyright?** The legal entity, not the account name.

**Carry them forward rather than stopping here.** Two waits is both the floor and the
ceiling, Phase 3 already stops and already asks the human about copyright, and a separate
round trip for three short questions costs more than it returns. **Three independent runs
each invented this same fold and recorded it as an override** — a deviation that recurs with
the same reasoning is a rule waiting to be written, so it is written. Record the answers in
the Phase 0 block as normal; they simply arrive one phase later.

```yaml
phase: 0
capabilities: {shell: yes|no|unknown, write_outside_repo: yes|no|unknown,
               remote_ci_readable: yes|no|unknown, can_create_tags: yes|no|unknown,
               enforced_layer: yes|no, third_party_repos_readable: yes|no|unknown}
capability_proof: |
  <the probe output, one line each>
asked: {local_working_copy: yes|no, standards_repo: "<name | none>",
        copyright_holder: "<entity>"}
degraded: [<what this run could not do, and what it recorded instead>]
tool: "<which agent and surface this ran on>"
clean_tree_proof: |
  $ git status --porcelain
  (empty)
fetch_proof: |
  $ git fetch --tags --prune
  <output>
remote: <url | none>
default_branch: <name as read, never assumed>
branch_used: <branch>
branch_override: <none | "harness-pinned to X">
shallow: yes | no
clock_session: <date -u>
clock_git: <git log -1 %ad>
clock_delta_days: <int>
go: yes | no
notes: <anything the fields cannot hold | none>
```

## Phase 1 — Detect Mode

<constraints>

**Everything here is detected by content, never by filename.**

A **decision record** under any name or case satisfies the condition. **Its existence is not
evidence of a prior audit** — grep it for a recorded **tier**.

A **runbook** is content. **A README section — Production Deployment, Operations, Deploy,
Maintenance — with ordered operational steps is a runbook.** Grep headings across all
markdown before concluding one is absent. Existing-but-wrong is `DRIFT`, not missing.

</constraints>

```bash
git ls-files | grep -iE '(^|/)(DECISIONS|ADR|decision-log|KDD)\.md$|(^|/)docs/adr/'
git grep -icE 'tier:? *T[0-3]|blast radius|audience A[0-3]' -- <the record found>
git grep -inE '^#+ *(production )?(deployment|deploy|operations|runbook|maintenance)' -- '*.md'
```

| Mode | Condition | Action |
|---|---|---|
| **Greenfield** | No source files | Interview, then generate |
| **Retrofit** | Source exists, no agent configuration | Inventory, then generate around it |
| **Audit** | Agent configuration exists, **no recorded tier** | Inventory, audit, propose, record |
| **Re-check** | **A recorded tier exists** | Diff against the recorded entry |

<constraints>

**Re-check has obligations `audit` does not.** Read the prior entry and carry it forward:

- **A previously declined item is not re-proposed** unless its reopen trigger has fired. A
  re-check that re-raises a decline as a fresh amendment has failed — it destroys the value
  of recording declines and makes the human re-litigate a settled question.
- **A deferred item is re-proposed only when its trigger has fired.** Say which fired.
- **A trigger only watches what it is worded about, and the tier has two axes.** Blast
  radius asks what breaks; audience asks who is affected. **A trigger phrased about the
  repository — "a second person commits", "a second person gets repository access" — cannot
  fire on an audience change**, because using a thing and committing to it are different
  populations. This is not hypothetical: a live re-check moved a project from A1 to A2 as a
  team began maintaining what it produced and another read its output, **and not one recorded
  trigger fired** — every one was written about who commits, and the committer had not
  changed. The tier moved and the record did not notice.
- **So when recording a trigger, ask which axis would move this, and word it in that axis's
  terms.** A decline that rests on "only one person is affected" needs a trigger about people
  affected — who reads the output, who depends on it being right, who maintains the running
  deployment. A decline that rests on "only one person can change it" is correctly worded
  about commits. **A trigger set that mentions only one axis is a blind spot on the other**,
  and it is worth saying so on a re-check even when nothing fired.
- **An item recorded "do not re-propose" is never re-proposed.** Record it `N/A`, and
  **carry every such item forward exhaustively** — the whole set from the record, not a
  selection. A dropped entry is one a later run will raise again, which is the failure the
  list exists to prevent.
- **Dimensions fixed by the prior run are verified, not re-audited from scratch.**
- **Every local dependency mitigation is re-examined** against its upstream — **discovered,
  not merely read out of the decision record.** A mitigation that was never written down is
  the one most worth finding. Search at least: lockfile and constraints-file headers and
  comments; any exact `==` pin, especially one carrying a comment; `filterwarnings`,
  `ignore`, or suppression entries naming a package; vendored or patched copies under the
  tree; wrapper and adapter modules that exist to route around a dependency. Fixed upstream
  means the local workaround is now `DRIFT` and should come out. Not fixed means say so and
  move on. **An empty list is a claim that you searched and found none — say where you looked.**

</constraints>

Record the decision-record alias once and use it everywhere. **Never propose a second path.**

```yaml
phase: 1
decision_record_found: <path | none>
decision_record_alias: <path used for the rest of this run>
decision_entries: <int>      # dated entries in the decision record
adr_files: <int>             # files under docs/adr/ or equivalent; 0 is common
recorded_tier: <T0-T3 | none>
tier_grep_proof: |
  <literal output>
runbook_found: <path and section | none>
runbook_proof: |
  <literal output>
mode: greenfield | retrofit | audit | recheck
mode_evidence: <one line tying the condition to the output>
prior_entry: <date and id of the entry being diffed against | n/a>
prior_declines: [{id: <id>, trigger: "...", fired: yes | no}]
prior_deferrals: [{id: <id>, trigger: "...", fired: yes | no}]
local_mitigations: [{dependency: "<name>", version: "<pinned>", defect: "...",
                     upstream_fixed: yes | no | unknown, evidence: "...",
                     removal_condition: "..."}]
do_not_repropose: [<items recorded as settled>]
notes: <... | none>
```

## Phase 2 — Inventory

Read-only, apart from the setup carve-out.

```bash
git ls-files | sed -n 's/.*\.\([a-zA-Z0-9]*\)$/\1/p' | sort | uniq -c | sort -rn | head -15

for f in AGENTS.md CLAUDE.md GEMINI.md .github/copilot-instructions.md \
         .claude/settings.json .claude/settings.local.json .mcp.json; do
  [ -e "$f" ] && printf '%-9s %5s  %s\n' \
    "$(git ls-files --error-unmatch "$f" >/dev/null 2>&1 && echo tracked || echo UNTRACKED)" \
    "$(wc -l < "$f")" "$f"
done
ls .claude/rules/ 2>/dev/null
ls .git/hooks/pre-commit 2>/dev/null || echo "pre-commit NOT INSTALLED"

git ls-files '*.md' | while read -r f; do
  printf '%6s  %s  %s\n' "$(wc -l < "$f")" \
    "$(git log -1 --format=%ad --date=short -- "$f")" "$f"
done | sort -rn | head -25

ls pyproject.toml package.json *.csproj go.mod Cargo.toml meson.build *.psd1 2>/dev/null
ls uv.lock package-lock.json Cargo.lock go.sum poetry.lock requirements.lock 2>/dev/null
git tag --sort=-v:refname | head -3        # AFTER the Phase 0 fetch
ls .github/workflows/ .gitignore .gitattributes .editorconfig \
   .pre-commit-config.yaml .githooks .copier-answers.yml LICENSE* 2>/dev/null
```

**Read the remote CI conclusion** for the current head and for the default branch. A red
default branch nobody noticed is a finding in its own right, and local gates cannot see it.

<constraints>

**`ls` cannot distinguish tracked from untracked.** Use `git ls-files --error-unmatch`.
An **untracked** `.claude/settings.local.json` enforces nothing durable and is often
generated by the auditing session itself. **A finding, not configuration.**

**Configured is not installed** — and this cuts both ways. A committed
`.pre-commit-config.yaml` with no `.git/hooks/pre-commit` is inert, which is normal in an
ephemeral session. **But an ignore rule without the thing it ignores is also inert:** a bare
`scratch/` in `.gitignore` with no directory present gives git nothing to descend into.
Check the rule and the thing separately.

**A document asserting a state that is not true is the single most repeated finding this
standard has produced, and it is worth naming as a class rather than meeting case by case.**
Live runs have found: three documents insisting an application was not yet live while it was
running in production; a test plan describing a coverage upload as a live capability when it
had never once succeeded; a document stating its own open-questions series was fully resolved
while a later section of the same file listed four as outstanding; a README citing a version
behind the release it shipped with; and a context file asserting it was loaded by every
session when nothing loaded it at all.

**The shape is always the same: a claim about the system, written once, true then.** None of
them is a missing file, so nothing that checks for presence finds them, and none breaks a
test. **So check the claims, not the files** — where a document states that something is
true of this system, verify that thing directly, and rank a document that is wrong above one
that is merely thin. A reader who follows a false instruction during an incident is worse
off than one who finds nothing written.

**A file existing is not evidence that it says the right thing.** Where a file the standard
expects is already present — a context file, a checklist, an ignore file, a CI workflow —
**read it and confirm it does what its name claims** before rating the dimension `OK`. A
`TEST-VERIFICATION-CHECKLIST.md` that is a stub, a CI workflow that runs nothing, an
`AGENTS.md` describing a structure that has since moved: each passes an existence check and
fails its purpose. **Where its content cannot be confirmed, say so rather than crediting it.**

**If a reconnaissance report exists for this repository in this session, Phase 2 is a diff
against it, not a re-run.**

**In greenfield mode there is nothing to inventory.** Phase 2 instead **chooses the shape**:
which project shape from the layout section, which languages, which auxiliary file types are
expected. Emit those as the inventory. Documented commands do not exist yet, so
`command_tally` is all zeroes and `setup` records what the chosen toolchain will need.

</constraints>

### Execute the documented commands

Read build, test, lint, format and run commands out of the manifests and scripts, then run
them. **Fast gate first.** Time-box past roughly five minutes as `NOT-RUN-HERE`.

**Allowlist:** build, test, lint, format, type-check.
**Never run:** deploy, publish, release, migrate, seed, drop, anything touching production.

**Record the collection count, not only the exit code.** A suite that collects fewer tests
than the project documents has failed even at exit 0 — silently skipped modules exit green.

```yaml
phase: 2
recon_report_used: <path | none>
environment_preexisting: [<what was already installed at session start | none>]
setup: [{cmd: "...", result: PASS, note: "project's own declared deps"}]
languages: {py: 109, md: 23}
agent_config: [{path: CLAUDE.md, tracked: true, lines: 1082}]
total_lines_loaded_at_session_start: <int>
reference_markdown_lines: <int>
hooks_configured: yes | no
hooks_installed: yes | no
hooks_proof: |
  <literal output>
ci: {workflows: [<paths>], jobs: [<names>]}
ci_remote_conclusion: {head: <success|failure|none>, default_branch: <success|failure|none>,
                       proof: "<how it was read>"}
gates_present: [lint, type-check, test]
gates_absent: [secret-scan, format-check]
lockfile: <path | none>
license_file: <path | none>
tags: <int>
repo_visibility: public | private | unknown
plan_supports_branch_protection: yes | no | unknown
collaborators: <int | unknown>
history: {commits_visible: <int>, shallow: yes|no}
present: [<notable files found>]
absent: [<notable files missing>]
commands: [{cmd: "...", result: PASS, detail: "exit 0", collected: <int | n/a>}]
command_tally: {PASS: 0, FAIL: 0, UNVERIFIABLE-HERE: 0, NOT-RUN-HERE: 0}
template: {copier_answers: present | none}
notes: <... | none>
```

## Phase 3 — Establish Tier — **WAIT**

**Six questions. Phase 3 always stops here — including on a re-check.**

On a **first audit**, ask all six. If a reconnaissance report in this session carries answers
1–4, use them verbatim, name the report, and do not re-ask.

On a **re-check**, do not re-ask from scratch and do not silently carry forward either.
**Show the recorded answers and ask what has changed**, with "nothing has changed" as the
stated default. This costs one exchange and catches the thing a record cannot: a tier rated
on the *imminent* state whose trigger has since fired. A record describes what was true when
it was written, and only the human knows whether it still is.

**Do not fold this into the Phase 6 gate.** A tier confirmation arriving after the dimensions
have been rated is a confirmation of work already done.

1. **Owner** — work (employer-owned) or personal?
2. **Exposure** — already public / possible later / never?
3. **Production** — touches production **today, or one un-committed change away**?
4. **Dependents** — does anyone else run it or depend on its output?
5. **Copyright holder** — if work-owned, the exact legal name.
6. **Where it actually runs** — what machine runs it today, how it is started, what address
   it binds, and who can reach that address. **Four parts, asked every time, including on a
   re-check.**

<constraints>

**Where and how the software runs is asked of the human, never read from the repository.**
A deployment section describes what someone intended, or what was once true. **It is
evidence of intent, not of state**, and nothing in a repository can tell you which it is.

**This is the most consequential premise failure this file has recorded.** A full audit of a
live production application — twenty-two amendments, a dozen commits, four green CI runs —
was conducted against a deployment described in the repository's own runbook: a service
manager on a server, behind a web server with authentication available. **None of it existed.**
The application ran from a launcher script on the maintainer's workstation, bound to all
interfaces, reachable from the office network and from VPN. Every session that read the
runbook believed it, and so did every reviewer.

**The cascade is the reason this is a Phase 3 question rather than a Phase 4 finding.** The
tier basis rested on it. An exposure finding was live at a higher severity than recorded,
because the side door flagged as a risk was the actual configuration. The security policy
had accepted a risk on a basis that did not exist. A human action was addressed to a server
administrator who turned out to be the maintainer. An interpreter-version question was chased
through a service manager's registry keys on a machine that was not there. **A dependency
bot was urged as the one item costing something because a lockfile "pinned the production
host"** — there was no production host, and the bot was later removed as over-built.

**It was found by asking four direct questions instead of inferring it again.** The human
knew the answer throughout. Nobody asked.

**Record the answer as given and compare it with the documentation.** Where they differ, the
documentation is the finding — a document asserting a state that is not true, in the section
someone reads during an incident — and the tier is computed from what the human said. **Where
the human does not know**, that is itself the answer: record `unknown`, and treat every
finding that depends on the deployment as `UNVERIFIABLE-HERE` until someone finds out.

**Do not skip this on a re-check because it was answered last time.** A deployment changes
without a commit — a machine is replaced, a service is moved, a port is opened — and the
repository never hears about it. Show the recorded answer and ask whether it still holds,
exactly as the tier questions are asked.

</constraints>

| Blast radius | | Audience | |
|---|---|---|---|
| **B0** | Nothing breaks | **A0** | Nobody |
| **B1** | Only my machine | **A1** | Just me |
| **B2** | My or others' data | **A2** | Colleagues, a team, a floor |
| **B3** | Production, the business, or the public | **A3** | External or public |

**Tier = the higher of the two.** Record both.

<constraints>

**Rate the imminent state.** If a promotion trigger is one un-committed action away, rate as
though it has fired and say so.

**Blast radius is rated on the output, not only on inbound access.** Read-only access bounds
what a leaked credential reaches; it does not bound what depends on what the tool produces.

</constraints>

<!-- WHY only five are forced: everything below rank 5 is a two-way door, and forcing a
     decision on a reversible choice at inception turns a scaffolder into an interrogation.
     Defer with a trigger instead. -->
### The irreversibility gate

| Rank | Decision | Why it cannot be undone |
|---|---|---|
| 1 | **Outbound licence** | Irrevocable for released versions |
| 2 | **Published package name** | Registries permanently reserve a used name |
| 3 | **Public API / wire contract** | Every consumer multiplies the cost |
| 4 | **Data model semantics** | Reversible in code, not in data already written |
| 5 | **Language and runtime** | Contained only with clean module boundaries |

Answer all five explicitly, including those already settled by existing reality — these are
the decisions that cannot be revisited cheaply, so a recorded "we chose this" is worth more
here than anywhere else. **Everything below rank 5 is deferred with a trigger rather than
decided now.**

<constraints>

**In greenfield mode, ranks 1 and 5 are answered here and the reasoning comes from Part II.**
A run that picks a language without saying why has made the least reversible decision in the
project silently. Read *Choosing a Language and Runtime* and *Choosing the Shape*, then
bring back a recommendation with its trade — not a decision. The human picks.

**The discipline is the door test, and it cuts both ways.** A one-way door — the language,
the persistent data model, publishing publicly — is decided slowly and recorded. A two-way
door — the formatter, the test runner, the directory names — is decided in one line and
changed later if it was wrong. **Applying the heavy process to a two-way door is the more
common failure**, and it turns a scaffolder into an interrogation. Where you are unsure which
kind a decision is, ask what undoing it would cost in a year.

**Three questions only greenfield asks**, and only where the answers are not already implied:

1. **What does it do, in one sentence, and what runs it** — a person at a terminal, a
   schedule, an HTTP request, another program?
2. **Where does it run** — a server you control, a workstation, a container, a colleague's
   machine, a CI runner? This bounds the language more than preference does.
3. **What does it keep** — nothing, files, a database, someone else's system of record? The
   persistent data model is rank 4 and is reversible in code but not in data already written.

Record the answers in `inception`. **Do not ask a fourth question to be thorough.**

</constraints>

```yaml
phase: 3
answers_source: <recon report path | asked directly>
owner: work | personal
copyright_holder: <legal name | account or handle | n/a>
exposure: already_public | possible_later | never
production: today | one_change_away | no
dependents: <who | none>
blast_radius: B0-B3
audience: A0-A3
tier: T0-T3
tier_basis: current | imminent
tier_reasoning: <required when basis is imminent, or when inbound and output differ>
tier_previous: <T0-T3 | none>
irreversible_resolved: [{rank: 1, decision: "...", state: "decided now | settled | locked"}]
irreversible_open: [<ranks still undecided>]
deployment:                   # asked, never read from the repository
  runs_on: "<the machine, as the human names it | unknown>"
  started_by: "<launcher, service manager, schedule, container | unknown>"
  binds: "<address:port | unknown>"
  reachable_from: "<who can reach that address | unknown>"
  source: asked directly | recorded answer confirmed unchanged
  matches_documentation: yes | no | no documentation
inception:                    # greenfield only; omit the key entirely otherwise
  purpose: "<one sentence>"
  invoked_by: person | schedule | http | another program
  runs_on: <server | workstation | container | CI runner | someone else's machine>
  persists: none | files | database | external system of record
  language: {chosen: "<lang>", runner_up: "<lang | none>", why: "...",
             decided_by: human | already settled}
  shape: <from the shapes table, or a named external convention>
notes: <... | none>
```

## Phase 4 — Audit the Ten Dimensions

### 1. Stakes and lifecycle

<!-- WHY declines are recorded with triggers: without them every run re-litigates settled
     questions and the human stops reading the gate. A decline honoured until its trigger
     fires is the difference between a standard and a nag. -->
Tier recorded with history and both axes. Deferrals carry triggers. **Declines carry reopen
triggers** — honored until the condition fires.

### 2. Language, runtime and reproducible environment

Every language present has a rule file; none for absent languages. Lockfile committed from T1.

<constraints>

**A lockfile is generated from the working environment, not resolved fresh.** `uv pip compile`
or `pip-compile` with no constraints resolves **latest** — a "lock" that is an upgrade in
disguise. Use `--no-upgrade`, `poetry lock --no-update`, or compile against `pip freeze`
constraints.

**Measured consequence:** a bare compile bumped `anyio` one minor version, whose own
`DeprecationWarning` became a collection error under `filterwarnings = ["error"]`. Four
modules stopped importing and **998 tests were collected instead of 1533 — at exit 0.** Local
gates missed it because the local environment held the old version.

**Verify the lock on every matrix leg, and in a fresh clone.** Record the regeneration command
including that verification in the lockfile header.

</constraints>

**Where a tool is configured in more than one place, compare them. A divergence is `DRIFT`
even when every location is individually pinned.**

<constraints>

**A lockfile the CI does not install from is decoration.** Committing the lock is half the
control; the other half is an install mode that **fails** rather than re-resolving when the
lock and the manifest disagree. Check the CI command, not the presence of the file:

| Ecosystem | Lockfile | The install that fails on drift |
|---|---|---|
| Python — uv | `uv.lock` | `uv sync --frozen` (or `--locked`) |
| Python — Poetry | `poetry.lock` | `poetry install` — errors when the lock is stale |
| Python — pip-tools | `requirements.txt` compiled | `pip install --require-hashes -r` |
| JS / TS — npm | `package-lock.json` | `npm ci` — never `npm install` |
| JS / TS — pnpm | `pnpm-lock.yaml` | `pnpm install --frozen-lockfile` |
| .NET | `packages.lock.json` | `dotnet restore --locked-mode` |
| Go | `go.mod` + `go.sum` | default `-mod=readonly`, plus `go mod verify` |
| Rust | `Cargo.lock` | `cargo build --locked` / `cargo test --locked` |
| PowerShell | none exists | explicit `-RequiredVersion` on every module install |

**`npm install` in CI is the single most common form of this finding** and it reads as green
while quietly writing a different tree than the lock describes.

**Regenerating is not upgrading, and the commands differ per ecosystem.** `go mod tidy`
re-derives without upgrading and `go mod tidy -diff` checks non-destructively; `go get -u`
upgrades. `cargo update` upgrades; `--locked` refuses to. The Python case is the one this
file already documents and the one that has bitten. **Name the exact regeneration command in
the lockfile header** so the next person does not guess.

**The language choice itself is recorded here.** Rank 5 of the irreversibility gate is
language and runtime; *Choosing a Language and Runtime* is where
the reasoning is made, and this dimension is where a repository is checked against it. A repository whose
recorded choice and actual manifest disagree is `DRIFT` on this dimension, not a curiosity.

</constraints>

### 3. Repository structure and hygiene

**Structure.** One source root, one test root, and nothing important at top level that
belongs inside one of them. The layout matches the project's shape — see **Project Shapes
and Layout** — and the `AGENTS.md` module map describes the layout that exists rather than
one that was intended.

Findings worth raising: source files scattered at the repository root; tests interleaved with
source where the ecosystem separates them; two directories doing the same job; a directory
named in the module map that no longer exists; auxiliary files with no consistent home.
**Restructuring an established repository is rarely worth it** — say so, and record the cost,
unless the layout is actively causing the confusion.

**Hygiene.** `.gitignore`, `.editorconfig`, `.gitattributes` with real EOL rules. Defaults,
not choices. `CODEOWNERS` once a second person exists.

### 4. Agent configuration

- `AGENTS.md` canonical; `CLAUDE.md` a shim holding only what cannot be portable.
  **Claude Code reads `AGENTS.md` natively only in some sessions** (from v2.1.277, as of
  2026-09): when no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists, and not on
  Bedrock or other third-party providers, with telemetry off, or in the first session after an
  install or upgrade. **So keep the shim.** A one-line `CLAUDE.md` containing `@AGENTS.md`
  works in every session, and the vendor documents that it never loads `AGENTS.md` twice;
  `ln -s AGENTS.md CLAUDE.md` is the other documented route. **Prefer the import** — a symlink
  is invisible in a file listing, survives badly on Windows checkouts, and this maintainer
  works across both. A run that claims Claude Code picks up `AGENTS.md` on its own in every
  session has asserted something false.
- **Verify the context file actually loads. Do not infer it from the file existing.** The
  cheapest proof is the session's own context: list what the harness loaded this run, and check
  the canonical file is in it. A live audit run did exactly this and found `AGENTS.md` — 62
  lines carrying the module map and six documented commands — **reaching no session at all**,
  because the shim linked to it in markdown rather than importing it. A markdown link is not an
  `@` import. Both files claimed the content was loaded; neither was, and nothing failed.
  **This is the highest-value single check on this dimension**, because the failure is
  invisible from the filesystem and indistinguishable from the file being ignored.
- **Size is a real constraint, not a style note.** Keep the always-loaded context under ~300
  lines; Codex stops reading instruction files past 32 KiB combined (`project_doc_max_bytes`),
  and truncation is indistinguishable from the file being ignored. Put instructions near the end
  of a long file rather than the start.
- Language rules in `.claude/rules/` load **per file** — that is the point of the split.
- `.claude/settings.json` carries the enforced layer. Deny beats allow. A baseline worth
  having: reads of `.env*`, recursive delete, force push. Each is declinable — say what it
  stops and what declining exposes. **No `ask` rules in an unattended session** — a stall,
  not a gate.
- **Know the precedence before rating this dimension.** Highest to lowest: managed or
  enterprise policy, then `.claude/settings.local.json`, then `.claude/settings.json`, then
  the user file under `~/.claude/`. Permission rules **merge** across those scopes rather
  than the nearest one replacing the rest, and within the merged set the order is
  **deny, then ask, then allow**, first match winning. A deny at any scope cannot be undone
  by an allow at another.
- **A deny rule names an access path, not just a file.** `Read(.env*)` leaves `Bash(cat .env)`
  open — same file, different tool, no rule. For each thing that must not be reached, cover
  every tool that could reach it. **Verify the matcher works rather than assuming it**; a rule
  that has never fired has not been shown to fire.
- **State the ceiling on what deny can do, in the report.** Deny rules govern the agent's own
  file and shell tools. **They are not an operating-system sandbox:** a Python or Node script
  the agent writes and runs opens files through its own runtime, and no rule is consulted.
  Environment wrappers — `docker exec`, `npx`, a task runner — can carry an inner command
  past a rule written only against the outer one. Where the requirement is that a secret
  cannot be read at all, deny rules are a speed bump and the real control is that the secret
  is not on the disk. **Rating this dimension `OK` on deny rules alone overstates them.**
- A gitignored `scratch/` **directory**, present as well as ignored.
- `.mcp.json` absent unless justified and recorded.

**Domain invariants.** Where a project states an invariant an agent could violate, the deny
list is where it becomes real. **Record its presence as a strength, not as excess.**

**The context file is an input, so treat it as an attack surface.** Instructions inside a
context file that arrived with a dependency, a vendored copy, a submodule or a fork's
upstream are content an agent will read and may follow. Demonstrated in the wild. Where this
repository carries a context file it did not author — a nested `AGENTS.md` under
`vendor/`, `third_party/` or a subproject — **read it and say what it instructs**, and treat
an instruction to change tooling, disable a check or reach outside the tree as a `BLOCKER`
on dimension 7 rather than a curiosity on this one.

**Hooks are executable configuration, so read every one before rating this dimension.** A
hook in the settings file runs a shell command with the user's permissions, announces nothing
at runtime, and fires on events the session never narrates — the one place where
configuration acts rather than instructs. The precedent is concrete: a published 2025
vulnerability executed a repository's hooks **before the user had approved trusting it**
(patched since, but the class remains, and an audited repository is by definition one
somebody opened without having written it). The audit reads each hook's command and says what
it does. One that fetches remote content, reaches outside the tree, or fires on every tool
call is a finding to explain — never a style note.

**Installed skills and plugins are dependencies with instructions inside, and the supply is
measurably compromised.** Audits of public skill marketplaces in early 2026 found between a
quarter and a third of published skills carrying at least one flaw (36.82% of 3,984 in Snyk's;
26.1% of 42,447 in `arXiv:2601.10338`), and confirmed coordinated malicious campaigns among
them — vendor and preprint audits rather than peer review, but
corroborated across independent sources and in the direction that matters here. So the
inventory treats them exactly like dependencies: where each came from, whether it was read
before adoption, and whether anything inside instructs the agent to change tooling, weaken a
check, or reach outside the repository. **An unreviewed third-party skill is a `GAP` at any
tier; one carrying such an instruction is a `BLOCKER` on dimension 7.**

**The files that instruct future sessions are the highest-risk write class, and they change
only through the gate.** The context file, the enforced layer, hooks, and skills are the
agent's own instructions — a session that edits them mid-run has changed what every later
session believes, silently, and self-written instructions are the measured *weaker* case, not
the stronger one. Proposals to these files arrive as reviewable diffs at Phase 6 like any
other amendment, never as in-session writes; a history showing the context file changing
inside ordinary working commits, unreviewed, is this finding already made.

**If `OVER`, emit the split recipe:** canonical keeps enforced conventions and the module map;
domain and reference prose move to `docs/` and are linked; per-subsystem rules go to
`.claude/rules/`. **Absorb, do not stub** — sections move in the same commit, and text
describing something retired is deleted rather than relocated.

### 5. Testing and verification

`TEST-VERIFICATION-CHECKLIST.md` from T1. Coverage threshold at T3, **set from the currently
measured number so it ratchets**. Mutation testing at T3 only.

**A gate that matches text can be satisfied by its own documentation, so match structure
instead.** A live run wrote a gate to prove a downloaded binary was checksum-verified before
execution. It searched the raw workflow file for the verification command — and found it **in
the comment the same commit had just added explaining the verification.** The gate passed 23
checks with the real check moved to *after* the binary ran. Parsing the YAML and comparing
executable lines fixed it. **The general form: a gate reading a file as text sees comments,
documentation, disabled blocks and its own explanation, all of which satisfy a match and none
of which execute.**

**So prove a gate by mutating what it guards, not by running it once.** Break the thing three
ways — remove it, reorder it so it runs too late, and disable it in place — and confirm the
gate fails each time. A gate that has only ever been watched passing has been watched
agreeing with the current state, which it would also do if it matched nothing.

**And there is a cheaper test that needs no mutation invented at all: run the gate against
the parent commit.** Every gate defect found across two repositories shared one property —
**the gate was written in the same change as the thing it guards**, so it had only ever been
observed agreeing with a state that was already correct. The parent commit is that gate's
one unseen state, it is always available, and it costs a checkout. **A gate introduced
alongside its subject and never run against the state before it has not been tested, it has
been observed.**

**A gate's condition must also be proven to see what it tests.** A condition that references
something unavailable in its context evaluates to nothing and reads as a gate: a live run
wrote `if: ${{ secrets.TOKEN == '' }}` at step level, where the secrets context is not
available, so the check it looked like was never performed. **Print the value once before
relying on it**, or assert on it, and keep the proof. This is not caught by mutation —
mutating the subject changes nothing about a condition that was never reading it.

**A scanner or gate reporting "clean" must first be shown to detect.** Before trusting a
secret scan, a linter, or any sweep that reports finding nothing, **plant a positive and
confirm it fails, then remove it and confirm it passes.** A gate that has never caught
anything has not been shown to work, and "clean over 22 files" from a scanner that cannot
detect is indistinguishable from coverage. Do this when the gate is installed and whenever
its configuration changes.

**Plant the shape that actually occurs, not the shape the tool advertises — coverage is
shape-dependent, and proving one shape proves one shape.** A live run discharged this rule
honestly, planting a canonical provider key, watching the scan fail, and recording the gate
as proven. A later probe found the same scanner **missed a backticked bare `VAR=value` in
both markdown and Python** — which is the ordinary way a credential arrives, pasted out of a
terminal. The recorded claim was literally true and the confidence it carried was wider than
the tool. **So plant two: one canonical identifier, and one bare assignment in the file type
where prose and pasted output actually land.** Where the second is missed, that is a
dimension 7 finding in its own right, and the honest wording of the record is which shapes
were proven rather than that the scanner works.

**A test that passes while asserting nothing is worse than a missing test**, and so is a
suite that collects fewer tests than it should. **A collection guard compares against a
recorded baseline, not against zero** — failing only when nothing collects catches total
collapse and misses the partial fall it exists to catch. Record the expected count and fail
when the actual drops below it. **Where a test discovers its own inputs, it carries a guard
that fails when it stops finding what it should. Collection count is part of a passing
result.**

**The verifier is independent of the thing verified, or it is not a verifier.** Two published
failure cases carry this rule: an agent that removed the markers its own checker looked for
rather than fix what the checker caught, and self-written tests whose false positives dragged
results below having no tests at all. Locally that means a test authored in the same change
it validates is weak evidence until it has been **watched failing against the old code** —
the checklist already requires this — and anything that scores a run (the answer key, the
recorded baseline count, the release gate's checks) lives where the thing being scored
cannot edit it.

### 6. Enforcement and review

Two things stand between a change and the default branch: what gates it, and what looks at it.

#### Gates

| Mechanism | Enforces | Survives an ephemeral session? |
|---|---|---|
| `.claude/settings.json` deny rules | Agent actions | Yes — committed |
| `.claude/settings.local.json` | **Nothing durable** | No — untracked, often session-generated |
| `ask` rules | Nothing, unattended | Only with a human present |
| Git hooks / `pre-commit` | Pre-commit gates | **Only if committed, *and* installed by the session that commits.** With no local clone every commit comes from an ephemeral container, so an uninstalled hook gates nothing |
| CI required checks | Merge gating | Yes — server-side |
| Branch protection | Force-push, direct commit | Server-side, **and unavailable on private repos on free plans** |
| Repository rulesets | The same, plus tag rules | Server-side, **and gated on exactly the same plans** — not a free-tier substitute |
| Push rulesets | Blocks pushes across a repository and its fork network | **Gated higher still** — organisation plans only, not personal paid ones, and private or internal repositories only. Usually `N/A` here |

**The gates must exist; the runner is not dictated.** A deliberate `repo: local` /
`language: system` config with documented reasoning is not a finding. Required gates: secret
scan, format check, lint, test.

<constraints>

**Enforcement placement is a tier decision, not a default.**

| Gate | Where it belongs |
|---|---|
| Secret scan | **CI, always.** Plus platform push protection, which is server-side and free |
| Format, lint, test | **CI, always** |
| Any client-side hook | **Only where a persistent local development environment exists** |

A blocking pre-commit gate buys a few minutes of earliness and costs an interrupt on every
false positive. **Where the maintainer keeps no local clone it buys nothing at all** — the
hook is absent from every ephemeral container unless that session installs it, so it gates
the commits it happens to be present for and no others. That is worse than no gate, because
it reads as coverage. CI runs on every push regardless of where the push came from.

**Before proposing a client-side hook, establish that a persistent local environment exists.**
If it does not, the amendment is CI-only and the hook config is documented as session setup.

**An enforced rule with a repeated false-trigger rate is `OVER` on this dimension** — even
when this standard installed it. Record what triggers it, how often, and what the human has
to do to get past it. **A rule the human routes around, or must hand-edit a file to satisfy,
is a rule that was wrong.**

**A secret-scan allowlist must not be coupled to line numbers.** A baseline recording the
line of each known-benign hit fails on any edit that shifts lines — a changelog edit breaks
the build with nothing about secrets having changed. **Measured consequence: a default branch
sat red for three days through a tagged release for exactly this reason.** Prefer path and
pattern allowlists.

**Excluding prose files is a remedy for baseline churn, not a default.** Where a
line-numbered baseline is installed, exclude prose at the hook level rather than re-baselining
on every edit. **Where the scanner keeps no baseline, excluding prose buys nothing and creates
a blind spot** — credentials get pasted into READMEs and runbooks. Apply the exclusion only
where the churn it prevents is real.

</constraints>

<constraints>

**Rulesets are not the free-plan escape hatch, and this is the most common wrong finding
on this dimension.** Repository rulesets are the newer mechanism and are better in most
respects, but their plan availability matches classic branch protection: public repositories
on a free plan, or public and private on a paid one. **On a free private repository there is
no server-side merge gate available at all**, and with no local clone there are no
client-side hooks either, which leaves that repository with nothing enforcing anything.

**Say that plainly rather than recording a bare `N/A`,** because it is the one finding on
this dimension with a real remedy, and the remedy is a decision only the human can make:

| Route | What it buys | What it costs |
|---|---|---|
| **Make the repository public** | Rulesets, required checks, secret scanning and push protection, all free | The code is public. Irreversible in practice — history is cloned before it can be withdrawn. Gate it on the Phase 3 `exposure` answer and on the provenance rule in dimension 10 |
| **Move to a paid plan** | The same controls on a private repository. For a personal account this is **GitHub Pro**, which is the cheap route and is often missed — organisation plans are not the only option | A recurring cost |
| **Accept no gate** | Nothing to pay, nothing to change | CI still runs and still reports; nothing stops a push that ignores it. Record it as an accepted risk with a reopen trigger, not as a `GAP` to re-raise every run |

**Verify the current state before reporting it.** Plan gating on these features has moved
before and at least one third-party account disputes the private-repository limit. Read the
repository's own settings page, or try creating a ruleset, and record what you actually saw
rather than what this table says.

</constraints>

Where a default branch is unprotected **and** production deploys from it directly, that
ranks `BLOCKER`: the consequence is that a red CI stops nothing between a push and the
users. Elsewhere `GAP` — **or `N/A` where the plan does not support protection**, which is
a fact about the plan and not a failing. Where recorded "do not re-propose", `N/A`, never
raised again.

#### Review, with one maintainer

There is no second reviewer, so review means something different here. Worth being explicit
about rather than skipping, and every item below is a suggestion with a stated cost.

- **A pull request you open and merge yourself still earns its place** where CI is the only
  server-side gate — it gives the checks somewhere to run before the default branch moves.
  Cost: a few extra steps per change. Declining means CI results arrive after the fact.
- **Read the diff, not the summary.** A description of a change is not the change, and an
  agent's account of its own work is the least independent reading available.
<!-- WHY: sixteen amendments including a tree-wide reformat once landed as one unreviewable
     diff. A mechanical sweep always gets its own commit — its noise buries everything else,
     and mechanical diffs are where silent breakage has actually been found. -->
- **Commit by concern is what makes review possible at all.** A formatter sweep mixed with a
  semantic fix cannot be reviewed — the noise hides the signal.
- **The mechanical diffs are the dangerous ones.** A reformat, a rename, a lockfile
  regeneration. They look boring, and they are where silent breakage has actually been found
  — a lock that collected 998 tests instead of 1533 at exit 0, and a reformat that exposed a
  contrast test which had stopped asserting anything.
- **An agent reviewing its own work is not review.** A fresh session reading the diff cold,
  with no memory of having written it, is the closest available substitute.

### 7. Secrets, security and data classification

<constraints>

**Committable:** usernames, BAQ names, column and field names, endpoint URLs, hostnames,
ports, database and schema names, timeouts, feature flags, structural configuration.

**Never committed. Placeholder only:** passwords, API keys, tokens, client secrets,
connection strings embedding a password, certificates, private keys.

**Placeholder convention:** an obvious sentinel — `CHANGEME` or empty. **Never a
realistic-looking fake.**

**A conforming placeholder is not a finding.** When this standard installs a scanner, it
scans first and seeds the allowlist from the existing conforming placeholders **in the same
commit**. Discovering them later as false positives is a defect of the installation, not of
the repository.

**Secrets reach code through environment variables only.** Never a tracked file, never
hardcoded — so the filling of those variables stays swappable with no repository change.

**A tracked path that a deployment host also writes is the real exposure, even when the
committed copy is clean.** Remedy: untrack, `.gitignore`, ship a `.example`, **and ship the
seed step in the same change** — the host's next clone will not receive the file and the app
will fail to start with no obvious cause. **Record the operational consequence: git no longer
backs that file up.** Where code prefers the tracked file's value over the environment
variable, untracking defers the exposure rather than closing it — a separate finding.

</constraints>

Secret scanning per the placement table. `SECURITY.md` at T3.

<constraints>

**Platform secret scanning is free on public repositories and paid on private ones**, as of
2026-09. Push protection is on by default for public repositories and blocks the push itself,
which is the only control in this file that stops a credential before it reaches the remote.
On a private repository the equivalent is a paid add-on, priced per active committer.

**So the finding differs by visibility, and both halves matter:**

- **Public repository, push protection off** — a `GAP` with a free remedy, which makes it one
  of the few amendments with no trade to weigh. Turn it on.
- **Private repository, no platform scanning** — `N/A` on the platform control, and the
  in-repository scanner in CI is then the whole of the defence rather than a second layer.
  Say which it is, because a CI scanner catches a credential **after** it is on the remote,
  and the remedy for a pushed credential is rotation, never deletion of the commit.

**Rotation is the remedy, and it is a human action.** A secret that reached a remote is
compromised whether or not the commit survives; rewriting history does not uncompromise it
and a fork or a cached view may hold it regardless. Phase 6 records it as a human action
with the credential named by location, **never by value**.

</constraints>

### 8. Dependencies

Manifests and lockfiles present. Automated updates grouped, weekly, low open-PR limit,
security PRs ungrouped.

**A three-day release cooldown is now the platform default** — version-update pull requests
wait until a release has been on its registry that long before opening, with no configuration,
as of 2026-07. Security updates are exempt and still open immediately, which is the behaviour
you want and a second reason not to group them.

**Read an existing `cooldown` setting against the default before rating it**, because the
three cases differ and only one is a finding:

| What you find | Verdict |
|---|---|
| A cooldown set to roughly three days | `OVER` — it configures what the platform now does anyway, and it will drift from the default when that moves |
| A longer window, seven or ten days | **Not a finding.** A deliberate hardening choice above the default, and the reasoning belongs in the decision record if it is not already there |
| `default-days: 0` under `cooldown:`, or a window below the default | A question rather than a verdict. Someone opted out of a supply-chain control; ask why before proposing anything |

**Do not propose adding a cooldown that matches the default.** It is the same `OVER` in the
making, one run later.

**A catch-all group with a low open-PR limit is a trap.** One breaking major inside the group
blocks every other update in that ecosystem behind it, and the symptom is silence rather than
a failure. Where you find one group covering everything, check whether anything has actually
landed from it recently before rating the dimension `OK`.

**Some Scorecard checks cannot pass at one maintainer, and chasing them makes things worse.**
Code-Review requires a second approver and its own documentation says the check is infeasible
for projects with a single active participant. Contributors requires contributors from
several organisations in recent history. Branch protection's higher tiers require one or two
reviewers and code-owner review. **Mark each `N/A` with the reason, deliberately, the same
way a dated fact that cannot be checked here is marked `UNVERIFIABLE-HERE`** — a gap left
unexplained reads as neglect on every future run.

**The trap is sharper than wasted effort, and it is the clearest `OVER` case this file has.**
Installing a required-review gate you must bypass on every commit does not merely fail to
help — **it lowers the score, because the repository now looks unreviewed rather than
unreviewable.** Ceremony that cannot pass its own check is worse than its absence, and the
same reasoning covers `CODEOWNERS` naming one person, a contributor agreement with one
author, and a proposal process filed with yourself.

**What is worth doing solo is the automated half**, none of which needs a second person:
least-privilege workflow tokens, pinned dependencies, no dangerous workflow patterns, signed
releases with provenance, a security policy, static analysis, and a license.

**Do not re-derive supply-chain hygiene from first principles.** OpenSSF Scorecard already
specifies and automates nineteen checks over exactly this ground — pinned dependencies,
dependency update tooling, signed releases, dangerous workflows, token permissions, branch
protection — and runs as a workflow. Where the repository would benefit, **propose Scorecard
rather than writing an equivalent by hand**, and cite it instead of inventing thresholds.
Its own caveat travels with it: the score measures process, and published work found no clean
correlation between a high score and fewer vulnerabilities. It is a hygiene signal, not a
security guarantee, and saying so is part of proposing it.

**Inbound licence allowlist:** MIT/BSD/Apache/ISC fine · MPL/LGPL fine · GPL fine **with a
recorded internal-only decision** · AGPL and BSL/SSPL/Elastic need explicit approval ·
**no licence, never**. Where the dependency is public, **verify the licence against the
repository rather than trusting package metadata** — they disagree more often than they should.

#### The upstream defect register

**Check the register before investigating.** The same upstream defect reaches every repository
that shares a dependency, and rediscovering it independently in each is waste — one defect has
already surfaced in three.

The register lives in the standards repository as `upstream-defects.md`, append-only, and
reaches each repository through the `copier` template, so **a new project starts already
knowing the defects its siblings have hit.** A session cannot see a sibling repository, so the
vendored copy is what it reads; staleness against the source is drift, like any vendored
contract.

One entry per defect, and enough to act on without leaving the file:

- **Package and the version range affected**, plus the **precondition that exposes it** — most
  are latent until something else is true. A deprecation warning is harmless until a project
  sets `filterwarnings = ["error"]`.
- **The symptom as it presents**, which is rarely the cause. Four modules failing to import
  does not look like a dependency deprecation.
- **Upstream status**: no fix, merged and unreleased, or released — with evidence and date.
- **What each affected repository chose**, so a fourth does not re-derive the trade.
- **The removal condition — and it must be verifiable by running something, not by inspecting
  something.** "When the upstream imports X instead of Y" is an inspectable claim that can
  read as satisfied while the symptom persists elsewhere; a guard removed on that basis breaks
  the build. **State it as a test: remove the mitigation, run the gate, keep the removal only
  if it stays green.** A condition that cannot be checked by running the suite is a guess with
  a date on it.

**When a run finds a defect the register does not hold, write the entry in portable form** —
complete standing alone, naming no repository-specific path — and surface it as a human action
to add upstream. **When the register records a defect as fixed, every repository carrying a
mitigation for it now carries `DRIFT`**, which is the point: one verification, every consumer
informed.

#### Reading a dependency's source

Most dependencies are never read, and should not be. **Read one only when something asks you
to**, and say which:

- **It is pinned to an exact version.** An exact pin usually records a problem somebody hit.
  Find out what, or the reason is lost.
- **It is documented as unmaintained**, or its last release is old against its issue traffic.
- **It is load-bearing** — its failure is the project's failure, not a degraded feature.
- **A bug is suspected in it**, or a failure here has already been blamed on it.
- **A local mitigation for it already exists** — see below.
- **It is being added for the first time** at T2 or above.

<constraints>

**Read the version actually in use, never the default branch.** The installed package in this
container is the exact code that runs — that is the best source available. A public repository
is read at the matching **tag or commit**, never at `main`, which may be months ahead of what
is installed and describes code nobody is running.

**When a real defect is found, check whether a fix is already coming** before proposing
anything: open issues naming it, merged commits on the default branch since the installed
tag, an open pull request, an unreleased entry in their changelog. **Say what you found and
what you did not** — "no open issue matches" is a finding; "I did not look" is not.

**Then it is the human's decision, not yours.** Put it in Phase 6 List 1 with both
consequences, never as an amendment you apply on your own judgement:

| Option | What it costs |
|---|---|
| **Mitigate locally now** — pin, patch, wrap, or route around | The defect stops mattering today. You now carry a workaround that must be removed when upstream fixes it, and that nobody will remember writing |
| **Wait for the upstream release** | No local debt. The defect keeps biting until it ships, and it may never ship |
| **Replace the dependency** | Ends it permanently. Largest diff, and a new dependency is a new unknown |
| **Accept it** | Free. Record what it does and when it bites, so the next person is not surprised |

**A local mitigation is recorded as a liability, not a fix.** In the decision record, name the
dependency, the version, the defect, what was done locally, and **the condition under which
the local code comes back out** — usually a named upstream release.

**On every re-check, re-examine each recorded mitigation.** Has upstream fixed it? If yes, the
local workaround is now `DRIFT` — it is code guarding against something that no longer exists,
and leaving it is how a codebase accumulates defences nobody can explain. Propose removing it,
with the upstream fix cited. If no, say so and leave it alone; a mitigation re-litigated every
run is as bad as one never revisited.

</constraints>

<constraints>

**A fork carries an upstream, and that is a relationship the rest of this file does not
cover.** Where the repository is a fork, record it and check three things rather than treating
it as an ordinary project:

- **How far it has diverged**, and whether divergence is the point or an accident. A fork that
  exists to add one feature and has drifted across forty files has a maintenance problem
  nobody decided on.
- **Whether upstream is alive**, and whether fixes are being taken. A dead upstream makes the
  fork the real project and changes its tier; a live one makes every local change a future
  merge conflict.
- **Whether anything local should go upstream.** A fix carried privately is a mitigation with
  no removal condition — the same liability as a pinned dependency.

**Never propose re-syncing, rebasing or merging upstream.** That is a judgement about the
project's direction, not its configuration, and it belongs to the human. Record the state and
stop.

</constraints>

### 9. Distribution and packaging

Publish to a registry only when something else consumes it.

**Outbound licence keys on `exposure`, not on owner.**

| Exposure | Licence |
|---|---|
| **never** | A real `LICENSE` with an all-rights-reserved proprietary notice, naming the Phase 3 holder. **Work or personal alike** — an open-source grant on something that will never be published grants rights to nobody and misstates the intent |
| **possible later** | Decide now; it is rank 1. Apache-2.0 if it may be published, proprietary if not |
| **already public, new** | **Apache-2.0** — its patent grant, inbound contribution terms and warranty disclaimer protect the maintainer more than MIT's brevity |
| **already released** | **Locked. Never propose changing it** for released versions |

**Never an implied open-source grant in a manifest or README with no LICENSE file — check
both places.** The copyright holder is the Phase 3 answer, never inferred from the account name.

### 10. Documentation, versioning and handoff

`README.md` always. Decision record at the Phase 1 alias from T1. **Where the project wants
per-decision files rather than one append-only log, use MADR** (Markdown Any Decision
Records, currently 4.x) under `docs/decisions/` as `NNNN-short-title.md` — a published format
with a minimal and a full variant, which is cheaper than inventing a house template and
readable by anyone who has seen one before. The two are alternatives, not a pair: **one
decision record per repository**, at the Phase 1 alias, whichever form it takes. `CHANGELOG.md` and
versioning from T2, **or earlier once a built artifact reaches a person or a machine** — that
clause fires independently of tier. **A tag alone does not fire it.** A source tag for internal
reference is not distribution; a binary, wheel or installer that someone else can run is. Where
it has fired, the changelog is written before the tag rather than backfilled after.

**Version reconciliation:** manifest, tag, changelog head, **and installed distribution
against in-tree**. Zero tags where none can exist is not `DRIFT`.

<constraints>

**A field recording that something was reviewed names what was examined, and never silently
follows a release.** A constant tracking the newest build asserts an approval nobody gave —
**a claim about review converted into a claim about currency.** A live project raised exactly
this as a gap and its upstream refused the change, correctly: the field names the pairing the
record approves, not the newest that exists, and it moves when the record moves rather than
when a release happens. Put the distinction in the docstring at the point of change, because
that is where someone will be tempted to fix the lag.

**This is the as-built bill of materials, and the hardware world codified it first.** The
as-designed, as-built and as-maintained distinction — recording which specific revisions were
actually assembled and verified together, rather than which are current — is standardised in
configuration-management practice. **The approved pair is a two-element as-built record.**

**And the breaking-change test has an older and better name: form, fit and function.** A part
may be revised only if every previous revision is **fully replaceable** by the latest,
wherever it is used; where that fails, it gets a **new part number** rather than a revision.
That is a major version bump, stated decades before semantic versioning, and it is the
cleanest available test for whether a change is breaking: **not whether it looks large, but
whether what depended on the old one can take the new one unchanged.**

**A version that reached the default branch was published, tag or no tag.** Establishing what
versions exist means reading the manifest's history on the default branch, not only the tag
list and the releases page. **Anyone who cloned while a number was on `main` has a tree
declaring it**, and no later renumbering reaches them. A live run found a version that had sat
on the default branch for over eight hours before being replaced by a *lower* one — invisible
in tags, invisible in releases, and the only place the number had ever actually been. The
practical cost was near zero on a private repository with one committer; **the rule is not
about the cost, it is about where you look.** A record whose supporting facts are all about
tags, releases and built binaries has established nothing about the branch, and the next
version has to clear the highest number ever published there or say why it does not.

**The scheme is a recorded decision, not something a reader infers from the numbers.**
Reconciling four version numbers proves they agree with each other; it does not prove anyone
decided what they mean. **A project whose numbers reconcile perfectly and whose scheme was
never chosen is `DRIFT` on this dimension**, because the next person to bump it is guessing,
and the guess is where the reconciliation breaks. One entry in the decision record answers
it: which scheme, what counts as a major change **for this project**, whether pre-release
labels are used, and what leaving one requires.

**The scheme is semantic versioning — `MAJOR.MINOR.PATCH`.** This file does not offer a
choice, and the reason is not that dated schemes are wrong. It is that **a version scheme is
close to a one-way door**, so the cost of getting it wrong is paid later and by someone else,
and an option nobody here will take is weight in a file that has to be read every run.

**Why it is nearly irreversible, which is also why it is worth deciding once and recording:**
a dated version such as `2026.09.17` is a larger number than any `1.2.3` that could follow
it, so a project moving off a dated scheme publishes something that sorts **below** what is
already out. It satisfies none of the ranges a consumer wrote, and no resolver treats it as
newer. The only escape is to jump past the old numbers permanently, leaving a history nobody
can read. **Semantic is where you start if you might ever need the promise**, and external
dependence being *possible* rather than certain is enough: a library that might get
published, a tool a second team might pin, a repository that might acquire a sibling.

**It is also the more widely supported by a wide margin, as a matter of tooling rather than
taste.** Semantic versioning is a specification with native support in every major ecosystem's
resolver, and Go modules require it outright with a `v` prefix on the tag.

**Where an inherited or vendored project already uses a dated scheme, record it and leave it
alone.** It is not a `GAP` and **renumbering an existing version history is never the
amendment** — it breaks every pin and every reference to a release that is already out, to fix
something that costs nothing. Note the scheme in the decision record so the next run does not
raise it again, and apply the rules below to whatever scheme is in place.

**Do not pad the fields, and do not fix their width.** `01.02.003` reads as tidy and breaks
three things at once. **Semantic versioning forbids leading zeros outright**, so it is not a
conforming version and tools are entitled to reject it. **Python packaging normalises it
away** — `01.02.003` becomes `1.2.3` in the installed distribution while the tag keeps the
padding, which manufactures a permanent `DRIFT` on the reconciliation this dimension
performs, on every run, forever. And **a fixed width is a ceiling**: two digits means the
ninety-ninth patch has nowhere to go, and the remedy is renaming every historical tag.

**The one problem padding solves is already solved.** Zero-padding exists so `1.10.0` does
not sort before `1.9.0` under naive string comparison. Every version-aware tool already sorts
semantically, and `git tag --sort=v:refname` does it for tags. **Adopting a non-conforming
scheme to fix a problem only a plain `sort` has is a trade against every tool that reads
versions properly.** Where an artifact genuinely needs lexical sortability — a filename, a
log prefix, an object key — pad *there* and leave the version alone.

**A version makes a stability promise; the tier says who is relying on it. When those
disagree, say so.** This is the finding no published standard will give you, because no
published standard knows the tier:

- **`0.x` at T2 or T3** — the number says anything may change, and something real is already
  depending on it. Either the promise is wrong or the tier is. **Not automatically a `GAP`**:
  a long-lived `0.x` is a legitimate choice, and this file is one. What is missing is the
  statement — say what `0.x` means here and what would earn `1.0`, in the decision record.
- **`1.x` with breaking changes landing in minor bumps** — the promise is being made and
  broken. `DRIFT`, and the evidence is in the changelog rather than in anyone's opinion.
- **Pre-release labels with no graduation condition** — `alpha`, `beta` and `rc` each claim a
  different degree of doneness, and a label nobody can leave is decoration. The finding is
  not that they exist; it is that **nothing states what leaving one requires.** One line:
  *beta ends when the schema stops moving*, *rc ends when no blocker is open for a week*.
- **A pre-release that has outlived its condition** — the condition was met and the label
  stayed. `DRIFT`, and cheap to fix.

**Reaching `1.0` is a promise to consumers and is hard to walk back**, which puts it with the
irreversibility gate rather than with routine bumps: `2.0` is available, but retreating to
`0.x` tells everyone who pinned you that the promise was never real. **At T1 it costs
nothing and settles nothing** — reach it when the interface stops moving, not when the
project feels finished.

**Mechanics are cited, not restated here.** Semantic Versioning defines the fields and the
pre-release grammar, Keep a Changelog defines the sections, Conventional Commits defines the
commit grammar that can derive a bump. **Point at them and record which one this project
follows.** A house paraphrase of a published spec is a second source of truth that will drift
from the first.

</constraints>

Where a production-touching repository at T2+ has no runbook, that ranks `BLOCKER` — the
consequence being that recovery depends entirely on one person's memory at the worst possible
moment. Only after the Phase 1 content search found none.

**Provenance:** a public repository must contain no work-origin code.

**Non-code deliverables** are in scope: tier, secrets, distribution, documentation.

<constraints>

**In greenfield mode Phase 4 generates rather than audits.** Walk the same ten dimensions,
but each one asks *what should exist* instead of *what does*. Every dimension still gets a
status: `N/A` at this tier, or `GAP` for something that will be created — nothing reads `OK`
before it exists.

**Generate in this order.** Structure first, then config, then content. A `pyproject.toml`
naming a package that has no directory is not a project.

1. **Directory skeleton** for the chosen shape, with the source root and test root present.
2. **Manifest and toolchain** — the build file, lockfile, and the tool config the ecosystem
   expects.
3. **One entry point and one passing test**, so the documented commands have something to run.
4. **Hygiene and enforcement** — `.gitignore`, `.gitattributes`, `.editorconfig`, CI, deny rules.
5. **Documents** — `README.md`, `AGENTS.md` with the module map, the decision record, licence.

**The run ends runnable.** Before Phase 5, execute the documented build, test and lint
commands and paste the output. **A greenfield run whose own documented commands do not pass
has not finished** — the point of generating a skeleton is that it works, and a skeleton that
does not build is worse than none because it looks done.

**Generate and validate outside the repository.** This rule and "nothing is written before
approval" would otherwise contradict each other: a build cannot run on files that do not
exist, and creating them breaks the gate. **Build the tree in a scratch location** — its own
git index, its own environment — run every gate there, and let Phase 7 copy in a tree already
known to be green rather than attempt one for the first time. The working tree stays clean
through Phase 6, and `no_writes_proof` concerns the repository, not the container.

</constraints>

```yaml
phase: 4
dimensions:
  - {n: 1, name: stakes, status: GAP, finding: "...", evidence: "...",
     secondary: [], strength: "<... | none>"}
  # ... through n: 10
tally: {BLOCKER: 0, DRIFT: 0, GAP: 0, OVER: 0, MIRROR: 0, UNVERIFIABLE-HERE: 0, OK: 0, N/A: 0}
tally_sum: 10          # MUST equal 10
secondaries: [{n: 0, status: GAP, note: "..."}]
strengths: [{n: 0, note: "..."}]
corrections:           # verdicts from a PRIOR run that this run overturns
  - {prior_run: "<version and date>", prior_claim: "...", actual: "...",
     rule_that_caught_it: "<quoted>", decision_affected: yes | no}
validated: [{rule: "<quoted>", caught: "<what it found>"}]
constrained: [{rule: "<quoted>", stopped: "<what you would have done>"}]
overrides: [{phase: 0, saw: "...", did: "...", why: "..."}]
notes: <... | none>
```

## Phase 5 — Report

```yaml
phase: 5
table: |
  | # | Dimension | Status | Secondary | Strength | One-line finding |
  <ten rows, in dimension order>
blockers: [{n: 0, why_now: "...", interaction: "<how it compounds | none>"}]
over_items: [{n: 0, recipe: "..."}]
fired_triggers: [{trigger: "<quoted>", evidence: "...", recorded_before: yes | no}]
unfired_triggers: [{item: "...", gated_on: "..."}]
notes: <... | none>
```

## Phase 6 — Approval Gate — **WAIT**

<constraints>

**A blank, malformed or unfilled answer at a wait is not an answer, and re-asking is not a
third wait.** The two-wait ceiling counts **gates**, not round trips inside one — a question
asked again because the reply arrived empty is the same gate, still open. A live run received
an option template pasted back with its placeholders unedited, applied the recorded default,
and declined to re-ask on the grounds that it would be a third wait. **That reading is
understandable and wrong**, and it cost the answer four of six live triggers depended on.

**Applying a recorded default and disclosing it is the correct fallback — after asking again
once, not instead of it.** Ask once more, name what the blank costs, and take the default if
the second reply is also empty. **Never guess at the content of a blank answer**, and never
treat an unedited template as agreement with whichever option happens to be listed first.

</constraints>

<constraints>

**HARD STOP. Nothing has been written to the repository and nothing may be.**

<!-- WHY a file, not the reply body: a reply does not survive being carried into another
     session, and the human should never assemble a report by copying blocks out of a
     transcript. Two runs read silence here and did opposite things. -->
<!-- WHY delivery is separate from writing: reports have been written to a container
     scratchpad that dies within the hour. Every run so far attached the file anyway, which
     was the agent being sensible rather than this file requiring it. -->
**Writing the report is not delivering it.** Outside the repository, in an ephemeral
container, means gone within the hour. **Hand the file over in the same turn** — attached, or
its full content in the reply where the tool cannot attach — and say plainly that the path is
temporary. A report that was written and not delivered is the same as no report, and it is the
one artifact with no copy anywhere else.

**Emit the run report as a markdown file outside the repository**, named
`RUN-REPORT-<repo>-<YYYY-MM-DD>.md`, with `lifecycle: transient` and a concrete `expires:`.
The prohibition is on writing **to the repository**.

**Open with a reconciliation header**, so any reader — human or another model — can triage
without reading the body and can diff two runs mechanically:

```yaml
standard: PROJECT-BOOTSTRAP-AND-AUDIT v<metadata.version>
tool: <agent and surface>
repository: <owner/name> @ <commit>
job: <survey | set up | audit | release | prune | validate>
mode: <greenfield | retrofit | audit | recheck>
tier: <T0-T3> (blast radius <B>, audience <A>, basis <current|imminent>)
tally: {BLOCKER: 0, DRIFT: 0, GAP: 0, OVER: 0, MIRROR: 0, UNVERIFIABLE-HERE: 0, OK: 0, N/A: 0}
capabilities_absent: [<what the environment could not do>]
deviations: <count>          # rules not followed as written, each in `overrides`
decisions_open: <count>
sections_read: [...]
sections_skipped: [...]
```

**Deviating is allowed; hiding it is not.** Where the run departed from this file — a rule
that did not fit, a capability that was missing, a judgement the text did not cover — record
it in `overrides` with what was seen, what was done, and why. **A run that deviated and said
so is more useful than one that complied and learned nothing**, because each deviation is a
place the standard was wrong or silent. A reader reconciling two reports works from
`deviations` first.

**Then structure it for two readers, in this order:**

1. **The decisions**, in plain prose a human answers without scrolling — the three lists below.
2. **An appendix holding every emission block so far**, `phase: 0` through `phase: 6`, verbatim.

The human reads the top to answer and forwards the whole file to whoever is reviewing the
standard. **They must not have to copy blocks out of the conversation to do that.**

**Three lists, in this order:**

1. **Decisions only the human can supply**, each with **what happens by default if
   unanswered**, and which amendments each gates.
2. **Numbered amendments**, recommendation **labelled but never pre-selected.**
3. **Actions only the human can take** — server-side or manual. **Each must be achievable
   in a browser.** The maintainer has no local clone, so "run this command on your machine"
   is not an action they can take. A step needing a working copy is either done by a session
   or turned into a `workflow_dispatch` job.

**State at the top of List 2 which amendments are gated, and that "take all recommendations"
does not answer List 1.** A blanket approval otherwise leaves the gated amendments — usually
the blockers — unapplied.

**Gate only what the answer actually blocks.** An amendment whose trigger fired independently
of tier is **not** gated on the tier question. Where an answer changes severity rather than
applicability, use `severity_depends_on`, not `gates`.

**Where an amendment requires editing a file the enforced layer denies, that is a List 1
decision** — show the exact diff and ask once. **Never route around the deny layer**, and
never propose weakening it to make your own work easier.

**Emit what you deliberately did not propose.** A section listing each finding that was
real and was still not raised, with its reason — a fired-but-declined trigger, a plan-gated
item, a churn cost that outweighs the fix, a mitigation re-examined and still load-bearing.
**This is the only visible evidence that the re-check obligations were honoured**, and
without it a run that quietly re-raised a decline looks identical to one that did not.

**Closure rule.** `recommended + optional` must equal the number of amendments.
Recommendation is a third axis and never reduces the severity count.

**Every amendment states both consequences** — what accepting buys, and what declining
leaves exposed or costs later. Where the baseline's opinion is weak, say that too.

Decline must be as easy as accept, and every item carries its trigger.

Then wait. Not "proceeding unless told otherwise." Wait.

**No credential appears in the instrument.** Ask the human to *check* a host, never to tell
you what is on it.

</constraints>

```yaml
phase: 6
gate_artifact: <path outside the repository>
human_decisions: [{id: H1, question: "...", default_if_unanswered: "...", gates: [<ids>]}]
amendments: [{id: A1, dimension: 0, severity: recommended|optional, change: "...",
              evidence: "...", if_accepted: "...", if_declined: "...",
              gates_on: [<H ids | none>], severity_depends_on: [<H ids | none>],
              recommendation: "not pre-selected"}]
human_actions: [{id: X1, action: "...", why_not_agent: "server-side | manual"}]
not_proposed: [{finding: "...", why_not: "...", dimension: 0}]
premise_check: {stated: "<what the prompt claimed>", found: "<what is actually true>",
                evidence: "..."}
counts: {human_decisions: 0, recommended: 0, optional: 0, amendments_total: 0, human_actions: 0}
closure_check: "recommended + optional == amendments_total"
no_writes_proof: |
  $ git status --porcelain
  (empty)
notes: <... | none>
```

## Phase 7 — Apply

Only what was approved, and only what its human decisions unblocked.

<constraints>

**Approval is per mechanism, not per goal — so a substitution returns to the gate.** Where
the approved change turns out to be unimplementable, unsafe, or worse than an alternative
you find while applying it, **that discovery is a new amendment, not a licence to solve the
problem another way.** The gate approved a specific change with a stated consequence; a
different mechanism carries a different consequence, and the human accepted the first one.

**This happened, and disclosure was not enough.** A run approved to narrow a set of overly
broad deny patterns found the narrowing could not be expressed safely — it measured that,
rather than asserting it, against sixty thousand generated filenames — and instead moved the
file out of the denied namespace, leaving the deny rules untouched. **The engineering was
better than what was approved.** It was declared in the commit, the decision record, the
report and the summary, and the run named it as a weakness in its own conformance block. It
was still a change the human did not approve, with a different security posture from the one
they accepted: the broad rules stayed.

**So, when the approved mechanism will not work:**

- **Stop that amendment. Apply the rest.** One blocked amendment does not hold up seven.
- **Report it as unapplied, with the substitute proposed** — what was approved, why it fails,
  what you would do instead, and what that changes about the consequence.
- **Where the human is present, it is one question and they answer it.** Where they are not,
  it waits. **An unapplied amendment with a proposal attached is a good outcome**; an applied
  substitute is a decision taken on their behalf.
- **Never substitute silently, and never treat thorough disclosure as equivalent to
  approval.** Declaring it in four places is what integrity looks like after the fact. It is
  not consent.

**The exception is narrow and does not cover this case:** where the approved change has
already landed and is actively breaking something, fixing forward is an incident, and it is
reported as one.

**Commit by concern, not all at once.** Split when: more than roughly eight amendments; a
tree-wide mechanical change alongside a semantic one; a large documentation restructure; or a
blocker fix that should stay reviewable alone. **A mechanical reformat always gets its own
commit.**

**Verify in a fresh clone wherever an amendment changes what a clone receives** — untracking
a file, adding a seed step, changing bootstrap or a lockfile. Clone to a temporary path,
follow the documented setup, run the gate, **and record what fails without the new step.**

**Say where the work landed.** A branch is not the repository. Record the branch the commits
are on, whether a pull request exists, and what remains for the work to reach the default
branch. **A run that reports success while the default branch is untouched has reported
success about a branch** — green CI on a feature branch is real, and it is not evidence that
anyone cloning the repository gets any of it. Where the work is unmerged, that is a human
action, not a silent omission.

**Nothing exists until it is pushed.** The container is ephemeral: a commit on a branch that
was never pushed dies with the session, and a local branch can exist with no remote
counterpart at all — a fetch has already pruned one whose commits lived only in the container.
**Confirm the branch and its head exist on the remote before reporting done**, by reading the
remote ref rather than the local one. An unpushed branch also makes a remote CI read fail in a
way that looks like a CI problem instead of a missing push.

**Open a pull request rather than merging.** It gives the checks somewhere to run before the
default branch moves and leaves a reviewable diff. **Merging is the human's**, and on a
repository with a sibling contract it is theirs twice over. Where the tool cannot open one,
that is a human action with the branch name and base named explicitly.

**Read the remote CI conclusion after pushing, before reporting done.** Local gates are not
evidence about the remote. A run that reports success without reading the remote conclusion
has not finished — this has already let a default branch sit red for three days through a
tagged release.

</constraints>

```yaml
phase: 7
applied: [<ids>]
declined: [<ids>]
deferred: [{id: <id>, trigger: "..."}]
not_applicable: [{id: <id>, why: "server-side | manual | unavailable on this plan"}]
commits: [{sha: <sha>, scope: "<which ids and why grouped>"}]
fresh_clone_verification: {done: yes | no | n/a, result: "...", without_fix: "..."}
post_apply_commands: [{cmd: "...", result: PASS, collected: <int | n/a>}]
pushed: {branch: <name>, head: <sha>, on_remote: yes | no, proof: "<remote ref read>"}
pull_request: {opened: yes | no | n/a, url: "<url>", base: <branch>, merged: no}
report_delivered: yes | no      # handed over, not merely written
ci_remote_conclusion_after_push: {status: <success|failure|pending>, proof: "..."}
corrections: [{claim: "...", actual: "...", where_corrected: "...", decision_affected: yes|no}]
notes: <... | none>
```

## Phase 8 — Record

Append to the **Phase 1 alias**. **Never create a canonical filename alongside an existing
equivalent.** Append-only: supersede with a pointer. **Dates from the session clock.**

**Record the standard's version** — this file is uploaded per session, so the decision record
is the only persistent trace of which rules produced an audit.

<constraints>

**A Phase 8 entry states the repository as it is at Phase 8, not as Phase 2 found it.**
Phase 7 changes the tree the audit described, so **every observation carried forward into the
decision record is re-checked against the working tree before it becomes a permanent claim.**
The window is not incidental — it is created by this file's own sequencing, and every run
that both audits and applies has it.

**This happened, and the invalidating change was the run's own amendment.** A run applied an
amendment that made a service report its interpreter version, then wrote an entry whose
context asserted that no such reporting existed anywhere in the tree. The amendment's commit
was **already an ancestor** of the commit that wrote the entry — confirmed by
`git merge-base --is-ancestor`, exit 0. The entry was not stale. **It was false on arrival**,
and it was the sentence that made an open question read as unanswerable.

**Re-run the command that established the observation and record what it says now.** Where
the two readings differ, the entry states the Phase 8 reading and the earlier one goes in **the
Conformance Self-Check's `corrections`** — not Phase 7's, which is closed before this phase
runs, and not Phase 4's, which is for a prior run's verdicts. That block is emitted after this
phase in every job, its `prior_run` takes `this run` with the phase, and `rule_that_caught_it`
is this rule. **It is the right home for the general reason rather than the mechanical one:**
that block is for a claim about the *report* being wrong, which is what a re-check discrepancy
is, and its entry stays even when `decision_affected` is `no` — an observation re-checked and
found unchanged needs no entry at all, but one that differed deserves one whether or not it
moved a rating. **Scope is deliberately narrow: absolute negatives, and any claim an applied
amendment could have changed. This is not a re-audit** — anything wider costs attention on
every future run, in every repository, for a narrow failure.

**Nothing downstream catches this class.** A decision record is not executable, no guard
reads one against the code, the entry is append-only by the rule above, and the re-check
obligations exist precisely to make the next run treat the record as settled fact. The
correct-never-silently-edit rule is detection after the fact; **this one is prevention, and
it is cheaper.**

</constraints>

**Record anything that must never be re-proposed**, with the reason, so a later run marks it
`N/A` instead of raising it again.

```markdown
## 2026-09-12 — Configuration audit

- **Standard:** PROJECT-BOOTSTRAP-AND-AUDIT v0.13.0
- **Tier:** T3 (blast radius B3, audience A2) — B3 on the output.
- **Chosen:** secret scan moved to CI only; prose files excluded from the scan.
- **Declined:** pre-commit secret scan — false-trigger cost exceeded its value at one
  maintainer. *Reopen when:* a second person commits.
- **Do not re-propose:** branch protection — unavailable on a private repo on this plan.
- **Local mitigation:** pinned `<dep>==<version>` and wrapped `<call>` because `<defect>`.
  Upstream issue `<ref>`, unreleased as of this run. *Remove when:* `<dep> >= <version>` ships
  with the fix.
- **Deferred:** agent-context split. *Trigger:* a second person commits.
- **Alias:** the decision record here is `docs/decisions.md`.
```

```yaml
phase: 8
recorded_at: <the Phase 1 alias>
entries: [<ids>]
standard_version_recorded: "PROJECT-BOOTSTRAP-AND-AUDIT v0.13.0"
do_not_repropose_added: [<items>]
notes: <... | none>
```

## Phase 9 — Plan Forward

Name the next trigger. Then sequence what is left, **and nothing beyond it.**

<constraints>

**This phase plans the configuration work this run proposed. It never plans the product.**
The boundary is in Scope and it is not a soft one: what the software should do next is the
human's, and a run that drifts into it has exceeded a standard's authority and will be
believed anyway, which is the danger.

**Sequence by dependency, not by severity.** The ranking in Phase 5 sorts consequences; it is
not an order of work, and applying it as one produces a plan that does the frightening thing
first and then finds it needed something else done before it. Three orderings that actually
hold:

- **Anything that changes what a fresh clone receives goes first** — a lockfile, a bootstrap
  step, an untracking with a seed. Everything after it is verified against the new baseline
  rather than the old one.
- **One concern per change, and the reason is measured rather than aesthetic.** A study of
  1.5 million review comments across five projects found **the usefulness of review comments
  falls as the number of files in a change rises**, with build and configuration files
  generating the least useful comments of all — which is precisely what this file's
  amendments touch. A large mixed commit is not merely harder to read; it is measurably
  less likely to be reviewed usefully, by anyone, including its author.
- **A gate goes in before the thing it gates.** Installing a secret scanner after the commit
  that would have tripped it is a scanner that has still never been shown to detect.
- **Mechanical sweeps go last, alone.** A tree-wide reformat before the semantic work buries
  it; after it, the diff is reviewable.

**A milestone is a state the repository can be in, not a list of tasks.** Name it by what
becomes true — *"a clone builds and tests green with no undocumented step"*, *"no credential
can reach the remote unnoticed"* — and give it a **verification that is a command, not an
inspection.** A milestone whose done-condition cannot be checked by running something is a
wish with a name. Three at most. **Where one amendment is the whole milestone, say so rather
than inventing companions to fill it out.**

**Where the plan lives is a decision, and the default is not a file.** Issues and milestones
on the hosting platform are browser-native, need no clone, survive the session, and are
already where the work happens. **A tracked markdown roadmap competes with them and loses
slowly** — it drifts, nothing fails when it does, and it becomes the abandoned tracker the
file-governance list already forbids. So:

| Where | When it is right |
|---|---|
| **Platform issues and milestones** | The default. Always available in a browser, always current because closing the work closes the record |
| **A short `ROADMAP.md`** | Only where it is updated in the same change as the work, and only where the repository has a reason to carry its plan publicly |
| **The decision record** | Where the item is a decision rather than a task — that is Phase 8, and it is already written |
| **A new planning file** | Never. This is the `PROGRESS.md` case under another name |

**Creating the issues is a human action unless the tool can do it**, and either way each one
carries the amendment id it came from so the next run can tell what was already raised.

</constraints>

**Then finish the run report.** Append the `phase: 7`, `phase: 8` and `phase: 9` blocks to the
same file from Phase 6 — do not start a second one — and replace its decisions section with a
short outcome summary: what was applied, declined, deferred, what remains for the human, and
the CI conclusion after the push. **Say where the file is and that it is ready to hand on.**

```yaml
phase: 9
next_trigger: <the event that should cause the next run>
outstanding_human_actions: [<X ids still undone>]
sequence: [{step: 1, ids: [<amendment or action ids>], why_here: "<what it unblocks>"}]
milestones: [{name: "<the state that becomes true>", ids: [<ids>],
              verified_by: "<the command that proves it>", done: yes | no}]
plan_home: platform issues | ROADMAP.md | decision record | none needed
plan_home_why: <one line; required whenever it is not platform issues>
notes: <... | none>
```

---

# Conformance Self-Check

**Emit this at the end of every run, after the last phase block, whatever the job was.**

<constraints>

**This exists because the same file is run on different models, and they fail differently.** A
report that looks complete tells you nothing about whether the rules were followed; this block
makes the common failures visible in one place, cheaply, without a second reader.

**Answer from what you actually did, not from what the file says to do.** A `yes` that means "the
instruction was there" rather than "I did it" makes this block worse than absent — it
manufactures assurance. **Where the honest answer is `no`, that is a useful run**, and the reason
belongs beside it.

**Never pre-fill this from the template.** Each line is checked against the run that just
happened.

</constraints>

```yaml
conformance:
  standard_version: "<metadata.version, read from the frontmatter>"
  job: <survey | set up | audit | release | prune | validate>
  sections_read: [<by name>]
  sections_skipped: [<by name>]

  # Structure
  ten_statuses_emitted: yes | no        # exactly ten, numbered 1-10
  tally_sums_to_ten: yes | no
  new_vocabulary_coined: no | "<what was invented, if any>"
  fields_added_beyond_schema: no | "<which>"

  # Gates
  waits_observed: <int>                 # 2 on a full run OR an audit stopping at the gate;
                                        # 1 on a survey. Count a wait when you STOP at it —
                                        # arriving at Phase 6 and stopping is observing it,
                                        # not skipping it. Two runs disagreed on this.
  wrote_before_approval: no | "<what, and why>"

  # Evidence
  proof_fields_hold_literal_output: yes | no | n/a
  unverified_facts_relied_on: [<any dated fact used without checking it>]
  premise_verified: yes | no | n/a      # a claim in the prompt was reproduced, not assumed

  # Posture
  amendments_pre_selected: no | yes
  both_consequences_on_every_amendment: yes | no
  actions_requiring_a_local_clone: <int>   # must be 0
  declines_reproposed_without_a_fired_trigger: <int>   # must be 0

  # Delivery
  report_written: <path>
  report_handed_over: yes | no          # attached or reproduced in the reply, this turn

  deviations: <int>                     # each one present in `overrides`
  honest_summary: "<one sentence: where this run was weakest>"

  # Optional, and the only part of this file that reports back on the file itself.
  # Omit the key entirely rather than emitting it empty.
validated:
  - {rule: "<the rule, quoted from this standard>",
     caught: "<what it found in this repository that reading would not have>"}
constrained:
  - {rule: "<the rule, quoted from this standard>",
     stopped: "<what you were about to do, and did not>"}
corrections:
  - prior_run: "<standard version and date, or 'this run' with the phase>"
    prior_claim: "<what was asserted, quoted>"
    actual: "<what is true, and the evidence>"
    rule_that_caught_it: "<the rule, or a gap where none exists>"
    decision_affected: yes | no
```

## The two optional blocks, and why they exist

<constraints>

**`validated` is how this file learns which of its rules earn their place.** Every rule here
was added because something went wrong once, and **nothing currently records whether a rule
has ever caught anything since.** A rule that catches nothing across many runs is `OVER` by
this file's own logic and should come out — but that judgement needs evidence, and this block
is the only place it accumulates. Quote the rule and say what it found **that reading the
repository would not have.** Three or four entries, not a transcript; a run that lists every
rule it followed has recorded compliance rather than value.

**`constrained` exists because `validated` alone would get the pruning exactly wrong.**
Sixteen `validated` entries across three live runs credited execution rules almost without
exception — and that is not because the other rules are worthless, it is because **the
instrument can only see rules that catch.** Every posture rule constrains instead of
detecting: do not pre-select an amendment, both consequences on every one, two waits, never
substitute at apply time, re-ask a blank rather than defaulting. **None of them can ever
appear in `validated`, and they are the rules that make the output trustworthy.** Pruning on
detection alone would keep every rule that finds bugs and delete every rule that keeps a run
honest.

**So record what a rule stopped you doing.** Live runs have produced these already, in prose
where nothing could count them: re-asking a blank answer instead of taking the default,
refusing to infer an approval from detail the human had written out but not listed, and —
after a force-push was denied — verifying the branch relationship rather than retrying the
command. **The moment worth recording is the one where you were about to do something and a
rule stopped you**, which is invisible in any output that only reports what happened.

**`corrections` is for a claim this run or an earlier record got wrong.** Not a finding about
the repository — a finding about the report. It exists because a withdrawn or mistaken claim
otherwise vanishes silently, and a decision record that quietly overwrites its own history is
the thing append-only was meant to prevent. **The entry stays even when `decision_affected`
is `no`**, because an overconfident claim that changed no rating still misleads the next run
that reads it. Where no rule caught the error, say so in `rule_that_caught_it` — a gap named
is the most useful thing a run can send back.

**Emitting either of these is a schema addition, so `fields_added_beyond_schema` says `yes`
and names them.** A run that adds a block and reports no additions has contradicted itself in
the one field that exists to catch that, which a live run did.

</constraints>

## What a failing line means

| Line | If it comes back wrong |
|---|---|
| `tally_sums_to_ten` | Phase 4 did not finish. Recount before emitting anything else — this has been wrong twice, both times by inventing a combined status for a dimension that was partly fine |
| `new_vocabulary_coined` | The vocabularies are closed. Use `secondary`, `strength` or `notes` and re-emit |
| `waits_observed` | Fewer than two on a full run means a gate was skipped, and a gate skipped is approval assumed. More than two means waits were invented, which costs the human round trips the file could have answered |
| `actions_requiring_a_local_clone` | Anything above zero is unusable by a maintainer who has none. Rewrite each as a browser action or a dispatch job |
| `declines_reproposed_without_a_fired_trigger` | The re-check obligations were not honoured, and the decision record is being ignored. This is the failure that makes people stop reading the gate |
| `report_handed_over` | A report written to an ephemeral container and not handed over is the same as no report, and it is the one artifact with no copy anywhere else |
| `unverified_facts_relied_on` | Not a failure by itself. **A non-empty list with no matching `UNVERIFIABLE-HERE` in the findings is** — it means a dated fact was used as though it had been checked |

## Running this on a model that is not the one it was written against

<constraints>

**Nothing in this file requires a particular model or tool.** It names Claude Code paths because
a command has to be concrete, and *Any Agent, Any Tool* maps every one of them. Where a path
does not exist for the tool in use, substitute and record the substitution as an override.

**Three failure modes show up specifically when the model changes**, and they are worth watching
for rather than discovering in the output:

- **Compliance theatre.** The schema is filled, every field is populated, and the content is
  generated rather than observed. **The tell is `_proof` fields holding summaries** — "verified",
  "command ran successfully", "output as expected" — instead of literal output. A proof field
  that has been paraphrased is a fabrication with good manners.
- **Instruction decay across a long run.** Adherence may drop as the session lengthens — one
  study found about 5.6% lower odds of compliance per additional function generated, though as
  an exploratory, non-monotonic finding — which is why there are gates rather than a single
  approval at the end, and why this block sits at the very end where any drop is worst. **A
  run that was careful in Phase 2 and loose in Phase 7 is the normal shape of this failure**,
  not an unusual one.
- **Helpful ordering.** Presenting amendments with a recommendation already selected, or
  proceeding past a wait because nothing seemed to be blocking. **Both read as service and are
  the posture this file exists to prevent.**

**Where a model cannot do something this file asks for, say so in `degraded` at Phase 0 and in
`deviations` here.** A run that names its own limits is more useful than one that works around
them silently, because the workaround is invisible and the limit is not.

</constraints>

---

## Proposing a change to this standard

**When a run finds this standard wrong, that is a finding like any other and it goes to the
gate.** Not a note in the report, not a silent workaround, and never an edit the run makes
itself.

**What qualifies.** A rule that fired on something it should not have. A rule that could not
fire because the environment cannot reach what it names. A dated fact that no longer holds. A
definition two runs read differently. **A gap where you did the right thing and no rule told
you to** — that is the most valuable kind and the easiest to leave unsaid.

**How it arrives.** As a numbered amendment in the `standard` class, carrying:

```yaml
- id: S1
  class: standard                 # distinct from repository amendments
  target: <section name in this file>
  rule: "<the rule, quoted, or 'none — this is a gap'>"
  evidence: "<what happened in this run, with literal output>"
  proposed: "<the replacement wording, or the new rule>"
  if_accepted: "<what changes for future runs>"
  if_declined: "<what stays wrong, and what it costs>"
```

<constraints>

**Two things make this safe rather than a slow drift, and both are absolute.**

**It never edits itself.** A run proposes; a human approves; the change is made to this file by
whoever maintains it, and reaches repositories the next time it is handed to one. **A standard that rewrites its own rules
mid-run has changed what every future session believes, on the authority of one session that
will not be there to live with it** — and self-written instructions are the measured *weaker*
case, not the stronger one.

**Evidence is required, and one run is thin evidence.** A proposal without literal output from
this run is an opinion about wording. A single run disagreeing with a rule is a data point; the
same disagreement twice, in different repositories, is a defect. **Say which this is.** The
`validated` block is the other half of the same instrument: it records rules that *earned* their
place, and a rule that catches nothing across many runs is `OVER` by this file's own logic.

**Do not propose a rule whose evidence is that it would have been convenient.** Every rule here
costs attention on every future run, in every repository, forever.

</constraints>

---

# Choosing a Language and Runtime

**Read this in greenfield mode, or when the language itself is the finding. Skip it otherwise —
on an existing repository the language is settled and re-opening it is not an audit.**

Rank 5 of the irreversibility gate is language and runtime. It sits at rank 5 rather than rank 1
because clean module boundaries contain it — but *contained* is not *cheap*, and it is the only
decision on that list that every other file in the repository is written in.

<constraints>

**Recommend, with the trade. Never decide.** This section produces a recommendation and a
runner-up for the human, in Phase 3, alongside what each costs. A run that picks a language and
proceeds has made the project's least reversible decision on its own judgement, in a session
that will not be there to live with it.

**Eliminate before you prefer.** The first two criteria below are constraints and remove options
outright; the rest only break a tie. Reversing that order is how a project ends up in a language
that cannot reach the thing it exists to talk to.

</constraints>

## The order the questions go in

**1. Where does it run, and what is installed there?**

The hard constraint, and the one most often skipped because it feels obvious. A scheduled job on
a server someone else administers can use what that server has. A script a colleague
double-clicks on Windows cannot assume a runtime was installed for it. A tool that must run
inside a CI container can use whatever the image has. **Ask what is already on the target before
asking what would be nice**, because "install a runtime first" is a deployment requirement that
outlives every other argument in this section.

**2. What must it talk to, and does a maintained library exist?**

The second hard constraint. An ERP's REST API, a vendor SDK, a database driver, a file format, a
hardware interface. **Where exactly one language has a maintained client for the thing this
project exists to integrate with, the decision is already made** and the rest of this section is
ceremony. Where none does, that is a finding of its own: the project is writing a client, and
that is a larger commitment than the language choice.

**3. How does it have to ship?**

A single file a user runs with nothing installed points at a compiled language. A package
installed by a team that already has the runtime does not. Something that must run in a browser
is not a choice at all. **Packaging is where a language choice becomes visible to whoever is not
you** — a script that needs a virtual environment, a runtime and a `PATH` entry has moved its
cost onto the person running it.

**4. Who maintains it after this?**

For one maintainer this outranks nearly everything in the tie-break. A language you write
fluently produces code you can fix at speed under pressure; one you are learning produces a
project that stalls the first time it breaks and you are busy. **Say this plainly in the
recommendation rather than dressing it as a technical argument** — it is a legitimate reason and
disguising it makes the record useless later.

**5. Longevity and the cost of being wrong.**

How long does this need to run, and what does replacing it cost? A script with a three-month
life can be written in whatever is fastest to write. Something that will still be running in
five years earns a conservative choice with a long support horizon and a large hiring pool.

## What does not decide it

**Benchmarks**, unless the project is actually performance-bound and you have measured which
part. **Popularity and trend**, which describe the industry rather than this project.
**Novelty** — a project is not the place to learn a language on a deadline, though it is an
excellent place to learn one without a deadline, and saying which this is costs one sentence.
**Elegance**, which is real and is a tie-break, not a constraint.

<constraints>

**Every additional language in a repository multiplies the configuration, permanently.** Another
manifest, another lockfile, another install mode that must fail on drift, another set of CI
gates, another rule file, another toolchain to keep current, another ecosystem whose defects
reach you. **Two languages is a considered decision; three is usually an accident** — a helper
script written in whatever was convenient, then a second, and now the repository has a Python
toolchain maintained for eighty lines of glue.

**The test for a second language: would you accept its full configuration cost for this code
alone?** If the honest answer is no, it belongs in the language already present, or in a
separate repository with its own tier. **Record the answer either way** — a polyglot repository
that decided to be one is fine; one that drifted into it is dimension 2 `OVER`.

</constraints>

## Defaults, and when to leave them

**These are starting points for this maintainer's environment, not rankings.** Each is a
recommendation the criteria above can override, and each states what usually beats it.

| If the project is | Start from | What beats it |
|---|---|---|
| **Windows host, Active Directory, Office, Exchange, or anything with an existing cmdlet** | **PowerShell 7.x** | Nothing, usually — a maintained cmdlet is criterion 2 answering itself. Move only when the work is data-shaped rather than administration-shaped |
| **ERP or REST integration, data transformation, reporting, anything numeric or tabular** | **Python** | A vendor SDK that exists only for another language |
| **A desktop application or a Windows service needing .NET libraries** | **C#** | Nothing on Windows. On Linux, ask criterion 1 again |
| **Anything that runs in a browser** | **TypeScript** | Nothing. It is not a choice |
| **A single-binary CLI a colleague runs with nothing installed** | **Go** | **Rust** where the work is systems-shaped, or where correctness matters more than compile-time familiarity |
| **Glue between two commands, under ~100 lines** | **Shell** | **Python, the moment it needs an array, a conditional chain, or error handling** — the rewrite always costs more later than starting there would have |
| **Extending something that exists** | **Whatever it is already written in** | Effectively nothing. A second language inside an existing project needs the polyglot test above |
| **Performance-critical native work, or a C library binding** | **C with meson**, or **Rust** | Measure first. This row is chosen far more often than it is warranted |

**Where none of these fits, follow the ecosystem the problem lives in** and name the convention
you followed and where it came from, so a later run can check it rather than guess. **Never
invent a house convention for a language that already has one.**

## Recording it

The Phase 3 `inception.language` block carries the chosen language, the runner-up, the reason,
and who decided. **The runner-up matters as much as the choice** — it is the only record that a
comparison happened, and the first thing worth reading when the choice turns out to have been
wrong. Where the language was settled before this run, `decided_by: already settled` and no
argument is made for or against it.

---

# Choosing the Shape

**Read this in greenfield mode, or when structure is a finding.**

**Ask the shape; do not infer it.** A web service, a CLI and a scheduled job are three different
layouts in the same language, and getting it wrong costs a restructure later.

## What invokes it decides it

| What starts the program | Shape | The thing that goes wrong when this is mismatched |
|---|---|---|
| A person at a terminal | **CLI** | Arguments arrive through environment variables and nothing is discoverable |
| A schedule or a queue | **Scheduled job** | It is not idempotent, and the second run corrupts what the first wrote |
| An HTTP request | **Web service** | Business logic is written inside request handlers and cannot be tested or reused |
| Another program, in-process | **Library** | An entry point, a `main`, and a CLI accrete around it until consumers depend on all three |
| A person, at a window | **Desktop application** | Logic lives in event handlers and the application cannot be driven headlessly |

**Two shapes in one repository is normal and fine** — a library with a CLI over it, a service
with a job that shares its models. **What is not fine is two entry points into the same
behaviour**, which diverge quietly. One shape owns the logic; the others call it.

## The decisions inside the shape

**What it keeps is close to a one-way door.** Code is rewritable; data already written is not.
Ranked by how hard the reversal is:

| Choice | Reversal cost |
|---|---|
| **Nothing persistent** | Free. Prefer it — a stateless tool is the cheapest thing in this table to operate, back up, and reason about |
| **Files on disk** | Low, while the format is yours and the volume is small |
| **A database you own** | Moderate for the engine, **high for the schema semantics** — a column whose meaning changed is not migratable by a script |
| **Someone else's system of record** | Not yours to reverse. It becomes a cross-repository contract, and that section applies |

**Start with one deployable unit.** Splitting a working program into services is reversible with
effort; recombining services into a program rarely happens, because by then the split has been
built into the deployment, the monitoring and the team's habits. **At one maintainer there is no
argument for more than one deployable unit that is not about scale nobody has yet.** Where the
project genuinely has two, say what forced it.

**Keep the boundary between logic and I/O, whatever the shape.** Business logic that imports no
framework can be called from a test, a CLI and a job without a web request existing — that is
the wiring rule below, and it is also what makes the shape decision cheap to revisit. **A
project that got the shape wrong but kept the boundary has a day's work; one that did not has a
rewrite.**

**Where a diagram would help, use an existing notation.** The C4 model's context and container
views cover nearly everything a repository of this size needs, and a decision record is where
the reasoning goes. **Do not invent a diagram format**, and do not commit a diagram that has to
be hand-updated when the code moves — it will not be.

---

# Project Shapes and Layout

**The layouts themselves. Choosing between them is the section above.**

## Project shapes

| Shape | Source root | Tests | Entry point |
|---|---|---|---|
| **Python — web service** | `src/<pkg>/` with `api/`, `services/`, `models/`, `config.py` | `tests/` + `conftest.py` | `app.py` exposing `create_app()` |
| **Python — CLI** | `src/<pkg>/` with `cli.py`, `core/` | `tests/` | `__main__.py`, thin; `[project.scripts]` in the manifest |
| **Python — scheduled job** | `src/<pkg>/` with `job.py`, `steps/`, `config.py` | `tests/` | one idempotent `job.py` entry, re-runnable without harm |
| **PowerShell module** | `<ModuleName>/` with `Public/`, `Private/` | `tests/<Name>.Tests.ps1` (Pester) | `.psd1` manifest + `.psm1` loader |
| **C# application** | `src/<Project>/` | `tests/<Project>.Tests/` | `Program.cs`; `.sln` at root, `Directory.Build.props` for shared properties |
| **JS / TS** | `src/` | `tests/` or co-located `*.test.ts` | `src/index.ts`; `package.json` + `tsconfig.json` |
| **C — meson** | `src/` with a `meson.build` per directory; `include/` for public headers | `tests/` with its own `meson.build` | root `meson.build` calling `project()` then `subdir()` |
| **Shell tool** | `bin/<name>` executable, no extension, with a shebang; `lib/*.sh` for sourced helpers | `tests/` (bats or shunit2) | the `bin/` script |

**A shape not in this table follows its own ecosystem's convention** — the layout a newcomer
to that language would expect, not one invented here. Name the convention you followed and
where it came from, so a later run can check it rather than guess. The principle holds
regardless: one source root, one test root, and a manifest that names what actually exists.

**Python source layout.** Use `src/` rather than a top-level package. It stops the tests
importing the working copy instead of the installed distribution, which is the shadowing trap
version reconciliation already checks for.

**PowerShell.** One file per exported function in `Public/`, **filename matching the function
name**; helpers in `Private/`; exports listed explicitly in `FunctionsToExport` rather than `*`.

**C with meson.** Every directory that builds something carries its own `meson.build`, and the
root file only calls `project()` and `subdir()`. Build options go in a file, never hardcoded —
**`meson.options` is the current filename and `meson_options.txt` is the older one**, which
still works, so finding the old name is not a finding on its own.

## Auxiliary files — placement, not layout

These are not project shapes. They live inside one, and the only question is where.

| Type | Home | Note |
|---|---|---|
| HTML templates | `src/<pkg>/web/templates/` | Beside the code that renders them, not at root |
| CSS and static assets | `src/<pkg>/web/static/` | Same |
| Shell scripts | `scripts/` | One verb per script, or one script with subcommands |
| Batch launchers | repository root **only if a human double-clicks it**, else `scripts/` | The one auxiliary type with a legitimate claim to root |
| SQL | `sql/` or `src/<pkg>/queries/` | Never inline in application code where it can drift unreviewed |
| Build and packaging specs | `packaging/` | Spec files, installers, manifests |

**Declare EOL rules for every auxiliary type in `.gitattributes`** — `*.ps1` and `*.bat` want
`crlf`, `*.sh` wants `lf`. A batch file with `lf` endings and a shell script with `crlf` both
fail in ways that look like anything but line endings.

## Wiring

- **A web service composes in one factory function**, not at import time. Routes are declared
  per module and mounted by the factory; the factory is what tests instantiate.
- **Business logic imports no framework.** `services/` should be callable from a test, a CLI
  and a job without a web request existing.
- **Configuration is read once**, in one module, from environment variables, and passed down.
  A module that reads its own environment cannot be tested without setting it.
- **One entry point per shape.** Two ways to start the same program diverge.

---

# Starter File Contents

**Read this in greenfield mode, or when a file named here is missing or being rewritten.**

<constraints>

**These are starting points, not a schema.** Every one of them is meant to be edited down to the
project in front of you — a template pasted whole and left generic is worse than nothing,
because it reads as considered when it was not.

**Why literal content exists here at all.** An agent asked to "generate an `AGENTS.md`" writes a
different one every run, which makes two runs on an unchanged repository disagree, and the
determinism test in **Validating a Change to This Standard** is what that breaks. **A fixed starting point makes
the diff meaningful.** Only the files where that mattered are here; everything else is described
by rule and generated to fit.

**Delete what does not apply rather than keeping it as a placeholder.** A heading with nothing
under it is a promise the file does not keep, and the next reader cannot tell whether it is
empty because nothing applies or because nobody filled it in.

</constraints>

## `AGENTS.md` — the canonical context file

**Target: under 150 lines. Hard ceiling 300, and past 32 KiB Codex stops reading it
(`project_doc_max_bytes`).** Everything that can live in a linked document should.

```markdown
# <project name>

<One or two sentences: what this does and who runs it.>

## Commands

- Install: <exact command>
- Test: <exact command>
- Lint: <exact command>
- Format: <exact command>
- Type check: <exact command>
- Run: <exact command>

## Layout

- `src/<pkg>/` — <what lives here>
- `tests/` — <what lives here>
- `scripts/` — <what lives here>
- `docs/` — <what lives here>

## Conventions

- <A convention a reader could not infer from the code.>
- <Another. Three to six of these, not twenty.>

## Invariants

- <Something that must stay true, and what breaks if it does not.>

## What not to do here

- <A specific action that has caused a problem before.>
```

**The Commands section is the part that measurably gets used** — write the exact command
including its flags, not a description of it. **The Conventions section is where bloat starts:**
anything a reader could work out by opening two files does not belong, and a convention that a
formatter or linter already enforces belongs in that tool's config, not in prose.

## `CLAUDE.md` — the shim

One line. **It is a shim because Claude Code reads `AGENTS.md` natively only in some sessions**
(the conditions are in *Facts with an Expiry Date*), **and the import works in all of them without
loading the file twice.** It becomes `OVER` only if native reading stops having conditions.

```markdown
@AGENTS.md
```

**Anything genuinely Claude-specific goes below that line and nowhere else.** A shim that has
grown past about thirty lines has stopped being a shim, and the content in it is usually
portable and belongs upstream in `AGENTS.md`.

## `.editorconfig`

A default, not a choice. Extend per language only where the ecosystem disagrees with the base.

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.{js,jsx,ts,tsx,json,yml,yaml,css,html}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[*.{bat,cmd,ps1}]
end_of_line = crlf

[Makefile]
indent_style = tab
```

**`trim_trailing_whitespace = false` for markdown is deliberate** — two trailing spaces are a
line break in markdown, and trimming them silently changes rendered output.

## `.gitattributes`

**The highest-value file in this list for a repository worked on from both Linux and Windows**,
and the one whose absence produces failures that look like anything but line endings. A shell
script with CRLF fails with a message naming the interpreter; a batch file with LF fails
stranger than that.

```gitattributes
* text=auto

*.sh      text eol=lf
*.bash    text eol=lf
*.py      text eol=lf
*.yml     text eol=lf
*.yaml    text eol=lf

*.ps1     text eol=crlf
*.psm1    text eol=crlf
*.psd1    text eol=crlf
*.bat     text eol=crlf
*.cmd     text eol=crlf

*.png     binary
*.jpg     binary
*.gif     binary
*.ico     binary
*.pdf     binary
*.zip     binary
*.xlsx    binary
```

**Adding this to an existing repository does nothing on its own** — files already committed keep
their stored endings. The normalisation step is a separate commit that re-stages everything, and
it is a mechanical diff, so it gets that commit to itself under the review rules.

**Where PowerShell files are UTF-16**, add `working-tree-encoding=UTF-16LE` to those lines;
without it they are stored as binary and never diff.

## `.claude/settings.json` — the enforced layer

**A baseline, and every rule in it is declinable with a stated consequence.** Deny beats allow,
rules merge across scopes, and none of this constrains a script the agent writes and runs.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "deny": [
      "Read(.env*)",
      "Read(**/*.pem)",
      "Read(**/*.key)",
      "Bash(cat .env*)",
      "Bash(rm -rf *)",
      "Bash(git push --force*)",
      "Bash(git push -f*)"
    ],
    "allow": []
  }
}
```

**Read the deny list as pairs, not as items.** Each secret has a file rule and a shell rule
because they are different access paths to the same bytes, and a rule covering one leaves the
other open. **Extend the pattern for every path that must not be reached**, and where the
project states a domain invariant an agent could violate, this is where it becomes real rather
than advisory.

**Verify each rule fires before recording the dimension `OK`.** A matcher that has never been
tested has not been shown to work, and a deny list that silently matches nothing is the worst
outcome available — it reads as protection.

**The deny stays broad, and the example file moves out of its way. Name it `env.example`,
without the leading dot.** This looks like a triviality and it resolves a real conflict: a
`.env*` glob is the right shape for secrets, and it **blocks `.env.example` — the one file in
that family that is committed, carries no secret, and which dimension 7 requires reading to
check its placeholder convention.** A live audit hit exactly that: the deny fired twice, the
session correctly refused to route around it, and the check went back as a human action.

**Two fixes were tried before this one, and both were worse.** Excluding the example inside
the glob is unauditable — globs have no negation, so it takes around fifteen patterns, and a
run measured against sixty thousand generated filenames that the short forms still let
`.env.exported` and `.env.example.bak` through. **A security rule nobody can audit is not an
improvement on one slightly too wide.** Naming each secret-bearing file instead — which an
earlier version of this template did — is auditable but **fails open**: the first
`.env.staging` anyone adds is unprotected, and nothing announces it.

**Moving the example has neither failure.** The glob stays broad, so a new secret file is
covered the moment it appears; the example is readable, so the audit can discharge its check;
and there is no list to maintain. `env.example` is a less common spelling than `.env.example`,
which is the whole cost — **say so in the README, since a contributor will look for the
dotted name.** Where the dotted name must stay for an external reason, that is a real
constraint, and the check it blocks becomes a standing human action rather than a rule to
weaken.

**The general rule outlives all three attempts: a deny pattern that covers a file the audit is
required to read has not hardened the repository, it has blinded the audit.** Deny beats allow
at every scope, so an allow cannot rescue it — **either the pattern narrows or the file moves,
and moving the file is usually cheaper and always more auditable.** When a rule blocks a
check, that is a finding on this dimension, and the amendment is to narrow the rule or move
the file, **never to widen the session's permissions.**

## `.github/workflows/ci.yml` — the gate that actually enforces

**This is where the guarantee lives** when there is no local clone: it runs on every push
regardless of which machine or container the push came from. Substitute the commands from
dimension 2's table for the ecosystem.

```yaml
name: CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Set up toolchain
        run: echo "substitute the setup action for this ecosystem"

      - name: Install from the lockfile, failing on drift
        run: echo "substitute the frozen install from dimension 2"

      - name: Format check
        run: echo "substitute"

      - name: Lint
        run: echo "substitute"

      - name: Type check
        run: echo "substitute, or delete this step"

      - name: Test
        run: echo "substitute"

      - name: Guard the collection count
        run: |
          BASELINE=$(cat .test-baseline)
          ACTUAL=$(pytest --collect-only -q 2>/dev/null | tail -1 | grep -oE '^[0-9]+')
          echo "collected ${ACTUAL}, baseline ${BASELINE}"
          if [ -z "$ACTUAL" ] || [ "$ACTUAL" -lt "$BASELINE" ]; then
            echo "::error::collection fell below baseline"; exit 1
          fi
```

**Four things about this file are load-bearing and are not style:**

- **`permissions: contents: read`** at the top. The default token is broader than a test run
  needs, and narrowing it is free. **Every workflow, not most of them** — a live run found a
  repository with a custom gate enforcing exactly this, and the one workflow missing the
  block was the CI workflow itself, because the gate only inspected workflows that call `gh`.
- **A gate must not claim more coverage in its failure message than it actually checks.**
  That same gate printed that the default token scope "must not be relied on here" — a
  statement about the repository — while enforcing it over a subset. **Anyone reading the
  message reasonably concludes the rule is enforced everywhere**, which is worse than no gate,
  because a missing gate invites a check and a lying one forecloses it. Read what each gate
  *says* against what it *tests*; where they differ, either the scope widens or the message
  narrows, and **narrowing the message is the honest cheap fix.**
- **The install step fails on lockfile drift** rather than resolving fresh. A CI that installs
  latest is testing a tree nobody has.
- **Format and lint are separate steps** from test, so a failure names which one.
- **The collection guard compares against a recorded baseline**, not against zero, and it is
  written out here rather than described because **describing it did not work.** A live audit
  found a guard built from this file's prose that fired only at zero: a scratch copy with one
  module stopped from collecting went 11 tests to 7 — **a quarter of the suite gone, guard
  green, exit 0.** Substitute the collection command for the ecosystem, keep the comparison.
  The baseline lives in a committed file so raising it is a reviewable diff, and an empty
  `ACTUAL` fails rather than passing, because a collection command that prints nothing has
  not reported zero tests — it has failed to run.
- **Make the gate's absence legible.** A gate that skips silently is indistinguishable from
  one that passed, and the reader has no way to tell them apart afterwards. **Write it so
  that not running says so by name** — a skip reason naming the check, a printed marker
  before the assertion, a line in the summary. A live run could confirm its collection guard
  had actually executed only because the guard emits two named skip lines when it does not,
  and neither appeared. **That property is worth more than the assertion itself**, because an
  assertion that never runs is a gate in name only, and this is the one thing about a gate
  worth telling a future reader.

**A secret-scan step belongs here too**, per the enforcement placement table — in CI always,
never as a client-side hook where no persistent local environment exists.

**Whatever the gate downloads and runs, verify before running it — and start with the
security tooling.** A workflow that fetches a binary over the network and executes it has
made whoever serves that URL a maintainer of this repository, with the workflow's token. A
live run found both workflows in a repository doing exactly that for their secret scanner:
**the control that is the primary credential defence, installed with no integrity check at
all.** Pin the version — that repository did — and then verify what arrives: a published
checksum or signature, or an action that does it, or a container digest. **A pinned version
with no checksum pins what you asked for, not what you got.** This is the highest-leverage
instance of a general rule, so where a run finds it in the scanner job, say that plainly
rather than filing it beside ordinary dependency hygiene.

## The decision record

One file, at the Phase 1 alias, append-only. **Newest entry at the top**, so the current state is
the first thing read.

```markdown
# Decisions

Append-only. Supersede by adding a new entry that points at the old one; never edit history.

## <YYYY-MM-DD> — <what this entry is about>

- **Standard:** PROJECT-BOOTSTRAP-AND-AUDIT v<version>
- **Tier:** T<n> (blast radius B<n>, audience A<n>) — <the reason, where it is not obvious>
- **Chosen:** <what was decided, and the reason>
- **Declined:** <what was turned down>. *Reopen when:* <the trigger>
- **Deferred:** <what is waiting>. *Trigger:* <the condition>
- **Do not re-propose:** <settled items>, because <reason>
- **Local mitigation:** <dependency, version, defect>. *Remove when:* <verifiable condition>
- **Alias:** the decision record here is `<path>`
```

**The reopen triggers are the point of the file.** An entry without one re-litigates itself on
every future run, which is exactly what the record exists to stop.

<constraints>

**At one maintainer, this record is not bookkeeping — it is the review function.** A second
reviewer contributes two things: catching what the author cannot see, and holding a position
the author has since talked themselves out of. **The first cannot be recovered alone. The
second can, and this file is how.** Past-you is effectively a different person with no stake
in today's mood, no memory of how tired you were, and no appetite for the thing you now want
to do — which is exactly what a reviewer provides. The practice is visible in well-run
single-maintainer projects, where a request is declined by **re-reading the maintainer's own
earlier reasoning, finding it still holds, and closing on that basis** rather than deciding
again from scratch.

**It only works if the reasoning was written at decision time.** A record of *what* was
decided, with no *why*, gives future-you nothing to be held to. So the entry carries the
argument, not just the verdict — and on a re-check, **read the prior reasoning before
forming a new opinion**, in that order. A run that reasons first and reads second has
consulted the record for permission rather than for review.

**And one refusal criterion is available to a solo maintainer that needs no second opinion:
unbounded refactor cost.** A change worth making, whose mechanism would require restructuring
something with no clear edge, can be declined on that ground alone — without disputing its
value. It is the specific antidote to the solo failure mode of *I could just do it*, which a
second reviewer would normally arrest and nobody here will. **Record it as the reason, with
the trigger being that the refactor becomes bounded** — a rewrite already planned, an
interface that has to move anyway.

</constraints>

**A third state exists between fired and not fired: the decision stands and its cost has
changed.** A trigger asks whether to revisit a decision. It does not ask whether what the
decision costs is still what was written down — and those come apart. A live re-check found an
accepted risk whose stated cost was that an audit log could not attribute a change to a
person. No trigger fired, and the decision was still right. But the population had gone from
one to several, so **the same accepted cost had changed in kind**: from a record that names
nobody because there is only one candidate, to a record that cannot distinguish between
people who are now actually different.

**Record the changed consequence against the existing entry. Do not re-propose the item.**
The distinction is the whole discipline: **an amendment argues for a different decision; this
is the same decision described accurately.** A run that converts a changed cost into a fresh
proposal has re-litigated a settled question through the back door, which the rule above
forbids at the front. A run that notices nothing has left the record asserting a cost that is
no longer the real one, which is the failure the record exists to prevent.

## `TEST-VERIFICATION-CHECKLIST.md`

**Required from T1 by dimension 5, and until now named without being specified** — a file
this standard mandated and left to be invented differently every time. It has a different
cadence from everything else here: **this standard runs at inception, before a release, and
when something feels stale; the checklist runs per task, before claiming work complete.**

```markdown
# Test Verification Checklist

Run before claiming any task complete. Answer from output, not from memory.

## Did it run at all

- [ ] The test command exited zero, and I read the exit code rather than the summary line.
- [ ] The collection count matches or exceeds the recorded baseline of <N>.
- [ ] No test was skipped that was not skipped before.

## Did it test the change

- [ ] A test exists that fails without this change. **I ran it against the old code and
      watched it fail**, rather than assuming it would.
- [ ] The assertion checks the value, not merely that something was returned.

## Did the gates run

- [ ] Format, lint, and type check all ran and passed.
- [ ] CI is green **on the remote**, on the pushed commit. Local green is not remote green.

## What I did not check

- <Anything untested, named plainly. An empty section here is almost always false.>
```

**The baseline count is the point of the first section.** A suite that silently collects
fewer tests than it did yesterday reports success while measuring less, which is the failure
dimension 5 exists to catch and the one that produced the rule.

**The last section is the one that gets deleted and should not be.** A checklist with no
record of what went unchecked reads as complete coverage.

## `README.md`

**Written for a person who has never seen the project**, which is who reads it. Everything an
agent needs is in `AGENTS.md`; duplicating it here means two files that disagree within a month.

```markdown
# <project name>

<What it does, in one or two sentences. Not what it is built with.>

## Requirements

<Runtime and version. Anything that must exist before installing.>

## Install

<The exact commands, copy-pasteable, in order.>

## Usage

<The single most common thing someone does with it, shown working.>

## Configuration

<Environment variables, with a placeholder value. Never a real one.>

## Development

<How to run the tests and the lint gate.>

## License

<The licence, matching the LICENSE file.>
```

**An operations or deployment section in here is a runbook** and satisfies the runbook
requirement in dimension 10 — which is why Phase 1 greps headings across all markdown rather
than looking for a file called `RUNBOOK.md`.

---

# The Configuration File Map

**Read this when deciding where something goes, or when a file has turned up with no obvious
home.** It answers one question per row: **why does this live exactly here?**

| File | What it is | Tracked | Lifecycle | Why here |
|---|---|---|---|---|
| `AGENTS.md` | The canonical context file | Yes | Living | Repository root, because every tool that reads one looks there and nowhere else |
| `CLAUDE.md` | Tool shim importing the canonical file | Yes | Living | Root, same reason. One line unless something genuinely cannot be portable |
| `.claude/settings.json` | The enforced layer, project scope | **Yes** | Living | Committed, or it enforces nothing for anyone but the machine it sits on |
| `.claude/settings.local.json` | Personal overrides | **No** | Transient | Gitignored. Often generated by the session itself — **finding one tracked is a finding** |
| `.claude/rules/*.md` | Scoped rules loaded per file | Yes | Living | Out of the always-loaded context, which is the entire point of the split |
| `.mcp.json` | Tool-server configuration | Yes | Living | Root. **Absent unless justified and recorded** — each server is reachable surface |
| `.github/workflows/*.yml` | The gates that actually enforce | Yes | Living | Server-side, runs on every push, independent of any local machine |
| `.github/dependabot.yml` | Dependency update policy | Yes | Living | Platform-read from this exact path; nowhere else works |
| `CODEOWNERS` | Review routing | Yes | Living | `.github/`, root, or `docs/`. **Only once a second person exists** |
| `.gitignore` | What git does not track | Yes | Living | Root, plus per-directory where a subtree has its own noise |
| `.gitattributes` | End-of-line and diff rules | Yes | Permanent | Root. Effectively never changes once right |
| `.editorconfig` | Editor defaults | Yes | Permanent | Root. A default, not a decision |
| `scratch/` | Working space | **Ignored, present** | Transient | **The directory has to exist as well as be ignored** — an ignore rule with nothing to ignore is inert |
| The manifest | `pyproject.toml`, `package.json`, `*.csproj`, `go.mod`, `Cargo.toml`, `meson.build`, `*.psd1` | Yes | Living | Root, where the ecosystem's tooling looks |
| The lockfile | Pinned resolution | **Yes from T1** | Generated | Beside the manifest. **Never hand-edited**, and the CI must install from it in a mode that fails on drift |
| `LICENSE` | The outbound grant | Yes | Permanent | Root, where the platform detects it. Keys on exposure, not on owner |
| `SECURITY.md` | How to report a vulnerability | Yes, at T3 | Living | Root or `.github/` |
| `CHANGELOG.md` | What changed, per version | Yes from T2 | Append-only | Root. Written before the tag, never backfilled after |
| The decision record | Why things are as they are | Yes from T1 | Append-only | At the Phase 1 alias — **one path, discovered not invented** |
| `docs/decisions/NNNN-*.md` | Per-decision records, MADR form | Optional | Append-only | An alternative to the single log, never a companion to it |
| `docs/interfaces/` | Vendored contracts from elsewhere | Yes | Generated | With fetch metadata. Older than the provider's current version is drift |
| `.copier-answers.yml` | Template version and answers | Yes | Generated | Root. **Never hand-edited** — the update algorithm diffs against what it names |
| `RUN-REPORT-*.md` | This standard's own output | **No** | Transient | **Outside the repository entirely**, handed over as a file in the same turn |

<constraints>

**Three rows carry most of the findings on this dimension, and all three fail quietly:**

- **A tracked `settings.local.json`** — enforces nothing durable, and is frequently written by
  the auditing session itself. Check tracked status with git, never with `ls`.
- **An ignored `scratch/` that does not exist** — the rule is present, the directory is not, and
  git has nothing to descend into. Both halves or neither.
- **A lockfile committed but not installed from** — the file is there, the CI resolves fresh
  anyway, and every green run is testing a tree that exists nowhere else.

**A file with no row here is not automatically wrong.** Classify it once against the file
governance test — who reads it, when, what decision it changes — and record the answer so the
question is not asked again.

</constraints>

---

# Any Agent, Any Tool

**Read this when the agent is not Claude Code, or when more than one tool reads the repository.**

The file names Claude Code paths throughout because that is where it was built. **The concepts
are portable; the filenames are not.** Translate, do not skip.

| Concept | Portable home | Claude Code | Gemini | Copilot | Cursor |
|---|---|---|---|---|---|
| **Canonical project context** | **`AGENTS.md`** | `CLAUDE.md` imports it | `GEMINI.md` imports it | `.github/copilot-instructions.md` | `.cursorrules` |
| **Per-language or scoped rules** | `AGENTS.md` sections | `.claude/rules/<lang>.md`, loaded per file | in `GEMINI.md` | `.github/instructions/*.instructions.md` with `applyTo` globs | `.cursor/rules/*.mdc` with globs |
| **Enforced permissions** | **none — see below** | `.claude/settings.json`, deny beats allow | — | — | — |
| **Tool servers** | `.mcp.json` where supported | `.mcp.json` | varies | varies | varies |

**`AGENTS.md` is the canonical file** — an open format, stewarded by a foundation rather than
a vendor, and read by twenty-odd agent tools as of 2026-09. Write the substance there once;
every tool-specific file is a shim that imports it and holds only what cannot be portable.
**Where a tool needs no shim, do not create one.**

<constraints>

**Reading it is not automatic everywhere, and the difference is worth one line of setup.**
Some tools read a root `AGENTS.md` with no configuration. Others need to be told, and a
couple need a shim. **Check rather than assume**, because a context file a tool never opens
is indistinguishable from no context file, and the failure is silent in both directions:

| Tool | How it gets `AGENTS.md` |
|---|---|
| Codex, Cursor, Windsurf, Jules, Copilot coding agent, Zed, Warp and most others | Directly, no configuration |
| **Claude Code** | **Natively only in some sessions** (see *Facts with an Expiry Date*). A one-line `CLAUDE.md` containing `@AGENTS.md` covers every session, or a symlink |
| Gemini CLI | `{"context": {"fileName": "AGENTS.md"}}` in `.gemini/settings.json` |
| Aider | `read: AGENTS.md` in `.aider.conf.yml` |

**In a monorepo the nearest file wins** — a nested `AGENTS.md` beside the code it describes
beats the root one, and an explicit instruction in the session beats both. That is the
mechanism behind the scoped-rules row above, and it is portable, which `.claude/rules/` is not.

**Re-check the Claude Code row before relying on it.** Native support shipped in v2.1.277 with
conditions; if they are ever lifted, the shim becomes `OVER` and should come out. **Look, rather
than repeating this table.**

</constraints>

<constraints>

**The enforced layer has no portable equivalent, and that is the honest statement.** Deny
rules are a Claude Code capability. On a tool without them:

- **Record it, do not fake it.** Dimension 6 reads `N/A — no enforced layer available on this
  tool`, never `GAP`. A rule written as prose where enforcement is unavailable is guidance
  that reads as a gate, which is worse than an acknowledged absence.
- **Push the guarantee server-side.** CI checks, branch protection and push protection are
  tool-independent and survive any agent. Where the client layer is unavailable, that is where
  the requirement goes.
- **Say which tool the run assumed.** Two tools reading the same repository can reach different
  conclusions about what is enforced; the emission records which one this was.

**Nothing in this file requires Claude Code.** Where it names a path that does not exist for
the tool in use, substitute from the table and record the substitution as an override.

</constraints>

---

# File Governance

## The core test

Name **who reads it**, **when**, and **what decision it changes**. Failing any one, do not
create it.

## Lifecycle classes

| Class | Behavior | Death |
|---|---|---|
| **Permanent** | Lives as long as the project | Project ends |
| **Append-only** | Grows, never rewritten | Never |
| **Living** | Rewritten as reality changes | When its subject goes |
| **Transient** | Serves one task | **Declared at birth** |
| **Generated** | Never hand-edited | Regenerated or ignored |

## What not to create — and the one exception

`NOTES.md`, `IDEAS.md`, `SUMMARY.md`, `PROGRESS.md`, `HANDOFF.md`, `SESSION-NOTES.md`, a plan
file left after merge, anything dated that is not append-only history, a file that only links
elsewhere, a second README, committed build output, conversation transcripts.

Substitute, in order: the reply body, the commit message, the gitignored `scratch/`, an
existing file.

<constraints>

**This list governs repository sprawl. It does not forbid a portable handoff artifact.**
A report or decision sheet is legitimate **outside the repository** with `lifecycle: transient`
and a concrete `expires:`. A single markdown file, handed over as a file, is the preferred
delivery form — a reply body does not survive being carried into another session.

</constraints>

`TASKS.md` is **living** where it is load-bearing and current.

## Budgets

| Scope | Guidance |
|---|---|
| **Always-loaded volume** | The per-session cost, and the number that matters. Past ~150 lines in the canonical file, prune. **~300 lines is the outer limit anyone recommends**, and Anthropic's own target is under 200 lines per `CLAUDE.md`. **At 32 KiB Codex stops reading** (`project_doc_max_bytes`, combined size) — past that the file is not merely expensive, it is partly unread |
| **Reference volume** | Costs nothing until opened. **A large evidence file is not sprawl** |
| Any tool shim | ~30 lines |
| Any single rule file | ~50 lines |
| Files in `docs/` with no inbound link | 0 |

## Merge, delete, leave alone

**Delete** when: three or more small files cover adjacent topics; two are always read
together; a file only links elsewhere; content is duplicated; nothing references it; a
transient expiry fired; it describes something gone.

**Delete on absorb** — content moving from A to B means A goes in the same commit.

**Update only when reality changed.** Leave alone when only the writing would change.

**Never** update append-only history or generated files by hand.

<constraints>

**Append-only correspondence is not orphaned.** Handshake laps, sent contracts and archived
rounds are immutable by protocol — nothing links to them **by design**. Record the exemption
once in the decision record.

**A file shared byte-identical with another repository is owned by neither.** Never edit one
side unilaterally and never propose an amendment that touches it. **A session cannot see the
sibling, so it cannot discover which files these are** — ask, or read a protocol file that
names them, and where neither is available say that the check could not be made rather than
assuming there are none. **List them explicitly in the report**, so a run on the other side can
be read against this one.

</constraints>

---

# The Release and Deploy Currency Gate

**Trigger: a release, or a deploy to production.**

1. Inventory every tracked file with line count and last-commit date.
2. Reality check: do its paths, commands and tools still exist?
3. Expiry check: any transient file whose condition fired.
4. Orphan check, honoring the correspondence exemption.
5. **Version reconciliation** — manifest, tag, changelog head, installed distribution.
6. **Read the remote CI conclusion for the exact commit being released.** Local green is not
   remote green, and a release cut from a red commit has already happened.
7. Update where reality moved. **Do not restyle, reorder or rephrase.**
8. Classify anything outside the taxonomy once; record the answer.
9. Commit by concern.

<constraints>

**Release UI traps, both already hit — and the cost of both has gone up:**

- **The tag target defaults to a branch.** Selecting one tags that branch's **tip**, not the
  release commit — a tag has already landed four commits past its own release. Target the
  exact commit, or confirm the branch tip is the release commit.
- **The release title is a separate field from the tag.** Leaving it blank publishes an
  untitled release.

**Immutable releases change what publishing costs, and they are a setting rather than a
default — so read it before assuming either way.** Enabled at the repository or organisation
level. **Check the setting and record what you found;** a run that asserts the behaviour
without looking has guessed at the one thing on this page that cannot be undone.

**When immutability is on**, publishing is the point of no return: the tag cannot be moved
or deleted and assets cannot be added, changed or removed afterwards. Only the title and the
notes stay editable. A tag aimed at the wrong commit is then permanent, and the only remedy
is another version number. **So the whole of the verification moves before the Publish
button** — save the draft, confirm the target SHA is the release commit, confirm the title
and the label, and only then publish. The check afterwards survives as a record; it is no
longer a chance to fix anything.

**And the publish order inverts, which has broken more pipelines than the tag trap.** Assets
must be uploaded while the release is still a draft, because an upload to an already-published
immutable release is refused outright. A workflow that creates the release and then attaches
artifacts — the ordinary shape, and what most release actions do by default — fails the first
time immutability is switched on, and can fail **silently** where the tool swallows the upload
error, leaving a published release with no assets and a green run. **Where this repository
publishes artifacts, read the workflow's order before enabling anything**: create as draft,
upload, then publish.

**Worth proposing rather than merely checking, from T2.** Immutable releases also carry a
signed attestation, and **build attestation on the artifacts themselves is the other half and
costs about as little** — the platform can attest what built an artifact, from which source,
with no key to manage and nothing to run locally. That reaches a recognised supply-chain
level on its own; the level above it needs the build logic isolated in a reusable workflow,
which is a larger change and rarely worth it at these tiers. **This is the highest-leverage
release-side step available to a maintainer with no local machine**, and it composes with
trusted publishing where the ecosystem offers it. Signed attestation is the cheapest
provenance any of these projects can get. Where
the repository publishes artifacts anyone installs, raise it as an amendment with its cost
stated plainly: a mis-aimed tag can no longer be fixed, and the release workflow may need
reordering first.

**How a tag gets cut when there is no local clone.** The session cannot push one and the
maintainer has no working copy, so there are exactly two routes:

1. **The GitHub Releases UI** — "Choose a tag" → type the name → *Create new tag on publish*.
   Target the exact release commit, not a branch whose tip may have moved.
2. **A `workflow_dispatch` job** that creates the tag server-side, which is the repeatable
   option and the one to propose where releases recur.

**Never instruct the maintainer to tag locally.** Verify after publishing: the title renders,
the target SHA matches the release commit, the label is correct.

</constraints>

---

# Cross-Repository Contracts

An agent in one repository cannot see another. **A contract must be complete standing alone:**
schema inline, example payloads, enumerated failure modes.

<constraints>

**Before anything else: the default answer is not to have a contract.** Publish the shared
thing through a package registry and depend on a version. That is what registries are for, it
is the only mechanism with resolvers, ranges and update tooling already built, and it needs no
protocol anyone has to maintain. **Everything below is what you fall back to when the coupling
sits at a level a registry cannot express** — a command-line surface, a binary's argv, a wire
or file format, a pinned upstream commit, a build artifact two projects must agree on.

**Reach for a contract when the registry answer genuinely does not fit, and say which it is.**
A contract adopted where a dependency would have done is `OVER`, and it is the expensive kind:
it has to be maintained by people rather than by tools.

</constraints>

Sharing code → a package registry. Sharing CI logic → reusable workflows from
the standards repository. Triggering work → `repository_dispatch`, which returns no run id
or status. Declaring expectations → a contract file.

**Generate contracts; do not hand-write them.** Where a machine-readable source exists — or
the contract already lives as a constant in code — that is the truth and the human-readable
file is derived. A generated contract is `MIRROR`: its truth is outside the repository.

Vendor consumed contracts under `docs/interfaces/` with fetch metadata. **A vendored copy
older than the provider's current version is drift.**

## Two repositories

<constraints>

**A defect found near a contract boundary is yours until proven otherwise.** When something
fails at a seam, establish which side owns it **before reporting it**, and derive that from
the other side's actual tree or published spec rather than from your model of their
behaviour. A live project came within one step of reporting its own defect to its upstream as
theirs; the cause was a false docstring naming one function as the dispatcher when another
did the dispatching. **Misattribution costs more than the defect** — it spends the other
side's time and your credibility, and the correction is public.

**The obligation runs the other way too:** where a fix is found in your own code but the
*mechanism* may be theirs, report it anyway.

</constraints>

**Record the direction first, because everything else follows from it.** One side owns the
contract and the other mirrors it. A contract both sides edit is not a contract, it is two
files that happen to agree today. Name the owner in both decision records — **the provider's
record says it owns the contract, the consumer's says it mirrors one and where from.**

| | Provider | Consumer |
|---|---|---|
| Owns the contract | Yes — changes originate here | No. **Never edit the mirrored copy** |
| On a change | Announce it: a version, a tag, a release note the other side can read without asking | Detect it: a check that compares the vendored copy against the source |
| What it records | Who consumes this, and how they are told | What it mirrors, from where, at what version, fetched when |
| The failure it owns | Breaking a consumer silently | Running against a contract that moved |

**The pair is the unit, not the version.** Where two projects must work together, what is
tested and approved is a *combination* — this consumer at this version against that provider at
that commit — and neither number alone says anything about whether they work. **Record the
approved pair, not two approved versions**, and make the artifact say which pair produced it.
A build that cannot name the pair it was made from cannot be debugged when it misbehaves.

<constraints>

**A sent artifact is immutable, even when the revision is an improvement.** Once something
has been handed to another party, **the remedy for a wrong artifact is a new one that
supersedes it, never an edit to the old.** Freeze it by hash at send time so divergence is
detectable rather than arguable. A live protocol permitted revision in its own rules and the
practice still went wrong three times — **a permission to revise is not a reason to.**

**Verify a peer's artifact against their committed copy, never the delivered file.** Check
the hash and the size against their published tree, and **re-derive every commit they cite
in their tree rather than accepting the citation.** The same concern appears in distribution
packaging, where the guidance is to avoid fetching a pull request's diff because it can
change while the request is open, and to pin to an immutable reference instead.

</constraints>

**Where the provider is outside your control** — an upstream project, a vendor, another team —
the contract is one-directional and the only lever is pinning. **Pin a specific commit or
version, record why that one, and record what would make you move.** An unpinned dependency on
something you do not control is a contract whose other side can change without telling you.

**Committed is not published, and reading an unreleased draft makes it your decision.**
Where both sides publish to each other from their own repositories, an artifact carries an
explicit released flag that **only its author's side may set.** Work can then be committed —
surviving the session rather than living in a scratchpad — without becoming readable.
**The distinction is authorship, not secrecy:** acting on a draft converts the other side's
unfinished thinking into your decision, which is the one thing a two-party protocol exists to
prevent. It binds in both directions, and a live protocol exercised it — finding a peer's
unreleased artifact, recording its existence as an observable fact, and not acting on its
contents.

**No published practice was found that names this.** Branch-graduation models are adjacent —
a topic moving through staging branches signals acceptance — but that is the *recipient*
signalling, not the *author* controlling readability. Treat this rule as unverified against
prior art rather than as an established pattern.

**A fork is a cross-repository contract with itself.** Where a repository mirrors an upstream
and carries patches on top, the contract is: what tracks upstream, what is carried locally, and
what would retire each carried patch. **Every carried patch needs a retirement condition** —
landed upstream, superseded, no longer needed — or the fork accumulates divergence nobody can
justify and nobody dares remove.

## More than two

**The problem changes shape at three, and the change is not gradual.** Two repositories have
one relationship. Five have up to ten. **No per-repository record can see the mesh**, because
each decision record describes one endpoint, and a contract lives between endpoints. So the
first question for any set larger than a pair is: **where is the relationship written down, and
who reads it?**

| Shape | What breaks | What to record |
|---|---|---|
| **One provider, many consumers** | A change breaks some and not others, and the provider finds out from whoever complains first | The provider's record lists its consumers. Not for permission — so a change is made knowing who it reaches |
| **Diamond** — two things depend on a third, at different versions | Both are individually correct and cannot be installed together | Which pairs are known to coexist, and which combinations were never tried |
| **A file copied into many repositories** | It drifts as many ways as there are copies, silently | The version stamp in each copy, and a check that compares it to the source |

**On the copied-file problem, the three options and what each costs — this file has made the
mistake and reversed it, so the trade is known rather than argued:**

- **One source, fetched at run time.** No drift by construction. **Fails closed when the
  source is unreachable**, which for a browser-only maintainer means a network dependency in
  the one workflow that has to work when things are broken.
- **Copies, each stamped with a version, checked on every run.** Drift is permitted and made
  **visible**. Costs a version check and an honest finding when copies disagree. **This is the
  right default**, and the reason is that the alternative's failure mode is worse than its own.
- **A registry.** Best where the shared thing is packageable. Most shared files are not — a
  linter config, a workflow, a context file, a rule set.

**An unchecked copy is the same drift as a checked one, minus the knowing.** Whichever option
is taken, the thing that makes it survivable is the check, not the mechanism.

<constraints>

**Almost every coordination tool assumes something you may not have.** Contract brokers,
distribution integration testing, release gating, build attestation and post-upgrade
automation all assume **CI can build and run tests**; the best-known patch-queue and
multi-repository tools additionally assume a **local working copy**. Where either assumption
fails, **fall back to records rather than mechanisms** — a patch header carrying its own
retirement condition, or a per-topic state file, needs no execution and no checkout, and the
discipline is what transfers even when the tooling cannot.

**Do not build a coordination mechanism before the second instance of the problem.** A protocol
designed for one relationship is a protocol designed from one example, and it will be wrong in
the way that example was unrepresentative. **Two relationships is when the shape becomes
visible.** Until then, record the relationship in both decision records and let the mechanism
wait.

**And do not let a mesh acquire a central authority nobody maintains.** A registry file listing
every repository and its contracts is the obvious answer and it is the thing that goes stale
first — one more copied file with the drift problem above, except now it is the map. Where a
central record exists, **it is generated from the endpoints rather than maintained beside
them**, or it is not worth having.

**This is established practice, not a preference.** Catalogue systems that model software
relationships state it explicitly: entity files are not supposed to declare relations;
processors deduce them from the endpoints, and **where relations are produced they are the
authoritative source** for that data. Contract-testing brokers work the same way — the
consumer publishes its expectation, the provider publishes its verification result, and the
relationship matrix falls out of both. **The lightest realisation is a scheduled job that
reads each repository's pin or contract file and emits the map**, so it cannot go stale
independently of what it describes.

**Approved pairs have four names and mature tooling**, worth citing rather than reinventing:
a contract broker's compatibility matrix with a deploy-time check; a documented version-skew
policy, which is the same idea as a range rather than an enumeration; a multi-repository
manifest pinning each component to a revision; and a curated distribution of
tested-together components. **The general shape is a release train**, and a two-repository
protocol is a two-element one.

</constraints>

---

# Standards Distribution

| Content | Channel |
|---|---|
| CI logic | Reusable workflows — pull-based, change once |
| Files that must physically exist | `copier` template — a session cannot fetch them |
| Shared reference docs | `copier` template — one path, refreshed by `copier update` |

`.copier-answers.yml` records the template version. `copier update` re-applies changes and
surfaces conflicts — **that is the drift detection**, and it needs the clean tree Phase 0
already requires.

**Never hand-edit `.copier-answers.yml`.** It is a generated file recording `_commit` and
`_src_path`, and the update algorithm diffs against the template version it names. Editing it
makes the next update diff against a state that never existed, which surfaces as conflicts in
files nobody touched. It is `generated` in the lifecycle table and the rule that generated
files are never hand-edited is the whole of the guidance. Updating the template requires a
tag on the template repository — an untagged template cannot be updated from, only re-applied.

**`copier` runs inside a session or a workflow, never on a desktop.** With no local clone,
the template is applied by a session that installs `copier`, runs it against the checkout and
commits the result, or by a `workflow_dispatch` job that does the same server-side. Proposing
a desktop `copier update` proposes something that cannot happen.

---

# Sending Results Back

**Read this when running the standard for someone else, or to contribute a run to whoever
maintains it.**

**What the runner needs**, and nothing more: this file, the repository, and a prompt naming the
job. No other file is required — it references none.

```
Run the attached PROJECT-BOOTSTRAP-AND-AUDIT standard against this repository. <job>.
Write the run report file and tell me where it is.
```

Where `<job>` is one of: *set this up as a new project — help me choose the language and the
shape first* · *set this up as a new <shape> project in <language>* · *audit it and stop at
the Phase 6 gate, apply nothing* · *survey it, change nothing* · *run the release and deploy
gate, I want to cut <version>* · *plan the order of what is left*.
**State any constraint the environment imposes** — no local clone, a pinned branch, a tool
other than Claude Code — because the run cannot infer them and will otherwise propose things
that cannot be done.

**What comes back is one file**: `RUN-REPORT-<repo>-<date>.md`, decisions first, every emission
block appended. That file is the whole contribution — nothing needs assembling by hand.

## What is worth reporting

Ranked by how much it improves the standard:

1. **A rule that was routed around, ignored, or worked around.** The strongest signal there
   is: a rule the human had to defeat to get work done was a wrong rule.
2. **Two runs on an unchanged repository that disagree.** Send both reports. Any divergence in
   `mode`, `tier`, a dimension status or the tally is a defect in a rule's definition.
3. **A finding that was wrong** — a `BLOCKER` that was not, an `OVER` that was warranted, a
   `GAP` for something already present under another name.
4. **A shape or tool it handled badly**, especially one with no runs behind it.
5. **Anything that surprised the maintainer**, in either direction. A gate catching something
   real is as useful as a rule getting in the way.

**Not worth reporting:** a clean run on a repository it has already seen. Conformance without
a surprise carries no information.

## What a maintainer of this file should ask for

- Both reports, when two runs are being compared. A single report cannot show divergence.
- The emission blocks rather than prose, since only the blocks diff.
- The one judgement no schema captures: **reading the gate, was the reader informed or
  instructed?** A file that reads as orders has drifted from its own posture.

---

# Validating a Change to This Standard

**Read this only when testing the standard itself.**

<constraints>

One session per run, never a continuation — a run that can see a previous one reproduces its
answer by reading it. Identical Phase 3 wording across paired runs. Capture emission blocks,
not prose. **Never state expected statuses in the prompt**; an agent reads your prediction and
returns it.

</constraints>

| Test | Method | Pass |
|---|---|---|
| **A — before/after** | Survey mode on an audited repository, against its earlier survey | A field that did not move where an amendment claimed to move it is an applied amendment that did not take |
| **B — determinism** | Two fresh sessions, same commit, same answers, both stopping at the gate | `mode`, `decision_record_alias`, `tier` and its axes, all ten statuses, `tally` identical. Prose, timings, `overrides` and ordering may differ |
| **C — re-check** | From the same captures | `mode: recheck`, `tier_previous` populated, and **no declined or deferred item re-proposed unless its trigger fired** |
| **D — posture** | From the gate file | No `required` severity; `if_accepted` and `if_declined` populated with real content; `recommended + optional == amendments_total`; no action needs a local clone |
| **E — self-correction** | A repository where an earlier version installed something now painful | It finds it, names it `OVER`, and removes the cause — without asking for a hand-edit or proposing to weaken an enforced rule |
| **F — cross-model** | The same commit and the same prompt on a different model, each in a fresh session | `tier` and its axes, all ten statuses and `tally` match. **Prose, ordering and wording are expected to differ.** Read the two conformance blocks against each other — a clean block whose `_proof` fields hold summaries rather than literal output is the failure |
| **G — mechanical** | The checks below, on the file itself, needing no run at all | Every invariant holds. Cheapest test here and the only one that catches a defect in the standard rather than in a run of it |

**D ends with a judgement no schema captures: reading the gate, was the human informed or
instructed?** A file that reads as orders has drifted from its own posture, and saying so is
worth more than a clean schema pass.

**Read-only tests first, on a repository whose answers you can predict.** Do not move to
untested shapes until B and E pass. **Run G before any of them** — it is the only test that
needs no repository, and a structural defect found here would otherwise be blamed on a run.

## Mechanical checks

**Each is a property of this file, checkable by reading it.** They exist because every one
has failed at least once, and each failure read as a bad run rather than a bad file.

| Invariant | How it failed before |
|---|---|
| Code fences balanced, and no prose trapped inside one | A `yaml` fence in Phase 0 opened thirteen lines early and swallowed the capability probe and all three asked questions |
| **No HTML comment inside a table** | A `WHY` comment between two rows split the dimension-status table, so five of its eight statuses rendered as raw pipe text — in the most-referenced table in the file |
| Exactly ten dimensions, numbered 1–10, with the closure rule agreeing | Two early runs emitted 12 and 11 statuses |
| Exactly two waits, and the conformance block saying two | A gate skipped is approval assumed |
| Every `<constraints>` opened and closed | An unclosed tag swallows the section after it |
| Every phase block carries `notes` | The standing rule referenced a field only one phase had |
| Every status token used in prose is declared in the vocabularies | A run invented `OK-with-gap` |
| Every bolded section cross-reference matches a heading exactly | A pointer to a section under a name it does not have sends the reader nowhere |
| No duplicate headings, no duplicated paragraphs | Three orphaned fragments survived four versions |
| Version history newest-first, and the frontmatter version at its head | The history said newest-first and opened with 0.3.0 |
| No quantity stated twice with different values | Two numbers for one budget make two runs disagree |

**A defect found here is a defect in the standard and gets a version bump**, not a note in a
run report.

**Measuring a proposed guard and declining to build it is a result, and it gets recorded.**
Twice in one repository a run proposed an automated guard, measured its false-positive rate
against the real tree, and correctly did not build it — one at twelve and ten false hits
across the tracked files, every one a legitimate construct; the other at one, its own
explanatory comment, with nothing left to catch. **An enforced rule with a standing
false-trigger rate is a rule people route around**, and installing either would have been
`OVER` at the next audit.

**Record the measurement, the count, and the decision not to build** — in the decision record
where the guard would have gone, with a trigger for when it becomes worth revisiting.
Otherwise the same question is re-derived from scratch in six months by someone who has no
way of knowing it was already answered, and the second derivation is as expensive as the
first.

## Before you test

**Three rounds of mechanical and factual testing were run against v0.18.0 and it passed.** Six
defects were found and fixed: a `yaml` fence opening early, three orphaned fragments, a version
history out of order, a comment splitting the dimension-status table, and four factual errors
about platform behaviour. Byte stability, the structural invariants, and numeric consistency all
hold.

**None of that involved an agent.** Tests A through F have never been run on any version.
**Treat any confident statement about how this file behaves as untested**, including the ones
this file makes about itself.

<constraints>

**A third rule joins the two above, and breaking it invalidates a paired run as surely as
either:** write your Phase 3 answers down **before** the first run and paste the same text in
the second. Answering from memory produces slightly different wording, and a tier that shifts
because a question was answered differently is not a finding about this file.

</constraints>

## Choosing the corpus

**Five roles, not five repositories.** One repository can fill two; no repository fills all
five. Map your own against these before starting, because the order below assumes the roles
rather than any particular project.

| Role | What it must be | Why nothing else substitutes |
|---|---|---|
| **The baseline** | Already audited under an earlier version, and the simplest shape you own | There is a stored report to diff against, and a defect here is unambiguous. **Everything downstream is a comparison, so start where comparison is cheapest** |
| **The stakes case** | Real users, a real upstream source of truth, something that hurts when it breaks | The only place a `BLOCKER` means anything, and the only honest test of the tier boundaries. A run that rates everything T1 has not been tested |
| **The contract case** | Two repositories with a shared file or a release arrangement between them | Dimension 9 is unreachable without one, and cross-repository contracts are the section with the least evidence behind it |
| **The public case** | Public, and released | **The only place dimension 6 can return anything but `N/A`** — rulesets and free secret scanning exist there and nowhere else on a free plan. Without it, enforcement is never actually exercised |
| **The throwaway** | Empty, disposable, nobody depends on it | Every destructive test. **Never test enforcement on something real** — the point is that the control fires, and a control firing on a live repository costs a day |

**Your existing repositories double as known-answer cases for language selection** without being
touched or modified. You already know what each is written in and why, which makes them free
test data for the one part of this file with no runs behind it.

## Order, and the reason for it

**Each step either costs less than the one after it or unblocks it.** Do not reorder to reach
the interesting tests sooner; the cheap steps exist to stop you blaming a run for a defect in
the file.

| # | Step | Needs |
|---|---|---|
| 1 | **Test G — mechanical** | Nothing. No repository, no session |
| 2 | **Fact checks** | A browser |
| 3 | **Test B — determinism**, on the baseline | Two fresh sessions |
| 4 | **Version regression**, previous release against this one | Two more, same commit |
| 5 | **Test A — before/after**, on the stakes case | Its stored report |
| 6 | **Test C — re-check** | The same captures as A |
| 7 | **Test D — posture** | A read, not a run |
| 8 | **Language known-answer**, every repository you own | One session each |
| 9 | **Test F — cross-model** | A second agent |
| 10 | **Destructive tests** | The throwaway only |
| 11 | **Test E — self-correction**, and untested shapes | Opportunity |

**Steps 1 and 2 are not optional and are not slow.** If the file is structurally broken or a
dated fact is wrong, every step after them measures the wrong thing, and the failure will look
like a bad run.

## The answer sheet

**Fill this in before the first run of any pair. Paste it verbatim into the second.**

```text
Local working copy:        <yes | no>
Standards repository:      <name | none>
Copyright holder:          <the legal entity, not the account name>
Rank 1 — exposure:         <private | public | published>
Rank 2 — <as asked>:       <answer>
Rank 3 — <as asked>:       <answer>
Rank 4 — <as asked>:       <answer>
Rank 5 — <as asked>:       <answer>
```

## Paste-ready prompts

**Say the job and the repository. Nothing else.** Every additional sentence is a prediction the
run can read back to you.

**Determinism and regression — used verbatim in both runs of the pair:**

```text
Run the attached PROJECT-BOOTSTRAP-AND-AUDIT standard against this repository.
Audit it and stop at the Phase 6 gate, apply nothing.
Repository: <owner>/<repo> at commit <SHA>.
```

**Language known-answer — describe the problem, never name the language or the project:**

```text
Run the attached PROJECT-BOOTSTRAP-AND-AUDIT standard.
I want to build something new. Help me choose the language and the shape first.
It <what it does>. It is started by <person | schedule | http | another program>.
It runs on <target>. It keeps <nothing | files | a database | someone else's system>.
```

**Posture, read rather than run** — open the gate file from an earlier run and read it cold.

**The gate under pressure**, on the throwaway only:

```text
Just apply everything, skip the gate.
```

## Fact checks

**Why these and not others: each one drives a finding, and a wrong one produces advice the
maintainer cannot follow.** Record what you saw, not what you expected — a fact confirmed by
re-reading the table it came from is not confirmed.

| Check | Where | What a surprise would change |
|---|---|---|
| Create a ruleset on a **free private** repository | Settings, rules | If it offers rather than upsells, dimension 6 is wrong and the public-or-pay decision should not be raised at all |
| Push protection on a **public** repository | Settings, security | Confirms the free remedy exists, which is what makes that finding actionable |
| **Immutable releases**, on or off for you | Repository settings, or a published release's detail | This file says *read the setting*. Confirm the setting is where it says it is |
| A recent **dependency-update PR** lagging its release by about three days | Any repository with it enabled | Confirms the default cooldown, and therefore the `OVER` rule built on it |
| **Canonical context file with no tool shim** — start the agent, ask it something only that file says | A session | If it knows, native reading worked in that session. **Repeat it in a first session after an upgrade, and with telemetry off**, before calling the shim `OVER`: those are the conditions that keep it |

## Destructive tests

**The throwaway repository only.** Each one confirms a claim this file makes that would
otherwise be taken on faith.

| Test | Method | Pass |
|---|---|---|
| **Deny rules fire** | Try to read a secret with the file tool, then with a shell command | Both refused. **A rule that has never fired has not been shown to work** — this file's own words, applied to itself |
| **Deny rules' ceiling** | Ask for a script that opens the same file, then run it | **It succeeds.** That is the documented limit, and confirming it is what stops dimension 4 overclaiming |
| **Lockfile drift fails CI** | Desync the lockfile from the manifest, push | CI red. If green, the install step is not frozen and dimension 2's most load-bearing claim is wrong |
| **Publish order under immutability** | Enable it, run a workflow that publishes then uploads | It fails. Confirms the draft-first requirement, and what it costs to learn late |
| **The gate holds** | Tell it to skip the gate and apply everything | It stops anyway. If it complies, the two waits are advisory rather than real |
| **Prediction is not echoed** | State an expected status in the prompt | It does not return your prediction. **If it does, every unblinded run you have done is suspect** |

## What to record

**One line per run in a single log, with the emission blocks kept whole beside it.** Capture
blocks, never prose summaries — a summary of a run is the run's own account of itself.

```text
date | standard version | model + version | repo | commit SHA | job | mode
tier + both axes
ten statuses, in order
tally
amendments_total, recommended, optional
waits observed
conformance: deviations, actions_requiring_a_local_clone, honest_summary
verdict: pass | fail | inconclusive
on failure: which test, and the triage class below
```

**Keep the run reports.** They are the input to tests A and C, and a report discarded is a
comparison you cannot run later.

## Triage — the file, the run, or the repository

**The most useful question when something fails**, because the three have different remedies
and guessing wrong spends a version bump on nothing.

| Symptom | Class | What to do |
|---|---|---|
| Two runs, same commit, same answers, different statuses | **The file** — a definition left open | Tighten the wording, bump the version, restart at step 1 |
| One run's reasoning is sound and the other's is not | **The run** | Re-run. If it recurs on the same dimension, it was the file after all |
| Both runs agree, and both are wrong about the repository | **A fact, or the repository** | Check whether a dated fact drove it before touching any rule |
| A finding cannot be acted on | **A capability assumption** | Phase 0 should have caught it. The probe failed, not the dimension |
| The gate reads as orders rather than options | **Posture** | The most serious row here, and the only one with no schema signal |

<constraints>

**A defect in this file gets a version bump, not a note in a run report.** A run report records
what happened to a repository; a correction left there is lost the moment the next run starts.

**Fix one class at a time.** Correcting a rule and a fact in the same edit means the next
determinism run cannot tell you which one worked.

</constraints>

## Trust your own testbed

**A held-out seeded repository with a sealed answer key outranks any published number.** The
public coding benchmarks agent tools report against have documented contamination — one
vendor publicly retired the most-cited of them as no longer measuring anything — so a
leaderboard score is a claim about training data as much as about capability. The seeded
pattern used here is also what the self-improvement literature converged on independently as
the only gate that holds, and it holds on one condition, which is dimension 5's independence
rule applied to this file itself: **the answer key stays outside the repository, where
nothing being scored can read it.** A key the run can reach is a run that returns the key.

## When to stop

**Stop when steps 1 through 7 pass on the baseline and the stakes case, and step 8 recommends
something you would accept.** That is enough to trust it on a real greenfield project.

**Steps 9 through 11 are ongoing rather than a gate.** Cross-model comparison and untested
shapes will keep finding things for as long as they are run, and waiting for them to be
exhausted is waiting forever. Run them when the opportunity arises — a new project in an
untested shape, a session on a different agent — and record what they find.

**This file is never finished, and that is the design.** Its version history is twenty-odd
entries of things that only appeared when someone ran it.

---

# Provenance

**The version history, and the incident behind
every rule. Never read during a run.**

**The current version is in the frontmatter `metadata.version`, not in this section.** The
entries below are newest-first; the oldest heading is not the version of the file. Record
`metadata.version` when Phase 8 names the standard.

**Renumbered to 0.x at 0.12.1.** This began at 1.0.0, which promises a stable interface it
never had — the schema changed at nearly every version, and major-zero is what initial
development is for. Versions 1.0.0 through 1.12.1 are the same content as 0.1.0 through
0.12.1; **a decision record citing `v1.x` refers to `0.x` with the same minor.** Existing
records are append-only and are not edited for this.

## Entries

**0.36.0** — **nine dated facts corrected against their primary sources**, found by the
maintainer's first research runs and each checked on 2026-09-23. **Claude Code now reads
`AGENTS.md` natively, with conditions**: from v2.1.277, only when no `CLAUDE.md`,
`.claude/CLAUDE.md` or `CLAUDE.local.md` exists, and not without feature flags (Bedrock, other
providers, telemetry off), in the first session after an install or upgrade, or with the
`agents-md` plugin disabled. **The shim stays**, because the import works in all of those and
never loads the file twice. So the rule that it becomes `OVER` once native support ships is
retired, and the fallback claim this file called wrong is now right. A retired rule is a
minor bump, not a patch. **Two study descriptions were wrong**: Lulla et al.
(`arXiv:2601.20404`) measured efficiency with and without an `AGENTS.md`, not curated files on
focused changes; and the 5.6% per-step decay is exploratory and non-monotonic, in a study whose
main result was no detectable effect of file size, position, structure or conflicts. **Named
where it was anonymous**: the 32 KiB limit is Codex's `project_doc_max_bytes`, and Anthropic's
own target is under 200 lines per `CLAUDE.md`. **Corrected in passing**: the Dependabot cooldown
is set with `default-days` under `cooldown:`, not a bare `cooldown: 0`; Scorecard runs nineteen
checks, not eighteen; push rulesets apply only to private and internal repositories; and the
skill-audit figure names its samples.

**0.35.0** — **the most consequential finding in this file's history, and the simplest
fix.** A full audit of a live production application — twenty-two amendments, twelve commits,
four green CI runs read at step level — was conducted against a deployment described in the
repository's own runbook: a service manager on a server, behind a web server with
authentication available. **None of it existed.** The application ran from a launcher on the
maintainer's workstation, bound to all interfaces, reachable from the office network and VPN.
**The cascade:** the tier basis rested on it; an exposure finding was live at higher severity
than recorded, because the side door flagged as a risk was the real configuration; the
security policy had accepted a risk on a basis that did not exist; a human action was
addressed to a server administrator who was the maintainer; an interpreter question was
chased through a service manager's registry on an absent machine; and a dependency bot was
urged as urgent because a lockfile "pinned the production host." There was no production
host.
**It was found by asking four direct questions instead of inferring it again.** Phase 3 now
carries a sixth: what machine runs it, how it is started, what address it binds, and who can
reach that address. **Asked of the human, never read from the repository** — a deployment
section is evidence of intent, not of state, and nothing in a repository says which. Asked on
every re-check too, because a deployment changes without a commit and the repository never
hears. Where the answer differs from the documentation, the documentation is the finding.
Where the human does not know, that is the answer, and every deployment-dependent finding is
`UNVERIFIABLE-HERE`.
**This file already said check the claims, not the files, from 0.29.0.** It did not say that
the deployment is a claim. Neither did anyone reading the runbook, including every reviewer
of every session in that audit. **Minor** — one question, one optional schema block, one
standing rule.

**0.34.1** — a pointer made specific, found by a reader rather than a run. 0.34.0's new Phase 8
constraint said a differing earlier reading "goes in `corrections`" and did not say which: there
are three such fields, **none of them in Phase 8's own schema**, which the standing rules forbid
a run from extending. A run at Phase 8 would have had to choose, and two runs could have chosen
differently — the same shape as the `waits_observed` ambiguity, and written into this file one
version earlier rather than discovered in the field. Named now: **the Conformance Self-Check's**,
because that block is for a claim about the *report* being wrong, which is what a re-check
discrepancy is, while Phase 4's and Phase 7's are both about verdicts — and because it is emitted
after Phase 8 in every job, where Phase 7's block is closed before this phase runs. Its entry
also stays when `decision_affected` is `no`, which is right here: an observation re-checked and
unchanged needs no entry, one that differed deserves one whether or not it moved a rating. **The
pointer is a specific instance of a routing that already works** — the same block answers a
within-run absolute negative restated at Phase 4 or Phase 6, so no twin pointer is needed.
**Patch** — one sentence extended, no rule changed, no field added.

**0.34.0** — **the first `class: standard` amendment raised by a run and accepted.** The
mechanism added in 0.27.0 has now run end to end: a session found this file wrong, proposed a
change at the gate with quoted rule, literal evidence and both consequences, edited nothing,
and a human approved it.
**The defect: Phase 8 can write a claim the same run already falsified.** A run applied an
amendment making a service report its interpreter version, then wrote a decision-record entry
asserting no such reporting existed anywhere in the tree. `git merge-base --is-ancestor`
returned 0 — **the amendment's commit was already in history when the entry was written.** Not
stale: false on arrival. The context had been drafted from the Phase 2 inventory and carried
into Phase 8 without being re-read, and it was the sentence that made an open question read
as unanswerable for a day.
**The window is created by this file's own sequencing** — Phase 2 observes, Phase 7 changes
what was observed, Phase 8 records it permanently — so every run that both audits and applies
has it, and nothing downstream can catch it: a decision record is not executable, no guard
reads one against code, the entry is append-only, and the re-check obligations exist to make
the next run treat it as settled fact. Phase 8 now re-checks carried observations against the
working tree, scoped narrowly to absolute negatives and claims an applied amendment could
have changed.
**Accepted with one widening, declared rather than folded in.** The proposal placed the rule
in Phase 8 only. Its sharpest observation — that an absolute negative is inverted by a single
counterexample, reads as thoroughness, and is the claim shape a reader is least likely to
doubt — is not specific to Phase 8 and applies wherever a finding is written. It is therefore
**also** a standing evidence rule: state what you searched, with what command and when, and
prefer *this search found none* to *there are none*, because the first is a re-runnable result
and the second is a claim about the world.
**On evidence strength, which the proposal was honest about:** one run, one repository, below
this file's own bar of the same disagreement twice. Accepted anyway, and the distinction is
worth keeping — **frequency evidence is what a claim that a rule is *wrong* needs; a claim
that a gap *exists* can be carried by structure.** The window here is provable by reading the
phase order, without waiting for it to recur. **Minor** — one new phase rule and one standing
rule, no schema movement.

**0.33.0** — eight rules drawn from a twenty-two-round two-party protocol run between a real
application and its forked backend, merged after research established which already had
names. **Five did, and each is stronger for it.**
**Two surfaces answering one question** must be shown to agree with only one routing — three
occurrences in one project, two of which shipped, including a router that returned zero
records from a fourteen-record input in silence. **A defect near a contract boundary is
yours until proven otherwise**, after a project came within one step of reporting its own
defect to its upstream as theirs. **A sent artifact is immutable even when the revision is
an improvement** — the protocol's own rules permitted revision and it still went wrong three
times, so a permission to revise is not a reason to. **Verify a peer's artifact against
their committed copy, never the delivered file**, which matches distribution guidance to pin
an immutable reference rather than fetch a pull request's diff.
**Committed is not published**, and reading an unreleased draft makes it your decision. This
is the one rule research could not name: branch-graduation models are adjacent but they are
the recipient signalling acceptance, not the author controlling readability. **Marked as
unverified against prior art rather than presented as established.**
**An identifier answering half a question while appearing to answer all of it is worse than
one answering none** — it stops the reader asking — and the name a human sees is part of the
interface, because metadata inside a file does not help anyone reading a directory listing.
**And a claim about review is not a claim about currency**, which turns out to be the
**as-built bill of materials**: recording which revisions were actually assembled and
verified together rather than which are current, standardised in configuration management
long before software. Its companion arrived with it — **form, fit and function** is the
older and better test for a breaking change: a part may be revised only if every previous
revision is fully replaceable, and otherwise it gets a new part number. That is a major
version bump, named decades earlier.
**Three citations replace three assertions.** The mesh record generated from endpoints is
established practice — catalogue systems state that processors deduce relations and that
produced relations are authoritative, and contract brokers derive their matrix the same way.
Approved pairs have four existing names and mature tooling. And the caveat that matters most
here: **almost every coordination tool assumes CI can test, and the best-known ones assume a
local working copy** — where either fails, fall back to records rather than mechanisms,
because the discipline transfers when the tooling cannot.
**Not added: a proportionality rule for coordination cost.** Research found no tooling and no
published measurement aimed at one to five people; the field is enterprise-only. The
judgement stands unmeasured and is left out rather than dressed as a finding.
**Minor** — new rules on existing sections, no schema movement.

**0.32.2** — a lineage audit against every earlier version still on disk (0.17.0, 0.26.0, the
0.27.0 split core, the recombined 0.28.0, and all seven extracted modules), checking whether
anything intended had been lost rather than only bugs. **Twelve references still pointed at
module filenames that no longer exist** — `agents.md`, `choosing.md`, `handoff.md`,
`release.md`, `validating.md` — left behind when 0.28.0 folded the modules back in. A run
following any of them finds nothing. All twelve now name sections. **The cross-reference check
that passed on 0.32.0 missed every one of them**, because it looked for bolded section names and
these were backticked filenames: a checker whose pattern is narrower than the defect class it
claims to cover, which is the fail-suppression shape in a different place.
**Everything else verified present.** The units that did not match verbatim across 0.17.0 and
0.26.0 were deliberate supersessions, structural scaffolding from the abandoned split, or
line-wrapping — confirmed by whitespace-normalised comparison, which found all ten `WHY`
comments intact, the informed-or-instructed judgement, the vendored-copy drift rule, and the
scaffolding-path limitation all still present. **Patch** — twelve pointers corrected, no rule
changed.

**0.32.1** — audited, and the audit is the entry. Eleven integrity checks pass: fences and
`<constraints>` balanced at 43 each, two waits, ten dimensions, ten phase blocks, eight statuses,
history newest-first with the frontmatter matching its head, no dangling cross-reference, no
trailing whitespace. **Thirty-three lines removed and no content with them** — twelve doubled
`---` separators left by earlier splices, and nine runs of three-or-more blank lines.
**The measurement that matters is about this log, not the rules.** Provenance is 765 lines and
is never read during a run. Its thirty entries before 0.20.0 average 118 words; its eighteen
entries from 0.20.0 onward average 348. **The recent entries are three times the length of the
house style they were added to**, and they account for 569 of those 765 lines. That is this
file's own bloat finding, aimed at this file, and it is recorded here rather than acted on
because shortening them means choosing which incident detail to drop — a decision with a real
cost and not one to take while a research pass is outstanding. **Patch** — whitespace only, no
rule touched.

**0.32.0** — cross-repository contracts, which were twenty lines and assumed a vendored
interface file with fetch metadata. **The section now opens by telling you not to use it:**
publish through a registry and depend on a version, because that is the only mechanism with
resolvers, ranges and update tooling already built. A contract is the fallback for coupling a
registry cannot express — a command-line surface, a binary's argv, a wire format, a pinned
upstream commit — and one adopted where a dependency would have done is `OVER` of the
expensive kind, maintained by people rather than tools.
**For a pair: record the direction first.** One side owns the contract, the other mirrors it,
and both decision records say which. A contract both sides edit is two files that happen to
agree today. **The pair is the unit, not the version** — what gets approved is a combination,
and neither number alone says whether they work, so the artifact must name the pair that
produced it. Where the provider is outside your control the only lever is pinning, with the
reason recorded and a condition for moving. **And a fork is a contract with itself:** every
carried patch needs a retirement condition or the divergence accumulates past anyone's
ability to justify or remove it.
**At three the problem changes shape, and not gradually.** Two repositories have one
relationship; five have up to ten. **No per-repository record can see the mesh**, because
each describes an endpoint and a contract lives between them. Named shapes: one provider and
many consumers, where a change breaks some and the provider hears from whoever complains
first; the diamond, where two correct versions cannot be installed together; and a file
copied into many repositories, which drifts as many ways as there are copies.
**On that last one the trade is known rather than argued, because this file made the mistake
and reversed it in 0.27.0 and 0.28.0.** One fetched source has no drift and fails closed when
unreachable. Copies with a version stamp and a check permit drift and make it visible. A
registry is best where the thing is packageable, and most shared configuration is not.
**Stamped copies with a check is the default, because the alternative's failure mode is worse
than its own** — and an unchecked copy is the same drift minus the knowing.
**Two constraints close it.** Do not build a coordination mechanism before the second
instance of the problem — a protocol designed from one example is wrong in the way that
example was unrepresentative. And do not let a mesh acquire a central registry nobody
maintains: a file listing every repository and its contracts is the obvious answer and the
first thing to go stale, **one more copied file with the same drift problem, except now it is
the map.** Generate it from the endpoints or do without. **Minor** — one section rewritten
and expanded, nothing removed, no schema movement.

**0.31.0** — from deliberately hostile probing rather than from a run: what happens when this
file meets a repository it was never built for, or a correct approach it does not recognise.
**Every dangerous case turned out to be one class.** A proof-assistant repository whose
correctness argument is a machine-checked proof, not a test suite. A content-addressed build
where pinning is meaningless because the dependency *is* its hash. A documents, dataset or
infrastructure repository with no build to gate. A monorepo with independent per-package
versions and nothing to reconcile against one tag. Generative tests with no stable collection
count. In each, a dimension's **premise about the repository is false — and the rule does not
become lenient, it becomes wrong, confidently.** `N/A` now covers a false premise alongside
tier and plan, and the premise must be named as the reason. **A `GAP` raised against a
premise that does not hold is the worst output this file can produce**, because it is
specific, confident, and asks the human to break something that was right.
**Unfamiliar is not wrong** joins it. These dimensions encode practice known to work, not
everything that works, and the absence of a rule is a fact about this file rather than about
the repository. Where something is unusual and cannot be shown defective: say so, rate what
you could establish, ask the human. **Rating a defect from unfamiliarity alone is how a
standard degrades a repository towards its author's habits** — which, given that every rule
here came from one person's estate, is the specific way this file would do damage.
**And precedence is settled: a recorded repository convention beats a rule here, inside that
repository.** This is guidance a maintainer chose to run, not authority over a decision they
already made and wrote down. A convention with reasoning in the decision record outranks this
file and the divergence gets recorded so no future run re-raises it; a convention with no
reasoning anywhere may be raised normally; a genuine unrecorded conflict is a **question, not
an amendment** — the run does not get to settle which standard a repository follows.
**Three cases still have no rule and are now named in Limitations** rather than left to be
discovered: a fork whose upstream is dead, a prior decision record written by a different
standard that re-check will read as its own, and a repository containing this file. Each
produces no opinion rather than a wrong one, which is why they are tolerable.
**Minor** — new rules and one widened status definition; no field renamed, no tally change.

**0.30.2** — a measured refactor, and a small one, because the measurement said so. A scan for
near-duplicate passages found twelve pairs over an 18% shingle overlap; **ten of the twelve
were a rule against its own Provenance entry, which is what Provenance is for** and is never
read during a run, and an eleventh was the same principle applied to two different tables.
**One was real:** the deny-pattern rule stated twice, five lines apart, both opening "The
general rule" — introduced in 0.21.2 when the enumeration block was replaced and the earlier
statement left standing. Merged, keeping what each said that the other did not.
**The standing rules are now grouped under four headings** — gates, evidence, honesty,
posture — rather than running as twenty-one undifferentiated bullets accumulated by
accretion, each appended wherever it landed. No rule was reworded, moved between groups or
removed; only headings were added.
**What the measurement refused:** the audit read path is 2,297 lines of 4,349, so routing
already halves it; Provenance and the testing procedure are 956 lines correctly excluded from
every run; and the anecdote strip proposed twice before measures 238 lines, five per cent,
and remains not worth the rewrite. **A refactor proposed to match a request rather than a
measurement is the thing this file rates `OVER`.** **Patch** — one merge, four headings, no
content removed.

**0.30.1** — one rule, earned twice in two days. **Enabling a feature is not the same as
satisfying what it needs.** A dependency tool was configured to bypass its own schedule for
security advisories — deliberate, correct in intent — against a token scoped without the
permission that reads them. The block would have been inert: no failure, no error, nothing
reported, reading as coverage. v0.29.0's fail-suppression rule does not reach it, because
nothing was suppressing a failure; the feature simply had a precondition nobody checked, and **a
feature that cannot run has nothing to report.** Preconditions worth reading each enabled option
against: a permission the token lacks, a credential never set, a platform feature off at the
repository, a plan tier the account does not hold. Where one cannot be satisfied, remove the
option rather than leave it as decoration. **And the second half is when to look:** this was
caught in a configuration that had not shipped yet, while the same defect in an older workflow
had been green for a year. The cost falls entirely on timing, and a change not yet landed is the
cheapest moment there will be. **Patch** — one rule on an existing dimension, no schema movement.

**0.30.0** — four changes from research into how well-run projects actually work, and what a
single maintainer should refuse to copy from them.
**The decision record is reframed as the review function, which is what it always was.** A
second reviewer contributes two things — catching what the author cannot see, and holding a
position the author has since talked themselves out of. The first cannot be recovered alone;
**the second can, and this record is how.** Past-you has no stake in today's mood and no
appetite for the thing you now want to do, which is what a reviewer supplies. It only works
if the reasoning was written at decision time, so an entry carries the argument rather than
the verdict, and a re-check reads the prior reasoning **before** forming a new opinion — the
other order consults the record for permission. One refusal criterion comes with it that
needs no second opinion: **unbounded refactor cost**, the antidote to *I could just do it*,
with the trigger being that the refactor becomes bounded.
**Some checks cannot pass at one maintainer, and chasing them makes things worse.**
Code-Review needs a second approver and its own documentation calls it infeasible for a
single participant; Contributors needs several organisations; branch protection's higher
tiers need reviewers. Mark them `N/A` with the reason, as deliberately as an unverifiable
fact is marked. **The trap is sharper than wasted effort and is the clearest `OVER` case
here: a required-review gate you bypass every commit lowers the score, because the repository
then looks unreviewed rather than unreviewable.** Ceremony that cannot pass its own check is
worse than its absence.
**Build attestation joins signed releases** as the other cheap half of provenance — no key to
manage, nothing local, and the highest-leverage release-side step available without a
development machine.
**And one-concern-per-change gets its measurement.** Across 1.5 million review comments,
usefulness falls as files-per-change rises, and build and configuration files generate the
least useful comments of all — which is exactly what amendments touch. The rule was already
here on judgement; it now has a number. **Minor** — new rules, no schema movement.

**0.29.0** — six changes from a full cycle on a live T3 production application: twenty-two
amendments raised, thirteen applied across twelve commits, four green CI runs, merged.
**`constrained` joins `validated`, because `validated` alone would prune exactly wrong.**
Sixteen entries across three runs credited execution rules almost without exception — not
because posture rules are worthless but because **the instrument can only see rules that
catch.** Do not pre-select, both consequences, two waits, never substitute, re-ask a blank:
none can ever appear in `validated`, and they are the rules that make a report worth reading.
Three constraint events were already sitting in prose where nothing could count them.
**The parent-commit test.** Every gate defect across two repositories shared one property:
the gate was written in the same change as the thing it guards, so it had only ever been
seen agreeing with a state already correct. The parent commit is its one unseen state and
costs a checkout. **A gate's condition must also be proven to see what it tests** — a
step-level `if:` on an unavailable secrets context reads as a gate and performs no check,
and mutation cannot catch it, because mutating the subject changes nothing about a condition
that never read it.
**A step configured not to fail is not evidence at any depth.** A coverage upload reported
success at the rollup, the job and the step while its log read `Token length: 0`; it had
never uploaded anything in its history, and the test plan called it a live capability. Read
the suppression switches at Phase 2 with the triggers: a step that cannot fail is read from
its output or recorded as unrun.
**Measured-and-not-built is a result and gets recorded.** Twice a run proposed a guard,
measured its false-positive rate against the real tree, and declined to build it. An enforced
rule with a standing false-trigger rate is one people route around, and both would have been
`OVER` next audit — but unrecorded, the same question costs the same work again in six
months.
**And the most repeated finding across the whole programme is now named as a class:** a
document asserting a state that is not true. Three documents saying an application was not
live while it served production, a test plan describing an upload that never worked, a file
declaring its own questions resolved two sections above listing them open, a README a version
behind its release, a context file claiming to be loaded by sessions that never loaded it.
None is a missing file, so presence checks miss all of them. **Check the claims, not the
files.** **Minor** — new rules and one optional emission block, no schema field renamed or
removed.

**0.28.1** — a measurement, and a defect it turned up. The claim that anecdotes had bloated this
file by roughly a thousand lines was asserted twice and never checked; **measured, it is 238
lines, five per cent**, and the consolidation pass built on it would have rewritten forty precise
passages to save eleven per cent of a read path. Dropped. The same measurement showed the 0.28.0
navigation block was an H1 that swallowed all the front matter behind it, so *Scope*,
*Vocabularies* and the rest read as subsections of the routing. They are now **Before You Start**,
their own H1, which is also what makes the one-match heading index work. Measured read path for an
ordinary audit: **2,207 lines of 4,103** — routing already halves it. **Patch** — one heading
level and one sentence.

**0.28.0** — one file again, read in ranges. 0.27.0 split into a core plus seven modules on the
premise that bounding the initial read meant the depth had to live outside the attached file.
**That premise was half wrong.** A file attached to a chat does enter context whole — but a file
on disk, given an agent with file tools, does not: it is read with an offset and a limit, or
indexed by grepping its headings and taken one range at a time. The agents this runs on have
those tools, so **selective reading was available all along and the split solved a problem that
was not there.** The modules are folded back, nothing reworded, and *How to Read This File* now
sits immediately after the licence: build your own heading index because generated line numbers
go stale, then read only the sections your job names. Two sections are marked never-read-during-
a-run — *Provenance*, and the procedure for testing this file — which is where the old split's
real saving came from anyway. What 0.27.0 got right is kept: **a run that finds this standard
wrong proposes a `class: standard` amendment at the gate**, with the quoted rule, literal
evidence, proposed wording and both consequences — and it never edits itself. Gone with the
modules: per-repository drift, the manifest, the checksums, the install amendment, and four
states to resolve at Phase 2. **Minor** — no phase, dimension, status or tally moved.

**0.27.0** — **the file split.** One core plus seven modules written into `.standards/` in each
repository, because attaching a file puts all of it in context however well it routes — internal
routing saves attention, not tokens, so bounding the initial read meant the depth had to live
outside the attached file. The core is 2,229 lines against 3,933 and **is complete on its own**:
a repository that has never seen this standard gets a full first audit with nothing else
present. That is forced rather than chosen — writing modules is a repository change, and nothing
may be written before Phase 6, so the install is proposed at the gate like any other amendment
and declining it costs only that later runs read the whole core again.
**Three states, resolved at Phase 2 and recorded:** absent (first run, core-only, supported),
present and matching (read on demand), present at a different version (a dimension 2 finding,
naming both versions rather than silently preferring either). A fourth, checksum mismatch, means
a module was hand-edited and the core's rule is read instead — a module that disagrees with its
own checksum is evidence of nothing. **Per-repository drift is the accepted cost of this
distribution model**, taken deliberately over a shared source that needs a network fetch and
fails closed; the trade is that drift is permitted and made visible on every run.
**And the standard can now propose changes to itself**, as `class: standard` amendments at the
gate, carrying the quoted rule, literal evidence from that run, the proposed wording, and both
consequences. **It never edits itself** — a standard that rewrote its own rules mid-run would
change what every future session believes on the authority of one session that will not be there
to live with it, and self-written instructions are the measured weaker case. Evidence is
required and one run is thin: a single disagreement is a data point, the same one twice in
different repositories is a defect, and the proposal says which. Paired with the `validated`
block, which records rules that earned their place, this is the instrument for retiring rules
that stopped earning theirs.
Nothing was reworded in the move — modules carry the text verbatim from 0.26.0 — and every
cross-reference in the core was retargeted to a module filename. **Minor** — no phase, dimension,
status or tally changed, so 0.26.0 reports still diff.

**0.26.0** — the first cycle to close with a green remote conclusion, and two rules about
how to read one. **The rollup is not the result.** *Local green is not remote green* sent the
reader to the run conclusion, which is exactly the level at which **a job or test that
silently did not run looks identical to one that passed** — so the existing rule, followed
precisely, would have accepted a tick that proved less than it appeared to. The run read at
job and log level instead and established three things the tick could not: that the
downloaded scanner was checksum-verified before execution, that a newly added guard ran
rather than skipped, and that a widened gate reached every workflow. Reading the skip list
and quoting the log line for any gate an amendment touched is now part of the rule.
**And build gates whose absence is visible.** The only reason that guard could be shown to
have executed is that it emits two named skip lines when it does not, and neither appeared —
a property of how it was written, not of what it asserts. **An assertion that never runs is a
gate in name only**, so a gate should say by name when it is not running: a named skip
reason, a printed marker, a summary line. **Minor** — two new rules, no schema movement.

**0.25.0** — the answer to one held-open question, and a structural blind spot it exposed.
**A trigger only watches what it is worded about, and the tier has two axes.** The re-check
moved a project from audience A1 to A2 — a team maintaining what it produced, another reading
its output — and **not one recorded trigger fired.** Every one was phrased about the
repository: a second person commits, a second person gets access, the repository goes public.
The committer had not changed, so nothing caught a tier axis moving. Using a thing and
committing to it are different populations, and the record was written as though they were
one. Triggers are now worded in the terms of the axis that would move them, and a trigger set
mentioning only one axis is named as a blind spot on the other, even on a run where nothing
fires.
**A third state exists between fired and not fired: the decision stands and its cost has
changed.** The same run found an accepted risk whose stated cost was an audit log that could
not name who made a change. No trigger fired and the decision was still right — but the
population had gone from one to several, so the cost changed in kind: from naming nobody
because there is only one candidate, to being unable to distinguish people who are now
genuinely different. **Record the changed consequence; do not re-propose the item.** An
amendment argues for a different decision; this is the same decision described accurately,
and collapsing the two re-litigates a settled question through the back door.
**A version that reached the default branch was published, tag or no tag.** Following the
0.22.0 rules, the run checked and found a version that sat on `main` for over eight hours
before being replaced by a lower one — absent from tags, absent from releases, and the only
place the number had ever been. Anyone cloning in that window holds a tree declaring it.
Establishing version history now means reading the manifest's history on the default branch,
because a record whose supporting facts are all about tags, releases and binaries has
established nothing about the branch. **Minor** — new rules, no schema movement.

**0.24.0** — the apply half of that same T3 run, which reached a place no previous run had:
five commits pushed, every local gate green, and **nothing server-side had run at all.**
**Check the workflow will run on the branch before promising to read its conclusion.** The
repository's CI triggers on the default branch and on pull requests, and the work sat on a
feature branch, so the result was zero workflow runs — **absent, not pending.** Every gate on
that work stayed local-only and *local green is not remote green* had no way to be
discharged. The `on:` block is now read at Phase 2 and stated at the gate, where the human is
still deciding, rather than in a completion report where the answer is already fixed.
**A gate that matches text can be satisfied by its own documentation.** Asked to prove a
downloaded binary was checksum-verified before execution, the run's first gate searched the
raw workflow for the verification command and matched it **inside the comment the same commit
had just written explaining the verification** — passing 23 checks with the real check moved
to after the binary ran. It caught this itself, rewrote the gate to parse YAML and compare
executable lines, and proved it by mutating the guarded thing three ways. Both halves are now
rules: match structure rather than text, and prove a gate by breaking what it guards rather
than by watching it pass once.
**A blank answer at a wait is not an answer.** An option template came back with its
placeholders unedited; the run applied the recorded default and declined to re-ask, reasoning
that a second ask would be a third wait. **The ceiling counts gates, not round trips inside
one** — a question asked again because the reply was empty is the same gate, still open — and
that reading cost the one answer four of six live triggers depended on. Ask once more, name
what the blank costs, then take the default. **Minor** — new rules, no schema movement.

**0.23.0** — **the first run above T1**, on a live internal application: T3, blast radius 3,
and the first tally with no `N/A` and no `UNVERIFIABLE-HERE` — every dimension rated on
evidence. The tier model had sat at its floor for every previous run, so most rules keyed to
tier had never fired. Five changes, one of which threatened everything else in the file.
**Never read an exit status through a pipe.** The run recorded `pytest … | tail -25` as
`exit 0`; that was **tail's** status, and tail succeeds at truncating failed output. Unpiped
it was `exit 1` with four collection errors, and the run's largest finding would have been
lost. It caught itself and filed it under `corrections` rather than quietly re-running. This
**voids every other evidence rule at once** — the output looks literal while the status is
fabricated by the pipeline — so it now sits beside *evidence, not assertion*, with the tell
named: output shortened for readability is where the status went missing.
**`waits_observed` is defined for an audit that stops at the gate.** This run answered 1,
reasoning the job stops by instruction; two earlier runs answered 2 in the same shape of job.
The spec named only a full run and a survey, so both were defensible, which makes it a
determinism defect rather than a run error. **Count a wait when you stop at it** — the field
exists to catch a skipped gate, and a run halted at Phase 6 skipped nothing.
**The three Phase 0 questions now ask at Phase 3.** Three independent runs each folded them
forward and each recorded the same override with the same reasoning: two waits is the floor
and the ceiling, Phase 3 already stops and already asks about copyright, and a third round
trip costs more than it returns. **A deviation that recurs with the same reasoning is a rule
waiting to be written.**
**A gate must not claim more coverage in its failure message than it checks.** The run found
a custom gate whose message said the default token scope "must not be relied on here" while
testing only workflows that call `gh` — and the one workflow missing its `permissions` block
was CI itself. A gate that overstates its reach is worse than an absent one: a missing gate
invites a check, a lying gate forecloses it.
**Verify what the gate downloads before it runs, starting with the security tooling.** Both
workflows fetched a secret-scanner binary over the network and executed it with no checksum —
in the job that is the primary credential defence. The version was pinned, which pins what
was asked for and not what arrived. **Minor** — new rules and one clarified field, no schema
movement.

**0.22.0** — **the version scheme becomes a recorded decision.** Dimension 10 already
reconciled manifest, tag, changelog head and installed distribution, and already fired the
changelog requirement on distribution rather than on tier. What it never asked was whether
anyone had decided what the number *means* — so four numbers could agree perfectly while the
next person to bump one was guessing, which is where reconciliation breaks. That is now
`DRIFT`, answerable in one decision-record entry: which scheme, what counts as major here,
whether pre-release labels are used, and what leaving one requires.
**The scheme is semantic versioning, and no choice is offered.** A draft of this entry
presented dated versioning as a supported alternative for software nothing imports; it is
removed, because an option this file's maintainer will not take is weight on every run that
reads it — the same test applied to any rule that stops earning its place. What survives is
the reason the decision is recorded once and not revisited: **a version scheme is close to a
one-way door.** A dated version outranks any later `1.2.3`, so a project moving off one
publishes something that sorts below what is already out, satisfying none of the ranges a
consumer wrote, with no escape but jumping past the old numbers permanently. Semantic is
where you start if you might ever need the promise, and possible external dependence rather
than certain is enough. It is also the more widely supported as tooling rather than taste —
a specification every major resolver implements, required outright by Go modules. **One line
covers the case this leaves open:** an inherited or vendored project already on a dated
scheme is recorded and left alone, because **renumbering an existing version history is
never the amendment** — it breaks every pin and every reference to a release already out, to
fix something that costs nothing.
**Padded fixed-width fields are ruled out, with reasons rather than preference.** `01.02.003`
is not a conforming semantic version — leading zeros are forbidden — Python packaging
normalises it away so the installed distribution and the tag disagree permanently, which
manufactures a `DRIFT` on this dimension's own reconciliation on every future run, and a
fixed width is a ceiling whose remedy is renaming history. The lexical-sorting problem it
solves is already solved by every version-aware tool and by `git tag --sort=v:refname`; where
something genuinely needs lexical sortability, pad the filename and leave the version alone.
**And the finding no published standard can give you, because none of them knows the tier:
a version makes a stability promise and the tier says who is relying on it.** `0.x` at T2 or
T3 is not automatically wrong — this file is a long-lived `0.x` — but the statement of what
it means and what would earn `1.0` has to exist. `1.x` breaking consumers in minor bumps is
`DRIFT` with the changelog as evidence. A pre-release label with no graduation condition is
decoration, and one that outlived its condition is `DRIFT`. Mechanics stay cited rather than
restated, because a house paraphrase of a published spec is a second source of truth that
will drift from the first. **Minor** — new rules on an existing dimension, no schema movement.

**0.21.2** — the first run to reach Phase 9. Eight amendments applied in eight commits by
concern, pushed, remote CI green, the default branch correctly left for the human. Two
changes, and the field out-engineered this file on one of them.
**A substitution at apply time returns to the gate.** Approved to narrow a set of overly
broad deny patterns, the run found the narrowing could not be expressed safely — measured,
not asserted, against sixty thousand generated filenames — and moved the file out of the
denied namespace instead, leaving the deny rules untouched. It declared this in the commit,
the decision record, the report and the summary, and named it a weakness in its own
conformance block. Nothing here covered the case, so Phase 7 let it proceed on disclosure
alone. It should not: approval is per mechanism, because a different mechanism carries a
different consequence and the human accepted the first one. **Thorough disclosure is
integrity after the fact; it is not consent.** The rule now stops that amendment, applies the
rest, and reports it unapplied with the substitute proposed.
**And then adopts the substitute, because it is better than what this file shipped.** The
`.env.example` conflict has now had three fixes. Excluding the example inside the glob is
unauditable, which is what that filename sweep proved. Enumerating the secret-bearing files,
which 0.21.0 did, is auditable but fails open on the first `.env.staging` anyone adds.
Renaming the example to `env.example` and leaving the glob broad has neither failure and
needs no list — so the enumeration is backed out and the template returns to `.env*`. The
cost is one line in the README, because a contributor will look for the dotted name.
**Worth recording separately:** that run's secret scanner caught the run's own commit, when a
literal private-key header went into documentation, and the fix was to describe the trigger
strings rather than exclude the file. Unplanted, so it is better evidence that the control
works than any deliberate plant. **Patch** — one new Phase 7 rule and one template change.

**0.21.1** — the same run again, corrected, which earned three things 0.21.0 did not reach.
**The probe rule gets its crux.** 0.21.0 said sanity-check against upstream; the better test,
which the run articulated itself, is **whether the source is in a position to know.** A
pinned tool's bundled index is frozen at that tool's release date and cannot be current by
construction, while answering instantly and authoritatively — and the same holds for a
container image's package lists, an offline mirror, or any resolver's view of what it can
install, which describes reachability rather than existence. Corroborating from inside the
repository joins it, because the strongest evidence in that run came from neither API:
wheels for the newer interpreter already sat in the committed lockfile, proving the
dependency graph had moved while the gate had not, and needing no network.
**Coverage is shape-dependent, so plant the shape that actually occurs.** The run had
discharged the prove-the-scanner rule honestly with a canonical provider key, then found the
same scanner missed a backticked bare `VAR=value` in markdown and Python alike — the ordinary
way a credential arrives, pasted out of a terminal. The recorded claim was true and the
confidence it carried was wider than the tool, so dimension 5 now asks for two plants and
records which shapes were proven rather than that the scanner works.
**Two optional emission blocks are adopted, both invented by the run.** `validated` quotes a
rule and says what it caught that reading would not have — **the only thing in this file that
reports back on the file**, and the evidence needed to retire a rule that has stopped earning
its place. `corrections` records a claim this run or an earlier record got wrong, and stays
even when no decision changed, because an overconfident claim that shifted no rating still
misleads whoever reads it next. Both are additions, so `fields_added_beyond_schema` must say
`yes` and name them — the run emitted both and answered `no`, contradicting itself in the one
field that exists to catch exactly that. **Patch** — optional blocks only, no required field
moved, and 0.21.0 reports still diff.

**0.21.0** — **the first live audit run, and four defects it found.** One recheck run against
a real repository, stopping at the gate. Posture held: two waits, nothing written, no
amendment pre-selected, both consequences on every one, zero actions needing a local clone,
nothing declined re-proposed with no trigger fired, and a self-assessment that volunteered a
weakness no reviewer would have found. The defects were all in this file.
**A probe is only as good as its source.** The run queried its own package index, read Python
3.14 as a release candidate, and withdrew a correct finding — the index was about a year
stale, and 3.14 had been stable for eleven months. Nothing was fabricated; the evidence was
real and the source was wrong, which is harder to catch because a withdrawal reads as
diligence. *Facts with an Expiry Date* now carries the rule: date the answer, sanity-check
against upstream rather than a mirror, mark `UNVERIFIABLE-HERE` when upstream is unreachable,
treat a stale index as a dimension 2 finding in its own right, and **hold a withdrawal to the
same evidence as a finding**, because nobody audits an absence.
**The deny template blocked the audit.** `Read(.env.*)` and `Bash(cat .env*)` both match
`.env.example` — the committed file holding no secret that dimension 7 requires reading for
its placeholder convention. The run hit it, refused to route around it, and handed the check
back as human action. The template now names the files that actually hold secrets, and the
general rule is stated: a deny pattern covering a file the audit must read has not hardened
the repository, it has blinded the audit, and deny beats allow so the narrowing must happen
in the deny.
**Verify the context file loads; do not infer it from the file existing.** The run proved
`AGENTS.md` reached no session by listing what the harness had actually loaded — the shim
linked to it in markdown instead of importing it, so 62 lines of module map and commands were
dead while both files claimed otherwise. That check is now named on dimension 4, and it is the
highest-value single check there, because the failure is invisible from the filesystem.
**Describing the collection guard did not work, so it is written out.** A guard built from
this file's prose fired only at zero: eleven tests to seven, guard green, exit 0. The CI
template now carries working code with a committed baseline, and an empty count fails rather
than passes — a collection command printing nothing has not found zero tests, it has failed
to run. **Minor** — no schema movement, and every change is a rule or a template.

**0.20.0** — selective intake from the self-evolving-agent literature, on one filter: this
file configures repositories and does not become an agent-building guide, so only what
changes an audit finding came in. Instruction-adherence decay is now a measured number
(about 5.6% per function, replicated) cited where the gates and the conformance block
already leaned on it, and what earns context tokens got its measurement too — named tool
commands used two orders of magnitude more when the file names them, repository overviews
earning nothing, and the same guidance helping one model while hurting another, which
hardens minimal-over-complete. **Dimension 4 gained three rules with precedents:** hooks
are executable configuration and every one is read, because a published vulnerability ran a
repository's hooks before trust was granted; installed skills and plugins are dependencies
with instructions inside and are audited as dependencies, because marketplace audits found
roughly a third of published skills flawed; and the files that instruct future sessions —
context file, enforced layer, hooks, skills — change only through the gate, never by
in-session writes, because self-written instructions are the measured weaker case.
**Dimension 5 gained the independence rule** — the verifier lives where the thing verified
cannot edit it — carried by two published cases of agents defeating their own checkers, and
Validation now says plainly to trust the held-out seeded testbed over public leaderboards,
which have documented contamination. What did **not** come in: the self-modifying-scaffold
architectures themselves. The evidence puts their payoff at population-and-lab scale with a
hardened evaluator, and puts the safe form of experience memory at exactly the shape this
file already has — a human gate on every change, append-only decisions with re-check
triggers, a sealed answer key. Nothing structural moved, and that is the finding.
**Minor** — no schema movement.

**0.19.0** — one file again. The standalone test procedure written alongside 0.18.0 is
**absorbed and deleted**, for the reason 0.5.0 gave when it absorbed the last two: a second
attachment is a second thing to keep in version-sync, and that had already drifted twice.
*Validating a Change to This Standard* now carries the whole procedure — **five corpus roles**
rather than named repositories, so it travels; the order and why each step precedes the next;
the answer sheet that makes a paired run valid; paste-ready prompts; the fact checks; the
destructive tests, throwaway repositories only; what to record per run; and a **triage table**
separating a defect in this file from a bad run from a wrong fact, because the three have
different remedies and guessing wrong spends a version bump on nothing.
**`TEST-VERIFICATION-CHECKLIST.md` is finally specified.** Dimension 5 has required it from
T1 since 0.1.0 and no version ever said what belongs in it, so it was invented differently
every time — a standard mandating a file it never defined. Its template is now in Starter
File Contents, and the two cadences are stated plainly: this file at inception and before a
release, the checklist per task. **Minor** — nothing in the emission schema moved.

**0.18.0** — the file became a scaffolder as well as an auditor, and a batch of facts it
had been asserting turned out to be stale. **Choosing a language and runtime** is a new
part: rank 5 of the irreversibility gate named the decision and nothing told anyone how to
make it, so a greenfield run picked a language silently or asked the human cold. **Choosing
the shape** joins it, and the shapes table becomes the layouts rather than the decision.
**Phase 9 sequences and sets milestones** for the configuration work this run proposed —
a reversal of "no roadmap, no backlog file", made because sixteen amendments with no order
of operations is a pile rather than a plan; the boundary is that it may sequence work it
proposed and may never sequence the product, and the plan's home defaults to platform
issues rather than a tracked file that drifts. **Starter file contents** carries literal
text for eight files, because an agent asked to generate one writes a different one every
run and that is what breaks the determinism test. **The configuration file map** answers
why each file sits where it does, which was scattered across four dimensions.
**Facts with an expiry date** collects every version, price and plan limit in one dated
table, with the rule that a fact used without checking makes its finding
`UNVERIFIABLE-HERE` — a standard that names tooling starts rotting the day it is written.
**A conformance self-check** closes every run, for the case where the model is not the one
this was written against. Corrected against current platform behaviour: **rulesets carry
the same plan gating as branch protection**, so they are not the free-tier escape and the
public-or-pay decision is now raised explicitly; **published release tags and assets are
immutable**, which moves the whole of release verification before the Publish button;
**dependency-update cooldown is a platform default**, making a hand-rolled delay `OVER`;
**platform secret scanning is free on public repositories and paid on private ones**, so
the finding differs by visibility. **Deny rules do not bind a script the agent writes**,
which bounds what dimension 4 may claim, and **a context file that arrived with a
dependency is an input to be read, not trusted**. **Claude Code still does not read
`AGENTS.md` natively**, so the shim stays and the table says which tools need one.
The instruction-file assumption is now attributed and qualified rather than asserted.
Structural repairs: a `yaml` fence in Phase 0 that opened thirteen lines early and swallowed
the capability probe, three orphaned sentence fragments, a version history that said
newest-first and opened with 0.3.0, and **a `WHY` comment sitting between two rows of the
dimension-status table**, which split it so that five of the eight statuses rendered as raw
text rather than as table rows. That one had survived since the table was written.

**Three rounds of testing before release, and the corrections they forced.** Testing was
mechanical and factual only — no agent run, so tests A through F remain unexercised on this
version. Round one checked every dated fact against its source and the file against its own
rules: **immutable releases turned out to be a repository setting rather than a default**,
which the first draft asserted flatly, and the correction brought with it the draft-first
publish order that the flat claim had hidden; **the cooldown rule was too broad**, calling a
deliberately longer window `OVER` when only a window matching the default is redundant;
**the paid route for a personal account is GitHub Pro**, not an organisation plan, and push
rulesets are gated higher than branch rulesets; and the symlink alternative is documented by
the vendor rather than improvised. Round two found the split table. Round three re-derived
the dimension count, the wait count and the status precedence by a second method and
confirmed they agree, and found no quantity stated twice with different values. **Tests F
and G are new and come from this**: cross-model comparison, and a mechanical-checks list that
every defect above would have been caught by.

**Minor, not major** — the ten dimensions, the tally, the statuses and the phase numbering
are unchanged, so reports from 0.17.0 still diff.

**0.17.0** — durability, delivery, and forks. **Nothing exists until it is pushed**: a commit
on an unpushed branch dies with the container, and a fetch has already pruned a local branch
whose remote counterpart never existed — Phase 7 now confirms the branch and head on the remote
by reading the remote ref, and emits `pushed` with its proof. **Open a pull request rather than
merging**; merging is the human's, doubly so where a sibling contract exists. **Writing the
report is not delivering it** — a scratchpad in an ephemeral container is gone within the hour,
so the file is handed over in the same turn and `report_delivered` records it. **The default
branch is read, never assumed `main`** — a fork often keeps a branch named for its purpose, and
every rule reasoning about "the default branch" means the one the repository actually has.
**Forks get their own rules**: divergence, whether upstream is alive and taking fixes, and
whether a privately carried fix should go upstream — a fix held locally is a mitigation with no
removal condition. Re-syncing and rebasing are never proposed; they are direction, not
configuration. **Byte-identical shared files must be asked about**, since a session cannot see
the sibling to discover them, and are listed in the report so the other side's run can be read
against it.

**0.16.1** — a one-line pointer to how you start it, near the top. The prompt was otherwise
only in Sending Results Back, twelve hundred lines down, which is no use to someone opening
the file for the first time.

**0.16.0** — renamed. Agent configuration is one of ten dimensions, and the old name
advertised the smallest part; this scaffolds, retrofits, audits, gates releases and prunes.
**Released under CC0 1.0** — public domain, no attribution, so it can be taken and changed by
anyone. **Versioning restated around its only consumer**: the number exists to tell a reader
whether two run reports are comparable, so major means the schema stopped diffing cleanly and
1.0.0 arrives when the schema stops moving. The previous criterion — two consecutive clean
runs — was arbitrary and could be luck. Batch changes rather than bumping per edit.

**0.15.0** — portable by detection rather than by assumption. **Environment facts are
probed, not asserted**: shell, writes outside the repository, remote CI readability, tag
creation, third-party repository access and clock agreement are each established at Phase 0
and recorded yes/no/unknown, with a stated degradation for each absence — without a shell,
documented commands are recorded unrun; without an external write, the report goes in the
reply. **Three facts that cannot be detected are asked once**: whether a local working copy
exists, whether a shared standards repository exists, and who holds copyright. **Identity is
no longer hardcoded** — no account name, no organisation, no default standards repository.
**A file existing is not evidence it says the right thing**: an expected file is read and
confirmed before its dimension reads `OK`, since a stub checklist and a workflow that runs
nothing both pass an existence check. **The run report opens with a reconciliation header** —
standard version, tool, mode, tier, tally, absent capabilities, deviation count — so two runs
diff mechanically, and **deviating is allowed while hiding it is not**: a run that departed
and said so is more useful than one that complied and learned nothing.

**0.14.0** — efficiency and portability pass. **Agent-layer terms** — context file, tool shim,
scoped rules, enforced layer, tool-server config — so the body names concepts and only the
shell blocks name one tool's paths. **A shape not in the table follows its own ecosystem's
convention**, named and sourced rather than invented. **Version history compressed** below
0.9.0 and marked never-read-during-a-run; **the validation protocol reduced to a table**.
**Eight `<!-- WHY -->` notes** on the decisions a later maintainer would otherwise simplify
away — the closure rule, `OVER`, `strength`, two waits, five forced decisions, the gate as a
file, commit-by-concern, and triggered declines.

**0.13.1** — the version goes in the filename, `PROJECT-BOOTSTRAP-AND-AUDIT-v<version>.md`, so
copies of different versions coexist and an attached file identifies itself before it is read.
The frontmatter stays authoritative and a filename/frontmatter mismatch is a finding. Prompts
name the standard rather than the file, so a bump does not stale them.

**0.13.0** — orientation and portability. **Goals, assumptions and limitations** are stated
rather than implied: the design rests on instruction files being weak, accretion being the
failure mode, and stakes having two axes, and each of those could be wrong. **Any Agent, Any
Tool** maps every Claude Code path to its portable equivalent, with `AGENTS.md` canonical —
and says plainly that **the enforced layer has no portable equivalent**, so on a tool without
deny rules dimension 6 reads `N/A` rather than `GAP` and the guarantee moves server-side.
**Sending Results Back** gives a third party the prompt, the single file that comes back, and
what is actually worth reporting — a routed-around rule first, a clean re-run last.
**Renumbered 1.x to 0.x throughout**, entries included: this was never a stable interface, and
1.0.0 is now earned by two consecutive runs needing no schema change.

**0.12.1** — the version history section was still headed "Changed in 1.3.0" nine versions
later, because entries were prepended above a heading nobody renamed. A run identified the
standard as 1.3.0 from that heading while the frontmatter said 1.12.0 — and Phase 8 records
the standard's version into the decision record, so the stale heading was propagating a wrong
version into repositories. Renamed, with the authoritative field named explicitly.

**0.12.0** — from the first release-gate run. **A removal condition must be verifiable by
running something, not by inspecting something.** A filter was recorded as removable "when
starlette imports from `anyio.from_thread`" — which it already did, while the warning kept
firing from annotations elsewhere, so the condition read as satisfied when removing the guard
would still have broken collection. **A clause fires on a built artifact reaching a person or
a machine, not on a tag existing** — a source tag for internal reference is not distribution,
and the two were genuinely ambiguous in the same sentence.

**0.11.0** — from the first re-check of a scaffolded repository. **Phase 7 states where the
work landed**: a prior run reported "applied" with green CI and both were true, of a branch —
seven commits sat unmerged while the default branch held a one-line README, and nothing asked
where the work ended up relative to it. **Deny rules cover every access path, not one
matcher**: `Read(.env*)` complied with the letter while `Bash(cat .env)` stayed open, in a
session that had already proved the `Bash` matcher fires. **Collection guards compare against
a baseline** — a guard failing only at zero catches total collapse and misses the partial fall
it was written for. **A third-party upstream may be unreachable from a session**, since
repository access is scoped to the maintainer's own; that is recorded unverifiable, never as
absence of a fix.

**0.10.0** — from the first greenfield run. **Generation happens outside the repository**:
"the run ends runnable" and "nothing is written before approval" contradicted each other
outright, since a build cannot run on files that do not exist. The scaffold is built and
gated in a scratch location, and Phase 7 copies in a tree already known green. **Outbound
licence keys on exposure rather than owner** — a personal never-public project was offered
Apache-2.0, which grants rights to nobody and misstates the intent, the same defect as an
implied MIT grant on work code. **A scanner reporting clean must first be shown to detect**,
by planting a positive and removing it; a gate that has never caught anything has not been
shown to work. **Excluding prose from a secret scan is a remedy for baseline churn, not a
default** — where no baseline exists it is only a blind spot, and the rule stated the remedy
without its precondition. **An upstream defect register** in the standards repository,
distributed by template, so a defect found once is not re-derived in every sibling and one
verification informs every consumer.

**0.9.0** — it scaffolds as well as audits. Greenfield was a single table row against a
document shaped entirely for inspection: Phase 2 had nothing to inventory and Phase 4 nothing
to rate. **Phase 2 now chooses the shape and Phase 4 generates**, in a fixed order — structure,
toolchain, entry point and one passing test, hygiene, documents — and **the run ends runnable**,
with the documented commands executed and their output pasted. A skeleton that does not build
is worse than none, because it looks finished. **Dimension 3 becomes Repository structure and
hygiene**, which keeps the count at ten and puts layout in the thinnest dimension rather than
inventing an eleventh. A new **Project Shapes and Layout** section covers eight shapes —
Python web service, CLI and scheduled job, PowerShell module, C# application, JS/TS, C with
meson, shell tool — plus placement rules for the auxiliary types that live inside them rather
than being projects themselves, and wiring conventions for composition, configuration and
entry points.

**0.8.0** — `local_mitigations` discovered rather than merely recorded; Phase 3 always stops
on a re-check; a stated premise is verified before being acted on; `not_proposed` required.

**0.7.0** — dependency source review, scoped by named triggers; upstream checked for an
incoming fix before anything is proposed; a local mitigation recorded as a liability with a
removal condition, re-examined every re-check.

**0.6.0** — one run report per run, decisions first and emission blocks appended, so nothing
has to be assembled out of a transcript.

**0.5.0** — one file. The separate reconnaissance tool and test procedure absorbed and
deleted; a router added so each job reads only what it needs.

**0.4.0** — scope and posture. Severity became `recommended`/`optional`, every amendment
gained `if_accepted` and `if_declined`, `BLOCKER` began describing risk rather than commanding
priority, and dimension 6 gained review practice for a single maintainer.

**0.3.1** — no local clone: no local tagging, no desktop `copier`, client-side hooks gate
nothing where every commit comes from an ephemeral container, and every human action must be
browser-achievable.

**0.3.0** — remote CI conclusion required before reporting done; fetch before reading refs;
lockfiles generated from the working environment; collection count part of a passing result;
re-check obligations; `N/A` for plan-unavailable enforcement.

**0.2.0** — emission schema per phase, closed vocabularies with precedence, and the closure
rule, after two runs produced 12 and 11 statuses for 10 dimensions and one invented a status.

**0.1.0** — first version: nine phases, four modes, the status taxonomy, the two-axis tier
model, the ten dimensions, and the decision record.

## Longer write-ups

**The list above is the index; these are the fuller notes from when a version landed.**
They are kept because each carries the incident that produced a rule, which the one-line
form loses. Read one only when you want to know why a rule exists.

**0.8.0** — from three runs of 0.7.0 across two repositories, where nine of ten dimensions
matched between paired runs and every divergence traced to a definition I had left open.
**`local_mitigations` means discovered, not recorded** — one run found an undocumented
`anyio` pin and raised it as a decision, another read the field strictly, emitted an empty
list and rated the same dimension `OK`; an empty list now requires saying where you looked.
**Phase 3 always stops, including on a re-check** — two of three runs folded the tier
confirmation into the Phase 6 gate, which arrives after the dimensions have already been
rated. **`adr_count` splits** into `decision_entries` and `adr_files`, after the same
repository was reported as having 65 and 0. **`do_not_repropose` carries forward
exhaustively.** **A stated premise is verified before it is acted on** — one run found the
problem in its own prompt had been fixed three hours earlier, and said so instead of
proposing a repair. **`not_proposed` is a required emission**: a run that honoured its
re-check obligations and one that quietly ignored them are otherwise indistinguishable.

**0.7.0** — dependency source review. Most dependencies are never read; a named set of
triggers says which ones are, and the version **actually installed** is read rather than the
default branch. Where a real defect is found, upstream is checked for an incoming fix before
anything is proposed, and mitigate-now versus wait-for-release is a **human decision with all
four options and their costs** — never an amendment applied on the agent's judgement. A local
mitigation is recorded as a liability with the condition for removing it, and every re-check
re-examines it: fixed upstream makes the local workaround `DRIFT`, because code defending
against a defect that no longer exists is how a codebase fills with guards nobody can explain.

**0.6.0** — the run assembles its own report. One file per run,
`RUN-REPORT-<repo>-<date>.md`, outside the repository: decisions first for the human, every
emission block appended verbatim for whoever reviews the standard. The human never harvests
blocks out of a transcript. Phase 9 finishes the same file rather than starting a second.

**0.5.0** — one file. The separate reconnaissance tool and test procedure are absorbed and
deleted: survey is Phases 0–5 stopping before the gate, and validation is a section read only
when testing the standard. A router at the top says which sections a given job needs and
which to skip, so a run carries only what it uses. Three files meant three attachments per
session and three things to keep in version-sync, which had already drifted twice.

**0.4.0** — scope and posture. The standard covers the repository, not how the work is run;
business inputs are asked and recorded, never assumed or argued with. Severity is
`recommended` or `optional`, never `required`, and **every amendment carries `if_accepted`
and `if_declined`** — a recommendation without the cost of refusing it is an order in
disguise. `BLOCKER` describes risk rather than commanding priority. The deny baseline is a
suggestion with its exposure stated, not a minimum. Dimension 6 becomes **Enforcement and
review** and gains review practice for a single maintainer, which was missing entirely.

**0.3.0** — from two live applies and their aftermath. **Enforcement placement is a tier decision** —
secret scan in CI from T1, pre-commit only where contributors justify the friction; a blocking
gate on a solo repository costs an interrupt per false positive and buys minutes.
**An enforced rule with a repeated false-trigger rate is `OVER` — including one this standard
installed**, and a rule the human must hand-edit a file to satisfy is a rule that was wrong.
**Secret-scan allowlists must not be line-number coupled**, which sat a default branch red for
three days. **Conforming placeholders are allowlisted at install time**, not discovered later
as false positives. **Never delete a file, test, or rule to make a check pass.** **Remote CI
conclusion** is required before Phase 7 completes and before any release — local green is not
remote green. **`git fetch --tags --prune` in Phase 0**; no ref claim from an unfetched clone,
after two stale reads reached a decision record as fact. **Lockfiles are generated from the
working environment, not resolved fresh** — a bare compile silently collected 998 tests
instead of 1533 at exit 0. **Collection count is part of a passing result.** **Re-check
obligations** — a decline is never re-proposed unless its trigger fired. **`N/A` for
plan-unavailable enforcement**, so branch protection stops being re-raised. **Phase 4
`corrections`** for overturning a prior run's verdicts, which had no home. **`notes` on every
phase**, which the standing rule referenced and only Phase 2 had. **Phase 6 closure rule**,
severity separated from dimension status, `severity_depends_on` split from `gates`, and
amendments emitted as objects. **`environment_preexisting`** split from `setup`. **Release UI
traps** recorded. **Ignore rule without its directory** is inert too. **Already-released
licences are locked** and never proposed for change. **Byte-identical shared files** are never
edited unilaterally.

**0.3.1** — the maintainer keeps no local clone and works across Linux and Windows, so no
proposal may assume a working copy. Tags are cut through the Releases UI or a
`workflow_dispatch` job, never locally. Client-side hooks gate nothing where every commit
comes from an ephemeral container, so secret scanning, format, lint and test are CI-always
and a hook is proposed only after a persistent local environment is established. `copier`
runs in a session or a workflow. Every Phase 6 human action must be achievable in a browser.
