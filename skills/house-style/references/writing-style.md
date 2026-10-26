# Writing style

Read this for writing or reviewing prose or Markdown: headings, lists, wrapping, code, tables,
links, file names, a README's sections, word choice and spelling, and why each rule is what it is.

It details the thirteen rules in this skill's `SKILL.md`, numbered as there.
Running the check is `prose-check`. Commit subjects and changelog structure are git-workflows'.

## Rules

### Headings

- **Sentence case:** the first word and proper nouns capitalized, nothing else: "Where new
  content goes", not "Where New Content Goes".
- **One `#` heading per file,** as its title, then `##` and `###` in order, none skipped and
  none deeper than `####`. A file that needs a fifth level wants splitting.
- **A heading names what follows,** with no trailing full stop, and is never used for emphasis.
- **A name lowercase by nature,** such as a repository or a command, goes in code formatting or
  the repository's vocabulary, so the check accepts it.

### Paragraphs and line length

- **Wrap prose at 100 characters.** A table row, a URL or a code line can run longer.
- **One idea per paragraph,** led by its point (rule 1).
- **A rule or a list item may open with its point in bold,** then the detail, as here.
- **Blank lines surround each heading, list, table and code block.** No line ends in spaces,
  and the file ends in one newline, both kept by a repository's `.editorconfig`.

### Lists

- **`-` for bullets.** Numbers only for steps done in order, or items the text cites by number.
- **A sentence introduces each list,** ending in a colon where the list completes it.
- **Items in one list share a form:** all sentences, or all fragments.
- **Continuation lines indent** under the item's text: two spaces under `- `, three under `1. `.
- **Two levels of nesting at most.** Deeper reads better as a table or as sections.

### Code

- **Fenced code blocks name their language:** `sh`, `python`, `yaml`, `json`, `ini`, or `text`
  for output and plain text.
- **Inline code** holds commands, paths, file names, identifiers, keys, and values to type
  (rule 9), never emphasis.
- **A destructive command** shows its dry run or its confirmation first.

### Tables

- **A table compares things on the same points,** or holds reference data looked up by a key.
  Anything read in order is a list.
- **Every table has a header row,** and a cell holds one fact.

### Links and emphasis

- **Link text says where it goes:** "the setup reference", not "here".
- **Links inside a repository are relative,** so they work on a fork, a clone and a branch.
- **Bold** opens a paragraph or list item with its key phrase, and *italics* name a section
  being cited. Neither does anything else.

### File names

- **Lowercase with hyphens,** such as `authoring-a-skill.md` (rule 9), apart from the usual
  capitalized root files: `README.md`, `LICENSE`, `CHANGELOG.md`, `SECURITY.md`,
  `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, and others a tool expects by name.

### A README's sections

Every README has at least these, in this order, under these headings (rule 10); others go where
they fit. project-bootstrap-and-audit's README template adds Requirements before Install, and
Configuration after Usage.

| Section | Holds |
|---|---|
| The opening paragraph | Under the title: what the project does, and for whom |
| Install | The commands, from nothing to installed |
| Usage | The first thing to do with it, and where the rest is documented |
| Development | How to build, test and check it, and release it if it releases |
| Operations | How to run it, and roll back or withdraw something gone wrong |
| Security | How to report a vulnerability, or a link to `SECURITY.md` |
| License | Its license, by name, linked to the file |

### Words to cut, and what to use instead

Rule 3 names six words, and HouseStyle's `Filler` rule finds each.

| Word | Instead |
|---|---|
| `just` | Delete it. Where it means "only" or "a moment ago", say that |
| `simply` | Delete it |
| `very` | A precise word, or the number |
| `seamless` | Say what works and what's needed |
| `robust` | Say what it withstands |
| `leverage` | Use, build on, or take advantage of |

Unearned hedging goes too: "should work", "might help" or "probably" where the fact can be
checked (rule 4).

### Plain words

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

### American spelling

HouseStyle's `Spelling` rule finds common British forms and gives the American (rule 12), most
by a pattern:

| British | American | For example |
|---|---|---|
| -ise, -isation | -ize, -ization | organize, organization, recognize |
| -our | -or | behavior, color, favor |
| -re | -er | center |
| -ogue | -og | catalog |
| -ence (some nouns) | -ense | license, defense, offense |
| a doubled `l` before -ed, -ing | a single `l` | labeled, canceled, modeling |
| -ement after -dg | -ment | judgment, acknowledgment |

The rule lists the words it changes, so it leaves alone -ise words that are the same in both,
such as advise, exercise, promise, otherwise and expertise. Names, such as the Open
Government Licence, and quotes keep their own spelling.

### Records and dates

- **Dates are `YYYY-MM-DD`,** read the same way anywhere, and sortable.
- **A time is stamped in UTC, with its zone,** such as `14:05 UTC`, or ISO 8601 with `Z`. A
  local time, if wanted, is derived from the stamp and shown with it, each with its zone, in the
  order the reader chose: `8:55 PM EDT, Fri Oct 16 (2026-10-17 00:55 UTC)`. A time with no zone
  guesses at the reader's clock, and a local time without its stamp goes wrong twice a year.
- **A time copied from a source is converted to UTC from the source's zone.** One audit copied a
  log's `5. October 2026, 22:48 (UTC-04:00)` as `2026-10-05 22:48`, so its date disagreed with
  the file it cited, named for the next day, the date in UTC.
- **An append-only record's past entries stay as written.** New entries follow the style.

## Mistakes

- **Title Case headings,** copied from a template or another guide (rule 8).
- **"Just", "simply" and the rest of the six,** in any sense: the check flags `just` meaning
  "only" too (rule 3).
- **A hedge where the fact can be checked,** such as "should work" (rule 4).
- **Three names for one thing,** such as "the record", "the log" and "the history" (rule 2).
- **Session detail,** such as "as we discussed" or "the earlier run", which a reader who wasn't
  there can't follow (rule 7).
- **Restyling what the style leaves alone:** upstream-shared files, third-party files, quotes,
  and an append-only record's past entries.
- **Converting a quote to American spelling** (rule 12).
- **Link text that says "here"** or "this link".

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| The checked rules pass | `git ls-files -z '*.md' \| xargs -0 vale`, where `prose-check` is set up | `GAP` per file that fails | Fix the text, or add a flagged name to the vocabulary |
| The answer comes first | The first paragraph of each README, report and pull request description | `GAP` where it opens with background | Move the result to the top |
| Facts carry sources and dates | Versions, dates and support windows in the prose | `GAP` per stale-prone fact lacking either | Check it and add both, or say it wasn't checked |
| The README's sections | Each README's headings, against rule 10's order | `GAP` per missing section | Add it; short is fine |
| Lines wrap at 100 | `awk 'length > 100' FILE`, leaving out tables, URLs and code | `DRIFT` | Rewrap the paragraph |
| File names | `git ls-files` for capitals or underscores outside the usual root files | `DRIFT` | Rename, and fix the links |

## Why

Each rule's reason, what others do, and the cost, numbered as in `SKILL.md` and checked
2026-10-05. The check's own reasons are in `prose-check`.

### 1. The answer first

**Why:** most readers stop early: a reviewer skimming a pull request, an owner reading a report
on a phone, an agent reading a context file. A reason read first is read without knowing what
it's for. **Cost:** a reader who needs the reasoning to trust the answer reads on. **Choose
differently:** in a tutorial, where the reader builds up to the result, the steps come first.

### 2. Plain words, and one term for each thing

**Why:** readers vary in their English, and many read through a translation tool. A plain word
survives that, and a synonym used for variety looks like a second thing. GOV.UK makes plain
English mandatory (fact `govuk-avoid`). **Cost:** plainer prose, which is the intent.

### 3. No filler, hype or unearned hedging

**Why:** each of the six adds nothing or claims what the text should show. Google calls `just`
usually filler, and asks writers to try cutting `simply` (fact `google-just`), since what's
simple for one reader isn't for another. Google avoids `leverage` meaning "use" (fact
`google-leverage`). GOV.UK avoids it outside finance, and `robust` unless of a sturdy object,
as vague (fact `govuk-avoid`). `very` and `seamless` are this style's own: an intensifier or a
claim stands in for the fact. **Others:** Google and GOV.UK list many more words. This style
keeps the six seen in practice, so the check stays quiet on fine text. **Cost:** finding the
precise word or the number, and rewording `just` meaning "only". A word mentioned as a word, as
here, goes in code formatting, which the check skips.

### 4. Checked facts

**Why:** a wrong fact copied into many repositories is wrong in all of them. A date on a fact
tells the next reader when to doubt it. Saying what wasn't checked costs a sentence, and stops a
guess passing for a finding. **Cost:** time at writing, and a date to check again by, which
the owner's skills keep on a schedule.

### 5. Short sentences in the active voice

**Why:** a long sentence holds its reader's memory until its verb arrives. The active voice names
who does what, which matters in instructions and in records of who decided. **Choose
differently:** where the actor is unknown or doesn't matter, the passive is fine: "the file is
generated".

### 6. Rules that say what breaks, and statuses that say who's waiting

**Why:** a rule with its reason can be judged, and dropped when the reason goes. A rule without
one is kept forever, or broken on a guess. A status that names who it waits on gets answered.

### 7. A reader who wasn't there

**Why:** repositories outlive the conversations that changed them. A reader a year on, or a new
agent, has only the text.

### 8. Markdown's form

**Why:** sentence case is Google's and Microsoft's choice (facts `google-sentence-case`,
`ms-sentence-case`). It's quicker to read, with no doubt over which small words to capitalize.
Wrapped lines make a diff show the sentence that changed, and spare a reviewer scrolling
sideways. Fenced code with a language gets highlighted, and stands apart from prose.
**Others:** some guides use title case. The check takes one side, so a repository mixing the two
is flagged. **Cost:** rewrapping a paragraph changes every line after the edit. Wrapping at
sentence ends would avoid that, at the price of ragged files, so this style wraps by length.

### 9. Code formatting and file names

**Why:** code formatting tells a reader what to type exactly. Lowercase names avoid clashes
between file systems that do and don't care about case, and hyphens read as word breaks in a
URL.

### 10. One README layout

**Why:** a reader who knows one repository can find the install steps in all of them. **Cost:**
a small repository has some short sections. Short is fine; missing makes a reader hunt.

### 11. Commits, changelogs and decisions

git-workflows has the reasons and the alternatives.

### 12. American spelling

**Why:** the owner chose it. The tools and platforms these repositories use write American
English, and so does their code: a skill's frontmatter has a `license` field, and GitHub has
organizations. Mixed spelling reads as two authors, and a search for one form misses the other.
**Cost:** converting British text, done here once in its own commit. A few British forms remain
inside quotes. **Choose differently:** a project whose readers write British English, such as
one for a UK public body, would choose British, and swap the spelling rule's direction.

### 13. Formatters for code

**Why:** a formatter ends arguments about layout, and its output is the same on every machine.

## Facts

What other style guides say, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `google-sentence-case` | Google puts headings in sentence case | [Headings and titles](https://developers.google.com/style/headings) | "Use sentence case for headings and titles." | 2026-10-05 | 2027-04-05 |
| `ms-sentence-case` | Microsoft uses sentence-style capitalization | [Capitalization](https://learn.microsoft.com/en-us/style-guide/capitalization) | "Microsoft style uses sentence-style capitalization." | 2026-10-05 | 2027-04-05 |
| `google-just` | Google calls "just" usually filler, and suggests cutting "simply" | [Word list](https://developers.google.com/style/word-list) | "Usually, just is a filler word" and "Try eliminating this word" | 2026-10-05 | 2027-04-05 |
| `google-leverage` | Google avoids "leverage" meaning "use" | [Word list](https://developers.google.com/style/word-list) | "Avoid using if you mean use." | 2026-10-05 | 2027-04-05 |
| `google-license` | Google's style guide is under CC BY 4.0 | [Style guide](https://developers.google.com/style) | "licensed under the Creative Commons Attribution 4.0 License" | 2026-10-05 | 2027-04-05 |
| `govuk-avoid` | GOV.UK makes plain English mandatory, and avoids "leverage" and "robust" | [Style guide, A to Z](https://www.gov.uk/guidance/style-guide/a-to-z) | "Plain English is mandatory" and "leverage (unless in the financial sense)" and "robust (unless talking about a sturdy object)" | 2026-10-05 | 2027-04-05 |

## Sources

Rules here are in this skill's own words, and each brief, attributed quote is a dated fact above.

| Source | Used for | License |
|---|---|---|
| [Google developer documentation style guide](https://developers.google.com/style) | Sentence case; "just", "simply", "leverage" | CC BY 4.0 (fact `google-license`): short quotes, attributed |
| [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/) | Sentence-style capitalization | Microsoft's terms of use: one short quote, for a fact |
| [GOV.UK style guide](https://www.gov.uk/guidance/style-guide/a-to-z) | Plain English; "leverage", "robust" | Open Government Licence v3.0: short quotes, attributed |
