# Setup: the house style's check in a repository

Read this when you add the house style's check to a repository, run it on your own machine, or
tune it for a repository's own names and records. Facts are named by ID from `facts.md`.

## Contents

- [What it takes](#what-it-takes)
- [The configuration](#the-configuration)
- [A repository's own names](#a-repositorys-own-names)
- [Files the style leaves alone](#files-the-style-leaves-alone)
- [The CI job](#the-ci-job)
- [Running it locally](#running-it-locally)
- [When a rule doesn't fit](#when-a-rule-doesnt-fit)

## What it takes

- **Vale,** the prose linter (facts `vale-current`, `vale-license`). It installs with
  `go install`, from its module (fact `vale-module`).
- **The HouseStyle package,** which each release of claude-code-skills publishes as
  `HouseStyle.zip`. Vale fetches a package by URL, and installs it with `vale sync` (fact
  `vale-packages`).
- **A `.vale.ini`** at the repository's root, and one CI job.

Naming the latest release's package means a change to the style reaches every repository at
its next CI run, with no change there. The price is that a new rule can fail a repository that
was passing yesterday. Each release's notes say what changed.

## The configuration

`.vale.ini`, at the repository's root:

```ini
StylesPath = .vale/styles
MinAlertLevel = suggestion
Packages = https://github.com/rmccann-hub/claude-code-skills/releases/latest/download/HouseStyle.zip
```

The package carries its own configuration, which runs HouseStyle on every Markdown file. The
repository's own configuration overrides it (fact `vale-layers`).

Add what `vale sync` installs to `.gitignore`, so it isn't committed:

```text
.vale/styles/HouseStyle/
.vale/styles/.vale-config/
```

## A repository's own names

The heading rule accepts common proper nouns, such as GitHub, Python and Keep a Changelog. It
leaves out Go, because "go" is also a verb. A repository adds its own names to a vocabulary,
which the heading and spelling rules both accept (fact `vale-exceptions`):

1. Put one name per line in `.vale/styles/config/vocabularies/Repository/accept.txt`, and
   commit it.
2. Add `Vocab = Repository` to `.vale.ini`, above the first section.

## Files the style leaves alone

A later section of `.vale.ini` replaces an earlier section's styles (fact `vale-sections`), so
an empty list turns the style off for the files it matches:

```ini
[*.md]
BasedOnStyles = HouseStyle

# Append-only records keep their past entries as written.
[docs/decisions.md]
BasedOnStyles =
```

Leave these alone:

- an append-only record's history, such as a decision record or dated research results;
- files a fork shares with its upstream project;
- third-party files, such as vendored code and other projects' licenses.

Where a file quotes its sources in double quotes, such as a facts table, skip the quotes and
check the rest:

```ini
[references/facts.md]
TokenIgnores = "(?:[^"\\]|\\.)*"
```

## The CI job

Copy [assets/workflows/prose.yml](../assets/workflows/prose.yml) into the repository's
`.github/workflows/`. It's tested, and claude-code-skills runs the same file on itself. Its steps:

1. **Install Vale** at a pinned version. `go install` checks the module's checksums against Go's
   checksum database.
2. **Fetch the style** with `vale sync`, from the package `.vale.ini` names.
3. **Prove the style catches each kind of mistake.** It checks a canary file written outside the
   repository, with a Title Case heading, a filler word and a British spelling, and fails unless
   all three rules report. A check that measures nothing can't pass.
4. **Check every tracked Markdown file.** The files to leave alone are set in `.vale.ini`, not
   in the workflow, so a person running `vale` locally gets the same answer as CI.

The workflow runs on every push and pull request, with no path filter, so it can be a required
check. Its action pins go stale like any other. In claude-code-skills, Dependabot moves the copy
it runs, and the asset follows.

## Running it locally

```sh
go install github.com/vale-cli/vale/v3/cmd/vale@v3.24.0
vale sync
git ls-files -z '*.md' | xargs -0 vale
```

Vale is also packaged for Homebrew, Chocolatey and others. Any install of the same version gives
the same answer. A build from `go install` reports its version as `master`, and
`go version -m "$(command -v vale)"` shows the version it was built from.

## When a rule doesn't fit

- **A proper noun is flagged:** add it to the repository's vocabulary.
- **A quote is flagged:** put it in double quotes in a file that skips quotes, or in a block
  quote, and say where it's from.
- **A rule is wrong for the repository:** set it to a warning in `.vale.ini`, under the files'
  section, such as `HouseStyle.Headings = warning`. Record why in the decision record, and tell
  claude-code-skills, because a rule that's wrong in one repository may be wrong in all of them.
