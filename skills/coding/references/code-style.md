# Code style

Read this for naming a variable, function or type, formatting code and adopting a formatter,
deciding when a function or file is too long, writing comments, TODOs and docstrings, removing
dead or commented-out code, and matching the style around a change, in any language; and for
reviewing code on any of these.

The contract's first two rules, read before you write and make the smallest change, apply here;
this module says what to match and how. Each language module names its formatter and linter:
`python-coding` (Ruff), `javascript-coding`, `csharp-coding` (`dotnet format`),
`powershell-scripts` (PSScriptAnalyzer) and `bash-coding` (shfmt). What a type annotation says
is `types`. File and folder names are the standard's *Project shapes and layout* and a planned
`repo-structure` module; redesign beyond a function is a planned `architecture-and-design`
module. Prose and Markdown are house-style.

## Rules

1. **The nearest code's style wins: the function, the file, the project, then the ecosystem's
   guide.** Your taste comes last (fact `style-pep8`).
   Change a project's convention on purpose, everywhere at once, in a change of its own.
2. **A name says what a thing is or does, in its ecosystem's case.** Whole words, apart from
   abbreviations every reader knows (`id`, `url`) and the project's own terms. Length grows
   with scope: `i` in a three-line loop, `pending_invoices` across a module (fact
   `style-google-names`). One word per concept across the code base.
3. **The formatter formats; nobody formats by hand.** Run the project's formatter on the files
   you change, and its check in CI. A reformat of code you didn't otherwise change goes in its
   own commit, listed in `.git-blame-ignore-revs` (fact `style-blame-ignore`).
4. **A function does one thing at one level of detail.** Length and nesting are smells, with no
   fixed limit (facts `style-google-length`, `style-kernel`). Return early rather than nest. A
   complexity score is a prompt to look, never a target (fact `style-clippy-cognitive`).
5. **A comment says why; the code says what.** Write the reason, the constraint, the rejected
   option, where a number came from, and the bug a workaround works around, with its link.
   Change the comment in the same change as the code (fact `style-pep8`).
6. **Every public name gets a doc comment in its ecosystem's format:** what it does, takes,
   returns and raises, and any side effect. Types go in the signature where the language has
   them.
7. **Delete dead and commented-out code.** Version control keeps it (fact `style-ruff-era`).
8. **A style rule that matters is checked by a tool.** One left to review or a prompt drifts.

### Names

- Booleans read as a question: `is_ready`, `has_rows`. A unit the type doesn't carry goes in
  the name: `timeout_ms`, `size_bytes`. A function is a verb phrase, a value a noun phrase.
- `data`, `info`, `manager`, `helper` or `utils` alone say nothing. No type in a name
  (`strName`, `user_list`) where the type system holds it.
- Acronyms follow the ecosystem, and ecosystems disagree: `ServeHTTP` in Go, `Uuid` in Rust,
  `IOStream` but `HtmlParser` in .NET (fact `style-acronyms`).
- A public name is an interface: renaming it breaks callers, so it gets its own change, with a
  deprecation where the ecosystem has one.

### Comments and TODOs

- No comment narrates the next line (`# loop over users`) or speaks to the reviewer (`# fixed`,
  `# new helper`). That belongs in the commit message.
- A TODO names its issue: `TODO(#123): drop once the API returns UTC` (fact `style-google-todo`).
  One with no issue is a wish nobody tracks: file the issue, or delete the TODO.

### Doc comments by ecosystem

| Language | Format | A public item's doc holds | Checked by |
|---|---|---|---|
| Python | PEP 257 docstrings, Google or NumPy sections | Summary line, Args, Returns, Raises | Ruff `D` rules, such as `D103` |
| TypeScript, JavaScript | JSDoc; TSDoc for TypeScript | `@param`, `@returns`, `@throws` | eslint-plugin-jsdoc or eslint-plugin-tsdoc |
| C# | XML comments, `///` | `<summary>`, `<param>`, `<returns>`, `<exception>` | `CS1591`, once docs are generated |
| PowerShell | Comment-based help | `.SYNOPSIS`, `.DESCRIPTION`, `.PARAMETER`, `.EXAMPLE` | `Get-Help` shows it |
| Go | A comment starting with the name, on every exported name | What it does | `go doc` |
| Rust | rustdoc, `///` in Markdown | `# Errors`, `# Panics`, `# Safety` | `missing_docs` lint |
| Bash | A header comment per function (Google's shell guide) | Globals, Arguments, Outputs, Returns | None |
| C | The project's: Doxygen, or kernel-doc in Linux | Ownership, errors, thread safety | Doxygen |

## Mistakes

- **Reformatting a file to fix one line.** The fix hides among hundreds of changed lines, and
  `git blame` loses each line's history. Format what you touched; sweep in its own commit.
- **A new helper, or a built-in, where the project already has a function.** It is the most
  common way model-written code departs from the code around it (fact
  `style-llm-api-preference`). Search the project for the task's verbs first.
- **One ecosystem's habits in another:** `snake_case` methods in C#, `UUID` in a Rust type,
  `ServeHttp` in Go.
- **A comment that restates the code, or a docstring that repeats the signature.** Both go
  stale, and teach readers to skip comments, the useful ones too.
- **Commented-out code kept "in case."** Nobody knows whether it still compiles, or why it's
  there. A feature flag with an issue and a removal date is the honest form.
- **Splitting a function into one-call fragments to quiet a complexity rule.** The reader now
  jumps between five functions to follow one idea. Split where the meaning splits.
- **Renaming in the same change as a fix.** Review can't see either clearly.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| No formatter check in CI | A `--check`, `--verify-no-changes` or `-d` step per language | `GAP` | Add the language module's check |
| The tree fails its own formatter | The check, run locally | `DRIFT` | Reformat in one commit, listed in `.git-blame-ignore-revs` |
| A reformat mixed with a behavior change | `git show --stat` on the change's commits | `DRIFT` | Split it in two |
| Commented-out code | Ruff `ERA001`, or comment lines that parse as code | `DRIFT` | Delete it |
| TODOs without an issue | `git grep -n -E 'TODO\|FIXME'`, or Ruff `TD003` | `GAP` | Link an issue, or delete it |
| Public names without docs | The table's checker | `GAP` in a library or shared module | Write them; turn the checker on |
| Names off the project's convention | The linter's naming rules, then a read | `DRIFT` | Rename in its own commit |
| A function far longer or deeper than its neighbors | Length, nesting, complexity output | `OVER` | Split by meaning, in its own change |

## Why

### Consistency with the code around it

- **The reason:** a reader learns a file's conventions on its first screen and reads the rest
  by them; a change in another idiom costs every later reader a second look. PEP 8 ranks
  consistency in one function above PEP 8 itself (fact `style-pep8`). Models drift from a
  project most by re-implementing what it has (fact `style-llm-api-preference`).
- **What it costs:** an old convention you'd not choose lives on. **Choose differently** when
  the project decides to change: everywhere, in one sweep, recorded in its linter config.

### Names

- **The reason:** whole-word names helped 72 professional developers find defects about a fifth
  faster than letters or abbreviations (fact `style-names-study`).
- **What others do:** other studies found no difference, so the effect is modest. The Linux
  kernel wants short local names and descriptive global ones (fact `style-kernel`), close to
  Google's length by scope (fact `style-google-names`).
- **What it costs:** longer lines. **Choose differently** for a loop variable, or a name that
  matches the notation of a paper or formula the code implements.

### The formatter, and reformatting apart

- **The reason:** a formatter ends layout debate, which Go built into its tools (fact
  `style-gofmt`). A reformat mixed into a fix can't be reviewed, as the standard's *Review, with
  one maintainer* says. `.git-blame-ignore-revs` keeps `git blame` on the change that wrote each
  line (fact `style-blame-ignore`).
- **What it costs:** the formatter's choices over yours, and one large commit on adoption.
  **Choose differently** for a file kept byte for byte the same as another repository's. A
  project with no formatter keeps its layout until the owner adopts one, apart from any
  feature.

### Size and complexity

- **The reason:** a long, nested function holds more state than a reader can track. Google
  asks for a second look past about 40 lines (fact `style-google-length`); the kernel ties the
  limit to complexity and nesting, so a long flat `switch` can be fine (fact `style-kernel`).
  Clippy keeps its complexity lint out of the defaults, since no score measures understanding
  (fact `style-clippy-cognitive`).
- **Files:** the standard's *File governance* budgets context and rule files, not source. A
  source file's size is a smell: a file holds one topic, and two unrelated topics split.
- **What it costs:** more names to jump between. **Choose differently** where a split would
  separate steps that only make sense together.

### Comments, doc comments and dead code

- **The reason:** the code shows what it does; only a comment keeps why, which the next person
  needs before changing it. A stale comment misleads (fact `style-pep8`). The kernel says
  comment what, not how (fact `style-kernel`): both rule out narrating the code. Dead code is
  read and maintained like live code, and nobody knows if it still works (fact
  `style-ruff-era`).
- **Tools over review:** a rule only reviewers enforce is enforced unevenly, and a model
  forgets it between sessions; a linter doesn't.
- **What it costs:** comments to keep current. **Choose differently** for a private helper
  whose name and signature say everything.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `style-pep8` | PEP 8 ranks local consistency first, and a stale comment below none | [PEP 8](https://peps.python.org/pep-0008/) | "Consistency within one module or function is the most important." and "Comments that contradict the code are worse than no comments." | 2026-11-11 | 2027-05-11 |
| `style-google-names` | Google: name length grows with scope | [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) | "descriptiveness should be proportional to the name's scope of visibility." | 2026-11-11 | 2027-05-11 |
| `style-google-length` | Google: look again past about 40 lines | [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) | "If a function exceeds about 40 lines, think about whether it can be broken up" | 2026-11-11 | 2027-05-11 |
| `style-google-todo` | Google: a TODO links its context | [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) | "a parenthesized link to a resource that contains the context, ideally a bug reference" | 2026-11-11 | 2027-05-11 |
| `style-kernel` | Linux: length by complexity, short locals, comments say what | [Kernel coding style](https://www.kernel.org/doc/html/latest/process/coding-style.html) | "inversely proportional to the complexity and indentation level" and "LOCAL variable names should be short" and "tell WHAT your code does, not HOW" | 2026-11-11 | 2027-05-11 |
| `style-clippy-cognitive` | Clippy's complexity lint isn't a measure | [Clippy lints](https://rust-lang.github.io/rust-clippy/master/index.html) | "so as to not mislead users into using this lint as a measurement tool" | 2026-11-11 | 2027-02-11 |
| `style-gofmt` | Go leaves layout to `gofmt` | [Effective Go](https://go.dev/doc/effective_go) | "let the machine take care of most formatting issues" | 2026-11-11 | 2027-05-11 |
| `style-acronyms` | Go, Rust and .NET case acronyms differently | [Go](https://go.dev/wiki/CodeReviewComments), [Rust](https://rust-lang.github.io/api-guidelines/naming.html), [.NET](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/capitalization-conventions) | "ServeHTTP not ServeHttp" and "use Uuid rather than UUID" and "A special case is made for two-letter acronyms" | 2026-11-11 | 2027-05-11 |
| `style-ruff-era` | Ruff: commented-out code is dead code | [Ruff ERA001](https://docs.astral.sh/ruff/rules/commented-out-code/) | "Commented-out code is dead code, and is often included inadvertently." | 2026-11-11 | 2027-02-11 |
| `style-blame-ignore` | Git and GitHub skip listed commits in blame | [git blame](https://git-scm.com/docs/git-blame), [GitHub](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files) | "Ignore changes made by the revision when assigning blame" and "are hidden from the blame view" | 2026-11-11 | 2027-02-11 |
| `style-llm-api-preference` | Models most often skip the project's own functions | [Wang et al., FSE 2025](https://arxiv.org/html/2407.00456) | "API Preference Inconsistency stands out with a significantly higher frequency" and "re-implementing the functionality without calling existing functions" | 2026-11-11 | 2027-05-11 |
| `style-names-study` | Words beat abbreviations by about 19%; other studies found no difference | [Never Work in Theory](https://neverworkintheory.org/2021/08/09/abbreviated-vs-full-names.html) | "words lead to, on average, 19% faster comprehension speed" and "found no difference in development effort or efficiency" | 2026-11-11 | 2027-05-11 |

## Sources

Rules in our own words; quotes short and attributed.

| Source | Used for | License |
|---|---|---|
| [PEP 8](https://peps.python.org/pep-0008/), [PEP 257](https://peps.python.org/pep-0257/) | Consistency, comments, docstrings | Public domain |
| [Google style guides](https://google.github.io/styleguide/) | Names, length, TODOs, shell headers | CC BY 3.0 (fact `sh-google-license`) |
| [Kernel coding style](https://www.kernel.org/doc/html/latest/process/coding-style.html) | Length, names, comments | GPL-2.0: short quotes |
| [Go docs](https://go.dev/doc/) | `gofmt`, doc comments, initialisms | CC BY 4.0 text, BSD code |
| [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/), [Clippy](https://rust-lang.github.io/rust-clippy/) | Acronyms, doc sections, complexity | MIT or Apache-2.0 |
| [Microsoft Learn](https://learn.microsoft.com/dotnet/) | .NET acronyms | CC BY 4.0 text, MIT code |
| [Ruff](https://docs.astral.sh/ruff/rules/) | `ERA001`, `D103`, `TD003` | MIT |
| [git](https://git-scm.com/docs/git-blame), [GitHub Docs](https://docs.github.com/) | Ignoring commits in blame | GPL-2.0; CC BY 4.0 |
| [Wang et al.](https://arxiv.org/abs/2407.00456) | Model-written code against a project's style | arXiv license: short quotes |
| [Never Work in Theory](https://neverworkintheory.org/2021/08/09/abbreviated-vs-full-names.html) | Naming studies, with Hofmeister et al.'s abstract | None stated: short quotes |
