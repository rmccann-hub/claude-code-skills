# Python coding

Read this for writing, reviewing or fixing Python 3 code: `pyproject.toml`, uv, Ruff and a type
checker, type hints, idioms, encodings, time zones, and which Python versions to target.

Untrusted input, from shells to paths and secrets, is `python-security`'s. Releases, lockfiles and
CI are the project-bootstrap-and-audit standard's *Language toolchains*; test design is the testing
skill's. Retries are `error-handling`, pinning dependencies `supply-chain-security`, async
`performance-and-concurrency`, and time zone policy beyond Python's API `internationalization`.
pandas and NumPy belong to a planned data skill, and Python 2 to `legacy-languages`.

## Rules

1. **Set a new project up with `pyproject.toml`, uv and the src layout,** and run every tool
   through `uv run`. A one-file script declares its dependencies inline. A build that already
   locks and pins stays (Why 1).
2. **Lint and format with Ruff, and turn on its security and time zone rules** (`S`, `DTZ`),
   most of which its defaults leave out.
3. **Annotate new code, and check it with a type checker in strict mode.**
4. **Use aware datetimes:** UTC inside the program, `zoneinfo` at its edges, never `utcnow()`.
5. **Name the encoding on every text file you open, and every `subprocess` call in text mode.**
6. **Declare the oldest Python you test in `requires-python`,** such as `>=3.12` if that's 3.12,
   with no upper bound. Supported branches are the standard's *Language toolchains*: 3.10 has
   ended, and 3.11 ends in 2027-10 (facts `py-eol-310`, `py-eol-311`).

### The project and its tools

- **`pyproject.toml` holds the project:** `[project]`, `requires-python`, a `dev` dependency
  group for Ruff, pytest and the type checker, kept out of the built package (fact
  `py-dep-groups`), and each tool's settings under `[tool.*]`.
- **The src layout** puts the package under `src/<name>/` (fact `py-src-layout`). `uv init`
  creates it, with a build system, since uv 0.12 (fact `py-uv-init`).
- **Run tools through uv,** as `uv run mypy`, at the versions the lockfile pins.
  `uv add --dev ruff` adds one to the group.
- **A one-file script** carries a `# /// script` block of its `requires-python` and
  dependencies (fact `py-inline-script`), written by `uv add --script`.

Ruff reads its target version from `requires-python` (fact `py-ruff-target`):

```toml
[project]
name = "example-tool"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
example-tool = "example_tool.cli:main"

[dependency-groups]
dev = ["mypy", "pytest", "ruff"]

[tool.ruff.lint]
extend-select = ["S", "DTZ"]

[tool.mypy]
strict = true
```

### Types

- **Annotate every new function's parameters and return.** mypy skips the body of an
  unannotated function (fact `py-mypy-untyped`).
- **Strict mode** is `strict = true` under `[tool.mypy]`, or each flag it sets, a list that
  can change (fact `py-mypy-untyped`). Pyrefly is stable (fact `py-pyrefly-stable`); ty is in
  beta (fact `py-ty-beta`), so not a project's only gate.
- **Write current syntax:** `list[str]`, `X | None`, and the `type` statement for an alias from
  3.12 (fact `py-type-stmt`). Ruff's `UP` rules rewrite the old forms.

### Idioms

- **A mutable default is shared across calls** (fact `py-mutable-default`): default to `None`,
  as below. Ruff's `B006` catches it.
- **Pass `encoding="utf-8"` to every text `open()`,** `read_text()` and `write_text()`, and to
  `subprocess` in text mode the command's own, usually UTF-8, with `errors="replace"`
  where bad bytes may pass (fact `py-subprocess-text`). 3.15 made UTF-8 the default, and still asks
  for it: older Pythons use the locale's (fact `py-utf8-default`).
- **Use `pathlib` for paths,** and `with` for anything that must be closed.

```python
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    tags = [] if tags is None else tags
    tags.append(tag)
    return tags
```

### Time zones

- **`datetime.now(UTC)`, never `utcnow()`,** which returns a naive value and is deprecated
  (fact `py-utcnow`). Store, compare and compute in UTC.
- **`ZoneInfo("America/New_York")` for a named zone,** at input and display. Declare `tzdata`
  where there's no time zone database, as on Windows (fact `py-tzdata`).
- **Naive and aware values don't mix:** subtracting or ordering them raises `TypeError`.
- **Adding a `timedelta` to a local time moves the wall clock,** not elapsed time. Across a
  daylight-saving change, "a day later" in New York is 25 hours on:

```python
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

NEW_YORK = ZoneInfo("America/New_York")

stamp = datetime(2026, 11, 1, 4, 30, tzinfo=UTC)
local = stamp.astimezone(NEW_YORK)
print(local)  # 2026-11-01 00:30:00-04:00

print(local + timedelta(days=1))  # 2026-11-02 00:30:00-05:00, 25 hours on
print((stamp + timedelta(days=1)).astimezone(NEW_YORK))  # 2026-11-01 23:30:00-05:00
```

## Mistakes

- **`datetime.utcnow()`, or `datetime.now()` with no zone,** compared with an aware value: a
  `TypeError`, or a local time stored with nothing to say so. Use `datetime.now(UTC)`.
- **"Same time tomorrow" as 24 hours in UTC, or "24 hours on" as a day in local time.** Wall
  clock goes in the local zone, elapsed time in UTC.
- **`open(path)` or `run(…, text=True)` with no encoding,** read differently before 3.15 on
  a non-UTF-8 locale.
- **`def f(items=[])`,** which every call shares.
- **Adding mypy to unannotated code and calling it typed,** or trusting Ruff's defaults to find
  security problems.
- **`from typing import List, Optional`** in new code, or an upper bound such as `<3.15` in
  `requires-python`, which blocks every user of the next release.

## Audit

Severity uses the standard's status words. `DTZ` is Ruff's; the `S` checks are
`python-security`'s.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Naive datetimes | `DTZ` | `GAP` | `datetime.now(UTC)`, `zoneinfo` (facts `py-utcnow`, `py-naive-aware`) |
| Text opened with no encoding | `open(`, `read_text(`, `write_text(` or `text=True` with no `encoding=`: `PLW1514`, then the grep below | `GAP` | `encoding="utf-8"`, or what the command writes (facts `py-utf8-default`, `py-subprocess-text`) |
| Ruff's security and time zone rules | `[tool.ruff.lint]` without `S` and `DTZ` | `GAP` | `extend-select = ["S", "DTZ"]` |
| No type checker, or not strict | No mypy or Pyrefly settings; mypy with neither `strict = true` nor every flag it sets | `GAP` | Strict mode, raised module by module |
| Empty suppressions | `RUF100`: a `noqa` code unused, or for a rule not enabled | `DRIFT` | Delete it, or enable the rule (fact `py-ruff-unused-noqa`) |
| A type check that checks nothing | A type checker in CI over unannotated code | `DRIFT` | Annotate, or `disallow_untyped_defs` (fact `py-mypy-untyped`) |
| `requires-python` | Missing, with an upper bound, or naming an ended branch | `GAP` | `>=` the oldest version you test (facts `py-requires-upper`, `py-eol-310`) |

`PLW1514` is in preview, and misses `subprocess` and paths it can't type (fact
`py-ruff-plw1514`). This finds those, with false hits such as a binary `open`:

```sh
git grep -nE '\b(open|read_text|write_text)\(|text=True|universal_newlines=True' -- '*.py' |
  grep -v 'encoding='
```

## Why

**1. `pyproject.toml`, uv and the src layout.** They give one resolver, a lock, a pinned interpreter
and a declared floor. With the package at the root, tests import the working tree and pass against
files the built package leaves out (fact `py-src-layout`), and `uv run` uses the locked environment,
not whatever is installed. Poetry, which the standard also supports, gives all four, as do
pip-tools' hashed requirements beside a bundler such as PyInstaller; the flat layout runs without an
install. Cost: an install before the code runs, which `uv run` does each time. Otherwise: a build
giving all four stays. Dependency-free scripts in a project in another language need no package: a
Ruff config in their directory (fact `py-ruff-target`) with `target-version` at the oldest Python
you test, named in the context file too.

**2. Ruff, with `S` and `DTZ`.** Ruff's defaults catch classic mistakes such as a mutable default
(fact `py-ruff-defaults`), but not `shell=True` (`S602`) or `datetime.now()` with no zone (`DTZ005`)
(fact `py-ruff-security-off`). Others run flake8 with plugins, isort and Black, which Ruff replaces,
and Bandit, from which the `S` rules derive. Cost: `S603` and `S607` flag safe calls too: see
`python-security`. Otherwise: a project on flake8 and Black can stay, and add Bandit.

**3. Annotations and strict checking.** A checker sees only what's annotated, so an unannotated
module passes unchecked; strict mode finds `Any` leaking from parsed data, `None` where a value is
needed, and missing returns. Many type gradually, strict for new modules and lenient for old, as
mypy's guide to existing code describes. Cost: time, and on old code, hundreds of errors at once.
Otherwise: on a large untyped codebase, start with `disallow_untyped_defs` per module, and raise the
rest module by module.

**4. Aware datetimes, UTC inside.** A naive value doesn't say which clock it's on, mixing the two
raises `TypeError` (fact `py-naive-aware`), and local arithmetic moves the wall clock (fact
`py-wall-clock`), so durations come out an hour off twice a year. Cost: converting at the edges,
and `tzdata` on Windows. Otherwise: a calendar's "every morning at nine" is a wall-clock rule:
keep the local time and its zone, and compute each occurrence in that zone.

**5. An explicit encoding.** Before 3.15 the default is the locale's, so the same code reads a
file or a command's output differently on another machine. Cost: a keyword per call.

**6. `requires-python`.** An upper bound blocks every user of the next release (fact
`py-requires-upper`), and a floor below what you test promises what nobody checked. Otherwise:
an application on one known interpreter pins it in `.python-version`, which `uv init` writes.

**Suppressions.** A `noqa` records a hand check; one for a rule not enabled records a check
nothing runs.

## Facts

Each named here by its ID; `python-security` holds `py-subprocess-text` and the Ruff
facts.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `py-eol-311` | 3.11 gets security fixes until 2027-10 | [versions](https://devguide.python.org/versions/) | "3.11 PEP 664 security 2022-10-24 2027-10" | 2026-10-26 | 2027-04-26 |
| `py-eol-310` | 3.10 ended on 2026-10-01 | [versions](https://devguide.python.org/versions/) | "3.10 PEP 619 end-of-life 2021-10-04 2026-10-01" | 2026-10-26 | 2027-04-26 |
| `py-uv-init` | `uv init` uses `src/` and a build system, for applications since uv 0.12 | [uv init](https://docs.astral.sh/uv/concepts/projects/init/) | "place source files in a dedicated src/" and "Prior to v0.12, uv did not define a build system for applications by default" | 2026-10-26 | 2027-04-26 |
| `py-src-layout` | src keeps the working tree off the import path | [src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) | "prevent accidental usage of the in-development copy" | 2026-10-26 | 2027-10-26 |
| `py-dep-groups` | Dependency groups stay out of the built package | [groups](https://packaging.python.org/en/latest/specifications/dependency-groups/) | "not included in project metadata when it is built" | 2026-10-26 | 2027-10-26 |
| `py-inline-script` | A script can declare dependencies inline | [inline](https://packaging.python.org/en/latest/specifications/inline-script-metadata/) | "can be embedded in single-file Python scripts" | 2026-10-26 | 2027-10-26 |
| `py-requires-upper` | The guide warns against an upper bound | [pyproject](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) | "Think twice before applying an upper bound" | 2026-10-26 | 2027-10-26 |
| `py-mypy-untyped` | mypy skips unannotated bodies; `--strict`'s flags may change | [mypy](https://mypy.readthedocs.io/en/stable/command_line.html) | "the bodies of functions without annotations are not type checked" and "the exact list of flags enabled by running --strict may change over time" | 2026-10-27 | 2027-04-27 |
| `py-pyrefly-stable` | Pyrefly: stable on PyPI | [pyrefly](https://pypi.org/pypi/pyrefly/json) | "Development Status :: 5 - Production/Stable" | 2026-10-26 | 2027-04-26 |
| `py-ty-beta` | ty: beta on PyPI | [ty](https://pypi.org/pypi/ty/json) | "Development Status :: 4 - Beta" | 2026-10-26 | 2027-04-26 |
| `py-type-stmt` | The `type` statement arrived in 3.12 | [statements](https://docs.python.org/3/reference/simple_stmts.html) | "type is a soft keyword." and "Added in version 3.12." | 2026-10-26 | 2027-10-26 |
| `py-mutable-default` | A default argument is evaluated once | [tutorial](https://docs.python.org/3/tutorial/controlflow.html) | "evaluated only once" | 2026-10-26 | 2027-10-26 |
| `py-utf8-default` | 3.15 defaults to UTF-8, and still asks for an explicit one | [3.15](https://docs.python.org/3/whatsnew/3.15.html) | "Python now uses UTF-8 as the default encoding" and "an explicit encoding argument is always provided" | 2026-10-26 | 2027-04-26 |
| `py-utcnow` | `utcnow()` returns a naive value, deprecated since 3.12 | [datetime](https://docs.python.org/3/library/datetime.html) | "with tzinfo None." and "Deprecated since version 3.12" | 2026-10-26 | 2027-10-26 |
| `py-naive-aware` | Subtracting naive from aware raises `TypeError` | [datetime](https://docs.python.org/3/library/datetime.html) | "If one is aware and the other is naive, TypeError is raised." | 2026-10-26 | 2027-10-26 |
| `py-wall-clock` | Adding a `timedelta` makes no time zone adjustment | [datetime](https://docs.python.org/3/library/datetime.html) | "no time zone adjustments are done" | 2026-10-26 | 2027-10-26 |
| `py-tzdata` | `zoneinfo` may need `tzdata`, as on Windows | [zoneinfo](https://docs.python.org/3/library/zoneinfo.html) | "declare a dependency on tzdata" | 2026-10-26 | 2027-10-26 |

## Sources

The rules and examples are this module's own words and code.

| Source | Used for | License |
|---|---|---|
| [Python docs](https://docs.python.org/3/) and [Developer's Guide](https://devguide.python.org/) | `datetime`, `zoneinfo`, encodings, idioms; end-of-life dates | PSF License Version 2, and CC0 1.0 for the guide: short quotes, attributed |
| [Packaging User Guide](https://packaging.python.org/) | src layout, dependency groups, inline metadata, `requires-python` | CC BY-SA 3.0: short quotes, attributed, the rest in our words |
| [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/) and [mypy](https://mypy.readthedocs.io/en/stable/) documentation | `uv init`; Ruff's defaults and target version; strict mode, gradual typing | MIT, and MIT or Apache-2.0 for uv: short quotes |
| [PyPI metadata](https://pypi.org/) for Pyrefly and ty | Release status | MIT (both projects): the classifiers, quoted |
