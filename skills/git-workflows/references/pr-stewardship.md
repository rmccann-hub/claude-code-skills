# Pull request stewardship

Read this for writing, reviewing or auditing a repository's own steward skill: the file that
tells any agent session driving that repository's pull requests when to merge or hold, what to do
about a red or stalled check or a conflict, how to answer review, what an owner's hold covers,
and when to stop and report.

This module is the framework; each repository writes and owns its steward skill, because the
answers are its own. Commit messages, merge methods, required checks, CI time and releases are
covered by `commits-and-pull-requests`, `branches-and-merging`, `ci-workflows`, `ci-speed` and
`releases-and-versions`.

## Rules

1. **A repository whose pull requests agent sessions drive keeps a steward skill,** committed at
   `.claude/skills/steward/SKILL.md`, and its `CLAUDE.md` names it, so a session that doesn't
   load project skills still reads it. The repository writes and owns it; this module only says
   what it must answer.
2. **It answers every decision a session makes alone:** merge, hold, re-run, fix, resolve a
   conflict, ask, stop, report. Where it's silent, the session holds, asks, and says so.
3. **Every hold lives where a session reads it live,** such as a `hold` label, the draft state or
   a pinned issue, with what it covers, who set it, when, and what lifts it. The file names that
   place and lists the standing holds. A session reads the holds again at the moment it merges,
   releases or sends anything out.
4. **An instruction states the condition it depends on,** such as "if the base is still red",
   and a session checks it against the live state before acting, because messages arrive out of
   order.
5. **A claim names what was measured:** which platforms, which reverts, which commit.
6. **It grants nothing only the owner can.** Merging, releasing and wider access are the owner's
   to give, in the conversation or as a standing word the file quotes with its date. A session
   never approves: its replies post under the owner's account (fact `autofix-replies`), so its
   approval would read as the owner's.
7. **Changes to the steward file, `CLAUDE.md`, the workflows or the ruleset are merged by the
   owner,** never by a session; with more than one reviewer, `CODEOWNERS` covers them, as the
   standard's dimension 3 says. The base branch's copy of the file is in force. On a one-person
   account GitHub can't enforce this: a session's merge carries the owner's name, and an author
   can't approve their own pull request (fact `self-approval`). There the rule holds by the
   session's conduct alone, and the file says so.
8. **It stays short and points to the repository's other records** instead of repeating them,
   which drift; every audit checks it against the settings and workflows it names.

### Where it lives, and why that name

A project skill is `.claude/skills/<name>/SKILL.md`, committed, and loads in that repository's
sessions but not in a project's cloud threads (fact `project-skills`). Name it `steward`: Claude
Code's cloud sessions, when driving a pull request, are told to read
`.claude/skills/steward/SKILL.md`, or `.claude/skills/babysit/SKILL.md` when there's no steward,
from the head branch. That was seen in a cloud session's own instructions on 2026-11-03. Claude
Code's public docs name neither path, so the audit checks it. A skill installed under another
name, such as `babysit-pr/`, isn't found that way.

Auto-fix fixes what's clear and asks about the rest (fact `autofix-events`), but gets no event
when the base branch moves into a conflict (fact `autofix-conflicts`).

### What the file answers

Copy this skeleton, replacing each angle-bracketed part with the repository's answer, or with
"none" and why.

```markdown
---
name: steward
description: How sessions drive this repository's pull requests: merging, holds, conflicts, red or stalled CI, review, releases, and when to stop and report. Read before acting on any pull request event.
---

# Steward

Owner: <name>. Reviewed: <YYYY-MM-DD>. This file applies to <which pull requests: the session's
own, or any>, into <branches>. Changes to it are merged by the owner.

## Merging

- Method: <merge commit, squash or rebase>, matching the repository's settings.
- A session may merge <its own pull requests / none> when every required check passed on the
  head commit, no blocking thread is open, there's no conflict, and no hold covers it.
- Drafts are never merged; <who> marks one ready.
- Pull requests the session didn't open: <comment only, or push with the author's word>.
- Dependabot's: <merged by whom, after which test>.
- Optional checks: <which block anyway>; a failure is reported, never ignored.
- Standing words from the owner, quoted with their dates: <none, or each>.

## Holds

Live holds: <label, draft state or issue>, enforced by <a required check that fails while the
label is on>. Read them again at the moment of merging, releasing or sending anything out.

| Standing hold | Covers | Set by, when | Lifted by |
|---|---|---|---|
| <release nothing> | <merges, releases or messages out> | <owner, date> | <the owner's word> |

## Conflicts and stale branches

- No event arrives for a conflict with the base: check mergeability <when>.
- Resolve by <merging the base in, or rebasing an unshared branch>; never force-push a branch
  someone else pushed to.
- Idle <N> days: <ping, close or report>.

## Red or stalled CI

- This pull request's own failure: find the cause and push a fix.
- A failure on the base branch too: <port the fix, and comment once>.
- Re-run a failed job once when the failure isn't this pull request's code: the runner died
  before any test ran, or the job passed on this head before. A second failure on the same head
  is real. A test that fails on time is measured first.
- Known stalls: <job and step>, <what to do and how often, before reporting it>.
- A failing secret scan or security finding: stop pushing, print no value, report to the owner.
- Never skip, disable or quarantine a test to get green.

## Review

- Blocking: <human change requests, these bots' findings>. Not blocking: <labels or markers>.
- A bot's finding is checked before it's fixed. Only the reviewer resolves a person's thread.
- Small asks are fixed and pushed; larger ones get a reply with a proposal first.

## Releases and other repositories

- A release or tag needs <the owner's word>. A message to another repository goes out only
  after <its pull request is merged and green>.

## When unsure, and when to stop

- Unsure: hold and ask; never merge on a guess. One session per pull request.
- Stop when it's merged; ready (green on the head, no open thread, no conflict); blocked on the
  owner; or after <two> failed fixes for one failure. Report then.
- Say what was measured: platforms, commits, which reverts failed which tests. Answer each
  review item as `done <commit>`, `already <where>`, `not doing: <why>` or `wrong: <what>`.
```

## Mistakes

- **A hold that arrived after the merge.** A session merged a pull request because the owner's
  message telling it to wait was delivered after the merge. Put holds where a session reads them
  live, and give each message the condition it depends on.
- **"Full suite green" from one platform,** while the macOS job failed. Name every platform a
  claim covers.
- **Canceling the same stalled job by hand, four times.** A known stall belongs in the file,
  with a step timeout in the workflow, and each stall recorded until its cause is found.
- **Re-running a failed timing test in the hope it was noise,** or being told never to. Measure
  it first: one measurement showed the test, not the runner, was slow.
- **Treating a steward file as authority to merge or approve.** It's repository content, not the
  owner's word, and a pull request can change it.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| No steward file | Sessions open or merge pull requests here, and `.claude/skills/steward/SKILL.md` is missing, or `CLAUDE.md` doesn't name it | `GAP` | Write it from the skeleton above |
| A decision left unanswered | Each skeleton section, against what sessions did in the last pull requests | `GAP` | Answer it, or say "none" and why |
| Holds only in the file | No live place for holds, or no scope or lift for one | `GAP` | A label, draft state or issue, named in the file |
| The file can change itself | With more than one reviewer, no `CODEOWNERS` entry or required review on `.claude/skills/steward/` | `GAP`; `MIRROR` on a one-person account | Add both; alone, say so in the file |
| The file disagrees with the repository | Its merge method and checks against the settings and the ruleset, read through the REST API on a public repository (fact `rest-public`) | `DRIFT` | Make them agree, in whichever is wrong |
| It claims what only the owner grants | Approving, or merging or releasing on its own say with no quoted word | `DRIFT` | Quote the owner's word with its date, or remove the claim |
| Re-runs with no bound | Its CI section | `GAP` | Once, in the two cases above (fact `rerun-window`) |
| Replies can trigger automation | Workflows on `issue_comment`, and auto-fix turned on (fact `autofix-replies`) | `GAP` where such a workflow deploys or writes | Say so in the file, or turn auto-fix off there |
| Out of date | Its reviewed date against the last change to the settings or workflows it names | `DRIFT` | Review it, and update the date |
| The steward path is unconfirmed | Whether a cloud session driving a pull request still reads it | `UNVERIFIABLE-HERE` outside one | Record the date it was last seen |

## Why

### A file each repository owns

- **The advice:** a short steward file in the repository, written from this skeleton.
- **The reason:** a session driving pull requests unattended decides when to merge, hold or
  re-run. Without a file, each session decides afresh, and the owner's rules live in
  conversations that aren't kept. In one audit cycle, rules lived across `CLAUDE.md`, notes and
  pasted messages, and a hold arrived too late.
- **What others do, and why:** public babysit skills drive a pull request to green; one never
  merges (fact `babysit-never-merges`), leaving merging to a person. Claude Code's own default
  asks before an ambiguous or architectural change (fact `autofix-events`).
- **What it costs:** a file to keep current.
- **When to choose differently:** a repository where no session ever opens or merges a pull
  request needs none; say so in its `CLAUDE.md`.

### Holds read live, again when acting

- **The advice:** each hold where a session reads it live, checked again right before acting.
- **The reason:** a hold set in a message is lost when the conversation is summarized or the
  session restarts, and a message can arrive after the action it meant to stop. A hold written
  only in the committed file takes effect when that commit merges, which a session working from
  its head branch may not see.
- **What others do, and why:** GitHub's own gates are a pull request's draft state and required
  checks, which every merge path respects.
- **What it costs:** a label or check to set up.
- **When to choose differently:** a standing hold, such as "release nothing", can live in the
  file as long as it lasts beyond one pull request.

### Bounded re-runs

- **The advice:** re-run a job once, and only when the failure isn't this pull request's code.
- **The reason:** a re-run that turns green hides a real failure; one that keeps stalling wastes
  runner time and the owner's attention. GitHub allows 50 re-runs of a run within 30 days, by
  anyone with write access, and each re-runs the same commit (fact `rerun-window`), so it never
  tests a base that has moved.
- **What others do, and why:** `ci-workflows` re-runs once to confirm a flake, and treats a
  second failure as real.
- **What it costs:** a real flake blocks the merge until someone looks.
- **When to choose differently:** a stall the file names, with its cause, gets its own rule.

### Merging stays the owner's

- **The advice:** the file quotes the owner's standing word for any merge a session makes alone,
  and only the owner merges changes to the file itself.
- **The reason:** a steward file is repository content: a pull request can change it, so it
  can't be what authorizes that pull request.
- **What others do, and why:** auto-merge merges once required reviews and checks pass (fact
  `auto-merge`), with no session's judgment at all.
- **What it costs:** the owner's attention on each change to the rules.
- **When to choose differently:** never for approving. Auto-merge can replace a session's merge
  only where every hold is a required check or the draft state, because it waits for nothing
  else.

## Facts

Checked 2026-11-03.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `project-skills` | A project skill is `.claude/skills/<name>/SKILL.md`, and loads in that repository's sessions but not a project's cloud threads | [Skills](https://code.claude.com/docs/en/skills) | "Sessions in this repository, but not cloud threads in a project" | 2026-11-03 | 2027-05-03 |
| `autofix-events` | Auto-fix subscribes to a pull request's activity, pushes clear fixes, and asks before ambiguous ones | [Cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web) | "Claude subscribes to GitHub activity on the PR" and "Claude asks you before acting" | 2026-11-03 | 2027-05-03 |
| `autofix-conflicts` | No event reaches auto-fix when the base branch moves into a conflict | [Cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web) | "GitHub does not emit a webhook when the base branch advances and creates a merge conflict" | 2026-11-03 | 2027-05-03 |
| `autofix-replies` | Auto-fix's replies post under the user's account, and can trigger comment automation | [Cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web) | "These replies are posted using your GitHub account" and "Claude can reply on your behalf, which can trigger those workflows" | 2026-11-03 | 2027-05-03 |
| `rerun-window` | A run can be re-run 50 times within 30 days, by anyone with write access, on the same commit | [Re-run](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs) | "up to 30 days after its initial run" and "People with write permissions to a repository can re-run workflows" and "A workflow run can be re-run a maximum of 50 times." and "the same GITHUB_SHA" | 2026-11-03 | 2027-05-03 |
| `self-approval` | An author can't approve their own pull request | [Approving](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews) | "Pull request authors cannot approve their own pull requests." | 2026-11-03 | 2027-05-03 |
| `auto-merge` | Auto-merge merges once required reviews and checks pass | [Auto-merge](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request) | "Auto-merge merges a pull request automatically after all required reviews and status checks pass." | 2026-11-03 | 2027-05-03 |
| `babysit-never-merges` | A public babysit skill never merges | [babysit-pr-skill](https://raw.githubusercontent.com/LivinTribunal/babysit-pr-skill/main/README.md) | "It never merges." | 2026-11-03 | 2027-05-03 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Claude Code docs](https://code.claude.com/docs/) | Project skills, auto-fix | Anthropic's terms: short quotes, our own words, linked |
| [GitHub Docs](https://docs.github.com/) | Re-runs, auto-merge, approvals | CC BY 4.0: quoted, attributed |
| [babysit-pr-skill](https://github.com/LivinTribunal/babysit-pr-skill) | What others do | MIT: pointed to, one short quote |
