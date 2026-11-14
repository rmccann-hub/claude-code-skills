# RESEARCH RUN R30: From user issues to fixes

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 14 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 14 November 2026.

This run informs these categories: user-experience (a planned feedback-loop module), testing (visual regression), logging-and-observability (crash and usage data), and the issue and triage advice in git-workflows.

## What this run is for

The repository's skills say how to build and review an interface, but not how a team learns
what's wrong with it once people use it, or how to build it so a fix is quick and safe. This
run covers the loop: collecting feedback, crash reports and usage data with consent; turning
them into issues a developer can act on; triaging them; and code and tests that let a team
change an interface without breaking the rest. It serves small internal tools as well as
public products.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R30 · FORM: research-result v1
Save as: R30-RESULT.md
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

- An in-app "report a problem" that attaches the version, the screen and recent log lines gets
  more actionable reports than an email address.
- Crash reporting (Sentry, Crashpad, Windows Error Reporting, Apple's crash reports) needs
  symbol files kept per release to be readable.
- Usage analytics in the EU need consent unless strictly necessary (ePrivacy Directive Article
  5(3)), and many open-source desktop programs make telemetry opt-in.
- Visual regression tests (Playwright screenshots, Chromatic, Percy) catch unintended layout
  changes, at the cost of flaky diffs from fonts and rendering.
- Keeping view code apart from state and logic (MVVM, MVU, presenter patterns) makes interface
  changes cheaper and testable.

## Questions

### Priority

1. **Collecting feedback in the product:** published practice on in-app feedback and bug-report
   forms (what to attach automatically: version, OS, screen, recent logs, a screenshot with the
   user's say), issue forms (GitHub issue forms' current syntax), and getting reports from
   people who won't file an issue (internal tools on a local network included).
2. **Crash reports and usage data:** current crash-reporting tools per platform and runtime
   (Sentry, Crashpad and Breakpad, Windows Error Reporting, Apple, Qt, .NET, Python), symbols
   per release, and opt-in usage data: what GDPR and the ePrivacy Directive require, what
   well-known open-source programs do (VS Code, Firefox, KDE, GNOME), and OpenTelemetry for
   client apps, with versions.
3. **Triage:** published practice on severity against priority for UX issues (NN/g's severity
   ratings, bug-triage guides from large open-source projects), labels, reproducing a report,
   duplicates, and closing the loop with the reporter.
4. **Building an interface to change:** separating view from state and logic (MVVM, MVU/Elm,
   presenters) per toolkit (WPF and WinUI, Qt, GTK, React, SwiftUI), strings and settings in
   one place, feature flags for interface changes (OpenFeature's status), and what the sources
   say each costs.

### Standard

5. **Visual regression testing:** Playwright's screenshot assertions, Chromatic, Percy, Qt and
   GTK reference tests; handling fonts and anti-aliasing; versions.
6. **Measuring whether a fix helped:** task success, time on task, error rates, support tickets,
   and A/B testing's limits for small user bases.
7. **Release notes and telling users what changed,** from published guidance.
8. **Common mistakes,** including what AI coding assistants get wrong fixing interface bugs
   (fixing one screen and not its siblings, no test for the regression), with sources.
