---
name: agent-engineering
description: "TODO(new-skill) Draft: Runs and audits AI agent sessions that review each other's work across two repositories: rounds, close conditions, messages, and where agents must stop for a person."
license: Apache-2.0
metadata:
  reviewed: "TODO(new-skill) the date of its review, YYYY-MM-DD"
---

# Agent engineering

TODO(new-skill) One paragraph: the situations that load this skill, and which neighboring skill takes
what it doesn't. Draft scope: building agents and their context, and running agent sessions that
work together. Its first module is `review-loops`; `skill-builder`, `agent-context-files` and
`ai-agent-security` follow, as the roadmap plans.

## What applies to every module

TODO(new-skill) The rules every request here meets, whichever module it reads, each in a line or two.

## Modules

Read the module that fits the request, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources.

| Module | Read it for |
|---|---|
| [`review-loops`](references/review-loops.md) | TODO(new-skill) Draft: two agent sessions in two repositories reviewing each other in rounds: setting up, writing messages, closing a round, and stopping for a person |

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
