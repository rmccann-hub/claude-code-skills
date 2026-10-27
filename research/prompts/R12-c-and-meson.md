# RESEARCH RUN R12: C, built with Meson

For the repository rmccann-hub/claude-code-skills · Prompt version 3 · Written 27 October 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 27 October 2026.

This run informs these categories: c (a `c-coding` module and a `c-security` module beside it),
and the C with Meson rows of the repository's standard.

## What this run is for

The repository's `coding` skill covers Python, TypeScript, HTML and CSS, C#, PowerShell and Bash,
each as a module of rules, common mistakes, review checks, reasons and dated facts, with a
security module beside it. It has nothing for C. An audit of a real C program built with Meson,
one that reads data from hardware and from outside sources and writes files named from it, is
what showed the gap. This run is the research for the two C modules: what a professional writing
or reviewing C built with Meson must know and check today, with each fact sourced.

Go, Rust and C++ were in earlier versions of this run. They now have a run of their own, R25, so
this one goes deep on C.

## Rules

1. **Primary sources first:** official documentation, specifications and standards bodies, and
   each project's own release notes, changelogs and security advisories. Use secondary sources
   (respected books, well-known engineering blogs, surveys) only where no primary source covers
   the point, and label them "secondary".
2. **Cite every fact:** the URL, the exact sentence you relied on in quotation marks, and a date
   (the source's own date, otherwise the date you read it).
3. **Never guess.** Write "not found" when you can't source something. Write "contested" when good
   sources disagree, and give each side with its source.
4. **Versions:** for every product, give
   - the current stable version and its release date;
   - its end-of-support date;
   - any release due within 6 months, with the expected date and its source.

   Flag anything that reaches end of support within 12 months.
5. **"What we believe" is my current understanding and may be wrong or out of date.** Confirm or
   correct every item, each with a source. The corrections are the most valuable part of this run.
6. **Licences:** for each source, name its licence and say what an Apache-2.0 repository may do
   with it: quote briefly, paraphrase, or adapt its code examples, and with what attribution.
7. **Depth over breadth.** Finish the Priority questions fully. If you run out of room, list the
   rest under "Not covered".
8. **Beliefs marked "(the standard, date)"** come from this repository's own standard,
   PROJECT-BOOTSTRAP-AND-AUDIT v0.48.2, in its section of dated facts. Checking them also
   checks that standard, so say plainly when one is wrong.
9. **Every code example compiles.** Give the compiler, version and flags you'd build it with, and
   mark any example you couldn't check as "not compiled".

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R12 · FORM: research-result v1
Save as: R12-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.
```

Then these sections, in this order:

1. **Summary:** at most 15 bullets a professional must know today.
2. **Corrections:** every "What we believe" item that was wrong or out of date, with the right
   fact and its source.
3. **Facts table:** `| # | Fact | Value | Source URL | Exact quote | Date |`
4. **Findings:** one section per question below, numbered to match.
5. **Tools:** `| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |`
6. **Changing in the next 12 months:** deprecations, end-of-support dates, announced breaking
   changes.
7. **Common mistakes,** including those AI coding assistants make in this area, with sources.
8. **Review checklist:** `| Check | What to look for | How bad if missing | Fix |`, for reviewing
   a C program and its Meson build.
9. **Sources and licences:** `| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |`
10. **Not found, contested, not covered.**

## What we believe (confirm or correct each)

- C23 is ISO/IEC 9899:2024, published in 2024, and GCC 15 defaults to `-std=gnu23`.
- Clang's default C mode is `gnu17`, and Clang supports most of C23 with `-std=c23`.
- MSVC supports C11 and C17 with `/std:c11` and `/std:c17`, and parts of C23 with `/std:clatest`.
- C23 added `<stdckdint.h>` (`ckd_add`, `ckd_sub`, `ckd_mul`) for checked integer arithmetic,
  `nullptr`, `constexpr` objects, `typeof`, `#embed`, `bool` as a keyword, and `[[attributes]]`.
- `gets` was removed in C11. Annex K's bounds-checked functions (`strcpy_s` and the rest) are
  optional, and almost no C library outside Microsoft's implements them.
- glibc 2.38 added `strlcpy` and `strlcat`, and POSIX.1-2024 standardizes them.
- `-D_FORTIFY_SOURCE=3` needs GCC 12 or later, or a recent Clang, with glibc 2.34 or later, and
  works only with optimization on.
- The OpenSSF publishes a "Compiler Options Hardening Guide for C and C++" with a recommended set
  of warning and hardening flags.
- Debian, Ubuntu and Fedora already turn on some hardening by default (stack protector, PIE,
  `_FORTIFY_SOURCE`), so a project's own flags add to theirs.
- GCC's `-fanalyzer` is useful for C, and not yet for C++.
- Gating CI on `-Werror` breaks when a new compiler adds warnings; gating on a count of warnings
  under the shipped flags doesn't. A test log can look sanitized when the binary wasn't built
  with the sanitizer, so CI should ask the binary itself.
- (the standard, 2026-10) For C with Meson, `meson.options` is the current options filename, and
  `meson_options.txt` still works.
- Meson's `warning_level=3` adds `-Wall -Wextra -Wpedantic`, `werror=true` makes warnings errors,
  and `b_sanitize=address,undefined` builds with both sanitizers.
- CISA and the NSA asked software makers to publish memory-safety roadmaps by 1 January 2026.
- SEI CERT C's newest edition is from 2016, and its wiki is still kept up to date.

## Questions

### Priority

1. **Standards and compilers:** C23's status, and the next standard's (C2y) schedule; the default
   C mode and current version of GCC, Clang and MSVC, with each one's support window; which
   standard a portable program should target today, and how to say so in a Meson build.
2. **Warnings and how CI gates on them:** the recommended warning set for GCC, Clang and MSVC
   (`-Wall -Wextra -Wpedantic`, `-Wconversion`, `-Wshadow`, `-Wformat=2` and the rest), with what
   each catches and which are too noisy to keep; `-Werror` against a count of warnings; MSVC's
   `/W4` and `/analyze`.
3. **Hardening:** `_FORTIFY_SOURCE`, `-fstack-protector-strong`, `-fstack-clash-protection`,
   `-fcf-protection`, PIE and full RELRO, `-ftrivial-auto-var-init`, and which of these the main
   Linux distributions already turn on, so a project doesn't repeat or weaken them. Cite the
   OpenSSF guide's current version.
4. **Sanitizers and dynamic analysis:** AddressSanitizer, UndefinedBehaviorSanitizer,
   ThreadSanitizer, MemorySanitizer, LeakSanitizer and Valgrind: what each finds, which can run
   together, their cost in CI, and how to check that a binary really is instrumented.
5. **Static analysis:** clang-tidy (which check groups suit C: `bugprone`, `cert`,
   `clang-analyzer`, `security`), cppcheck, GCC's `-fanalyzer`, scan-build and CodeQL for C, with
   current versions; clang-format for layout.
6. **Meson:** the current version and its release pace; `project()`'s `meson_version` and
   `default_options`; `warning_level`, `werror`, `buildtype`, `b_sanitize`, `b_lundef` and
   `b_ndebug`; `meson test` with suites, timeouts and `--wrap` (for Valgrind); `dependency()`,
   pkg-config and WrapDB, and how to pin a wrapped dependency; what Meson deprecated or changed
   in the last 12 months.
7. **C security, the `c-security` module:** for each, the safe pattern, with a source:
   - buffers and strings: the unsafe functions and their replacements, and `strncpy`'s traps;
   - format strings;
   - integer overflow and signed overflow as undefined behavior, and `ckd_*`;
   - paths from outside data: `..`, absolute paths, symlinks, `openat` and `O_NOFOLLOW`, and
     time-of-check-to-time-of-use races;
   - running programs: `system` and `popen` against `posix_spawn` and `execve` with an argument
     array;
   - temporary files with `mkstemp`, and the environment and locale as input;
   - text from outside written to a log or a terminal: control characters and line breaks;
   - the C entries of the current CWE Top 25, and SEI CERT C's rules that matter most.
8. **Memory-safety guidance:** what CISA, the NSA and others asked of C projects (2023 to 2026),
   and what a roadmap means in practice for a small open-source C program.

### Standard

9. **Testing and fuzzing in C:** `meson test`; unit test frameworks (cmocka, Unity, Check,
   Criterion, µnit) with each one's activity and licence; libFuzzer and AFL++ in a Meson build;
   what OSS-Fuzz requires of a project.
10. **Mistakes AI assistants make in C,** with sources where they exist.
11. **Legacy C:** moving C89 and C99 code to C17 or C23 safely, and what changes meaning on the
    way.
