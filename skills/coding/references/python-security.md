# Python security

Read this for Python code that takes input from outside: running a command with `subprocess`,
`eval` and `exec`, `pickle` and `yaml.load`, SQL, archives, temporary files, paths built from
input, and tokens and secrets.

It covers the Python calls that turn input into code, commands, queries or file writes.
`python-coding` covers the rest of Python: the project, uv, Ruff and its rule sets, types,
idioms, encodings and time zones. Injection beyond these calls, authentication and cryptography
are `secure-coding`'s, and escaping for a web page is `web-security`'s. Where a project keeps its
secrets, and how CI reads them, is the project-bootstrap-and-audit standard's. Which
dependencies to trust is `supply-chain-security`.

## Rules

1. **Pass `subprocess` a list, never `shell=True` on input.**
2. **Never hand untrusted input to `eval`, `exec`, `pickle` or `yaml.load`.** Parse data with
   `json` or `yaml.safe_load`.
3. **SQL takes placeholders,** never a query built from strings.
4. **Make temporary files with `tempfile`'s safe functions.**
5. **Confine every path built from input to its base directory,** archives included.
6. **Make tokens and passwords with `secrets`,** not `random`.

### Commands, code and data

- **`subprocess` with a list, never `shell=True` on input.** With a shell, quoting is the
  caller's job (fact `py-subprocess-shell`). Put `--` before input that could start with `-`,
  where the program accepts it, and set a timeout. On Windows a `.bat` or `.cmd` file runs in
  a shell whatever you pass (fact `py-subprocess-shell`).
- **No `eval` or `exec` on input** (fact `py-eval`). `ast.literal_eval` runs no code, but its
  docs don't recommend it for untrusted data either (fact `py-literal-eval`). Use `json.loads`.
- **No `pickle` on data from outside** (fact `py-pickle`), and `yaml.safe_load`, never
  `yaml.load` (fact `py-yaml-load`). Check the shape of what it returns, as `read_config` does
  below.
- **SQL takes placeholders,** such as `cursor.execute("SELECT * FROM t WHERE id = ?", (key,))`,
  never a query built with an f-string, `%` or `+` (fact `py-sql-params`). Table and column
  names can't be parameters, so pick them from a fixed set.
- **Archives:** extract with `filter="data"`, which 3.14 made `tarfile`'s default and older
  versions need written out (fact `py-tar-filter`). `zipfile` warns that members can land
  outside the target (fact `py-zip-extract`).
- **Tokens, passwords and reset links** come from `secrets`, such as `secrets.token_urlsafe()`,
  never `random`, which is meant for modeling and simulation (fact `py-secrets`).

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

- **`subprocess.run(f"convert {name}", shell=True)`.** The input becomes shell syntax. Pass a
  list.
- **`yaml.load` or `pickle.loads` on an upload, a request or a cache others can write.** Both
  can run code. Use `yaml.safe_load`, and JSON instead of pickle.
- **`f"SELECT … WHERE name = '{name}'"` passed to `execute`,** which lets the input rewrite the
  query. Pass the value as a parameter.
- **`eval(text)` to parse a number or a list.** Use `int()`, `float()` or `json.loads`.
- **`tempfile.mktemp()`, a fixed `/tmp/app.log`, or an unchecked `base / name`.**
- **`random.choice` or `random.randint` for a token or a one-time code,** which an attacker
  can predict. Use `secrets`.

## Audit

Severity uses the standard's status words. The `S` codes are Ruff's, run as
`uv run ruff check --extend-select S .`; `python-coding` turns them on for good.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Shell commands from input | `S602`, `S604`, `S605` (fact `py-ruff-security-off`) | `BLOCKER` where input reaches it, else `GAP` | A list of arguments, no shell (fact `py-subprocess-shell`) |
| SQL from strings | `execute(` with an f-string, `%`, `+` or `.format` in the query: Ruff's `S608` | `BLOCKER` where input reaches it, else `GAP` | Placeholders (fact `py-sql-params`) |
| Code run from data | `eval`, `exec`, `pickle`, `yaml.load`: `S301`, `S307`, `S506` | `BLOCKER` where input reaches it, else `GAP` | `json.loads`, `yaml.safe_load` (facts `py-pickle`, `py-yaml-load`) |
| Unsafe temporary files | `mktemp`, or a fixed path under `/tmp`: `S306`, `S108` | `GAP` | `tempfile.TemporaryDirectory` or `mkstemp` (fact `py-mktemp`) |
| Paths from input | A request's or an archive's name joined to a base with no check; `extractall` without `filter=` | `BLOCKER` where reachable, else `GAP` | Resolve, then `is_relative_to`; `filter="data"` (facts `py-is-relative-to`, `py-tar-filter`) |
| Weak tokens | `random` making a token, password or code: `S311` | `BLOCKER` where it guards access, else `GAP` | `secrets` (fact `py-secrets`) |

## Why

**1 to 5. Input that becomes commands, code, queries or files.** List arguments for
`subprocess`, JSON or `safe_load` for data, placeholders for SQL, `tempfile`'s safe functions,
and a containment check on every path from input. Each unsafe call runs or writes what the input
says, and Python's own docs warn on every one (facts `py-subprocess-shell`, `py-eval`,
`py-pickle`, `py-yaml-load`, `py-sql-params`, `py-mktemp`). Cost: pipes and globbing are written
in Python instead, and the containment check also rejects a symlink in the base that points out,
since `resolve()` follows it. Otherwise: `pickle` between processes inside one trust boundary,
such as a cache only the program writes, signed with `hmac` where it could be tampered with.

**6. `secrets` for tokens.** `random` is built for modeling and simulation, so its output can be
predicted; `secrets` draws on the operating system's secure source (fact `py-secrets`). It costs
nothing: the calls are as short. Otherwise: `random` with a seed stays right for simulations and
tests that must repeat.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked
2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `py-ruff-security-off` | Ruff's rules page marks each default rule; `S602` (`shell=True`) and `DTZ005` (`datetime.now()` with no zone) aren't marked. Checked by reading the page | [Ruff rules](https://docs.astral.sh/ruff/rules/) | "Enabled by default" | 2026-10-26 | 2027-04-26 |
| `py-sql-params` | Python's `sqlite3` docs warn against building queries with string operations | [sqlite3](https://docs.python.org/3/library/sqlite3.html) | "as they are vulnerable to SQL injection attacks" | 2026-10-26 | 2027-10-26 |
| `py-secrets` | `secrets`, not `random`, for security tokens; `random` is for modeling and simulation | [secrets](https://docs.python.org/3/library/secrets.html) | "secrets should be used in preference to the default pseudo-random number generator in the random module, which is designed for modelling and simulation, not security or cryptography." and "the most secure source of randomness that your operating system provides" | 2026-10-26 | 2027-10-26 |
| `py-subprocess-shell` | With `shell=True`, quoting input is the caller's job, and on Windows a batch file runs in a shell regardless | [subprocess](https://docs.python.org/3/library/subprocess.html) | "If the shell is invoked explicitly, via shell=True, it is the application's responsibility to ensure that all whitespace and metacharacters are quoted appropriately to avoid shell injection vulnerabilities." and "may be launched by the operating system in a system shell regardless of the arguments passed to this library." | 2026-10-26 | 2027-10-26 |
| `py-eval` | `eval` runs arbitrary code | [Built-in functions](https://docs.python.org/3/library/functions.html) | "This function executes arbitrary code. Calling it with untrusted user-supplied input will lead to security vulnerabilities." | 2026-10-26 | 2027-10-26 |
| `py-literal-eval` | `ast.literal_eval` isn't recommended for untrusted data | [ast](https://docs.python.org/3/library/ast.html) | "Calling it on untrusted data is thus not recommended." | 2026-10-26 | 2027-10-26 |
| `py-pickle` | Unpickling can run code | [pickle](https://docs.python.org/3/library/pickle.html) | "The pickle module is not secure. Only unpickle data you trust." | 2026-10-26 | 2027-10-26 |
| `py-yaml-load` | PyYAML's `yaml.load` isn't safe on untrusted data | [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation) | "It is not safe to call yaml.load with any data received from an untrusted source!" | 2026-10-26 | 2027-10-26 |
| `py-mktemp` | `tempfile.mktemp` is deprecated and unsafe | [tempfile](https://docs.python.org/3/library/tempfile.html) | "Use of this function may introduce a security hole in your program." | 2026-10-26 | 2027-10-26 |
| `py-is-relative-to` | `PurePath.is_relative_to` compares strings, and doesn't resolve `..` | [pathlib](https://docs.python.org/3/library/pathlib.html) | "This method is string-based; it neither accesses the filesystem nor treats" ... "segments specially." | 2026-10-26 | 2027-10-26 |
| `py-tar-filter` | `tarfile` extraction defaults to the `data` filter from 3.14; earlier versions need it set | [tarfile](https://docs.python.org/3/library/tarfile.html) | "Changed in version 3.14: The filter parameter now defaults to 'data'." and "to support Python versions with a less secure default (3.13 and lower)" | 2026-10-26 | 2027-10-26 |
| `py-zip-extract` | `zipfile` extraction from an untrusted archive can write outside the target | [zipfile](https://docs.python.org/3/library/zipfile.html) | "It is possible that files are created outside of path" | 2026-10-26 | 2027-10-26 |

## Sources

Every source, with its license and how this module uses it. The rules and examples are this
module's own words and code.

| Source | Used for | License |
|---|---|---|
| [Python documentation](https://docs.python.org/3/library/) | Security warnings for `subprocess`, `eval`, `pickle`, `sqlite3`, `tempfile`, `pathlib`, `tarfile`, `zipfile` and `secrets` | PSF License Version 2 for text: short quotes, with attribution |
| [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation) | `yaml.load` and `safe_load` | MIT (the project): one short quote |
| [Ruff documentation](https://docs.astral.sh/ruff/rules/) | The `S` rules and which are on by default | MIT: facts with short quotes |
