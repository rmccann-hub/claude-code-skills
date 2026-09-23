# RESEARCH RUN R16: Office (Excel, Word, VBA), Epicor Kinetic and SOLIDWORKS

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: excel, vba, word-documents, epicor-kinetic, solidworks-api, legacy-languages (VBA, VBScript).

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R16 · FORM: research-result v1
Save as: R16-RESULT.md
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

- Microsoft 365 Apps are 64-bit by default; VBA 7.1 is current; since 2022 Office blocks macros in files from the internet by default.
- Microsoft is deprecating VBScript and said VBA will get built-in regular expressions, so projects using VBScript.RegExp keep working.
- ActiveX controls have been disabled by default in Microsoft 365 Apps since 2025.
- The new Outlook for Windows supports neither COM add-ins nor VBA; classic Outlook remains supported for years.
- Excel added REGEXTEST, REGEXEXTRACT and REGEXREPLACE, GROUPBY, PIVOTBY, PERCENTOF, TRIMRANGE and a COPILOT function; Python in Excel is generally available; Aptos is the default Office font.
- openpyxl 3.1.x is in maintenance; XlsxWriter 3.2.x is active; python-calamine is a fast reader; python-docx 1.2 is current.
- In OOXML, newer Excel functions are stored with a `_xlfn.` prefix, LET and LAMBDA parameters with `_xlpm.`, and some worksheet functions with `_xlws.`.
- Epicor releases Kinetic yearly (for example 2025.1, 2025.2) with REST API v2 and API keys; BPM custom code is C#; Kinetic Functions replace many BPM workflows; the classic client is retired.
- SOLIDWORKS 2026 was released in October 2025; its API help is at help.solidworks.com; VSTA macros use .NET Framework.

## Questions

### Priority

1. VBA and Office automation today:
   - support status and roadmap: VBA, 64-bit Declare statements (PtrSafe, LongPtr), macro blocking and Trusted Locations, the ActiveX default
   - the VBScript deprecation phases, and the replacement for VBScript.RegExp in VBA
   - the timeline for new Outlook versus classic Outlook, and Office LTSC 2024 support dates
   - what a professional uses instead of VBA for new work (Office Scripts, Office JS add-ins, Power Automate, Python in Excel), and when VBA is still right
2. Excel:
   - functions added since 2023 (confirm the list); Python in Excel's status and limits
   - where Office Scripts run (web, Windows, Mac); current Office JS API requirement sets; the status of the unified JSON manifest for add-ins
   - changes to Power Query M and DAX (DAX user-defined functions); Power BI's newer project and report formats (PBIP, PBIR)
3. Generating Office files from code:
   - current versions and maintenance status: openpyxl, XlsxWriter, python-calamine, pandas engines; ClosedXML and Open XML SDK 3.x (.NET); ExcelJS and SheetJS (JS); python-docx, python-pptx, docx (npm)
   - OOXML prefix rules for newer functions (`_xlfn.`, `_xlpm.`, `_xlws.`), citing Microsoft's [MS-XLSX]
   - recalculation options (LibreOffice headless, Excel through COM) and their pitfalls
4. Word templates: content controls versus placeholders; fields and table-of-contents updating (updateFields); numbering definitions (w:num, w:abstractNum) and restarting lists; what python-docx and the Open XML SDK can and can't do; document accessibility (Microsoft's accessibility checker, PDF/UA).
5. Epicor Kinetic, from public sources only (Epicor's public documentation and release notes, public EpicWeb and EpicCare pages, the Epicor User Help Forum), saying which facts are customer-only:
   - the current release, the release cadence, and the support status of Epicor ERP 10.2.x
   - REST API v2: authentication (API keys plus user credentials or tokens), URL shapes for business objects, BAQs and Kinetic Functions, OData options, paging
   - BPM in Kinetic: the web designer, C# version, server .NET version, restrictions in Epicor-hosted cloud tenants
   - BAQ Designer changes; Application Studio versus classic customizations; UD fields (`_UD` tables and `_c` columns)

### Standard

6. The SOLIDWORKS API: the current release, where the API help lives, methods made obsolete in the 2024-2026 releases and their replacements (for example OpenDoc6/7, SaveAs, InsertBomTable, CreateSectionViewAt), VSTA's .NET versions, Document Manager API licensing, the PDM API, STEP AP242 export options.
7. Power Platform, where it bears on Office automation: Power Automate desktop versus cloud flows, Power Apps, licensing basics.
8. Mistakes AI assistants make in VBA, Excel formulas, Office file generation, Epicor BPM and SOLIDWORKS macros.
