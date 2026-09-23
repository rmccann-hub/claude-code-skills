# RESEARCH RUN R17: Legacy languages and modernization

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: legacy-languages, legacy-modernization.

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

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R17 · FORM: research-result v1
Save as: R17-RESULT.md
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

- Microsoft's "It Just Works" support statement covers the VB6 runtime on current Windows versions, but not the IDE.
- VBScript is being phased out of Windows (disabled by default around 2027, then removed); classic ASP is still supported in IIS.
- COBOL's current standard is ISO/IEC 1989:2023, and GnuCOBOL 3.2 is current.
- Fortran 2023 (ISO/IEC 1539-1:2023) is the current standard; fpm is Fortran's package manager; LFortran is in development.
- Delphi 12 or 13 is current, and Free Pascal 3.2.x.
- Perl 5.42 is current. Python 2 reached end of life in January 2020, and PHP 7.4 in November 2022.
- .NET Framework 4.8.1 is the last version and is supported as part of Windows.
- AngularJS reached end of life in December 2021.
- IBM i 7.6 was released in 2025, and free-form RPG IV is the modern style.
- Visual FoxPro reached end of support in 2015.

## Questions

### Priority

1. For each legacy language or platform, give its current support status with dates, the modern target or targets most sources recommend, the official or best migration tools, the main risks when reading and changing its code, and how to test before changing it:
   - Microsoft: VB6, VBScript, classic ASP, old VBA patterns, .NET Framework (WinForms, WebForms, WCF, Remoting), Windows PowerShell 5.1, batch/CMD, Access, Visual FoxPro
   - mainframe and midrange: COBOL, RPG (IBM i)
   - other languages: Fortran, Pascal/Delphi, Perl 5, Python 2, PHP 5-7, Java 8 and older, C89/C++98, ColdFusion
   - the web: jQuery and AngularJS
2. Techniques, citing Michael Feathers, Martin Fowler and others, with current tools (such as ApprovalTests):
   - characterization (golden master) tests and approval testing
   - the strangler fig pattern, branch by abstraction, anti-corruption layers
   - incremental database migration
   - differential testing to prove equivalence
3. AI-assisted modernization: what AWS Transform (formerly Amazon Q Developer's transformation feature), GitHub Copilot app modernization, IBM watsonx Code Assistant for Z and similar tools do today; published results and failure modes; how to verify code an AI translated.

### Standard

4. Reading unfamiliar old code: tools (tree-sitter grammars for legacy languages, ctags, code search, dependency graphs), documentation archaeology, finding dead code.
5. Case studies of successful and failed legacy migrations from 2023-2026 (for example government COBOL systems, banks), with their lessons.
6. Mistakes AI assistants make when reading or translating legacy code (for example COBOL decimal arithmetic, VB6 Variant semantics, implicit conversions).
