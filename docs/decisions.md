# Decisions

Append-only. Supersede by adding a new entry that points at the old one; never edit history.

## 2026-09-30 — The standard moves to v0.40.0

- **Asked:**
  - After the first live re-check, the owner said to "update anything needed on your side".
    The re-check ran on v0.39.0 on 2026-09-29, from the owner's run file, against the
    repository of the first live audit. After its gate, the owner asked it to review and merge
    its pull request, and to check the branches before calling any safe to delete.
  - On 2026-09-30 the owner raised one more (F70) and named FFmpeg as a model to read (F71 to
    F79). Then: "Include the checks for more maintainers, but you need to ask if that's the
    case. Fix everything else." (F80)
- **Chosen:** twenty-one fixes, F60 to F80. `ROADMAP.md` gives each one's evidence, and the
  version history groups them by what found them:
  - **Up to the gate,** F60 to F64. The scratch clone comes from the remote where it can, and
    its `origin/<default>` is checked against the working copy's either way. A shallow clone is
    deepened before history is read. A result the run's own mistake produced goes in
    `corrections`. The address-domain command counts commits. A step the standard directs isn't
    a deviation.
  - **The apply half,** F65 and F66. Settings the run can't read are asked for at the Phase 3
    wait, as a screenshot or a reading. Phase 7's block has `overrides`.
  - **After the gate,** F67 to F69. A second reader reviews the whole branch before the report
    is handed over. Work asked for after Phase 9 has a `post_gate` block, and a merge the owner
    asks for takes only the head that was checked. A branch is advised for deletion only after
    checking what still needs it.
  - **From the owner,** F70 and F80. A working session says what it's waiting on, and from
    whom. Whether anyone else maintains, reviews or commits is asked at the Phase 3 wait,
    drafted from the history's authors, and the checks for more than one maintainer apply only
    once the human says so.
  - **From reading FFmpeg,** F71 to F79: the canonical forge, a security contact outside
    `SECURITY.md`, a checked commit grammar of either family, one merge strategy, annotated
    tags, interfaces others build on, a second release line, damaged-input tests and mixed
    licences.
- **Where the evidence left a choice, and what was chosen:**
  - **F60:** where the run can't reach the remote, as in a parity run, it clones the working
    copy and copies the working copy's remote-tracking refs across. Refusing to replay gates
    without the remote would have stopped every parity run.
  - **F65:** without a screenshot or a reading, a platform setting is `UNVERIFIABLE-HERE`. It is
    never rated done because a record says so.
  - **F67:** the second reader is a fresh session or subagent, given the branch's diff and the
    approved amendments and none of the run's reasoning. It reads in Phase 9, after the decision
    record is pushed, because one of the three defects was in the record, and Phase 7's block is
    closed before Phase 8 writes it. Where the tool can't start one, the human's review of the
    pull request is the second reading, with no third wait. The self-check no longer says it
    works "without a second reader".
  - **F66:** each phase's overrides go in the next block it emits, so Phase 9's block holds
    those of Phases 8 and 9.
  - **F69:** where a sibling can't be read, the human is asked, or the check is recorded as not
    made and no deletion is advised. A squash-merged branch qualifies when nothing cites its
    commits.
  - **F68:** the run merges only when the human asks. It passes the checked head to the merge
    as the expected head, and reads the default branch's CI on the merge commit.
  - **F80:** asked, not inferred, at the owner's word. It supersedes F24 and F56's reading of a
    second committer from the history's authors, which are now the draft. Unanswered or
    `unknown`, the default is no, nothing that depends on it is rated, and a default taken goes
    in Phase 6's first list. Phase 8 records the answer, and a re-check asks it again. The
    checks are `CODEOWNERS`, a maintainers list, review required before a merge, the
    contributing guide's review rules, a sign-off or agreement for outside contributions, and a
    security contact that isn't one inbox, each `GAP` from T2.
  - **F73:** the grammar is checked in CI over a pull request's commits, and by a commit-msg hook
    only where dimension 6 places client-side hooks, since a hook no session installs checks
    nothing.
  - **F74:** a strategy left unrecorded, or recorded while the platform allows the others, is
    `GAP`. A choice the human recorded isn't re-raised.
  - **F75:** from T2, a route that makes lightweight release tags is `GAP`. The run rates how the
    next tag gets made, not the tags already published, since immutable releases may not let
    anyone replace them. The dispatch job makes the tag object, with a tagger identity set.
  - **F76:** `N/A` where nobody builds on the interface. From 1.0.0 a removal needs a
    deprecation in an earlier release; before it, the changelog names each removal.
  - **F73 and F74:** both rated from T2. Under squash the pull request's title is the subject,
    so the grammar check reads the title.
  - **F78:** from T2. A fuzzer is the strong form, and a handful of damaged samples the floor.
  - **F71:** the mirror's own platform settings are rated `MIRROR`, and the canonical forge's
    CI is read where the run can reach it.
- **Chosen:** 0.40.0, a minor bump. The new fields are `more_maintainers` in Phase 0's `asked`,
  `forge` and `mirror_of` in Phase 2's `ci`, `readings` in Phase 3, `overrides` in Phase 7,
  `review` and `overrides` in Phase 9, the `post_gate` block, `second_reader` in the
  self-check, and `deepened` for Phase 0's `shallow`. Older reports stay readable.
- **Checked,** in this session on 2026-09-29 and 2026-09-30:
  - The corrected domain command, run with mawk 1.3.4 on the live repository's full history,
    gives each commit one count per domain. Allowing for the eight commits merged since, it
    matches the re-check's corrected per-commit counts, where the old command's didn't.
  - The ref copy moved a scratch clone's `origin/main` from the working copy's stale local
    branch to its fetched `origin/main`, in a throwaway repository.
  - On 2026-09-30, with git 2.43.0: `git describe` fails outright where only lightweight tags
    exist, and `git cat-file -t` reads `commit` for a lightweight tag and `tag` for an annotated
    one.
  - FFmpeg's facts, read from its tree and history on 2026-09-30, are in
    `research/runs/2026-09-30-ffmpeg-reference.md`.
  - GitHub's page on merge methods, read on 2026-09-30: "Rebase and merge on GitHub: Always
    updates the committer information and creates new commit SHAs." So a rebase-merge strands
    commits cited from outside, as a squash does.
- **Reviewed** cold, before the pull request opened, by a subagent that hadn't written the
  change. It found four blocking defects, all fixed: the second reader read before the decision
  record existed, Phase 7's `overrides` claimed later phases, the scratch clone didn't check out
  the audited commit, and the branch check had no fallback where a sibling can't be read.
- **Reviewed again,** cold, after F70 to F80, by another subagent. It found four blocking defects,
  all fixed: F80's question wasn't recorded, shown again on a re-check or used by every rule it
  gates; the checks for more maintainers had no tier; annotated tags clashed with the tag routes
  the gate recommends; and three claims about FFmpeg went beyond what was read. Its smaller
  points were fixed too. Among them: rebase-merge strands cited commits as squash does, the
  forge is found before CI is read, and dimension 4 raises the waiting-on line. The sentence on
  a licence-changing build option went, as beyond the approved text.
- **Parity:** held until the owner has seen the decisions and options, at the owner's word. The
  runs draw on the same weekly allowance as the owner's working sessions, and the pull request
  merges after them. F80's question is asked at the Phase 3 wait, so every sample reaches it,
  the greenfield one included.

## 2026-09-29 — The standard moves to v0.39.0

- **Asked:** before the fork's first audit, the owner approved fixing the standard: "I approve
  you to do what you need to." Then they asked for their public repositories and branches to
  be read, and for this repository to fix itself against what they show.
- **Chosen:** forty-one fixes: F18 to F50 without F21, which v0.38.0 applied; F51 and F52
  from reading the repositories; and F53 to F59 from this version's own parity runs.
  `ROADMAP.md` gives each one's evidence, and the version history groups them by what found
  them:
  - **The first live audit,** F39 to F50. The default branch is read as `origin/<default>`
    after the fetch. A secret-scan job is read by its range and its count. A status command's
    exit goes in `notes`. What the gates leave behind is listed. An approved change can be
    held. Before each push, the base is fetched and the full gate runs. The fresh clone
    comes from the remote. Each human action records what was seen. Re-checks run on the
    merged tree. An optional tool is probed by its capability. A report committed to a public
    repository gets a privacy pass.
  - **Preparing it, and its dry run,** F26 to F35. Phase 3 drafts answers with their
    evidence. What CI installs counts as declared. A long suite runs in the background. The
    history's address domains are compared with the owner answer. A Phase 3 stop has a report
    shape. A documented one-command gate runs for what it covers. The hook probe reads
    `core.hooksPath`. The release-asset fact is checked again. A boundary finding names its
    side. Seven smaller schema points are settled.
  - **R22,** F36 to F38: synced plugins, synced skills, and "Is that still the case?"
  - **The v0.38.0 parity runs,** F18 to F20 and F22 to F25: the routing row for choosing
    first, a scheduled job's settings and task definition, a refused command, a default record
    path, `CODEOWNERS`, and actions pinned by tag.
  - **Reading the owner's two public repositories and their sessions,** F51 and F52. The fork's
    default branch mirrors upstream, untouched since 2026-08-21, and its working branch is 1,090
    commits ahead with the only context file, so the run reads `working_branch` wherever the
    standard says the default branch. Two sessions started in July still ran Claude Code
    2.1.233, so the run records its agent's version. Private repositories weren't read.
  - **This version's parity runs,** F53 to F59:
    - The choosing row names the shapes section and Phase 6.
    - `job` takes `choose`.
    - The tier grep has a target without a record.
    - `CODEOWNERS` is rated where the plan honours it.
    - Native `AGENTS.md` reading reaches third-party providers from v2.1.281.
    - A `Read` deny covers `cat`.
    - An unattended run meets the Phase 3 wait with the answers it was given.
- **Where the evidence left a choice, and what was chosen:**
  - **F25:** an action pinned by tag is a `GAP` where its workflow reads a secret, grants its
    token write access or publishes, or from T2. Elsewhere the pin is `optional`. The final
    v0.38.0 re-check had rated one `GAP` at T1, with no secret, and offered the pin as
    optional.
  - **F24 and F56:** `CODEOWNERS` is due from a second committer, read from the history's
    authors, where the plan honours the file. Where the plan can't be read, it stays `GAP`, with
    its amendment gated on the human's answer, as the re-check run did.
  - **F26:** the confidence words are `high`, `medium` and `low`. Production, dependents and
    where it runs are never drafted, as R22's first pass has it. The deeper pass would also
    ask work-or-personal and lifetime outright; piece 1 decides that with the front door.
  - **F29:** the question goes to the gate's first list, naming domains and counts, never an
    address, and the default is the owner answer as given.
  - **F31:** the documented one-command gate runs for the gates it covers, and CI's other jobs
    run as the workflow runs them.
  - **F20:** a registration script is preferred, with an encoding rule as the fallback.
  - **F42:** leftovers are removed by comparing with Phase 0's list, never with
    `git clean -X`, which also deletes files such as a `.env`.
  - **F59:** an unattended run's Phase 3 is met by the answers given in advance, and the tier
    goes first at the Phase 6 gate. The other choice was to keep the stop and let every
    unattended run record a deviation, which two runs did.
- **Chosen:** 0.39.0, a minor bump. The new fields are `ignored_at_start`, `drafts`,
  `fix_side`, `held`, `base`, `mergeable`, `base_commits` and `human_action_states`. There are
  new values for `answers_source`, `deployment.source` and the self-check's structure lines.
  Older reports stay readable.
- **Checked,** in this session on 2026-09-29:
  - **Cloud environments page:** it still says an unattached repository's release assets get
    a 403.
    - Downloads from `cli/cli` and `gitleaks/gitleaks` returned 200, through
      `release-assets.githubusercontent.com`.
    - Their API returned 403 (F33).
  - **Plugin and skill docs:**
    - The plugin-loading page names Cowork and signed-in terminal sessions for synced
      plugins. The skills page names cloud sessions for synced skills.
    - The settings reference gives `syncClaudeAiSkills` and `syncClaudeAiPlugins` the scopes
      "User, local, or managed", and `skillOverrides` "Any file". It adds "Overrides don't
      apply to plugin skills".
    - The changelog's 2.1.282 and 2.1.283 entries change `Skill(anthropic-skills:…)` allow
      and deny rules (F36, F37).
  - **gitleaks-action and gitleaks:**
    - gitleaks-action at v3.0.0 (`e0c47f4`) builds
      `--log-opts=--no-merges --first-parent <base>^..<head>` for push and pull-request
      events.
    - gitleaks 8.24.3 and 8.30.1 run `git log -p -U0 --full-history --all` by default (F40).
  - **gh and Debian:**
    - gh's `pkg/cmd/attestation` exists at v2.47.0 and not at v2.46.0. Its `--signer-workflow`
      flag is defined at v2.51.0 and not at v2.50.0. The first live run's installer check
      passes that flag, so F49's example probes for it.
    - sources.debian.org lists gh 2.46.0 for trixie and sid, and 2.23.0 for bookworm (F49).
  - **git 2.43.0:**
    - `git rev-parse --git-path hooks` follows `core.hooksPath` and resolves in a worktree,
      where `.git/hooks` isn't a directory (F32).
    - A UTF-16 file diffs as binary. With `working-tree-encoding=UTF-16LE-BOM`, it's stored as
      UTF-8 and diffs as text (F20).
    - `TZ=UTC` with `--date=iso-strict-local` prints the committer date in UTC (F35).
  - **Microsoft's `Out-File` reference, for Windows PowerShell 5.1:** the default encoding is
    `unicode`, "UTF-16 with the little-endian byte order" (F20).
  - **GitHub's code owners page:** "You can define code owners in public repositories with
    GitHub Free and GitHub Free for organizations, and in public and private repositories with
    GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server" (F56).
  - **Claude Code's docs:**
    - The memory page: "Before v2.1.281, some sessions, such as those on Amazon Bedrock or with
      telemetry disabled, read CLAUDE.md files only." The changelog has `AGENTS.md` support
      "also work on Amazon Bedrock, Google Vertex AI, Microsoft Foundry, LLM gateways, and
      sessions with telemetry disabled" (F57).
    - The permissions page: `Read` and `Edit` deny rules "apply to Claude's built-in file tools,
      to file commands Claude Code recognizes in Bash, such as cat, head, tail, sed, and tee",
      but not to "a command that reads files without naming them" (F58).
- **Parity:** one run of each sample, on `48c6ecd`, graded and compared with the baseline. Each
  passed every check and left its sample unchanged.
  - **Greenfield:** seven checks, and no difference from the baseline. It found F53 to F55. Its
    fourth override, reading `core.hooksPath` with `--local`, came from the prompt's limit on
    the directories a run may read.
  - **Re-check:** thirteen checks. Two values moved:
    - dimension 3 to `GAP`, which F24 was meant to do;
    - dimension 8 to `UNVERIFIABLE-HERE`, because the run tried the existing licence check on
      the dev tools and had no network.

    It kept the declines and the item never to be proposed again. It rated tag-pinned actions
    no finding at T1, as F25 says, and found F56.
  - **Audit:** twenty checks, with all thirteen planted problems found. One value moved:
    dimension 4 to `BLOCKER`. That's the v0.37.0 rule, which every v0.38.0 audit run also
    moved. It found F57 to F59.
  - **Not re-run** after the fixes the runs found, because the owner's account is near its
    weekly limit. The fixes are text a run reads, and skillcheck, the tests and a reading
    checked them.
- **Also changed, at the owner's word to fix everything open:**
  - `CLAUDE.md` here no longer says this repository's settings can't turn the synced skills
    off. It now says they can't stop the sync, and that hiding one is documented but untried.
    The owner's browser test 3 settles which.
  - `docs/testing-the-skill.md` names a second known limit of the parity prompt: it says
    nothing about the network. The audit run read PyPI, public repositories and vendor docs,
    while the other two made no network reads.
- **Not done:** the prompt itself is unchanged, because settling either limit means a new
  baseline.

## 2026-09-28 — R22's deeper pass is taken in

- **Taken in:** a second R22 result, a deeper pass from the same day, filed as
  `research/runs/2026-09-27-R22-deeper-pass.md` with its verification table. The filed copy
  leaves out the first live repository's name and three model names from two study rows.
- **Corrects the entry below:** its "Not established" bullet says some study figures aren't in
  the abstracts cited, and that the current abstract contradicts row 65. Following the deeper
  pass's sources to earlier versions and full texts, all of them check out: rows 56 and 66 in
  the full papers, row 64 in its v1 abstract and row 65 in its v2 abstract. Later versions
  changed or dropped those figures. The first pass's table now says so.
- **Found, and checked:**
  - The French page the deeper pass cites for synced plugins in cloud sessions now says what
    the English one does, so F36 stays settled. This session also runs with
    `SKIP_PLUGIN_MARKETPLACE=true`.
  - Plugins have a sync key of their own, `syncClaudeAiPlugins` (F37).
  - The Help Center gives an uploaded skill's description 200 characters at most, and the
    Agent Skills specification 1,024. This skill's description is 446 characters, so an
    upload may be refused.
  - A committed project skill can carry `disable-model-invocation` and hooks, and a
    PreToolUse hook blocks a call by exiting with code 2.
  - At least 5.2% of the packages that commercial code models suggest don't exist, and 21.7%
    for open-source models (USENIX Security 2025).
  - `AskUserQuestion` takes at most four questions a call. How it shows in the mobile app isn't
    documented.
- **Not established:** the Android bug report the deeper pass cites, since github.com refused
  this session.
- **Chosen:** as with the first pass, nothing in the skill or the catalog changes. The deeper
  pass's alternatives go into the front-door plan in `ROADMAP.md`, for piece 1 to weigh:
  - a thin uploaded skill that fetches the reference at a pinned commit;
  - five questions asked outright instead of three;
  - a warning rather than a stop when `main` is newer;
  - a committed project skill whose hook enforces the approval gate.
- **Open, for the owner:** the entry below's three choices stand, with one change to the
  first. An upload of the skill as it stands may be refused over its 446-character
  description. If it is, a shorter description is a change to the skill, with the authoring
  review.

## 2026-09-28 — R22's result is taken in: the route is an uploaded skill

- **Taken in:** R22's result, filed as `research/runs/2026-09-27-R22-one-command-front-door.md`
  with its verification table, under `research/README.md`. The filed copy leaves out three
  phrases: the model its first line names, a company name, and the first live repository's
  name.
- **Found, and checked:**
  - Skills on the owner's claude.ai account load in cloud sessions and routines. Synced plugins
    are documented only for Cowork and signed-in terminal sessions, which settles F36.
  - An uploaded skill may carry only the six Agent Skills fields, so `disable-model-invocation`
    can't keep it from loading unasked. A narrower description is the lever the upload allows.
  - In a cloud session a synced skill's `` !`command` `` lines run, so the skill can hash its
    own reference file there.
  - Claude Code updates an installed plugin only when the version its catalog entry pins
    changes, and it has said 0.1.1 since 2026-09-23, so a copy installed before v0.37.0 still
    has v0.36.0. The chat copy the owner found is, by the report's hash and timestamp, the
    0.1.1 release's commit, `cbe163f`, with v0.36.0.
- **Not established:** the report's reason for the chat copy, the unchanged version. claude.ai's
  docs say a marketplace the owner added updates through Check for updates, or Sync
  automatically, and don't say how claude.ai decides that a plugin changed. Some study figures
  aren't in the abstracts cited (its rows 56 and 64), and the current abstract contradicts
  row 65's 48% with 45%. None of them changes a file here.
- **Chosen:** nothing in the skill or the catalog changes in this intake. The report's four
  proposed files wait for piece 1, which moves the procedure into `SKILL.md`, and pass the
  authoring review and parity runs there:
  - its `SKILL.md` changes how Phase 3 asks, narrows when the skill loads, and asks whether to
    go on when `main` is newer, a stop outside the standard's two waits;
  - `scripts/verify_reference.py` has no tests, and ruff and coverage don't reach `skills/`;
  - `assets/decisions-answers-block.md` adds a second answers schema beside the run
    report's Phase 3 block, and changes what Phase 8 writes in other repositories;
  - the `marketplace.json` version change is a release, which the v0.37.0 entry left to the
    owner.

  *Considered:* applying them now, as the report advises. In a scratch clone they passed
  `skillcheck`, the tests and the catalog validator, but none of those checks runs the script
  or the new questions.
- **Chosen:** `ROADMAP.md` gets F38, from the report's checked survey sources: a re-check's
  stated default, "nothing has changed", invites confirming a stale answer.
- **Open, for the owner:**
  - whether to upload the skill to the claude.ai account as it stands, which its frontmatter
    allows, and turn the plugin off there, so chat doesn't carry two copies;
  - whether installs follow releases, with a release at each standard change, or follow
    `main`, with no pinned version;
  - the report's three browser tests, with Check for updates tried before any version change,
    so the first test can tell the two explanations apart.
- **Deferred:** the front door, still in piece 1. *Trigger:* the first live audit's report is
  triaged. R22's half of the earlier entry's trigger is met.

## 2026-09-28 — One command from any repository: researched before it's built

- **Asked:** the owner wants one short command, typed in any repository's session, that starts
  the standard. In an existing repository it reads the repository first and asks only what it
  can't show. In a new one it interviews the owner and recommends a language, runtime and
  shape. Every run stops for approval before it writes anything.
- **Chosen:** research first. R22 (`research/prompts/R22-one-command-front-door.md`) tests the
  building session's plan against the evidence: the route into sessions, knowing which copy
  ran, drafted answers confirmed in one reply, the new-project interview, and keeping the
  answers for the next run. The result is taken in by `research/README.md`, and only checked
  claims reach the skill. The plan is in `ROADMAP.md`.
- **Chosen:** the filed prompt names neither of the owner's two paired repositories, since the
  v0.38.0 entry keeps the first live repository's name out of this repository. It doesn't
  describe the systems that earlier runs audited, either. The owner's draft named both, and the
  research needs neither.
- **Checked:** the draft's statements about this repository and the standard, on 2026-09-27
  and 2026-09-28, before filing. The filed prompt corrects them:
  - F15 was fixed in v0.38.0, and F18 is the one still open.
  - Phase 8 writes to whatever decision record Phase 1 found.
  - The standard already has three things the draft didn't mention:
    - a re-check that shows the recorded answers;
    - a limit on the questions a new project is asked;
    - a Scope line that rules out product direction.
  - The testing plan is piece 0, already built.
  - Each belief marked as the standard's now says what its dated fact says.
- **Found:** by the owner's report, a claude.ai chat on 2026-09-27 loaded the plugin's skill as
  `standards:project-bootstrap-and-audit` with standard v0.36.0, while `main` held v0.38.0.
  The catalog has said 0.1.1 since 2026-09-23, as the v0.37.0 entry chose, and GitHub holds no
  `v0.1.1` tag.
- **Found:** read on 2026-09-28, Claude Code's plugin docs say synced plugins load in Cowork
  sessions and in terminal sessions signed in with a claude.ai account, and name no cloud
  session. The 2026-09-23 entry read them as naming cloud sessions. The settings docs also let
  a committed settings file hide or deny a skill, which may reach a synced one. These are
  `ROADMAP.md` items F36 and F37, for R22 to settle.
- **Found:** the 2026-09-23 entry says the standard's versions up to v0.36.0 stay CC0-1.0.
  v0.37.0 and v0.38.0 carry the CC0 dedication too. The rebuilt skill becomes Apache-2.0 at
  piece 6, as that entry chose.
- **Deferred:** the front door, in piece 1. *Trigger:* R22's result is filed and checked, and
  the first live audit's report is triaged.
- **Open:** whether colleagues will run it on work repositories. If they do, their company's
  rules live in their own repositories or a private organization skill, never here.

## 2026-09-24 — The standard moves to v0.38.0

- **Asked:** the owner asked whether anything in the file should change before it audits their
  repositories, and to make the change if so. Then they asked for everything to be checked
  again before the first live run, and for anything new or valuable to be rolled in.
- **Chosen:** fifteen fixes and one addition, applied together.
  - **From the v0.37.0 parity runs:**
    - **F10:** on a Windows host, the PowerShell recommended follows criterion 1. That's
      Windows PowerShell 5.1 where nobody will install and patch PowerShell 7 on the host,
      and 7, with that upkeep named as its cost, where someone will.
    - **F11:** a PowerShell scheduled job has a layout: a module that holds the logic, one
      entry script that the task runs with `-NoProfile -NonInteractive -File`, and the task's
      definition in `packaging/`.
  - **From reading the first live repository before its run.** Its name stays out of this
    repository.
    - **F12:** Phase 1 finds a decision record by content, as its constraint always said. It
      counts numbered decisions and dated entries in headings, and its tier grep asks for the
      tier's codes. That repository keeps its numbered decisions inside a planning document,
      and the words "blast radius" in its prose were enough for the old grep to count a tier.
      Tried on that repository, both samples and this one, the new commands find each record,
      and the tier grep matches no prose.
    - **F13:** a repository's precedence over this file covers findings, not the run. That
      repository's context file tells agents to act without asking, commit as they go,
      release on their own and write a session log before ending. None of that lifts the
      waits.
    - Context files are measured in bytes as well as lines, since that one held 141 KB in 549
      lines.
    - Evidence files are read in parts, and listed with their sizes.
  - **From this version's own parity runs:**
    - **F14:** Phase 0 says a fetch writes only remote-tracking refs, and what to do when one
      can't run.
    - **F15:** the routing table's set-up row covers a repository that holds no source yet.
    - **F16:** an install that is itself a gate counts in `command_tally`. The setup
      carve-out had let a failing lockfile install, CI's first step, sit beside a tally of
      all `PASS`.
    - **F17:** the Phase 6 block gains `standard_amendments`, because a run had nowhere to
      put its `class: standard` amendment.
    - **F21:** dimension 6 states that every workflow sets `permissions:`. The rule lived only in
      the starter template, which an audit doesn't read, and one final audit missed the planted
      workflow without it.
  - **Found while reviewing:**
    - The starter CI pins `actions/checkout` to its v7.0.1 commit, with the version in a
      comment, and says what that costs.
    - Its load-bearing list says six, which is how many it lists. It said four.
    - The frontmatter's `standards_repo` placeholder says the question is asked at the
      Phase 3 wait.
    - An upload that renames the file isn't a version mismatch.
  - **The addition:** a run can read the file from a link pinned to a commit, downloaded whole
    and checked against its SHA-256.
    - *Sending Results Back* gives the prompt.
    - *Standards Distribution* names the option.
    - The self-check records `standard_sha256`.
- **Chosen:** 0.38.0, a minor bump. F10 changes a recommendation, and `standard_sha256`,
  `bytes`, `total_bytes_loaded_at_session_start` and `standard_amendments` are new fields, so
  older reports stay readable.
- **Checked:** each new fact against its primary source, on 2026-09-24.
  - **Claude Code's cloud environments page:**
    - "A cloud session doesn't install the plugins a repository turns on under
      `enabledPlugins`".
    - "GitHub API and release-asset requests reach only repositories attached to the session".
    - `raw.githubusercontent.com` "is in the default Trusted list".
  - **Claude Code's tools reference,** on WebFetch: "For most fetches, Claude receives that
    model's answer, not the raw page."
  - **GitHub's secure-use reference:**
    - "Pinning an action to a full-length commit SHA is currently the only way to use an
      action as an immutable release".
    - "Dependabot only creates alerts for vulnerable actions that use semantic versioning and
      will not create alerts for actions pinned to SHA values."
  - **`git ls-remote https://github.com/actions/checkout`:** `v7` and `v7.0.1` both resolve to
    `3d3c42e5aac5ba805825da76410c181273ba90b1`.
  - **Microsoft's PowerShell support lifecycle** (updated 2026-08-13): "Windows PowerShell is a
    component of the Windows operating system and is subject to the Windows support lifecycle."
  - **Microsoft's migration guide** (2024-04-02): "PowerShell 7 is designed to coexist with
    Windows PowerShell 5.1".
  - **`about_Pwsh` and `about_PowerShell_exe`:** both list `-NoProfile`, `-NonInteractive` and
    `-File`.
  - **In a cloud session:**
    - Both skill files, downloaded from `raw.githubusercontent.com` at a pinned commit,
      matched git's copies byte for byte.
    - A file the owner attached arrived byte for byte, renamed with a prefix and underscores.
- **Parity:** runs on the samples, graded and compared with the baseline. Runs on commits a
  later fix superseded were stopped.
  - **Greenfield:** two runs, on `224fc39` and `545f7b6`. Each passed every check with no value
    moved, and the text it reads is unchanged at `488d89b`.
  - **Audit:** five runs. Each found all thirteen planted problems but one. A full-file run on
    `545f7b6` missed the workflow without a `permissions:` block, whose rule lived only in the
    starter template; that became F21. The final run, on the trimmed file at `488d89b`, found
    it in dimension 6, with its own amendment.
  - **Every audit run moved one value:** dimension 4, from `DRIFT` to `BLOCKER`. That's the
    v0.37.0 rule for a tracked `settings.local.json`, as that version's entry expected.
  - **Re-check:** two runs, on `2322967` and `488d89b`. Both passed every check and kept the
    declines and the do-not-re-propose item.
    - Both moved dimension 3 off `OK`: they applied its `CODEOWNERS` rule, which the sample's
      second committer triggers and the baseline run didn't. They split between `GAP` and
      `UNVERIFIABLE-HERE` (F24).
    - The final run moved dimension 8 to `GAP` for actions pinned by tag, following the new
      fact on SHA pins, which dimension 8 doesn't yet rule on (F25).
    - The first run found F16 and F17. The final one counted the failing lock install as
      `FAIL`.
  - **The trimmed file:** three runs, at `2322967`, `545f7b6` and `488d89b`, each given the file
    the way the owner will give it. Each matched the full file's results, and recorded the
    trimmed file's own SHA-256.
  - **Cut off:** the full-file audit on `488d89b` was cut off by a usage limit and not rerun.
    The trimmed-file run applies the same audit rules.
  - **No run changed its sample.**
- **Delivered:** an audit extract for the owner's first live run. It is this version without
  the two sections no run reads, *Validating a Change to This Standard* and *Provenance*, and
  a note at its top names the commit it came from. It isn't committed; the full file here is
  the standard. Its SHA-256 is
  `5980efd64233763d47b8531ca9f08c61ff82b34277df024f33c87bdfafaf1948`, from commit `488d89b`.
- **Not included:**
  - The rule on fewest dependencies at their newest versions: it waits for R21.
  - F18-F20 and F22-F25, which the final runs raised. None changes an audit of a repository
    that has a decision record and pins its actions, and each is one run's evidence, so they
    wait for the next revision. The roadmap lists them.
  - Splitting the file: that's the rebuild's pieces.
  - The report format: it's decided at piece 1.

## 2026-09-24 — This repository's guard and grader get their fixes

- **Done:** the two deferrals in the v0.37.0 entry below, whose trigger fired when that change
  merged.
  - CI's collection guard now matches the standard's template, with this repository's
    collection command. Run under `bash -e` with nothing collected, the old guard exited 1 and
    printed nothing, and the new one names the failure. It was checked in three states: as
    committed, with a baseline above the count, and with nothing collected.
  - The grader's `not_proposed` check reads each amendment's `change:` only. The v0.37.0
    re-check report's two false alarms clear, and a change that names a declined item still
    fails the check.
- **Changed:** `.test-baseline` goes to 144, for the four new grader tests.

## 2026-09-24 — Fewest dependencies, newest versions: researched before it's a rule

- **Asked:** the owner wants every repository the standard sets up or audits to run on as few
  dependencies as possible, each at its newest version. There's less to keep current, and
  less for CI and dependency tools to check, so runs are shorter and the attack surface is
  smaller.
- **Chosen:** research first, at the owner's direction. R21
  (`research/prompts/R21-fewest-dependencies-newest-versions.md`) tests the aim against the
  evidence and asks where it needs a limit: a release taken the day it's published, and
  hand-written code replacing a mature package. The result is taken in by `research/README.md`,
  and only checked claims reach the standard, as a change of its own.
- **Found:** what v0.37.0 already covers, read on 2026-09-24. Dimension 8 asks for grouped
  weekly updates with security updates apart, and rates a cooldown against the three-day
  default. Dimension 2 has the lockfile installs that fail on drift. *Choosing a Language and
  Runtime* says every extra language multiplies the configuration, and `OVER` rates
  configuration heavier than the tier needs. There's no rule on how many dependencies a
  repository carries, on unused or duplicate ones, on backports its runtime floor makes
  redundant, on how far behind a runtime or a dependency may fall, or on how many runtime
  versions CI tests. Two defaults bear on it. The language table recommends Vitest for new
  JavaScript and TypeScript tests, where Node.js has a built-in runner, and it holds Pester at
  5.7.x because Pester 6 breaks things. R21 asks which runner a new project needs, and when
  staying a major version behind is right.
- **Deferred:** the rule. *Trigger:* R21's result is filed and checked.
- **Deferred:** holding this repository to it: its dependencies and pins in `pyproject.toml`,
  `package.json` and CI. *Trigger:* the rule is in the standard.

## 2026-09-23 — The standard moves to v0.37.0

- **Chosen:** twenty-two fixes to the standard, applied together at the owner's request, so
  the one file can audit the owner's public repositories now and bring results back:
  - the nine findings from the parity baseline, F1-F9 in `ROADMAP.md`;
  - the set-up run's open amendments S2-S7 and S9-S11;
  - four that this version's own parity runs found, below.

  Each had been proposed and was waiting for approval. They land in the standard file rather
  than piece by piece, and the rebuild's pieces move the fixed text.
- **Chosen:** 0.37.0, a minor bump. The new rules and fields are additive (`owner: mixed`,
  `recommended` and `pending` in the Phase 3 block, `shape_recommended`, `category_checks`), so
  older reports stay readable.
- **Not included:** S8, a Keep current mode for the standard. The roadmap's `keeping-current`
  skill covers it.
- **Checked:** the facts behind two new rules, against their primary sources on 2026-09-23.
  GitHub's workflow syntax says a `run` step with no `shell:` runs `bash -e {0}`, and naming
  `shell: bash` adds `-o pipefail`. Git's documentation says `GIT_OPTIONAL_LOCKS` set to false
  "will prevent git status from refreshing the index". Under `bash -e` with nothing collected,
  the old guard exited 1 and printed nothing; the new one names the failure.
- **Not checked here:** the current `actions/checkout` release. This session can't reach that
  repository, so v7.0.1 is the set-up run's reading, and the release this repository's
  Dependabot pins.
- **Parity:** one run of each sample on `8c18f51`, compared with the v0.36.0 baseline.
  - The audit and greenfield samples passed every check, and no value moved.
  - The re-check sample failed two checks, and its dimension 8 moved from `OK` to
    `UNVERIFIABLE-HERE`. Reading the report settles all three. The run proposed neither
    Dependabot nor branch protection, and lists both under `not_proposed` with the right
    reasons; the grader matched the words in two amendments' reasoning. Dimension 8 rests on
    the new dated fact that `actions/checkout` is at v7, which an offline run can't confirm,
    so marking it is the rule working.
  - No run changed `.git/index`, where every v0.36.0 run did.
- **Chosen:** four more fixes the runs found, applied before this merged. A lockfile header
  doesn't survive in `uv.lock`: two runs found it gone after `uv lock`, so the command goes in
  the context file's commands. The CI conclusion takes `unknown`. Greenfield proposals get a
  field in Phase 2. A run that stops at Phase 3 keeps its overrides in `notes`.
- **Chosen:** the rule for a tracked `settings.local.json` moves into dimension 4. The audit
  run never read *The Configuration File Map*, where it first went, because the routing table
  doesn't send an audit there, and rated the sample's `pip install` grant `DRIFT`. A second
  audit run, on `ecababf`, rated it `BLOCKER`, as the rule intends. Every planted problem was
  still found, and dimension 4 was the only value that moved from the baseline.
- **Deferred:** a release, at the owner's choice. The catalog stays at 0.1.1, so until the next
  release `main` carries standard v0.37.0 while the 0.1.1 release carries v0.36.0, under one
  version number, as the v0.36.0 entry recorded for 0.1.0. The `v0.1.1` tag goes on
  `cbe163f`, the release's merge commit, not on `main`. *Trigger:* the next release.
- **Deferred:** this repository's own CI guard copies the template's, and gets the same fix in
  a change of its own. So does the grader's `not_proposed` check, which should read what an
  amendment proposes rather than every word in it. *Trigger:* this change merges.

## 2026-09-23 — Release 0.1.1: the marketplace takes the repository's name

- **Chosen:** the marketplace is renamed from `rmccann-skills` to `claude-code-skills`, so that
  it matches the repository. The owner asked for the names to match. claude.ai shows a
  marketplace added from a repository by the repository's name, while Claude Code shows the
  catalog's `name`, so the two differed. This supersedes the marketplace name in the inception
  entry's H3. The plugin stays `standards`.
  - *Considered:* renaming the repository instead. That touches 36 files, among them the
    owner-file lines in `AGENTS.md` and dated research records.
  - *Risk:* Claude Code blocks marketplace names that impersonate official ones, and re-checks
    at every load. `claude-code-skills` isn't on the reserved list, and Claude Code 2.1.280's
    strict validator passes it (checked 2026-09-23). *Reopen when:* Claude Code rejects the
    name.
- **Chosen:** the rename ships as release 0.1.1, with standard v0.36.0. A version that reaches
  `main` is published, so a breaking change can't reach it under 0.1.0. And 0.1.0 already named
  two standards: v0.35.0 at its tag, and v0.36.0 on `main`. This settles the release that the
  v0.36.0 entry deferred. The owner chose 0.1.1 over 0.2.0: under 0.x anything may change
  (A13), and 0.2.0 stays the rebuild's release.
- **Chosen:** the catalog's plugin entry names its author and repository, as a plugin's own
  manifest does. Claude Code's strict validator asks a manifest for an author.

## 2026-09-23 — The plugin reaches the account, not cloud sessions

- **Found:** the plugin can be enabled for the owner's claude.ai account. The owner added this
  repository as a marketplace of their own, under Customize > Plugins > Personal plugins > Add
  marketplace > Add from a repository, and installed `standards` 0.1.0 with no error. claude.ai
  took the catalog as it stands, with the plugin defined in `marketplace.json`
  (`strict: false`) and no `plugin.json`. It names the marketplace after the repository,
  `claude-code-skills`, rather than the catalog's `rmccann-skills`.
- **Found:** cloud sessions don't load it.
  - A fresh session started a few minutes after the install, on Claude Code 2.1.281. Its
    folder for synced plugins was empty, and it had no `standards` skill.
  - About ten minutes after the install, a lookup of the account's enabled plugins still found
    none.
  - The working session that made the lookup had pulled in the account's skills when it
    started, but none of the Anthropic plugins listed on the account since the day before.

  Claude Code's plugins reference says cloud sessions download the plugins enabled for the
  account when they start (checked 2026-09-23). So either the product doesn't yet match its
  docs, or a condition applies that they don't state.
- **Found:** the organization route is closed to this repository. The Help Center says a
  GitHub-synced organization marketplace "must be private or internal" (checked 2026-09-23),
  and this repository is public. An organization could still take the plugin as an uploaded ZIP
  file, one upload per release.
- **Chosen:** H2 stands, and with it the six-field frontmatter rule: uploading the skill to
  claude.ai stays the route into cloud sessions. That answers the *To verify* item in the entry
  below. Nothing is lost yet, because the plugin carries only a skill. Hooks and subagents are
  what would need the plugin route.
  *Reopen when:* a cloud session's `~/.claude/plugins/synced/` holds the account's plugins, or
  a piece of the rebuild adds hooks or subagents.
- **Chosen:** sessions on this repository don't load an installed copy of the plugin, so a
  session rebuilding the skill, or a parity run, can't pick up an older one. `.claude/settings.json`
  turns off `standards@synced` and `standards@claude-code-skills`, which Claude Code's docs let a
  project do in its committed settings (checked 2026-09-23). A copy uploaded as a claude.ai
  skill can't be turned off from here, so `CLAUDE.md` says the file here wins, and a parity run
  needs it turned off on the account.

## 2026-09-23 — The standard is rebuilt into the skill

- **Chosen:** the standard stops being a separate document. Its content becomes the parts of the
  `project-bootstrap-and-audit` skill:
  - a procedure;
  - references by topic;
  - tested templates;
  - scripts;
  - a report schema.

  Its self-management goes: its own version, version history, test procedure and change
  process. This repository's history, changelog, decision record and tests already do that job.
  The owner approved a section-by-section map of where everything goes. Its pieces are in
  `ROADMAP.md`.
- **Chosen:** it lands in seven pieces, with the parity checks first. Each piece moves its
  sections out of the standard file in the same commit, and is checked against the version
  before it (`docs/testing-the-skill.md`). The file is deleted in the last piece, which is
  release 0.2.0.
- **Chosen:** built for Claude Code first, and kept usable with other AIs such as Gemini and
  ChatGPT without going out of the way (the owner's direction):
  - frontmatter stays at the six Agent Skills fields;
  - scripts use only Python's standard library;
  - each Claude Code-only feature is marked with what it does, so another tool can look for its
    own equivalent.
- **Chosen:** the owner works in cloud sessions, and those load only what's enabled on the
  owner's claude.ai account or committed to the repository being worked on (Claude Code's docs,
  checked 2026-09-23). So the claude.ai account stays the route into them, and H2 (below) stands.
  *To verify:* whether this repository's plugin can be enabled for that account. If it can, its
  hooks and subagents would reach cloud sessions.
- **Chosen:** the rebuilt skill is Apache-2.0, like the rest of the repository, from piece 6.
  The standard's versions up to v0.36.0 stay CC0-1.0 in git. From then on, this supersedes the
  inception entry's line that the standard keeps its own CC0-1.0 dedication.
- **Chosen:** parity runs happen in the working session, as fresh subagents.
  - *Deferred:* `claude plugin eval` in CI. *Trigger:* an Anthropic API key is stored as a
    repository secret.
  - *Open:* the report's format, Markdown with YAML blocks and a checker, or JSON. It's decided
    at piece 1.
- **Supersedes, from piece 6:** the inception entry's gate default that the standard ships as a
  skill (H6).

## 2026-09-23 — The standard moves to v0.36.0

- **Chosen:** nine of the standard's dated facts were corrected, each checked against its
  primary source (research R01, R02, R05 and R08). The maintainer approved the fixes, and they
  were applied on their own.
- **Chosen:** 0.36.0 rather than 0.35.1. One fix retires a rule: the `CLAUDE.md` shim no longer
  becomes `OVER` once Claude Code reads `AGENTS.md` natively, because native reading has
  conditions. The standard's versioning makes that a minor bump, since a patch changes no
  output.
- **Not included:** the other amendments to the standard from the set-up run (S2-S11). They
  stay open for the maintainer.
- **Deferred:** a release for it, at the maintainer's choice. The catalog stays at 0.1.0, so
  copies already installed at 0.1.0 keep v0.35.0: Claude Code updates an installed plugin only
  when its version changes. Until the next release, `main` and the `v0.1.0` tag carry different
  standards under the same version number. *Trigger:* the next release.

## 2026-09-23 — Hidden-character checks beyond skills

- **Chosen:** `skillcheck` checks `AGENTS.md`, `CLAUDE.md`, `.claude/` and `research/` for hidden
  and bidirectional characters, as it already did for skills (A30). Agents read these files as
  instructions or context, and research results are pasted in from outside the repository.
  R01 recommends this check for agent-instruction files. The owner approved it on taking in
  R01-R05 and R08.

## 2026-09-23 — Before the first merge: the 0.1.0 release, and a cost of SHA pins

- **Chosen:** the first merge to `main` is the 0.1.0 release (A29), because a version that
  reaches `main` is published, tag or no tag. The changelog's entries moved under `[0.1.0]`,
  and the README's Operations section says how to withdraw a bad skill. This settles the
  runbook that the inception entry below deferred until the first release.
- **Chosen:** keep A16's SHA pins, knowing a cost the gate didn't state. GitHub's secure-use
  reference (checked 2026-09-23) says "Dependabot only creates alerts for vulnerable actions
  that use semantic versioning and will not create alerts for actions pinned to SHA values."
  Weekly version updates still cover the pins, and their tag comments on the same line.
  *Reopen when:* GitHub raises alerts for SHA-pinned actions, or a vulnerability in a pinned
  action is found before an update for it reaches this repository.

## 2026-09-23 — Inception: set up against the standard

- **Standard:** PROJECT-BOOTSTRAP-AND-AUDIT v0.35.0. Job: set up; mode: greenfield. The run
  stopped at its Phase 6 gate, and the maintainer approved everything below there.
- **Tier:** T3 (blast radius B3, audience A3), rated on the imminent state. B3 on the output:
  skills from here load into sessions on work repositories whose output reaches production.
  A3: public users are intended. Both become current with the first consumer install.
- **Ownership and permission:** the sessions that produced this material ran on an
  organization's Claude plan, and under Anthropic's Commercial Terms (checked 2026-09-23) the
  organization owns their output. The maintainer holds the organization's written permission,
  from someone who can sign for it, to publish the generic, non-confidential skills and
  tooling here under Apache-2.0. The permission itself is kept privately. No copyright notice
  was added: none was named at the gate, and Apache-2.0 does not require one.
- **Chosen:** layout. Flat `skills/<name>/` in the Agent Skills layout, grouped into plugins only
  by `.claude-plugin/marketplace.json` entries (`source: "./"`, `strict: false`). Regrouping
  never moves files, and each skill directory can be uploaded to claude.ai or copied into
  another repository unchanged.
- **Chosen:** tooling in Python with uv; runner-up TypeScript. Python is present in cloud
  sessions and CI, most scripts in the old skills this library rebuilds from are Python, and
  `pwsh` is not installed in cloud sessions (re-checked 2026-09-23).
- **Chosen:** Apache-2.0 for the repository, replacing the CC0-1.0 file it was created with,
  before any content was added. The standard keeps its own CC0-1.0 dedication, and its skill's
  `license` field says so.
- **Chosen:** versioning (A13). Semantic Versioning, with one version for the whole repository,
  set in each catalog entry and bumped only on release. The changelog is written before the
  tag, and no pre-release labels are used.
  - *Major:* anything a consumer cannot take unchanged. That includes renaming or removing a
    skill, because a skill's name is public interface.
  - *0.x:* anything may change, and breaking changes are listed first in the changelog.
  - *1.0:* when the maintainer is ready to keep the skill names and the catalog's shape. That
    decision is recorded here when it is made.
  - A version that reaches `main` is published, tag or no tag.
- **Chosen, as the gate's defaults:**
  - released skills reach the maintainer's own sessions by upload to claude.ai (H2);
  - the marketplace is `rmccann-skills`, and the first plugin is `standards` (H3);
  - the standard ships as a skill (H6);
  - the skill-building toolkit is included (H7).
- **Chosen:** GitHub Actions pinned to full commit SHAs, each with its release tag in a comment
  (A16). A library that other repositories install from is part of their supply chain.
- **Chosen:** the plan lives in `ROADMAP.md`, not in issues (A28). This repository publishes its
  plan, and `skillcheck` fails whenever the roadmap, the README's skill table and `skills/`
  disagree.
- **Chosen:** the standard's own mechanical checks (its Test G) run in CI on every change (A27).
- **Declined:** A17, an OpenSSF Scorecard workflow. Its Code-Review and Contributors checks
  cannot pass with one maintainer. *Reopen when:* a second person commits.
- **Declined:** A18, a local pre-commit hook. Cloud sessions commit without it, and CI gates the
  same checks. *Reopen when:* a secret or a lint failure reaches a pushed branch.
- **Declined:** A19, mutation testing. Branch coverage is 100%, so every finding the checker can
  raise is raised by at least one test. *Reopen when:* a check is found letting through a
  defect its test says it catches.
- **Not applied:** S1-S11, changes to the standard itself. A run never edits the standard, and
  none was ticked at the gate. They are in the run report, for the maintainer.
- **Deferred:** A21, the `skill-builder` skill. *Trigger:* its turn in the build order.
- **Deferred:** a runbook for withdrawing a bad skill. *Trigger:* before the first release.
- **Deferred:** the upstream defect register, a `copier` template and reusable workflows.
  *Triggers:* in `ROADMAP.md`, under Repository.
- **Do not re-propose:** rewriting history to change the initial commit's author email. It would
  rewrite a published default branch.
- **Do not re-propose:** importing or adapting Anthropic's source-available document skills
  (docx, pdf, pptx, xlsx). Their licence forbids derivative works and copies outside Anthropic's
  services (checked 2026-09-23).
- **Alias:** the decision record here is `docs/decisions.md`.
