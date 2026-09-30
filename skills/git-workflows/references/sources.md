# Sources

Read this when you need to know where a rule comes from, or whether a source may be quoted or
adapted. The dated facts, with their quotes, are in `facts.md`. Everything here was read on
2026-09-30.

## Primary sources

| Source | What it's used for | Licence | How it's used here |
|---|---|---|---|
| [Git documentation](https://git-scm.com/docs) (git-branch, git-cherry-pick, git-commit, git-describe, git-interpret-trailers, git-tag, githooks, gitignore, BreakingChanges, SubmittingPatches) | Commands, trailers, hooks, ignore rules, commit-message guidance | GPL-2.0 | Facts in our own words, with short quotes |
| [GitHub Docs](https://docs.github.com/) (workflow syntax, triggering a workflow, disabling workflows, security hardening, merge methods, merge queues, immutable releases, linking issues, co-authors) | GitHub Actions and repository settings | CC BY 4.0 | Facts in our own words, with short quotes |
| [GitHub changelog](https://github.blog/changelog/) (2025-08-15, 2025-09-19, 2025-11-07, 2026-06-18, 2026-09-17) | Dated platform changes | © GitHub; short quotes only | Facts with short quotes |
| [actions/checkout README](https://github.com/actions/checkout) | Credentials and the bot identity | MIT | Facts with short quotes |
| [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) | One commit grammar | CC BY 3.0 | Summarised, with attribution |
| [Semantic Versioning 2.0.0](https://semver.org/) | Version numbers | CC BY 3.0 | Summarised, with attribution |
| [Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/) | Changelog format and guidance | MIT | Summarised |
| [DORA: trunk-based development](https://dora.dev/capabilities/trunk-based-development/) | Branching evidence | Not stated | A short quote, with the link |
| [github/gitignore](https://github.com/github/gitignore) | Starting templates | CC0 1.0 | Pointed to, not copied |
| [uv CLI reference](https://docs.astral.sh/uv/reference/cli/) | `--locked` against `--frozen` | MIT or Apache-2.0 (uv's own licence) | A fact with a short quote |
| [Rust blog, 2023-08-29](https://blog.rust-lang.org/2023/08/29/committing-lockfiles/) | Committing `Cargo.lock` | MIT or Apache-2.0 | A fact with a short quote |
| PyPI pages for [pre-commit](https://pypi.org/project/pre-commit/), [prek](https://pypi.org/project/prek/) and [zizmor](https://pypi.org/project/zizmor/); tags of [actionlint](https://github.com/rhysd/actionlint) | Tool versions | MIT (all four) | Versions only |

## Practice observed in projects

- **FFmpeg**, read from its own tree and history on 2026-09-30: its "area: summary" commit
  grammar and the check that enforces it, `Fixes:` and `Found-by:` trailers, cherry-picks with
  `-x` on `release/9.0`, its backport automation, and its developer guide's rule that backports
  stay focused. Facts about the project, stated in our own words.
- **Two live repositories of this skill's owner,** unnamed here: squash merges that stranded
  cited commits, a branch deleted four minutes after a squash merge, hooks that never ran in
  cloud sessions, and pinned tools installed from another range.

## What this skill was built from

- The owner's earlier `git-workflows` skill, as a list of topics, checks and lessons. Nothing
  was copied from it. Where it advised against a lesson listed above, such as squash-merging
  feature branches, bulk-deleting merged branches, `--no-verify` or a status section in
  `CLAUDE.md`, the advice was dropped.
- Research runs R08 (Git, GitHub, CI/CD) and R05 (versioning, releases), filed in this skill's
  repository. They were leads until each claim was checked. Two were out of date when checked:
  Git 2.56.0 had replaced 2.55.0, and Keep a Changelog 2.0.0 had replaced 1.1.0.
