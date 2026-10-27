# C coding

Read this for writing, reviewing or fixing C: the standard and compilers, undefined behavior,
ownership and copying a library's structs, bounds at every write, checking every write and
close, test exit codes, and moving old code to C17 or C23.

Meson, warnings, hardening, sanitizers, static analysis and fuzzing are c-build's. Outside data
is c-security's: strings, format strings, integer overflow, paths, temporary files, running
programs and escaping output. Test design is the planned testing skill's. The standard's
*Language toolchains* names no C compiler, so take versions from the project's own pins.

## Rules

1. **Name the standard in the build; never take the compiler's default.** Target C17, and C23
   only where every supported compiler has each feature used.
2. **Write no undefined behavior.** The optimizer assumes there is none, and deletes the checks
   that would catch it.
3. **Give every allocation one owner; copy and free a library's objects with its functions.**
4. **Check the room left at every write into a buffer,** not once before the first.
5. **Check every call that can fail, `fclose` included, and report the first failure.**
6. **A test exits 0 to pass and 77 to skip;** one that can't run its probe fails, unless
   another environment runs it.
7. **Move old code one standard at a time,** and let the compiler's errors list the work.

### Standards and compilers

- **The defaults differ and move:** GCC 15 and later use `gnu23`, Clang `gnu17`, and MSVC
  without `/std:c11` or `/std:c17` C89 with extensions (facts `c-gcc-default`,
  `c-clang-default`, `c-msvc-default`).
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
- **Use after `free`,** which AddressSanitizer finds; **uninitialized reads,** which only
  Valgrind or Clang's MemorySanitizer find; **a pointer past one beyond an array,** caught only
  when dereferenced.

### Ownership

Copying a struct copies its pointers. `b = a` or `memcpy(&b, &a, sizeof a)` on a struct owning
heap memory makes two owners: freeing `a` leaves `b.label` dangling, a use after free, and
freeing `b` frees it again, a double free. Use the library's copy and free functions; GMP warns
against copying its objects at all (fact `c-gmp-copy`). Otherwise lend a pointer, or write a
deep copy:

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
checks the room left, terminator included. On failure, take back the partial record.

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
    size_t start = b->len;
    if (buf_append(b, key, strlen(key)) != 0 || buf_append(b, "=", 1) != 0 ||
        buf_append(b, value, strlen(value)) != 0 || buf_append(b, "\n", 1) != 0) {
        b->len = start;
        if (start < b->cap)
            b->data[start] = '\0';
        return -1;
    }
    return 0;
}
```

### Errors and files

- **A `FILE` buffers,** so `fwrite` and `fprintf` succeed on a full disk, and the error comes
  at `fflush` or `fclose` (fact `c-posix-stdio`). Check `fwrite`'s count, every `fflush` and
  `fclose`; after unchecked `fprintf` or `putc` calls, test `ferror` before `fclose`.
- **`fclose` closes the stream even if it fails:** never call it twice.
- **Keep the first error:** save `errno` at once, since the next call may change it, and never
  let a cleanup call's status, or `perror` after one, replace it.
- **Check `stdout` before exiting** where output is the product: `fflush(stdout) == EOF ||
  ferror(stdout)`. Unchecked, `prog > /dev/full` exits 0.

```c
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdio.h>

/* Writes a new file. Returns 0, or the errno of the first failure. */
int write_file(const char *path, const void *data, size_t size)
{
    FILE *f = fopen(path, "wb");
    if (f == NULL)
        return errno;
    int err = 0;
    if (fwrite(data, 1, size, f) != size)
        err = errno ? errno : EIO; /* only POSIX promises errno here */
    if (fclose(f) == EOF && err == 0) /* a full disk may show only here */
        err = errno ? errno : EIO;
    return err;
}
```

`"wb"` empties an existing file first, losing it on failure. To replace it, write a temporary
file in its directory (c-security's `mkstemp`); `fflush`, `fsync`, `fchmod` to the old mode and
`fclose` it; then `rename` it over the old, so readers never see half of it, and `fsync`
the directory (fact `c-replace`).

### Tests

`meson test` passes 0, skips 77 and calls 99 an error (fact `c-meson-exit-codes`). A test that
can't run its probe prints why and fails, or returns 77 where another job runs it. Test write
errors with Linux's `/dev/full`, which gives `ENOSPC`.

### Moving old code forward

Build with the target standard named, and fix in this order:

1. **C99's removals:** implicit `int` and calls to undeclared functions are errors from GCC 14
   (fact `c-gcc14-errors`). Add the type; include the header.
2. **`f()`:** C23 reads it as `f(void)`, so a call with arguments fails (fact `c-gcc15-c23`).
3. **K&R definitions,** `int f(a) int a; {…}`: removed in C23 (fact `c-clang-knr`). In C23
   mode Clang 18 rejects them and GCC 13 warns; in `gnu17` Clang warns and GCC is silent.
4. **New keywords:** `bool`, `true`, `false`, `nullptr`, `thread_local` and others (fact
   `c-gcc15-c23`), so `typedef int bool;` fails. Use `<stdbool.h>`, but `bool` isn't `int` in
   the ABI: check structs in files and interfaces.

## Mistakes

- **Relying on the default standard:** AI assistants write `nullptr`, or `bool` with no
  header; GCC 15's default builds it, and Clang 18's rejects it.
- **`p = realloc(p, n)`:** on failure the old block stays allocated (fact `c-realloc`) and the
  pointer to it is lost. Assign to a temporary; on success, to `p`.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Standard | No `-std` or `c_std`; C23 features in a C17 project | `GAP`; `DRIFT` for the mismatch | Name C17 |
| Shallow copies | `=` or `memcpy` of a struct with owned pointers | `BLOCKER` where both copies are freed, else `GAP` | The library's copy |
| Bounds | A buffer write with no check of the room left at that write | `BLOCKER` where outside data sets the length, else `GAP` | One checked append |
| Unchecked writes | `fwrite`, `fflush`, `fclose` or the product's `stdout` unchecked; a later status replacing the first | `BLOCKER` where the output is the product, else `GAP` | Check each; keep the first error |
| In-place rewrites | `"w"` on a file that must survive failure | `GAP` | Temporary file, `rename` |
| Undefined behavior | `x + 1 < x`; a null test after a dereference; casts between pointer types | `BLOCKER` where outside data reaches it, else `GAP` | Test before the operation; `memcpy` |
| Unprobed tests | Exit 0 when the test couldn't run | `BLOCKER` | Fail, or 77 if another job runs it |
| Old C | K&R definitions; `()` called with arguments; `bool` typedefs | `DRIFT` | Prototypes; `<stdbool.h>` |

## Why

**1. The standard.** A project naming none changed language when GCC 15 moved to `gnu23` (fact
`c-gcc15-c23`). C17 is the newest standard all three accept by name (fact `c-msvc-default`); the
Linux kernel names `gnu11` (fact `c-kernel-flags`). Cost: no `nullptr` or `ckd_*`. Otherwise:
C23 where each compiler's status page lists every feature used.

**2. Undefined behavior.** A check that can only fire after undefined behavior is deleted (fact
`c-gcc-ub-opts`). Linux turns such assumptions off (fact `c-kernel-flags`), a choice c-build
weighs. Cost: a test before the operation.

**3. Ownership.** An audit found a library's struct copied with `memcpy`, then both copies
freed. GMP discourages any copy (fact `c-gmp-copy`). Cost: a copy function per type. Otherwise:
an arena, which frees everything at once.

**4. Bounds at every write.** A check before the first write misses writes added later. GLib's
`GString` grows instead of failing. Cost: a call per write. Otherwise: grow when no limit is set.

**5. Every call, and the first failure.** Buffering moves a full disk's error to `fclose`, so a
program checking only `fwrite` reports success for data it lost. The first failure is the
cause. Cost: an error path to test. Otherwise: a write whose
loss doesn't matter, said in a comment.

**6. Test exit codes.** A test that exits 0 unprobed is a pass that measured nothing. Meson
reads 77, or `1..0 # SKIP` from a TAP test, as a skip (fact `c-meson-exit-codes`).

**7. One standard at a time.** GCC 14 made old warnings errors (fact `c-gcc14-errors`), and C23
changes meanings. Cost: a CI job per standard. Otherwise: pin `gnu17` for code no one changes.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `c-gcc-default` | GCC's default C mode | [GCC](https://gcc.gnu.org/onlinedocs/gcc/Standards.html) | "The default, if no C language dialect options are given, is -std=gnu23." | 2026-10-27 | 2027-04-27 |
| `c-clang-default` | Clang's default C mode | [Clang](https://clang.llvm.org/docs/UsersManual.html) | "If no -std option is specified, clang defaults to gnu17 mode." | 2026-10-27 | 2027-04-27 |
| `c-msvc-default` | MSVC's C modes; no VLAs | [/std](https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version?view=msvc-170) | "implements ANSI C89, but includes several Microsoft extensions" and "/std:c17 Enables ISO C17 conformance" and "Variable length array (VLA) support isn't planned." | 2026-10-27 | 2027-04-27 |
| `c-gcc15-c23` | GCC 15 moved to C23 | [GCC 15](https://gcc.gnu.org/gcc-15/porting_to.html) | "from -std=gnu17 to -std=gnu23" and "In C23 such declarations mean (void)" and "including bool, true, false, nullptr, and thread_local" and "the bool type is not the same as int at ABI level" | 2026-10-27 | 2027-10-27 |
| `c-gcc14-errors` | GCC 14's errors; strict modes | [GCC 14](https://gcc.gnu.org/gcc-14/porting_to.html) | "In GCC 14, these issues are now reported as errors" and "The GNU C library automatically suppresses these extensions in standard C mode" | 2026-10-27 | 2027-10-27 |
| `c-clang-knr` | C23 drops K&R | [Clang](https://clang.llvm.org/c_status.html) | "Remove support for function definitions with identifier lists N2432 Clang 15" | 2026-10-27 | 2027-10-27 |
| `c-gcc-ub-opts` | Null tests after use; aliasing | [GCC](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) | "if a pointer is checked after it has already been dereferenced, it cannot be null" and "The -fstrict-aliasing option is enabled at levels -O2, -O3, -Os." | 2026-10-27 | 2027-10-27 |
| `c-kernel-flags` | Linux's standard and flags | [Makefile](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Makefile) | "-std=gnu11" and "-fno-strict-aliasing" and "-fno-delete-null-pointer-checks" | 2026-10-27 | 2027-04-27 |
| `c-gmp-copy` | GMP: don't copy | [GMP](https://gmplib.org/manual/Variable-Conventions) | "it is discouraged to make copies of the GMP object itself" | 2026-10-27 | 2027-10-27 |
| `c-posix-stdio` | `fclose` flushes; `errno` | [fclose](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fclose.html), [fwrite](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fwrite.html), [errno](https://pubs.opengroup.org/onlinepubs/9799919799/functions/errno.html) | "Any unwritten buffered data for the stream shall be written to the file" and "Whether or not the call succeeds, the stream shall be disassociated from the file" and "[CX] and errno shall be set" and "until it is changed by the next function call" | 2026-10-27 | 2027-10-27 |
| `c-realloc` | A failed `realloc` keeps the block | [malloc(3)](https://man7.org/linux/man-pages/man3/realloc.3.html) | "If these functions fail, the original block is left untouched" | 2026-10-27 | 2027-10-27 |
| `c-replace` | Atomic `rename`; `fsync` the directory | [rename](https://pubs.opengroup.org/onlinepubs/9799919799/functions/rename.html), [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html) | "shall remain visible to other threads throughout the renaming operation" and "an explicit fsync() on a file descriptor for the directory is also needed" | 2026-10-27 | 2027-10-27 |
| `c-meson-exit-codes` | `meson test`: 77 skips, 99 errors | [Meson](https://mesonbuild.com/Unit-tests.html) | "error code 77" and "1..0 # SKIP" and "error code 99" | 2026-10-27 | 2027-04-27 |

## Sources

| Source | Used for | License |
|---|---|---|
| [GCC](https://gcc.gnu.org/onlinedocs/gcc/), [GMP](https://gmplib.org/manual/) | Defaults, C23, copies | GFDL 1.3; GCC's release notes, verbatim only: short quotes |
| [Clang](https://clang.llvm.org/docs/) | Defaults, K&R | Apache-2.0 with LLVM exception: short quotes |
| [Microsoft Learn](https://learn.microsoft.com/en-us/cpp/) | MSVC | CC BY 4.0: short quotes, attributed |
| [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/), [man7.org](https://man7.org/linux/man-pages/) | Files, `errno`, `realloc` | All rights reserved; each page's own: short quotes |
| [Meson](https://mesonbuild.com/Unit-tests.html) | Test exit codes | CC BY-SA 4.0: short quotes, attributed |
| [Linux](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Makefile), [GLib](https://docs.gtk.org/glib/struct.String.html) | What others do | GPL-2.0, LGPL-2.1-or-later: pointed to |
