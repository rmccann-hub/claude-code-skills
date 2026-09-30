# FFmpeg as a reference (2026-09-30)

The owner named FFmpeg as a model of open-source practice and asked what the standard should
learn from it: contributions, review, merging, branches, versions, naming, options, code and
documentation. This is a reading by this repository's session, not a research result. Every
row was read from FFmpeg's own tree, or measured from its history, on 2026-09-30.

- **Read:** `github.com/FFmpeg/FFmpeg`, a mirror, at master `18ee27e6` (committed
  2026-09-29) and `release/9.0` at `2a571b60`, in a partial clone. History figures come from
  master's last 3,004 commits (2026-04-16 to 2026-09-29) and `release/9.0`'s last 80.
- **Not read:** ffmpeg.org, the settings of FFmpeg's Forgejo, its mailing lists, and FATE's
  servers.
- **Licence:** FFmpeg is LGPL-2.1-or-later, with optional GPL parts. It is quoted here only in
  short phrases, as citation.

## What FFmpeg does

| Area | FFmpeg | Source |
|---|---|---|
| Where changes come in | Pull requests on its own Forgejo, or patches to the ffmpeg-devel list. GitHub pull requests "will be ignored" | `CONTRIBUTING.md` |
| CI | Forgejo Actions run the pre-commit hooks on every pull request and push to master, and FATE, its test suite, on three builds. Each first rebases the pull request onto its target | `.forgejo/workflows/lint.yml`, `test.yml`; `.forgejo/actions/rebase-pr/` |
| History | Linear: "The master tree will reject pushes with merge commits." 4 merges in 3,004 commits, all subtree merges of one vendored upstream | `doc/git-howto.texi`, Rebasing; measured |
| Commit subjects | "area changed: short 1 line description", then the why. 2,970 of 3,004 subjects follow it, at a median 57 characters. A commit-msg hook rejects any other shape, Conventional Commits' `feat:` and `fix:` included | `doc/developer.texi`, Commit messages; `tools/check_commit_msg.sh`; measured |
| Commit scope | Unrelated changes apart, cosmetic changes in their own commit, and a fix meant for backporting kept small. Every commit passes the test suite, not only the series | `doc/developer.texi`, Patches/Committing; `doc/git-howto.texi`, Pre-push checklist |
| Review | Every patch is reviewed, the author answers every comment, and a resubmission changes only what review asked. Without an answer, a push waits 12 hours for a build or security fix, 3 days for a small change and a week for a large one | `doc/developer.texi`, Patch review process and Always wait long enough |
| Reviewers | `MAINTAINERS` names who looks after each area, with a status from 2, "someone actually looks after it", through 1 and 0, "no current maintainer", to X, old code. `.forgejo/CODEOWNERS` names expected reviewers, who "don't own the code" | `MAINTAINERS`; `.forgejo/CODEOWNERS` |
| Contributors | 220 authors and 65 committers across the 3,004 commits; 960 were committed by someone other than their author | measured |
| Release lines | Branches named `release/X.Y`. A point release takes a security fix, a documented bug or documentation, and keeps source and binary compatibility. 78 of `release/9.0`'s last 80 commits are cherry-picks that name their source commit, made by a workflow that backports a labelled pull request | `doc/developer.texi`, Release process; `.forgejo/workflows/backports.yml`; measured |
| Tags | Annotated: `nX.Y.Z` for a release, and `nX.Y-dev` where master moves on after a branch. `ffbuild/version.sh` builds the version from `git describe` | `git ls-remote --tags`; `ffbuild/version.sh` |
| Interface versions | Each library has its own major.minor.micro, apart from the release number. The public API stays compatible within a major. A removal is deprecated first, guarded by an `FF_API_*` macro keyed to the major that removes it, and goes only at a scheduled bump. An addition bumps the minor. `doc/APIchanges` logs each change with its date, library version and header | `doc/developer.texi`, Library public interfaces; `doc/APIchanges` |
| User changelog | `Changelog`: a `version <next>:` list of features, newest release first | `Changelog` |
| Naming | snake_case functions and variables, CamelCase types, UPPERCASE macros and enum constants. `ff_` marks library-internal names, `avpriv_` cross-library internal ones, and each library has a public prefix | `doc/developer.texi`, Naming conventions |
| Options | `configure` takes `--enable-*` and `--disable-*`. The GPL parts are off unless `--enable-gpl` is passed, which turns the build's licence to GPL | `LICENSE.md`; `.forgejo/workflows/test.yml` |
| Licences | LGPL by default, with the GPL files listed by name. A new file gets its licence header from an existing file | `LICENSE.md`; `doc/developer.texi`, Licenses for patches |
| Robustness | A decoder or demuxer is tested against damaged data, and must not crash, loop or allocate without bound | `doc/developer.texi`, Patch submission checklist |
| Security reports | A private list and a web page, named in `MAINTAINERS`. There is no `SECURITY.md` in the tree | `MAINTAINERS`; the tree |
| Hooks | One pre-commit config installs a pre-commit and a commit-msg hook: whitespace, line endings, a byte-order mark, shebangs, case clashes, spelling and the commit message | `.forgejo/pre-commit/config.yaml` |
| Templates | A pull request asks for a summary and any new test samples. An issue asks for the exact command, samples and logs | `.forgejo/PULL_REQUEST_TEMPLATE.md`, `.forgejo/ISSUE_TEMPLATE.md` |

## Where a run of the standard would misjudge FFmpeg

1. **CI.** Phase 2 lists `.github/workflows/`, which FFmpeg's tree doesn't have, so a run
   would record no CI. FFmpeg's CI is in `.forgejo/workflows/`, and its GitHub repository is a
   mirror whose pull requests are ignored. The standard has a `MIRROR` status for a source of
   truth outside the repository, but nothing that finds the forge that is canonical. (F71)
2. **Security reports.** `SECURITY.md` is due at T3, and FFmpeg has none. Its private list and
   its page are named in `MAINTAINERS`. (F72)
3. **Commit grammar.** The standard names Conventional Commits as the commit grammar, in its
   standards table and dimension 10. FFmpeg's hook rejects Conventional Commits and requires
   "area: summary". Both are grammars. What matters is having one and checking it. (F73)
4. **Actions pinned by tag or branch.** FFmpeg pins `actions/checkout@v6` by tag and
   `actions/git-backporting@main` by branch, the second with a token secret on
   `pull_request_target`. The standard rates that `GAP`, and it is right to: whoever moves
   that branch runs with the secret. No change.
5. **A version file.** Master's `RELEASE` reads `8.0.git` beside tags up to `n9.1-dev`.
   Reconciliation would call that drift, while `version.sh` reads only whether it contains
   `git`. It can mislead a reader but not the build, which the standard's rule to check claims
   rather than files already covers. No change.

## Where FFmpeg and the standard agree

- Every commit on a branch passes on its own, not only the last.
- A mechanical reformat goes in its own commit.
- A hook that isn't installed enforces nothing, so CI runs the same checks.
- `CODEOWNERS` names reviewers, once there is more than one person to review.
- A pull request is tested as it would merge, on top of its base.

## What the owner's two live repositories show beside it

- **The first live repository:** 62 release tags, all lightweight, made by `gh release create`
  in its release workflow. Of its last 1,000 commits, 156 are merges, by its recorded choice,
  and 781 subjects follow Conventional Commits. Its median subject is 71 characters.
- **Its sibling, a fork:** no tags on its remote, though its build file names each release's
  version. Its subjects are sentences rather than "area: summary", as about three quarters of
  upstream's last 300 are.

## Proposals, approved on 2026-09-30

Each is written up in `ROADMAP.md` as F71 to F79, and v0.40.0 applies them.

- **F71:** find the canonical forge before reading CI and settings.
- **F72:** accept a security contact the repository names, where there is no `SECURITY.md`.
- **F73:** a commit grammar is stated and checked by a hook, and Conventional Commits is one
  choice among others.
- **F74:** the merge strategy is chosen, recorded and enforced, and squash is ruled out where
  commits are cited from outside.
- **F75:** release tags are annotated.
- **F76:** an interface others build on gets a change log and a deprecation before any removal.
- **F77:** where more than one release line is kept, backports name their source and a point
  release takes only compatible fixes.
- **F78:** code that parses input it doesn't control gets a damaged-input test.
- **F79:** where licences mix, each file names its own, and the licence file says which parts
  are which.

**Taken in at the owner's word, as F80:** a maintainers list, review before merging, review
waiting times, the `Signed-off-by` sign-off (on 1,928 of the 3,004 commits) and a shared
security contact. They are rated only where the human says more than one person maintains.

**Not proposed:** mailing-list review, which is one project's route, and naming prefixes by
visibility, which belong to a language's own conventions.
