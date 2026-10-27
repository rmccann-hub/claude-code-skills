# C security

Read this for C handling outside data: buffers and strings, format strings, sizes and counts,
file names, running programs, temporary files, the environment, escaping output, secrets in
`argv`, plain HTTP, and memory-safety roadmaps.

The language, undefined behavior, ownership and error checks are c-coding's; flags, sanitizers,
analyzers and fuzzing are c-build's. Secret storage and `SECURITY.md` are the
project-bootstrap-and-audit standard's, in its dimension 7.

## Rules

1. **Bound every write into a buffer, and check for truncation.** No `gets`, `strcpy`,
   `strcat`, `sprintf` or `scanf("%s")` on outside data.
2. **A format string is always a literal:** `printf("%s", s)`, never `printf(s)`.
3. **Check a size or count from outside before use:** against the array it indexes, and with
   `ckd_*` before it sizes an allocation.
4. **A name from outside is one allowlisted component,** opened with `openat`, `O_NOFOLLOW`,
   and `O_CREAT | O_EXCL` to create. `fstat` after, never `stat` before.
5. **Run programs with `posix_spawn` or `execve` and an argument array,** never `system` or
   `popen` with outside data.
6. **Make temporary files with `mkstemp` or `tmpfile`,** never `tmpnam` or `mktemp`.
7. **In a privileged program, distrust the environment:** `secure_getenv`, absolute paths, and
   `<ctype.h>` given an `unsigned char`.
8. **Escape outside text for where it lands:** a log, a terminal, or a parsed file.
9. **Keep secrets out of `argv` and logs, and fetch over HTTPS,** with verification on.

### Strings and buffers

- **`snprintf` returns the length it wanted** (fact `csec-snprintf`): `n < 0 || (size_t)n >=
  size` means it was cut short.
- **`strncpy` makes a padded field, not a string** (fact `csec-strings`): a source that fills
  the buffer leaves no terminator.
- **`strlcpy` is in glibc 2.38 and POSIX.1-2024** (fact `csec-strlcpy`); older systems need a
  build check (c-build). It returns `strlen(src)`: compare that with the size.
- **C11 removed `gets`** (fact `csec-strings`); **Annex K's `_s` functions are optional,** and
  rarely shipped (fact `csec-annex-k`).

### Sizes and counts from outside

A count from a device or a file indexes a fixed array only after a check against its size, and
`malloc(n * size)` waits for `ckd_mul(&total, n, size)`. C23's `ckd_*` are in GCC 14 and
Clang 18; before C23, `__builtin_mul_overflow` and kin (fact `csec-ckd`).

```c std=c23
#include <stdckdint.h>
#include <stddef.h>
#include <stdint.h>

enum { MAX_CHANNELS = 16 };

/* count and bytes come from a device: neither is trusted. */
int read_levels(uint16_t level[MAX_CHANNELS], const uint8_t *bytes, size_t len, size_t count)
{
    size_t need;
    if (count > MAX_CHANNELS || ckd_mul(&need, count, (size_t)2) || need > len)
        return -1;
    for (size_t i = 0; i < count; i++)
        level[i] = (uint16_t)(bytes[2 * i] | bytes[2 * i + 1] << 8);
    return 0;
}
```

### Paths from outside data

Reject, don't repair: the allowlist refuses `/`, `.`, `..`, an empty name, a leading `-`,
spaces and control bytes. `O_NOFOLLOW` checks only the last component (fact `csec-nofollow`),
hence one; for more, Linux 5.6's `openat2` with `RESOLVE_BENEATH` (fact `csec-openat2`).

```c
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <string.h>

/* Fails if the name exists, even as a link. */
int create_output(int dirfd, const char *name)
{
    static const char ok[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-";
    size_t len = strlen(name);
    if (len == 0 || len > 255 || name[0] == '.' || name[0] == '-' || strspn(name, ok) != len) {
        errno = EINVAL;
        return -1;
    }
    return openat(dirfd, name, O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW | O_CLOEXEC, 0644);
}
```

### Programs, temporary files and the environment

- **`system` and `popen` run `sh -c`** (fact `csec-system`): input becomes shell syntax.
- **`mkstemp` creates with `O_EXCL`, mode 0600** (fact `csec-mktemp`).
- **`secure_getenv` returns `NULL` in a set-user-ID program,** whose `PATH` is the caller's
  (fact `csec-system`): spawn by absolute path.
- **`isalpha` and kin take an `unsigned char` value or `EOF`,** and other locales admit more
  letters (fact `csec-ctype`): check bytes by range, as `create_output` does.

```c
#define _POSIX_C_SOURCE 200809L
#include <spawn.h>
#include <sys/types.h>
#include <sys/wait.h>

extern char **environ;

/* The name is an argument, never shell text. */
int compress(const char *path)
{
    char *argv[] = {"gzip", "--", (char *)path, NULL};
    pid_t pid;
    int status;
    if (posix_spawn(&pid, "/usr/bin/gzip", NULL, NULL, argv, environ) != 0 ||
        waitpid(pid, &status, 0) < 0)
        return -1;
    return WIFEXITED(status) ? WEXITSTATUS(status) : -1;
}
```

### Output, secrets and the network

- **A line break in a field forges a line** in a log or a line-based file, and an escape byte
  drives a terminal (fact `csec-output`). Write each byte outside printable ASCII, and `\`
  itself, as `\xNN`, or quote by the format's own rule.
- **Any user can read a command line** (fact `csec-cmdline`): take a secret from a file, a pipe
  or the environment, and never log `argv` whole.
- **libcurl allows every protocol it was built with** (fact `csec-curl`): set
  `CURLOPT_PROTOCOLS_STR` and `CURLOPT_REDIR_PROTOCOLS_STR` to `"https"`, and leave
  `CURLOPT_SSL_VERIFYPEER` on.

## Mistakes

- **`snprintf` or `strlcpy` with the return ignored:** a cut-short path names another file.
- **`printf(msg, n)` with `msg` from input:** `-Werror=format-security` misses it, as it has
  arguments; `-Wformat=2` catches it (tried: GCC 13, Clang 18).
- **`malloc(count * size)` with `count` from a header,** which wraps to a small buffer.
- **Stripping `../` from a name,** which `....//` defeats.
- **`system()` on a command from `snprintf`,** which assistants call safe with quotes escaped.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Copies | `gets`, `strcpy`, `strcat`, `sprintf`, `scanf("%s"`; `snprintf` returns dropped | `BLOCKER` if reachable, else `GAP` | Bound and check (fact `csec-snprintf`) |
| Formats | A non-literal format; no `-Wformat=2` | `BLOCKER` if reachable, else `GAP` | `"%s"` (fact `csec-format`) |
| Counts and sizes | An index or allocation size from input, unchecked | `BLOCKER` if reachable | A bound; `ckd_mul` (fact `csec-ckd`) |
| Paths | Input joined into a path; no `O_NOFOLLOW`; `stat` before `open` | `BLOCKER` if reachable, else `GAP` | Allowlist, `openat` (fact `csec-nofollow`) |
| Commands | `system`, `popen`; `execvp` in privileged code | `BLOCKER` if reachable, else `GAP` | `posix_spawn` (fact `csec-system`) |
| Temporary files | `tmpnam`, `mktemp`, a fixed `/tmp` name | `GAP` | `mkstemp` (fact `csec-mktemp`) |
| Output | Outside text raw in a log, a terminal or a parsed file | `GAP` | Escape it (fact `csec-output`) |
| Secrets, transport | A secret in `argv` or a log; `http://`; verification off | `BLOCKER` | Facts `csec-cmdline`, `csec-curl` |
| Roadmap | Shipped C parsing input, with no memory-safety plan | `GAP` | Publish one (fact `csec-cisa`) |

## Why

**1 and 3. Bounds and counts.** Out-of-bounds writes are fifth in the 2025 CWE Top 25 (fact
`csec-top25`). An entry check misses a later write, so each write is checked. Others: Annex
K, which a 2015 WG14 paper proposed removing (fact `csec-annex-k`). Cost: a size passed with
every buffer.

**2. Literal formats.** An outside format reads and writes memory through `%s` and `%n`;
OpenSSF lists both warnings (fact `csec-format`). Cost: none. A wrapper taking a format needs
`__attribute__((format(printf, …)))` to check callers.

**4. One component, in a directory.** Path traversal is sixth (fact `csec-top25`). A reject is
easier to prove than a cleanup, and `O_EXCL` closes the check-then-use race. Cost: other
names fail; map them. Otherwise: `openat2` for several components.

**5 and 6. No shell, no guessable names.** A shell runs input as code, which CISA and the FBI
ask makers to prevent (fact `csec-cisa`); a guessed temporary name can be taken first. Cost:
pipes and globs written in C. Otherwise: `system` on a fixed string.

**8 and 9. Output and secrets.** A forged line hides an attack, a command line is public, and
plain HTTP lets the network change what's fetched. Cost: an escape step and a secret file.

**The roadmap.** CISA and the FBI's non-binding guidance asked for a memory-safety roadmap for
existing products by the end of 2025 (fact `csec-cisa`). This module's advice: name the
code parsing outside input, the flags, sanitizers and fuzzing guarding it (c-build), and
whether it could move to a memory-safe language; date it, and revisit it.

## Facts

Each named above by ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `csec-snprintf` | `snprintf` returns the length it would have written | [POSIX](https://pubs.opengroup.org/onlinepubs/9799919799/functions/snprintf.html) | "would be written to s had n been sufficiently large" | 2026-10-27 | 2027-10-27 |
| `csec-strings` | `strncpy` doesn't make a string; C11 removed `gets` | [strncpy(3)](https://man7.org/linux/man-pages/man3/strncpy.3.html), [gets(3)](https://man7.org/linux/man-pages/man3/gets.3.html) | "a null-padded character sequence, not a string" and "ISO C11 removes the specification of gets()" | 2026-10-27 | 2027-10-27 |
| `csec-strlcpy` | `strlcpy` is in glibc 2.38 and POSIX.1-2024 | [glibc 2.38](https://sourceware.org/pipermail/libc-alpha/2023-July/150524.html), [POSIX](https://pubs.opengroup.org/onlinepubs/9799919799/functions/strlcpy.html) | "The strlcpy and strlcat functions have been added." and "First released in Issue 8." | 2026-10-27 | 2027-04-27 |
| `csec-annex-k` | Annex K is optional; in 2015, unshipped in open source, and proposed for removal | [N1967](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1967.htm) | "new, optional functions" and "none of the popular Open Source distribution" and "we propose that Annex K be either removed" | 2026-10-27 | 2027-10-27 |
| `csec-format` | OpenSSF (2026-08-20): `-Werror=format-security` skips calls with arguments; `-Wformat=2` doesn't | [OpenSSF](https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html) | "2026-08-20" and "used without arguments as errors" and "(-Wformat-nonliteral)" | 2026-10-27 | 2027-04-27 |
| `csec-ckd` | `<stdckdint.h>`: GCC 14, Clang 18; the built-ins are always defined | [GCC 14](https://gcc.gnu.org/gcc-14/changes.html), [Clang](https://clang.llvm.org/c_status.html), [built-ins](https://gcc.gnu.org/onlinedocs/gcc/Integer-Overflow-Builtins.html) | "The <stdckdint.h> header" and "Towards Integer Safety N2683 Clang 18" and "fully defined behavior" | 2026-10-27 | 2027-04-27 |
| `csec-nofollow` | `O_NOFOLLOW` checks only the last component | [open(2)](https://man7.org/linux/man-pages/man2/open.2.html) | "Symbolic links in earlier components of the pathname will still be followed." | 2026-10-27 | 2027-10-27 |
| `csec-openat2` | `openat2` came in Linux 5.6, with no glibc wrapper | [openat2(2)](https://man7.org/linux/man-pages/man2/openat2.2.html) | "Linux 5.6." and "glibc provides no wrapper for openat2()" | 2026-10-27 | 2027-04-27 |
| `csec-system` | `system` and `popen` run `sh`, which uses `PATH`; `secure_getenv` returns `NULL` when privileged | [system](https://pubs.opengroup.org/onlinepubs/9799919799/functions/system.html), [popen](https://pubs.opengroup.org/onlinepubs/9799919799/functions/popen.html), [system(3)](https://man7.org/linux/man-pages/man3/system.3.html), [getenv(3)](https://man7.org/linux/man-pages/man3/getenv.3.html) | "invoked the sh utility using" and "PATH could be manipulated" and "returns NULL in cases where" | 2026-10-27 | 2027-10-27 |
| `csec-cisa` | CISA and the FBI: non-binding; roadmaps by the end of 2025; commands apart from input | [CISA](https://www.cisa.gov/resources-tools/resources/product-security-bad-practices) | "publish a memory safety roadmap by the end of 2025" and "non-binding" and "command inputs are clearly delineated" | 2026-10-27 | 2027-04-27 |
| `csec-mktemp` | Never `mktemp`, avoid `tmpnam`; `mkstemp` uses mode 0600 | [mktemp(3)](https://man7.org/linux/man-pages/man3/mktemp.3.html), [tmpnam(3)](https://man7.org/linux/man-pages/man3/tmpnam.3.html), [mkstemp(3)](https://man7.org/linux/man-pages/man3/mkstemp.3.html) | "Never use mktemp()." and "avoid using these functions" and "permissions 0600" | 2026-10-27 | 2027-10-27 |
| `csec-ctype` | `<ctype.h>` takes `unsigned char` or `EOF`; locales add letters | [isalpha(3)](https://man7.org/linux/man-pages/man3/isalpha.3.html) | "otherwise, the behavior is undefined" and "additional characters for which isalpha() is true" | 2026-10-27 | 2027-10-27 |
| `csec-output` | Unescaped input forges log lines and control sequences | [CWE-117](https://cwe.mitre.org/data/definitions/117.html), [CWE-150](https://cwe.mitre.org/data/definitions/150.html) | "insert false entries into the log file" and "escape, meta, or control character sequences" | 2026-10-27 | 2027-10-27 |
| `csec-cmdline` | `/proc/<pid>/cmdline` is readable by all by default | [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html) | "Everybody may access all /proc/pid directories." | 2026-10-27 | 2027-10-27 |
| `csec-curl` | libcurl allows all its protocols by default; the option came in 7.85.0 | [PROTOCOLS_STR](https://curl.se/libcurl/c/CURLOPT_PROTOCOLS_STR.html) | "accepts all protocols it was built with support for" and "Added in curl 7.85.0" | 2026-10-27 | 2027-04-27 |
| `csec-top25` | 2025 CWE Top 25: 787 is 5th, 22 6th, 78 9th; 190 is absent (read) | [Top 25](https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html) | "5 CWE-787" and "6 CWE-22" and "9 CWE-78" | 2026-10-27 | 2027-04-27 |

## Sources

Rules and examples are this module's own; sources are quoted briefly.

| Source | Used for | License |
|---|---|---|
| [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/) | `snprintf`, `strlcpy`, `system` | The Open Group, all rights reserved |
| [Linux man-pages](https://man7.org/linux/man-pages/) | Libraries and system calls | Linux-man-pages-copyleft |
| [WG14 N1967](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1967.htm) | Annex K | WG14 document |
| [GCC](https://gcc.gnu.org/onlinedocs/), [Clang](https://clang.llvm.org/c_status.html) | `ckd_*` | GFDL; Apache-2.0 |
| [OpenSSF guide](https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html) | Format warnings | CC BY 4.0, attributed |
| [CISA](https://www.cisa.gov/resources-tools/resources/product-security-bad-practices) | Roadmaps, commands | US government work |
| [CWE](https://cwe.mitre.org/) | Top 25, CWE-117 | CWE Terms of Use |
| [libcurl](https://curl.se/libcurl/c/) | Protocols, verification | curl license |
