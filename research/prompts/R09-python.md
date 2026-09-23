# RESEARCH RUN R09: Python and Python for data

For the repository rmccann-hub/claude-code-skills · Prompt version 2 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: python, and the Python side of data-and-sql and excel.

## Rules

1. **Primary sources first:** official documentation, specifications and standards bodies, and
   each project's own release notes, changelogs and security advisories. Use secondary sources
   (respected books, well-known engineering blogs, surveys) only where no primary source covers
   the point, and label them "secondary".
2. **Cite every fact:** the URL, the exact sentence you relied on in quotation marks, and a date
   (the source's own date, otherwise the date you read it).
3. **Never guess.** Write "not found" when you can't source something. Write "contested" when good
   sources disagree, and give each side with its source.
4. **Versions:** for every product, give
   - the current stable version and its release date;
   - its end-of-support date;
   - any release due within 6 months, with the expected date and its source.

   Flag anything that reaches end of support within 12 months.
5. **"What we believe" is my current understanding and may be wrong or out of date.** Confirm or
   correct every item, each with a source. The corrections are the most valuable part of this run.
6. **Licences:** for each source, name its licence and say what an Apache-2.0 repository may do
   with it: quote briefly, paraphrase, or adapt its code examples, and with what attribution.
7. **Depth over breadth.** Finish the Priority questions fully. If you run out of room, list the
   rest under "Not covered".
8. **Beliefs marked "(the standard, date)"** come from this repository's own standard,
   PROJECT-BOOTSTRAP-AND-AUDIT v0.35.0, in its section of dated facts. Checking them also
   checks that standard, so say plainly when one is wrong.

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R09 · FORM: research-result v1
Save as: R09-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.
```

Then these sections, in this order:

1. **Summary:** at most 15 bullets a professional must know today.
2. **Corrections:** every "What we believe" item that was wrong or out of date, with the right
   fact and its source.
3. **Facts table:** `| # | Fact | Value | Source URL | Exact quote | Date |`
4. **Findings:** one section per question below, numbered to match.
5. **Tools:** `| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |`
6. **Changing in the next 12 months:** deprecations, end-of-support dates, announced breaking
   changes.
7. **Common mistakes,** including those AI coding assistants make in this area, with sources.
8. **Sources and licences:** `| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |`
9. **Not found, contested, not covered.**

## What we believe (confirm or correct each)

- Python 3.14 was released in October 2025; Python 3.15 is due in October 2026; Python 3.10 reaches end of life in October 2026, and 3.9 reached it in October 2025.
- (the standard, 2026-09) Python 3.14.x has been stable since October 2025, and 3.13.x is still maintained. uv carries the momentum, Poetry is fully supported, and pip-tools suits minimalists. Dependency groups are standardised.
- Python 3.14 added deferred evaluation of annotations (PEP 649 and 749), template strings (PEP 750), official free-threaded support (PEP 779), `concurrent.interpreters` (PEP 734), `compression.zstd` (PEP 784), and a default `data` filter for tarfile extraction.
- uv (Astral) is the fastest-growing Python package and project manager, and ruff is the dominant linter and formatter; Astral's ty and Meta's pyrefly type checkers are in beta or early release.
- PEP 751 (pylock.toml) was accepted in 2025; PEP 735 dependency groups are supported by uv and pip; PEP 639 standardized SPDX licence expressions in metadata.
- pandas 3.0 made Copy-on-Write the default and uses a dedicated string dtype by default; NumPy 2.x is current; Polars 1.x is widely used.

## Questions

### Priority

1. Python release status today: the latest patch release of each supported branch, end-of-life dates, the 3.15 schedule and its headline features (confirm the PEP numbers), and which versions a new project should target and test.
2. Modern idioms a professional uses today that an older codebase won't have:
   - typing: type parameter syntax (PEP 695), `type` aliases, `Self`, `TypeIs`, `override`
   - data classes: dataclasses versus attrs versus Pydantic v2
   - `match`, exception groups, `pathlib`, f-strings (PEP 701) and t-strings
   - `asyncio.TaskGroup` and `timeout`, `importlib.resources`, `zoneinfo`, `tomllib`

   What is deprecated or removed in 3.13-3.15 (for example `datetime.utcnow`, and the modules removed under PEP 594)?
3. Tooling:
   - uv: current version, `uv sync --locked` in CI, `uv tool`, `uv python`, `uv build`, the uv_build backend
   - ruff: current version, rule sets for new projects, the formatter, Markdown code-block formatting
   - type checkers (mypy, pyright or basedpyright, ty, pyrefly): status, speed, strictness
   - pytest (current version and key plugins), coverage.py, pre-commit or prek, pip-audit
4. Packaging: pyproject.toml fields (PEP 621), build backends (hatchling, setuptools, uv_build, flit), dependency groups (PEP 735), lock files (uv.lock, pylock.toml), licence expressions (PEP 639), trusted publishing to PyPI, and attestations (PEP 740).
5. Security in Python:
   - `subprocess` with shell=False, and `shlex`
   - `pickle` and `marshal`, `yaml.safe_load`, `tarfile` and `zipfile` extraction, `xml` (defusedxml)
   - `secrets` versus `random`, `hashlib` and `hmac`, SQL parameters
   - ruff's S rules versus bandit
   - typosquatting and slopsquatting on PyPI

### Standard

6. Free-threaded Python: its status in 3.14 and 3.15, library compatibility tracking, and when to use it.
7. Data:
   - pandas 3.x changes: Copy-on-Write, the string dtype, removed APIs, `read_excel` engines, `.xls` support
   - NumPy 2.x migration notes; Polars, DuckDB and PyArrow
   - which to recommend for new work, and when
8. Async: current asyncio best practice, structured concurrency, the status of anyio and trio, common mistakes.
9. Command-line tools and apps: argparse versus click versus typer; logging configuration; configuration with pydantic-settings; packaging a CLI (uv tool, pipx).
10. Legacy Python: reading and migrating Python 2 and early 3.x code (2to3 is removed; pyupgrade and ruff's UP rules; six and future), and upgrading 3.8 and 3.9 codebases.
11. Mistakes AI assistants make in Python, from studies or vendor guidance.
