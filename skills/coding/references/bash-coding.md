# Bash coding

Read this for writing, reviewing or fixing a Bash or POSIX `sh` script: the shebang, strict mode
and its traps, quoting, tests and globs, arrays, lines and file names, temporary files,
portability to macOS and dash, and ShellCheck, shfmt and bats.

Deletes, `eval`, fetched code, arithmetic on input, secrets and input checks: bash-security.
Containers and Linux: the planned operations skill. CI files: git-workflows. Test design: the
planned testing skill. Layout and when to use Python: project-bootstrap-and-audit.

## Rules

1. **Name the shell in the shebang:** `#!/usr/bin/env bash`, or `#!/bin/sh` only for POSIX
   linted as `sh`.
2. **Start Bash with `set -euo pipefail`, and know its gaps:** conditions, functions called
   from them, `local`, and `((n++))` at zero. Leave out `-e` only for a hook that must never fail
   its caller, or a probe collecting every result, and say so by `set`.
3. **Quote every expansion:** `"$var"`, `"$(cmd)"`, `"${list[@]}"`, or say why not in a
   ShellCheck directive.
4. **Hold a list in an array, never a string:** a Bash array, or `"$@"` in `sh`.
5. **Read lines with `while IFS= read -r`, and names with `-print0`, `find -exec … {} +` or
   git's `-z`.** Never parse `ls`.
6. **`mktemp` for temporary files, removed in an `EXIT` trap.**
7. **Run ShellCheck and shfmt, locally and in CI;** bats runs the tests.
8. **A script that deletes or overwrites follows bash-security's guards:** `${var:?}`, `--`,
   and a dry run first.

### The shell and the shebang

- **Debian's `/bin/sh` is dash** (fact `sh-debian-dash`): a `#!/bin/sh` script using `[[`,
  arrays or `function` fails there. `sh tool` ignores the shebang.
- **`#!/usr/bin/env bash`** finds a newer Bash than macOS's `/bin/bash` 3.2 (fact
  `sh-macos-bash`). The login shell, zsh (fact `sh-macos-zsh`), doesn't matter.
- **Know which Bash a feature needs:** associative arrays and `mapfile`, 4.0 (fact
  `sh-bash-versions`); an empty array under `set -u`, 4.4 (fact `sh-bash44-empty-array`);
  `${ cmd; }`, 5.3 (fact `sh-bash53-nofork`), the current release (fact `sh-bash-current`).
  For 3.2, avoid them, or check:

```bash
if ((BASH_VERSINFO[0] < 4)); then
  printf '%s needs Bash 4 or later; this is %s\n' "${0##*/}" "$BASH_VERSION" >&2
  exit 1
fi
```

### Strict mode and its traps

`pipefail` fails a pipeline when any stage fails, not only the last (fact
`sh-pipefail-bash`). The gaps:

- **`-e` is off in a condition** (after `if`, `while`, `until` or `!`, left of `&&` or `||`),
  and in a function called there (fact `sh-errexit`): `if deploy; then` hides its failures.
- **`local x=$(cmd)` returns `local`'s status** (fact `sh-local-status`), as do `export` and
  `readonly`. Declare, then assign.
- **`((n++))` at 0 returns 1** (fact `sh-arith-status`): `-e` stops. Use `n=$((n + 1))`.
- **A command substitution runs without `-e`** unless `shopt -s inherit_errexit` (fact
  `sh-bash-versions`): `out=$(step1; step2)` runs `step2` after `step1` fails.
- **`pipefail` fails when a reader stops early:** in `producer | head -n 1` the producer can die
  of `SIGPIPE`, status 141 (fact `sh-signal-status`); add `|| true`. ShellCheck's next release
  flags `grep -q` there (fact `sh-shellcheck`).
- **`PIPESTATUS`** holds each stage's status, read on the next line (fact `sh-pipestatus`).
- **In `sh`,** `pipefail` is POSIX since 2024 (fact `sh-posix-pipefail`), but dash has it only
  from 0.5.13 (fact `sh-dash-pipefail`); Debian 13 ships 0.5.12. Probe:

```sh
set -eu
# shellcheck disable=SC3040
(set -o pipefail 2>/dev/null) && set -o pipefail
```

### Quoting, tests and globs

- **An unquoted expansion is split, then globbed** (fact `sh-expansion`): `a b` becomes two
  arguments, and `*` a listing.
- **`[[ … ]]`** doesn't split or glob. Quote the right side of `==` to compare literally:
  `[[ $a == "$b" ]]`. In `sh`, `[ "$a" = "$b" ]`.
- **Numbers** compare with `(( a > b ))` or `[ "$a" -gt "$b" ]`; in `[ ]`, `>` redirects.
  Input is checked as digits first: bash-security (fact `sh-arith-eval`).
- **`printf '%s\n' "$x"`, not `echo`,** for data: `echo` differs on backslashes and `-n` (fact
  `sh-echo`).
- **An unmatched glob stays as written:** test `[ -e "$f" ]`, or `shopt -s nullglob`. Write
  `./*.txt`, so a file named `-rf` isn't an option.

### Arrays

Build arguments in an array, expanded quoted:

```bash
src=build dest=/srv/www dry_run=1
args=(--archive --delete)
if ((dry_run)); then
  args+=(--dry-run)
fi
rsync "${args[@]}" -- "$src/" "$dest/"
```

In `sh`, use `"$@"`: `set -- "$@" --dry-run`. Before Bash 4.4 with `set -u`, expand a
maybe-empty list as `${args[@]+"${args[@]}"}`.

### Lines and file names

- **`IFS=` keeps edge spaces, and `-r` backslashes** (fact `sh-read-r`); `|| [[ -n $line ]]`
  keeps a last line with no newline.
- **A loop at a pipe's end is a subshell** (fact `sh-pipeline-subshell`) and loses its
  variables. Feed it with `done < <(cmd)`.
- **Names hold spaces, newlines and dashes.** `-print0` and `xargs -0` are POSIX since 2024
  (fact `sh-posix-print0`); `find -exec … {} +` works everywhere.
- **git quotes a name with a byte over 0x80,** as `"Bj\303\266rk.flac"`, in `ls-files`,
  `diff --name-only` and `status` (fact `sh-git-quotepath`): `'\.flac$'` misses it. Use `-z`.

```bash
while IFS= read -r line || [[ -n $line ]]; do
  printf '%s\n' "$line"
done <input.txt

find . -type f -name '*.md' -exec grep -l -e 'TODO' -- {} +

while IFS= read -r -d '' path; do
  printf 'found: %s\n' "$path"
done < <(find . -type f -name '*.log' -print0)

git diff -z --name-only main -- '*.flac' | xargs -0 -r flac --test --
```

### Temporary files and cleanup

`mktemp` makes a random name, GNU's owner-only (fact `sh-mktemp`). Trap `EXIT`, and the
signals, which may skip it (fact `sh-exit-trap`):

```sh
#!/bin/sh
set -eu

tmpdir=$(mktemp -d)
cleanup() { rm -rf -- "$tmpdir"; }
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

sort -- "$1" >"$tmpdir/sorted"
```

### Tools and portability

- **ShellCheck** (fact `sh-shellcheck`) reads the shebang: `shellcheck bin/* lib/*.sh`. Fix,
  or disable on the line, saying why. Not installed? `uvx --from shellcheck-py shellcheck` runs
  it from PyPI (fact `sh-shellcheck-py`). Failing that, read for the gaps above by hand, and
  mark the lint `UNVERIFIABLE-HERE`.
- **shfmt** (fact `sh-shfmt`) reads `.editorconfig`; `shfmt -d bin lib` fails with a diff.
- **bats** (fact `sh-bats-version`) runs `.bats` files: `bats tests`.
- **`sed -i` differs on BSD** (fact `sh-sed-inplace`): write a temporary file, then `mv`.

## Mistakes

- **`#!/bin/sh` on a Bash script:** fails on Debian. Name Bash, or lint as `sh` and port it.
- **`((count++))` under `set -e`:** stops at 0. Use `count=$((count + 1))`.
- **`local out=$(cmd)` or `export out=$(cmd)`:** hides the failure. Split the line.
- **`for f in $(ls)`, `for f in $(find …)`, `ls | while read`:** split names. Use a glob,
  `find -exec`, or `-print0` with `read -d ''`.
- **Options in a string,** such as `opts="--exclude '*.tmp'"; rsync $opts`: the inner quotes
  stay literal. Use an array.
- **A fixed path such as `/tmp/myscript.tmp`:** another user can create it first.
- **`cd "$dir"` unchecked:** the script runs on elsewhere. `cd -- "$dir" || exit`.
- **A comment after a line-continuation backslash:** the next line runs alone. Move it.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| ShellCheck | `shellcheck` on every script | `GAP` per warning; SC2115 as bash-security's unsafe deletes; `UNVERIFIABLE-HERE` where it can't run | Fix, or disable on the line with why |
| Dialect | `shellcheck --shell=sh` on `#!/bin/sh`: `[[`, arrays, `source`, unprobed `pipefail` | `DRIFT` | Name Bash, or port it |
| Strict mode | Bash without `set -euo pipefail` | `GAP`, unless rule 2's hook or probe says so by `set` and checks each command it needs | Add it; fix what breaks |
| git name lists | `ls-files`, `diff --name-only` or `status` read without `-z`, then matched by a pattern | `BLOCKER` where a check passes on names it never matched, else `GAP` | `-z`, read with `-d ''` |
| Masked failures | `local`, `export` or `readonly` with `$(…)`; `((n++))` under `-e`; a side-effecting function as an `if` condition | `GAP` | Split; `n=$((n + 1))`; check in the function |
| Temporary files | Fixed `/tmp` paths; `mktemp` with no `EXIT` trap | `GAP` | `mktemp` and a trap |
| Formatting | `shfmt -d` | `DRIFT` | `shfmt -w`, and a CI step |
| Version reach | Bash 4 features for macOS's `/bin/bash` | `DRIFT` | Remove, or check `BASH_VERSINFO` |

## Why

**The shell.** `#!/bin/sh` promises POSIX, dash holds it to that, and a Bash feature fails at
run time, often on an untested branch. Google allows only Bash, and a rewrite past 100 lines
(fact `sh-google`). Costs: `env` follows `PATH`, so cron or `sudo` may find another Bash; `sh`
has no arrays. Otherwise: a fixed-`PATH` system script names `/bin/bash`; past a hundred lines,
or with structured data, use Python.

**Strict mode.** Without `-e`, the next step runs on bad input; without `pipefail`, a failed
download piped to `tar` succeeds; without `-u`, a typo is empty. Costs: `grep` and the like
need `if` or `|| true`. Checking each status by hand is more code to get wrong. Otherwise: in
rule 2's two cases stopping costs more, so each command relied on is checked.

**git's `-z`.** By default git quotes a name with a byte over 0x80, so a check filtering the
list by pattern passes having read nothing. `core.quotePath=false` still escapes tabs, newlines,
quotes and backslashes; `-z` escapes none.

**Quoting and arrays.** Unquoted, a script breaks on a name with a space, `*` or `-`; a string
can't hold arguments with spaces. Costs: noise, and arrays need Bash.

**Temporary files.** Another user can plant a link at a predictable path. Costs: a trap line.

**Tools.** The standard's *Language toolchains* names these three. ShellCheck finds unquoted
expansions, masked statuses (SC2155) and unguarded deletes (SC2115); shfmt ends layout debates.
Costs: three tools to pin, and some directives. A hand read misses most of what ShellCheck
finds, so the lint stays `UNVERIFIABLE-HERE`.

## Facts

bash-security holds the versions and the shared facts.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `sh-bash44-empty-array` | 4.4 allows empty arrays under `-u` | [CHANGES](https://tiswww.case.edu/php/chet/bash/CHANGES) | "nounset option is enabled no longer throws an unbound variable error" | 2026-10-26 | 2027-10-26 |
| `sh-macos-zsh` | zsh since macOS 10.15 | [Apple](https://support.apple.com/en-us/102360) | "Starting with macOS 10.15, your Mac uses zsh" | 2026-10-26 | 2027-10-26 |
| `sh-posix-pipefail` | POSIX.1-2024 added it | [POSIX](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html) | "adding -o pipefail" | 2026-10-26 | 2027-10-26 |
| `sh-posix-print0` | POSIX.1-2024 added `-print0`, `-0` | [find](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/find.html), [xargs](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/xargs.html) | "adding the -print0 primary" and "adding the -r and -0 options" | 2026-10-26 | 2027-10-26 |
| `sh-errexit` | `-e` is off in conditions | [Manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "part of the test in an if statement" and "shell function executes in a context where -e is being ignored" | 2026-10-26 | 2027-10-26 |
| `sh-local-status` | `local` has its own status | [Manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "zero unless local is used outside a function" | 2026-10-26 | 2027-10-26 |
| `sh-arith-status` | `((0))` returns 1 | [Manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "otherwise the return status is 1" | 2026-10-26 | 2027-10-26 |
| `sh-signal-status` | Signal N: 128+N | [Manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "128+N as the exit status" | 2026-10-26 | 2027-10-26 |
| `sh-pipefail-bash` | `pipefail` is off by default | [Manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "last (rightmost) command to exit with a non-zero status" and "This option is disabled by default." | 2026-10-26 | 2027-10-26 |
| `sh-pipestatus` | `PIPESTATUS` has each status | [Manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "list of exit status values from the commands" | 2026-10-26 | 2027-10-26 |
| `sh-pipeline-subshell` | Stages are subshells | [Manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "where pipes are created, is executed in its own subshell" | 2026-10-26 | 2027-10-26 |
| `sh-read-r` | `read -r` keeps backslashes | [Manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "backslash does not act as an escape character" | 2026-10-26 | 2027-10-26 |
| `sh-sed-inplace` | BSD needs a suffix | [GNU](https://man7.org/linux/man-pages/man1/sed.1.html), [FreeBSD](https://man.freebsd.org/cgi/man.cgi?query=sed&sektion=1) | "-i[SUFFIX], --in-place[=SUFFIX]" and "[-i extension]" | 2026-10-26 | 2027-10-26 |
| `sh-google` | Bash only; rewrite past 100 lines | [Google](https://google.github.io/styleguide/shellguide.html) | "the only shell scripting language permitted" and "more than 100 lines long" and "rewrite it in a more structured language" | 2026-10-26 | 2027-10-26 |
| `sh-google-license` | Google's guides: CC BY 3.0 | [LICENSE](https://raw.githubusercontent.com/google/styleguide/gh-pages/LICENSE) | "Attribution 3.0 Unported" | 2026-10-26 | 2027-10-26 |
| `sh-git-quotepath` | git quotes unusual names unless given `-z` | [git-config](https://git-scm.com/docs/git-config) | "bytes with values larger than 0x80" and "Double-quotes, backslash and control characters are always escaped" and "verbatim using the -z option" and "The default value is true." | 2026-10-27 | 2027-10-27 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Bash](https://tiswww.case.edu/php/chet/bash/bashtop.html) | Behavior, releases | GFDL 1.3, GPL-3.0: short quotes |
| [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/) | `pipefail`, `-print0` | All rights reserved: short quotes |
| [ShellCheck](https://www.shellcheck.net/) | dash, releases | GPL-3.0; wiki states none: short quotes |
| [shfmt](https://github.com/mvdan/sh), [bats-core](https://github.com/bats-core/bats-core) | Releases | BSD-3-Clause, MIT: pointed to |
| [Google](https://google.github.io/styleguide/shellguide.html) | Shell choice | CC BY 3.0 (fact `sh-google-license`): short quotes, attributed |
| [git](https://git-scm.com/docs/git-config), [shellcheck-py](https://pypi.org/project/shellcheck-py/) | `core.quotePath`; ShellCheck from PyPI | GPL-2.0, MIT: short quotes |
| [man7.org](https://man7.org/linux/man-pages/), [FreeBSD](https://man.freebsd.org/), [Apple](https://support.apple.com/en-us/102360), [Debian](https://packages.debian.org/trixie/dash) | `sed -i`, default shells | Each site's terms: short quotes |
