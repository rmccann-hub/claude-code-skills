# RESEARCH RUN R18: Accessibility, internationalization, privacy and licensing compliance

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: accessibility, internationalization, privacy-and-compliance, documentation (licences and notices).

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R18 · FORM: research-result v1
Save as: R18-RESULT.md
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

- WCAG 2.2 (October 2023) is the current W3C Recommendation and was adopted as ISO/IEC 40500:2025; WCAG 3.0 is a working draft.
- The European Accessibility Act has applied since 28 June 2025; EN 301 549 is being updated to WCAG 2.2; the US Department of Justice's ADA Title II web rule sets compliance dates in 2026 and 2027.
- APCA is not part of WCAG 2.x.
- Unicode 17.0 was released in September 2025; CLDR 48 and ICU 78 are current; ICU MessageFormat 2 was finalized in 2025.
- The EU Cyber Resilience Act's reporting obligations apply from 11 September 2026 and its main obligations from 11 December 2027, with a lighter regime for open-source stewards.
- SPDX 3.0 and the REUSE specification 3.3 are current.

## Questions

### Priority

1. Accessibility:
   - WCAG 2.2's success criteria new since 2.1, and WCAG 3.0's status
   - legal requirements today: the EAA, the current EN 301 549 version, the ADA Title II rule dates, Section 508
   - ARIA 1.2 and 1.3, and the ARIA Authoring Practices Guide
   - testing tools with current versions: axe-core, Lighthouse, Pa11y, Accessibility Insights, screen readers
   - accessible documents (Word, PDF/UA-2) and data visualizations
2. Colour and contrast: WCAG 2.2's contrast requirements for text and for non-text elements, APCA's status, and tools that compute contrast.
3. Internationalization:
   - Unicode 17 (or current), UTF-8 everywhere, normalization, grapheme clusters
   - current CLDR and ICU versions; ECMAScript Intl and Temporal
   - time zones: the IANA tz database, storing UTC, daylight-saving pitfalls
   - formatting numbers, dates and currency; right-to-left layout (CSS logical properties)
   - pluralization and ICU MessageFormat 2; gettext and Fluent; locale-aware sorting
4. Privacy for developers:
   - data minimization, personal data in logs, retention, pseudonymization, privacy by design
   - GDPR basics for developers; an overview of US state privacy laws (how many are in force in 2026); cookie consent
   - the EU AI Act's obligations timeline relevant to software teams, and any 2025-2026 changes
5. The EU Cyber Resilience Act: its dates; who counts as a manufacturer and who as an open-source steward; vulnerability reporting obligations (ENISA's single reporting platform); SBOM requirements; and what, if anything, a small open-source project that publishes skills and tools must do.

### Standard

6. Licensing compliance:
   - SPDX licence expressions and SPDX 3.0; the REUSE specification (current version) and the reuse tool
   - licence compatibility (Apache-2.0 with GPL-2.0, GPL-3.0, MIT, BSD and MPL)
   - third-party notices practice; DCO versus CLA; OpenChain (ISO/IEC 5230)
   - the copyright status of AI-generated code: the US Copyright Office's 2025 report, Part 2, and court rulings through 2026
7. Security policy files: security.txt (RFC 9116), SECURITY.md, coordinated disclosure norms (ISO/IEC 29147 and 30111), CVE numbering for small projects (GitHub as a CNA).
