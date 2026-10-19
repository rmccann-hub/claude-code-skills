# Writing style

Read this for writing or reviewing prose or Markdown: headings, paragraphs, lists, code, tables,
links, file names, a README's sections, the words to cut, plain words and American spelling,
and why each rule is what it is.

It holds the detail behind the rules in this skill's `SKILL.md`, numbered as there. Running the
check is `prose-check`. Commit subjects and changelog structure are git-workflows'.

## Rules

The thirteen rules are in `SKILL.md`. This is how each applies to Markdown and to words.

### Headings

- **Sentence case:** capitalize the first word and proper nouns, nothing else (facts
  `google-sentence-case`, `ms-sentence-case`). "Where new content goes", not "Where New Content
  Goes".
- **One `#` heading per file,** as its title, then `##` and `###` in order, with no level
  skipped, and none deeper than `####`. A file that needs a fifth level wants splitting.
- **A heading names what follows.** No trailing full stop, and no heading used for emphasis.
- **A name that is lowercase by nature,** such as a repository or a command, goes in code
  formatting or in the repository's vocabulary, so the check accepts it.

### Paragraphs and line length

- **Wrap prose at 100 characters.** A diff then shows which sentence changed, and a reviewer
  reads it without scrolling sideways. A table row, a URL or a code line can run longer.
- **One idea per paragraph,** led by its point (rule 1).
- **A rule or a list item may open with its point in bold,** followed by the detail, as this
  file does.
- **A blank line goes before and after each heading, list, table and code block.** No line ends
  in spaces, and the file ends in one newline. A repository's `.editorconfig` keeps the last
  two.

### Lists

- **`-` for bullets.** Numbers only for steps done in order, or items the text refers to by
  number.
- **A list follows a sentence that introduces it,** ending in a colon where the list completes
  that sentence.
- **Items in one list share a form:** all sentences, or all fragments.
- **Continuation lines indent** to line up under the item's text: two spaces under `- `, three
  under `1. `.
- **Two levels of nesting at most.** A deeper list reads better as a table or as sections.

### Code

- **Fenced code blocks name their language:** `sh`, `python`, `yaml`, `json`, `ini`, or `text`
  for output and plain text.
- **Inline code** holds commands, paths, file names, identifiers, keys, and values to type
  (rule 9). It isn't used for emphasis.
- **A command that does something destructive** shows its dry run or its confirmation first.

### Tables

- **Use a table to compare things on the same points,** or for reference data looked up by a
  key. Use a list for anything read in order.
- **Every table has a header row.** A cell holds one fact.

### Links and emphasis

- **Link text says where it goes:** "the setup reference", not "here".
- **Links inside a repository are relative,** so they work on a fork, a clone and a branch.
- **Bold** marks a key phrase that opens a paragraph or list item. *Italics* name a section
  being cited. Neither is used for anything else.

### File names

- **Lowercase with hyphens,** such as `authoring-a-skill.md` (rule 9).
- **Apart from the usual capitalized files at a repository's root:** `README.md`, `LICENSE`,
  `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, and others a
  tool expects by name.

### A README's sections

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

### Words to cut, and what to use instead

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

Once a thing has a name, keep it. Calling one file "the record", "the log" and "the history"
in turn makes a reader wonder whether there are three.

### American spelling

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

### Records and dates

- **Dates are written `YYYY-MM-DD`.** A reader anywhere reads them the same way, and they sort.
- **A time is stamped in UTC, with its zone,** such as `14:05 UTC`, or ISO 8601 with `Z`. A
  reader's local time, where they want one, is worked out from the stamp and follows it, with
  its own zone: `00:55 UTC (8:55 PM EDT, Fri Oct 16)`. A time with no zone is a guess at the
  reader's clock, and a local time on its own goes wrong twice a year.
- **A time copied from a source keeps the zone the source gave it,** and is converted to UTC
  from that zone. One audit copied a log's `5. October 2026, 22:48 (UTC-04:00)` as
  `2026-10-05 22:48`, and its date then disagreed with the file it cited, named for the next
  day, the date in UTC.
- **Commit subjects, the changelog and the decision record** follow rule 11. git-workflows has
  the detail.
- **An append-only record's past entries stay as they were written.** New entries follow the
  style.

## Mistakes

- **Title Case headings,** copied from a template or another guide. Sentence case is the rule
  (rule 8), and the check flags the rest.
- **"Just", "simply" and the rest of the six,** in any sense. The check flags each, so `just`
  meaning "only" gets reworded too (rule 3).
- **A hedge where the fact can be checked:** "should work", "might help", "probably". Check it,
  or say it wasn't checked (rule 4).
- **Three names for one thing,** such as "the record", "the log" and "the history" for one file
  (rule 2).
- **Session detail in a repository,** such as "as we discussed" or "the earlier run". A reader
  who wasn't there can't follow it (rule 7).
- **Restyling text the style leaves alone:** files shared with an upstream project, third-party
  files, quotes, and past entries in an append-only record.
- **Converting a quote to American spelling.** A quote keeps its source's words (rule 12).
- **Link text that says "here"** or "this link". Say where it goes.

## Audit

Severity uses the standard's status words: `BLOCKER`, `DRIFT`, `GAP`, `OVER`, `MIRROR`,
`UNVERIFIABLE-HERE`, `OK` and `N/A`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| The checked rules pass | `git ls-files -z '*.md' \| xargs -0 vale`, where `prose-check` is set up | `GAP` per file that fails | Fix the text, or the vocabulary where a name is flagged |
| The answer comes first | Read the first paragraph of each README, report and pull request description | `GAP` where it opens with background | Move the result to the top |
| Facts carry sources and dates | Versions, dates and support windows in the prose, each with its source and checked date | `GAP` per stale-prone fact without one | Check it, and add the source and date, or say it wasn't checked |
| The README's sections | Each README's headings, against rule 10's order | `GAP` per missing section | Add it; short is fine |
| Lines wrap at 100 | `awk 'length > 100' FILE`, leaving out tables, URLs and code | `DRIFT` | Rewrap the paragraph |
| File names | `git ls-files` for capitals or underscores outside the usual root files | `DRIFT` | Rename, and fix the links |

## Why

Each rule's reason, what other guides do, and what each choice costs, numbered as in `SKILL.md`.
Checked 2026-10-05. The reasons for the check itself are in `prose-check`.

### 1. The answer first

**The advice.** Lead with the answer or the result, then the reasons.

**Why.** Most readers stop early. A reviewer skimming a pull request, an owner reading a report
on a phone, and an agent reading a context file all get the point before they stop. A reason
read first is a reason read without knowing what it's for.

**What it costs.** A reader who needs the reasoning to trust the answer has to read on. That's
the cost the rule accepts.

**When to choose differently.** In a tutorial, where the reader builds up to the result, the
steps come first.

### 2. Plain words, and one term for each thing

**The advice.** A common word where one exists, and the same term for the same thing every time.

**Why.** Readers vary in their English, and many read through a translation tool. A plain word
survives that, and a synonym that's only there for variety looks like a second thing. GOV.UK
makes plain English mandatory for all its pages (fact `govuk-avoid`).

**What it costs.** Prose with no varied wording reads plainer. That's the intent.

### 3. No filler, hype or unearned hedging

**The advice.** No `just`, `simply`, `very`, `seamless`, `robust` or `leverage`, and no
"should work" where the fact can be checked.

**Why.** Each word either adds nothing or claims what the text should show. Google's word list
calls `just` usually filler, and asks writers to try cutting `simply` (fact `google-just`). It
avoids `leverage` where it means "use" (fact `google-leverage`). GOV.UK lists both `leverage` and
`robust` as words to avoid (fact `govuk-avoid`). `very` and `seamless` are this style's own
additions, for the same reason: an intensifier or a claim stands in for the fact that would
show it.

**What others do.** Google and GOV.UK publish long lists of words to avoid. This style keeps six,
the ones that turned up in practice, so the check stays quiet on text that's fine.

**What it costs.** A writer sometimes has to find the precise word, or the number. The check
flags each of the six in any context, so `just` meaning "only" needs rewording too. A word
mentioned as a word, as here, goes in code formatting, which the check skips.

### 4. Checked facts

**The advice.** Every fact is checked against its source. Anything that can go stale carries its
source and date, and anything not checked says so.

**Why.** A wrong fact copied into many repositories is wrong in all of them. A date on a fact
tells the next reader when to doubt it. Saying what wasn't checked costs a sentence, and stops a
guess passing for a finding.

**What it costs.** Time at writing, and a date to check again by. In the owner's skills, each
dated fact is checked again on a schedule.

### 5. Short sentences

**The advice.** Short sentences, in the active voice, with one idea each.

**Why.** A long sentence holds its reader's memory until its verb arrives. The active voice names
who does what, which matters in instructions and in records of who decided.

**When to choose differently.** Where the actor is unknown or doesn't matter, the passive is
fine: "the file is generated".

### 6. Rules that say what breaks, and statuses that say who's waiting

**The advice.** A rule says what fails without it. A status says what's waiting, and on whom.

**Why.** A rule with its reason can be judged, and dropped when the reason goes. A rule without
one is kept forever, or broken on a guess. A status that names who it waits on gets answered.

### 7. A reader who wasn't there

**The advice.** No session detail and no private shorthand.

**Why.** Repositories outlive the conversations that changed them. A reader a year on, or a new
agent, has only the text.

### 8. Markdown's form

**The advice.** Sentence-case headings, `-` bullets, prose wrapped at 100 characters, fenced code
with its language, and tables for comparisons.

**Why.**

- **Sentence case** is what Google's and Microsoft's guides use (facts `google-sentence-case`,
  `ms-sentence-case`). It's quicker to read, and it leaves no doubt over which small words to
  capitalize.
- **Wrapped lines** make a diff show the sentence that changed.
- **Fenced code with a language** gets highlighted, and readers can tell it from prose.

**What others do.** Some guides use title case for headings. The check takes one side, so mixing
the two in one repository is flagged.

**What it costs.** Rewrapping a paragraph changes every line after the edit. Wrapping at
sentence ends would avoid that, at the price of ragged files, so this style wraps by length.

### 9. Code formatting and file names

**The advice.** Commands, paths and identifiers in code formatting. File names lowercase with
hyphens, apart from the usual capitalized root files.

**Why.** Code formatting tells a reader what to type exactly. Lowercase names avoid clashes
between file systems that do and don't care about case, and hyphens read as word breaks in a
URL.

### 10. One README layout

**The advice.** The same sections in the same order in every README.

**Why.** A reader who knows one repository can find the install steps in all of them.

**What it costs.** A small repository has some short sections. Short is fine; missing makes a
reader hunt.

### 11. Commits, changelogs and decisions

**The advice.** "area: summary" commit subjects, a Keep a Changelog changelog, and one decision
record, newest first. git-workflows has the reasons and the alternatives for each.

### 12. American spelling

**The advice.** American spelling throughout. Quotes and names keep their own.

**Why.** The owner chose it. The tools and platforms these repositories use write American
English, and so does their code: a skill's frontmatter has a `license` field, and GitHub has
organizations. Mixed spelling reads as two authors, and makes a search for one form miss the
other.

**What it costs.** Converting text written in British English, done once here as its own
commit. A quote keeps its source's spelling, so a few British forms remain inside quotation
marks.

**When to choose differently.** A project whose readers write British English, such as one for a
UK public body, would choose British, and swap the spelling rule's direction.

### 13. Formatters for code

**The advice.** Each language's own formatter and linter, set up by project-bootstrap-and-audit.

**Why.** A formatter ends arguments about layout, and its output is the same on every machine.

## Facts

What other style guides say, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `google-sentence-case` | Google's developer documentation style guide puts headings in sentence case | [Headings and titles](https://developers.google.com/style/headings) | "Use sentence case for headings and titles." | 2026-10-05 | 2027-04-05 |
| `ms-sentence-case` | Microsoft's style guide uses sentence-style capitalization: the first word and proper nouns | [Capitalization](https://learn.microsoft.com/en-us/style-guide/capitalization) | "Microsoft style uses sentence-style capitalization." | 2026-10-05 | 2027-04-05 |
| `google-just` | Google's word list calls "just" usually filler, and asks writers to try cutting "simply" | [Word list](https://developers.google.com/style/word-list) | "Usually, just is a filler word that you can delete without affecting your meaning." and "Try eliminating this word from the sentence because usually the same meaning can be conveyed without it." | 2026-10-05 | 2027-04-05 |
| `google-leverage` | Google's word list avoids "leverage" where it means "use" | [Word list](https://developers.google.com/style/word-list) | "Avoid using if you mean use." | 2026-10-05 | 2027-04-05 |
| `google-license` | Google's developer documentation is under CC BY 4.0, and its code samples under Apache 2.0 | [Google developer documentation style guide](https://developers.google.com/style) | "licensed under the Creative Commons Attribution 4.0 License" | 2026-10-05 | 2027-04-05 |
| `govuk-avoid` | GOV.UK makes plain English mandatory, and lists "leverage" and "robust" among the words to avoid | [Style guide, A to Z](https://www.gov.uk/guidance/style-guide/a-to-z) | "Plain English is mandatory for all of GOV.UK" and "leverage (unless in the financial sense)" and "robust (unless talking about a sturdy object)" | 2026-10-05 | 2027-04-05 |

## Sources

Every rule here is written in this skill's own words. Sources are quoted only briefly, with
attribution, and each quote is a dated fact above.

| Source | Used for | License |
|---|---|---|
| [Google developer documentation style guide](https://developers.google.com/style) | Sentence-case headings, and the words "just", "simply" and "leverage" | CC BY 4.0 (fact `google-license`): short quotes, with attribution |
| [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/) | Sentence-style capitalization | Microsoft's terms of use: one short quote, for a fact |
| [GOV.UK style guide](https://www.gov.uk/guidance/style-guide/a-to-z) | Plain English, and the words "leverage" and "robust" | Open Government Licence v3.0: short quotes, with attribution |
