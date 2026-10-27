# Prose check

Read this for adding the house style's Vale check to a repository, running it locally, tuning it
for a repository's own names and records, or a rule that flags something it shouldn't.

It covers the check, which finds breaks of rules 3, 8 and 12 in this skill's `SKILL.md`. What
the rules mean, and the rest of them, is `writing-style`.

## Rules

1. **Check the prose in CI** with Vale and the HouseStyle package, named by URL from the latest
   release.
2. **Prove the check catches each kind of mistake** before trusting it to pass.
3. **Set the files to leave alone in `.vale.ini`,** not in the workflow, so a local run and CI
   agree.
4. **Fix a flagged proper noun in the vocabulary,** and a wrong rule in the package, not by
   switching the check off.

HouseStyle is kept in [assets/vale/HouseStyle/](../assets/vale/HouseStyle/.vale.ini) and
published as `HouseStyle.zip` on each release. It checks three of the rules:

| Rule | Vale rule | What it catches |
|---|---|---|
| 3 | `HouseStyle.Filler` | The six words, in any case |
| 8 | `HouseStyle.Headings` | A heading that isn't in sentence case, apart from listed proper nouns and the repository's own vocabulary. A capital may follow a colon (fact `heading-colon`), but not a dash, by this style's choice |
| 12 | `HouseStyle.Spelling` | Common British spellings, with the American form to use |

The spelling rule lists the words it changes, most by a pattern: -ise and -isation to -ize and
-ization (organize, organization, recognize); -our to -or (behavior, color, favor); -re to -er
(center); -ogue to -og (catalog); -ence to -ense in some nouns (license, defense, offense); a
doubled `l` to one before -ed and -ing (labeled, canceled, modeling); and -ement after -dg to
-ment (judgment, acknowledgment). So it leaves alone -ise words the same in both, such as
advise, exercise, promise, otherwise and expertise.

Rule 8's wrap has its own check, below. The rest are for review: Vale can't tell whether the
answer comes first, or whether a fact was checked. Rule 11's commit subjects have their own
check, in git-workflows.

### What it takes

- **Vale,** the prose linter (facts `vale-current`, `vale-license`). It installs with
  `go install`, from its module (fact `vale-module`).
- **The HouseStyle package,** which each release of claude-code-skills publishes as
  `HouseStyle.zip`. Vale fetches a package by URL, and installs it with `vale sync` (fact
  `vale-packages`).
- **A `.vale.ini`** at the repository's root, and one CI job.

Naming the latest release's package brings a change to the style to every repository's next CI
run, with no change there. Each release's notes say what changed.

### The configuration

`.vale.ini`, at the repository's root:

```ini
StylesPath = .vale/styles
MinAlertLevel = suggestion
Packages = https://github.com/rmccann-hub/claude-code-skills/releases/latest/download/HouseStyle.zip
```

The package's own configuration runs HouseStyle on every Markdown file and skips words in
double quotes. The repository's configuration overrides its settings (fact `vale-layers`) and
adds to its lists.

Add what `vale sync` installs to `.gitignore`, so it isn't committed:

```text
.vale/styles/HouseStyle/
.vale/styles/.vale-config/
```

### A repository's own names

The heading rule accepts common proper nouns, such as GitHub, Python and Keep a Changelog. It
leaves out Go, because "go" is also a verb. A repository adds its own names to a vocabulary,
which the heading and spelling rules both accept (fact `vale-exceptions`):

1. Put one name per line in `.vale/styles/config/vocabularies/Repository/accept.txt`, and
   commit it.
2. Add `Vocab = Repository` to `.vale.ini`, above the first section.

### Files the style leaves alone

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
- files kept byte for byte the same as another repository's, such as a fork's upstream files;
- third-party files, such as vendored code and other projects' licenses.

### Quoted words

The package's `TokenIgnores` skips words in double quotes (fact `vale-tokenignores`). A quote
opens only after a space, a line's start or punctuation, so `5"` or a `"` after a backtick
opens none. It may wrap, but stops at its paragraph's end and at a line opening a list item,
heading, block quote, table row or code fence. Two cases still hide the words up to the
paragraph's next `"`: a stray `"` after a space, such as `5 "`, and one after a space inside
inline code, such as `` `a "b` ``. Typographic quotes aren't skipped.

A repository's own `TokenIgnores` adds to the package's (fact `vale-list-keys`), so it names
only its own markup:

```ini
[docs/*.md]
TokenIgnores = (:[a-z_]+:)
```

### The CI job

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

It runs on each pull request and each push to `main` (or the default branch's own name), with
no path filter, so it can be a required check. A branch with no pull request gets no run. Its
action pins go stale like any other; in claude-code-skills, Dependabot moves the copy it runs,
and the asset follows.

### Running it locally

```sh
go install github.com/vale-cli/vale/v3/cmd/vale@v3.24.0
vale sync
git ls-files -z '*.md' | xargs -0 vale
```

Vale is also packaged for Homebrew, Chocolatey and others. Any install of the same version gives
the same answer. A build from `go install` reports its version as `master`, and
`go version -m "$(command -v vale)"` shows the version it was built from.

### The wrap check

[scripts/wrap-check.sh](../scripts/wrap-check.sh), tested, names each line over 100
characters (fact `awk-length`), skipping frontmatter, fenced code, tables and URLs, and fails
if it finds one. With `HOUSE_STYLE` set to this skill's directory:

```sh
git ls-files -z '*.md' | xargs -0 sh "$HOUSE_STYLE/scripts/wrap-check.sh"
```

### When a rule doesn't fit

- **A proper noun is flagged:** add it to the repository's vocabulary.
- **A quote is flagged:** put it in double quotes, and say where it's from. A block quote is
  checked like any prose. A label or value from code goes in code formatting.
- **A rule is wrong for the repository:** set it to a warning in `.vale.ini`, under the files'
  section, such as `HouseStyle.Headings = warning`. Record why in the decision record, and tell
  claude-code-skills, because a rule that's wrong in one repository may be wrong in all of them.

## Mistakes

- **Pinning the package to a release and never moving the pin.** Fixes to the style never
  arrive. Name the latest release, and read its notes when a run fails.
- **Skipping files in the workflow's command line.** A local `vale` run then disagrees with CI.
  Skip them in `.vale.ini`.
- **A path filter on the prose job.** It can't then be a required check, because a pull request
  that skips it never merges.
- **Trusting a pass without the canary.** A job whose style failed to install checks nothing,
  and passes.
- **Turning a rule off for one flagged word.** Add the word to the vocabulary instead, so the
  rule still catches the rest.
- **Committing what `vale sync` installs.** It's fetched each run; ignore it.
- **Quoting your own words to quiet the check.** Fix the text instead.

## Audit

Severity uses the standard's status words: `BLOCKER`, `DRIFT`, `GAP`, `OVER`, `MIRROR`,
`UNVERIFIABLE-HERE`, `OK` and `N/A`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| No prose check | A workflow running `vale` on the tracked Markdown | `GAP` where the repository is meant to follow the house style | Copy `assets/workflows/prose.yml`, and add `.vale.ini` |
| The check measures nothing | The workflow's canary step, which fails unless all three rules report | `BLOCKER` where the job can pass with no style installed | Restore the canary step from the shipped workflow |
| The job is path-filtered | The workflow's `on:` block | `GAP`: it can't be a required check | Remove the filter |
| Records are checked | `.vale.ini` sections for append-only records and third-party files | `DRIFT`: past entries get flagged, and someone rewrites them | Add an empty `BasedOnStyles =` section for each |
| A quote pattern of the repository's own | A `TokenIgnores` in `.vale.ini` matching double quotes | `DRIFT`: one crossing a blank line hides prose after a stray mark | Remove it; the package skips quotes |
| What `vale sync` installs is committed | `git ls-files .vale/styles/HouseStyle` | `DRIFT` | Remove it, and ignore it |
| Vale's version is behind | The workflow's pinned version, against fact `vale-current` | `DRIFT` | Move the pin, and the version in the local install command |

## Why

### Checking it with Vale

**The advice.** Check the prose in CI with Vale and the HouseStyle package, named by URL from the
latest release.

**Why.** Vale is a common prose linter, MIT-licensed (fact `vale-license`), and it installs
packages by URL (fact `vale-packages`). So one change here reaches every repository's next run,
with no copies to keep in step.

**What others do.** markdownlint checks Markdown's structure, not its words. A check written into
this repository's own tooling would only run here.

**What each choice costs.**

| Choice | Gains | Costs |
|---|---|---|
| Vale, with the package by URL | One style, checked the same way in every repository, updated in one place | A Go install in each CI run, about a minute. A new rule can fail a repository that passed yesterday |
| Vale, with the package pinned to a release | No surprise failures | Each repository has to move its pin to get a fix |
| No check | Nothing to install | The style drifts, and nobody notices |

**What could be better.** The heading rule's list of proper nouns is a guess at what's common.
Each repository adds its own to its vocabulary, and names that recur belong in the package.

### Skipping quoted words

**The advice.** The package skips words in double quotes, within one paragraph.

**Why.** The style leaves a source's words as written, so flagging them is wrong, and a fix per
file, in each repository, is one more thing to miss.

**What it costs.** A writer can hide a word by quoting it, which review has to catch. A stray
mark hides little, since a quote opens only where one can and stops at its paragraph, a list,
a table or code. A quote wrapped onto such a line is checked: the safe way to be wrong. The
pattern sees text, not Markdown, so the two cases under *Quoted words* remain.

**When to choose differently.** A repository's own patterns only add (fact `vale-list-keys`),
so one that wants its quotes checked asks here for a change.

## Facts

Vale's version and behavior, and the guides the heading rule follows, each named by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `vale-current` | Vale's newest release is v3.24.0 | `git ls-remote --tags https://github.com/vale-cli/vale` | `refs/tags/v3.24.0` | 2026-10-05 | 2027-01-05 |
| `vale-module` | Vale installs with `go install`, from the module `github.com/vale-cli/vale/v3` | [go.mod at v3.24.0](https://raw.githubusercontent.com/vale-cli/vale/v3.24.0/go.mod) | "module github.com/vale-cli/vale/v3" | 2026-10-05 | 2027-04-05 |
| `vale-license` | Vale is under the MIT license | [LICENSE at v3.24.0](https://raw.githubusercontent.com/vale-cli/vale/v3.24.0/LICENSE) | "MIT License" | 2026-10-05 | 2027-04-05 |
| `vale-packages` | A package is a ZIP holding one folder named for it. `.vale.ini` lists it by URL under `Packages`, and `vale sync` installs it | [Packages](https://vale.sh/docs/keys/packages) | "A URL to a .zip archive." and "the archive has to hold one folder with that name" and "Packages lists what vale sync installs into the StylesPath" | 2026-10-05 | 2027-04-05 |
| `vale-layers` | A package's configuration is overridden by later packages, and by the project's own | [Packages](https://vale.sh/docs/keys/packages) | "the first package is overridden by the second, and local configuration overrides both" | 2026-10-05 | 2027-04-05 |
| `vale-sections` | In `.vale.ini`, a later section matching the same files replaces the earlier list of styles | [.vale.ini](https://vale.sh/docs/vale-ini) | "A later matching section replaces the list rather than adding to it." | 2026-10-05 | 2027-04-05 |
| `vale-tokenignores` | Vale skips a `TokenIgnores` match by wrapping it as inline code | [TokenIgnores](https://docs.vale.sh/keys/tokenignores) | "They work by wrapping each match in the format's inline code delimiter" | 2026-10-27 | 2027-04-27 |
| `vale-list-keys` | A list key, such as `TokenIgnores`, gathers every configuration file's values, as `vale ls-config` showed on Vale 3.25.1 | [.vale.ini](https://docs.vale.sh/topics/.vale.ini) | "A list key gathers every value from every file" | 2026-10-27 | 2027-04-27 |
| `heading-colon` | Google and Microsoft capitalize after a heading's colon. Google puts a colon, not a dash, after a label; Microsoft's em dash sets off a remark | [Google](https://developers.google.com/style/capitalization), [dashes](https://developers.google.com/style/dashes); [Microsoft](https://learn.microsoft.com/en-us/style-guide/capitalization), [dashes](https://learn.microsoft.com/en-us/style-guide/punctuation/dashes-hyphens/emes) | "the first word in a subheading after a colon" and "Appendix A: My first appendix" and "If a title or heading includes a colon, capitalize the first word after it." and "parenthetical remark that you want to add within a sentence" | 2026-10-27 | 2027-04-27 |
| `awk-length` | awk's `length` counts characters, and in the POSIX locale each is one byte | [awk](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/awk.html), [locale](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap06.html) | "return the length, in characters, of arg taken as a string" and "The POSIX locale shall contain 256 single-byte characters" | 2026-10-27 | 2027-10-27 |
| `vale-exceptions` | Capitalization and substitution rules take a list of exceptions, and accept the project's vocabularies unless told not to | [capitalization](https://vale.sh/docs/checks/capitalization) | "An array of strings to be ignored." and "If false, disables all active vocabularies for this rule (default: true)." | 2026-10-05 | 2027-04-05 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Vale's documentation](https://docs.vale.sh) | How packages, configuration, rule exceptions and `TokenIgnores` work | No license stated: facts with short quotes |
| [POSIX](https://pubs.opengroup.org/onlinepubs/9799919799/) | How awk counts a line's length | Facts with short quotes |
| Google's and Microsoft's style guides | Colons and dashes in headings | As in `writing-style`: short quotes, attributed |
| [Vale](https://github.com/vale-cli/vale) | The checker | MIT (fact `vale-license`): run as a tool, nothing copied from it |

The HouseStyle package's rules are original to this skill.
