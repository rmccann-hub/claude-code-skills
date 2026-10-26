# Bash security

Read this for the parts of a Bash or POSIX `sh` script where a mistake destroys data or runs
someone else's code: deletes and other destructive commands, `eval` and fetched scripts,
arithmetic on input, secrets on the command line, and checking input.

The rest of shell scripting, from the shebang and strict mode to quoting, arrays, temporary
files, portability and ShellCheck, is bash-coding's. Secret storage and rotation are the
project-bootstrap-and-audit standard's; a secret already committed is git-workflows'.
Containers and Linux administration are the planned operations skill's.

## Rules

1. **Guard each destructive command:** `${var:?}` in a path, quotes and `--` around operands,
   and a dry run before the real one.
2. **Keep untrusted text away from `eval`,** `bash -c`, `source` and an unquoted `$cmd`.
   Dispatch with `case`, and pass data as arguments.
3. **Never pipe a downloaded script into a shell.** Download it, verify it, read it, then run
   it.
4. **Check a number from input is digits before any arithmetic on it.**
5. **Keep secrets off the command line:** read them from a file or the environment, and hand
   them to tools that read files.
6. **Validate input against what you accept,** rather than stripping what you fear.

### Destructive commands

- **`${var:?}` in every path a command deletes or overwrites.** `rm -rf "$dir/"*` with `dir`
  empty deletes from `/`; `"${dir:?}/"*` stops the script instead (fact `sh-sc2115`).
- **Quote the operand, and put `--` before it.** Unquoted, `$file` is split and globbed (fact
  `sh-expansion`), and a name starting with `-` is read as an option.
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

### `eval` and fetched code

- **No `eval` on anything a user, a file or the network supplied.** The same goes for
  `bash -c "$text"`, sourcing a downloaded file, and running an unquoted `$cmd`. Choose the
  action with `case`, and pass the data as arguments:

```bash
action=${1:?usage: tool build|test}
case $action in
  build) make all ;;
  test) make check ;;
  *)
    printf 'unknown action: %s\n' "$action" >&2
    exit 2
    ;;
esac
```

- **To build a command from parts,** use an array (bash-coding's *Arrays*), never a string
  passed to `eval`.
- **Never pipe a fetched script into a shell.** Download it to a file, check it against a
  signature or checksum you trust separately, read it, then run it.

### Arithmetic on input

`(( ))`, `$(( ))`, `let` and the `[[ … -gt … ]]` tests evaluate a variable's value as an
arithmetic expression (fact `sh-arith-eval`), and a command in an array subscript runs: a value
such as `x[$(cmd)]` runs `cmd`. So a value from input reaches arithmetic only after it's
checked to be digits. `[ "$a" -gt "$b" ]` refuses such a value. A leading `0` reads as octal
(fact `sh-arith-octal`), so `08` is an error; `10#$n` forces decimal:

```bash
count=${1:?usage: retry COUNT}
if [[ ! $count =~ ^[0-9]+$ ]]; then
  printf 'not a number: %s\n' "$count" >&2
  exit 2
fi
count=$((10#$count))
```

### Secrets

- **Secrets stay off the command line,** where other local users can read them (fact
  `sh-cmdline`). Read them from a file or the environment, and hand them to tools that read
  files. curl takes headers from a file (fact `sh-curl-header-file`):

```bash
# auth-header holds one line: Authorization: Bearer CHANGEME
curl -fsS -H @"$HOME/.config/example/auth-header" https://api.example.com/v1/status
```

- **A secret written to disk goes in a `mktemp` file,** which GNU's `mktemp` makes readable by
  its owner alone (fact `sh-mktemp`), removed by a trap on `EXIT` and on the signals, since a
  signal may skip the `EXIT` trap (fact `sh-exit-trap`).

### Validating input

- **Accept what matches a pattern,** such as `[[ $id =~ ^[0-9]+$ ]]`, rather than stripping
  what you fear. `[[ … ]]` doesn't split or glob the value (fact `sh-expansion`).
- **Print untrusted text with `printf '%s\n' "$x"`,** never `echo`, which may read a leading
  `-n` or backslashes in it (fact `sh-echo`).

## Mistakes

- **`rm -rf "$dir/"*` without `:?`,** and `rm $file` without quotes or `--`.
- **A secret in an argument,** such as `curl -H "Authorization: Bearer $token"` or
  `mysql -p"$password"`. Use a file the tool reads, or its environment variable.
- **Arithmetic on an unchecked argument,** such as `(( $1 > 0 ))`, which runs a command hidden
  in the argument. Check it against `^[0-9]+$` first.
- **`eval` to build a command from parts,** which runs any `;` or `$(…)` in them. Use an array.
- **A blocklist,** such as stripping `;` and `|` from input, which misses the next character.
  Match what you accept.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Unsafe deletes | `rm -r` or `rm -f` on a variable path without `:?` or `--`; a deleting script with no dry run | `BLOCKER` | `"${dir:?}/"`, `--`, and a listing by default |
| Secrets on the command line | Tokens or passwords in arguments, or printed to the log | `BLOCKER` | A file or environment variable the tool reads |
| Arithmetic on input | `(( ))`, `$(( ))`, `let` or `[[ -eq ]]`-style tests on a value from arguments, files or the network with no digits check before it | `BLOCKER` | `[[ $x =~ ^[0-9]+$ ]]` first (fact `sh-arith-eval`) |
| `eval` and fetched code | `eval`, `bash -c` or `source` on input; a downloaded script piped into a shell | `BLOCKER` | `case` dispatch; download, verify, read, run |

## Why

### Guarding deletes

**The advice.** `:?`, quotes and `--` around every deleted path, and a dry run by default.

**Why.** An empty variable in a delete path deletes from the root directory, and `${dir:?}`
costs four characters (fact `sh-sc2115`). A file named `-rf` becomes an option without `--`.

**What it costs.** A second run to delete for real. A script run unattended, such as from
cron, passes `--delete` in its schedule, so the default stays safe.

### `eval` and fetched code

**The advice.** No `eval`, `bash -c` or `source` on outside text; no fetched script piped into
a shell.

**Why.** `eval` reads its arguments as shell code, so data holding `;` or `$(…)` runs as
commands. A piped script runs as it arrives, with nothing checked or read first.

**What it costs.** A `case` per action, and a checksum or signature to keep for each download.
A tool's documented installer is no exception: download it, check it and read it first.

### Arithmetic on input

**The advice.** A digits check before any arithmetic on input.

**Why.** Bash evaluates a variable's value as an expression (fact `sh-arith-eval`), so a value
holding an array subscript runs the command inside it. This is easy to miss, because the line
looks like a comparison, and it gives whoever controls the input a shell.

**What it costs.** One test per value. A script whose numbers come only from its own code
needs none.

### Secrets

**The advice.** Secrets in files or the environment, never in arguments.

**Why.** A process's command line is readable while it runs, and curl's own manual says to keep
credentials off it (fact `sh-cmdline`).

**What it costs.** A file to create and protect, or a tool that reads its secret from the
environment. Where a tool takes a secret only as an argument, run it where no other user can
list processes, or choose another tool.

### Validating input

**The advice.** Match input against what you accept.

**Why.** A pattern of what's allowed fails closed; a list of what's forbidden misses whatever
its author didn't think of.

**What it costs.** A pattern per input, and rejecting some odd but valid values.

## Facts

Versions, dates and defaults, each named elsewhere by its ID; bash-coding names several of these
too. Checked 2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `sh-arith-eval` | Bash evaluates a variable's value as an arithmetic expression when an expression refers to it | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "The value of a variable is evaluated as an arithmetic expression when it is referenced" | 2026-10-26 | 2027-10-26 |
| `sh-arith-octal` | In arithmetic, a leading 0 means octal | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "Constants with a leading 0 are interpreted as octal numbers." | 2026-10-26 | 2027-10-26 |
| `sh-expansion` | Unquoted expansions are split; `[[ … ]]` doesn't split or glob; a glob with no match stays as written | [Bash manual](https://tiswww.case.edu/php/chet/bash/bashref.html) | "did not occur within double quotes for word splitting" and "The words between the [[ and ]] do not undergo word splitting and filename expansion." and "the word is left unchanged" | 2026-10-26 | 2027-10-26 |
| `sh-sc2115` | `${var:?}` fails when the variable is empty or unset | [ShellCheck wiki, SC2115](https://www.shellcheck.net/wiki/SC2115) | "Using :? will cause the command to fail if the variable is null or unset." | 2026-10-26 | 2027-10-26 |
| `sh-cmdline` | A process's command line can be read from `/proc`, and curl says to keep credentials off it | [proc_pid_cmdline(5)](https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html), [curl manual](https://curl.se/docs/manpage.html) | "This read-only file holds the complete command line for the process" and "should be retrieved from a file instead or similar and never used in clear text in a command line" | 2026-10-26 | 2027-10-26 |
| `sh-curl-header-file` | curl reads headers from a file with `-H @file` | [curl manual](https://curl.se/docs/manpage.html) | "This option can take an argument in @filename style, which then adds a header for each line in the input file." | 2026-10-26 | 2027-10-26 |
| `sh-mktemp` | GNU `mktemp` creates files readable and writable only by their owner | [mktemp(1)](https://man7.org/linux/man-pages/man1/mktemp.1.html) | "Files are created u+rw, and directories u+rwx, minus umask restrictions." | 2026-10-26 | 2027-10-26 |
| `sh-exit-trap` | POSIX lets a shell skip the `EXIT` trap when a signal ends it | [POSIX.1-2024, Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html) | "may occur when the shell terminates abnormally as a result of delivery of a signal" | 2026-10-26 | 2027-10-26 |
| `sh-echo` | `echo` isn't portable with escapes or a leading option | [POSIX.1-2024 echo](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/echo.html) | "It is not possible to use echo portably across all POSIX systems unless escape sequences are omitted" | 2026-10-26 | 2027-10-26 |

## Sources

Every rule here is in this module's own words. Sources are quoted briefly, each quote a dated
fact above.

| Source | Used for | License |
|---|---|---|
| [Bash Reference Manual](https://tiswww.case.edu/php/chet/bash/bashref.html), the maintainer's copy | Arithmetic evaluation, expansions | GFDL 1.3: facts in our own words, short quotes |
| [ShellCheck wiki](https://www.shellcheck.net/wiki/SC2115) | SC2115 | The wiki states no license: facts in our own words, short quotes |
| [man7.org](https://man7.org/linux/man-pages/) (proc_pid_cmdline(5), mktemp(1)) | Command-line visibility, `mktemp` | Each page's own license: short quotes |
| [curl manual](https://curl.se/docs/manpage.html) | Headers from a file, credentials off the command line | curl license, MIT style: short quotes |
| [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/) | `EXIT` traps, `echo` | Copyright IEEE and The Open Group, all rights reserved: short quotes |
