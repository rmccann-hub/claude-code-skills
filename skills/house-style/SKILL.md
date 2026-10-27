---
name: house-style
description: "Writes and checks prose and Markdown in one house style: the answer first, plain words, facts with sources, American spelling. Ships a Vale style. Use for a README, docs, records, changelogs, pull requests and reports."
license: Apache-2.0
metadata:
  reviewed: "2026-10-16"
---

# House style

One style for everything written in the owner's repositories: documentation, records, pull
requests, commit bodies and reports. It should be recognizable because it's plain, exact and
checked, not because of whose it is. In Claude Code, apply it as you write. On claude.ai, apply
it to the text you hand back.

## What applies to every module

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
11. Commit subjects follow the grammar the repository records, and "area: summary" where it
    records none. Changelogs follow Keep a Changelog. Decisions go in one append-only record,
    newest first; an existing record that runs oldest first keeps its order, and says so at its
    top.
12. American spelling throughout. A label or value the code defines is written as the code
    spells it, in code formatting; in the project's own code, fix the spelling there first.
13. Code follows its language's own formatter and linter, which project-bootstrap-and-audit sets
    up.

**What the style leaves alone**

- **Files kept byte for byte the same as another repository's,** such as those a fork shares
  with its upstream project, or a file two repositories keep identical, keep the format they
  share. Reformatting one copy makes every merge or sync conflict. The style covers what's
  yours: your documents, your commits, your new files, and your own block inside a shared file,
  such as a fork's section of upstream's README. A section a rule requires, such as rule 10's,
  goes inside that block, not over upstream's structure. A file the fork now writes alone, such
  as a changelog upstream started, is the fork's own: its past entries stay, as below.
- **Third-party files,** such as licenses and vendored code, stay exactly as they came.
- **Words quoted from a source** stay as the source wrote them, spelling included.
- **Past entries in an append-only record,** such as a decision record or a dated research
  result, stay as written, in their order. New entries follow the style.
- **Generated text,** such as a README section a script builds from another file, is fixed at
  its source and generated again. A comment marks where the output starts and ends, and names
  what writes it.

HouseStyle, a Vale style shipped in [assets/vale/HouseStyle/](assets/vale/HouseStyle/.vale.ini),
checks rules 3, 8 and 12, and skips words in double quotes. The rest are for review.

## Modules

Read the module that fits the request, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources. A module names a fact by its ID, such
as fact `vale-current`, and the fact's row is in whichever module holds it.

| Module | Read it for |
|---|---|
| [`writing-style`](references/writing-style.md) | writing or reviewing prose or Markdown: headings, lists, wrapping, code, tables, links, file names, a README's sections, word choice and spelling, and why each rule is what it is |
| [`prose-check`](references/prose-check.md) | adding the Vale check to a repository, running it locally, tuning it for a repository's own names and records, or a rule that flags something it shouldn't |

## What this doesn't cover

- **Commit subjects, branch names, pull requests and the changelog's structure:** use
  git-workflows.
- **How code is formatted:** each language's own formatter and linter, which
  project-bootstrap-and-audit sets up.
- **What goes in an agent's context file,** such as `AGENTS.md`: project-bootstrap-and-audit
  rules on that. The prose in it follows this style.

## When something here is wrong

If the person says advice here is wrong, out of date, failed or doesn't fit, answer their
problem first. Then say in one sentence whether the fault looks like this skill's, and why: a
fact past its check-by date, an example that fails, two rules that disagree, or a case the skill
doesn't cover. If the fault is elsewhere, such as their setup, say that instead.

When the fault is the skill's own, draft a full report they can paste as a new issue at
https://github.com/rmccann-hub/claude-code-skills/issues.
Give the skill and module, the plugin's version or the skill's date in its frontmatter, their
request word for word, the line of the skill that misled, what happened, what's right with its
source, and the fix you'd suggest. Leave out their private data, company detail and repository
names. File it only if they ask you to.
