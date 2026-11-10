# RESEARCH RUN R27: User experience: GUIs that work, are easy to use and are clear

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 10 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 10 November 2026.

This run informs: a planned `user-experience` skill: usability review, windows and dialogs,
settings and options, and testing a GUI.

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
   PROJECT-BOOTSTRAP-AND-AUDIT v0.49.0, in its section of dated facts. Checking them also
   checks that standard, so say plainly when one is wrong.

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R27 · FORM: research-result v1
Save as: R27-RESULT.md
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

- Nielsen's ten usability heuristics (visibility of system status, match with the real world,
  user control, consistency, error prevention, recognition rather than recall, flexibility,
  minimal design, error recovery, help) are still the standard checklist for a heuristic review.
- A status line or panel that keeps showing the last result while a new operation runs breaks
  "visibility of system status".
- Too many options in one place (choice overload) slows people and raises errors; progressive
  disclosure, good defaults and presets are the usual remedies.
- A setting belongs in one place; the same choice offered in several dialogs drifts.
- Desktop toolkits (Qt, GTK, WinUI, Cocoa) each publish human interface guidelines for dialogs,
  modality and window behaviour: GNOME HIG, KDE HIG, Apple HIG, Microsoft's Windows app design.
- A window shown before it's ready, a modal dialog hidden behind another window, and dialogs
  stacked several deep are common desktop defects.
- GUIs can be tested automatically through accessibility interfaces (AT-SPI on Linux, UI
  Automation on Windows, the macOS accessibility API), with toolkit test helpers such as
  pytest-qt or Qt Test, and on the web with Playwright.

## Questions

### Priority

1. **Heuristic review:** the current form of Nielsen's heuristics and of other review methods
   (cognitive walkthrough, Shneiderman's golden rules), how to run one, how many reviewers find
   how much, and severity ratings. Cite the originals and current updates.
2. **Windows and dialogs on the desktop:** what the GNOME, KDE, Apple and Microsoft guidelines
   say about modality, when to show a window, focus, z-order, dialogs on top of dialogs,
   progress for long operations, notifications, and confirming destructive actions. Quote each
   rule and note where they disagree.
3. **Settings and options:** guidance and evidence on defaults, progressive disclosure, presets,
   "advanced" sections, how many choices is too many (choice overload and its replication
   record), and keeping each setting in one place.
4. **Status and feedback:** showing what the program is doing and what it found: stale status,
   long operations, results that must not mislead (a verdict word such as "OK" over a failure),
   and error messages a user can act on.
5. **Testing a GUI:** automated tests through accessibility interfaces (AT-SPI, UI Automation),
   toolkit helpers (pytest-qt, Qt Test, GTK's test tools), Playwright for web; screenshot and
   visual regression tests; what each can and can't catch. Current versions and release dates.

### Standard

6. **Testing with people:** task-based usability tests, how many participants, think-aloud,
   first-run tests, and measuring task success and time (SUS and its current use).
7. **Power users:** keyboard shortcuts, scripting, dense layouts, and how expert-oriented
   programs stay learnable (the guidelines and the evidence).
8. **Mistakes AI assistants make building GUIs:** documented patterns such as dialogs for
   everything, options added instead of decisions made, missing states (empty, loading, error).
9. **Accessibility basics every GUI review checks,** with a pointer to WCAG 2.2 and the
   platform guidelines; full accessibility is another run (R18).
