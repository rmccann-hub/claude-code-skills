# RESEARCH RUN R29: Modern interfaces and consistency

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 14 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 14 November 2026.

This run informs these categories: user-experience (a planned interface-patterns module, and command-line-interfaces), visual-design (visual-theme: components beyond tokens).

## What this run is for

R27 built the `user-experience` skill: heuristic review, windows and dialogs, settings and
options, and GUI tests. R20 (tokens, colour, typography, charts) and R18 (accessibility,
internationalization) cover how an interface looks and who can use it. Neither says what a
current interface on each platform is built from, how a team keeps many screens consistent,
or how a command-line program should behave. This run covers that, for desktop, web and
terminal programs, including tools a few people use every day at work. Don't repeat R27's
heuristics or R20's tokens and colour.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R29 · FORM: research-result v1
Save as: R29-RESULT.md
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

- Each platform publishes a current design language: Microsoft's Fluent 2 (with WinUI 3),
  Google's Material 3 (with Material 3 Expressive, 2025), Apple's Human Interface Guidelines
  (with Liquid Glass, 2025), GNOME's Human Interface Guidelines (libadwaita) and KDE's.
- A design system is tokens plus components plus usage guidance; consistency comes from reusing
  components, not from copying styles.
- clig.dev (Command Line Interface Guidelines) is the most cited guide to command-line UX, and
  GNU's and POSIX's argument conventions still hold.
- A skeleton screen feels faster than a spinner for loads of a few seconds.
- Empty states should say what goes there and how to add the first item.

## Questions

### Priority

1. **Platform design languages today:** for Fluent 2, Material 3, Apple's HIG, GNOME's HIG and
   KDE's, the current version or date, what changed in 2025 and 2026, the toolkit or component
   library that implements each (WinUI 3 and the Windows App SDK, Fluent UI React, Material
   Web and Jetpack Compose, SwiftUI, libadwaita, Kirigami) with versions, and where they agree
   and disagree on navigation, layout, density and window sizes.
2. **Consistency at scale:** what a design system holds (tokens, components, patterns, usage
   rules, content guidelines), published systems worth learning from (GOV.UK Design System,
   USWDS, Carbon, Primer, Atlassian), how teams keep screens consistent (one component per
   pattern, an inventory of screens and components, lint rules and Storybook-style catalogues,
   visual regression), and what the sources say goes wrong when a team skips this.
3. **Layout, forms and states:** responsive and adaptive layout for desktop and web (window
   sizes, breakpoints, high-DPI and scaling), form design (labels, inline validation, required
   fields, error placement, from GOV.UK, NN/g, Baymard and platform guides), and the states every
   screen needs: empty, loading (skeletons, progress, optimistic updates), partial, error and
   offline, with the evidence behind each.
4. **Command-line interfaces:** clig.dev, GNU's and POSIX's argument conventions, `--help` and
   man pages, exit codes, output for people against output for programs (`--json`, colour only
   on a terminal, `NO_COLOR`), progress and quiet modes, confirming destructive commands, and
   the current argument-parsing libraries per language (argparse, Click, Typer, clap, cobra,
   System.CommandLine, commander), with versions.

### Standard

5. **UX writing:** labels, buttons, microcopy and error text, from Microsoft's, Google's,
   Apple's, GNOME's and GOV.UK's content guides, and NN/g.
6. **Keyboard-first and power users:** command palettes, shortcut conventions per platform, and
   type-ahead, from the platforms' guides.
7. **Onboarding and change:** first-run experience, what's-new notices, and changing a familiar
   layout without losing people (feature tours, gradual rollout, keeping the old way for a time),
   with evidence.
8. **Common mistakes,** including those AI coding assistants make when building interfaces
   (only the happy path, inconsistent components, invented platform APIs), with sources.
