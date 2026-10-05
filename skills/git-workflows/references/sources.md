# Sources

Read this when you need to know where a rule comes from, or whether a source may be quoted or
adapted. The dated facts, with their quotes, are in `facts.md`. Everything here was read on
2026-09-30.

## Primary sources

| Source | What it's used for | License | How it's used here |
|---|---|---|---|
| [Git documentation](https://git-scm.com/docs) (git-branch, git-checkout, git-cherry-pick, git-commit, git-describe, git-interpret-trailers, git-push, git-reflog, git-rerere, git-rm, git-tag, githooks, gitignore, BreakingChanges, SubmittingPatches), and Git's [maintainer howto](https://raw.githubusercontent.com/git/git/master/Documentation/howto/maintain-git.adoc) | Commands, trailers, hooks, ignore rules, commit messages, Git's own branches | GPL-2.0 | Facts in our own words, with short quotes |
| [GitHub Docs](https://docs.github.com/) (workflow syntax, events, conditions, concurrency, caching, limits, triggering a workflow, disabling workflows, security hardening, protected branches, merge methods, squashing, merge queues, automatic branch deletion, checking out pull requests, immutable releases, linking issues, co-authors, Dependabot options, GitHub flow) | GitHub Actions and repository settings | CC BY 4.0 | Facts in our own words, with short quotes |
| [GitHub changelog](https://github.blog/changelog/) (2025-08-15, 2025-09-19, 2025-11-07, 2026-06-18, 2026-09-17) | Dated platform changes | © GitHub; short quotes only | Facts with short quotes |
| [actions/checkout README](https://github.com/actions/checkout) | Credentials and the bot identity | MIT | Facts with short quotes |
| [actions/starter-workflows](https://github.com/actions/starter-workflows) | How GitHub pins actions in its own templates | MIT | A fact with short quotes |
| [gh manual](https://cli.github.com/manual/gh_release_create) | The tag `gh release create` makes | MIT | A fact with a short quote |
| [CVE-2025-30066](https://cveawg.mitre.org/api/cve/CVE-2025-30066) | The moved tags of `tj-actions/changed-files` | CVE's terms of use | A fact with a short quote |
| [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) | One commit grammar | CC BY 3.0 | Summarized, with attribution |
| [Semantic Versioning 2.0.0](https://semver.org/) | Version numbers | CC BY 3.0 | Summarized, with attribution |
| [Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/) | Changelog format and guidance | MIT | Summarized |
| [DORA: trunk-based development](https://dora.dev/capabilities/trunk-based-development/) | Branching evidence | Not stated | A short quote, with the link |
| [github/gitignore](https://github.com/github/gitignore) | Starting templates | CC0 1.0 | Pointed to, not copied |
| [uv CLI reference](https://docs.astral.sh/uv/reference/cli/) | `--locked` against `--frozen` | MIT or Apache-2.0 (uv's own license) | A fact with a short quote |
| [Rust blog, 2023-08-29](https://blog.rust-lang.org/2023/08/29/committing-lockfiles/) | Committing `Cargo.lock` | MIT or Apache-2.0 | A fact with a short quote |
| PyPI pages for [pre-commit](https://pypi.org/project/pre-commit/), [prek](https://pypi.org/project/prek/) and [zizmor](https://pypi.org/project/zizmor/); tags of [actionlint](https://github.com/rhysd/actionlint) | Tool versions | MIT (all four) | Versions only |

## What other projects do

Each is a fact in `facts.md`, checked again like any other, because a project can change its
practice. Where a page states no license, only short quotes are used.

| Source | What it's used for | License |
|---|---|---|
| [Linux kernel documentation](https://docs.kernel.org/) (rebasing and merging, submitting patches, stable kernel rules) | Merges, subject lines, stable backports | Not stated on the pages |
| [CPython devguide](https://devguide.python.org/getting-started/pull-request-lifecycle/) | Squash merges, and review without force-pushes | Not stated on the page |
| [rustc-dev-guide: CI](https://rustc-dev-guide.rust-lang.org/tests/ci.html) | The merge queue, rollups and pull request builds | MIT or Apache-2.0 |
| [Go contribution guide](https://go.dev/doc/contribute) | Package-prefixed subjects, Gerrit's `Change-Id` | Not stated on the page |
| [LLVM Developer Policy](https://llvm.org/docs/DeveloperPolicy.html) | Area tags, and reverting first | Not stated on the page |
| [Software Engineering at Google, chapter 23](https://abseil.io/resources/swe-book/html/ch23.html) | Presubmit and post-submit tests, flake classification | CC BY-NC-ND 4.0: quoted, never adapted |
| [Chromium CQ](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/infra/cq.md) | What runs before a change lands | Not stated on the page |
| [Prow jobs](https://docs.prow.k8s.io/docs/jobs/) | Kubernetes' presubmit, postsubmit and periodic jobs | Apache-2.0 |
| [Martin Fowler, Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) | The ten-minute build, and staged builds | © Martin Fowler: quoted, never adapted |
| [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) | Git Flow's author's own advice | CC BY-SA |
| [towncrier](https://towncrier.readthedocs.io/en/stable/), [pip's release process](https://pip.pypa.io/en/stable/development/release-process/), [semantic-release](https://github.com/semantic-release/semantic-release) | Changelog fragments, calendar versions, versions from commits | Not stated on the pages |

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
- A cold review by a second reader on 2026-09-30, whose findings were each checked against the
  files and the standard before they were fixed.
