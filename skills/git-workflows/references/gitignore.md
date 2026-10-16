# The `.gitignore` file

Read this for writing or debugging a `.gitignore`, finding which rule ignores a file, ignoring
secret files, deciding whether to commit a lockfile, or untracking a file that's already
committed.

It covers what Git tracks. A secret that was already committed is `leaked-data`.

## Rules

1. **Start from GitHub's template for your language,** and cut what doesn't apply.
2. **A comment goes on its own line,** and a file can't be re-included under an excluded
   directory.
3. **Commit the lockfile, never ignore it.**
4. **Ignore secret files,** and commit an example file without the values.
5. **Your own editor and OS files go in your global excludes file,** not the project's.

### Writing `.gitignore`

- **Start from GitHub's template** (github/gitignore, CC0; fact `gitignore-templates`).
- **A comment goes on its own line.** `#` starts a comment only at the start of a line (fact
  `gitignore-comment`). `*.frx  # binary form data` is one pattern, "`*.frx  # binary form
  data`", and it matches nothing.
- **A file can't be re-included under an excluded directory** (fact `gitignore-parent`).
  `.vscode/` followed by `!.vscode/extensions.json` keeps nothing. Write `.vscode/*`, then the
  `!` line.
- **Commit the lockfile.** For Rust, commit `Cargo.lock` for libraries too, as the starting
  point: the Cargo team dropped its old advice against it (fact `cargo-lock`).
- **Ignore secret files** such as `.env` and `.env.*`, and commit a `.env.example`. A secret that
  was already committed is rotated first: removing it from the tree doesn't take it back.
- **Your own editor and OS files** go in your global excludes file (`core.excludesFile`), not the
  project's `.gitignore`.

### Debugging and untracking

- **To find the rule that matched:** `git check-ignore -v <path>`. `git status --ignored` lists
  the ignored files.
- **To stop tracking a file,** `git rm --cached <path>`: it leaves your copy on disk (fact
  `rm-cached`), and the file stays in history. Everyone else who pulls that commit has the file
  deleted, because to their clone it's a tracked file being removed. Tell them to copy it
  first.

## Mistakes

- **Comments after a pattern in `.gitignore`,** which become part of the pattern (fact
  `gitignore-comment`).
- **`!` re-including a file under an ignored directory,** which keeps nothing (fact
  `gitignore-parent`).
- **Ignoring `Cargo.lock` in a library,** which was the old advice (fact `cargo-lock`).
- **`git rm --cached` on a file others have,** such as a shared config. Their next pull
  deletes it from their working tree. Warn them first.
- **Adding a file to `.gitignore` and expecting Git to stop tracking it.** Ignore rules apply
  only to untracked files. Untrack it with `git rm --cached`.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| `.gitignore` lines that do nothing | Inline `#` comments, or `!` under an ignored directory: test with `git check-ignore -v` | `DRIFT` | Facts `gitignore-comment`, `gitignore-parent` |
| The lockfile is ignored | `git check-ignore -v` on `uv.lock`, `package-lock.json`, `Cargo.lock` or the ecosystem's own | `GAP`: installs can't be reproduced | Remove the rule, and commit the lockfile (fact `cargo-lock`) |

## Why

### Comments and re-includes

**The advice.** Put each comment on its own line, and re-include a file under an ignored
directory by ignoring the directory's contents, not the directory.

**Why.** Both mistakes fail silently. A trailing comment turns the pattern into one that matches
nothing (fact `gitignore-comment`), and a `!` under an excluded directory is never read, because
Git doesn't look inside a directory it excludes (fact `gitignore-parent`). Nothing warns, so the
file is tracked, or not, against the author's intent.

### Committing the lockfile

**The advice.** Commit the lockfile, libraries included.

**Why.** Without it, each install resolves versions afresh, so CI and every clone test code
nobody reviewed. The Cargo team dropped its advice against committing `Cargo.lock` for libraries
(fact `cargo-lock`).

**What each choice costs.** A committed lockfile needs updates, which a bot such as Dependabot
raises. An ignored one costs nothing until a new release of a dependency breaks the build.

**When to choose differently.** Where a library's own CI must also test against the newest
versions its ranges allow, add a job that resolves them fresh, and keep the lockfile.

## Facts

Versions, dates and defaults, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `gitignore-comment` | In `.gitignore`, `#` starts a comment only at the start of a line, and trailing spaces are dropped | [gitignore](https://git-scm.com/docs/gitignore) | "A line starting with # serves as a comment." | 2026-09-30 | 2027-09-30 |
| `gitignore-parent` | A file can't be re-included once a parent directory is excluded | [gitignore](https://git-scm.com/docs/gitignore) | "It is not possible to re-include a file if a parent directory of that file is excluded." | 2026-09-30 | 2027-09-30 |
| `gitignore-templates` | GitHub's gitignore templates are CC0 1.0 | [github/gitignore LICENSE](https://raw.githubusercontent.com/github/gitignore/main/LICENSE) | "CC0 1.0 Universal" | 2026-09-30 | 2027-09-30 |
| `cargo-lock` | The Cargo team dropped its advice not to commit `Cargo.lock` for libraries, and now suggests committing it as the starting point | [Rust blog, 2023-08-29](https://blog.rust-lang.org/2023/08/29/committing-lockfiles/) | "We now recommend people do what is best for their project." | 2026-09-30 | 2027-09-30 |
| `rm-cached` | `git rm --cached` removes a path from the index and leaves the working tree's copy | [git-rm](https://git-scm.com/docs/git-rm) | "Use this option to unstage and remove paths only from the index. Working tree files, whether modified or not, will be left alone." | 2026-09-30 | 2027-09-30 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Git documentation](https://git-scm.com/docs) (gitignore, git-rm, git-check-ignore) | Ignore rules and untracking | GPL-2.0: facts in our own words, with short quotes |
| [github/gitignore](https://github.com/github/gitignore) | Starting templates | CC0 1.0: pointed to, not copied |
| [Rust blog, 2023-08-29](https://blog.rust-lang.org/2023/08/29/committing-lockfiles/) | Committing `Cargo.lock` | MIT or Apache-2.0: a fact with a short quote |
