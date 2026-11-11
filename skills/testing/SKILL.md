---
name: testing
description: "Writes, reviews and fixes tests: doubles, coverage, frameworks, checks that can fail, oracles, flaky tests, tests AI agents write, and acceptance runs on hardware. Use when writing tests, or when tests pass but the output is wrong."
license: Apache-2.0
metadata:
  reviewed: "2026-11-11"
---

# Testing

How to make a test, a CI gate or a grader worth trusting: one that can fail, checks against
something that didn't produce the output, and is scored by what it misses. It comes from audits
of repositories whose suites and acceptance runs were green while their output was wrong. CI
triggers, required checks and how long CI takes belong to `git-workflows`; the standard's
dimension 5 sets the rules for a repository's gates, and this skill says how to meet them. A GUI's
tests are `user-experience`.

## What applies to every module

These summarize the modules; each module holds the cases, the fixes and the reasons, so read
the one that fits before answering.

1. **A check you've only seen pass proves nothing yet.** See it fail on the defect it exists to
   catch before trusting its pass.
2. **"Couldn't check" is a failure,** never a pass: a missing input, an empty range or a tool
   that isn't there.
3. **Check output against something that didn't produce it,** and read that reference's own
   settings before trusting a match.
4. **Count what's wrong and reported as fine.** A pass rate hides the one result that matters.
5. **A failure that comes and goes is a defect,** in the test or the program, until shown
   otherwise. Never weaken, skip or re-run a test until it passes.
6. **Assert the invariant, not today's output.** A test that copies the current result checks
   only that nothing changed.

## Modules

Read the module that fits the request, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources.

| Module | Read it for |
|---|---|
| [`test-gates`](references/test-gates.md) | Proving a test, CI gate, script, checker or eval grader can fail: the parent commit, a planted defect, a script that exits 0 on missing input, a grader that passes without the plugin, tests that pass locally and fail in CI, mutating the checker |
| [`test-oracles`](references/test-oracles.md) | What a result is checked against: golden files, independent references and their settings, recorded real samples, eval baselines with and without (every case scoring 1.0), LLM graders, and scoring by the worst case |
| [`flaky-tests`](references/flaky-tests.md) | A test that passes and fails on the same code, on re-run: finding the cause, races in the program, retries, quarantine with an owner and a deadline, keeping a fixed flake fixed. A test that times out because CI is slow is `git-workflows`' `ci-speed` |
| [`testing-patterns`](references/testing-patterns.md) | Writing a test suite: coverage targets and gates, test doubles and adapters, contract tests with Pact, runner settings that let an empty or skipped run pass, property-based and mutation tools, and each language's framework and version |
| [`agent-written-tests`](references/agent-written-tests.md) | Tests an AI coding agent writes, changes or runs: tests first and seen failing, the agent told not to touch them, test diffs reviewed as high risk, gaming by special-casing, holdout tests, a way for the agent to stop, and mutation-testing what it wrote |
| [`acceptance-runs`](references/acceptance-runs.md) | Unattended acceptance runs on real hardware: a health check before the run, a device lost mid-run, rig failures told from product failures, retries, run tiers, the evidence a run keeps; fault injection for disk, memory and network faults on Linux, Windows and macOS |

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
