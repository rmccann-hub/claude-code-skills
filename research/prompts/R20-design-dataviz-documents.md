# RESEARCH RUN R20: Visual design, data visualization, documents and output formats

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: visual-theme, data-visualization, documentation (output), word-documents (styling).

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R20 · FORM: research-result v1
Save as: R20-RESULT.md
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

- The W3C Design Tokens Community Group published the first stable version of its Design Tokens specification in 2025.
- OKLCH colour and `light-dark()` are Baseline in CSS.
- Okabe-Ito (popularized by Wong, 2011) and viridis are the standard colour-blind-safe palettes.
- Aptos replaced Calibri as the default Office font in 2023-2024.
- PDF/UA-2 (ISO 14289-2) was published in 2024; PDF 2.0 is ISO 32000-2:2020.
- Common charting libraries are D3 7, Vega-Lite 6, Observable Plot, ECharts 6, Chart.js 4 and Recharts; in Python, matplotlib 3.10, seaborn 0.13, plotly 6 and Altair 5.

## Questions

### Priority

1. Design tokens: the DTCG specification (version, date, format), tooling (Style Dictionary 4 or 5, Tokens Studio), and how to map one token set to CSS, Office documents (theme XML), charts and dark mode.
2. Colour: building accessible palettes, WCAG contrast rules, OKLCH, colour-blind-safe categorical and sequential palettes (with sources), and dark-mode design guidance (Material, Apple's Human Interface Guidelines, Microsoft Fluent).
3. Data visualization practice: choosing chart types (the FT Visual Vocabulary, Datawrapper's guides, Few, Tufte); accessible charts (text alternatives, patterns, never colour alone; W3C and vendor guidance); dashboards (layout, KPI design); common mistakes.
4. Libraries: the current versions and maintenance status of the charting libraries above and the Python libraries, with recommendations for static reports, interactive dashboards, and Excel or PowerPoint charts.

### Standard

5. Typography: system font stacks, variable fonts, Office's default fonts (Aptos) and their availability outside Windows, font licensing (SIL OFL).
6. Documents: accessible Word and PowerPoint (headings, alt text, tables, reading order), PDF/UA-2 and PDF 2.0 tooling, Markdown-to-document pipelines (Pandoc's current version, Quarto), Mermaid for diagrams.
