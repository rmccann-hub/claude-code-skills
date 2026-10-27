# Python security

Read this for Python code that takes input from outside: running a command with `subprocess`,
`eval` and `exec`, `pickle` and `yaml.load`, SQL, archives, temporary files, paths built from
input, `assert` as a check, and tokens and secrets.

It covers the Python calls that turn input into code, commands, queries or file writes.
`python-coding` covers the rest of Python: the project, uv, Ruff and its rule sets, types,
idioms, encodings and time zones. Injection beyond these calls, authentication and cryptography
are `secure-coding`'s, and escaping for a web page is `web-security`'s. Where a project keeps its
secrets, and how CI reads them, is the project-bootstrap-and-audit standard's. Which
dependencies to trust is `supply-chain-security`.

## Rules

1. **Pass `subprocess` a list, never `shell=True` on input,** nor a list that starts a shell,
   such as `["sh", "-c", f"…"]`.
2. **Never hand untrusted input to `eval`, `exec`, `pickle` or `yaml.load`.** Parse data with
   `json` or `yaml.safe_load`.
3. **SQL takes placeholders,** never a query built from strings.
4. **Make temporary files with `tempfile`'s safe functions.**
5. **Confine every path built from input to its base directory,** archives included.
6. **Make tokens and passwords with `secrets`,** not `random`.
7. **Check input and permissions with an exception, never `assert`.**

### Commands, code and data

- **`subprocess` with a list, never `shell=True` on input.** With a shell, quoting is the caller's
  job. `["sh", "-c", …]` and `["bash", "-c", …]` are the same shell: keep input out of the command
  string. Put `--` before input that could start with `-`, where the program takes it, and set a
  timeout. On Windows a `.bat` or `.cmd` file runs in a shell whatever you pass (fact
  `py-subprocess-shell`).
- **No `eval` or `exec` on input** (fact `py-eval`). `ast.literal_eval` runs no code, but its
  docs don't recommend it for untrusted data either (fact `py-literal-eval`). Use `json.loads`.
- **No `pickle` on data from outside** (fact `py-pickle`), and `yaml.safe_load`, never
  `yaml.load` (fact `py-yaml-load`). It and `json.loads` return `Any`: check the shape, as
  `read_config` does below.
- **SQL takes placeholders,** such as `cursor.execute("SELECT * FROM t WHERE id = ?", (key,))`,
  never a query built with an f-string, `%` or `+` (fact `py-sql-params`). Table and column
  names can't be parameters, so pick them from a fixed set.
- **Archives:** extract with `filter="data"`, which 3.14 made `tarfile`'s default and older
  versions need written out (fact `py-tar-filter`). `zipfile` warns that members can land
  outside the target (fact `py-zip-extract`).
- **Tokens, passwords and reset links** come from `secrets`, such as `secrets.token_urlsafe()`,
  never `random`, which is meant for modeling and simulation (fact `py-secrets`).
- **`assert` isn't validation.** `python -O` removes it (fact `py-assert-o`). Raise an
  exception for anything a caller can get wrong.

```python
import subprocess
import tarfile
from pathlib import Path

import yaml


def search(pattern: str, root: Path) -> str:
    result = subprocess.run(
        ["grep", "-r", "-n", "--", pattern, str(root)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )
    if result.returncode > 1:  # grep exits 1 for no match, 2 for an error
        raise RuntimeError(result.stderr.strip())
    return result.stdout


def read_config(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise TypeError(f"{path}: expected a mapping at the top level")
    return data


def unpack(archive: Path, dest: Path) -> None:
    with tarfile.open(archive) as tar:
        tar.extractall(dest, filter="data")
```

### Temporary files and paths

- **`tempfile.TemporaryDirectory`, `NamedTemporaryFile` or `mkstemp`,** never `mktemp`, whose
  name another process can take first (fact `py-mktemp`), and never a fixed name under `/tmp`.
- **Confine a path built from input:** resolve it, then check it's inside the base.
  `is_relative_to` compares strings and doesn't treat `..` specially (fact
  `py-is-relative-to`), so it's safe only after `resolve()`.

```python
from pathlib import Path

UPLOADS = Path("/srv/uploads").resolve()


def upload_path(name: str) -> Path:
    target = (UPLOADS / name).resolve()
    if not target.is_relative_to(UPLOADS):
        raise ValueError(f"{name!r} is outside {UPLOADS}")
    return target
```

## Mistakes

- **`subprocess.run(f"convert {name}", shell=True)`, or `["sh", "-c", f"convert {name}"]`.**
  The input becomes shell syntax. Pass a list that runs `convert` itself.
- **`yaml.load` or `pickle.loads` on an upload, a request or a cache others can write.** Both
  can run code. Use `yaml.safe_load`, and JSON instead of pickle.
- **`f"SELECT … WHERE name = '{name}'"` passed to `execute`,** which lets the input rewrite the
  query. Pass the value as a parameter.
- **`eval(text)` to parse a number or a list.** Use `int()`, `float()` or `json.loads`.
- **`tempfile.mktemp()`, a fixed `/tmp/app.log`, or an unchecked `base / name`.**
- **`random.choice` or `random.randint` for a token or a one-time code,** which an attacker
  can predict. Use `secrets`.
- **`assert user.is_admin`,** which `python -O` removes.

## Audit

Severity uses the standard's status words. The `S` codes are Ruff's, run as
`uv run ruff check --extend-select S .`; `python-coding` turns them on for good.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Shell commands from input | `S602`, `S604`, `S605` (fact `py-ruff-security-off`); a list running `sh -c` or `bash -c` with input in the command, which only `S603` flags (fact `py-ruff-s603`) | `BLOCKER` where input reaches it, else `GAP` | A list of arguments, no shell (fact `py-subprocess-shell`) |
| SQL from strings | `execute(` with an f-string, `%`, `+` or `.format` in the query: Ruff's `S608` | `BLOCKER` where input reaches it, else `GAP` | Placeholders (fact `py-sql-params`) |
| Code run from data | `eval`, `exec`, `pickle`, `yaml.load`: `S301`, `S307`, `S506` | `BLOCKER` where input reaches it, else `GAP` | `json.loads`, `yaml.safe_load` (facts `py-pickle`, `py-yaml-load`) |
| Unsafe temporary files | `mktemp`, or a fixed path under `/tmp`: `S306`, `S108` | `GAP` | `tempfile.TemporaryDirectory` or `mkstemp` (fact `py-mktemp`) |
| Paths from input | A request's or an archive's name joined to a base with no check; `extractall` without `filter=` | `BLOCKER` where reachable, else `GAP` | Resolve, then `is_relative_to`; `filter="data"` (facts `py-is-relative-to`, `py-tar-filter`) |
| Weak tokens | `random` making a token, password or code: `S311` | `BLOCKER` where it guards access, else `GAP` | `secrets` (fact `py-secrets`) |
| `assert` for checks | `assert` outside tests guarding input or permissions: `S101` | `GAP` | Raise an exception (fact `py-assert-o`) |

`S603` and `S607` flag safe calls too (fact `py-ruff-s603`). Review each; for a directory of
the project's own tools whose calls all pass lists, ignore both there, saying what was checked:

```toml
[tool.ruff.lint.per-file-ignores]
# Reviewed 2026-10-27: every call in tools/ passes a list, no shell; S602 stays on.
"tools/**" = ["S603", "S607"]
```

## Why

**1 to 5. Input that becomes commands, code, queries or files.** List arguments for `subprocess`,
JSON or `safe_load` for data, placeholders for SQL, `tempfile`'s safe functions, and a containment
check on every path from input. A list that starts a shell, such as `["sh", "-c", …]`, parses its
command string as `shell=True` does. Each unsafe call runs or writes what the input says, and
Python's own docs warn on every one (facts `py-subprocess-shell`, `py-eval`, `py-pickle`,
`py-yaml-load`, `py-sql-params`, `py-mktemp`). Cost: pipes and globbing are written in Python
instead, and the containment check also rejects a symlink in the base that points out, since
`resolve()` follows it. Otherwise: `pickle` between processes inside one trust boundary, such as a
cache only the program writes, signed with `hmac` where it could be tampered with.

**`S603` and `S607` by directory.** Ruff calls `S603` prone to false positives (fact
`py-ruff-s603`), and hundreds of `noqa` lines bury the few that matter. Cost: the ignore hides new
calls there, a `sh -c` included, so review them, and `git grep -n -e '"-c"' -- tools` finds a shell.
Otherwise: where calls take outside input, as in a service, suppress each line.

**6. `secrets` for tokens.** `random` is built for modeling and simulation, so its output can be
predicted; `secrets` draws on the operating system's secure source (fact `py-secrets`). It costs
nothing: the calls are as short. Otherwise: `random` with a seed stays right for simulations and
tests that must repeat.

**7. No `assert` as a check.** `python -O` drops every `assert` (fact `py-assert-o`), so the
guard vanishes. Cost: an `if` and a `raise`. Otherwise: `assert` suits tests and invariants.

## Facts

Each named by its ID, here or in `python-coding`.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `py-ruff-security-off` | Ruff's rules page marks each default rule; `S602` (`shell=True`) and `DTZ005` (`datetime.now()` with no zone) aren't marked. Checked by reading the page | [Ruff rules](https://docs.astral.sh/ruff/rules/) | "Enabled by default" | 2026-10-26 | 2027-04-26 |
| `py-ruff-target` | Ruff prefers `requires-python` to its own setting, and uses the closest config | [settings](https://docs.astral.sh/ruff/settings/), [configuration](https://docs.astral.sh/ruff/configuration/) | "we recommend project.requires-python instead" and "Ruff supports hierarchical configuration" | 2026-10-27 | 2027-04-27 |
| `py-ruff-defaults` | Ruff's defaults span several categories, `B006` among them | [Ruff](https://docs.astral.sh/ruff/rules/) | "omitting any stylistic rules that overlap with the use of a formatter" | 2026-10-26 | 2027-04-26 |
| `py-ruff-plw1514` | `PLW1514` is in preview, for `open` and related calls | [PLW1514](https://docs.astral.sh/ruff/rules/unspecified-encoding/) | "This rule is unstable and in preview." and "open and related calls" | 2026-10-27 | 2027-04-27 |
| `py-ruff-unused-noqa` | RUF100 flags a `noqa` that applies to nothing | [RUF100](https://docs.astral.sh/ruff/rules/unused-noqa/) | "noqa directives that are no longer applicable" | 2026-10-27 | 2027-04-27 |
| `py-ruff-s603` | `S603` flags calls without a shell, with false positives | [S603](https://docs.astral.sh/ruff/rules/subprocess-without-shell-equals-true/) | "initiate a subprocess without a shell" and "Prone to false positives" | 2026-10-27 | 2027-04-27 |
| `py-subprocess-text` | `text=True` decodes with the default unless `encoding` is given | [subprocess](https://docs.python.org/3/library/subprocess.html) | "using the specified encoding and errors or the io.TextIOWrapper default" | 2026-10-27 | 2027-10-27 |
| `py-assert-o` | `python -O` drops `assert` | [statements](https://docs.python.org/3/reference/simple_stmts.html) | "emits no code for an assert statement" | 2026-10-26 | 2027-10-26 |
| `py-sql-params` | Python's `sqlite3` docs warn against building queries with string operations | [sqlite3](https://docs.python.org/3/library/sqlite3.html) | "as they are vulnerable to SQL injection attacks" | 2026-10-26 | 2027-10-26 |
| `py-secrets` | `secrets`, not `random`, for security tokens; `random` is for modeling and simulation | [secrets](https://docs.python.org/3/library/secrets.html) | "designed for modelling and simulation, not security or cryptography" and "the most secure source of randomness that your operating system provides" | 2026-10-26 | 2027-10-26 |
| `py-subprocess-shell` | With `shell=True`, quoting input is the caller's job, and on Windows a batch file runs in a shell regardless | [subprocess](https://docs.python.org/3/library/subprocess.html) | "it is the application's responsibility to ensure that all whitespace and metacharacters are quoted appropriately" and "may be launched by the operating system in a system shell regardless of the arguments passed to this library." | 2026-10-26 | 2027-10-26 |
| `py-eval` | `eval` runs arbitrary code | [Built-in functions](https://docs.python.org/3/library/functions.html) | "Calling it with untrusted user-supplied input will lead to security vulnerabilities." | 2026-10-26 | 2027-10-26 |
| `py-literal-eval` | `ast.literal_eval` isn't recommended for untrusted data | [ast](https://docs.python.org/3/library/ast.html) | "Calling it on untrusted data is thus not recommended." | 2026-10-26 | 2027-10-26 |
| `py-pickle` | Unpickling can run code | [pickle](https://docs.python.org/3/library/pickle.html) | "The pickle module is not secure. Only unpickle data you trust." | 2026-10-26 | 2027-10-26 |
| `py-yaml-load` | PyYAML's `yaml.load` isn't safe on untrusted data | [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation) | "It is not safe to call yaml.load with any data received from an untrusted source!" | 2026-10-26 | 2027-10-26 |
| `py-mktemp` | `tempfile.mktemp` is deprecated and unsafe | [tempfile](https://docs.python.org/3/library/tempfile.html) | "Use of this function may introduce a security hole in your program." | 2026-10-26 | 2027-10-26 |
| `py-is-relative-to` | `PurePath.is_relative_to` compares strings, and doesn't resolve `..` | [pathlib](https://docs.python.org/3/library/pathlib.html) | "This method is string-based; it neither accesses the filesystem nor treats" ... "segments specially." | 2026-10-26 | 2027-10-26 |
| `py-tar-filter` | `tarfile` extraction defaults to the `data` filter from 3.14; earlier versions need it set | [tarfile](https://docs.python.org/3/library/tarfile.html) | "Changed in version 3.14: The filter parameter now defaults to 'data'." and "to support Python versions with a less secure default (3.13 and lower)" | 2026-10-26 | 2027-10-26 |
| `py-zip-extract` | `zipfile` extraction from an untrusted archive can write outside the target | [zipfile](https://docs.python.org/3/library/zipfile.html) | "It is possible that files are created outside of path" | 2026-10-26 | 2027-10-26 |

## Sources

The rules and examples are this module's own words and code.

| Source | Used for | License |
|---|---|---|
| [Python documentation](https://docs.python.org/3/library/) | Security warnings for `subprocess`, `eval`, `pickle`, `sqlite3`, `tempfile`, `pathlib`, `tarfile`, `zipfile` and `secrets` | PSF License Version 2 for text: short quotes, with attribution |
| [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation) | `yaml.load` and `safe_load` | MIT (the project): one short quote |
| [Ruff documentation](https://docs.astral.sh/ruff/rules/) | The `S` rules and which are on by default | MIT: facts with short quotes |
