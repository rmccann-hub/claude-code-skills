# Style: Markdown, words and spelling

Read this when you write or review a Markdown file, choose a word, or check a spelling. The rules
are numbered as in `SKILL.md`. Facts are named by ID from `facts.md`.

## Contents

- [Headings](#headings)
- [Paragraphs and line length](#paragraphs-and-line-length)
- [Lists](#lists)
- [Code](#code)
- [Tables](#tables)
- [Links and emphasis](#links-and-emphasis)
- [File names](#file-names)
- [A README's sections](#a-readmes-sections)
- [Words to cut, and what to use instead](#words-to-cut-and-what-to-use-instead)
- [Plain words](#plain-words)
- [American spelling](#american-spelling)
- [Records and dates](#records-and-dates)

## Headings

- **Sentence case:** capitalize the first word and proper nouns, nothing else (facts
  `google-sentence-case`, `ms-sentence-case`). "Where new content goes", not "Where New Content
  Goes".
- **One `#` heading per file,** as its title, then `##` and `###` in order, with no level
  skipped, and none deeper than `####`. A file that needs a fifth level wants splitting.
- **A heading names what follows.** No trailing full stop, and no heading used for emphasis.
- **A name that is lowercase by nature,** such as a repository or a command, goes in code
  formatting or in the repository's vocabulary, so the check accepts it.

## Paragraphs and line length

- **Wrap prose at 100 characters.** A diff then shows which sentence changed, and a reviewer
  reads it without scrolling sideways. A table row, a URL or a code line can run longer.
- **One idea per paragraph,** led by its point (rule 1).
- **A rule or a list item may open with its point in bold,** followed by the detail, as this
  file does.
- **A blank line goes before and after each heading, list, table and code block.** No line ends
  in spaces, and the file ends in one newline. A repository's `.editorconfig` keeps the last
  two.

## Lists

- **`-` for bullets.** Numbers only for steps done in order, or items the text refers to by
  number.
- **A list follows a sentence that introduces it,** ending in a colon where the list completes
  that sentence.
- **Items in one list share a form:** all sentences, or all fragments.
- **Continuation lines indent** to line up under the item's text: two spaces under `- `, three
  under `1. `.
- **Two levels of nesting at most.** A deeper list reads better as a table or as sections.

## Code

- **Fenced code blocks name their language:** `sh`, `python`, `yaml`, `json`, `ini`, or `text`
  for output and plain text.
- **Inline code** holds commands, paths, file names, identifiers, keys, and values to type
  (rule 9). It isn't used for emphasis.
- **A command that does something destructive** shows its dry run or its confirmation first.

## Tables

- **Use a table to compare things on the same points,** or for reference data looked up by a
  key. Use a list for anything read in order.
- **Every table has a header row.** A cell holds one fact.

## Links and emphasis

- **Link text says where it goes:** "the setup reference", not "here".
- **Links inside a repository are relative,** so they work on a fork, a clone and a branch.
- **Bold** marks a key phrase that opens a paragraph or list item. *Italics* name a section
  being cited. Neither is used for anything else.

## File names

- **Lowercase with hyphens,** such as `authoring-a-skill.md` (rule 9).
- **Apart from the usual capitalized files at a repository's root:** `README.md`, `LICENSE`,
  `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, and others a
  tool expects by name.

## A README's sections

Every README has at least these, in this order, under these headings (rule 10). Others go
where they fit. project-bootstrap-and-audit's README template, in the standard's Starter file
contents, also has Requirements before Install, and Configuration after Usage.

| Section | Holds |
|---|---|
| The opening paragraph | Under the title: what the project does, and for whom |
| Install | The commands, from nothing to installed |
| Usage | The first thing to do with it, and where the rest is documented |
| Development | How to build, test and check it, and how to release it if it releases |
| Operations | How to run it, and how to roll back or withdraw something gone wrong |
| Security | How to report a vulnerability, or a link to `SECURITY.md` |
| License | Its license, by name, with a link to the file |

## Words to cut, and what to use instead

Rule 3 names six words. HouseStyle's `Filler` rule finds each.

| Word | Why it goes | Instead |
|---|---|---|
| `just` | Usually filler (fact `google-just`) | Delete it. Where it means "only" or "a moment ago", say that |
| `simply` | What's simple for one reader isn't for another (fact `google-just`) | Delete it |
| `very` | An intensifier, which claims what the facts should show | A precise word, or the number |
| `seamless` | A claim, not a description | Say what works and what's needed |
| `robust` | Vague, unless it describes a sturdy object (fact `govuk-avoid`) | Say what it withstands |
| `leverage` | Means "use", outside finance (facts `google-leverage`, `govuk-avoid`) | Use, build on, or take advantage of |

Unearned hedging goes too: "should work", "might help" and "probably" where the fact can be
checked. Check it, or say plainly that it wasn't checked (rule 4).

## Plain words

Rule 2: a common word where one exists, and one term for each thing.

| Instead of | Write |
|---|---|
| utilize | use |
| facilitate | help, or make possible |
| in order to | to |
| prior to | before |
| a number of | some, or the number |
| at this point in time | now |
| due to the fact that | because |

Once a thing has a name, keep it. Calling one file "the record", "the log" and "the history"
in turn makes a reader wonder whether there are three.

## American spelling

Rule 12. HouseStyle's `Spelling` rule finds the common British forms and gives the American
one. The pattern behind most of them:

| British | American | For example |
|---|---|---|
| -ise, -isation | -ize, -ization | organize, organization, recognize |
| -our | -or | behavior, color, favor |
| -re | -er | center |
| -ogue | -og | catalog |
| -ence (some nouns) | -ense | license, defense, offense |
| a doubled `l` before -ed, -ing | a single `l` | labeled, canceled, modeling |
| -ement after -dg | -ment | judgment, acknowledgment |

Some words in -ise are the same in both, such as advise, exercise, promise, otherwise and
expertise. The rule lists the words it changes, so it leaves these alone.

The names of things keep their own spelling, such as the Open Government Licence. So do words
quoted from a source.

## Records and dates

- **Dates are written `YYYY-MM-DD`.** A reader anywhere reads them the same way, and they sort.
- **Commit subjects, the changelog and the decision record** follow rule 11. git-workflows has
  the detail.
- **An append-only record's past entries stay as they were written.** New entries follow the
  style.
