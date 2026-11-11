# Documentation

Read this for organizing a project's documentation beyond its README: which kind of page to
write, whether to build a docs site and with what, diagrams kept as text, when to split a
document, reference generated from code, checks that keep docs true to the code, and docs in a
pull request.

It covers the documents as a set. How the prose reads, a README's sections, records and
generated sections are `writing-style`; the Vale check is `prose-check`. A pull request's
description is git-workflows'; a context file's content and budget, project-bootstrap-and-audit's.

## Rules

1. **Give each page one job, by what its reader is doing:** learning (a tutorial), doing a task
   (a how-to guide), looking up (reference) or understanding (explanation), the four kinds of
   Diátaxis (fact `docs-diataxis`).
2. **Generate reference from the code,** and write by hand only what the code can't say.
3. **Keep each fact in one place** and point to it. A copy that must exist is generated, or a
   test holds it to its source.
4. **Check docs in CI like code:** relative links, examples and generated sections on every pull
   request; external links on a schedule.
5. **Write a format beside the field that holds it,** not only in the test that enforces it.
6. **Take a figure or a summary from the final state and the implementation in use,** named by
   its version or commit.
7. **Keep diagrams as text beside what they describe,** Mermaid first, because GitHub renders
   it (fact `docs-github-diagrams`).
8. **Build a docs site only when Markdown in `docs/` no longer serves,** choosing the tool by
   ecosystem and support window.
9. **Split a document by reader and topic, within the standard's budgets.**
10. **Change the docs in the same pull request as the behavior they describe.**

### The four kinds

| Kind | The reader | Holds | Leaves out |
|---|---|---|---|
| Tutorial | Is learning | One path to a result that works | Options, alternatives, reasons |
| How-to guide | Has a task | The steps, assuming the basics | Teaching, background |
| Reference | Looks something up | Every option and field, in a fixed order | Steps, opinion |
| Explanation | Wants to understand | Reasons, trade-offs, history | Steps |

A page that mixes kinds is split, each part on its kind's page, linked.

### Docs sites

Markdown in `docs/`, linked from the README, renders on GitHub with no build and serves most
repositories. Where a site is needed, for search, versions or API reference:

| Ecosystem | Tool | State |
|---|---|---|
| Python, with API reference | Sphinx with autodoc | Current (facts `docs-sphinx`, `docs-autodoc`) |
| JavaScript or TypeScript | Docusaurus | Current (fact `docs-docusaurus`) |
| Rust | rustdoc | Runs doc tests too (fact `docs-rustdoc-tests`) |
| Markdown-first | MkDocs with Material | Not for a new site: facts `docs-mkdocs`, `docs-material-eol` |
| Markdown-first, accepting churn | Zensical | Before 1.0 (fact `docs-zensical`); builds MkDocs projects (fact `docs-zensical-compat`) |

### Diagrams

- **Mermaid in a fenced `mermaid` block** renders in GitHub's files, issues and pull requests.
  GitHub pins its own Mermaid version, which a block holding `info` shows (fact
  `docs-github-diagrams`): test a diagram there, not only in a newer editor.
- **D2 and PlantUML** need a render step GitHub doesn't run: commit the source and render in CI
  or on the site.
- **No image without its source.** An exported picture can't be diffed, and nobody updates it.
- **Use a notation readers know,** such as the C4 model's views, as the standard's *Choosing
  the shape* says; it also bars a diagram that must be hand-updated when the code moves.
- **Mermaid 12 re-lays out existing diagrams** (fact `docs-mermaid-12`). Review each before
  upgrading a site, or pin the old layout in its config.

### Size and splitting

The standard rules on size: *File governance*, under *Budgets*; dimension 4's split recipe; and
*Merge, delete, leave alone*. Follow them there. For any document:

- **Split by topic and kind,** never into parts 1, 2 and 3 of one topic.
- **Move a section whole,** deleting it from the old file in the same commit.
- **For a document an agent reads, one index links each part directly,** and a long part opens
  with a table of contents. Agents may preview files partly, and miss the end of a chain
  (fact `docs-skill-toc`).
- **A new file names the homes it considered,** as *File governance* requires.

### Checking docs against the code

- **Examples run as tests:** Python's `doctest` (fact `docs-doctest`), Rust's doc tests (fact
  `docs-rustdoc-tests`), or a job that extracts each fenced block and runs it, as this
  repository's `skillcheck --examples` does.
- **Links:** Sphinx's `linkcheck` builder (fact `docs-linkcheck`) or lychee. External links
  run on a schedule, since another site's outage fails a run that changed nothing.
- **Generated sections are rebuilt in CI and compared,** as this repository's `--bom-check`
  does for its dependency map.

## Mistakes

- **An options table copied by hand from `--help`.** Generate it from the parser, or link.
- **A count in prose beside the list it counts.** Delete the count, or generate it.
- **A tutorial that stops to list every option.** Move them to reference, and link.
- **autodoc over modules with side effects on import,** which it runs (fact `docs-autodoc`).
  Put the side effects behind a main function.
- **A report's summary copied from a first pass,** beside a verdict from a later one.

## Audit

Severity uses the standard's status words: `BLOCKER`, `DRIFT`, `GAP`, `OVER`, `MIRROR`,
`UNVERIFIABLE-HERE`, `OK` and `N/A`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Examples run | Code blocks in `docs/` and the README, and CI | `GAP` where nothing runs them | Doc tests, or a job running each block |
| Relative links resolve | A link checker's run | `DRIFT` per broken link | Fix it, and check links in CI |
| Hand copies of facts | Counts, option tables or versions restated beside their source | `DRIFT` where they disagree; `GAP` from T2, per the standard's dimension 10 | Delete the copy, or generate it |
| Diagrams have sources | Images in `docs/` with no text source | `GAP` per image | Redraw as text, or commit the source |
| Mermaid renders on GitHub | Each `mermaid` block, viewed there | `DRIFT` per error | Fix it for GitHub's version |
| The site's tool is supported | Facts `docs-mkdocs` and `docs-material-eol` | `GAP` where no move is planned | Record the plan |
| Behavior changes carry docs | Merged pull requests changing a command, option or output | `GAP` per change without docs | Document it |
| A tested format is written | Fields whose format only a test states | `GAP` | Write it beside the field |

## Why

### One job per page

A reader doing a task wants steps, and one learning wants a path: a page for both serves
neither. Diátaxis names four needs and four forms (fact `docs-diataxis`). **Cost:** links
between pages, and a kind chosen for each. **Choose differently:** a small tool's README can
hold all four in short sections.

### Generated reference, one home per fact, and checks

Prose no test reads drifts; a block code checks stays current (L40). One audit found 103
statements in a project's docs that its tree no longer supported, while its checked block
caught a stale line the same week. The standard's dimension 10 deletes a hand-copied fact
rather than policing it. **Cost:** a generator or test to keep, and examples written to run.
**Choose differently:** an example that can't run, such as one needing a live service, is
marked unchecked, with its reason.

**Formats beside fields:** a session learned a status field's format only from a failing test
(L29). A line beside the field saves the failed run.

**Figures from the final state and the tool in use:** one report carried a first-pass count, 12
of 14, beside a verdict of 13 of 14 written after a corrective pass (L44). One project's table
of a scoring program's deductions came partly from an unmaintained reimplementation, and
differed from the program in use on four rows (L48). A named version or commit lets a reader
check the figure.

### Diagrams as text

Text diffs, reviews and merges like code, and beside the code a change to one shows in the
other. **Others:** D2 and PlantUML give more control over layout, for a render step.
**Cost:** Mermaid's layout isn't exact, and a major version can change it (fact
`docs-mermaid-12`). **Choose differently:** a diagram needing exact layout may come from a
drawing tool, its source file committed beside it.

### Docs sites

A site adds search, navigation and versions, and a build to keep. The ecosystem's generator
builds its API reference; a tool past its support leaves security fixes to you. **Choose
differently:** an existing MkDocs site keeps working after Material's end of life, and moves
when a fix it needs won't come.

### Splitting

A reader finds a topic by its name, and a file holding one topic is changed whole. Agents may read
long files partly, so an index with direct links beats a chain (fact `docs-skill-toc`).
**Cost:** more files and links. **Choose differently:** a reference read in ranges, such as the
standard itself, can stay one file.

### Docs in the same pull request

A reviewer checks the docs against the change while both are in view. Django asks it of every
new or changed feature (fact `docs-django-pr`). **Cost:** a slower pull request. **Choose
differently:** a long guide may follow in its own pull request, linked, with the reference and
examples in the first.

## Facts

Versions, dates and practices, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `docs-diataxis` | Diátaxis sorts documentation into four kinds: tutorials, how-to guides, reference and explanation | [Diátaxis](https://diataxis.fr/) | "Diátaxis identifies four distinct needs, and four corresponding forms of documentation" | 2026-11-11 | 2027-05-11 |
| `docs-github-diagrams` | GitHub renders four diagram syntaxes, Mermaid among them, at a Mermaid version of its own | [Creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) | "You can create diagrams in Markdown using four different syntaxes: mermaid, geoJSON, topoJSON, and ASCII STL." and "Diagram rendering is available in GitHub Issues, GitHub Discussions, pull requests, wikis, and Markdown files." and "check the Mermaid version currently in use" | 2026-11-11 | 2027-02-11 |
| `docs-mermaid-12` | Mermaid is at 12.3.0; 12.0.0 changed the default layout of existing diagrams | [Mermaid changelog](https://raw.githubusercontent.com/mermaid-js/mermaid/develop/packages/mermaid/CHANGELOG.md) | "## 12.3.0" and "This changes how existing diagrams look." and "are now laid out by ELK instead of dagre" | 2026-11-11 | 2027-02-11 |
| `docs-mkdocs` | MkDocs' latest release is 1.6.1, of 2024-08-30 | [MkDocs release notes](https://www.mkdocs.org/about/release-notes/) | "Version 1.6.1 (2024-08-30)" | 2026-11-11 | 2027-02-11 |
| `docs-material-eol` | Material for MkDocs, at 9.8.1, is in maintenance and reaches end of life on 2027-05-05 | [Material changelog](https://squidfunk.github.io/mkdocs-material/changelog/) | "Material for MkDocs reaches end of life on May 5, 2027" and "9.8.1 November 7, 2026" | 2026-11-11 | 2027-02-11 |
| `docs-zensical` | Zensical is at 0.1.1 | `git ls-remote --tags https://github.com/zensical/zensical` | `ef9e91968fa6442839efe9087e777133c4c76117 refs/tags/v0.1.1` | 2026-11-11 | 2027-02-11 |
| `docs-zensical-compat` | Zensical builds existing MkDocs projects | [Zensical compatibility](https://zensical.org/compatibility/) | "Zensical can build existing MkDocs projects without requiring changes" | 2026-11-11 | 2027-02-11 |
| `docs-sphinx` | Sphinx 9.2.0 was released 2026-10-20 | [Sphinx changelog](https://www.sphinx-doc.org/en/master/changes/index.html) | "Release 9.2.0 (released Oct 20, 2026)" | 2026-11-11 | 2027-02-11 |
| `docs-docusaurus` | Docusaurus 3.10.2 was released 2026-07-10 | [Docusaurus changelog](https://raw.githubusercontent.com/facebook/docusaurus/main/CHANGELOG.md) | "## 3.10.2 (2026-07-10)" | 2026-11-11 | 2027-02-11 |
| `docs-autodoc` | autodoc builds reference from docstrings, importing the modules | [autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) | "pull in documentation from docstrings in a semi-automatic way" and "autodoc imports the modules to be documented" | 2026-11-11 | 2027-05-11 |
| `docs-linkcheck` | Sphinx's `linkcheck` builder checks external links | [Sphinx builders](https://www.sphinx-doc.org/en/master/usage/builders/index.html) | "This builder scans all documents for external links" | 2026-11-11 | 2027-05-11 |
| `docs-doctest` | Python's `doctest` runs the examples in documentation | [doctest](https://docs.python.org/3/library/doctest.html) | "executes those sessions to verify that they work exactly as shown" | 2026-11-11 | 2027-05-11 |
| `docs-rustdoc-tests` | rustdoc runs documentation examples as tests | [Documentation tests](https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html) | "rustdoc supports executing your documentation examples as tests." | 2026-11-11 | 2027-05-11 |
| `docs-django-pr` | Django asks for docs in the same change as a new or changed feature | [Submitting contributions](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/submitting-patches/) | "the change should also contain documentation" | 2026-11-11 | 2027-05-11 |
| `docs-skill-toc` | Anthropic: references one level deep, a table of contents past 100 lines, as files may be read partly | [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | "Keep references one level deep from SKILL.md." and "For reference files longer than 100 lines, include a table of contents at the top." and "head -100" | 2026-11-11 | 2027-02-11 |

## Sources

Rules here are in this skill's own words; each quote is a dated fact above.

| Source | Used for | License |
|---|---|---|
| [Diátaxis](https://diataxis.fr/) | The four kinds | Copyright Daniele Procida, no license stated: a short quote |
| [GitHub Docs](https://docs.github.com/) | Diagrams GitHub renders | CC BY 4.0: short quotes, attributed |
| [Mermaid](https://github.com/mermaid-js/mermaid), [Docusaurus](https://github.com/facebook/docusaurus), [Material](https://github.com/squidfunk/mkdocs-material), [Zensical](https://zensical.org/) | Versions, support, features | MIT: facts with short quotes |
| [MkDocs](https://www.mkdocs.org/), [Sphinx](https://www.sphinx-doc.org/) | Releases, autodoc, `linkcheck` | BSD-2-Clause: facts with short quotes |
| [Python docs](https://docs.python.org/3/library/doctest.html) | `doctest` | PSF License Version 2: a short quote, attributed |
| [The rustdoc book](https://doc.rust-lang.org/rustdoc/) | Doc tests | MIT or Apache-2.0: a short quote |
| [Django docs](https://docs.djangoproject.com/) | Docs in the same change | BSD-3-Clause: a short quote |
| [Anthropic's skill guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | How agents read long files | Anthropic's terms: short quotes, linked |
| This repository's checks, and audits of live repositories, unnamed | Checks in CI; lessons L29, L40, L44, L48 | Observed practice, in our own words |
