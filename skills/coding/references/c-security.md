# C security

Read this for C handling outside data: buffers, formats, numbers, file names, commands,
temporary files, the environment, output, secrets, HTTP and memory-safety roadmaps.

The language is c-coding's; flags, sanitizers and fuzzing, c-build's; secret storage and
`SECURITY.md`, the project-bootstrap-and-audit standard's dimension 7.

## Rules

1. **Bound every write into a buffer, and check for truncation.** No `gets`, `strcpy`,
   `strcat`, `sprintf` or `scanf("%s")` on outside data.
2. **A format string is always a literal:** `printf("%s", s)`, never `printf(s)`.
3. **Parse numbers with `strtol`, and check counts from outside:** against the array they
   index, and for overflow before they size an allocation.
4. **A name from outside is one allowlisted component,** or, built by the program, mapped as
   below; opened with `openat`, `O_NOFOLLOW`, and `O_CREAT | O_EXCL` to create. `fstat` after,
   never `stat` before.
5. **Run programs with `posix_spawn` or `execve` and an argument array,** never `system` or
   `popen` with outside data.
6. **Make temporary files with `mkstemp` or `tmpfile`,** never `tmpnam` or `mktemp`.
7. **In a privileged program, distrust the environment:** `secure_getenv`, absolute paths, and
   `<ctype.h>` given an `unsigned char`.
8. **Escape outside text for where it lands:** a log, a terminal, or a parsed file.
9. **Keep secrets out of `argv` and logs, and fetch over HTTPS,** with verification on.

### Strings and buffers

- **`snprintf` returns the length it wanted** (fact `csec-strlcpy`): `n < 0 || (size_t)n >=
  size` means it was cut short.
- **`strncpy` makes a padded field, not a string** (fact `csec-strings`): unterminated when full.
- **`strlcpy` is in glibc 2.38 and POSIX.1-2024** (fact `csec-strlcpy`); older systems need a
  build check (c-build). Compare its return, `strlen(src)`, with the size.
- **C11 removed `gets`** (fact `csec-strings`); **Annex K's `_s` functions are optional** (fact
  `csec-annex-k`).

### Numbers, sizes and counts from outside

- **Parse with `strtol` or `strtoul` and `&end`, never `atoi`, `sscanf("%d")` or a null
  `end`,** which miss errors (fact `csec-numbers`). Set `errno = 0`, then require digits, the
  terminator at `end`, no `ERANGE`, and a range check. `strtoul` takes `-1` as a huge value.
- **Check a count against the array it indexes,** and run C23's `ckd_mul(&total, n, size)`
  before `malloc(total)` (fact `csec-ckd`). In C17, `__builtin_mul_overflow` (fact
  `csec-overflow-builtins`), or refuse `size != 0 && n > SIZE_MAX / size`, both `size_t`.

### Paths from outside data

Reject, don't repair, a name a caller supplies: the allowlist refuses `/`, `..`, an empty name,
a leading `-`, spaces and control bytes. A name built from a template and outside values can't
be refused: map each value's `/` and control bytes before filling, then each empty, `.` or `..`
component. `O_NOFOLLOW` checks only the last component (fact `csec-nofollow`), hence one; for
more, Linux 5.6's `openat2` with `RESOLVE_BENEATH` (fact `csec-openat2`).

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
- **`secure_getenv` returns `NULL` in a set-user-ID program,** whose `PATH` and environment
  are the caller's (fact `csec-system`): spawn by absolute path, with a fixed environment.
- **`isalpha` takes an `unsigned char` value or `EOF`,** and locales add letters (fact
  `csec-ctype`): check bytes against a list, as `create_output` does.

```c
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <spawn.h>
#include <sys/wait.h>

/* 0 and the wait status, or an error number; the name is never shell text. */
int compress(const char *path, int *status)
{
    char *argv[] = {"gzip", "--", (char *)path, NULL};
    char *envp[] = {"PATH=/usr/bin:/bin", NULL};
    pid_t pid;
    int rc = posix_spawn(&pid, "/usr/bin/gzip", NULL, NULL, argv, envp);
    if (rc != 0)
        return rc;
    while (waitpid(pid, status, 0) < 0)
        if (errno != EINTR)
            return errno;
    return 0;
}
```

Success also needs `WIFEXITED(*status)` and exit status 0; `posix_spawn` returns its error
without setting `errno` (fact `csec-system`).

### Output, secrets and the network

- **A line break in a field forges a line** in a log or a line-based file, and an escape byte
  drives a terminal (fact `csec-output`). Write bytes outside printable ASCII, and `\`, as
  `\xNN`.
- **Any user can read a command line** (fact `csec-cmdline`): take a secret from a file, a pipe
  or the environment, and never log `argv` whole.
- **libcurl allows every protocol it has** (fact `csec-curl`): set `CURLOPT_PROTOCOLS_STR` and
  `CURLOPT_REDIR_PROTOCOLS_STR` to `"https"`; leave `CURLOPT_SSL_VERIFYPEER` on. Cap a
  response with `CURLOPT_MAXFILESIZE_LARGE`, mid-transfer from curl 8.4.0 (fact
  `csec-curl-max`), or count bytes in the write callback. Check a host answers HTTPS first.
- **Wipe a secret with `explicit_bzero` or C23's `memset_explicit`,** not `memset`, which
  the compiler may remove (fact `csec-wipe`).

## Mistakes

- **`snprintf` or `strlcpy` with the return ignored:** a cut-short path names another file.
- **`printf(msg, n)` with `msg` from input:** `-Werror=format-security` misses it, as it has
  arguments; `-Wformat=2` catches it (tried: GCC 13, Clang 18).
- **Stripping `../` from a name,** which `....//` defeats.
- **`system()` on a command from `snprintf`,** which assistants call safe with quotes escaped.

## Audit

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Copies | `gets`, `strcpy`, `strcat`, `sprintf`, `scanf("%s"`; returns dropped | `BLOCKER` if reachable, else `GAP` | Bound and check (fact `csec-strlcpy`) |
| Formats | A non-literal format; no `-Wformat=2` | `BLOCKER` if reachable, else `GAP` | `"%s"` (fact `csec-format`) |
| Numbers, sizes | `atoi`, `sscanf("%d")`, `strtol` with `end` unchecked; an unchecked index or size from input | `BLOCKER` where input reaches it and it indexes or sizes memory, else `GAP` | A bound; `ckd_mul` (fact `csec-ckd`) |
| Paths | Input joined into a path; a made component left empty, `.` or `..`; no `O_NOFOLLOW`; `stat` before `open` | `BLOCKER` if reachable, else `GAP` | Allowlist, `openat` (fact `csec-nofollow`) |
| Commands | `system`, `popen`; `execvp` in privileged code | `BLOCKER` if reachable, else `GAP` | `posix_spawn` (fact `csec-system`) |
| Temporary files | `tmpnam`, `mktemp`, a fixed `/tmp` name | `BLOCKER` if privileged, else `GAP` | `mkstemp` (fact `csec-mktemp`) |
| Output | Raw outside text in a log, terminal or parsed file | `GAP` | Escape it (fact `csec-output`) |
| Secrets, transport | A secret in `argv`, a log or unwiped; `http://`; verification off; no size cap | `BLOCKER` if reachable, else `GAP`; `GAP` for no size cap, and for `http://` to a host with no HTTPS | Facts `csec-cmdline`, `csec-wipe`, `csec-curl` |
| Roadmap | Shipped C parsing input, with no memory-safety plan | `GAP` | Publish one (fact `csec-cisa`) |

## Why

**1 and 3. Bounds and counts.** Out-of-bounds writes are fifth in the 2025 CWE Top 25 (fact
`csec-top25`); an entry check misses a later write. Others: Annex K, proposed for removal (fact
`csec-annex-k`). Cost: a size with every buffer.

**2. Literal formats.** An outside format reads and writes memory through `%s` and `%n`.
Cost: none. A wrapper taking a format needs `__attribute__((format(printf, …)))`.

**4. One component, in a directory.** Path traversal is sixth (fact `csec-top25`). A reject is
easier to prove than a cleanup. Cost: other names fail. Otherwise: `openat2`.

**5 and 6. No shell, no guessable names.** A shell runs input as code, which CISA and the FBI
ask makers to prevent (fact `csec-cisa`); a guessed name is taken first. Cost: pipes and globs
in C. Otherwise: `system` on a constant.

**8 and 9. Output and secrets.** A forged line hides an attack; plain HTTP lets the network
change what's fetched. Cost: an escape step, a secret file.

**The roadmap.** CISA and the FBI's non-binding guidance asked for one by the end of 2025 (fact
`csec-cisa`): name the code parsing input, what guards it (c-build), and whether it could move
to a memory-safe language, dated.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `csec-strings` | `strncpy`; `gets` | [strncpy(3)](https://man7.org/linux/man-pages/man3/strncpy.3.html), [gets(3)](https://man7.org/linux/man-pages/man3/gets.3.html) | "a null-padded character sequence, not a string" and "C11 removes the specification of gets()" | 2026-10-27 | 2027-10-27 |
| `csec-strlcpy` | `snprintf`'s return; `strlcpy` in glibc 2.38, POSIX.1-2024 | [snprintf](https://pubs.opengroup.org/onlinepubs/9799919799/functions/snprintf.html), [glibc 2.38](https://sourceware.org/pipermail/libc-alpha/2023-July/150524.html), [strlcpy](https://pubs.opengroup.org/onlinepubs/9799919799/functions/strlcpy.html) | "had n been sufficiently large" and "The strlcpy and strlcat functions have been added." and "First released in Issue 8." | 2026-10-27 | 2027-04-27 |
| `csec-annex-k` | Annex K: optional; removal proposed | [N1967](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1967.htm) | "new, optional functions" and "we propose that Annex K be either removed" | 2026-10-27 | 2027-10-27 |
| `csec-format` | `format-security` skips calls with arguments | [OpenSSF](https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html) | "2026-08-20" and "used without arguments as errors" and "(-Wformat-nonliteral)" | 2026-10-27 | 2027-04-27 |
| `csec-ckd` | `<stdckdint.h>`: GCC 14, Clang 18 | [GCC 14](https://gcc.gnu.org/gcc-14/changes.html), [Clang](https://clang.llvm.org/c_status.html) | "The <stdckdint.h> header" and "Towards Integer Safety N2683 Clang 18" | 2026-10-27 | 2027-04-27 |
| `csec-overflow-builtins` | Checked arithmetic | [GCC](https://gcc.gnu.org/onlinedocs/gcc/Integer-Overflow-Builtins.html), [Clang](https://clang.llvm.org/docs/LanguageExtensions.html) | "checking whether the operations overflowed" and "Clang provides the following checked arithmetic builtins" | 2026-10-27 | 2027-10-27 |
| `csec-curl-max` | libcurl's size cap | [MAXFILESIZE_LARGE](https://curl.se/libcurl/c/CURLOPT_MAXFILESIZE_LARGE.html) | "If the transfer instead exceeds the limit while it is in progress, libcurl aborts it at that point." and "Before curl 8.4.0, the limit was not applied to transfers in progress." | 2026-10-27 | 2027-04-27 |
| `csec-nofollow` | `O_NOFOLLOW`: last component only | [open(2)](https://man7.org/linux/man-pages/man2/open.2.html) | "earlier components of the pathname will still be followed" | 2026-10-27 | 2027-10-27 |
| `csec-openat2` | `openat2`: Linux 5.6, no glibc wrapper | [openat2(2)](https://man7.org/linux/man-pages/man2/openat2.2.html) | "Linux 5.6." and "glibc provides no wrapper for openat2()" | 2026-10-27 | 2027-04-27 |
| `csec-system` | `system`, `popen`; `secure_getenv`; `posix_spawn` | [system](https://pubs.opengroup.org/onlinepubs/9799919799/functions/system.html), [posix_spawn](https://pubs.opengroup.org/onlinepubs/9799919799/functions/posix_spawn.html), [popen](https://pubs.opengroup.org/onlinepubs/9799919799/functions/popen.html), [system(3)](https://man7.org/linux/man-pages/man3/system.3.html), [getenv(3)](https://man7.org/linux/man-pages/man3/getenv.3.html) | "invoked the sh utility using" and "PATH could be manipulated" and "returns NULL in cases where" and "an error number shall be returned" | 2026-10-27 | 2027-10-27 |
| `csec-cisa` | CISA and the FBI: roadmaps; commands | [CISA](https://www.cisa.gov/resources-tools/resources/product-security-bad-practices) | "roadmap by the end of 2025" and "non-binding" and "command inputs are clearly delineated" | 2026-10-27 | 2027-04-27 |
| `csec-mktemp` | `mktemp`, `tmpnam`; `mkstemp`'s mode | [mktemp(3)](https://man7.org/linux/man-pages/man3/mktemp.3.html), [tmpnam(3)](https://man7.org/linux/man-pages/man3/tmpnam.3.html), [mkstemp(3)](https://man7.org/linux/man-pages/man3/mkstemp.3.html) | "Never use mktemp()." and "avoid using these functions" and "permissions 0600" | 2026-10-27 | 2027-10-27 |
| `csec-ctype` | `<ctype.h>`'s argument; locales | [isalpha(3)](https://man7.org/linux/man-pages/man3/isalpha.3.html) | "otherwise, the behavior is undefined" and "additional characters for which isalpha() is true" | 2026-10-27 | 2027-10-27 |
| `csec-output` | Forged log lines; control sequences | [CWE-117](https://cwe.mitre.org/data/definitions/117.html), [CWE-150](https://cwe.mitre.org/data/definitions/150.html) | "insert false entries into the log file" and "escape, meta, or control character sequences" | 2026-10-27 | 2027-10-27 |
| `csec-numbers` | `atoi`, `sscanf`; `strtol`'s `errno`; `strtoul` | [atoi(3)](https://man7.org/linux/man-pages/man3/atoi.3.html), [sscanf(3)](https://man7.org/linux/man-pages/man3/sscanf.3.html), [strtol(3)](https://man7.org/linux/man-pages/man3/strtol.3.html), [strtoul(3)](https://man7.org/linux/man-pages/man3/strtoul.3.html) | "atoi() does not detect errors" and "undefined behavior for invalid input" and "should set errno to 0 before the call" and "negation of the result" | 2026-10-27 | 2027-10-27 |
| `csec-wipe` | Wiping: `explicit_bzero`, `memset_explicit` | [memset(3)](https://man7.org/linux/man-pages/man3/memset.3.html), [explicit_bzero(3)](https://man7.org/linux/man-pages/man3/explicit_bzero.3.html), [memset_explicit(3)](https://man7.org/linux/man-pages/man3/memset_explicit.3.html) | "may totally or partially remove the call" and "glibc 2.25." and "C23." | 2026-10-27 | 2027-10-27 |
| `csec-cmdline` | `/proc/<pid>` is readable by all | [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html) | "Everybody may access all /proc/pid directories." | 2026-10-27 | 2027-10-27 |
| `csec-curl` | libcurl's protocols; 7.85.0 | [PROTOCOLS_STR](https://curl.se/libcurl/c/CURLOPT_PROTOCOLS_STR.html) | "accepts all protocols it was built with support for" and "Added in curl 7.85.0" | 2026-10-27 | 2027-04-27 |
| `csec-top25` | 2025 CWE Top 25 | [Top 25](https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html) | "5 CWE-787" and "6 CWE-22" and "9 CWE-78" | 2026-10-27 | 2027-04-27 |

## Sources

Rules and examples are this module's own; sources are quoted briefly.

| Source | Used for | License |
|---|---|---|
| [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/) | C library and processes | The Open Group, all rights reserved |
| [Linux man-pages](https://man7.org/linux/man-pages/) | Libraries and system calls | Linux-man-pages-copyleft |
| [WG14 N1967](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1967.htm) | Annex K | WG14 document |
| [GCC](https://gcc.gnu.org/), [Clang](https://clang.llvm.org/) | Overflow checks | GFDL; Apache-2.0 |
| [OpenSSF guide](https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html) | Format warnings | CC BY 4.0, attributed |
| [CISA](https://www.cisa.gov/resources-tools/resources/product-security-bad-practices) | Roadmaps, commands | US government work |
| [CWE](https://cwe.mitre.org/) | Top 25, CWE-117 | CWE Terms of Use |
| [libcurl](https://curl.se/libcurl/c/) | Protocols, verification | curl license |
