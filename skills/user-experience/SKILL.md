---
name: user-experience
description: "Reviews, designs and tests how a desktop or web program behaves for its user: status and feedback, windows and dialogs that appear when they should, settings and options, and GUI tests. Use when building, reviewing or testing an interface."
license: Apache-2.0
metadata:
  reviewed: "2026-11-11"
---

# User experience

How a program behaves for the person using it: whether its status is current, whether its
windows and dialogs appear when they should and nowhere else, whether its settings are easy to
find and mean one thing each, and how to test all of that. It serves power-user programs as well
as simple ones: it never trades away a useful option to make a screen shorter. How the interface
looks (themes, palettes, charts) and accessibility belong to `visual-design`, and what people do
at work around a program to `human-factors`; the code itself to `coding`, and general test
design to `testing`.

## What applies to every module

These summarize the modules; each module holds the cases, the checks and the reasons, so read
the one that fits before answering.

1. **Follow the platform's guidelines,** GNOME's, KDE's, Apple's or Microsoft's, over a
   toolkit's defaults or a habit from another platform. The platforms set the rules; toolkits
   implement them.
2. **What the screen says is true now.** A status, a device list or a verdict that outlives the
   state it describes is a defect, not a cosmetic issue.
3. **Nothing appears that the person didn't ask for or can't see.** No window before it's
   ready, no dialog out of nowhere, none hidden behind another.
4. **Keep every useful option, and make the common path short:** good defaults, presets, and
   advanced options one step away.
5. **Prefer undo to a confirmation dialog** for anything that can be undone.
6. **Check behavior by running the program,** or with a test that drives it. Reading the code
   finds candidates; it can't show timing, stacking or focus.

## Modules

Read the module that fits the request, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources.

| Module | Read it for |
|---|---|
| [`usability-review`](references/usability-review.md) | Reviewing a program for what would confuse or annoy its users, with severity ratings; status and feedback that stay current; error messages; preventing and undoing destructive actions; making frequent actions faster for experts without removing options |
| [`windows-and-dialogs`](references/windows-and-dialogs.md) | When a window or dialog should appear; modality, parents and focus; default buttons; one dialog at a time (Qt, GTK, WinUI's ContentDialog, Apple); nothing hidden behind another or shown before it's ready; reviewing dialog code; long operations |
| [`settings-and-options`](references/settings-and-options.md) | Defaults and presets, progressive disclosure, hiding or graying out an option that doesn't apply, each setting in one place with one meaning, an inventory of every setting, how many choices is too many, and power users' options |
| [`gui-testing`](references/gui-testing.md) | Driving a GUI from tests per toolkit (Qt, GTK, web, Windows), catching windows that appear wrongly or status that goes stale, and testing with people |

## When something here is wrong

If the person says advice here is wrong, out of date, failed or doesn't fit, answer their
problem first. Then say in one sentence whether the fault looks like this skill's, and why: a
fact past its check-by date, an example that fails, two rules that disagree, or a case the skill
doesn't cover. If the fault is elsewhere, such as their setup, say that instead.

When the fault is the skill's own, draft a full report they can paste as a new issue at
https://github.com/rmccann-hub/claude-code-skills/issues.
Give the skill and module, the plugin's version or the skill's date in its frontmatter, their
request word for word, the line of the skill that misled, what happened, what's right with its
source, and the fix you'd suggest. Leave out their private data, company detail and repository
names. File it only if they ask you to.
