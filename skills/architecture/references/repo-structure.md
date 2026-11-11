# Repo structure

Read this for laying out or reorganizing a project: Python's src or flat layout, a Node
workspace, a .NET solution, a Go module, where tests go, feature or layer folders, naming files
and folders, one repository or several, and moving files without losing history.

The standard's *Project shapes and layout* gives each shape's source root, test root, entry
point and auxiliary files; this module covers what it leaves open. Each language's tooling is
its module in the `coding` skill, such as `python-coding`; ignore files are `gitignore`;
grouping commits is `commits-and-pull-requests`; Markdown file names are `writing-style`.

## Rules

1. **Start from the standard's shape, then the ecosystem's layout.** Where neither decides,
   record the convention chosen and its source in the context file, as the standard asks.
2. **Grow the layout with the code.** A folder arrives with its second file.
3. **Put files that change together in one folder,** keeping logic apart from I/O.
4. **Put tests where the runner looks,** and check that it finds them.
5. **Name for the contents,** in the ecosystem's case, portable, and stable once used.
6. **One repository per thing released together.**
7. **Move with `git mv`, in a commit of moves alone.**

### Layouts by ecosystem

- **Python:** the standard sets src. It keeps tests off the working tree (fact
  `py-src-layout`) at the cost of an install (fact `layout-src-install`), which `uv run` does.
  Scripts never installed need no package.
- **Node and TypeScript, several packages:** one workspace at the root, a folder per package
  under `packages/` with its own `package.json` (fact `layout-npm-workspaces`). In pnpm, a
  sibling dependency uses `workspace:`, so it never comes from the registry (fact
  `layout-pnpm-workspace`).
- **.NET:** the standard's `src/<Project>/` and `tests/<Project>.Tests/`, a folder per project,
  and one solution file, `.slnx` by default since .NET 10 (fact `layout-slnx`). IDE0130 holds
  namespaces to folders once a build can see `RootNamespace` and `ProjectDir` (fact
  `layout-ns-folder`).
- **Go:** go.dev's guidance: the package at the root, helpers in `internal/`, which other
  modules can't import, programs in `cmd/<name>/` (fact `layout-go-internal`). No `pkg/`:
  `golang-standards/project-layout` isn't official (fact `layout-go-unofficial`).

### Where tests go

| Ecosystem | Where | Fact |
|---|---|---|
| Python, C#, PowerShell, C, shell | The standard's test root for the shape | *Project shapes and layout* |
| Go | `x_test.go` beside `x.go`; fixtures in `testdata/` | `layout-go-tests` |
| Rust | Unit tests in each file's `tests` module; integration tests in `tests/` beside `src/` | `layout-rust-tests` |
| Node's runner | By default `*.test.js`, `*-test.js`, `*_test.js`, `test-*.js` and files under `test/`, not `tests/` | `layout-node-test-globs` |
| Angular | `*.spec.ts` in the folder of the code it tests | `layout-angular` |

### Feature or layer folders

Layer folders (`services/`, `models/`) pay while features are few. Past that, one feature's
change touches every layer folder, and feature folders (`billing/`) keep it in one (fact
`layout-angular`). Where the standard names a shape's folders, keep them, and group by feature
inside them.

### Names

- **Case:** Python modules short and lowercase (fact `layout-pep8-modules`); Go packages
  lowercase, no underscores or mixed case (fact `layout-go-pkg-names`); TypeScript files
  hyphenated (fact `layout-angular`); C# folders follow namespaces (fact `layout-ns-folder`);
  PowerShell, the standard's file per function.
- **Portable:** no spaces, no two names that differ only in case, no device names such as
  `con` or `aux`, and no name ending in a space or a period (fact `layout-win-names`).
- **Specific:** no `utils`, `common`, `misc` or `helpers`: the name says nothing of what's in
  it (fact `layout-go-pkg-names`).
- **Stable:** an import path, URL or script others call is an interface; rename it with a
  deprecation or a redirect.

### One repository or several

The standard says to start with one deployable unit (*Choosing the shape*) and to share code
between repositories through a package registry (*Cross-repository contracts*). Beyond that:

- **Split** when parts differ in visibility, owner or release cycle, or outsiders consume one.
- **Merge** when every change needs a pull request in both, or their versions move in lockstep.
- **Either way,** each dependency has one version across the whole (fact `layout-one-version`).

### Moving files

Git records no rename; it pairs a delete with an add that's similar enough (fact
`layout-git-renames`). Run `git mv`, commit the moves alone, then fix imports, links, CI paths
and the context file's layout section, found by searching for the old path. `git log --follow
-- <file>` reads history across the move (fact `layout-git-follow`).

## Mistakes

- **Copying `golang-standards/project-layout`** for a small program: `pkg/`, `cmd/` and
  `internal/` around one package. Start from go.dev's simplest layout.
- **Scaffolding empty folders for later,** such as `utils/` and `common/`, as AI assistants
  do. Add a folder when its second file arrives.
- **Layer folders in a growing app,** where each feature change edits `controllers/`,
  `services/`, `models/` and `dtos/`. Group by feature.
- **Tests in `tests/` under Node's runner,** named `parser.js`: `node --test` matches none
  (fact `layout-node-test-globs`). Name them `*.test.js`, or pass the glob.
- **`Readme.md` beside `README.md`, or a file named `aux.ts`:** a Windows checkout collides or
  fails (fact `layout-win-names`).
- **Splitting a repository for tidiness,** then opening two pull requests for every change.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Layout follows neither the standard's shape nor the ecosystem's | The tree against *Project shapes and layout* and the facts here | `DRIFT` | Move, or record the convention followed and why |
| Tests the runner doesn't find | The runner's test count against the test files in the tree | `BLOCKER` where CI passes anyway | Rename the files, or give the runner the glob |
| Skeleton or generic folders | Empty folders held by `.gitkeep`; `utils/`, `common/`, `misc/` | `OVER` when empty, `DRIFT` when generic | Delete, or name for the contents |
| Names that break on another system | `git ls-files \| sort -f \| uniq -di`; spaces, device names, trailing periods | `GAP` | Rename with `git mv` |
| .NET namespaces don't follow folders | IDE0130 off, or on without the two `CompilerVisibleProperty` items | `GAP` | Turn it on with both (fact `layout-ns-folder`) |
| Two repositories that change together | Paired pull requests across both histories | `OVER` | Merge, or record what forces the split |

## Why

### Ecosystem first, grown not scaffolded

- **The reason:** people, tools and agents look where the ecosystem says, and Node's runner
  finds only its own patterns. An empty folder guesses at code that doesn't exist; `utils/`
  grows into a package nobody can name (fact `layout-go-pkg-names`).
- **What others do:** go.dev grows a module in stages (fact `layout-go-internal`). A
  contributor arrives knowing their language's convention, not a house one.
- **What it costs:** one house layout across languages, and a later move, which `git mv` makes
  cheap.
- **When to choose differently:** a framework that requires its folders, or a shape no
  ecosystem covers: choose, and record it.

### Feature folders

- **The reason:** a change is easier to review in one folder than across four.
- **What others do:** Angular groups by feature, tests beside the code (fact `layout-angular`);
  the standard's Python service shape uses layers, which suits few features.
- **What it costs:** shared code needs a home, and the layer boundary is kept by review.
- **When to choose differently:** a small service, or a library whose layers are its API.

### Portable, stable names

Windows treats names differing only in case as one, and reserves device names (fact
`layout-win-names`), so a name fine on Linux can fail a colleague's checkout. A renamed import
path breaks every caller. Before anyone depends on a name, rename freely.

### Repository boundaries

- **The reason:** the boundary decides what moves together. Two repositories that change
  together cost two pull requests and a version kept in step; one holding parts on separate
  release cycles ties each release to unrelated work. This repository's owner keeps company
  detail in a private companion repository: a split forced by visibility.
- **What others do:** Google's book calls the choice each organization's, and one version of
  each dependency the part that matters (fact `layout-one-version`).
- **What it costs:** one repository needs tooling to test only what changed; several need a
  registry and version bumps.

### Moves on their own

Git infers renames from similarity (fact `layout-git-renames`), so a move with a rewrite can
read as a delete and an add, and `--follow` stops there. `commits-and-pull-requests` gives mass
renames their own commit too, for review. The cost is one more commit.

## Facts

Versions, defaults and guidance, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `layout-src-install` | src needs an install to run | [PyPA](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) | "The src layout requires installation of the project to be able to run its code, and the flat layout does not." | 2026-11-11 | 2027-05-11 |
| `layout-npm-workspaces` | npm workspaces: packages under one root | [npm](https://docs.npmjs.com/cli/v11/using-npm/workspaces) | "managing multiple packages from your local file system from within a singular top-level, root package" | 2026-11-11 | 2027-02-11 |
| `layout-pnpm-workspace` | `workspace:` resolves only locally | [pnpm](https://pnpm.io/workspaces) | "pnpm will refuse to resolve to anything other than a local workspace package" | 2026-11-11 | 2027-02-11 |
| `layout-slnx` | `.slnx` by default from .NET 10 | [Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/compatibility/sdk/10.0/dotnet-new-sln-slnx-default) | "Starting in .NET 10, dotnet new sln creates a SLNX-format solution file" | 2026-11-11 | 2027-02-11 |
| `layout-ns-folder` | IDE0130 matches namespaces to folders; command-line builds need two properties | [IDE0130](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/ide0130) | "uses the folder structure of the project to enforce namespace naming requirements" and "not available for command-line builds" | 2026-11-11 | 2027-05-11 |
| `layout-go-internal` | Go: helpers in `internal/`, programs in `cmd/` | [go.dev](https://go.dev/doc/modules/layout) | "Since other projects cannot import code from our internal directory" and "keep all Go commands together in a cmd directory" | 2026-11-11 | 2027-05-11 |
| `layout-go-unofficial` | `project-layout` isn't the Go team's | [GitHub](https://github.com/golang-standards/project-layout) | "NOT an official standard defined by the core Go dev team" | 2026-11-11 | 2027-05-11 |
| `layout-go-tests` | `*_test.go` and `testdata/` | [cmd/go](https://pkg.go.dev/cmd/go) | "with names matching the file pattern" and "available to hold ancillary data needed by the tests" | 2026-11-11 | 2027-05-11 |
| `layout-rust-tests` | Rust: a `tests` module per file, and `tests/` | [Rust book](https://doc.rust-lang.org/book/ch11-03-test-organization.html) | "create a module named tests in each file" and "We create a tests directory at the top level of our project directory, next to src" | 2026-11-11 | 2027-05-11 |
| `layout-node-test-globs` | `node --test` runs its default patterns, which match `test/`, not `tests/` | [Node](https://nodejs.org/api/test.html) | "By default, Node.js will run all files matching these patterns" | 2026-11-11 | 2027-02-11 |
| `layout-angular` | Angular: feature folders, tests beside code, hyphens | [Angular](https://angular.dev/style-guide) | "based on the features of your application" and "Unit tests should live in the same directory as the code-under-test." and "Separate words within a file name with hyphens" | 2026-11-11 | 2027-05-11 |
| `layout-pep8-modules` | Python modules: short, lowercase | [PEP 8](https://peps.python.org/pep-0008/) | "Modules should have short, all-lowercase names." | 2026-11-11 | 2027-05-11 |
| `layout-go-pkg-names` | Go packages: lowercase, never generic | [go.dev](https://go.dev/blog/package-names) | "They are lower case, with no under_scores or mixedCaps" and "provide clients with no sense of what the package contains" | 2026-11-11 | 2027-05-11 |
| `layout-win-names` | Windows: no case, device names or trailing space or period | [Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file) | "Do not assume case sensitivity." and "reserved names for the name of a file: CON, PRN, AUX, NUL" and "Do not end a file or directory name with a space or a period." | 2026-11-11 | 2027-05-11 |
| `layout-git-renames` | Renames are detected at 50% similarity | [git diff](https://git-scm.com/docs/git-diff) | "consider a delete/add pair to be a rename" and "The default similarity index is 50%." | 2026-11-11 | 2027-05-11 |
| `layout-git-follow` | `--follow` crosses renames | [git log](https://git-scm.com/docs/git-log) | "Continue listing the history of a file beyond renames" | 2026-11-11 | 2027-05-11 |
| `layout-one-version` | Google: one repository or many is yours to choose; one version matters more | [SWE at Google](https://abseil.io/resources/swe-book/html/ch16.html) | "These are decisions you'll need to make yourself." and "developers must not have a choice when adding a dependency onto some library that is already in use" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Packaging User Guide](https://packaging.python.org/) | src and flat | CC BY-SA 3.0: short quotes, attributed |
| [npm](https://docs.npmjs.com/), [pnpm](https://pnpm.io/), [go.dev](https://go.dev/), [project-layout](https://github.com/golang-standards/project-layout) | Workspaces, Go | Not stated: short quotes only |
| [Microsoft Learn](https://learn.microsoft.com/dotnet/) | .NET, Windows names | CC BY 4.0 text, MIT code: short quotes, attributed |
| [Rust book](https://doc.rust-lang.org/book/), [Node.js docs](https://nodejs.org/api/) | Where tests go | MIT or Apache-2.0; MIT: short quotes |
| [Angular style guide](https://angular.dev/style-guide) | Folders, tests, names | CC BY 4.0: short quotes, attributed |
| [PEP 8](https://peps.python.org/pep-0008/) | Python names | Public domain |
| [Git documentation](https://git-scm.com/docs) | Renames | GPL-2.0: our own words, short quotes |
| [SWE at Google, ch. 16](https://abseil.io/resources/swe-book/html/ch16.html) | Repository boundaries | CC BY-NC-ND 4.0: quoted, never adapted |
| This repository's own practice | A private companion repository | Our own words |
