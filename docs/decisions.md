# Decisions

Append-only. Supersede by adding a new entry that points at the old one; never edit history.

## 2026-10-21 — Release 0.1.19

- **Asked, by the owner:** "do everything you can up to 6 and release. plan 7 for the next
  release after we have more info", of a list of tasks given that day, and "update your own
  dependencies if possible, we should be practicing what we preach".
- **Carries:**
  - the example checker and the trigger-test runner, two of the rebuild plan's shared tools;
  - the three rules on what the text says (the entry below);
  - `--outdated`'s fixes: requirements locks, tag-pinned actions, a comment taken for a
    version, and each registry asked once a run;
  - the New York-first times and standard v0.48.1, merged on 2026-10-20.
- **The roadmap, corrected:** the weekly currency check is shipped as the Freshness workflow,
  less an end-of-life warning, now a row of its own; the map refresh on Dependabot's updates
  is shipped as CI's `--bom-check`.
- **Item 7, the two company audits' fixes:** planned in the private repository's roadmap,
  which can name them, to follow the owner's answers to the audits' questions.
- **Own dependencies:** nothing is behind. uv 0.13.4 and Claude Code 2.1.305 came out on
  2026-10-20, inside the three-day wait the rule keeps, so they wait for Dependabot's pull
  requests after 2026-10-23. Practicing the rule means waiting, too. ShellCheck comes in at
  its newest, `shellcheck-py` 0.11.0.1.
- **Release 0.1.19:** this pull request's merge, released by the Release workflow once CI
  passes on it.

## 2026-10-21 — Checking what the text says

- **Asked, by the owner:** "are we checking for good info security? for plausible deniability
  when needed it (for testing)? things like this? input and output sanitation, not just of
  type and int, etc, but of what they say? but we should do the rest too." Then, as examples:
  "i know this is a test, let me give fake data, not use real for a test", and "i need to make
  sure the other application cannot accidentialy read this data it is necessary to uphold our
  stanards".
- **Read as:** the habits an agent should have, fake data in tests and one application's data
  out of another's reach, so the checks enforce them. The owner was told so, and asked to say
  if they meant phrases to flag.
- **Done, as `skillcheck` rules that run with every check:**
  - `test-data`, in skills and tests: reserved email domains, RFC 5737 addresses, and
    `CHANGEME` or a placeholder for a secret's value; a real credential's prefix fails
    anywhere;
  - `content-safety`, in what agents read: fetch-and-run commands, and text steering an agent
    against its user. Quoted text passes, as a quotation;
  - `private-name`, everywhere: names this public repository withholds, listed only as
    SHA-256 hashes in `.github/private-names.sha256`. The list was seeded with the private
    repositories, the owner's employer and the repositories the skills ran on, and names none
    of them.
- **Considered for the names:** a list in a CI secret, which no local run or session could
  read; a keyed hash, the same. A plain hash can be confirmed by someone who already guesses a
  name, and reveals nothing to anyone who doesn't, which is the risk that matters here.
- **Left to the modules that teach it:** sanitizing input and output in the code the skills
  teach, by meaning and by context. That's `input-handling`, `secure-coding` and
  `ai-agent-security`, after research R04 and R01. Keeping one application's data from
  another goes there too, and into the standard as a proposed change once that research is in.

## 2026-10-21 — The example checker and the trigger-test runner

- **Asked, by the owner:** the rebuild plan's shared tools, approved on 2026-10-15 and 16, and
  "do everything you can up to 6".
- **Built:** `skillcheck --examples`, which CI runs, and `skillcheck --triggers` with
  `--tries`, which run by hand.
- **Chosen:** ShellCheck pinned through `shellcheck-py` (MIT) in the dev group rather than the
  runner image's, so CI and a local run use one version. PowerShell is parsed by `pwsh` from
  GitHub's Ubuntu image, fed on standard input so nothing runs; no skill holds PowerShell yet.
- **Found by the first live trigger run:** none of the four `gitignore` requests loaded
  `git-workflows` in Claude Code, which answered them from its own knowledge. The descriptions
  get tuned against the runner before the rebuilds.

## 2026-10-20 — Standard v0.48.1: the order of a local time and its stamp

- **Asked, by the owner:** "New York first", for how times are given to them; the entry below
  changed this repository.
- **Changed, in the standard, as F154 and a change of its own:** Phase 0's fifth question also
  asks which comes first, and `display_time` in the Phase 0 block records it. The stamp is
  unchanged: UTC, whatever the answer.

## 2026-10-20 — Times to the owner: New York time first, the UTC stamp beside it

- **Asked, by the owner:** "yes all should match", for how three repositories give times; then
  "New York first", when asked which order.
- **Supersedes, in part,** the entry of 2026-10-19 on UTC as the stamp. The stamp is
  unchanged: every record is UTC, and every local time is derived from it by the tool. Only the
  order shown to the owner changes, to the one the owner's other two projects agreed between
  them on 2026-10-19.
- **Changed here:** `skillcheck --time`'s output, the `times` check, AGENTS.md and the house
  style. The standard's own example changes on its own, as the standard's changes do.

## 2026-10-20 — Release 0.1.18

- **Asked, by the owner:** "proceed when ready", for release 0.1.18.
- **Carries:**
  - standard v0.48.0, with UTC as the stamp;
  - `skillcheck --time` and the `times` check;
  - `skillcheck --outdated` and its weekly run;
  - Python 3.15 and the other dependency updates;
  - the house style's rule on copied times;
  - the lessons from the two-repository loop.
- **Release 0.1.18:** this pull request's merge, released by the Release workflow once CI
  passes on it.

## 2026-10-19 — Every dependency on its newest release, checked weekly

- **Asked, by the owner:** "are all repos using the most up to date of all dependcies, they
  should. And we need a way to make sure they are. Like a weekly repo check".
- **The rule:** each dependency is on its newest stable release once that release has been out
  three days, the platform's default wait, which the standard already holds. Security fixes
  don't wait. Research prompt R21 tests the rule against the evidence; its result may change
  the wait or the exceptions.
- **Done here:** Python 3.15, uv 0.13.1 in CI, Claude Code 2.1.302 and the dev tools' newest
  releases (#66), and uv 0.13.1 in the private repository's CI.
- **The check:** `skillcheck --outdated`, run weekly by the Freshness workflow in an issue of
  its own. It reads what a repository uses through the dependency map's readers, so the two
  never disagree. It covers what Dependabot doesn't: tool versions a workflow names as
  inputs, `.python-version`, and a range in `pyproject.toml` that shuts out a new release.
- **Considered:** Dependabot alone, which can't see those three; Renovate, which can, but is a
  second update bot with its own configuration to keep. The check proposes nothing itself;
  Dependabot still opens the update pull requests.
- **Not covered:** runner images and system packages, since neither has a registry naming its
  newest version.
- **Other repositories:** the owner's other projects get their lists and the command to run,
  through the owner. Nothing in them was changed here.

## 2026-10-19 — A two-repository loop's audit against a reference tool, checked for lessons

- **Asked, by the owner:** "do a full check against both repos … see if you missed anything and
  fix yourself as well".
- **Read:** one repository's audit of its output against an established tool's, and each of
  its numbers against the primary logs, reports and source it cites. Nothing in either
  repository was changed; the findings went to the owner as a report outside this repository.
- **Taken into a shipped module:** `writing-style`, that a time copied from a source keeps the
  zone the source gave it.
- **Waiting for their modules,** as L41 to L44 in `ROADMAP.md`: a reference checked before a
  match with it counts, corroboration that is independent and carries weight, "not found"
  against "couldn't look", and a summary computed from the same state as its verdict.
- **Missed by this repository's earlier review of the same loop,** on 2026-10-19: the
  corroboration and absence findings. Both were in records it read.

## 2026-10-19 — Rounds 34 and 35 of the two-repository loop, read for lessons

- **Asked, by the owner:** "do a review of both repos and see what is learned".
- **Read:** both repositories' history from 2026-10-15, by two read-only reviewers, one per
  repository. Each lesson cites its commits or lap statements, and those quoted here were
  checked against them before they were used. Nothing in either repository was changed.
- **Taken into shipped modules:**
  - `ci-workflows`: a timeout with no known cause is recorded each time and instrumented, not
    hidden by a higher limit; diagnostics that print only on failure; a build chain that goes
    on after a step fails;
  - `releases-and-versions`: a release staged and never published; a candidate proved only in
    the working tree;
  - `commits-and-pull-requests`: a fix to inherited upstream code whose commit doesn't say so.
- **Waiting for their modules,** as L31 to L40 in `ROADMAP.md`: checks that can fail, a ratchet
  after a flaky fix, the seam between two tools, shared validation, four on running the loop,
  parallel helper sessions, and checked status against unchecked prose.
- **Already held here, so not added:** a push in the same command as a failing suite, trimmed
  output, a stale local branch, approval given with the request, and a file agreed word for
  word.

## 2026-10-19 — Standard v0.48.0: UTC is the stamp, and a first audit asks the reader's zone

- **Asked, by the owner:** "on an iniitial audit, you can ask for what to use, but gmt should
  be the "stamp"".
- **Changed, in the standard, as F153 and a change of its own:** Phase 0's questions that can't
  be detected gain a fifth, asked at the Phase 3 wait: the time zone and clock the human reads
  times in. Whatever the answer, every time a run writes is UTC with its zone; the answer adds a
  local time beside each stamp in what the run tells the human, worked out with the time zone
  database. The draft comes from the offsets on the human's own commit dates, and the default
  is UTC alone. `display_time` joins the Phase 0 block's `asked`.
- **Not done:** no parity run. The samples' answer keys rate findings, and a question asked at
  the wait changes no finding.

## 2026-10-19 — UTC is the stamp, local times are derived, and a check holds it

- **Asked, by the owner:** "GMT is the gold standrad, just derive from that. we need timestamps
  to be correct. make sure the check for this, and on an iniitial audit, you can ask for what to
  use, but gmt should be the "stamp"". This sharpens the entry below on times given in UTC and
  New York time.
- **Built:** `skillcheck --time STAMP [ZONE]` gives an ISO 8601 time, which must carry its
  offset, as UTC and as the zone's local time, worked out from the time zone database. Its
  tests cover the hour New York's clocks repeat on 2026-11-01. `now` is the current time.
- **Checked:** the `times` rule fails Markdown here that writes a time of day without UTC, or a
  12-hour local time with no UTC time before it on its line. It leaves code, ISO 8601 times,
  dated research results and decision entries dated before 2026-10-19 alone: the one time it
  finds today is in an entry of 2026-10-05, which stays as written.
- **Written down:** `AGENTS.md`, and the house style's *Records and dates*, which every
  repository using `house-style` follows. The standard asks the question at a first audit, in its
  own change.
- **GMT or UTC:** the stamp is written `UTC`, the name time zone databases and ISO 8601 use; `GMT`
  passes the check too, since for a timestamp the two agree.

## 2026-10-19 — Times given to the owner in UTC and New York time

- **Asked, by the owner:** "can you also provide them in my timezone, EST/NYC and using a 12 hour
  clock with AM/PM? present both. just as a standard until i change this."
- **Decided:** `AGENTS.md` asks every session to give a time to the owner as recorded, in UTC on
  a 24-hour clock, and in New York time on a 12-hour clock with AM or PM and the zone in effect,
  EDT or EST. Commits, records and files keep UTC alone, which the owner called fine for
  official records. The private repository's `AGENTS.md` says the same.

## 2026-10-17 — Release 0.1.17, for people beyond the owner

- **Asked, by the owner:** "release", so their brother installs the current skills: the
  modules, the report section in every skill, and the dependency updates.
- **Release 0.1.17:** this pull request's merge, released by the Release workflow once CI
  passes on it.

## 2026-10-16 — Every skill says when it's at fault, and drafts the report

- **Asked, by the owner:** "You should include some level of this in yourselve for all skills.
  It shouldn't be much, but if someone has an issue or concern, there would be a sentence or a
  word that gives it away and why. If it's a bug somewhere then yes give a verbose answer." The
  owner wants their brother, and later colleagues, to use the skills on real work and report
  what goes wrong.
- **Decided:** every `SKILL.md` ends with one shared section, `When something here is wrong`.
  When a person says advice is wrong, out of date, failed or doesn't fit, the model answers the
  problem first, then says in one sentence whether the fault looks like the skill's, and why.
  When it is the skill's, it drafts a full report to paste as an issue: skill and module,
  version, the request, the line that misled, what happened, what's right with its source, and
  a suggested fix. Private data, company detail and repository names stay out, and it files
  nothing unless asked.
- **Why one text, held word for word:** the section changes how every skill behaves, so it is
  kept once, in `src/skillcheck/core/reporting.py`. `skillcheck` fails a skill without it, or
  with any other wording, and `--new` writes it. The address comes from the catalog's
  `repository`, so a repository that uses these tools for its own skills reports to itself.
- **Why at the end of `SKILL.md`, not in a module:** it applies whatever module is read, and
  `SKILL.md` is always read when the skill loads. It costs about 900 characters per skill, and
  nothing in the listing, which holds descriptions only.
- **Also done the same day:** Dependabot's four open updates came in together, as #58, with the
  git-workflows example moved to the same `setup-uv` commit. The private repository's one
  update merged on its own.

## 2026-10-16 — `git-workflows` and `house-style` made of modules, and facts named across the repository

- **Asked, by the owner:** "do the rest if you can", on the weekend's work, which included
  converting both skills.
- **Changed, superseding part of "The tools for skills made of modules" below:** a module may
  name any fact the repository defines, not only its own. An ID is still unique across the
  repository, so a fact's name never means two things, and a module that moves keeps every fact
  it names. `skillcheck` reports a name no fact table defines.
- **Why:** the git-workflows facts were each named by several of its topics. Under the old rule
  each module would have needed its own copy of a shared fact, which the unique-ID rule forbids,
  or the topics would have had to stay together.
- **`git-workflows`, eight modules:** `commits-and-pull-requests`, `branches-and-merging`,
  `ci-workflows`, `actions-security`, `git-hooks`, `releases-and-versions`, `leaked-data` and
  `gitignore`. Its nine rules stay in `SKILL.md`, each naming the module that holds it, with the
  commands to check before acting and the audit's status words. Each of the 103 facts and 30
  audit checks went to exactly one module, by script, checked for none lost and none doubled.
  `leaked-data`, `git-hooks` and `gitignore` had no Why or Audit of their own, so they gained
  them, from reasons and checks the old files already stated.
- **`house-style`, two modules:** `writing-style`, with how each rule applies, its reasons and
  the style guides' facts, and `prose-check`, with the Vale check, its reasons and Vale's facts.
  The thirteen rules stay in `SKILL.md`, where the asset tests read rule 3.
- **Kept as they were:** both skills' names, descriptions, assets and asset tests. Each skill's
  trigger set in `tests/fixtures/skills/` stays, because the description still decides whether
  the skill loads. Each module has its own set in `tests/fixtures/modules/`, for which module a
  loaded skill reads.
- **`.vale.ini` skips double-quoted text in every module,** where it skipped it in `facts.md` and
  `sources.md` before, because each module now holds its own facts and sources.
- **Considered for the new trigger sets:** the skill-level sets, which answer a different
  question, and one file per skill, which a move would have to split. One file per module, as
  the module checks already require, moves with its module.

## 2026-10-16 — Skills made of modules work on claude.ai, and are tried there by hand

- **Asked, by the owner:** "This does still need work with claude.ai as well."
- **Read, at Anthropic's Agent Skills overview
  (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview, 2026-10-16):**
  - a skill's name and description are always loaded: "Claude loads this metadata at startup
    and includes it in the system prompt";
  - when triggered, "Claude reads SKILL.md from the filesystem using bash", and other files
    when its instructions point to them, so a module costs nothing until read, on claude.ai as
    in Claude Code;
  - the triggered file's cost is given as "Under 5k tokens";
  - custom skills on claude.ai need "code execution enabled", and there skills "may have full,
    partial, or no network access" by settings;
  - the API takes "up to 20 Skills for each request" (the skills guide, read the same day).
- **Changed:** `skillcheck` holds each `SKILL.md` to 20,000 characters, about 5,000 tokens.
  The authoring guide's step 5 adds the claude.ai rules: no Claude Code tool names, core
  guidance without the network, and the owner's tries listing for each module the skill and
  module a request should reach, and a near miss.
- **Chosen, by the owner:** claude.ai is tested as the six tries were, by the owner asking
  questions in new chats from a list the session gives, not by an API run, which needs a key
  and costs money. In their words: "that is fine, that is what i want for claude.ai."

## 2026-10-16 — The tools for skills made of modules

- **Built, as the roadmap's shared tools planned, with the owner's permission:**
  - `skillcheck` checks a skill made of modules: its router table, each module's file and its
    six sections, each module's trigger tests (requests that should reach it and near misses),
    no Markdown in `references/` outside a module, one home per module name, and each built
    module's shipped `ROADMAP.md` row naming its skill;
  - facts live in each module's Facts section, a module names only its own, and an ID is
    unique across the repository, so a module moves without a collision;
  - `skillcheck --new SKILL` writes a router, `--new-module MODULE SKILL` adds a module, and
    `--move MODULE SKILL` moves one, refusing with nothing changed when it can't;
  - the listing budget is room for 20 skills.
- **Why a router table and not a manifest file:** the table is what Claude reads to pick a
  module, so the one list both routes and registers, and can't disagree with itself.
- **Why `docs/module-moves.md`:** the moves need a record the command can append to and a
  person can read. `docs/decisions.md` is prose, appended by hand; `ROADMAP.md` holds the plan,
  not the history; a release's changelog is cut at release. None fits a row per move.
- **Not done yet:** `git-workflows` and `house-style` keep their older layout until they're
  converted, which the checks allow. The trigger-test runner, the example checker and
  `skill-builder` follow in their own pull requests.

## 2026-10-16 — Fifteen skills made of modules, in place of a hundred skills

- **Asked, by the owner, verbatim:** "I want the functionality and more, I don't. Care how it is
  divided, named, etc. I want it to be efficent and effective. So if that means a complete
  restructure I'm all for it, and now is the time to do a complete refactor on this. So don't
  hold back. But it needs to work, make sense, and be structured so that if we need to do so
  again it's easy and not a mystery with a ton of research. We should be able to spin off a
  skill into multiple if needed, or whatever."
- **Decided:** `ROADMAP.md` now plans 15 skills, each a trigger, made of modules. The 60
  planned skills become modules under their old names, each with one home skill, so the
  research prompts, lessons and intake that name them still apply. Its new section *How skills
  are structured* gives the rules: a module is one self-contained file, a router `SKILL.md`
  picks it, trigger tests decide when a module spins off, merges or moves, and a move is one
  `skillcheck` command with a record.
- **Why:** each installed skill's description is in context all the time, and Claude Code
  gives the listing 1% of the context window, 8,000 characters on a 200,000-token model (the
  2026-10-15 entry measured it). A hundred skills at 240 characters would leave most of them
  as bare names there, and colleagues' claude.ai accounts load the same descriptions. Fifteen
  fit. A module costs nothing until it's read.
- **Supersedes:**
  - the 2026-10-15 entry's room for 100 skills: the listing budget becomes about 20 skills in
    the shared tools;
  - the 2026-10-15 answer 7, replacing old skills in place: old copies are deleted as each
    wave ships, which the owner already chose earlier today;
  - decision 33's pairing map, which shrinks to the pairs between skills;
  - this session's own advice earlier today to keep a skill per language. One `coding` skill
    with a module per language costs one description instead of eleven, and its trigger tests
    decide whether any language spins off.
- **Not changed:** the three shipped skills keep their names. The research waves are the same.
  `AGENTS.md`'s invariant that every skill links `references/why.md`, the authoring guide's
  layout and the listing rule change with the module checks, in the shared tools' pull request.

## 2026-10-16 — The organization's library read, `code-standards` counted, and private skills by token tried

- **Read, from the owner's screenshots of the admin inventory:** the organization's library
  holds 28 of the owner's old skills, each with the audience "Everyone · installed by
  default". Colleagues use them: the owner says about five use claude.ai and one uses Claude
  Code.
- **Found:** `code-standards` is among the 28 but not among the copies synced into sessions.
  It left them on 2026-09-28, when the owner deleted their own copy, and the library kept it.
  The plan counted 33 old skills from the synced copies, so it missed it. `ROADMAP.md` now
  counts 34 and sends its topics to five planned successors, its old copy going last, since
  twelve old skills say they must read it first.
- **Chosen, by the owner, verbatim:** "we should just keep removing them as we replace them. i
  can then tell people to start using the plugins". Deleting an old copy takes it from
  colleagues too; they add this repository's plugins themselves. `ROADMAP.md` records it as
  its colleagues step.
- **Changed, in `docs/authoring-a-skill.md`:** step 12 has the old copy deleted in the
  organization library's inventory as well as in the owner's own settings.
- **Tried, and refused:** a read-only token for the private companion, held as a network secret
  in the cloud environment, so a session without the repository attached could install its
  skills. A fresh session with only this repository attached got 403 on every request: "GitHub
  access to this repository is not enabled for this session. Use add_repo to request access."
  The cloud's own access check comes before the secret, so attaching the repository stays the
  way in, and the owner deletes the secret and the token.

## 2026-10-16 — The private companion repository, set up, and the empty one deleted

- **Done, by the owner:** they deleted the empty organization repository, which item 29 of the
  2026-10-13 answers had said to archive; this supersedes that item. They created the private
  companion repository that item 5 of the 2026-10-15 answers asked for, set its settings by the
  steps given, and attached it to the session.
- **Set up against the standard, v0.47.0:** the run stopped at both waits, and the owner
  approved all ten items. Its record holds the answers. This entry names only what bears on
  this repository:
  - **Its tier is T1:** work-owned, never public, guidance and templates that change no system
    themselves, and used by the owner alone for now. Sharing it with colleagues through the
    organization's library raises it to T2, and the standard runs again first.
  - **It reuses this repository's tools rather than copying them.** Its CI runs `skillcheck`
    from this repository at release 0.1.16's commit, and the house style from that release's
    `HouseStyle.zip`. Each release here can be taken up there by raising one pinned commit.
  - **Its skills reach sessions** by a second personal marketplace on the owner's claude.ai
    account, and by attaching it to a cloud session: the cloud hook here downloads releases
    without credentials, which a private repository refuses.
  - **Its plugin and skill names** start with the company's name, so none clashes with a
    skill here.
- **Found:** on GitHub Free, a private repository's ruleset request is refused with "Upgrade to
  GitHub Pro or make this repository public", so its checks warn rather than block, as the
  standard's platform table says.
- **Said, by the owner:** this repository's skills are meant for colleagues too, in time, as
  the companion's are. It is public already, and rated T3 on the imminent state, so the tier
  stands; what changes is that a colleague's claude.ai account, not only the owner's, may
  install its plugins.
- **Changed:** the exclusion list's reason for `canvas-design` now says it is kept on claude.ai,
  as the previous entry records.

## 2026-10-16 — The dependency map checked on every pull request, `canvas-design` kept, and chat syncs

- **Chosen, by the owner:** CI runs `skillcheck --bom-check` on every pull request. This
  supersedes the 2026-10-05 entry's *Not run on pull requests*. A Dependabot update now fails
  until a session regenerates the map in its branch, which the 2026-10-13 answers already ask
  for before merging one. It would have stopped release 0.1.11's stale map at its pull request.
- **Chosen, by the owner:** `canvas-design` stays on claude.ai, and stays off in Claude Code
  through the exclusion list. This settles the 2026-10-15 entry's undecided item 3.
- **Found:** after release 0.1.16, a new claude.ai chat loaded standard v0.47.0 with nothing
  pulled by hand. With **Sync automatically** on, the plugins follow each release, which
  settles the question the earlier entry left for this release. No **Check for updates** step
  is needed after a release.

## 2026-10-16 — The six claude.ai tries, standard v0.47.0, and release 0.1.16

- **Tried, by the owner,** on claude.ai with the plugins at 0.1.15, each request in a new chat,
  as step 5 of `docs/authoring-a-skill.md` asks. All six pass:

  | Skill | Request | Result |
  |---|---|---|
  | `house-style` | Rewrite a paragraph in the house style | Pass: led with the change, cut the filler, American spelling, and asked about the hedge it dropped and the palette it couldn't name |
  | `house-style` | Which heading case a README uses | Pass: sentence case, citing the Vale rule; every other claim is in the skill |
  | `git-workflows` | A commit message for retry logic | Pass: a 48-character subject and a body saying why. It led with Conventional Commits, which the skill allows beside "area: summary"; the pass line named only the second, and was too narrow |
  | `git-workflows` | Squash or merge commits | Pass: merge commits, the reason and the trade. Its claims hold: all three of the owner's public repositories allow merge commits only |
  | `project-bootstrap-and-audit` | Set up a new Python CLI repository | Pass: asked the Phase 3 questions, drafted none of the three never-drafted answers, and wrote only its report. It didn't ask how long the tool must last, which the standard asks only when choosing a language, and Python was named |
  | `project-bootstrap-and-audit` | What an audit of configuration checks | Pass: the stakes questions and the ten dimensions. It found that the standard names no dangerous workflow trigger |

- **Found, and checked:**
  - python.org's release list, read 2026-10-16, gives Python 3.15.0 on 2026-10-09. The
    standard's toolchain table named 3.14.x.
  - The routing table sends "set up something new" with no repository yet through the run,
    and Phase 0 refused to continue without a git repository. The new-project run broke that
    rule to reach its questions, and recorded doing so.
  - The standard has no match for `pull_request_target`, `workflow_run` or template injection.
    `git-workflows` covers all three, in its security reference and row 13 of its audit.
- **Changed, approved by the owner on 2026-10-16, as standard v0.47.0, a change of its own:**
  F150, the Python row; F151, Phase 0's case for a new project before its repository exists;
  F152, dimension 6's rating of dangerous triggers and template injection, with a dated fact
  from GitHub's security hardening guide. A public repository with either is `BLOCKER`, as
  `git-workflows` rates it; a private one, where only collaborators open pull requests, `GAP`.
- **Not done:** no parity run. F150 changes a fact, F151 a case no sample reaches, since every
  sample has a repository, and F152 a pattern no sample's workflows contain.
- **Done, by the owner:** this repository's merge commits take the pull request's title, set
  under Settings, General, read back as `merge_commit_title: PR_TITLE`. Nothing here reads the
  old subject: the `subjects` check skips merges.
- **Release 0.1.16:** this pull request's merge, so the hook and the plugins carry v0.47.0.

## 2026-10-16 — claude.ai kept a plugin copy from 2026-09-23 until it was removed and added again

- **Found, in the owner's chat:** after the plugins were added from **Discover**, a new chat
  still loaded `project-bootstrap-and-audit` with standard v0.36.0. That is the copy installed
  on 2026-09-23, which the 2026-09-28 entry also found. It stayed through every catalog version
  from 0.1.1 to 0.1.15.
- **Fixed, by the owner:** they removed every `Standards` and `Engineering` under **Customize >
  Plugins > Yours**, and added both again from **Discover**. A new chat then loaded v0.46.0,
  with the skill's metadata and its copy of the standard agreeing, and no older copy beside it.
- **So:** a version change in the catalog doesn't reach a plugin claude.ai already holds unless
  something pulls it. Whether **Sync automatically** is that something is checked at the next
  release by asking a new chat the same question. If it isn't, each release's steps for the
  owner include **Check for updates**.

## 2026-10-16 — The automatic route, checked in the owner's environment

- **Done, by the owner:** `protect-main` now requires `prose` beside `checks`, `catalog` and
  `secret-scan`, all from GitHub Actions, read back from the ruleset at 12:34 that day. They
  deleted the old uploaded copies (step 2A of their steps), added this repository as a
  marketplace in their own **Customize > Plugins**, and added the setup lines to their cloud
  environment.
- **Found:** **Organization settings > Plugins & skills > Sync from GitHub** lists only private
  and internal repositories, and says to fork a public one into a private one first. That is
  the organization-wide route, and the attempt there failed; the owner's own **Customize >
  Plugins** took the same repository with no error.
- **Checked:** a fresh cloud session in that environment, with no repository, listed
  `git-workflows`, `house-style` and `project-bootstrap-and-audit`, with no prefix and no second
  copy. Its ledger said release 0.1.15, the hook and its `SessionStart` entry were in place,
  `syncClaudeAiPlugins` was false, and the standard said 0.46.0. That settles the 2026-10-16
  entry's untested half for cloud sessions. Whether claude.ai's automatic sync takes the next
  release is still to be seen, at the next release.

## 2026-10-16 — `human-factors`: where it applies, and research run R23

- **Said, by the owner,** answering the previous entry's three questions:
  - **Example:** a familiar, slower tool kept over a faster one.
  - **Where:** everywhere.
  - **Which agents:** only some, perhaps only a few. Most agents should be unbiased when they
    gather information, unless what they gather isn't objective fact.
- **Changed:**
  - `ROADMAP.md`: `human-factors` is loaded only by the few agents that design or change what
    people do, and never bends a factual finding. Its description will say so when it's built,
    so it doesn't load for research or fact-finding.
  - `research/prompts/R23-human-factors.md`, research run R23, priority 2, starts from the
    owner's example, asks the literature for the rest rather than a list of guesses, and tests
    the limit: language models' measured sycophancy, biases carried into gathered information,
    and where a person's preferences rightly count. Fatigue and shift design stay in R19.

## 2026-10-16 — `human-factors`: the skill `human-factor-audit` was meant to be

- **Said, by the owner:** `human-factor-audit` was meant to be much more than an audit of
  schedules and optimizers. It was to hold human notions, habits and mindsets that are common
  to people, that may look odd or wasteful to someone else, and that serve a purpose.
- **Changed, in `ROADMAP.md`:** the plan had `human-factor-audit` become
  `optimization-and-scheduling`, which kept only the schedules. A new planned skill,
  `human-factors`, takes the wider scope: what each such habit is for, how to spot one before a
  design, an automation or an optimization removes it, and how to design with it.
  `optimization-and-scheduling` keeps the human factors in plans and pairs with it. The name
  differs from the old one because the old one names only an audit, as step 12 of
  `docs/authoring-a-skill.md` allows.
- **Next:** research run R23, written once the owner has given the examples they had in mind,
  so the prompt asks about those first. R19's question 7 covers fatigue and shift design only.
- **Supersedes:** the previous entry's successor for `human-factor-audit`, which is
  `human-factors`. Keeping the old copy until then stays the recommendation, with more reason.

## 2026-10-16 — In a member's own settings, an uploaded skill is deleted, not turned off

- **Found, by the owner:** their claude.ai account belongs to an organization, on which they
  are also an Owner. In their own settings, **Customize > Skills**, it offers only removal for
  an uploaded skill, with no switch to turn it off. The Help Center's skills article, read on 2026-10-16,
  describes a switch beside each skill and deletion from the "..." menu, so the account and the
  article differ, and what the account shows is what stands.
- **Found, in the plugins page, read on 2026-10-16:** a plugin is turned off with its
  **Disable plugin** toggle and removed with **Remove** from its menu. A marketplace is added
  under **Customize > Plugins**, **Add > Add marketplace**, with **Check for updates** and, for
  one added from github.com, **Sync automatically**. A marketplace's plugins are then added from
  **Discover** with **Add**.
- **Found, in the plugins admin page, read on 2026-10-16:** an Owner manages the
  organization's plugins and skills under **Organization settings > Plugins & skills**, whose
  **Policy** tab holds **User-created skills**. With it off, members can't upload skills or add
  their own marketplace. Syncing a marketplace for the whole organization needs a private or
  internal repository, as the 2026-09-23 entry found, so this public one stays a member's own
  marketplace. Nothing here is set at the organization's level: that would reach every member.
- **Changed:** every step that turned an old claude.ai skill off now deletes it.
  `docs/authoring-a-skill.md` step 12 has the session say, for each skill that depends on an old
  copy, whether it would break or only names it, and the owner chooses which to delete. The
  previous entry's "turns off" for dependents is superseded by this.
- **For the owner's current step:** `human-factor-audit` only names `skill-orchestrator` and
  `markdown-standards` as companions, and one of its triggers can no longer fire. Deleting it
  would lose the source its rebuild, `optimization-and-scheduling`, is written from, so keeping
  it until then is the recommendation; the choice is the owner's.

## 2026-10-16 — Skills reach cloud sessions from the release, and release 0.1.15

- **Asked:** after release 0.1.14, the owner asked that getting the skills into sessions be
  made automatic. Uploading by hand is no trouble to them, so this was wanted only if it can
  be done, and with one condition: the owner removes the old skills, and anything that depends
  on them, first.
- **Found, by tests on 2026-10-16, with Claude Code 2.1.301 in this cloud environment:**
  - A skill that a `SessionStart` hook writes into `~/.claude/skills` loads in that same
    session. A headless session started in a scratch folder listed it and read it.
  - The same, with the hook in user settings, as `cloud-setup.sh` writes it: a fresh headless
    session ran it, restored a skill deleted to prove the hook ran, and listed all three skills
    by their plain names.
  - The claude.ai uploads of `git-workflows` and `project-bootstrap-and-audit` then loaded as
    well, as `anthropic-skills:git-workflows` and `anthropic-skills:project-bootstrap-and-audit`.
    Two copies of a skill is what the owner's condition prevents.
  - `skillOverrides` keys match the listed name: `"git-workflows": "off"` hid the installed
    copy, and the synced one came back under its prefix. That lasts only while the uploads do.
  - The tests restored this container's settings and removed what they installed.
- **Found, in the docs, read on 2026-10-16:**
  - A cloud session still doesn't install the plugins a repository turns on under
    `enabledPlugins`. The plugin-loading page names Cowork and terminal sessions for plugins
    synced from claude.ai, not cloud sessions.
  - A setup script runs before Claude Code starts, and its result is cached for about seven
    days, so an install there alone would lag the releases. The hook runs at every session start.
  - claude.ai updates a plugin from a personal marketplace when Sync automatically is on. Its
    docs don't say what counts as a change; each release here changes the version.
  - No public interface uploads a skill to a claude.ai account.
- **Chosen:** this supersedes how skills reach cloud sessions in item 35 of the 2026-10-13
  entry *The owner's answers to questions 19 to 35*, and the 2026-09-23 entry *The plugin reaches the account, not cloud sessions*:
  - **Cloud sessions:** each release carries `skills.zip` and `cloud-setup.sh`. The owner adds
    the setup lines to the environment once. The hook downloads the latest release's
    `skills.zip`, checks its manifest and every path in it, installs the skills into
    `~/.claude/skills`, and keeps a ledger, so it replaces and removes only what it installed.
    A failed download keeps what's there and never stops a session. It names any claude.ai copy
    still loading beside a skill, for the session to report. The setup lines also set
    `syncClaudeAiPlugins` to false, so a plugin copy can't load beside the hook's copy.
  - **claude.ai chat:** the two plugins from this repository's marketplace, with Sync
    automatically on, instead of uploaded ZIP files.
  - **The ZIP files stay on each release** as the fallback, uploaded by hand.

  *Considered:* installing the plugins from the setup script, cached for up to a week, and so
  up to a week behind a release; and a hook in each consuming repository, which would need a
  change in each.
  *Risk:* the hook runs nothing it downloads. It installs skills, whose scripts run only when a
  session runs them, as with any install, from a tag that the tag ruleset stops anyone
  moving. A bad release reaches every
  new session at once, which the withdrawal runbook in the README now covers.
- **Chosen:** removing old copies comes first, as the owner asked, and stays the order:
  `docs/authoring-a-skill.md` step 12 has the session name the old copy and what depends on
  it before a rebuild's release, which waits for the owner's word.
- **Changed:**
  - `house-style` is off in this repository's `skillOverrides`. The new `own-copies` rule
    fails these settings if any skill under `skills/` isn't off. It found `house-style` missing
    on its first run.
  - `bom.py`'s row for claude.ai says the account takes the plugins.
- **Release 0.1.15:** this pull request's merge, so that `cloud-setup.sh` and `skills.zip`
  exist on a release for the setup lines to fetch.

## 2026-10-15 — Standard v0.46.0: acceptance runs between rounds, and release 0.1.14

- **Asked:** the owner asked whether the acceptance test of two repositories in a review loop
  should run between rounds, on the released pair, with its result opening the next round, and
  who should start. They agreed with the recommendation, and asked that an audit of both
  repositories give it to both next time.
- **Changed, in the standard, as F149 and a change of its own:** *Two repositories* gains
  *A person's acceptance run goes between rounds, on the released pair, and opens the next
  round*. One side files every result and opens every round; the other reads the result there
  by its citation. A severe failure gets a fix release and a repeat run before any round. An
  audit that finds a pair in a review loop without this order proposes it to both, in the same
  words.
- **Why:** a run inside a round tests a pair a fix may already have replaced, and holds both
  sides until the person is free. The paragraph beside it already says a round approves a pair
  already released.
- **Not done:** no parity run, since the change adds one proposal and moves no rating.
- **Release 0.1.14:** this pull request's merge, so the owner's first upload of the three
  skills to claude.ai carries v0.46.0. Both catalog entries say 0.1.14.

## 2026-10-15 — Standard v0.45.0: the skill exclusion list

- **Asked:** the owner approved an exclusion list kept here and applied by the bootstrap skill
  (the previous entry, answer 2), then said: "do what you can".
- **Changed, in the standard, as F148 and a change of its own:** dimension 4's *Skills the
  owner keeps out of repository sessions*. A run proposes each entry of the standards
  repository's exclusion list that a repository's `.claude/settings.json` lacks, as
  `skillOverrides`, at Phase 6, and keeps the entries the repository already sets. It carries
  no rating. The enforced-layer template points to it, and *Facts with an expiry date* records
  the test from the previous entry.
- **The list:** `skills/project-bootstrap-and-audit/assets/skill-overrides.json`, 16 entries,
  each with its reason. Turned off: 8 of Anthropic's skills for chat (`canvas-design` among
  them, until the owner decides), `skill-creator` outside this repository,
  `procedure-generator`, and the owner's four retired skills. `docs` and `google-workspace` list
  their names only, since their connectors call them by name. Nothing this repository ships is
  on it, and the new `exclusions` rule fails a list that names one.
- **This repository applies it:** the `exclusions` rule fails `.claude/settings.json` when it
  lacks any entry, and lets this repository set its own value, as it does to keep
  `skill-creator` on.
- **Not done:** no parity run, since the change adds one proposal to dimension 4 and moves no
  rating. 13 tests cover the rule; `.test-baseline` is 382.
- **Release 0.1.13:** this pull request's merge, with standard v0.45.0, the exclusion list, the
  description cap and the shorter descriptions merged since 0.1.12, so the owner's uploads to
  claude.ai carry them. Both catalog entries say 0.1.13.

## 2026-10-15 — Room for 100 skills, on both surfaces, and an exclusion list for Claude Code

- **Asked:** the owner asked to plan for 75 to 100 skills, to make them work in Claude Code and
  on claude.ai even where that takes extra effort, to replace every older skill of theirs, and to
  keep a file listing the claude.ai skills Claude Code shouldn't load, applied by the bootstrap
  skill. On the seven questions that followed they answered, verbatim: "3. do all the word files
  and pdf, skill-creator maybe is only needed for this repo, unless you build a better one, but
  it should be kept as something refernce in case something changes in the future. convas
  design i am not sure. 5, fair, we can either make this repo private, but it was too
  restrictive, or make a private compananion repo […]. 6. yes, true, you would need to give me a
  prompt to run and test will on .ai to test in that direction. 7. we would likely try to
  replace in place if we can? if not agreed. otherwise all recommended".
- **Supersedes** the previous entry's "work on claude.ai only where that costs nothing". The
  authoring guide now asks for claude.ai too, with the owner's tries there before a skill ships.
- **Measured, in Claude Code 2.1.301's own code, since its documentation gives only the 1%:**
  the skill listing is 1% of the context window at 4 characters a token, so 8,000 characters
  for a 200,000-token model and 40,000 for a million. Each skill costs its name and description
  plus five characters. Over budget, Claude Code's bundled skills keep their descriptions, and
  the rest keep theirs in order of use until the budget runs out; the others keep only their
  names. 49 synced skills hold 26,894 description characters today: 16 of them Anthropic's
  (8,183), 33 the owner's (18,711).
- **Tested here:** `skillOverrides` set to `"off"` hides a synced claude.ai skill. With it in
  `.claude/settings.local.json`, then in `.claude/settings.json`, calling the skill was refused
  with "disabled for model invocation in skillOverrides settings". The documentation says
  plugin skills are exempt and says nothing of synced ones.
- **Decided:**
  - A description is at most 250 characters, with its main use first. The `listing` rule
    enforces it, and holds the whole listing to room for 100 skills at 240. The budget is raised
    only if that runs short (1).
  - The exclusion list is a file in this repository, and the bootstrap skill writes it into each
    repository's settings as `skillOverrides` (2). Its bootstrap step changes the standard, so
    it's proposed on its own. This repository already sets it for the retired skills and the
    synced copies of its own, which `CLAUDE.md` names.
  - Anthropic's `docx`, `xlsx`, `pptx` and `pdf` stay on. `skill-creator` is kept as a reference,
    on in this repository only, unless `skill-builder` replaces it. `canvas-design` is undecided,
    and off in Claude Code meanwhile (3).
  - `procedure-generator` stays on claude.ai and is off in Claude Code (4).
  - Company material, such as the company theme and template, goes in a private companion
    repository, which the owner creates. This repository stays public (5).
  - For each rebuilt skill, the session gives the owner two or three requests to try on
    claude.ai, each with what a pass looks like (6).
  - A rebuilt skill keeps its old skill's name where the name still fits its scope, so it can
    replace the old copy in place. That renames 18 planned skills in `ROADMAP.md`, such as
    `python` to `python-coding`, and `c`, `cpp`, `java` and `kotlin` to match. Four keep a new
    name, since the old one would misstate the scope (7).
  - `markdown-standards`, `skill-orchestrator`, `skill-stress-tester` and `code-planner` retire
    (7).

## 2026-10-15 — Claude Code first, and a skeleton for every new skill

- **Asked:** the owner asked whether the rebuilt skills would suit claude.ai, where the old ones
  were used, and then said: "It's mostly for Claude code to use. If it works for Claude.ai with
  minimal effort as a byproduct, excellent even better, let's improve the skills. But this was
  always secondary."
- **Decided:** skills are built for Claude Code. They work on claude.ai only where that costs
  nothing: spec fields only, which `skillcheck` already enforces because claude.ai rejects any
  other, and a description that stands on its own. `docs/authoring-a-skill.md` says so in place
  of its old pointer to decision H2 (a).
- **Changed, the first of the porting plan's shared tools:** `skillcheck --new <name>` writes a
  skill's `SKILL.md`, `why.md`, `facts.md`, `audit.md`, `mistakes.md`, `sources.md` and its
  trigger evaluations, in the authoring guide's shape. Each part still to be written is marked
  `TODO(new-skill)`, and a new rule, `placeholder`, fails any skill that still holds one, with
  the count and the first line. It refuses a bad name and never overwrites a skill or a trigger
  file that exists.
- **Tested:** 14 tests, including one that fills every placeholder in a fresh skeleton and finds
  it passes every rule, so the skeleton itself can't drift from the checks. `.test-baseline`
  is 365.

## 2026-10-15 — Release 0.1.12, after 0.1.11's files were refused

- **What happened:** the Release workflow tagged `v0.1.11` on `5ca99d0`, then its files step
  refused: `bom.json` and `docs/dependencies.md` counted 26 Python files, not 28. The session
  regenerated the map while the evidence verifier and its tests were still untracked, and the
  map counts tracked files. Pull request CI doesn't compare the map, so only the release caught
  it. No release page was published.
- **Changed:** the map is regenerated, and the same content ships as 0.1.12. The `v0.1.11` tag
  stays where it is, with no release, since the tag ruleset blocks deleting and moving tags, as
  it should.
- **Lesson, for this repository's own checks:** a check that only the release runs finds a
  mistake after the tag. Whether pull request CI should compare the map too is the owner's
  call, since a Dependabot pull request would then fail until a session regenerates it, which
  decision 27 already asks for before merging.

## 2026-10-15 — An evidence verifier in the standard's skill, and release 0.1.11

- **Asked:** the owner approved C1 of the round review on 2026-10-15: ship the verifier this
  repository's session used during the round, generic and tested.
- **Changed:** `skills/project-bootstrap-and-audit/scripts/verify_evidence.py`, Python 3.11 or
  later and nothing else, checks an evidence branch and its manifest in a local copy:
  - an orphan root, each later commit's one parent, no tag reaching the branch, and no history
    shared with the default branch;
  - with `--identity` and `--instant`, the move commit's pinned author, committer and dates;
  - the manifest's header, order and one row per path;
  - each row's file in its evidence commit, by size and SHA-256, the same blob as in its source
    commit, and no different file at that path on the default branch.
  
  It exits 0 when every check passes, 1 when any fails, and 2 when it couldn't check. Rulesets
  and CI are GitHub's to report, and it doesn't read them. `SKILL.md` links it.
- **Rebuilt, not copied:** the session's own script read GitHub's API and named the repositories
  it checked. This one reads only Git, so it works in any local copy, and its tests build their
  repositories. Building it found a defect the session's script never met: a branch wrongly
  rooted on the default branch walks into that branch's history, whose root also has no parent.
  It now lists only the branch's own commits.
- **Tested:** 22 tests in `tests/test_verify_evidence.py` plant each failure in a throwaway
  repository, including a non-ASCII path, and cover every line and branch of the script. Run on a
  live repository's real evidence branch, it passed all 16 checks over 1,032 rows.
- **Release 0.1.11:** this pull request's merge, with standard v0.44.0 and the `git-workflows`
  changes merged since 0.1.10. Both catalog entries say 0.1.11, and `.test-baseline` is 351.

## 2026-10-15 — Standard v0.44.0

- **Asked:** the owner approved nine additions, A1 to A9 in the review of a round between two
  live repositories, on 2026-10-15 ("do all recommendations"). They're F139 to F147 in
  `ROADMAP.md`, and a change of their own, as this repository requires of the standard.
- **Changed, in *Generated evidence*:** find the readers first (F139); build the move commit so
  anyone can rebuild it (F140); the removal's parent, CI's tree check and `-z` (F141);
  citations and checking every value they state (F142); filing order and redaction by a
  committed tool (F143); look at what makes evidence large (F145).
- **Corrected:** 0.42.0 told a tool to fetch evidence with `git fetch --depth 1 origin
  evidence`. Run in a full clone, that makes the whole clone shallow; both sides of the round
  hit or designed around it. The text now fetches into a temporary bare repository (F144).
- **Elsewhere:** a check proves every value its input states, beside the gate proofs (F146);
  and three sentences on the coordinator's messages, the reporting format and approvals given
  with the request, in *Cross-repository contracts* (F147).
- **Evidence:** each measurement is either re-checked on GitHub by this repository's session or
  is one side's report, named as such in the review. Neither repository is named.
- **Not changed:** no rating, no dimension, no wait. The dated facts are unchanged.

## 2026-10-15 — The owner's answers to questions 44 to 49, and what a round of review taught

- **Asked:** the owner was given every open question with a recommendation, and answered,
  verbatim: "do all recommendations. for 46, yes its my employers. for 47, ok. 12, can you
  just ignore them? 13, give me instructions for this. 15. done. 14, do recomended."
- **The porting plan for the owner's claude.ai skills** is approved, and recorded in
  `ROADMAP.md`, its only home:
  - examples CI can't run are checked as far as they parse, run once by the owner, and
    recorded with the version and date they were proven on (44);
  - Anthropic's `brand-guidelines` and `theme-factory` are off on the account: neither loads in
    sessions any more (45);
  - `my-theme`'s palette is the owner's employer's, so it stays on the account and nothing of it
    is published here (46);
  - PowerPoint and PDF are left to Anthropic's skills unless a repository needs to generate them
    (47);
  - old copies with known dangerous examples stay on until their successors ship (48);
  - work starts now: the shared tools here, and research wave 1 (R15, R09, R11, R10) with R21 by
    the owner (49).
- **Three retired synced skills** still load in sessions, since only the owner can turn them off
  on claude.ai. `CLAUDE.md` now names them, so sessions here don't use them (12).
- **A round of review between two live repositories,** which moved each one's run evidence to an
  `evidence` branch under standard v0.43.0's rule, closed on 2026-10-15. Both sides wrote a
  round summary and per-lap diagnostics for this repository, and the review of them is taken in
  three ways:
  - **`git-workflows`:**
    - read paths from Git with `-z`, since Git quotes non-ASCII names (a check reported 29
      present files missing);
    - push only after reading a green result, never in the command that runs the tests;
    - run every test that names an edited file;
    - pin and cache what CI builds from source (one job: 19.5 of 21 minutes);
    - timing tests assert on growth, and a slow test's timeout headroom is recorded;
    - a check is proven against every value its input states;
    - a merged branch's commits aren't pushed again;
    - the job-log endpoint's redirect.
    
    One more GitHub fact, that a job can't be re-run while its workflow run is still going, was
    observed once and has no GitHub source yet, so it isn't in the skill.
  - **`ROADMAP.md`:** lesson L30 for `review-loops`, on the reporting format, approvals given
    with the request, and steps run side by side.
  - **The standard:** nine additions on moving, filing and citing evidence, and on running a
    review loop, approved by the owner, go in as v0.44.0, a change of its own.
- **Measured, re-checked on GitHub:** checkouts fell from 479 to 73 MB and from 130 to 16 MB;
  full clones kept their size, since history keeps the files. Both evidence commits had the IDs
  their laps named before anything was pushed, and each side rebuilt the other's by plain Git.

## 2026-10-13 — CI runs once per pull request

- **Asked:** the owner asked whether running CI on a branch and again on `main` after the merge
  is redundant, and approved the fix on 2026-10-13.
- **Found:** `ci.yml` and `prose.yml` had a bare `push:` trigger, so each push to a branch with
  an open pull request ran both workflows twice: commit `793baa3` has a `push` run and a
  `pull_request` run of each. The two other repositories the owner keeps already limit `push`
  to their default branch.
- **Changed:** both workflows run `push` on `main` only. The pull request run still tests each
  branch merged with `main`, and `main`'s own run stays, because it tests the merge commit
  itself and the release workflow reads that commit's checks.
- **The house-style skill's copy follows:** a test holds this repository's `prose.yml` byte for
  byte to the one the skill ships, so the shipped workflow narrows `push` too, and its setup page
  says to name another default branch in place of `main`.
- **Costs:** a branch pushed with no pull request gets no run until one is opened. The standard
  already gives this trade-off and calls the narrowing optional for a fast suite; the owner
  chose fewer runs.

## 2026-10-13 — Standard v0.43.0, and release 0.1.10

- **Asked:** the owner approved F115 to F118 and F120 to F137 on 2026-10-13, with F138 from
  their answer to question 23. They're applied as v0.43.0, a change of its own, following a
  read-only plan that placed each one and named five that needed a reading:
  - F133 asks about an unfilled placeholder at once, and carries it to the Phase 3 wait, so
    the standard still has two waits;
  - F134 lets an owner's hold on pushing win over a stop hook, and over Phase 7's push and
    dimension 10's handoff, with the unpushed commits carried in the report;
  - F131 sends a false premise to Phase 6's first list as a question with a default, so a
    decline is still never re-proposed;
  - F129 replaces 0.41.0's generate-or-test paragraph with delete-first, and the standard's
    own "Eight things" count, which F115 made wrong, is gone;
  - F117 puts a CI job stuck at its locked install in dimension 2 as `DRIFT`.
- **Dated facts:** three new rows and one replaced, each quote checked at its source on
  2026-10-13: the checkout's `persist-credentials`, `uv run` locking and syncing, Claude Code
  hooks failing open unless they exit 2 or set `onFailure`, and lockfiles ranked above SHA
  pins.
- **Reviewed cold:** a fresh reviewer found thirteen defects in the first text, each checked
  against the text before it was applied. The worst was this change's own shell recipe, whose
  here-string threw away a failing producer's status, the fail-open shape F121 warns about.
  Others: gates after a failed locked install would have rewritten `uv.lock` in the working
  tree; an unfilled placeholder worked as a third wait; and the size rule had no template. The
  starter CI's new size step failed open in its first draft too, and was tested in four cases
  before it went in.
- **This repository meets the size rule:** `skillcheck` holds `AGENTS.md` and `CLAUDE.md` to
  300 lines and 32 KiB, and `AGENTS.md` now says its limits are enforced.
- **Parity runs:** one fresh session for each sample, on the first text, the skill as committed
  at `4363098`, whose standard's SHA-256 starts `ccdb33d4`. The review's fixes came after:
  - **Audit:** twenty of twenty checks, and both manual checks hold. One value moved: dimension
    4 to `BLOCKER`, the v0.37.0 rule every audit run has moved since. It proposed
    `persist-credentials: false`, weighed a size check and proposed none at T1, and named the
    gates that ran on a fresh resolution.
  - **Re-check:** all four planted checks pass, and the three manual checks hold. Dimension 6
    moved from `DRIFT` to `GAP`, which F117 meant: the stale lock is dimension 2's `DRIFT`. The
    grader failed "does not propose Dependabot", but the amendment's change reads "no update
    tool proposed (Dependabot declined)", so the reading wins, as the testing guide says. The
    run checked a decline's premise against the history, and held Dependabot back from the SHA
    pin.
  - **Greenfield:** seven of seven checks, no difference from the baseline, and both manual
    checks hold.
  - **Slips:** the audit and re-check runs fetched from the sample's bare remote, outside
    their directories, and the session refused their `rm -rf` of scratch files. The prompt's
    known limits cover the first.
- **Left for the rebuild:** the standard still restates a few counts and limits by hand, such
  as "Four things cannot be detected". F129 applies to them, and the rebuild's pieces move that
  text anyway.
- **Release 0.1.10:** this pull request's merge, released by the Release workflow once CI
  passes on the merge commit. Both catalog entries say 0.1.10.

## 2026-10-13 — The owner's answers to questions 36 to 43

- **Asked:** the owner was given eight more questions, six with a recommendation and two with
  options only, and answered, verbatim: "Do 5 questions, the fingerprint, warn, yes offer each
  time and only install with a yes, keep bumping, run the report.not now. File all 18, bit not
  right now, I will say."
- **The single start command,** from R22, as `ROADMAP.md` records beside each choice:
  - a run always asks five questions: where it runs, production, dependents, work or
    personal, and how long it must live (36);
  - the reference file's SHA-256 sits in `SKILL.md` and is checked at the start, rather than
    the skill fetching the reference on every run (37);
  - where `main` holds a newer standard than the copy running, the run warns and goes on (38);
  - after each approved run, the run offers a project skill whose hook blocks writes until
    approval, and installs it only on the owner's yes (39);
  - the catalog's version is bumped at every release (40);
  - a run keeps its answers about a repository in its run report's Phase 3 block (41).
- **Not now (42):** no work repositories are named, and `procedure-generator` stays as it is
  on the owner's account until `word-documents` is built.
- **The fork's upstream reports (43):** all 18 are to be filed, by the owner, but not until
  the owner says so. Nothing is posted until then.

## 2026-10-13 — The owner's answers to questions 19 to 35, and F115 to F137

- **Asked:** the owner was given each open question with a recommendation, and answered "I
  agree with you recommendations". Events had already settled 21 (F119, in v0.42.0), 22 and 23
  (history: only one email address was rewritten), 24 (releases went ahead without R21), 25
  (no wait for the rebuild), and the first two parts of 30.
- **Approved for the standard, as v0.43.0, a change of its own:** F115 to F118, F120 to F137,
  and F138, which replaces home-folder paths with `~` in a log before it's committed as
  evidence (23, from now on).
- **This repository:**
  - `house-style` follows the commit grammar a repository records, rather than requiring
    "area: summary" everywhere (26). A live repository that records lowercase Conventional
    Commits keeps them.
  - A session regenerates the dependency map in each Dependabot pull request before merging
    it (27).
- **The roll-out:**
  - Scope: the owner's six repositories, and no work repository without the employer's
    agreement (28).
  - Order: this repository; then the two quiet private ones; then the two live ones, the fork
    once its CI is green; then the empty organization repository is archived (29).
  - The fork gives each release an annotated tag, from its first (30).
  - The live repository marks only betas as prerelease, from its next release (31).
  - The owner starts one re-check session per repository at each release, with that release's
    kickstart file. Scheduling waits until a round of re-checks finds nothing to fix (32).
- **How skills work together:**
  - A checked pairing map replaces the orchestrator: each skill lists the skills it pairs with,
    `skillcheck` checks the map, and each repository's `AGENTS.md` names its route. It's built
    with the first language skill (33).
  - A `word-documents` skill here takes a template and a defaults file. The company template
    and defaults stay out of this public repository (34).
  - Skills reach cloud sessions by upload to claude.ai, until cloud sessions load plugins (35).

## 2026-10-12 — A live history rewrite, taken into `git-workflows`, and release 0.1.9

- **Asked:** the owner sent a live repository's session's feedback on removing one email
  address from that repository's history, which the owner ran on 2026-10-12. The feedback is
  taken in as data. Its claims about the rewrite were checked on GitHub from a fresh copy:
  - the address is in none of the 1,825 commits on the repository's branches and tags;
  - the commit map is committed;
  - both rulesets are back on.
- **`git-workflows` gains *Personal information in history*,** in `references/security.md`:
  - count every copy before choosing the scope;
  - rewrite only the metadata with `--mailmap`, `--sensitive-data-removal` and
    `--preserve-commit-hashes`;
  - commit an old-to-new map that every reader of commit IDs looks up first;
  - rehearse on a mirror with the full test suite;
  - hand the owner one checked script;
  - warn of lost signatures, a red first CI run, rulesets to switch off, pull request refs
    only GitHub Support can purge, and shipped apps pinned to commits;
  - refresh every clone afterward.

  Rule 3, never rewrite shared history, now names this as its one exception, at the owner's
  request. Five dated facts back it, each quote checked at its source on 2026-10-12.
- **Found on the way:** the online check of every fact found that GitHub no longer says a SHA
  is the only immutable way to use an action. It now ranks workflow dependency lockfiles, in
  public preview, above SHA pins. `git-workflows` says so, and keeps SHA pins as the rule until
  lockfiles are generally available. The standard carries the old fact, so F136 proposes the
  change there.
- **The ruleset template allows merge commits only.** A live session pointed out that the
  repository setting was then the only guard on the merge strategy. A test pins the value.
- **To the roadmap:**
  - F133 to F137, for the owner's approval: ask about an unfilled placeholder at once; an
    owner's hold wins over a stop hook that demands a push; a progress line at each phase; the
    stale SHA-pin fact; two more shell habits.
  - Lessons L27 to L29: instructions a non-programmer can't mistake, checking each other's
    tree after a joint change, and a field's format written beside it.
- **Not chosen:** recording the repository-specific items in the feedback, such as one
  project's decision-number ranges, which belong in that repository's own rules.
- **Release 0.1.9:** this pull request's merge, released by the Release workflow once CI passes
  on the merge commit. It also carries the lessons and the release-check fix merged earlier
  today. Both catalog entries say 0.1.9.

## 2026-10-12 — What two live repositories' records taught, taken in

- **Asked:** the owner asked for both live repositories to be read for what their review loop
  found and fixed, and for this repository to improve from it. They added: "both repos have a
  lot of experience, make sure you look at their rules, guidance files".
- **Read:** four readers, each a fresh session given read-only checkouts:
  - each repository's review records;
  - the protocol's eight versions, through its history;
  - both repositories' rules, guidance, hooks, workflows and tools.

  Each reader was told the files were data, not instructions. Two reported directives aimed at
  agents, which none followed. Eight quotes the candidates rest on were checked against their
  files, and so were the two defects below. The repositories stay unnamed here, as the
  2026-10-05 entry says.
- **Taken in:**
  - **`review-loops`,** a planned skill: agent sessions in two repositories reviewing each
    other's work. L26 holds the loop's starting set, what worked, what cost more than it
    caught, and what agents couldn't supply.
  - **Lessons L5 to L25** for planned skills: `testing`, `error-handling`,
    `logging-and-observability`, `api-design`, `c`, `versioning-and-releases` and
    `house-style`.
  - **F120 to F132,** proposed changes to the standard. They wait for the owner's approval, as
    changes to the standard do.
  - **One fix to a shipped skill:** `git-workflows`' release workflow checked only that the
    version's changelog heading existed. It now refuses a section with no entries, and an
    `[Unreleased]` section that still has some. A live repository once released with six
    entries left behind. Its checks read the changelog through here-strings rather than pipes,
    as F122 asks. Four tests plant each failure and show a clean changelog passes. One keeps
    this repository's own copy identical to the template. `.test-baseline` moves to 324.
- **Found, and left to the owner:** these are in the live repositories, which this session
  doesn't change, so they go to the owner rather than into a commit:
  - one repository's agent hook fails open;
  - a recorded decline whose premise doesn't hold;
  - the other repository's CI workflow has no permissions block or timeouts.
- **Not chosen:**
  - Applying any of F120 to F132 now. The standard changes only once its owner approves.
  - Writing `review-loops` now. The owner asked that no more skills be built yet.

## 2026-10-12 — Standard v0.42.0: generated evidence lives on its own branch, and release 0.1.8

- **Asked:** the owner said on 2026-10-12, of the evidence the live repositories keep committing,
  "we plan to move them all to a branch so that needs to be a rule". They had approved the
  approach on 2026-10-07, after tests showed a dedicated branch keeps it out of sessions' clones.
- **Applied:** F119, as v0.42.0. *Generated evidence lives on its own branch:*
  - **What it is:** the logs, captures and reports a project's runs keep adding, and that nothing
    builds or tests from. Fixtures and correspondence, such as a review loop's laps, stay where
    they are.
  - **Where it goes:** an orphan `evidence` branch, only appended to and never tagged, with an
    append-only manifest of each file's hash and commit on the default branch.
  - **How sessions avoid it:** a committed SessionStart hook adds a negative refspec. In a
    session holding several repositories, which runs no hooks, the context file tells the
    session to do it itself.
  - **What CI checks, from T2:** that no tag is reachable from the branch, and the hash of each
    new manifest row.
  - **Ratings:** dimension 3 rates such evidence on the default branch `GAP` at any tier, under
    10 MB in all aside. Dimensions 4 and 6 rate the missing exclusion and check, and the settings
    table gains an evidence-branch ruleset.
- **Why:** one live repository held 320 MB of such evidence on its default branch, 151 MB from
  one round of review, and every session's clone carried it.
- **Checked against Git:**
  - Negative refspecs are in Git 2.29.0's release notes and the `git fetch` page.
  - Tested in scratch repositories with Git 2.43 on 2026-10-07 and 2026-10-12. The exclusion
    kept a 3 MB branch out of a session-shaped clone, until a tag pointed into the branch: a
    plain fetch then took it, as a plain clone did.
  - The tag check fetched 24 KB, and flagged only the planted tag.
  - Both results are dated facts in the standard.
- **Reviewed cold, twice:**
  - The first review found three blocking defects: the rule would have moved a review loop's
    laps, which the standard keeps immutable; a survey never reached its rating; and a session
    holding several repositories runs no hooks. It also found seven smaller ones.
  - A second review of the fixes found two more: dimensions 4 and 6 didn't state their ratings,
    and the first tag check, every tag on the default or a release branch, would have failed
    repositories set up correctly.
  - Each finding was checked against the text before it was applied.
- **Parity run:** the audit sample, in a fresh session, on the rule's first text. The fixes
  touch only the new rule, and the sample has no evidence.
  - Twenty of twenty checks pass, and both manual checks hold.
  - One value moved: dimension 4 to `BLOCKER`, the v0.37.0 rule every audit run has moved since.
  - The run listed "an evidence branch: the project generates no evidence" among what it didn't
    propose.
  - Its slips: it fetched once from the sample's remote outside its directories, and pip wrote
    a cache under the system temporary folder. The prompt's known limits cover both.
- **Not chosen:**
  - Git LFS: it moves files out of history, but a clone still fetches the current ones, and the
    plan's storage and bandwidth limits apply.
  - Release assets: they can't be cited at a commit, and immutable releases freeze them.
  - Rewriting history to remove what is already there: it changes every commit ID, and every
    citation of one, so it stays a decision of its own.
- **Release 0.1.8:** this pull request's merge, released by the Release workflow once CI passes on
  the merge commit. Both catalog entries say 0.1.8.

## 2026-10-05 — Standard v0.41.0, reviewed cold and in the house style, and release 0.1.7

- **Asked:** the owner's answer 6 approved F81 to F114, to be applied as v0.41.0 in groups, each
  reviewed cold, with parity runs. Answers 11 to 13 put the standard into the house style.
- **Applied:** seven groups, one commit each, mapped first to the sections they change:
  - tests that report more than they ran, F81 to F88 and F105, in dimension 5 and the starter
    CI file;
  - CI and the context file, F89, F90, F92 to F95, F97, F99, F103, F106 and F107;
  - releases and other repositories, F91, F94's handoff half, F98 and F100 to F102;
  - the run's own shell habits, F96;
  - two facts corrected, F104 and F108, each read again at its source on 2026-10-05;
  - what the parity runs of v0.40.0 found, F109 to F113;
  - the platform settings, F114, which move from the kickstart file into the standard's dated
    facts.
- **Reviewed cold:** three sessions that hadn't written the text each read one group's diff
  against the approval and the rest of the file. They found 39 defects, 11 of them blocking:
  - one condition given two statuses, or none, in seven rules;
  - two rules that contradicted dimensions 6 and 8: a SessionStart hook against "documented as
    session setup", and grouped security updates against "security PRs ungrouped";
  - incidents nobody had reported, added to F94, F96 and F98;
  - a reachability test that would fail every correct pull request;
  - a recorded binary read the wrong way: a bare `command -v ruff` found a global ruff 0.15.8
    in this session while the gate ran the project's 0.16.10;
  - page links, a plan check and two of support's observations lost in moves.

  Each was checked against the text, and against its source where it named one, before it was
  applied, as F96 now asks.
- **A fourth review** read those fixes and found ten more, three of them blocking: a SessionStart
  hook runs only in a session holding one repository, a client-side hook still read as a gate
  where dimension 6 says it isn't one, and a tier that couldn't be computed from an unknown
  answer. They were checked and applied the same way.
- **The house style:** a commit of its own. 28 headings take sentence case, with 113 citations
  of them, among them the marker the release code cuts the kickstart file at. 59 spellings
  become American, and 12 filler words go. A first pass missed 12 citations that a line break
  splits or that name a section in short. It also left the release test's check that the
  kickstart file drops the validation section looking for the old heading, so the check
  couldn't fail. Both were fixed before the pull request, and a cut planted in the wrong place
  now fails the test. Past entries in the version history keep their spelling and section
  names, as this record's do, and the prose check skips them.
- **Security updates stay ungrouped.** Release 0.1.5's kickstart file said to group them, for
  each repository and for new ones on the account, against dimension 8. The standard's text
  wins. The owner is asked to turn grouped security updates off where they turned it on.
- **Not chosen:**
  - applying each review's proposed wording as written. Where a proposal claimed more than this
    session could check, the text says only what was seen: support's report that no plugin was
    enabled is dated 2026-09-30 alone. Where one would have changed a rule beyond its finding,
    it was narrowed: dimension 6 installs by SessionStart hook only a hook sessions already
    rely on, and proposes none where no local clone exists;
  - bringing past entries into the style, which would rewrite what each version said when it
    shipped.
- **Parity runs:** one fresh session for each of the three samples, given the documented prompt
  and the skill as committed at `a685e3b`, whose standard's SHA-256 starts `b36028ad`. Each was
  graded with `python -m skillcheck.parity` and compared with the baseline:
  - **Audit:** twenty checks, with all thirteen planted problems found, and both manual checks
    hold. One value moved: dimension 4 to `BLOCKER`, the v0.37.0 rule, which every audit run
    since has moved. The new rules showed: it proposed a job timeout, recorded the unanswered
    question with its default, weighed a SessionStart hook and proposed none, and counted no
    action needing a local clone.
  - **Re-check:** thirteen checks, and all three manual checks hold: the Dependabot decline
    stays, as its trigger hasn't fired, branch protection stays `N/A`, and the sample is
    unchanged. One value moved: dimension 6, from `DRIFT` to `GAP`. Both runs found the same
    stale lock; this one rated it in dimension 2 and the job's missing timeout in dimension 6.
    The key accepts either, and F117 asks the text to settle it.
  - **Greenfield:** seven checks, and no difference from the baseline. Both manual checks hold.
  - **What they found:** the re-check run proposed three changes to the standard. Two were gaps
    this version's own fixes opened, so they're closed here, as the run itself had handled them:
    a setting never re-proposes a recorded decline, and a re-check asks a question its record
    predates. The third waits as F116. Those two were not re-run: the text now says what the run
    did.
  - **The runs' own slips,** each disclosed in its report: the greenfield run's first, plain
    `git status` rewrote the sample's index, with no content changed, and the other two listed
    file names beside their directories or wrote temporary files outside them. The re-check run
    fetched from the sample's remote through git and used the network, the prompt's known limit.
- **Checked:** `uv run pytest` passes 320 tests, with 100% line and branch coverage. ruff,
  `skillcheck` with 0 findings, Vale on all 69 tracked Markdown files, and Claude Code 2.1.288's
  validator all pass. The kickstart file builds from the tree, and the release test fails on a
  cut planted in the wrong place.
- **Found on the way, for the owner:** four candidates, F115 to F118, wait in the roadmap for
  approval: the starter CI checkout's credentials, gates after a failed locked install, the
  dimension a blocked CI job belongs to, and the README template's sections (question 18).
  Dependabot's pull request 20 left the dependency map stale on main, since pull request CI
  doesn't check it. This pull request refreshes it, and the roadmap asks the owner how to keep
  it fresh.
- **Release 0.1.7:** this pull request's merge, released by the Release workflow once CI passes
  on the merge commit. Both catalog entries say 0.1.7.

## 2026-10-05 — `house-style`: one style for prose, checked by Vale, and release 0.1.6

- **Asked:** the owner asked for every repository and file to share one format and language,
  recognizable as theirs because it's plain, free of filler, and correct. Their answers 11 to
  13 chose American spelling, a Vale check whose style each release carries, and the draft
  rules as written.
- **Chosen:**
  - **A skill, `house-style`,** with thirteen rules: seven on voice and six on format. It ships
    in the `engineering` plugin, whose Apache-2.0 license it shares. The `standards` plugin is
    CC0-1.0. `.claude/settings.json` already turns off both plugins' copies here.
  - **Vale checks three of the rules:** the six filler words, sentence-case headings and
    American spelling. No linter can tell whether the answer comes first or a fact was
    checked, so the other ten are for review.
  - **Each release carries `HouseStyle.zip`,** and other repositories name the latest by URL. A
    change to the style reaches each one at its next CI run, and a new rule can fail a
    repository that passed the day before. Pinning a release was the alternative: no surprises,
    and a pin to move in every repository for each fix.
  - **This repository loads the style from its source,** so a changed rule meets this
    repository's text in the same pull request. The decision record, dated research, the
    parity fixtures and, until v0.41.0, the standard's references are left out. Tables of
    facts and sources skip their quotes.
  - **The roadmap:** `house-style` takes the `markdown` row, for Markdown that people read.
    Markdown for agents stays with `agent-context-files` and the standard. `documentation`
    narrows to docs sites, diagrams, and file size and splitting.
  - **README sections:** rule 10 uses the standard's README headings, Usage and Development.
    The standard's template also has Requirements and Configuration, which fit the order. It
    has no Operations or Security section, which the house style asks for. Adding them is for
    the standard's next version, as a proposal to the owner.
- **Built from:**
  - the owner's draft rules, approved as written;
  - Google's, Microsoft's and GOV.UK's style guides, for sentence case and the words to cut;
  - research R02's lead on Vale, checked at its source: v3.24.0, where R02 had v3.22.0;
  - the owner's claude.ai `markdown-standards` skill, as topics only. Its heading depth, list
    nesting and blank lines around blocks came in. Its XML tags for agents belong to
    `agent-context-files`, and its README template gave way to the standard's.
- **Sources and licenses:** short quotes only, each a dated fact in `references/facts.md`, and
  all 13 were found at their sources on 2026-10-05. Google's guide is CC BY 4.0, GOV.UK's is
  under the Open Government Licence v3.0, Microsoft's is under its terms of use, and Vale is
  MIT. With nothing copied beyond short quotes, no third-party notice is needed. The skill is
  Apache-2.0.
- **Whose work:** the rules are the owner's, written here. `markdown-standards` is an
  organization skill, and only generic topics came from it, under the organization's written
  permission recorded in the inception entry.
- **Reviewed** against `docs/authoring-a-skill.md`:
  - Items 1 to 4: see above. There's no company detail, and no example that needs a
    placeholder.
  - Item 5: no claude.ai paths and no destructive commands. Vale installs with `go install`
    from its module, which Go checks against its checksum database. Nothing is fetched and run.
  - Item 6: spec fields only, with a 780-character description in the third person.
  - Item 7: `SKILL.md` is a 94-line router. Its five references are one level deep, each with
    a title and a line on when to read it.
  - Item 8: the style and the CI job run. Vale v3.24.0 passes all 69 tracked Markdown files
    here, and the canary trips all three rules. `HouseStyle.zip`, built by the release code and
    served over HTTP to a scratch repository, installed with `vale sync`. It passed a clean
    file there, and failed a bad one on all three rules. actionlint and zizmor are clean.
  - Item 9: `tests/fixtures/skills/house-style.json` holds 23 requests, 10 of them near misses
    for neighboring skills.
  - Item 10: the skill is in the catalog, the roadmap and the README.
  - Item 11: the changelog has the entry, and `metadata.reviewed` is 2026-10-05.
  - Item 12: the claude.ai `markdown-standards` skill has another name, so an upload won't
    replace it. Turning it off is the owner's step once `house-style` is uploaded.
- **American spelling:** converted in a commit of its own. Quotes, names, file names, URLs,
  code and API values keep their own spelling: the Open Government Licence, the research result
  `2026-09-23-A-source-licences.md`, and GitHub's `cancelled` conclusion. `skillcheck`'s
  messages and the dependency map changed with it.
- **Also in this change:**
  - **Action pins:** each action is pinned to one commit across this repository's workflows and
    the ones its skills ship. Dependabot updates only `.github/workflows/`, so a test fails
    until a skill's copy follows, in the same pull request.
  - **Release files:** `release.py` packs each skill's Vale style as its own ZIP, and stops a
    release in which two files would share a name.
  - **The kickstart file** has a session write in the house style, and propose its check where
    a repository has none.
  - **The conflict-marker scan** covers `.vale/`, the new top-level directory, which holds the
    tracked vocabulary.
  - **Planted breakages:** a drifted pin, a canary missing a rule, a word swapped twice and a
    style not run on Markdown were each caught by the test meant for it.
- **Checked:** `uv run pytest` passes 320 tests, with 100% line and branch coverage, and
  `.test-baseline` moves from 293 to 320. ruff, `skillcheck` with 0 findings, Claude Code's
  validator, and `skillcheck --verify` with 105 quotes and 0 not confirmed all pass.
- **Release 0.1.6:** this pull request's merge, released by the Release workflow once CI passes
  on the merge commit. Both catalog entries say 0.1.6.

## 2026-10-05 — The owner's answers to questions 1 to 17

- **Answered:** the owner took every recommended option: "Do the recommended. And do the
  recommended yes." They're staying on GitHub Free.
- **Applied in this repository:**
  - **1 and 2:** release immutability on and the wiki off, which the owner had already set.
  - **4:** a session merges its own pull request once every check passes, for work the owner
    asked for. It merges Dependabot's once they've been tested together on `main`. Stated in
    `AGENTS.md`.
  - **5:** commit subjects read "area: summary". The `git-workflows` skill's commit-subject
    check runs on every pull request here, unchanged, and Dependabot's subjects carry a `deps:`
    prefix. Stated in `AGENTS.md`.
  - **7:** `v0.1.1` stays untagged.
  - **9:** the weekly freshness run stays. A session re-checks this repository against the
    standard at each release, as the README's release steps now say.
  - **15:** on GitHub Free, the owner's private repositories can have no ruleset or branch
    protection. CI still runs and reports there. The owner accepts this as a risk, to reopen
    when one of them ships something people rely on.
- **For the owner to set,** because this session's GitHub access refuses every settings write:
  - **3:** a pull request required on `main`;
  - **14:** a public `.github` repository holding a default `SECURITY.md`. The owner has its
    text;
  - **16:** merge commits as the only method in every repository;
  - **17:** archiving an empty placeholder repository;
  - the settings checklists for the account and each repository.

  The owner has the click paths for each, ordered so that nothing breaks before the change it
  depends on lands.
- **Approved, and applied in changes of their own:**
  - **6:** F81 to F114, as standard v0.41.0;
  - **11 to 13:** the house style, with American spelling, a Vale check, and the draft rules as
    written.
- **8:** the owner sets each other repository's settings. Then a session in each runs the
  kickstart file, through that repository's own process.
- **10:** the skills on claude.ai are for the owner only, not their organization.

## 2026-10-05 — The account's settings in the kickstart file, and release 0.1.5

- **Asked:** the owner sent screenshots of their account's Code security page, and asked for
  them to be checked, for anything else needed to go into the kickstart file, and for
  everything checkable to be checked.
- **Read:** the screenshots, GitHub's documentation, and the owner's repositories through the
  API, read-only and with the owner's leave. Nothing was changed in any of them. Four gaps
  turned up that the kickstart file didn't cover:
  - **Dependabot on self-hosted runners** was set to turn on for new repositories. With no
    runner labelled for it, Dependabot's jobs wait, and fail after 24 hours. The owner turned
    it off the same day, and the recent Dependabot runs in each repository had all passed.
  - **Commit addresses:** a personal address on commits stays public once they're published.
    The account's two email settings keep it off later ones.
  - **The plan:** on GitHub Free, a private repository can have no ruleset or branch
    protection, and the API says so in a 403.
  - **Two-factor authentication** wasn't in the list at all.
- **Chosen:**
  - The kickstart file's account settings become a table of nine, with the value for each and
    where it is.
  - A session reads the plan and the commit addresses itself. A personal address is named in
    the report only, never in a repository, and rewriting published history to remove it is
    never proposed. A session asks whether the email boxes are ticked, because a screenshot of
    the Emails page would show the addresses.
  - `git-workflows` gains four facts, and audit checks 29 and 30. Each fact's quote was found
    at its source on 2026-10-05.
- **Release 0.1.5:** this pull request's merge, released by the Release workflow once CI passes
  on the merge commit. Both catalog entries say 0.1.5, because `git-workflows` changed.

## 2026-10-05 — Repository settings in the kickstart file, two rulesets, and release 0.1.4

- **Asked:** the owner asked:
  - what they had missed in this repository's settings, with steps to check each;
  - what to do in their other repositories and across their account;
  - that all of it be part of the bootstrap file.
- **Read, through the API on 2026-10-05:**
  - As recommended: merge commits only, auto-merge, release immutability, secret scanning, push
    protection, Dependabot security updates, private vulnerability reporting and the
    `Release tags` ruleset.
  - Missing: `protect-main` has no pull request rule, and code scanning isn't set up.
  - Unread: this session's GitHub access can't read the Actions settings, so the owner checks
    those.
  - Not available: secret scanning's validity checks and generic patterns read as disabled.
    GitHub's documentation says neither exists outside an organisation on GitHub Team.

  The owner got the checklist as a file kept outside the repository.
- **Chosen:**
  - **The kickstart file's run instructions carry the settings checklist.** A session in any
    repository reads the settings it can, and asks for the rest at the Phase 3 wait. At the gate
    it lists each change as an action only the person can take. It changes no setting itself: a
    setting can't go on a branch for review, and the person keeps that control. The standard
    is unchanged, and F114 proposes moving the list into it.
  - **The `git-workflows` skill ships the two rulesets as JSON,** in the shape GitHub's own
    starter rulesets use, though none of their text. Each release attaches every ruleset a
    skill ships, because GitHub imports a ruleset from one file. The release-tag ruleset is
    this repository's own `Release tags` ruleset.
  - **Eight new facts in `git-workflows`.** `skillcheck --verify` found each quote at its source
    on 2026-10-05. Seven quote GitHub's documentation, or its starter rulesets' README.
    - The eighth is a practitioner's report: Semgrep found the SHA-pinning policy also fails an
      action that calls an unpinned one. It sits under practice in other projects. The advice
      built on it says to read each action's own `uses:` lines first, then watch the next runs.
  - **The SHA-pinning policy can be turned on here.** Each action this repository's workflows
    use is pinned to a full SHA and calls no other action, which reading each one's
    `action.yml` at its pinned commit showed. No documentation says whether GitHub's own
    Dependabot and CodeQL jobs pass the policy, so the owner watches the next run.
- **Release 0.1.4:** this pull request's merge, released by the Release workflow once CI passes
  on the merge commit. Both catalog entries say 0.1.4, because `git-workflows` changed. Nothing
  is breaking, so it's a patch release. It's the first release since release immutability was
  turned on, and the first under the `Release tags` ruleset, which leaves tag creation open.

## 2026-10-05 — Release 0.1.3

- **Asked:** the owner: "plan on release all as the next 0.1.3 release", then asked for GitHub
  to be tested by doing it.
- **Chosen:** this pull request's merge is release 0.1.3. It carries the dependency map,
  the release workflow that publishes the kickstart file, the skill packages and the map, and
  the `git-workflows` skill's fixed release example. Both catalog entries say 0.1.3, because
  the `git-workflows` skill changed and an installed copy updates only when the version does.
  Nothing is breaking, so it's a patch release.
- **Released by:** the Release workflow, run on this pull request's merge commit once CI passes
  there. It makes the annotated tag and publishes the release page with its files.

## 2026-10-05 — Releases publish their files, and the release job's defects are fixed

- **Asked:** the owner asked that what a release gives them be "the kickstart/bootstrap files",
  not only release notes and the plugin commands, and that everything since 0.1.2 be released
  as 0.1.3.
- **Found:** the Release workflow's first run, for `v0.1.1` on `cbe163f`, failed at the push:
  "refusing to allow a GitHub App to create or update workflow `.github/workflows/ci.yml`
  without `workflows` permission" (run 37258285607). GitHub's page on the workflow scope says
  why: "Workflow files can be committed without this scope if the same file (with both the
  same path and contents) exists on another branch in the same repository." No branch still has
  `cbe163f`'s `ci.yml`, and the job's token can't be given that permission. The run showed two
  more defects in the example. A failed attempt leaves a failing check on the commit, which the
  next attempt reads as a failed check. And a tag pushed by an attempt that then failed stops
  the next one.
- **Changed, in the `git-workflows` skill:** its example release job checks, before making
  anything, that a branch has each of the commit's workflow files as it is, and says what to do
  when none does. It leaves out the runs of its own jobs, named in `OWN_JOBS`, when it reads the
  commit's checks, and it carries on from a tag it would have made itself. The new fact
  `workflow-scope` holds the documentation's words, and `setup.md` says to tag before a later
  commit changes a workflow. Tests cover each change, and the skill's review date moves to
  2026-10-05.
- **Chosen, for this repository:**
  - The Release workflow keeps that job and adds two. `Release files` checks out the commit
    with no write access and runs `skillcheck --release-assets`. That refuses a catalog,
    changelog or dependency map that disagrees with the version, then builds `KICKSTART.md`, a
    ZIP of each skill and the page's notes. `Release page` publishes the page from the tag with
    those files attached, or updates it where an earlier attempt published it.
  - `KICKSTART.md` is the standard as one file, built the way the run files for the owner's
    live runs were, but naming no repository: it picks its job from what the repository holds.
    Its run instructions are in `src/skillcheck/kickstart.md`. GitHub serves the newest
    release's files at a fixed address, so one link always reaches the current kickstart file.
- **`v0.1.1` stays untagged.** The job can't make it while no branch has `cbe163f`'s workflow
  files, and the release it would mark has been superseded twice. Its changelog section and its
  merge commit remain its record.

## 2026-10-05 — A dependency map, kept in CycloneDX

- **Asked:** the owner asked for a full map of the projects, languages, versions, applications
  and dependencies this repository has or relies on, kept somewhere standard that sessions and
  other applications can read and use.
- **Chosen:** two files, which `skillcheck` builds from the files that decide them and nobody
  edits by hand:
  - `bom.json`, at the root, in CycloneDX 1.7. Research R05 found 1.7 current, and "the final
    version in the 1.x series". CycloneDX tools look for `bom.json` by name;
  - `docs/dependencies.md`, the same facts for people, with each package tree drawn.

  It reads every package at its exact version from `uv.lock` and `package-lock.json`, marking
  development-only ones as outside what ships. From the workflows it reads the pinned Actions,
  the versions the setup actions install, the tools `go install` builds and the runner labels.
  `.python-version` and `pyproject.toml` give Python and the build backend, the catalog and
  frontmatter give the plugins and skills, each skill's facts give the sources they cite, and
  `git ls-files` gives the languages. Two services that no file declares are stated in the code:
  the Go module proxy, which `go install` uses, and claude.ai, where the owner uploads the skills.
  The serial number comes from the content, so the same repository always builds the same file,
  and a check can compare the two byte for byte.
- **Checked:** the file validates against CycloneDX's official 1.7 JSON schema, with jsonschema
  4.25.1 in a throwaway environment, so the project gains no dependency. Four defects planted in
  copies were each caught. The tests cover every line and branch of the generator.
- **Not run on pull requests:** `skillcheck --bom-check` would fail every Dependabot update,
  which changes a lockfile but can't rebuild the map. The Freshness workflow runs it each week,
  and keeps its issue open while the map is out of date.

## 2026-10-05 — Release 0.1.2 is tagged, and releases get a workflow

- **Asked:** after the merge, the owner asked for everything to be merged and the release made,
  then agreed to a pull request that adds a release workflow and corrects this record.
- **Merged:** Dependabot's three open pull requests, #12 to #14, after they were tested together
  on `main`: ruff 0.16.10, `uv_build` from 0.12.19, and Claude Code 2.1.283 for the catalog
  validator. Every check passed before and after.
- **Found:** this session can't make a tag. Auto mode refused it as publishing. Once the owner
  turned auto mode off, the session's GitHub access refused writes to the tag API with a 403.
- **Released by the owner:** `v0.1.2`, from GitHub's release form, aimed at `main`. Its tag is
  lightweight, on `bc683ca`: the release commit `29bbaa1` plus the three tool updates, which
  change nothing an installed copy uses. Its notes are the changelog's 0.1.2 section, under the
  install commands. A published tag stays where it is, so this supersedes the Release 0.1.2
  entry's plan of an annotated tag on `29bbaa1`.
- **Chosen:** `.github/workflows/release.yml`, a copy of `git-workflows`' tested example, makes
  each release's tag from now on, the route the standard gives from T2. It runs from the Actions
  tab with a version and a commit's full SHA. It refuses a version that isn't Semantic
  Versioning, a commit not on `main`, a commit whose changelog has no section for the version,
  and a commit with a check that hasn't passed. Then it makes the annotated tag as
  `github-actions[bot]`, and only its one job can write. The release page is then published from
  that tag in GitHub's form, as the README's operations section now says.
- **Next:** one run of it makes `v0.1.1`, which the v0.37.0 entry deferred: version `0.1.1`, SHA
  `cbe163fe384d92025ca40d3981ae3dbff75b703a`. That commit's changelog has the section, and its
  three checks passed.

## 2026-10-05 — Release 0.1.2

- **Asked:** the owner: "get everything ready for the next release/version/commit, etc.", and
  then: "after you merge and make a new version and release".
- **Chosen:** this pull request's merge is release 0.1.2, carrying standard v0.40.0 and the
  `git-workflows` skill. The owner asked for the merge from this session, and it takes a merge
  commit, as `AGENTS.md` says. A version that reaches `main` is published, tag or no tag, so the
  release is written before the merge: the changelog's unreleased entries move under
  `[0.1.2]`, and both catalog entries say 0.1.2. Claude Code updates an installed copy only
  when that string changes, so copies installed since 2026-09-23 move on from v0.36.0.
  - *Why 0.1.2:* the 2026-09-23 release entry keeps 0.2.0 for the rebuild's release, and under
    0.x anything may change. Nothing in the release is breaking: no skill is renamed or
    removed, and the new plugin is added beside the old one.
  - *The date* is the day the changelog was written. If the merge falls on a later day, the
    heading takes the merge's date in the same pull request.
- **Waiting on the owner:** the tags. The `v0.1.1` tag, which the v0.37.0 entry deferred to this
  release, goes on `cbe163f`, that release's merge commit, and `v0.1.2` on this pull
  request's merge commit. Both are annotated, as the standard asks from T2. This session's
  permission settings refused making a tag through GitHub's API, so the standard's route from
  T2 applies: a `workflow_dispatch` job makes each annotated tag, as `git-workflows`' tested
  example does. The Releases UI would make a lightweight tag. Each tag's GitHub release follows
  it, as v0.1.0's did.

## 2026-10-05 — v0.40.0's parity runs

- **Asked:** the v0.40.0 entry held its parity runs until the owner had seen the decisions and
  options. The owner has, and asked to "update all".
- **Runs:** one run of each sample, each by a fresh subagent given the documented prompt, on the
  skill as committed at `c3da657`. Its standard last changed at `983b783`, and its SHA-256 starts
  `8f46f927`. Each run was graded with `python -m skillcheck.parity` and compared with the
  baseline. Each passed every check, and left its sample's working tree clean and its refs where
  they started.
  - **Audit:** twenty checks, and both manual checks hold. One value moved: dimension 4 to
    `BLOCKER`. That's the v0.37.0 rule for a tracked `settings.local.json`, which every audit run
    since has moved.
  - **Re-check:** thirteen checks, and all three manual checks hold. No value moved.
  - **Greenfield:** seven checks, and no difference from the baseline. Both manual checks hold:
    the recommendation names a runner-up and what each option costs, and leaves the pick to the
    person, and nothing was generated.
- **Found:**
  - The samples' prepared replies predate F80's question on co-maintainers, so every run took its
    default, "no", and showed it at the gate, as the text says. Settling that means changing the
    replies, which takes a new baseline.
  - Five gaps in the text, now F109 to F113 in `ROADMAP.md`, which wait with F81 to F108. Every
    run met F109.
- **Departures the runs recorded,** none touching a sample or a graded value:
  - the audit and greenfield runs each listed the file names in the sample's bare remote, which
    sits beside the sample, outside the directories the prompt allows. Neither opened anything
    there;
  - the audit run read PyPI, the known limit `docs/testing-the-skill.md` names, and kept a pip
    cache in `/tmp` while it ran.
- **Not done:** the procedure is unchanged. Moving each bare remote out of its sample's parent
  directory would prevent the first departure. It touches no graded value, so it can wait for
  the next baseline.

## 2026-10-05 — The repositories the skills run on go unnamed

- **Asked:** the owner asked that this repository name nothing a skill has been run on or
  tested against, unless it's a dependency or a research source, and that it read
  professionally, since people other than the owner may use it.
- **Chosen:** `AGENTS.md`'s convention for a public repository now says so. Such a repository
  is "a live repository" here, and goes unnamed even by a quote a search would find. Nothing
  checks it, since a check would have to name what it looks for.
- **Checked:** the tracked files, every commit message in the history, and every pull
  request's title and body. None names such a repository. The products named in research
  files are research sources.
- **Changed:** one lesson in `ROADMAP.md` quoted a live repository's own words, which a code
  search would find. It now describes the step instead, and the lesson after it no longer says
  what kind of input the catalogue lacked.

## 2026-09-30 — The text, audited against the repository

- **Asked:** the owner: "audit all text, readme, changelog, tasks, anything. we need this up to
  date".
- **How:** a reader agent was started for the sweep, but stopped at once when the account hit its
  spend limit, so the sweep was done in this session instead. Every relative link in the
  repository's Markdown was resolved, every table's rows were counted against their header, and
  the text was searched for versions, counts, statuses and "pending" or "not yet" wording, each
  compared with the repository and, for dated facts, their sources.
- **Found and fixed:**
  - a table row in `git-workflows`' audit that GitHub split in two, because a `|` in a command
    ends a cell even inside code. Escaping it would give an agent reading the raw file a broken
    command, so the command no longer uses a pipe, nor does a row of `SKILL.md` that had
    escaped one. `skillcheck` now fails on a table row whose cell count differs from its
    header's;
  - `.claude/settings.json` turned off the `standards` plugin's copies but not the new
    `engineering` plugin's, so a session here could load an installed `git-workflows` beside
    the one being edited;
  - `.claude/rules/python.md` said tests never read real skills, which the asset tests must;
  - the changelog linked Keep a Changelog 1.1.0, and said "The standard is now" of three
    versions it has since left;
  - the research prompt index still named `git-and-review`, shipped as `git-workflows`;
  - the README said nothing of the freshness checks, and its skill row nothing of the reasons.
- **Found and left, with the reason:**
  - `CHANGELOG.md` has a 0.1.1 section dated 2026-09-23, but the remote has only the tag
    `v0.1.0`. The release route is the owner's open decision, so no tag was made;
  - the plan was partly outside `ROADMAP.md`: this session's own planning notes numbered
    proposals past F102. Five checked today are now F103 to F107 in the roadmap. Two others,
    about the organisation marketplace and where GitHub looks for `SECURITY.md`, couldn't be
    confirmed from pages that load here, and stay out until they are;
  - this repository states no commit grammar and checks none, which the standard rates `GAP`
    from T2. Its recent subjects mix "area: summary" with plain sentences. Which grammar to
    adopt is the owner's call.
- **Checked:** `skillcheck` reports 0 findings, and the suite runs 261 tests at 100% coverage.
  `.test-baseline` moves from 259 to 261.

## 2026-09-30 — The repository keeps its facts current, and checks its own shape

- **Asked:** the owner: "This also needs to have a way to be kept up to date and audit itself".
  Then, later: "audit all text, readme, changelog, tasks, anything. we need this up to date".
- **Chosen:** what can be checked from the commit is checked on every pull request. What
  depends on the date or the web is checked on a schedule, so a pull request's result depends
  only on the commit.
  - `skillcheck` now reads every row of each skill's `references/facts.md`. A row needs one ID
    in backticks, used once; an https link, or the `git ls-remote --tags` command that shows
    the fact; a quote; and a check-by date after its checked date. Every fact another file
    names by ID must exist. It found three rows whose source was a command, which it now
    accepts, and prose in the standard that looked like a fact ID, which it now ignores.
  - `skillcheck --due [DATE]` lists the facts due to be checked again. `skillcheck --verify`
    fetches each source and looks for its quote, and runs `git ls-remote` for a tag's commit,
    which is how a moved tag gets caught.
  - `.github/workflows/freshness.yml` runs both every Monday and on demand. It keeps one issue
    open while anything is due, adds each run to it, and closes it once everything is current.
    Both modes end with a summary line, and a run without one fails, so a crash can't pass for
    a clean result.
  - Every skill except the standard's must link `references/why.md`. The standard gives its
    reasons inline, and changes only on its own.
  - A reference that names another reference's file, as the cold review found 19 times, now
    fails like a link to it. Naming `facts.md` is allowed, because a fact is looked up rather
    than read on to.
  - A test scans this repository's own workflows with zizmor.
- **Checked:**
  - The verifier ran against the live sources: 79 of the 82 facts have a quote, and every
    one was found. That includes the pinned action SHAs, read again with `git ls-remote`.
  - Three github.com pages couldn't be fetched from this container, which refuses them, so
    their facts now cite the same files on raw.githubusercontent.com.
  - PyPI serves a plain client a browser check. The three version rows it backs have no quote
    to look for, and are checked by hand when they fall due.
  - The new code is at 100% coverage. Each new rule has a test that plants the defect and
    asserts the rule fires alone.
  - `.test-baseline` moves from 228 to 259.
- **Not done:** a periodic self-audit by a Claude session, which would run this repository's own
  standard against it, and spend the account's usage each time. It is offered to the owner, not
  set up.

## 2026-09-30 — `git-workflows`: the cold review, the trigger check, and the reasons behind each rule

- **Asked:** the owner: "It is about both, guidance and format. And how to use langusges, and
  why, and how. It's everything. […] Why do we do it this way? Why is it logical? Could it be
  better? What do other people do and why do they do it? Pros and cons, etc". And: "I have
  repos with 15 minutes of ci before the can merge to main, then like another 25 minutes of ci
  on main. I don't want to weaken tests, but is this needed?"
- **Chosen:** every skill gets `references/why.md`. For each rule that matters it gives the
  advice, the reason, what other projects do and why, what each choice costs, when to choose
  differently, and what could be better. `git-workflows` has the first one. Its last section
  answers the CI question: how GitHub decides what a pull request tested, when a second run on
  the default branch repeats one already done, and how Rust, Google, Chromium, LLVM and
  Kubernetes split the work. What other projects do goes in `facts.md` like any other dated
  fact, so it is checked again when it falls due.
- **The cold review** (a second reader, 2026-09-30): "ready after the listed fixes". Each
  finding was checked against the files and the standard before it was fixed. It found four
  blocking defects:
  - B1: the release job tagged whatever commit the dispatched branch pointed at, and read no
    CI. It now takes a SHA, checks the commit is on the default branch, reads its
    `CHANGELOG.md` at that commit, and requires every check on it to have passed, with at
    least one check present.
  - B2: the release workflow granted `contents: write` to the whole workflow, and its
    checkout kept credentials. It now reads at the top, writes only in its job, keeps no
    credentials, and passes zizmor.
  - B3: two references said the standard's starter CI has both test guards. It has only the
    collection guard. The skill now ships `assets/workflows/tests.yml` with the completion
    guard, and proposes it to the standard.
  - B4: references pointed to other references 19 times, by name rather than link, which
    skillcheck couldn't see. Each now says what the reader needs, and skillcheck now fails on
    the named form too.

  And eight to fix before the upload:
  - S1, S2: the CI subject check refused `Revert "…"` commits, and the hook refused a message
    that began with a template's comment. They now share one list of exemptions, CI refuses
    `fixup!` commits that were never squashed, and the hook reads the subject after
    `git stripspace`, tested through `git commit`.
  - S3: `chmod +x` doesn't reach the commit from Windows. The skill now says
    `git add --chmod=+x`, and to check for `100755`.
  - S4: under squash, GitHub's default takes a one-commit pull request's own message. The
    skill now says to set the squash title to the pull request's title.
  - S5, S6: the audit's statuses now follow the standard, including `MIRROR` and
    `UNVERIFIABLE-HERE`. Its searches cover `.yaml` and `github.head_ref`, and the
    conflict-marker search has a CI form that fails when markers exist.
  - S7: the rules the standard owns are cited, not restated: review with one maintainer,
    point releases, the version scheme and deprecation, and when to propose a client-side hook.
  - S8: the version check took `1..4` and refused `1.4.0-rc.1`. It now takes Semantic
    Versioning with a pre-release label, reading the whole string.
- **The review's minor points, fixed:**
  - "stranded" now says the commits survive under the pull request's refs;
  - an archive tag is pushed;
  - `--delete-merged` skips most branches made with `git push -u`, so the skill says so and
    gives the `gone` check;
  - the local-refs caveat for shallow clones;
  - the `^{}` line of an annotated action tag;
  - `gh release create` and `--verify-tag`;
  - `co-authored` needs the address tied to an account;
  - the unused `setup-python-sha` fact is gone;
  - the description names conflicts, recovery and secrets;
  - a section on force-pushing safely, conflicts, `rerere` and the reflog;
  - `git rm --cached` on shared files;
  - `concurrency` and `merge_group` in the examples;
  - the hook test runs in a subshell.
- **Not fixed, and why:** that GitHub can restore a deleted head branch. The page that says so
  didn't load here, so the claim was left out rather than stated unchecked.
- **The trigger check,** judged by a model: all 22 requests routed as expected. Three positive
  requests passed on thin margins: a secret that reached a commit, a changelog entry or a
  version number, and a required check that never reports. The description now names all
  three. Five requests were added: slow CI, a rebase conflict, a lost commit, the merge
  strategy's reasons, and a near miss for the planned `ci-cd` skill. That makes 27, 9 of them
  near misses.
- **Sources:** 37 facts were added and one unused fact removed, 82 in all, each new quote found
  at its source on 2026-09-30. 18 are about other projects' practice: the Linux kernel, Git,
  CPython, Rust, Go, LLVM, Google, Chromium, Kubernetes, Fowler, Git Flow's author, towncrier,
  pip and semantic-release. 14 are about GitHub, and 5 about Git. `sources.md` gives each
  licence. Google's book is CC BY-NC-ND 4.0 and Fowler's article is copyrighted, so
  both are quoted and never adapted.
- **A new development dependency:** zizmor 1.30.1, locked, so the tests can scan the example
  workflows as the skill tells every repository to.
- **Checked:**
  - actionlint 1.7.12 and ShellCheck 0.11.0 pass on the four workflows and two hooks.
  - zizmor finds nothing with its default rules. Its pedantic rules leave only informational
    notes.
  - The asset tests grow from 18 to 51, and the suite runs 228 tests.
  - `.test-baseline` moves from 195 to 228.
- **Owner's step:** upload the changed `skills/git-workflows` to claude.ai again.

## 2026-09-30 — `git-workflows`: the first skill built from the owner's own skills

- **Asked:** the owner: "The point of this is not to make Claude skills run in Claude code
  sessions, but for you to assimilate the knowledge and information they already have and
  leverage in the repo." Asked how to start, the owner chose one area end to end, said all four
  areas are in daily use, and said company information comes here as generic knowledge only.
- **Chosen:** `git-workflows`, with the same name as the owner's claude.ai skill, so an upload
  replaces it. It ships in a new `engineering` plugin. It takes the ROADMAP's `git-and-review`
  row. `ci-cd` and `versioning-and-releases` stay planned, narrowed to caching, environments
  and deployment, and to release notes and support windows.
- **Built from:**
  - the owner's `git-workflows`, as topics, checks and lessons, with nothing copied. Its
    company examples were left out: a work scheduling project, ERP export names, the owner's
    machines. So was its advice against lessons the live repositories paid for: squash-merging
    feature branches, bulk-deleting merged branches, `--no-verify`, a "Current State" section in
    `CLAUDE.md`, and Conventional Commits as the only grammar.
  - its bugs, fixed rather than carried: `.gitignore` comments after patterns, a `!` under an
    ignored directory, a pre-push hook that checked the current branch, `paths` with
    `paths-ignore`, and `Cargo.lock` left out of libraries.
  - the lessons in `ROADMAP.md` from the live repositories (F74, F81, F85, F92, F93, F99),
    FFmpeg's practice (`research/runs/2026-09-30-ffmpeg-reference.md`), and research R08 and R05
    as leads.
  - the standard, cited by section rather than restated.
- **Sources:** every dated fact is in the skill's `references/facts.md`, with its source, a short
  quote, the date checked (2026-09-30) and a date to check it again. Three leads were out of date
  when checked: Git 2.56.0 was released 2026-09-28, where R08 had 2.55.0; Keep a Changelog 2.0.0
  was released 2026-06-07, where R05 had 1.1.0; prek is at 0.5.4, where R08 had 0.5.1. GitHub's
  rule on `GITHUB_TOKEN` now has a third exception: a pull request the token opens or updates
  gets runs that wait for approval.
- **Licences:** nothing is copied beyond short quotes, and `references/sources.md` names each
  source's licence, checked at its licence file on 2026-09-30. The skill is Apache-2.0, with no
  third-party notice needed.
- **Whose work:** the owner's skill is an organisation skill. Only generic, non-confidential
  knowledge came in, under the organisation's written permission recorded in the inception
  entry.
- **Reviewed** against `docs/authoring-a-skill.md`:
  - Items 1 to 4: whose work, sources, licences, and no company detail. See above; the
    examples use placeholders.
  - Item 5: no claude.ai paths, and destructive commands come with a dry run or confirmation.
  - Item 6: frontmatter fields from the spec only, with a 707-character description in the
    third person.
  - Item 7: `SKILL.md` is a 98-line router. Its references are one level deep, each with a
    title and a line on when to read it.
  - Item 8: every example lints or runs.
  - Item 9: `tests/fixtures/skills/git-workflows.json` holds 22 requests, 8 of them near misses
    for neighbouring skills.
  - Item 10: the skill is in the catalog, the ROADMAP and the README.
  - Item 11: the changelog has the entry, and `metadata.reviewed` is 2026-09-30.
  - Item 12, turning off the old copy, is the owner's step once the skill is uploaded.
- **Checked,** on 2026-09-30:
  - The two hooks and the two workflow scripts:
    - they pass ShellCheck 0.11.0 and actionlint 1.7.12, which found an unquoted `: ` in a step
      name that made the workflow invalid YAML;
    - they run in scratch repositories: the hooks refuse and accept what they should, the
      subject check fails when it has nothing to check, and the release job refuses a
      malformed version and makes and pushes an annotated tag.
  - `tests/test_git_workflows_assets.py` repeats those runs in CI, with 18 tests. They caught
    both planted breakages: a pre-push hook that checked the current branch, and a job without
    a timeout.
  - Every `facts.md` quote was found on its source page.
  - `.test-baseline` moves from 177 to 195.
- **Still running when this was committed:** a second reader's cold review, and a model-judged
  run of the trigger set. Their findings, and what changes, go in the next entry.
- **Owner's step:** upload `skills/git-workflows` to claude.ai, and turn off the old synced
  `git-workflows`, so sessions don't load two.

## 2026-09-30 — This repository, fixed against its own standard

- **Asked:** told that the owner's synced claude.ai skills advise against lessons the live
  repositories paid for, the owner said: "fix this repo first, then i can upload skills to fix.
  this repo will be the master for claude code, claude skills, and gnenerall non-llm coding
  practices, amungst other things".
- **Scope:** it goes into the first lines of `AGENTS.md` and the README, as the owner's word. The synced skills are fixed by uploading this repository's skills once they're built,
  not edited on their own.
- **Found:** this repository, read against v0.40.0 and the lessons in `ROADMAP.md` (F81 to
  F102), had five gaps:
  - Its merge strategy was unrecorded, though every pull request so far merged with a merge
    commit, and its commits are cited from outside. From T2 that is `GAP` (F74).
  - Nothing proved the test suite ran to the end (F81).
  - The standard's version is stated in the README's and the roadmap's rows as well as in the
    file, and nothing compared those copies (F97). The changelog's line about FFmpeg's
    proposals still said they awaited approval, which is the drift that rule is for.
  - Nothing looked for a merge's conflict markers (F92).
  - Its conventions didn't say which were checked and which were advice (F94).
- **Chosen:**
  - `AGENTS.md` records merge commits as the strategy, and says each convention's enforcement
    or that nothing checks it. It also takes the waiting-on convention the starter file got in
    v0.40.0 (F70), and asks a commit adding a Markdown file to name the homes it considered
    (F102).
  - `skillcheck` compares the README's and the roadmap's copies of the standard's version with
    the file's, and fails on conflict markers in the files at the root and under the tracked
    directories.
  - CI writes pytest's report and fails where it is missing or counts fewer tests than
    `.test-baseline`, which moves from 144 to 177.
- **Human action:** the merge strategy is enforced only once the repository's settings allow
  merge commits alone: Settings, General, Pull Requests, with squash merging and rebase merging
  turned off.
- **Checked,** on 2026-09-30:
  - The 33 new tests: 27 fail against the checks before this change, restored afterwards from a
    copy checked by its SHA-256. The other six assert that lookalikes and files outside the scan
    pass.
  - A pytest run whose second of three tests calls `os._exit(0)` exits 0 and writes no report.
    The new CI step, extracted from the workflow and run under `bash -e`, fails that, fails a
    report counting 133 tests against the baseline of 177, and passes the full report.
  - `git log --first-parent origin/main`: every commit since the first is a merge commit.

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
