---
name: human-factors
description: "Finds what a habit, workaround, double check or familiar tool in people's work is for before a redesign, automation or optimization removes it, and plans the change. Use when changing what people do; never to bend a factual finding."
license: Apache-2.0
metadata:
  reviewed: "2026-11-11"
---

# Human factors

For an agent about to change what people do: redesigning a process, automating a manual step,
optimizing a workflow or replacing a tool. People keep habits that look odd or wasteful from
outside, such as a double check, a shadow spreadsheet, a familiar slower tool or a bent rule.
Some serve a purpose, some are bias, and some are drift. This skill finds which before the
change removes it, and designs with it. It's loaded only for design, automation and
optimization work, never for research, retrieval or checking facts. People in plans and
schedules, such as fatigue, shifts and utilization, belong to `optimization-and-scheduling`;
interfaces to `user-experience`; checking a fact or result to `testing`.

## What applies to every module

These summarize the modules; they hold the cases, the checks and the reasons, so read the one
that fits before answering.

1. **Find what a step is for before removing or automating it:** watch the work as done, and
   ask the people who do it.
2. **Familiarity is not a reason by itself.** Test each habit: purpose, bias or drift.
3. **Plan a change as keep, change gradually or override,** and budget for a dip of months
   after a tool change, with no promise of recovery.
4. **Automate so people can still take over,** keeping their skill and calibrating their trust.
5. **Human factors never alter a fact.** Findings, measurements and quotes stay as found, and
   each output is marked Evidence or Recommendation.
6. **Say how strong and how general the evidence is:** most of it is from Western samples, and
   some of it is a position, not a measurement.

## Modules

Read the module that fits the request, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources.

| Module | Read it for |
|---|---|
| [`human-factors`](references/human-factors.md) | Removing, automating or redesigning a step people take: what a habit, workaround, double check or familiar tool is for, purpose versus bias or drift, keep or change or override, the dip after a tool change, take-over skill and trust in automation, and keeping facts apart from preferences |
| [`studying-work`](references/studying-work.md) | Finding out what a step is for: watching and interviewing people at their work, breaking a task into goals and plans and how deep to go, why asking alone misses purposes, a check that caught nothing while watched, and the traps that bend a study |

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
