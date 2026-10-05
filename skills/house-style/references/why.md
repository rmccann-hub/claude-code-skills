# Why: the reasons behind the house style, what others do, and what each choice costs

Read this when you want to know why a rule says what it does, when a guide you respect says
something else, or when you're deciding whether a rule fits a repository. The rules are numbered
as in `SKILL.md`. Facts are named by ID from `facts.md`, where each has its source and the date
it was checked.

Checked 2026-10-05.

## Contents

1. The answer first
2. Plain words, and one term for each thing
3. No filler, hype or unearned hedging
4. Checked facts
5. Short sentences
6. Rules that say what breaks, and statuses that say who's waiting
7. A reader who wasn't there
8. Markdown's form
9. Code formatting and file names
10. One README layout
11. Commits, changelogs and decisions
12. American spelling
13. Formatters for code
14. Checking it with Vale

## 1. The answer first

**The advice.** Lead with the answer or the result, then the reasons.

**Why.** Most readers stop early. A reviewer skimming a pull request, an owner reading a report
on a phone, and an agent reading a context file all get the point before they stop. A reason
read first is a reason read without knowing what it's for.

**What it costs.** A reader who needs the reasoning to trust the answer has to read on. That's
the cost the rule accepts.

**When to choose differently.** In a tutorial, where the reader builds up to the result, the
steps come first.

## 2. Plain words, and one term for each thing

**The advice.** A common word where one exists, and the same term for the same thing every time.

**Why.** Readers vary in their English, and many read through a translation tool. A plain word
survives that, and a synonym that's only there for variety looks like a second thing. GOV.UK
makes plain English mandatory for all its pages (fact `govuk-avoid`).

**What it costs.** Prose with no varied wording reads plainer. That's the intent.

## 3. No filler, hype or unearned hedging

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

## 4. Checked facts

**The advice.** Every fact is checked against its source. Anything that can go stale carries its
source and date, and anything not checked says so.

**Why.** A wrong fact copied into many repositories is wrong in all of them. A date on a fact
tells the next reader when to doubt it. Saying what wasn't checked costs a sentence, and stops a
guess passing for a finding.

**What it costs.** Time at writing, and a date to check again by. In the owner's skills, each
dated fact is checked again on a schedule.

## 5. Short sentences

**The advice.** Short sentences, in the active voice, with one idea each.

**Why.** A long sentence holds its reader's memory until its verb arrives. The active voice names
who does what, which matters in instructions and in records of who decided.

**When to choose differently.** Where the actor is unknown or doesn't matter, the passive is
fine: "the file is generated".

## 6. Rules that say what breaks, and statuses that say who's waiting

**The advice.** A rule says what fails without it. A status says what's waiting, and on whom.

**Why.** A rule with its reason can be judged, and dropped when the reason goes. A rule without
one is kept forever, or broken on a guess. A status that names who it waits on gets answered.

## 7. A reader who wasn't there

**The advice.** No session detail and no private shorthand.

**Why.** Repositories outlive the conversations that changed them. A reader a year on, or a new
agent, has only the text.

## 8. Markdown's form

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

## 9. Code formatting and file names

**The advice.** Commands, paths and identifiers in code formatting. File names lowercase with
hyphens, apart from the usual capitalized root files.

**Why.** Code formatting tells a reader what to type exactly. Lowercase names avoid clashes
between file systems that do and don't care about case, and hyphens read as word breaks in a
URL.

## 10. One README layout

**The advice.** The same sections in the same order in every README.

**Why.** A reader who knows one repository can find the install steps in all of them.

**What it costs.** A small repository has some short sections. Short is fine; missing makes a
reader hunt.

## 11. Commits, changelogs and decisions

**The advice.** "area: summary" commit subjects, a Keep a Changelog changelog, and one decision
record, newest first. git-workflows has the reasons and the alternatives for each.

## 12. American spelling

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

## 13. Formatters for code

**The advice.** Each language's own formatter and linter, set up by project-bootstrap-and-audit.

**Why.** A formatter ends arguments about layout, and its output is the same on every machine.

## 14. Checking it with Vale

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
