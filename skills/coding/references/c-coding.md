# C coding

Read this for writing, reviewing or fixing C: the standard and how GCC, Clang and MSVC differ,
undefined behavior, ownership and copying a library's structs, bounds at every write, checking
every write and close, test exit codes, and moving old code to C17 or C23.

Meson, warnings, hardening, sanitizers, static analysis and fuzzing are c-build's. Outside data
is c-security's: strings, format strings, integer overflow and `ckd_*`, paths, running programs
and escaping output. Test design is the planned testing skill's. The standard's *Language
toolchains* names no C compiler, so take versions from the project's own pins.

## Rules

1. **Name the standard in the build; never take the compiler's default.** Target C17, and C23
   only where every supported compiler has each feature used.
2. **Write no undefined behavior.** The optimizer assumes there is none, and deletes the checks
   that would catch it.
3. **Give every allocation one owner; copy and free a library's objects with its functions.**
4. **Check the room left at every write into a buffer,** not once before the first.
5. **Check every call that can fail, `fclose` included, and report the first failure.**
6. **A test exits 0 to pass and 77 to skip;** one that can't run its probe skips.
7. **Move old code one standard at a time,** and let the compiler's errors list the work.

### Standards and compilers

- **The defaults differ and move:** GCC 15 and later use `gnu23`, Clang `gnu17`, and MSVC
  without `/std:c11` or `/std:c17` C89 with extensions (facts `c-gcc-default`,
  `c-clang-default`, `c-msvc-default`). c-build sets `c_std`.
- **A strict mode hides POSIX:** under `-std=c17`, glibc declares no `strdup` until
  `_POSIX_C_SOURCE` is defined before the first `#include`, and GCC 14 and Clang 18 fail the
  call (fact `c-gcc14-errors`).
- **MSVC has no variable-length arrays and plans none** (fact `c-msvc-default`).

### Undefined behavior that bites

- **Signed overflow:** GCC 13 and Clang 18 delete `if (x + 1 < x)` on an `int` at `-O2`. Compare
  with `INT_MAX` first, or use c-security's `ckd_add`.
- **A null test after a dereference** is deleted (fact `c-gcc-ub-opts`).
- **Reading an object through a pointer to another type,** other than a character type, breaks
  strict aliasing, assumed from `-O2`. Copy the bytes with `memcpy`.
- **Uninitialized reads, use after `free`, and pointers past one beyond an array's end.**
  c-build's sanitizers find them.

### Ownership

Copying a struct copies its pointers. `b = a` or `memcpy(&b, &a, sizeof a)` on a struct owning
heap memory makes two owners: freeing `a` leaves `b.label` dangling, a use after free, and
freeing `b` frees it again, a double free. Use the library's copy and free functions; GMP warns
against copying its objects at all (fact `c-gmp-copy`). Where there are none, lend a pointer, or
write a deep copy beside the type:

```c
#include <stdlib.h>
#include <string.h>

struct reading {
    char *label; /* owned: reading_free releases it */
    double value;
};

int reading_copy(struct reading *dst, const struct reading *src)
{
    size_t size = strlen(src->label) + 1;
    char *label = malloc(size);
    if (label == NULL)
        return -1;
    memcpy(label, src->label, size);
    *dst = (struct reading){.label = label, .value = src->value};
    return 0;
}

void reading_free(struct reading *r)
{
    free(r->label);
    r->label = NULL;
}
```

### Bounds at every write

Keep pointer, length and capacity together, and send every write through one function that
checks the room left, terminator included. `snprintf` and `strlcpy` are c-security's.

```c
#include <stddef.h>
#include <string.h>

struct buf {
    char *data;
    size_t len; /* bytes in use, before the terminator; always below cap */
    size_t cap; /* bytes allocated */
};

static int buf_append(struct buf *b, const char *s, size_t n)
{
    if (n >= b->cap - b->len) /* no room for n bytes and the terminator */
        return -1;
    memcpy(b->data + b->len, s, n);
    b->len += n;
    b->data[b->len] = '\0';
    return 0;
}

int format_pair(struct buf *b, const char *key, const char *value)
{
    if (buf_append(b, key, strlen(key)) != 0 || buf_append(b, "=", 1) != 0 ||
        buf_append(b, value, strlen(value)) != 0 || buf_append(b, "\n", 1) != 0)
        return -1;
    return 0;
}
```

### Errors and files

- **A `FILE` buffers,** so `fwrite` and `fprintf` succeed on a full disk and the error comes at
  `fflush` or `fclose` (fact `c-close-errors`). Check `fwrite`'s count, every `fflush` and
  `fclose`; after unchecked `fprintf` or `putc` calls, test `ferror` before `fclose`.
- **`fclose` closes the stream even when it fails** (fact `c-posix-stdio`): never call it again.
- **Keep the first error.** Save `errno` at once, since the next call may change it (fact
  `c-posix-stdio`), and never let a cleanup call's status replace it.
- **Check `stdout` before exiting** where output is the product: `fflush(stdout) == EOF ||
  ferror(stdout)`. Unchecked, `prog > /dev/full` exits 0.

```c
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>

/* Returns 0, or the errno of the first call that failed. */
int write_file(const char *path, const void *data, size_t size)
{
    FILE *f = fopen(path, "wb");
    if (f == NULL)
        return errno;
    int err = 0;
    if (fwrite(data, 1, size, f) != size)
        err = errno;
    if (fclose(f) == EOF && err == 0) /* a full disk may show only here */
        err = errno;
    return err;
}
```

### Tests

`meson test` passes 0, skips 77 and calls 99 an error (fact `c-meson-exit-codes`). A test that
can't run its probe prints why and returns 77, never 0. On Linux, writing to `/dev/full` fails
with `ENOSPC`, which `write_file` returns and a version checking only `fwrite` misses: test it,
skipping where `/dev/full` isn't writable.

### Moving old code forward

Name the target standard, build, and fix what fails in this order:

1. **C99's removals:** implicit `int` and calls to undeclared functions are errors from GCC 14
   (fact `c-gcc14-errors`). Add the type; include the header.
2. **`f()`:** C23 reads it as `f(void)`, so a call with arguments fails (fact `c-gcc15-c23`).
3. **K&R definitions,** `int f(a) int a; {…}`: removed in C23 (fact `c-clang-knr`). Clang 18
   rejects them; GCC 13 warns. Rewrite as prototypes.
4. **New keywords:** `bool`, `true`, `false`, `nullptr`, `thread_local` and others (fact
   `c-gcc15-c23`), so `typedef int bool;` fails. Use `<stdbool.h>`, but `bool` isn't `int` in
   the ABI: check structs written to files or shared with other libraries.

## Mistakes

- **Relying on the default standard:** what GCC 15 builds fails on Clang or MSVC. AI
  assistants write `nullptr`, `bool` with no header, or `[[nodiscard]]` in a C17 project.
- **`memcpy` or `=` on a struct that owns memory, then freeing both copies.**
- **One length check before several writes,** or one that forgets the terminator.
- **`sizeof buf` on a parameter declared `char buf[64]`:** the pointer's size. Pass the length.
- **`fclose(f);` unchecked,** `rc = fclose(f)` replacing a write's failure, or `perror` after
  a cleanup call, reporting the cleanup's `errno`.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Standard | No `-std` or `c_std`; C23 features in a C17 project | `GAP`; `DRIFT` for the mismatch | Name C17 |
| Shallow copies | `=` or `memcpy` of a struct with owned pointers | `BLOCKER` where both copies are freed, else `GAP` | The library's copy |
| Bounds | A buffer write with no check of the room left at that write | `BLOCKER` where outside data sets the length, else `GAP` | One checked append function |
| Unchecked writes | `fwrite`, `fflush`, `fclose` or the product's `stdout` unchecked | `BLOCKER` where the output is the product, else `GAP` | Check each; test with `/dev/full` |
| First error lost | A later status or `errno` replacing an earlier failure | `GAP` | Save it at once |
| Undefined behavior | `x + 1 < x`; a null test after a dereference; casts between pointer types | `BLOCKER` where outside data reaches it, else `GAP` | Test before the operation; `memcpy` |
| Unprobed tests | Exit 0 when the test couldn't run | `BLOCKER` | Exit 77 |
| Old C | K&R definitions; `()` called with arguments; `bool` typedefs | `DRIFT` | Prototypes; `<stdbool.h>` |

## Why

**1. The standard.** A project naming none changed language when GCC 15 moved to `gnu23` (fact
`c-gcc15-c23`). C17 is the newest standard all three accept by name (fact `c-msvc-default`); the
Linux kernel names `gnu11` (fact `c-kernel-flags`). Cost: no `nullptr` or `ckd_*`. Otherwise:
C23 where each compiler's status page lists every feature used.

**2. Undefined behavior.** A check that can only fire after undefined behavior is deleted, so the
bug ships unguarded (fact `c-gcc-ub-opts`). The kernel turns three such assumptions off (fact
`c-kernel-flags`). Cost: a test before the operation. Otherwise: for code too large to audit,
the kernel's flags, which c-build weighs.

**3. Ownership.** An audit found a library's struct copied with `memcpy`, then both copies
freed: a use after free, then a double free. GMP discourages any copy (fact `c-gmp-copy`). Cost:
a copy function per type. Otherwise: an arena, which frees everything at once.

**4. Bounds at every write.** One check before the first write covers that write; writes added
later run unchecked. GLib's `GString` grows instead of failing. Cost: a call per write.
Otherwise: grow the buffer when the format sets no limit.

**5. Every call, and the first failure.** Buffering moves a full disk's error to `fclose`, so a
program checking only `fwrite` reports success for data it lost. GNU says to check every system
call (fact `c-gnu-check-calls`). The first failure is the cause; later ones are its echoes.
Cost: lines, and an error path to test. Otherwise: a write whose loss doesn't matter, such as a
last message to `stderr`, said in a comment.

**6. Test exit codes.** A test that exits 0 unprobed is a pass that measured nothing. Meson
reads 77, or `1..0 # SKIP` from a TAP test, as a skip (fact `c-meson-exit-codes`). Cost: none.

**7. One standard at a time.** GCC 14 made errors of old warnings (fact `c-gcc14-errors`), and
C23 changes meanings; small steps keep diffs reviewable. Cost: a CI job per standard while
moving. Otherwise: pin `gnu17` for code no one will change.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `c-gcc-default` | GCC's default C mode | [GCC](https://gcc.gnu.org/onlinedocs/gcc/Standards.html) | "The default, if no C language dialect options are given, is -std=gnu23." | 2026-10-27 | 2027-04-27 |
| `c-clang-default` | Clang's default C mode | [Clang](https://clang.llvm.org/docs/UsersManual.html) | "If no -std option is specified, clang defaults to gnu17 mode." | 2026-10-27 | 2027-04-27 |
| `c-msvc-default` | MSVC's C modes; no VLAs | [/std](https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version?view=msvc-170) | "implements ANSI C89, but includes several Microsoft extensions" and "/std:c17 Enables ISO C17 conformance" and "Variable length array (VLA) support isn't planned." | 2026-10-27 | 2027-04-27 |
| `c-gcc15-c23` | GCC 15 moved to C23: `()` and keywords | [GCC 15](https://gcc.gnu.org/gcc-15/porting_to.html) | "from -std=gnu17 to -std=gnu23" and "In C23 such declarations mean (void)" and "including bool, true, false, nullptr, and thread_local" and "the bool type is not the same as int at ABI level" | 2026-10-27 | 2027-10-27 |
| `c-gcc14-errors` | GCC 14's errors; strict modes hide extensions | [GCC 14](https://gcc.gnu.org/gcc-14/porting_to.html) | "In GCC 14, these issues are now reported as errors" and "The GNU C library automatically suppresses these extensions in standard C mode" | 2026-10-27 | 2027-10-27 |
| `c-clang-knr` | C23 drops K&R definitions; Clang 15 | [Clang](https://clang.llvm.org/c_status.html) | "Remove support for function definitions with identifier lists N2432 Clang 15" | 2026-10-27 | 2027-10-27 |
| `c-gcc-ub-opts` | Null tests after use; strict aliasing | [GCC](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) | "if a pointer is checked after it has already been dereferenced, it cannot be null" and "The -fstrict-aliasing option is enabled at levels -O2, -O3, -Os." | 2026-10-27 | 2027-10-27 |
| `c-kernel-flags` | Linux's standard and flags | [Makefile](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Makefile) | "-std=gnu11" and "-fno-strict-aliasing" and "-fno-delete-null-pointer-checks" and "-fno-strict-overflow" | 2026-10-27 | 2027-04-27 |
| `c-gmp-copy` | GMP: don't copy its objects | [GMP](https://gmplib.org/manual/Variable-Conventions) | "it is discouraged to make copies of the GMP object itself" | 2026-10-27 | 2027-10-27 |
| `c-close-errors` | Errors surface at close | [close(2)](https://man7.org/linux/man-pages/man2/close.2.html) | "errors on a previous write(2) operation are reported only on the final close()" | 2026-10-27 | 2027-10-27 |
| `c-posix-stdio` | `fclose` and `errno` | [fclose](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fclose.html), [errno](https://pubs.opengroup.org/onlinepubs/9799919799/functions/errno.html) | "Whether or not the call succeeds, the stream shall be disassociated from the file" and "until it is changed by the next function call" | 2026-10-27 | 2027-10-27 |
| `c-gnu-check-calls` | GNU: check every system call | [GNU](https://www.gnu.org/prep/standards/html_node/Semantics.html) | "Check every system call for an error return" | 2026-10-27 | 2027-10-27 |
| `c-meson-exit-codes` | `meson test`: 77 skips, 99 errors | [Meson](https://mesonbuild.com/Unit-tests.html) | "error code 77" and "1..0 # SKIP" and "error code 99" | 2026-10-27 | 2027-04-27 |

## Sources

The rules and examples are this module's own words and code.

| Source | Used for | License |
|---|---|---|
| [GCC](https://gcc.gnu.org/onlinedocs/gcc/), [GNU](https://www.gnu.org/prep/standards/), [GMP](https://gmplib.org/manual/) | Defaults, C23, checks, copies | GFDL 1.3; GCC's release notes, verbatim only: short quotes |
| [Clang](https://clang.llvm.org/docs/) | Defaults, K&R | Apache-2.0 with LLVM exception: short quotes |
| [Microsoft Learn](https://learn.microsoft.com/en-us/cpp/) | MSVC | CC BY 4.0: short quotes, attributed |
| [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/), [man7.org](https://man7.org/linux/man-pages/man2/close.2.html) | `fclose`, `errno`, `close` | All rights reserved; the page's own: short quotes |
| [Meson](https://mesonbuild.com/Unit-tests.html) | Test exit codes | CC BY-SA 4.0: short quotes, attributed |
| [Linux](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Makefile), [GLib](https://docs.gtk.org/glib/struct.String.html) | What others do | GPL-2.0, LGPL-2.1-or-later: pointed to |
