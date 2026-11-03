---
name: steward
description: How sessions drive this repository's pull requests to green and merge them, or hold, report and stop. Read before acting on any pull request, CI result, review comment or release here.
---

# Steward

Owner: rmccann-hub. Reviewed: 2026-11-03, against `git-workflows`' `pr-stewardship` module, and
the repository's settings and ruleset read that day. It applies to every pull request into
`main`. The base branch's copy of this file is in force, and only the owner merges a change to
it.

This file says how a session acts on a pull request here. `AGENTS.md` holds the repository's
conventions and commands, and `docs/decisions.md` the record of each choice; where this file
and either disagree, stop and ask the owner, because one of them is wrong.

## Why this repository needs care

- **A merge ships.** claude.ai's plugin sync reads `main`, so a merged skill change reaches the
  owner's chats at once.
- **Other repositories run what it releases,** in their sessions and their audits.
- **It's public.** Nothing names an audited repository (the `private-name` check), and nothing
  work-owned lands without a recorded permission.

## Merging

- **Method:** a merge commit, the only one the settings allow, titled
  `Merge pull request #<n> from <owner>/<branch>`. Pass the head commit's SHA to the merge, so a
  push that lands meanwhile stops it.
- **A session may merge its own pull request** for work the owner asked for, once every check
  has passed on the head commit, no thread waits on it, there's no conflict, and no hold covers
  it. That's `AGENTS.md`'s standing rule.
- **Only the owner merges a pull request that changes** this file, `AGENTS.md`, `CLAUDE.md`,
  anything under `.claude/`, `.github/workflows/`, or a ruleset (the owner's word of 2026-11-03,
  "do everything you need to", on that recommendation). The account is one person's, so GitHub
  can't enforce this: a session's merge carries the owner's name. It holds by a session's
  conduct alone. Open the pull request, say it's the owner's to merge, and stop.
- **A skill change passes `docs/authoring-a-skill.md` before it merges.** After the merge, give
  the owner the claude.ai tries from `uv run skillcheck --tries <module>`. A miss is fixed, or
  the merge reverted, at once.
- **Dependabot's pull requests** are never merged one by one. Bring the open ones in together
  on one branch, regenerate the dependency map with `uv run skillcheck --bom`, and merge that,
  once it passes, as #58 did. A single Dependabot pull request fails `--bom-check` by design.
- **Drafts are never merged.** Pull request #73 (`claude/brave-pasteur-40a2fq`) holds draft
  modules: never push `main` onto it, or merge it.
- **A pull request the session didn't open:** comment, and push only with its author's word.
- **Auto-merge is on** in the settings. It waits for required checks and nothing else, so a
  hold must be a required check to stop it.

## Holds

Live holds are the `hold` label on a pull request, enforced by the `hold` check, which fails
while the label is on. Read the holds again at the moment of merging, releasing or sending
anything out.

| Standing hold | Covers | Set by, when | Lifted by |
|---|---|---|---|
| Releases | Dispatching the Release workflow, or tagging | The owner, standing | The owner's word, for each release |
| The standard | Any edit to `skills/project-bootstrap-and-audit/references/` as part of other work | `AGENTS.md` | A change proposed, approved and applied on its own |
| The other repositories | Any push, comment, issue or pull request in a repository this one audits | The audit rules, in `audit-reports`' README | The owner's word, each time |

## Before every push

Run the repository's own checks, and regenerate the map last:

1. `uv run skillcheck .` and `uv run pytest`; `uv run ruff check` and `uv run ruff format --check`
   when Python changed.
2. `uv run skillcheck --verify` when a fact was added or changed.
3. `bash skills/house-style/scripts/wrap-check.sh <file>` on each changed Markdown file. Vale
   isn't installed in a cloud session, so keep to the house style: sentence-case headings,
   American spelling, and no filler words such as "just".
4. `npx --no-install claude plugin validate --strict .` when the catalog changed.
5. `uv run skillcheck --bom`, then `--bom-check`, as the last step before committing.

## Conflicts and stale branches

- No event arrives when `main` moves into a conflict. Check mergeability before merging and
  after each push to `main`.
- Merge `main` into the branch; regenerate `bom.json` and `docs/dependencies.md` with the
  tooling, never by hand. Never rebase or force-push a branch someone else pushed to.
- A branch idle for a week: report it to the owner; don't delete it.

## Red or stalled CI

The ruleset requires `checks`, `catalog`, `secret-scan` and `prose`. Treat `subjects` and `hold`
as required too, whether or not the ruleset lists them yet.

- **This pull request's own failure:** find the cause and push a fix.
- **`checks` fails on `bom: out of date`:** run `uv run skillcheck --bom`, commit, push.
- **`prose` fails:** fix each line Vale names; the job's log lists them.
- **`checks` fails on the test count:** `.test-baseline` is never lowered to get green.
- **Re-run a failed job once,** only when the failure isn't this pull request's code: the
  runner died before any test ran, or the job passed on this head before. A second failure on
  the same head is real. A source that answers 403 or 503 to `--verify` locally is noted, not
  re-run in CI.
- **`secret-scan` fails:** stop pushing, print no value, and report to the owner.
- **Never** skip, disable or quarantine a test, or loosen a check, to get green.

## Review

- **Blocking:** the owner's comments and change requests.
- **A bot's finding** is checked before it's fixed. Only the reviewer resolves a person's
  thread.
- **Small asks** are fixed and pushed. Anything larger gets a reply with a proposal first.

## Releases and other repositories

- **A release needs the owner's word.** Then:
  - open a pull request that dates the changelog section, moves both catalog versions, and
    records the release in `docs/decisions.md`;
  - merge it, and wait for CI to pass on the merge commit;
  - dispatch `release.yml` with the version and that commit's full SHA;
  - check the tag, the release page and `gh attestation verify` on one of its files.
- **Messages to another repository** go through the owner, as text or a file they send. Each
  carries the condition it depends on, such as "if the pull request is still open". Findings
  about another repository go to `audit-reports`, never here.

## When unsure, and when to stop

- **Unsure:** hold and ask; never merge on a guess. One session per pull request.
- **Stop** when the pull request is merged; ready, meaning green on the head with no open
  thread and no conflict; blocked on the owner; or after two failed fixes for one failure. Then
  report.

## Reporting

- **Times:** the UTC stamp, with New York time first for the owner, from
  `uv run skillcheck --time <stamp> America/New_York`.
- **Say what was measured:** which checks, on which commit, and what wasn't run.
- **Review items** are answered as `done <commit>`, `already <where>`, `not doing: <why>` or
  `wrong: <what>`.
- **A session that stops with work outstanding** says what it waits on, and from whom.
