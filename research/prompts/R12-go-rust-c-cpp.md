# RESEARCH RUN R12: Go, Rust, C and C++

For the repository rmccann-hub/claude-code-skills · Prompt version 2 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: go, rust, c, cpp, and legacy-languages (C89, C++98).

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
   PROJECT-BOOTSTRAP-AND-AUDIT v0.35.0, in its section of dated facts. Checking them also
   checks that standard, so say plainly when one is wrong.

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
8. **Sources and licences:** `| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |`
9. **Not found, contested, not covered.**

## What we believe (confirm or correct each)

- Go releases every February and August; Go 1.26 was released in February 2026; Go 1.27 was released or is due in August 2026; the two most recent releases are supported.
- Go 1.23 added range-over-func iterators; 1.24 added testing.B.Loop, `tool` directives in go.mod and Swiss-table maps; 1.25 added testing/synctest, WaitGroup.Go, container-aware GOMAXPROCS and an experimental encoding/json/v2.
- Go's official module layout guide does not endorse a `pkg/` directory.
- (the standard, 2026-09) Rust 1.98.x is current, on edition 2024, and Cargo.lock is committed for libraries too, which reversed the advice in 2023.
- (the standard, 2026-09) For C with meson, `meson.options` is the current options filename, and `meson_options.txt` still works.
- Rust releases every six weeks; the 2024 edition was stabilized in Rust 1.85 (February 2025); let chains were stabilized in 1.88 for the 2024 edition.
- thiserror 2 and anyhow are the standard error crates; cargo-deny, cargo-audit and cargo-vet cover the supply chain.
- C23 (ISO/IEC 9899:2024) is the current C standard, and GCC 15 defaults to it.
- C++23 is published; C++26 was finalized in 2025-2026 with static reflection, contracts and std::execution.
- CMake 4.0 removed compatibility with versions older than 3.5.
- CISA and the NSA asked vendors to publish memory-safety roadmaps by 1 January 2026.

## Questions

### Priority

1. Go: current releases and support; features added in 1.23-1.27 that change idiomatic code; official guidance on module layout, errors (wrapping, errors.Is, As and Join), context, generics and iterators; current versions of gofmt, go vet, staticcheck, golangci-lint v2 and govulncheck.
2. Rust: the current stable version, 2024 edition changes, notable features since 1.80, recommended clippy lint groups, the rustfmt style edition, supply-chain tools, MSRV policy guidance, async (tokio's current version and LTS policy), and the unsafe code guidelines.
3. C: C23 features (nullptr, constexpr, typeof, #embed, the bool keyword, attributes); compiler defaults and flags for GCC, Clang and MSVC; recommended warnings; sanitizers (ASan, UBSan, TSan, MSan); static analysis (clang-tidy, cppcheck, GCC -fanalyzer); SEI CERT C's status.
4. C++: C++23 features in use; C++26's status and headline features; compiler support tables; the C++ Core Guidelines; the status of safety profiles; module adoption; build and package tooling (CMake 4.x, vcpkg, Conan 2).
5. Memory safety: government guidance from CISA, the NSA and others (2023-2026); what a memory-safety roadmap means for a team using C or C++; hardening flags (_FORTIFY_SOURCE=3, -fstack-protector-strong, CFI); strategies for migrating to Rust or other memory-safe languages.

### Standard

6. Testing and fuzzing: go test features (fuzzing, synctest), cargo test and nextest, doctests, GoogleTest, Catch2 and doctest for C++, libFuzzer and AFL++.
7. Mistakes AI assistants make in Go, Rust, C and C++.
8. Legacy: modernizing C89/C99 and C++98/03 code (clang-tidy's modernize checks), and Go or Rust code written for old versions (Go 1.22 changed loop-variable semantics).
