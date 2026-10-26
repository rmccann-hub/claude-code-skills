# Bash coding

Read this for writing, reviewing or fixing a Bash or POSIX `sh` script: choosing the shell and
its shebang, `set -euo pipefail` and where it fails you, quoting, arrays, tests, reading lines
and file names, temporary files and cleanup, exit statuses through pipes, portability to
macOS's Bash and to dash, ShellCheck and shfmt, and shell security.

Containers, Linux administration and networking are the planned operations skill's. A CI
workflow file, including which shell runs a step and with which options, is git-workflows'.
Test design is the planned testing skill's; this module only names bats as the runner. Where a
shell tool's files go, and which tools it uses, are the project-bootstrap-and-audit standard's
*Language toolchains* and *Project shapes and layout*. When to stop writing shell and start
writing Python is its *Choosing a language and runtime*.

## Contents

- [Rules](#rules): the shell, strict mode, quoting, arrays, lines and file names, cleanup,
  destructive commands, security, tools
- [Mistakes](#mistakes), [Audit](#audit), [Why](#why), [Facts](#facts), [Sources](#sources)

## Rules

1. **Choose Bash or POSIX `sh` on purpose, and say which in the shebang.** `#!/usr/bin/env bash`
   for Bash; `#!/bin/sh` only for a script that is POSIX throughout and linted as `sh`.
2. **Start a Bash script with `set -euo pipefail`, and know where it doesn't stop you:** in
   conditions, in functions called from them, behind `local`, and after `((n++))` at zero.
3. **Quote every expansion:** `"$var"`, `"$(cmd)"`, `"${list[@]}"`. Leave one unquoted only
   where splitting is the intent, with a ShellCheck directive saying so.
4. **Hold a list in an array, never in a string:** a Bash array, or `"$@"` in POSIX `sh`.
5. **Read lines with `while IFS= read -r`, and file names with `find -print0` and `xargs -0`
   or `find -exec … {} +`.** Never parse `ls`.
6. **Make temporary files with `mktemp`, and remove them in an `EXIT` trap.**
7. **Guard each destructive command:** `${var:?}` in a path, `--` before operands, and a dry
   run before the real one.
8. **Keep secrets off the command line and untrusted text away from `eval`.** Never pipe a
   downloaded script into a shell.
9. **Lint with ShellCheck and format with shfmt, locally and in CI.** bats runs the tests.

### The shell and the shebang

- **Bash where it's there, POSIX `sh` where it might not be.** Debian's `/bin/sh` is dash
  (fact `sh-debian-dash`), so a `#!/bin/sh` script using `[[`, arrays or `function` fails
  there, while working where `sh` is Bash. `sh tool` ignores the shebang; run `./tool`.
- **`#!/usr/bin/env bash`** runs the first Bash on `PATH`, so on macOS a newer Bash installed
  beside the system's runs the script; `/bin/bash` there is 3.2 (fact `sh-macos-bash`). zsh is
  macOS's login shell (fact `sh-macos-zsh`), but the shebang, not the login shell, decides.
- **Know which Bash a feature needs.** Associative arrays and `mapfile` came in 4.0 (fact
  `sh-bash-versions`). An empty array under `set -u` is an error before 4.4 (fact
  `sh-bash44-empty-array`). `${ cmd; }` needs 5.3 (fact `sh-bash53-nofork`), the current
  release (fact `sh-bash-current`). A script for macOS's 3.2 avoids them, or checks first:

```bash
if ((BASH_VERSINFO[0] < 4)); then
  printf '%s needs Bash 4 or later; this is %s\n' "${0##*/}" "$BASH_VERSION" >&2
  exit 1
fi
```

### Strict mode and its traps

`set -e` exits on a failing command, `-u` on an unset variable, and `pipefail` fails a pipeline
when any stage fails, not only the last (fact `sh-pipefail-bash`). Each has gaps:

- **`-e` is off in a condition:** after `if`, `while` or `until`, left of `&&` or `||`, and
  after `!`. A function called from there runs with `-e` off throughout its body (fact
  `sh-errexit`), so `if deploy; then` hides every failure inside `deploy`.
- **`local x=$(cmd)` hides `cmd`'s failure,** because the status is `local`'s (fact
  `sh-local-status`). Declare, then assign, on two lines. `export` and `readonly` do the same.
- **`((n++))` fails when `n` is 0,** since an arithmetic command whose value is zero returns 1
  (fact `sh-arith-status`). Under `-e` the script stops there, silently. Write
  `n=$((n + 1))`.
- **A command substitution runs without `-e` in Bash** unless `shopt -s inherit_errexit`
  (Bash 4.4; fact `sh-bash-versions`), so `out=$(step1; step2)` runs `step2` after `step1`
  fails.
- **`pipefail` fails a pipeline whose reader stops early.** In `producer | head -n 1` the
  producer can die of `SIGPIPE`, giving status 141, which is 128 plus the signal's number
  (fact `sh-signal-status`). Mark that one pipeline: `producer | head -n 1 || true`.
  ShellCheck's unreleased changes add a warning for `grep -q` there (fact `sh-shellcheck`).
- **Each stage's status** is in `PIPESTATUS`, read on the next line (fact `sh-pipestatus`).
- **In POSIX `sh`,** `pipefail` is standard since 2024 (fact `sh-posix-pipefail`), but dash
  gained it only in 0.5.13 (fact `sh-dash-pipefail`), and Debian 13 ships 0.5.12 (fact
  `sh-debian-dash`). Turn it on where the shell has it:

```sh
set -eu
# shellcheck disable=SC3040
(set -o pipefail 2>/dev/null) && set -o pipefail
```

### Quoting, tests and globs

- **An unquoted expansion is split on `IFS` and then globbed** (fact `sh-expansion`). A file
  named `a b` becomes two arguments, and a value of `*` becomes the directory's listing.
- **`[[ … ]]` in Bash** doesn't split or glob (fact `sh-expansion`), and it has `&&`, `||` and
  `=~`. The right side of `==` is a pattern, so quote it to compare literally:
  `[[ $a == "$b" ]]`. In POSIX `sh`, write `[ "$a" = "$b" ]`, each operand quoted.
- **Numbers** compare with `(( a > b ))` in Bash, or `[ "$a" -gt "$b" ]`; inside `[ ]`, `>`
  is a redirection. A value from input reaches `(( ))`, `$(( ))`, `let` or `[[ … -gt … ]]` only
  after it's checked to be digits: Bash evaluates it as an expression, and a command in an array
  subscript runs (fact `sh-arith-eval`). `[ "$a" -gt "$b" ]` refuses such a value.
- **`printf '%s\n' "$x"`, not `echo "$x"`,** for data: `echo` differs between shells on
  backslashes and a leading `-n` (fact `sh-echo`).
- **A glob that matches nothing stays as written** (fact `sh-expansion`). Check `[ -e "$f" ]`
  in the loop, or `shopt -s nullglob` in Bash. Write `./*.txt`, not `*.txt`, so a file named
  `-rf` can't become an option.

### Arrays

Build a command's arguments in an array, and expand it quoted:

```bash
src=build dest=/srv/www dry_run=1
args=(--archive --delete)
if ((dry_run)); then
  args+=(--dry-run)
fi
rsync "${args[@]}" -- "$src/" "$dest/"
```

In POSIX `sh`, the positional parameters are the one array: `set -- "$@" --dry-run`. On Bash
before 4.4 with `set -u`, expand a list that may be empty as `${args[@]+"${args[@]}"}`.

### Lines and file names

- **`while IFS= read -r line`:** `IFS=` keeps leading and trailing spaces, and `-r` keeps
  backslashes (fact `sh-read-r`). `|| [[ -n $line ]]` catches a last line with no newline.
- **A loop at the end of a pipe runs in a subshell in Bash** (fact `sh-pipeline-subshell`), so
  `cmd | while read …` loses every variable it sets. Feed it with `done < <(cmd)` instead.
- **File names can hold spaces, newlines and leading dashes.** `find -print0` with `xargs -0`
  is POSIX since 2024 (fact `sh-posix-print0`); `find -exec … {} +` works on older systems
  too. In Bash, `read -d ''` reads the same NUL-separated list:

```bash
while IFS= read -r line || [[ -n $line ]]; do
  printf '%s\n' "$line"
done <input.txt

find . -type f -name '*.md' -exec grep -l -e 'TODO' -- {} +

while IFS= read -r -d '' path; do
  printf 'found: %s\n' "$path"
done < <(find . -type f -name '*.log' -print0)
```

### Temporary files and cleanup

`mktemp` creates a new file or directory with a random name, and GNU's gives only its owner
access (fact `sh-mktemp`). Set an `EXIT` trap to remove it on the next line. POSIX lets a shell
skip that trap when a signal ends the script (fact `sh-exit-trap`), so a `sh` script traps the
signals too:

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

### Destructive commands

- **`${var:?}` in every path a command deletes or overwrites.** `rm -rf "$dir/"*` with `dir`
  empty deletes from `/`; `"${dir:?}/"*` stops the script instead (fact `sh-sc2115`).
- **`--` before file operands,** so a name starting with `-` isn't read as an option.
- **List first, act second.** A script that deletes prints what it would delete by default:

```bash
#!/usr/bin/env bash
# Lists *.log files older than 30 days under DIR; deletes them only with --delete.
set -euo pipefail

dir=${1:?usage: prune-logs DIR [--delete]}
if [[ ${2-} == --delete ]]; then
  find "$dir" -type f -name '*.log' -mtime +30 -exec rm -f -- {} +
else
  find "$dir" -type f -name '*.log' -mtime +30 -print
fi
```

### Security

- **No `eval` on anything a user, a file or the network supplied.** Dispatch with `case`, and
  pass data as arguments. The same goes for `bash -c "$text"`, sourcing a downloaded file, and
  running an unquoted `$cmd`.
- **Never pipe a fetched script into a shell.** Download it to a file, check it against a
  signature or checksum you trust separately, read it, then run it.
- **Secrets stay off the command line,** where other local users can read them (fact
  `sh-cmdline`). Read them from a file or the environment, and hand them to tools that read
  files. curl takes headers from a file (fact `sh-curl-header-file`):

```bash
# auth-header holds one line: Authorization: Bearer CHANGEME
curl -fsS -H @"$HOME/.config/example/auth-header" https://api.example.com/v1/status
```

- **Validate input against what you accept,** such as `[[ $id =~ ^[0-9]+$ ]]`, rather than
  stripping what you fear. A number from input is checked this way before any arithmetic: a
  value such as `x[$(cmd)]` runs `cmd` inside `(( ))` (fact `sh-arith-eval`).

### Tools

- **ShellCheck** (fact `sh-shellcheck`) reads the shebang to pick the dialect:
  `shellcheck bin/* lib/*.sh`. Fix each warning, or disable it on its line with the reason.
- **shfmt** (fact `sh-shfmt`) takes its options from `.editorconfig`; `shfmt -d bin lib`
  fails with a diff, for CI.
- **bats** (fact `sh-bats-version`) runs `.bats` files: `bats tests`.
- **`sed -i` differs between GNU and BSD** (fact `sh-sed-inplace`). A portable script writes to
  a temporary file and moves it over the original.

## Mistakes

- **`#!/bin/sh` on a Bash script,** which fails on Debian. Name Bash, or lint with
  `shellcheck --shell=sh` and remove each Bash feature.
- **`((count++))` under `set -e`,** which stops the script when `count` is 0. Use
  `count=$((count + 1))`.
- **`local out=$(cmd)` or `export out=$(cmd)`,** which hides `cmd`'s failure. Split the line.
- **`for f in $(ls)`, `for f in $(find …)` and `ls | while read`,** which split names on
  spaces. Use a glob, `find -exec`, or `-print0` with `read -d ''`.
- **Options kept in a string,** such as `opts="--exclude '*.tmp'"` then `rsync $opts`. The
  quotes inside stay literal. Use an array.
- **`rm -rf "$dir/"*` without `:?`,** and `rm $file` without quotes or `--`.
- **A fixed temporary path such as `/tmp/myscript.tmp`,** which another user can create first.
- **A secret in an argument,** such as `curl -H "Authorization: Bearer $token"` or
  `mysql -p"$password"`. Use a file the tool reads, or its environment variable.
- **`cd "$dir"` with no check,** after which the script runs on in the wrong directory. Write
  `cd -- "$dir" || exit`, or run the step in a subshell.
- **Arithmetic on an unchecked argument,** such as `(( $1 > 0 ))`, which runs a command hidden
  in the argument. Check it against `^[0-9]+$` first.
- **A comment after a line-continuation backslash,** which breaks the continuation, so the next
  line runs as a command of its own. Put the comment on its own line.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| ShellCheck passes | `shellcheck` on every script | `GAP` per warning; `BLOCKER` for SC2115 | Fix it, or disable it on the line with the reason |
| Dialect matches the shebang | `shellcheck --shell=sh` on `#!/bin/sh` scripts: `[[`, arrays, `source`, unprobed `pipefail` | `DRIFT` | Name Bash, or make the script POSIX |
| Strict mode | A Bash script without `set -euo pipefail` near the top | `GAP` | Add it, then fix what it exposes |
| Masked failures | `local`, `export` or `readonly` assigning `$(…)`; `((n++))` under `-e`; a function with side effects as an `if` condition | `GAP` | Split the line; `n=$((n + 1))`; check inside the function |
| Unsafe deletes | `rm -r` or `rm -f` on a variable path without `:?` or `--`; a deleting script with no dry run | `BLOCKER` | `"${dir:?}/"`, `--`, and a listing by default |
| Temporary files | Fixed paths under `/tmp`, or `mktemp` with no `EXIT` trap | `GAP` | `mktemp`, and a trap on the next line |
| Secrets on the command line | Tokens or passwords in arguments, or printed to the log | `BLOCKER` | A file or environment variable the tool reads |
| Arithmetic on input | `(( ))`, `$(( ))`, `let` or `[[ -eq ]]`-style tests on a value from arguments, files or the network with no digits check before it | `BLOCKER` | `[[ $x =~ ^[0-9]+$ ]]` first (fact `sh-arith-eval`) |
| `eval` and fetched code | `eval`, `bash -c` or `source` on input; a downloaded script piped into a shell | `BLOCKER` | `case` dispatch; download, verify, read, run |
| Formatting | `shfmt -d` on the scripts | `DRIFT` | `shfmt -w`, and a CI step |
| Version reach | Bash 4 features in a script claimed to run on macOS's `/bin/bash` | `DRIFT` | Remove them, or check `BASH_VERSINFO` |

## Why

### Choosing the shell

**The advice.** Bash, through `#!/usr/bin/env bash`, where you know Bash is installed; POSIX
`sh` where it may not be, such as a minimal container.

**Why.** The shebang is the script's contract. `#!/bin/sh` promises POSIX, Debian holds it to
that with dash (fact `sh-debian-dash`), and a Bash feature then fails at run time, often on a
branch the tests didn't take. `env` finds the Bash the user installed, not macOS's 3.2.

**What others do.** Google's guide allows only Bash for executables, and starts them
`#!/bin/bash`. It says to rewrite a script past 100 lines, or with complex control flow, in a
structured language (fact `sh-google`).

**What it costs.** `env` follows `PATH`, so a cron job or `sudo` can find another Bash, or none,
and POSIX `sh` has no arrays.

**When to choose differently.** A system script with a fixed `PATH` names `/bin/bash`. Past a
hundred lines, or with structured data, move to Python (the standard's *Choosing a language and
runtime*).

### Strict mode

**The advice.** `set -euo pipefail` in every Bash script, and its gaps checked by hand.

**Why.** Without `-e`, a failed step is ignored and the next runs on bad input. Without
`pipefail`, a download piped into `tar` reports `tar`'s success when the download failed,
since a pipeline's status is its last command's by default (fact `sh-pipefail-bash`). Without
`-u`, a misspelled variable expands to nothing.

**What it costs.** A command that fails by design, such as `grep` with no match, needs an `if`
or `|| true`, and a reader that stops early fails under `pipefail`. The other choice, checking
every status by hand with no `-e`, is more code to get wrong; this module keeps `-e` as the net
and names its holes (fact `sh-errexit`).

### Quoting and arrays

**The advice.** Quote every expansion, and keep lists in arrays.

**Why.** Splitting and globbing apply to every unquoted expansion (fact `sh-expansion`), so a
script works on its author's file names and breaks on the first with a space, a `*` or a
leading `-`. A string can't hold arguments that contain spaces; an array can.

**What it costs.** Noisier code, and arrays tie the script to Bash.

### Temporary files, deletes and secrets

**The advice.** `mktemp` with an `EXIT` trap; `:?`, `--` and a dry run around deletes; secrets
in files, not arguments.

**Why.** A predictable `/tmp` path lets another user plant a file or link there first. An
empty variable in a delete path deletes from the root directory, and `${dir:?}` costs four
characters (fact `sh-sc2115`). A command line is visible to other local users while the process
runs, and curl's own manual says to keep credentials off it (fact `sh-cmdline`).

**What it costs.** A trap line per script, and a second run to delete for real.

### Linting, formatting and tests

**The advice.** ShellCheck and `shfmt -d` in CI, and bats for tests: the three tools the
standard's *Language toolchains* names for shell.

**Why.** ShellCheck finds unquoted expansions, masked statuses (SC2155), unguarded deletes
(SC2115) and features the shebang's shell lacks, and its wiki explains each code. shfmt ends
arguments about layout, from the same `.editorconfig` the editor reads.

**What it costs.** Three tools to install and pin in CI, and now and then a directive.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked 2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `sh-bash-current` | Bash 5.3 is the current release | [Bash home page](https://tiswww.case.edu/php/chet/bash/bashtop.html) | "The current version of bash is bash-5.3" | 2026-10-26 | 2027-04-26 |
| `sh-bash53-nofork` | Bash 5.3 added `${ command; }`, command substitution without a subshell | [Bash NEWS](https://tiswww.case.edu/php/chet/bash/NEWS) | "to capture the output of COMMAND without forking a child process" | 2026-10-26 | 2027-10-26 |
| `sh-bash-versions` | Bash 4.0 added associative arrays and `mapfile`; 4.4 added `inherit_errexit`, and command substitutions otherwise run without `-e` | [Bash NEWS](https://tiswww.case.edu/php/chet/bash/NEWS) | "The shell provides associative array variables" and "to populate an array with lines from a given file" and "causes command substitutions to inherit the -e option. By default, those subshells disable -e." | 2026-10-26 | 2027-10-26 |
| `sh-bash44-empty-array` | Before Bash 4.4, expanding an empty array under `set -u` is an error | [Bash CHANGES](https://tiswww.case.edu/php/chet/bash/CHANGES) | "when the nounset option is enabled no longer throws an unbound variable error" | 2026-10-26 | 2027-10-26 |
| `sh-macos-bash` | The Bash in Apple's published macOS source is 3.2 | [apple-oss-distributions/bash](https://raw.githubusercontent.com/apple-oss-distributions/bash/main/bash-3.2/configure.in) | "Configure script for bash-3.2" | 2026-10-26 | 2027-04-26 |
| `sh-macos-zsh` | zsh has been macOS's default login and interactive shell since 10.15 | [Apple Support](https://support.apple.com/en-us/102360) | "Starting with macOS 10.15, your Mac uses zsh as the default login shell and interactive shell." | 2026-10-26 | 2027-10-26 |
| `sh-debian-dash` | Debian 13 (trixie) ships dash 0.5.12 as its default system shell | [Debian packages: dash in trixie](https://packages.debian.org/trixie/dash) | "Package: dash (0.5.12-12)" and "it is used as the default system shell on Debian systems" | 2026-10-26 | 2027-04-26 |
| `sh-dash-pipefail` | dash added `pipefail` in 0.5.13 | [ShellCheck wiki, SC3040](https://www.shellcheck.net/wiki/SC3040) | "dash version 5.13 included pipefail along with other POSIX.1-2024 features." | 2026-10-26 | 2027-10-26 |
| `sh-posix-pipefail` | POSIX.1-2024 added `set -o pipefail` | [POSIX.1-2024, Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html) | "Austin Group Defect 789 is applied, adding -o pipefail." | 2026-10-26 | 2027-10-26 |
| `sh-posix-print0` | POSIX.1-2024 added `find -print0` and `xargs -0` | [POSIX.1-2024 find](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/find.html), [xargs](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/xargs.html) | "Austin Group Defect 243 is applied, adding the -print0 primary." and "Austin Group Defect 243 is applied, adding the -r and -0 options." | 2026-10-26 | 2027-10-26 |
| `sh-exit-trap` | POSIX lets a shell skip the `EXIT` trap when a signal ends it | [POSIX.1-2024, Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html) | "and may occur when the shell terminates abnormally as a result of delivery of a signal" | 2026-10-26 | 2027-10-26 |
| `sh-echo` | `echo` isn't portable with escapes or a leading option | [POSIX.1-2024 echo](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/echo.html) | "It is not possible to use echo portably across all POSIX systems unless escape sequences are omitted" | 2026-10-26 | 2027-10-26 |
| `sh-errexit` | `set -e` doesn't exit on a failure in a condition, nor anywhere in a function called from one | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "The shell does not exit if the command that fails is part of the command list immediately following a while or until reserved word, part of the test in an if statement" and "none of the commands executed within the compound command or function body will be affected by the -e setting" | 2026-10-26 | 2027-10-26 |
| `sh-local-status` | `local`'s status is its own, not the assigned command's | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "The return status is zero unless local is used outside a function" | 2026-10-26 | 2027-10-26 |
| `sh-arith-status` | An arithmetic command whose value is 0 returns 1 | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "If the value of the expression is non-zero, the return status is 0; otherwise the return status is 1." | 2026-10-26 | 2027-10-26 |
| `sh-signal-status` | A command killed by signal N exits with 128 + N | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "When a command terminates on a fatal signal whose number is N, Bash uses the value 128+N as the exit status." | 2026-10-26 | 2027-10-26 |
| `sh-pipefail-bash` | Bash's `pipefail` is off by default | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "If set, the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status" and "This option is disabled by default." | 2026-10-26 | 2027-10-26 |
| `sh-pipestatus` | `PIPESTATUS` holds each stage's status | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "containing a list of exit status values from the commands in the most-recently-executed foreground pipeline" | 2026-10-26 | 2027-10-26 |
| `sh-pipeline-subshell` | Each stage of a Bash pipeline runs in a subshell | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "Each command in a multi-command pipeline, where pipes are created, is executed in its own subshell" | 2026-10-26 | 2027-10-26 |
| `sh-expansion` | Unquoted expansions are split; `[[ … ]]` doesn't split or glob; a glob with no match stays as written | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "The shell scans the results of parameter expansion, command substitution, and arithmetic expansion that did not occur within double quotes for word splitting." and "The words between the [[ and ]] do not undergo word splitting and filename expansion." and "If no matching filenames are found, and the shell option nullglob is disabled, the word is left unchanged." | 2026-10-26 | 2027-10-26 |
| `sh-arith-eval` | Bash evaluates a variable's value as an arithmetic expression when an expression refers to it | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "The value of a variable is evaluated as an arithmetic expression when it is referenced" | 2026-10-26 | 2027-10-26 |
| `sh-read-r` | `read -r` keeps backslashes | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "If this option is given, backslash does not act as an escape character." | 2026-10-26 | 2027-10-26 |
| `sh-mktemp` | GNU `mktemp` creates files readable and writable only by their owner | [mktemp(1)](https://man7.org/linux/man-pages/man1/mktemp.1.html) | "Files are created u+rw, and directories u+rwx, minus umask restrictions." | 2026-10-26 | 2027-10-26 |
| `sh-sc2115` | `${var:?}` fails when the variable is empty or unset | [ShellCheck wiki, SC2115](https://www.shellcheck.net/wiki/SC2115) | "Using :? will cause the command to fail if the variable is null or unset." | 2026-10-26 | 2027-10-26 |
| `sh-cmdline` | A process's command line can be read from `/proc`, and curl says to keep credentials off it | [proc_pid_cmdline(5)](https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html), [curl manual](https://curl.se/docs/manpage.html) | "This read-only file holds the complete command line for the process" and "Such sensitive data should be retrieved from a file instead or similar and never used in clear text in a command line." | 2026-10-26 | 2027-10-26 |
| `sh-curl-header-file` | curl reads headers from a file with `-H @file` | [curl manual](https://curl.se/docs/manpage.html) | "This option can take an argument in @filename style, which then adds a header for each line in the input file." | 2026-10-26 | 2027-10-26 |
| `sh-sed-inplace` | GNU sed's `-i` takes an optional attached suffix; FreeBSD's takes a required one | [GNU sed(1)](https://man7.org/linux/man-pages/man1/sed.1.html), [FreeBSD sed(1)](https://man.freebsd.org/cgi/man.cgi?query=sed&sektion=1) | "-i[SUFFIX], --in-place[=SUFFIX]" and "[-i extension]" | 2026-10-26 | 2027-10-26 |
| `sh-google` | Google's shell guide allows only Bash for executables, and says to rewrite a script past 100 lines | [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) | "Bash is the only shell scripting language permitted for executables." and "Executables must start with #!/bin/bash and minimal flags." and "If you are writing a script that is more than 100 lines long, or that uses non-straightforward control flow logic, you should rewrite it in a more structured language now." | 2026-10-26 | 2027-10-26 |
| `sh-google-license` | Google's style guides are under CC BY 3.0 | [google/styleguide LICENSE](https://raw.githubusercontent.com/google/styleguide/gh-pages/LICENSE) | "Attribution 3.0 Unported" | 2026-10-26 | 2027-10-26 |
| `sh-shellcheck` | ShellCheck 0.11.0, from 2025-08-03, is the newest release; its unreleased changes warn about `grep -q` under `pipefail` | [ShellCheck changelog](https://raw.githubusercontent.com/koalaman/shellcheck/master/CHANGELOG.md) | "v0.11.0 - 2025-08-03" and "in pipelines under pipefail" | 2026-10-26 | 2027-04-26 |
| `sh-shfmt` | shfmt 3.14.1, from 2026-09-06, is the newest release, and it reads EditorConfig files | [mvdan/sh changelog](https://raw.githubusercontent.com/mvdan/sh/master/CHANGELOG.md), [shfmt(1)](https://raw.githubusercontent.com/mvdan/sh/master/cmd/shfmt/shfmt.1.scd) | "[3.14.1] - 2026-09-06" and "If any EditorConfig files are found, they will be used to apply formatting options." | 2026-10-26 | 2027-04-26 |
| `sh-bats-version` | bats-core 1.14.0, from 2026-07-21, is the newest release | [bats-core changelog](https://raw.githubusercontent.com/bats-core/bats-core/master/docs/CHANGELOG.md) | "[1.14.0] - 2026-07-21" | 2026-10-26 | 2027-04-26 |

## Sources

Every rule here is in this module's own words. Sources are quoted briefly, each quote a dated
fact above.

| Source | Used for | License |
|---|---|---|
| [Bash Reference Manual](https://tiswww.case.edu/php/chet/bash/bashref.html), the maintainer's copy | Strict mode, expansions, `read`, pipelines | GFDL 1.3: facts in our own words, short quotes |
| [Bash home page, NEWS and CHANGES](https://tiswww.case.edu/php/chet/bash/bashtop.html) | The current release, and which version added what | Part of Bash, GPL-3.0: short quotes |
| [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/) | `pipefail`, `-print0`, `xargs -0`, `EXIT` traps, `echo` | Copyright IEEE and The Open Group, all rights reserved: short quotes |
| [ShellCheck](https://www.shellcheck.net/) wiki and changelog | SC2115, SC3040, dash's `pipefail`, releases | Tool GPL-3.0; the wiki states no license: facts in our own words, short quotes |
| [shfmt (mvdan/sh)](https://github.com/mvdan/sh) | EditorConfig, release | BSD-3-Clause: pointed to |
| [bats-core](https://github.com/bats-core/bats-core) | Test runner, release | MIT: pointed to |
| [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) | Bash for executables, the 100-line advice | CC BY 3.0 (fact `sh-google-license`): short quotes, with attribution |
| [curl manual](https://curl.se/docs/manpage.html) | Headers from a file, credentials off the command line | curl license, MIT style: short quotes |
| [man7.org](https://man7.org/linux/man-pages/) (proc_pid_cmdline(5), mktemp(1), GNU sed(1)) and [FreeBSD sed(1)](https://man.freebsd.org/cgi/man.cgi?query=sed&sektion=1) | Command-line visibility, `mktemp`, `sed -i` | Each page's own license: short quotes |
| [Apple Support](https://support.apple.com/en-us/102360) and [Apple's Bash source](https://github.com/apple-oss-distributions/bash) | macOS's shells | Apple's terms; the source is GPL: facts with short quotes |
| [Debian packages](https://packages.debian.org/trixie/dash) | Debian's `/bin/sh` | Debian's site: a fact with a short quote |
