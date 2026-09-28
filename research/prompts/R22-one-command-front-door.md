# RESEARCH RUN R22: One command from any repository, and the questions it asks

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 27 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

Everything you need to know about the owner's repositories is written below. GitHub often
refuses automated page fetches. If you can't open a GitHub page, that is not evidence the page or
file is missing: say "could not open", try the same file at `raw.githubusercontent.com`, and
otherwise rely on what this prompt states. Never report a repository, branch or file as missing
because a fetch failed.

## Who this is for

A public repository, rmccann-hub/claude-code-skills (Apache-2.0), that other code repositories
are set up, audited and kept current against. It holds Agent Skills for Claude Code, the checks
that test them, and research like this. Its main skill runs the owner's standard,
PROJECT-BOOTSTRAP-AND-AUDIT (CC0-1.0). Professional developers will judge it, so it must be
current, precise and sourced. Today is 27 September 2026.

The owner is an engineer with a mechanical engineering background, not a professional software
developer. He knows good practice from bad and works toward best practice. He works only in
Claude Code on the web, on Linux and on Windows, with no local clone of any repository, no
desktop app and no terminal CLI. Anything recommended must work from a browser, the GitHub web
UI or the Claude mobile app, or be a file or prompt he can paste. His Claude seat belongs to a
work organization on a Team or Enterprise plan, and he runs personal projects from the same seat.

This run informs these categories: project-bootstrap-and-audit (the routing table, Phase 1
Detect Mode, the Phase 3 questions, Phase 8 Record, Choosing a Language and Runtime, Choosing the
Shape, Starter File Contents, Standards Distribution and Cross-Repository Contracts), skill-builder
(distribution, versions and trigger tests), agent-context-files, and ai-agent-security (repository
content as data). It also informs how this repository's skills are distributed.

## What this run is for

The owner's words: "i give a command to another repo to read one file from you, and you either
read the current repo and ask a bunch of questions, or its a new repo and you ask even more, like
what are you doing, why, where, etc to inform you and you can give recommendations on languages,
directions, all of that."

So the goal is one short command, typed in any repository's Claude Code session, that starts the
standard.

- **Existing repository:** it reads the repository first, then asks what the repository can't
  show.
- **New or nearly empty repository:** it interviews the owner (what the project does, for whom,
  why, where it runs, what data it keeps) and recommends a language, runtime, shape and
  direction, with the trade-offs.
- **Every run:** it stops for the owner's approval before it writes anything.

Find the best way to get there. Test the current plan below against the evidence, and say plainly
where it is wrong, weak or incomplete. Name what the owner has missed. A better design than the
one below is the most valuable thing this run can find.

## Where things stand

### The standard, past and present

- **Name:** first named AGENT-SETUP-AND-AUDIT, then renamed PROJECT-BOOTSTRAP-AND-AUDIT at
  v0.16.0. Versions are 0.x (it began at 1.0.0 and was renumbered at 0.12.1), with the version
  in the filename.
- **Today:** v0.38.0, one Markdown file of about 5,100 lines (332 KB) at
  `skills/project-bootstrap-and-audit/references/PROJECT-BOOTSTRAP-AND-AUDIT-v0.38.0.md`,
  commit `d655752`. It is read in ranges from a heading index, never end to end, and it has a
  two-axis stakes model and ten dimensions.
- **A run:** Phases 0 to 9, with two waits: Phase 3 (establish the tier, with the owner's
  answers) and Phase 6 (the approval gate). Nothing is written to the repository before
  approval.
  - The report, and a new project's first tree, are built outside the repository.
  - Phase 8 appends to the decision record Phase 1 found, whatever it is called, and never
    starts a second one. The entry records the standard's version, because the standard is
    uploaded per session and that record is the only lasting trace of which rules ran. It also
    records the tier on both axes, and what was chosen, declined (with a reopen trigger) or
    deferred. It has no field for the Phase 3 answers themselves, although a re-check is told
    to show "the recorded answers". Where no record exists, the standard names no default path
    (F23).
- **Already covered by the standard:**
  - It tells a new repository from an existing one.
  - Phase 3 asks six questions: work or personal, exposure, production, dependents, copyright
    holder, and where it runs. A new project gets three more: what it does and what starts it,
    where it runs, and what it keeps. The standard says "Do not ask a fourth question to be
    thorough."
  - A re-check shows the recorded answers and asks what has changed, with "nothing has changed"
    as the default. It asks where the software runs every time. Answers 1 to 4 from a
    reconnaissance report in the same session are used without asking again.
  - For new projects it has sections on choosing a language, a runtime and a shape. Choosing a
    Language and Runtime orders five criteria: where it runs and what is installed there, what it
    must talk to, how it ships, who maintains it, and how long it must last. It recommends with a
    runner-up and never decides, and it asks the shape rather than inferring it. Its Limitations
    say the choosing part "has never been exercised on a real project."
  - Its starter files: `AGENTS.md` as the canonical context file, and `CLAUDE.md` as a one-line
    `@AGENTS.md` shim, with Claude-specific lines below it up to about 30. Then
    `.claude/settings.json`, a CI workflow, `.editorconfig`, `.gitattributes`, `README.md`,
    `TEST-VERIFICATION-CHECKLIST.md` and a template for the decision record.
  - Its Scope rules out product direction: "this file may sequence work it proposed; it may never
    sequence the product." Recommending a direction beyond language, runtime and shape would
    widen that scope, so say whether it should, and where the line goes.
- **Delivery today:** the owner uploads the standard to a Claude Code session for each run, or
  links it at a fixed commit and has the session check its SHA-256.
- **Applied so far:** earlier versions ran live on the owner's own repositories: audits,
  applies, re-checks and a greenfield run. The standard's Provenance records them without
  naming them, and its Limitations say every rule since v0.17.0 came from "Python web
  applications and a C fork, all single-committer". From this repository, the recorded runs are
  its own set-up (v0.35.0), parity runs on synthetic samples, and the dry run below.
- **First live run of v0.38.0:** prepared for the owner's public desktop app (below). Preparing
  it found F26 to F29, and a dry run that stopped at the Phase 3 wait found F30 to F35. The
  findings relevant here, with one from the v0.38.0 test runs:
  - **F26:** Phase 3 asked its questions in the abstract, and the owner couldn't answer them as
    asked. The repository's own records held nearly every answer except where it runs. The fix
    would offer drafted answers with their evidence and still ask where it runs.
  - **F18:** v0.38.0 added a routing row for a repository that holds no source yet (F15). Its
    "Choose a language" row assumes no repository exists, so choosing a language first, in a
    repository that holds only a README, fits neither row.
  - **F27:** a cloud container lacked `libEGL.so.1`, so a Qt test suite couldn't import. The
    repository's CI installs that library with apt.
  - **F28:** the run's time-box of about five minutes rates a longer suite `NOT-RUN-HERE`, and
    that repository's suite ran about eight minutes in one process in a cloud container.
  - **F29:** nothing compares the email addresses in commit history with the owner's answer on
    ownership. A public personal repository whose commits carry an employer's address should be
    put to the owner at the Phase 6 gate.
  - **F30:** a run that stops at Phase 3 has its content defined (phases 0 to 3 and the
    questions), but not its report header or its self-check, which are defined only for Phase 6.
  - **F34:** a finding on the boundary between two repositories has no field for the side that
    owns it.
- **Rebuild:** under way. Piece 0, the parity checks, has shipped. The standard stops being one
  separate document and becomes the skill's own parts, one piece at a time, each checked by
  parity runs:
  - a `SKILL.md` procedure (the jobs, phases, two stops and report);
  - one-topic `references/`;
  - `assets/` with tested starter templates and the report's skeleton and schema;
  - `scripts/` in standard-library Python.

  Piece 1, next, moves the procedure into `SKILL.md`: the routing table, the stop rules, and the
  report's skeleton and schema. F18, F26 and F30 are assigned to it, and the building session
  calls it the "front door". The Phase 3 questions themselves move with the phase files in
  piece 4. The last piece, release 0.2.0, deletes the standard file and makes the skill
  Apache-2.0.
- **Testing:** already built, as rebuild piece 0 (`docs/testing-the-skill.md`).
  - A parity run gives the skill a job on a sample repository, built in a scratch folder from
    a manifest with planted problems (thirteen in the audit sample).
  - It grades the report against an answer key the run never sees, and against a baseline of
    earlier runs, where two runs of a sample show the noise.
  - The three samples are an audit, a re-check, and a greenfield choice that stops at Phase 3.
  - Determinism means two fresh sessions on the same commit with the same answers.
  - Live runs on the owner's repositories come between pieces, and each report is triaged.
  - No sample yet tests the front door's questions.

### How the skill reaches sessions (decisions of 2026-09-23 and what was seen since)

- **Plugin:** the repository is its own plugin marketplace. It carries the plugin `standards`
  0.1.1, a single skill, and the marketplace is named `claude-code-skills`. The owner added it on
  claude.ai under Customize > Plugins > Personal plugins > Add marketplace.
- **What reached cloud sessions:** none. A fresh cloud session on Claude Code 2.1.281 had an
  empty synced-plugins folder and no `standards` skill. The working session that checked had
  loaded the skills enabled on the owner's claude.ai account, but none of the plugins enabled
  there, Anthropic's included: the account's plugin list came back empty. On 2026-09-23 Claude
  Code's plugin docs were read as saying cloud sessions download the account's plugins. Read on
  2026-09-28, they say "Synced plugins load in Cowork sessions and in terminal sessions where you
  sign in with your claude.ai account", and name no cloud session, while the skills docs still
  say cloud sessions load the account's skills. The owner has a support ticket open about
  plugins.
- **Decision:** uploading the skill to claude.ai is the route into cloud sessions.
- **Organization route:** a GitHub-synced organization marketplace must be a private or internal
  repository, and this one is public. An organization could still take the plugin as an
  uploaded ZIP, one upload per release.
- **Controls:** a repository's committed `.claude/settings.json` can turn off the plugin's copies
  (`"standards@synced": false` and `"standards@claude-code-skills": false` under
  `enabledPlugins`), and this repository's does. It can't stop claude.ai skills syncing:
  `syncClaudeAiSkills: false` is honoured in user, local (`.claude/settings.local.json`) and
  managed settings, and ignored in the committed `.claude/settings.json`. Claude Code's docs let
  any settings file, the committed one included, hide a skill with `skillOverrides` or block it
  with a `Skill(...)` deny rule. Whether either keeps one uploaded skill out of a repository's
  sessions hasn't been tried.
- **Stale copy:** on 2026-09-27 a claude.ai chat (the one this prompt was drafted in) loaded the
  plugin's skill as `standards:project-bootstrap-and-audit`, carrying standard v0.36.0, while
  the repository was at v0.38.0. A copy can therefore be two versions behind with no warning.
  The plugin's version in `.claude-plugin/marketplace.json` has stayed 0.1.1 since 2026-09-23,
  while the standard inside it moved from v0.36.0 to v0.38.0, which may be why the chat never
  took the newer copy. The repository chose this: its v0.37.0 decision deferred a release, and
  its README says installed copies update only when the version changes. That rule is
  documented for Claude Code, not for claude.ai chats. GitHub holds a `v0.1.0` tag and release,
  and no `v0.1.1` tag.
- **Older skills:** the owner also keeps an older skill set (about 32 organization skills and a
  personal set, synced from GitHub by PowerShell scripts, coordinated by a skill-orchestrator).
  They load in every cloud session on the account, this repository's included. This repository
  copies nothing from them: they are a list of topics, checks and lessons. Once a rebuilt skill
  ships, its old claude.ai copy is turned off or replaced, so sessions don't load two versions
  of one skill.

### The plan so far (a building session on 2026-09-27)

1. **No file to fetch:** upload the skill to the claude.ai account once. Cloud sessions load
   account skills automatically. Each release produces a ready-to-upload file, and the pinned
   link stays as a fallback.
2. **Fewer, easier questions:**
   - For an existing repository, it reads the code first, drafts each answer with where it found
     it, and has the owner confirm or correct in one reply. It asks outright only what no
     repository shows: where it actually runs, who uses it, and whether it is work or personal.
   - For a new repository, it runs a short plain-language interview (what it does, who uses it,
     where it runs, what data it keeps), then recommends a language and layout with trade-offs.
   - Next time, it shows the last answers and asks only what changed.
3. **Order:** build it as the rebuild's front-door piece, with F26's question style. Run the
   first live audit, on the app below, first, to learn from a real run. The fork below is then
   the first one-command run.
4. **Open question:** is this only for the owner, or will colleagues run it on work
   repositories? If colleagues use it, their company's rules must live in work repositories or a
   private organization skill, never in this public one.

Refinements proposed since, to test:

- **Call the skill by name:** "run project-bootstrap-and-audit" beats relying on a phrase
  matching its description. An account skill sits in every cloud session, so a vague phrase
  could misfire mid-task.
- **Keep the byte check:** put the expected SHA-256 of the reference file in `SKILL.md` and
  compare it at Phase 0, so a stale or partial copy stops the run.
- **Keep the answers in the repository's decision record,** where Phase 8 already writes the
  version, so the next run can read them. The report outside the repository is invisible to the
  next session.
- **Read paired repositories from their protocol files:** where one names the files shared
  byte-identical with a sibling repository, read it instead of asking. Never touch shared files
  or append-only records.

### The first real test: two paired repositories

The first is the owner's public Python and Qt desktop app for Linux. The second is his C fork of
the upstream command-line tool the app drives. The fork's default branch mirrors upstream, and
the work lives on a separate branch. They coordinate through a formal handshake:

- laps are files committed in both repositories;
- four shared documents are kept byte-identical, with custody in the fork (`docs/OWNERSHIP.md`);
- a lap counts as sent, and its verdict can be read, only once the owner releases it.

Their always-loaded context files are far over the standard's budgets. The app's `CLAUDE.md` is
77 KB over 359 lines, and the fork's is 145 KB over 2,306 lines, against a one-line shim and an
`AGENTS.md` under about 150 lines. Neither repository has `AGENTS.md`, `.claude/rules/` or
`docs/decisions.md`; the app keeps its numbered decisions in `PLANNING.md`.

A proposal the owner has given both sides hands their `CLAUDE.md` restructuring to the
standard's runs, and asks whether a run's approved changes may land while a handshake round is
open.

## Rules

1. **Primary sources first:** official documentation, specifications and standards bodies, and
   each product's own release notes and changelogs. For Claude Code and claude.ai, that means
   Anthropic's documentation, help center, changelog and engineering posts. Use secondary sources
   only where no primary source covers the point, and label them "secondary".
2. **Cite every fact:** the URL, the exact sentence you relied on in quotation marks, and a date
   (the source's own date, otherwise the date you read it).
3. **Never guess.** Write "not found" when you can't source something. Write "contested" when good
   sources disagree, and give each side with its source.
4. **Documented or observed:** for every claim about how Claude Code or claude.ai behaves, say
   whether it is documented, observed, or both, with the product version and date where known.
   Where the documentation and the behaviour described in this prompt disagree, say so. That gap
   is a finding.
5. **"What we believe" is the owner's current understanding and may be wrong or out of date.**
   Confirm or correct every item, each with a source. The corrections are the most valuable part
   of this run.
6. **Licences:** for each source, name its licence and say what an Apache-2.0 repository may do
   with it: quote briefly, paraphrase, or adapt its code examples, and with what attribution.
7. **Depth over breadth.** Finish the Priority questions fully. If you run out of room, list the
   rest under "Not covered".
8. **Beliefs marked "(the standard, 2026-09)"** come from PROJECT-BOOTSTRAP-AND-AUDIT v0.38.0's
   section of dated facts, some with a later observation added. Checking them also checks that
   standard, so say plainly when one is wrong.
9. **Measured over asserted.** Where a question asks what works better, give measurements: what
   was measured, on what, when, and how large the effect was. Label an estimate or an opinion as
   one.
10. **Browser only.** Don't recommend anything that needs a local clone, a terminal CLI or the
    desktop app, unless you name it as out of reach and give the browser route beside it.

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R22 · FORM: research-result v1
Save as: R22-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.
```

Then these sections, in this order:

1. **Summary:** at most 15 bullets a professional must know today.
2. **Corrections:** every "What we believe" item that was wrong or out of date, with the right
   fact and its source.
3. **Facts table:** `| # | Fact | Value | Documented or observed | Source URL | Exact quote | Date |`
4. **Findings:** one section per question below, numbered to match.
5. **Routes compared:** `| Route | Reaches | Pin or verify | Update cost | Token cost | Stale risk | Empty repo | Colleagues | Sources |`.
   "Reaches" covers the web, mobile, claude.ai chat, routines, CLI and desktop. "Empty repo" asks
   whether it works in a repository with no source yet.
6. **Recommended design:** the front door step by step: how it is triggered, how it tells new from
   existing, what it reads, what it drafts, what it asks and how, what it recommends, where it
   stops, and what it records for next time. Say which rebuild piece each part belongs to, what
   the owner can use first, and what waits.
7. **Changing in the next 12 months:** announced or likely changes to skills, plugins, cloud
   sessions and routines.
8. **Common mistakes,** including those AI coding assistants make when interviewing an owner or
   recommending a stack, with sources.
9. **Sources and licences:** `| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |`
10. **Not found, contested, not covered.**

## What we believe (confirm or correct each)

- Claude Code loads a skill when a request matches its description. Until then only the name and
  description sit in context, so a long reference file costs nothing until it's opened.
- A skill can be invoked explicitly by naming it, which triggers more reliably than a phrase that
  happens to match its description.
- (the standard, 2026-09) Skills uploaded to a claude.ai account load in Claude Code cloud sessions
  under that account. The standard holds this only as one account's observation on 2026-09-23,
  and its Standards Distribution table names the uploaded skill as the route into cloud
  sessions.
- (the standard, 2026-09) Plugins enabled on a claude.ai account are documented to load in cloud
  sessions as `<name>@synced`. For one account, on 2026-09-23, none did, from any source, while
  its skills did: the sync ran and received an empty list. Read on 2026-09-28, the plugin docs
  name only Cowork and terminal sessions, so the documented part may no longer hold.
- (the standard, 2026-09) A cloud session installs no plugin that a repository's
  `.claude/settings.json` turns on under `enabledPlugins`, including those from marketplaces it
  lists under `extraKnownMarketplaces`. `syncClaudeAiSkills: false` in a project's committed
  settings is ignored, while user, local and managed settings honour it.
- A plugin installed from a personal marketplace on claude.ai reaches claude.ai chats, but a chat
  can keep an old copy: on 2026-09-27 a chat had standard v0.36.0 while the repository held v0.38.0.
- A marketplace client decides whether to update a plugin by its version number, so a plugin whose
  content changes while its version stays the same is never updated.
- (the standard, 2026-09) A GitHub-synced organization plugin marketplace must be a private or
  internal repository.
- An organization can instead take a plugin as an uploaded ZIP.
- Team and Enterprise admins can provision skills for every member, and those skills reach members'
  Claude Code sessions.
- An uploaded skill may carry a large reference file and scripts, within limits on upload size and
  file count that we haven't confirmed.
- Claude Code has a built-in tool for asking the user multiple-choice questions, and it works in
  web sessions and the mobile app.
- A Claude Code web session needs a GitHub repository to start, so a brand-new project needs an
  empty repository created first, unless its interview happens in a claude.ai chat.
- (the standard, 2026-09) In a cloud session, a public repository's committed files arrive
  through `raw.githubusercontent.com`, which is on the default Trusted network list, while GitHub
  API and release-asset requests reach only repositories attached to the session. The
  release-asset half has been seen failing (F33): on 2026-09-26, and again on 2026-09-27, an
  unattached public repository's release asset downloaded with a 200 while its API returned 403.
  Say what holds.
- (the standard, 2026-09) Claude Code's web-fetch tool returns a small model's answer about a page,
  not the page, and `curl` gets the page.
- Routines are saved Claude Code configurations (a prompt, repositories, an environment and
  connectors), started by a schedule, an API call, a GitHub event or Run now, and they run without
  approval prompts.
- Claude Code Projects aren't available on Team or Enterprise plans yet.
- (the standard, 2026-09) Anthropic's target for `CLAUDE.md` is under 200 lines, and Claude Code
  loads one of up to 4 MiB in full and skips a larger one.
- Path-scoped rules in `.claude/rules/` load only when a matching file is read.
- (the standard, 2026-09) `AGENTS.md` is read directly by most other major agent tools, and Gemini
  CLI and Aider need one config line. Claude Code reads it natively from v2.1.277, but only when
  no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists, and not in sessions without
  feature flags (Bedrock, other providers, telemetry off), in the first session after an install
  or upgrade, or with the built-in `agents-md` plugin disabled. So a one-line `CLAUDE.md` shim,
  `@AGENTS.md`, imports it: that works in all of them and "never makes Claude read `AGENTS.md`
  twice".
- Showing an owner drafted answers with their evidence, to confirm or correct, takes less effort
  and gives more accurate answers than asking open questions. We have one observation (F26) and
  no measurement.

## Questions

### Priority

1. **The one command, route by route.** For each route, say which surfaces it reaches, whether the
   owner can pin and verify the exact version, what an update costs per release, what it costs in
   tokens per session, how stale copies arise and are prevented, whether it's documented or only
   observed, and what the owner types to start it. The routes:
   - a skill uploaded to the claude.ai account;
   - a skill provisioned by the organization's admins;
   - a plugin from a personal or organization marketplace;
   - a link to the standard at a fixed commit plus its SHA-256, pasted as a prompt;
   - a remote MCP server or claude.ai connector that serves the standard or runs the interview;
   - a routine started with Run now;
   - a GitHub template repository or a copier template for new projects;
   - a line committed in each repository's context file;
   - the Claude Code GitHub Action;
   - anything better.
2. **Knowing which copy ran.**
   - How versions of uploaded, synced and plugin skills are managed, and whether uploading a new
     version replaces the old or adds a second.
   - What happens when copies share a name, and how to find and remove a stale copy like the
     v0.36.0 one above.
   - Whether a skill can verify its own bytes at start, and how published skills record which
     version ran.
3. **Fewer, better questions for an existing repository.**
   - What a repository can and can't reveal: where it runs, who uses it, what data it holds,
     work or personal, how bad a failure would be, how long it must live.
   - How to draft answers with evidence for one-reply confirmation, and how to word questions
     for an owner who isn't a software professional.
   - Whether multiple choice with a recommended default helps or biases.
   - How the built-in question tool renders on the web and on mobile.
   - What requirements-elicitation, survey-design and human-computer-interaction research say
     about the number of questions, defaults and leading questions.
   - What studies of AI agents asking clarifying questions found, and when asking helps or
     annoys. Give measurements where they exist.
4. **The new-project interview and the recommendation.**
   - The fewest questions that let a tool choose a language, runtime, shape and layout
     responsibly, and the published decision frameworks for it.
   - How to present trade-offs to a non-specialist and record the choice.
   - How to weigh fewest dependencies and newest versions (run R21, whose result is pending), and
     the owner's platforms: Windows Server, Linux, Epicor Kinetic, SOLIDWORKS and Office.
   - The biases AI assistants show here: defaulting to Python or JavaScript, trendy frameworks,
     outdated versions.
   - Whether the interview should start before a repository exists (in a claude.ai chat), in an
     empty repository, or in one that holds only a README.
5. **Remembering answers between runs.**
   - Where answers should live: the repository's decision record, a machine-readable block in
     it, or somewhere else.
   - How the next run shows the last answers, asks only what changed, and notices when an answer
     has gone stale.
   - What must never be written into a public repository's answers, including work details and
     private addresses (F29).

### Standard

6. **Paired and multi-repository projects.**
   - How a run detects that a repository has a sibling.
   - How it reads a protocol file that names byte-identical shared files, and keeps away from
     append-only records.
   - Published practice for agent context across several repositories, compared with the
     standard's Cross-Repository Contracts section.
7. **Colleagues and the organization.**
   - How Team and Enterprise admins provision and control skills.
   - How company-specific rules stay private while the standard stays public.
   - What the CC0 standard inside an Apache-2.0 repository means for someone who copies or
     adapts it, now and after rebuild piece 6, when the skill becomes Apache-2.0 (decision of
     2026-09-23).
8. **A safe one-command run.**
   - Treating repository content as data, never as instructions.
   - Keeping the two waits when the whole run starts from a single command.
   - Token and time budgets for a 332 KB standard read in ranges, test suites longer than the
     time-box (F28), and cloud containers missing system libraries (F27), with cost estimates
     where published.
9. **Testing the front door.**
   - How skill authors test that a skill triggers reliably.
   - How to score question quality: questions asked, answers the owner corrected, time to the
     first report, tokens used.
   - How the owner's planned determinism runs and seeded testbed repository should measure them.
10. **What we missed.** Anything else a professional would build into a one-command setup and
    audit tool for one owner who works only in a browser, or expect of it. Examples: scheduled
    re-audits, the mobile app, or a way back to a known-good state.
