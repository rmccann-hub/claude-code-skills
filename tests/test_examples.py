"""Every code example in a skill runs under its language's own tool (examples.py)."""

import subprocess
from pathlib import Path

from skillcheck import examples
from skillcheck.cli import main

GOOD = """\
# A module

```yaml
on:
  push:
    branches: [main]
```

```bash
git switch -c <branch>
git push -u origin <branch>
```

```sh
set -eu
printf '%s\\n' "done"
```

```python
if ready:
    publish(release)
```

```json
{"name": "fixture"}
```

```toml
[project]
name = "fixture"
```

```ini
root = true

[*]
charset = utf-8
```

```yaml
answers_source: <recon report path | given in the prompt |
                 asked directly>
```

~~~markdown
```yaml
not: [checked
```
~~~

  ```text
  free text: [is not checked
  ```

```
no language
```
"""

BAD = """\
```yaml
key: [unclosed
```

```python
def broken(:
```

```json
{"a": 1,}
```

```toml
[project
```

```ini
[section]
key
```

```bash
if true; then
```

```sh
for f in $(ls); do echo "$f"; done
cd somewhere
```

<!-- example: unchecked, shows the error the reader will see -->
```yaml
key: [deliberately broken
```

<!-- example: unchecked -->
```yaml
key: value
```
"""


def skill(root: Path, text: str, name: str = "module.md") -> Path:
    path = root / "skills" / "fixture" / "references" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return root


def test_a_skill_whose_examples_all_work_passes(tmp_path):
    result = examples.check(skill(tmp_path, GOOD))
    lines, summary, code = result.report()
    assert (lines, code) == ([], 0)
    assert summary == (
        "skillcheck: 8 example(s) checked, 0 failed, 0 skipped with a reason, "
        "3 in a language with no checker (markdown 1, no language 1, text 1)"
    )


def test_each_broken_example_fails_with_its_tools_words(tmp_path):
    lines, summary, code = examples.check(skill(tmp_path, BAD)).report()
    where = "skills/fixture/references/module.md"
    assert code == 1
    assert lines[0].startswith(f"{where}:1: yaml: ")
    assert lines[1] == f"{where}:5: python: line 1: invalid syntax"
    assert lines[2].startswith(f"{where}:9: json: line 1: ")
    assert lines[3].startswith(f"{where}:13: toml: ")
    assert lines[4].startswith(f"{where}:17: ini: ")
    assert lines[5].startswith(f"{where}:22: bash: ") and "syntax error" in lines[5]
    assert lines[6] == f"{where}:26: sh: ShellCheck: SC2045, SC2164"
    assert lines[7] == f"{where}:37: skipped with no reason; give one"
    assert lines[8] == f"{where}:32: skipped: shows the error the reader will see"
    assert "9 example(s)" not in summary and "7 example(s) checked, 8 failed" in summary


def test_powershell_is_parsed_and_never_run(tmp_path, monkeypatch):
    seen = []

    def run(command, **options):
        seen.append((command, options["input"]))
        message = "Missing closing '}'" if "{" in options["input"] else ""
        return subprocess.CompletedProcess(command, 0, stdout=message, stderr="")

    monkeypatch.setattr(examples.shutil, "which", lambda tool: f"/usr/bin/{tool}")
    text = "```powershell\nGet-ChildItem\n```\n\n```pwsh\nif ($true) {\n```\n"
    lines, _, code = examples.check(skill(tmp_path, text), run).report()
    assert lines == ["skills/fixture/references/module.md:5: pwsh: Missing closing '}'"]
    assert code == 1
    assert seen[0][0][:4] == ["pwsh", "-NoProfile", "-NonInteractive", "-Command"]
    assert seen[0][1] == "Get-ChildItem\n"


def test_a_missing_tool_fails_rather_than_passing_unchecked(tmp_path, monkeypatch):
    monkeypatch.setattr(examples.shutil, "which", lambda tool: None)
    text = "```ps1\nGet-Date\n```\n"
    lines, _, code = examples.check(skill(tmp_path, text)).report()
    assert lines == [
        "skills/fixture/references/module.md:1: ps1: needs pwsh, which isn't installed"
    ]
    assert code == 1


def test_shellcheck_with_no_codes_reports_its_output(tmp_path, monkeypatch):
    def run(command, **_):
        failed = command[0] == "shellcheck"
        return subprocess.CompletedProcess(command, int(failed), stdout="odd", stderr="")

    monkeypatch.setattr(examples.shutil, "which", lambda tool: tool)
    lines, _, _ = examples.check(skill(tmp_path, "```shell\ntrue\n```\n"), run).report()
    assert lines == ["skills/fixture/references/module.md:1: shell: ShellCheck: odd"]


def test_the_command_reports_and_exits_by_what_it_found(tmp_path, capsys):
    assert main([str(skill(tmp_path, GOOD)), "--examples"]) == 0
    assert capsys.readouterr().out.startswith("skillcheck: 8 example(s) checked")
    assert main([str(skill(tmp_path, BAD, "other.md")), "--examples"]) == 1
    assert "other.md:1: yaml:" in capsys.readouterr().out


def test_a_block_left_open_at_the_end_is_still_checked(tmp_path):
    lines, summary, _ = examples.check(skill(tmp_path, '```json\n{"open": [\n')).report()
    assert lines[0].startswith("skills/fixture/references/module.md:1: json: ")
    assert summary.startswith("skillcheck: 1 example(s) checked, 1 failed")


C_GOOD = """\
```c
#include <stddef.h>
size_t twice(size_t n) { return n * 2; }
```

```c std=c23
#include <stdckdint.h>
#include <stddef.h>
bool doubled(size_t n, size_t *out) { return !ckd_mul(out, n, 2); }
```
"""

C_BAD = """\
```c
int unused(void) { int x; return 0; }
```

```c std=c23
#include <stdckdint.h>
int f(void) { return undeclared; }
```

```c std=k&r
int f();
```
"""


def test_c_is_compiled_at_the_standard_its_fence_names(tmp_path):
    lines, summary, code = examples.check(skill(tmp_path, C_GOOD)).report()
    assert (lines, code) == ([], 0)
    assert summary.startswith("skillcheck: 2 example(s) checked, 0 failed")


def test_a_c_warning_fails_and_names_its_line(tmp_path):
    lines, _, code = examples.check(skill(tmp_path, C_BAD)).report()
    where = "skills/fixture/references/module.md"
    assert code == 1
    assert lines[0].startswith(f"{where}:1: c: line 1: unused variable 'x'")
    assert lines[1].startswith(f"{where}:5: c: line 2: use of undeclared identifier")
    assert lines[2] == (
        f"{where}:10: c: std=k&r isn't a C standard this check knows; "
        "use c99, c11, c17 or c23, or its gnu form"
    )


def test_c_is_never_linked_or_run_and_an_odd_failure_is_reported_whole(tmp_path, monkeypatch):
    seen = []

    def run(command, **options):
        seen.append(command)
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="clang: crashed\n")

    monkeypatch.setattr(examples.shutil, "which", lambda tool: f"/usr/bin/{tool}")
    lines, _, _ = examples.check(skill(tmp_path, "```c std=gnu23\nint x;\n```\n"), run).report()
    assert lines == ["skills/fixture/references/module.md:1: c: clang: crashed"]
    assert seen == [
        ["clang", "-x", "c", "-std=gnu23", "-fsyntax-only", "-Wall", "-Wextra", "-Werror", "-"]
    ]
