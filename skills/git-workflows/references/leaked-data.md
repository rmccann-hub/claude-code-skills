# Leaked data

Read this when a secret, a token, an email address or other personal information has reached a
commit, a log or a release, or when someone asks to rewrite history to remove it.

It covers what to do once the data is in history. Keeping it out in the first place is
`gitignore` for secret files, `commits-and-pull-requests` for the address commits carry, and
`actions-security` for secrets in workflows.

## Rules

1. **Rotate a leaked secret first.** Once pushed, it's compromised, and removing the commit
   doesn't take it back.
2. **Name the secret by where it was, never by its value,** in the issue, the commit message
   and the decision record.
3. **Rewrite history only when the owner asks for it, knowing what it costs.** That's the one
   exception to never rewriting shared or cited history.
4. **Count before choosing, change only what you must, and rehearse first.**

### A secret in a commit

1. **Rotate it first.** Forks, clones, caches and the platform's own views may hold it.
2. **Then remove it from the tree,** add the file to `.gitignore`, and commit an example file
   without the value.
3. **Rewrite history only if you must,** for example where the value is still sensitive after
   rotation. It rewrites every later commit, breaks everyone's clone and strands every citation.
   Rotation is the remedy; a rewrite is cleanup.
4. **Name the secret by where it was.**

project-bootstrap-and-audit rates secret handling, push protection and the secret-scan job
(dimension 7), and its facts give push protection's defaults.

### Personal information in history

An email address in commit metadata, or a home folder in a committed log, can't be rotated.
Removing it means rewriting history, and only when the owner asks for it.

1. **Count before choosing.** Read-only, count each item in every place it can be:
   - commit metadata, messages and files;
   - release notes and release files, and published packages;
   - tags, branches and pull request refs.

   Then let the owner choose the scope with the numbers in front of them. Some copies can't be
   changed at all: a published package, an immutable release, a transparency log. A username
   that also starts the owner's public handle hides almost nothing when it's removed. In one
   live repository, narrowing the job to the email address alone made it about fifty times
   smaller, and left the other repository it shared a review loop with untouched.
2. **Change only what you must.** For an address in metadata only, use
   `git filter-repo --mailmap` (fact `filter-repo-mailmap`) with `--sensitive-data-removal`,
   version 2.47 or later (fact `sdr-version`). Add `--preserve-commit-hashes` to keep commit
   messages byte for byte (fact `filter-repo-hashes`). Every commit ID still changes, from the
   first rewritten commit on.
3. **Keep cited IDs resolvable.** Commit the tool's old-to-new map, and have every reader of
   commit IDs look an old ID up in it before asking Git, since an older clone still holds the
   old objects. Leave sent records as written. Keep the map file out of any citation scan:
   otherwise it meets the scan's floor on its own. Where another repository cites yours, agree
   the change with it word for word first, then run each side's checker on the other's tree.
4. **Rehearse on a scratch mirror,** and run the full test suite there. In that live rewrite,
   the suite found all 32 places that read commit IDs in one pass. The rewrite is
   deterministic, so the rehearsal's map has the same digest as the real run's, unless a
   branch moved in between.
5. **Hand the owner one script** that:
   - works in a new folder it names at the start and the end;
   - installs the pinned tool there, checked with `--require-hashes`;
   - before it pushes, checks for zero matches, the same commit count and the same refs, and
     that the trees, names, dates and messages are unchanged;
   - asks the owner to type `YES`, and pushes only then;
   - pushes with `--atomic` and `--force-with-lease=<ref>:<old>` on every ref, under
     `-c credential.helper=`, so the token isn't saved;
   - compares `git ls-remote` with what it pushed, and prints a summary to paste back.

   Rehearse the script itself against a local bare repository, including someone typing "no"
   and a stale lease. A fine-grained token needs Workflows write access as well as Contents,
   since the push rewrites commits that carry workflow files (fact `workflow-scope`).
6. **Warn the owner in advance:**
   - every signed commit loses its Verified badge (fact `rewrite-signatures`);
   - the first CI run after the force push can go red, where a gate compares against a commit
     that no longer exists;
   - rulesets that block force pushes must be off for the push, and on again after;
   - old commits stay viewable through `refs/pull/*` until GitHub Support removes them (fact
     `pr-refs-readonly`). On 2026-10-12, GitHub's support form had no "sensitive data"
     category: the route that worked was Repositories, then Repository features, then
     Branches. Its "Deletes" choice leads to deleting the whole repository, so avoid it;
   - a shipped app that checks out a fixed commit from the rewritten repository can't install
     afterward. Check every consumer of the repository first.
7. **Afterward, refresh every clone, the agent's own included.** A stale local branch still
   points at old history: one checker read the map from one and reported 13 false refusals.
   Run `git fetch --force --tags`, reset each local branch to its remote, or check from a
   fresh clone.

## Mistakes

- **Removing a leaked secret from the tree and calling it done.** It's still in history, in
  every clone and fork. Rotate it.
- **Quoting the secret's value** in the issue, the fix's commit message or the record. That
  leaks it again. Name the file and line.
- **Rewriting history before counting** what the rewrite would change, and where else copies
  live. The owner can't choose the scope without the numbers.
- **A force push without a lease,** or one that saves the token in the credential helper. Push
  with `--force-with-lease=<ref>:<old>` under `-c credential.helper=`.
- **Trusting a clone made before the rewrite.** Its branches still point at the old history.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A secret file is tracked | `git ls-files -z \| tr '\0' '\n' \| grep -E '(^\|/)\.env($\|\.)' \| grep -v '\.example$'`, and a secret scanner such as `gitleaks` over the history | `BLOCKER` while the value is live | Rotate it, untrack the file, ignore it, and commit an example file (`gitignore`) |
| A rewrite's map isn't used | After a history rewrite: the old-to-new map is committed, and every reader of commit IDs looks old IDs up in it | `DRIFT`: citations of old IDs fail | Commit the map, and route every reader through it |

## Why

### Rotate first, rewrite last

**The advice.** Rotate a leaked secret before anything else, and rewrite history only when the
owner asks, after counting and rehearsing.

**Why.** A pushed secret is copied at once: into forks, clones, caches and the platform's views,
some of which no rewrite reaches, such as `refs/pull/*` (fact `pr-refs-readonly`). Rotation makes
every copy worthless. A rewrite reaches only the copies you control, and costs every clone and
every citation.

**What others do.** GitHub's own procedure for removing sensitive data rotates first, then
rewrites with git-filter-repo's sensitive-data mode (fact `sdr-version`), and asks GitHub
Support to purge cached views.

**What each choice costs.** Rotation costs a new credential and its rollout. A rewrite costs a
coordinated force push, every signature (fact `rewrite-signatures`), and a map that every reader
of commit IDs must consult from then on.

**When to choose differently.** Personal information can't be rotated, so there the rewrite is
the only remedy, and the owner decides whether its cost is worth paying.

## Facts

Versions, dates and defaults, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `filter-repo-mailmap` | `git filter-repo --mailmap` rewrites names and email addresses, and nothing else | [git-filter-repo manual](https://raw.githubusercontent.com/newren/git-filter-repo/main/Documentation/git-filter-repo.txt) | "when rewriting author, committer, and tagger names and emails" | 2026-10-12 | 2027-10-12 |
| `filter-repo-hashes` | git-filter-repo rewrites old commit IDs written in commit messages unless given `--preserve-commit-hashes` | [git-filter-repo manual](https://raw.githubusercontent.com/newren/git-filter-repo/main/Documentation/git-filter-repo.txt) | "Use this flag to turn off updating commit hashes in commit messages." | 2026-10-12 | 2027-10-12 |
| `sdr-version` | GitHub's procedure for removing sensitive data needs git-filter-repo 2.47 or later, for `--sensitive-data-removal` | [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | "You need a version with the `--sensitive-data-removal` flag, meaning at least version 2.47." | 2026-10-12 | 2027-04-12 |
| `rewrite-signatures` | Rewriting history removes commit and tag signatures, so rewritten commits lose GitHub's Verified badge | [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | "will simply remove the signatures" | 2026-10-12 | 2027-04-12 |
| `pr-refs-readonly` | A push can't change or delete `refs/pull/*`, so old commits a pull request holds stay until GitHub Support removes them | [Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | "This command will fail to push any refs starting with `refs/pull/`, since GitHub marks those as read-only." | 2026-10-12 | 2027-04-12 |

## Sources

| Source | Used for | License |
|---|---|---|
| [GitHub Docs: removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | The procedure, its tool version, and what a rewrite can't reach | CC BY 4.0: facts in our own words, with short quotes |
| [git-filter-repo manual](https://raw.githubusercontent.com/newren/git-filter-repo/main/Documentation/git-filter-repo.txt) | `--mailmap` and `--preserve-commit-hashes` | MIT: facts with short quotes |
| One live history rewrite by this skill's owner, unnamed here | Counting first, the map, the rehearsal, the script, the support route | Observed practice, in our own words |
