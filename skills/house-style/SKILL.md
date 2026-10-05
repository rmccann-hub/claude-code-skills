---
name: house-style
description: Writes and checks prose and Markdown in one house style across every repository. That means the answer first, plain words, no filler or hype, facts with their sources and dates, American spelling, sentence-case headings, lines wrapped at 100 columns, and the same README sections everywhere. It ships HouseStyle, a Vale style each repository's CI loads from the latest release. Use when writing or reviewing a README, documentation, a decision record, a changelog entry, a pull request description, a report or any Markdown file, when choosing between British and American spelling, or when adding the prose check to a repository's CI. For commit subjects, branch names and changelog structure, use git-workflows. For a full audit of a repository, use project-bootstrap-and-audit.
license: Apache-2.0
metadata:
  reviewed: "2026-10-05"
---

# House style

One style for everything written in the owner's repositories: documentation, records, pull
requests, commit bodies and reports. It should be recognizable because it's plain, exact and
checked, not because of whose it is. In Claude Code, apply it as you write. On claude.ai, apply
it to the text you hand back.

Dated facts, such as Vale's version and what other guides say, live in
[references/facts.md](references/facts.md), and the other files name them by ID, such as fact
`vale-current`.

## The rules

**Voice**

1. Lead with the answer or the result. Reasons come after.
2. Plain, common words. One term for each thing, used everywhere.
3. No filler, hype or unearned hedging: no `just`, `simply`, `very`, `seamless`, `robust` or
   `leverage`.
4. Every fact is checked against its source. Anything that can go stale carries its source and
   date. Say plainly what wasn't checked.
5. Short sentences in the active voice, one idea each.
6. A rule says what breaks without it. A status says what's waiting, and on whom.
7. Write for a reader who wasn't there: no session detail, and no private shorthand.

**Format**

8. Markdown with sentence-case headings, `-` bullets, lines wrapped at 100 characters, code
   blocks marked with their language, and tables for comparisons.
9. Commands, paths and identifiers go in code formatting. File names are lowercase with hyphens,
   apart from the usual capitalized root files, such as `README.md`.
10. Every README has the same sections in the same order: what it is, install, usage,
    development, operations, security and license.
11. Commit subjects read "area: summary". Changelogs follow Keep a Changelog, and decisions go
    in one record, newest first.
12. American spelling throughout.
13. Code follows its language's own formatter and linter, which project-bootstrap-and-audit sets
    up.

**What the style leaves alone**

- **Files a fork shares with its upstream project** keep upstream's format. Reformatting them
  would make every merge from upstream conflict. The style covers what's yours: your documents,
  your commits and your new files.
- **Third-party files,** such as licenses and vendored code, stay exactly as they came.
- **Words quoted from a source** stay as the source wrote them, spelling included.
- **Past entries in an append-only record,** such as a decision record or a dated research
  result, stay as written. New entries follow the style.

## Check it

HouseStyle is a Vale style, kept in
[assets/vale/HouseStyle/](assets/vale/HouseStyle/.vale.ini) and published as `HouseStyle.zip`
on each release. It checks three of the rules:

| Rule | Vale rule | What it catches |
|---|---|---|
| 3 | `HouseStyle.Filler` | The six words, in any case |
| 8 | `HouseStyle.Headings` | A heading that isn't in sentence case, apart from listed proper nouns and the repository's own vocabulary |
| 12 | `HouseStyle.Spelling` | Common British spellings, with the American form to use |

The rest are for review. Vale can't tell whether the answer comes first, or whether a fact was
checked at its source. Rule 11's commit subjects have their own check, in git-workflows.

To run it: `vale sync`, then `vale` with the files to check. Setting it up in a repository's CI
takes a `.vale.ini` and one job, both in [references/setup.md](references/setup.md).

## Where to go

| When you're | Read |
|---|---|
| writing or reviewing Markdown: headings, lists, wrapping, code, tables, links, file names or a README's sections | [references/style.md](references/style.md) |
| choosing a word, or checking a spelling | [references/style.md](references/style.md) |
| adding the check to a repository, or running it locally | [references/setup.md](references/setup.md) |
| asking why a rule is what it is, what other guides do, or what a choice costs | [references/why.md](references/why.md) |
| checking a version, or what a source says | [references/facts.md](references/facts.md) |
| checking a source's license | [references/sources.md](references/sources.md) |

## What this doesn't cover

- **Commit subjects, branch names, pull requests and the changelog's structure:** use
  git-workflows.
- **How code is formatted:** each language's own formatter and linter, which
  project-bootstrap-and-audit sets up.
- **What goes in an agent's context file,** such as `AGENTS.md`: project-bootstrap-and-audit
  rules on that. The prose in it follows this style.
