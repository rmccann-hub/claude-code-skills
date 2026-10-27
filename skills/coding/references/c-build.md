# C build

Read this for building and checking C: Meson's `project()`, options, tests and wraps, warnings
and the CI gate, hardening, sanitizers and Valgrind, static analysis, and fuzzing.

The language, memory, errors and test exit codes: c-coding. Outside data: c-security. Layout
and the options file's name: project-bootstrap-and-audit (*Language toolchains*). CI files:
git-workflows.

## Rules

1. **Set `meson_version` to the oldest Meson that builds the project,** and prove it in CI.
2. **Configure in `project()`, and add flags with `add_project_arguments`.**
3. **Ship without `werror`. CI counts warnings under the shipped flags** and fails above a limit.
4. **Ask for hardening yourself,** filtered by `cc.get_supported_arguments`.
5. **Test under ASan and UBSan, and Valgrind on a plain build;** ask the binary if it's
   instrumented.
6. **Make every checker fail on a finding.** Most exit 0 by default.
7. **Run a static analyzer in CI.**
8. **Fuzz every parser of outside data,** with the code under test instrumented too.
9. **Pin each wrap.**

### The project

```meson
project('reader', 'c',
  meson_version : '>=1.3.0',  # c_std's fallback list
  default_options : ['c_std=gnu17,c17', 'warning_level=3',
    'buildtype=debugoptimized', 'b_ndebug=if-release', 'b_pie=true'])

cc = meson.get_compiler('c')
flags = ['-Wformat=2', '-Wconversion', '-Wimplicit-fallthrough',
  '-Werror=format-security', '-Werror=implicit',
  '-Werror=incompatible-pointer-types', '-Werror=int-conversion',
  '-fstack-protector-strong', '-fstack-clash-protection',
  '-fstrict-flex-arrays=3', '-fcf-protection=full', '-U_FORTIFY_SOURCE']
# FORTIFY needs -O1 or more, and sanitizers don't support it.
if get_option('b_sanitize') == 'none' and get_option('optimization') not in ['0', 'plain']
  flags += '-D_FORTIFY_SOURCE=3'
endif
if cc.has_function('strlcpy', prefix : '#include <string.h>')
  flags += '-DHAVE_STRLCPY=1'
endif
add_project_arguments(cc.get_supported_arguments(flags), language : 'c')
if get_option('fuzzing')  # Clang: coverage for the code the fuzzer drives
  add_project_arguments('-fsanitize=fuzzer-no-link', language : 'c')
endif
add_project_link_arguments(cc.get_supported_link_arguments(
  '-Wl,-z,relro', '-Wl,-z,now', '-Wl,-z,noexecstack'), language : 'c')
add_test_setup('valgrind', timeout_multiplier : 10,
  exe_wrapper : ['valgrind', '--error-exitcode=1', '--leak-check=full'])

subdir('src')    # parse = static_library('parse', 'parse.c'); the executable
subdir('tests')  # test('parse', exe, suite : 'unit', timeout : 30)
if get_option('fuzzing')
  subdir('fuzz')  # executable('fuzz-parse', ..., link_args : '-fsanitize=fuzzer')
endif
```

- **The root** holds `project()`, the flags, which precede every target, and `subdir()`; each
  directory's `meson.build` holds its targets.
- **The floor:** Meson warns of newer features (fact `cb-feature-new`), but 1.12.1 passed the
  `c_std` list under `>=1.2`, which Meson 1.2 rejects. CI builds with `meson==1.3.0` too.
- **`c_std=gnu17,c17`** falls back to ISO C on MSVC, where a bare `gnu17` is to become an error
  (fact `cb-c-std`).
- **Defaults:** `buildtype` `debug` (`-O0`), `b_pie` and `werror` off; `-Ddebug=false` leaves
  `NDEBUG` out (fact `cb-meson-defaults`). `default_options` reach new build directories only,
  and `c_args` there drops the packager's `CFLAGS` (fact `cb-default-options`). Packagers'
  `CFLAGS` come last and win: `-D_FORTIFY_SOURCE=2` there lowers the level.
- **Tests:** `timeout` defaults to 30 seconds (fact `cb-test-env`); `meson test --suite unit`
  runs a suite, `--setup valgrind` the setup above.

### Warnings and the CI gate

The set is a subset of OpenSSF's (fact `cb-openssf`): add its production flags, such as
`-ftrivial-auto-var-init=zero` and `-fno-strict-overflow`, where speed allows, and
`-mbranch-protection=standard` on aarch64. Turn on `-Wconversion` in old code by degrees. The
gate builds fresh, like the release, and counts:

```bash
set -euo pipefail
meson setup build-ci --buildtype=release -Db_colorout=never
meson compile -C build-ci 2>&1 | tee build-ci.log
count=$(grep -c -E ':[0-9]+:[0-9]+: warning:' build-ci.log || true)
limit=$(<.warning-limit)
if ((count > limit)); then
  printf 'compiler warnings: %d, limit %d\n' "$count" "$limit" >&2
  exit 1
fi
```

Ninja shows warnings only for files it compiles, and color breaks the pattern.

### Hardening and the distributions

Ubuntu builds hardening into its GCC (fact `cb-ubuntu`); Debian and Fedora put it in package
build flags (facts `cb-debian`, `cb-fedora`), which a developer's `gcc` never sees. On Ubuntu
24.04, GCC 13.3 at `-O2` set `_FORTIFY_SOURCE` to 3 and Clang 18.1 not at all (checked
2026-10-27), so ask: `echo | gcc -O2 -dM -E - | grep FORTIFY`. Level 3 needs GCC 12 and glibc
2.35, or Clang 9 and glibc 2.33 (fact `cb-fortify3`). Check the binary: `readelf -h` shows
`DYN`, `readelf -d` `BIND_NOW`, `readelf -l` `GNU_RELRO`.

### Run-time checks

- **`-Db_sanitize=address,undefined`,** and `-Db_lundef=false` under Clang (fact `cb-sanitize`).
  `meson test` makes ASan and UBSan abort (fact `cb-test-env`). Run alone, a UBSan binary
  reports and exits 0 (fact `cb-sanitizers`): set `UBSAN_OPTIONS=halt_on_error=1`.
- **Ask the binary, not the log:** `nm build/tests/test-parse | grep -c __asan_init`, or
  `__ubsan_handle_`; `grep -q` stops early, and `pipefail` fails on `nm`'s broken pipe.
- **Threaded code** gets a `-Db_sanitize=thread` job; TSan can't join ASan (fact `cb-sanitizers`).
- **Valgrind returns the program's status** unless `--error-exitcode` is set (fact
  `cb-valgrind`), so a leaking test passes. On an ASan build it stops at once.

### Static analysis

- **`-fanalyzer`** is for C, and slow (fact `cb-analyzer`): a job of its own.
- **clang-tidy** is Meson's `clang-tidy` target with a `.clang-tidy`, failing only on checks
  named in `WarningsAsErrors` (fact `cb-clang-tidy`).
- **scan-build** is `SCANBUILD='scan-build --status-bugs' ninja -C build scan-build`, or a
  versioned `scan-build-NN`; the target takes none
  (fact `cb-scan-build`).
- **cppcheck** needs `--error-exitcode=1`, with `--project=build/compile_commands.json` (fact
  `cb-cppcheck`).

### Fuzzing

A target hands any bytes to the parser and never calls `exit()` (fact `cb-libfuzzer`). Build it
with Clang and `-Dfuzzing=true`; `build/fuzz/fuzz-parse corpus/*` replays a corpus.

```c
#include <stddef.h>
#include <stdint.h>

int parse_record(const uint8_t *data, size_t size, char *name, size_t name_size);
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size);

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    char name[64];
    (void)parse_record(data, size, name, sizeof name);
    return 0;
}
```

### Wraps

`revision = HEAD` in a `wrap-git` follows upstream: name a tag or commit, or use a `wrap-file`
with `source_hash`. Given `subprojects/wrapdb.json`, Meson downloads missing dependencies;
`--wrap-mode=nodownload` stops it (fact `cb-wrap`).

## Mistakes

- **`werror=true` in shipped `default_options`:** a newer compiler fails the user's build, and
  since Meson 1.12 a linker warning (fact `cb-werror-linker`).
- **`-D_FORTIFY_SOURCE=2` in project flags:** silently lowers Ubuntu's GCC from 3.
- **`-fsanitize=fuzzer` on the fuzz target alone:** the library lacks coverage; `cov:` stays flat.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Floor | A feature above `meson_version` | `DRIFT` | Raise it; build on it |
| Shipped flags | `werror=true` or `c_args` in `default_options` | `GAP` | Move them |
| Warning gate | None, or flags other than the release's | `GAP` | The count gate |
| Hardening | Flags missing, or `_FORTIFY_SOURCE=2` | `GAP` | The set above |
| Sanitizer job | None, or not checked by `nm` | `GAP`; `BLOCKER` if uninstrumented | `b_sanitize` |
| Silent checkers | A checker that can't fail | `BLOCKER` | The flags above |
| Fuzzing | A parser of outside data unfuzzed | `GAP` | A target |
| Wraps | `revision = HEAD`; no `source_hash` | `DRIFT` | Pin |

## Why

**The count gate.** OpenSSF keeps blanket `-Werror` to development: in shipped source it ties
the build to one compiler (fact `cb-openssf`). Counting under the release's flags is this
repository's own lesson: a CI-only `-Werror` job at
`-O0` misses warnings GCC gives only when optimizing (fact `cb-gcc-opt-warnings`), and a limit
lets old code ratchet down. Cost: the pattern fits GCC and Clang, not MSVC.
Otherwise: OpenSSF's `-Dwerror=true` in CI, on a pinned compiler.

**Hardening.** Distribution defaults vary and reach only their packages; a build's flags reach
every user, at some cost in speed.

**Sanitizers, and asking the binary.** They catch what tests pass over, when built in: a test
log once looked sanitized while the binary wasn't. Cost: tests run 2 to 4 times slower, 20 to 50
under Valgrind (fact `cb-openssf`).

**Checkers that fail.** Exiting 0 on a finding reports success while measuring nothing.

**Fuzzing** finds inputs nobody tested. Cost: Clang and CI time. libFuzzer gets fixes, not
features (fact `cb-libfuzzer`); AFL++ runs the same target. **Pinned wraps** build the same code
each day, at the cost of updating by hand.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `cb-feature-new` | Newer features warn | [0.47](https://mesonbuild.com/Release-notes-for-0-47-0.html) | "that's newer than the version specified inside project()" | 2026-10-27 | 2027-10-27 |
| `cb-c-std` | `c_std` lists, 1.3; `gnuXX` on MSVC | [Options](https://mesonbuild.com/Builtin-options.html) | "Since 1.3.0 c_std and cpp_std options now accept a list of values." and "will become an hard error" | 2026-10-27 | 2027-04-27 |
| `cb-meson-defaults` | Defaults | [Options](https://mesonbuild.com/Builtin-options.html) | "werror false" and "b_pie false" and "-Ddebug=false does not cause the compiler preprocessor macro NDEBUG to be defined" | 2026-10-27 | 2027-04-27 |
| `cb-default-options` | First run; `c_args` | [project()](https://mesonbuild.com/Reference-manual_functions.html) | "only used when running Meson for the first time" and "the CFLAGS environment variable is not used" | 2026-10-27 | 2027-10-27 |
| `cb-werror-linker` | 1.12: linker too | [1.12](https://mesonbuild.com/Release-notes-for-1-12-0.html) | "fatal-warnings flag to the linker" | 2026-10-27 | 2027-10-27 |
| `cb-sanitize` | `b_lundef`, Clang ASan | [Options](https://mesonbuild.com/Builtin-options.html) | "incompatible with the address sanitizer when building shared libraries with clang" | 2026-10-27 | 2027-04-27 |
| `cb-test-env` | Aborts; 30 s | [test()](https://mesonbuild.com/Reference-manual_functions.html) | "set to enable aborting on detected violations" and "defaults to 30 seconds" | 2026-10-27 | 2027-04-27 |
| `cb-sanitizers` | UBSan continues; TSan alone | [GCC](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html) | "may indicate success even when errors have been reported" and "cannot be combined with -fsanitize=address" | 2026-10-27 | 2027-10-27 |
| `cb-fortify3` | Level 3 floors | [2.33](https://lists.gnu.org/archive/html/info-gnu/2021-02/msg00000.html), [2.35](https://savannah.gnu.org/news/?id=10075) | "available only on LLVM 9 and later" and "compiling with glibc and gcc 12 and later" | 2026-10-27 | 2027-10-27 |
| `cb-valgrind` | Status passed through | [Valgrind](https://valgrind.org/docs/manual/manual-core.html) | "will always be the return value of the process being simulated" | 2026-10-27 | 2027-10-27 |
| `cb-openssf` | Guide of 2026-08-20 | [OpenSSF](https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html) | "2026-08-20" and "should not be used in this blanket form when distributing source code" and "Requires -O1 or higher" and "2× to 4× slowdown" and "20× to 50×" and "CC BY 4.0" | 2026-10-27 | 2027-04-27 |
| `cb-gcc-opt-warnings` | Warnings need `-O` | [GCC](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html) | "may not be issued at all unless optimization is enabled" | 2026-10-27 | 2027-10-27 |
| `cb-ubuntu` | Ubuntu patches GCC | [Ubuntu](https://documentation.ubuntu.com/security/docs/security-features/security-features-overview/) | "Built with Fortify Source gcc patch" | 2026-10-27 | 2027-04-27 |
| `cb-debian` | Debian | [dpkg-buildflags](https://manpages.debian.org/testing/dpkg-dev/dpkg-buildflags.1.en.html) | "during build of Debian packages" and "adds -D_FORTIFY_SOURCE=2" and "if relro is not enabled. Disabled by default." | 2026-10-27 | 2027-04-27 |
| `cb-fedora` | Fedora | [buildflags](https://src.fedoraproject.org/rpms/redhat-rpm-config/raw/rawhide/f/buildflags.md) | "By default, the build flags include -Wp,-D_FORTIFY_SOURCE=3" | 2026-10-27 | 2027-04-27 |
| `cb-analyzer` | `-fanalyzer`: C, costly | [GCC](https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html) | "much more expensive than other GCC warnings" and "only suitable for use on C code" | 2026-10-27 | 2027-04-27 |
| `cb-clang-tidy` | Target; errors | [0.52](https://mesonbuild.com/Release-notes-for-0-52-0.html), [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) | "automatically define a clang-tidy target" and "Upgrades warnings to errors" | 2026-10-27 | 2027-10-27 |
| `cb-scan-build` | `SCANBUILD`; `--status-bugs` | [Meson](https://mesonbuild.com/howtox.html), [man](https://raw.githubusercontent.com/llvm/llvm-project/main/clang/tools/scan-build/man/scan-build.1) | "use the SCANBUILD environment variable" and "Set exit status to 1 if it found potential bugs" | 2026-10-27 | 2027-10-27 |
| `cb-cppcheck` | Exits 0 by default | [cppcheck](https://raw.githubusercontent.com/danmar/cppcheck/main/cli/cmdlineparser.cpp) | "If errors are found, integer [n] is returned instead of" | 2026-10-27 | 2027-10-27 |
| `cb-libfuzzer` | Targets; status | [libFuzzer](https://llvm.org/docs/LibFuzzer.html) | "It must not exit() on any input." and "have stopped active work on it" | 2026-10-27 | 2027-04-27 |
| `cb-wrap` | `HEAD`; WrapDB fetch | [Wrap](https://mesonbuild.com/Wrap-dependency-system-manual.html), [wraptool](https://mesonbuild.com/Using-wraptool.html) | "HEAD to track upstream's default branch" and "available in WrapDB will automatically be downloaded" | 2026-10-27 | 2027-10-27 |

## Sources

The rules and examples are this module's own, run on 2026-10-27.

| Source | Used for | License |
|---|---|---|
| [Meson](https://mesonbuild.com/) | Meson | CC BY-SA 4.0: short quotes |
| [OpenSSF](https://best.openssf.org/) | Flags | CC BY 4.0 (fact `cb-openssf`): attributed |
| [GCC](https://gcc.gnu.org/onlinedocs/gcc/), Valgrind, glibc | Sanitizers, FORTIFY | GFDL: short quotes |
| [LLVM](https://llvm.org/docs/LibFuzzer.html), cppcheck | Fuzzing, analysis | Apache-2.0 with LLVM exceptions; GPL: short quotes |
| [Ubuntu](https://documentation.ubuntu.com/security/), Debian, Fedora | Distribution flags | CC BY-SA 3.0; site terms: short quotes |
