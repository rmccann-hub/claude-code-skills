# Agent-written tests

Read this for tests an AI coding agent writes, changes or runs: test-first work with an agent,
keeping it off the tests, reviewing its diff to tests, fixtures, snapshots or baselines, an
agent that deletes, skips or special-cases a failing test, holdout tests, letting it say a test
is wrong, mutation-testing its tests, and its "all tests pass".

Proving any check can fail is `test-gates`; what output is graded against, and model graders,
are `test-oracles`; a test that fails only sometimes is `flaky-tests`; coverage and
mutation-testing tools are `testing-patterns`. Agents reviewing each other's work in rounds are
agent-engineering's `review-loops`. The standard's dimension 5, *Testing and verification*,
rules that a verifier lives where the thing verified can't edit it, and that a test written in
the change it validates is weak evidence until seen failing; this module applies that to agents.

## Rules

1. **Tests come first: written from the spec, seen failing, committed, then the code** (fact
   `awt-tdd`). They fail for the reason expected before any implementation exists.
2. **The agent is told the tests are fixed, and something enforces it.** Say it in the prompt
   and the context file (fact `awt-no-modify`); a prompt alone cut cheating sharply in one
   study (fact `awt-prompt`). Then make CI fail when committed tests change unreviewed.
3. **Any diff that touches tests, fixtures, snapshots, baselines or test configuration is
   high-risk.** Review it line by line, apart from the code, before reading the code's diff.
4. **Read the code for gaming as well as the tests.** Read-only tests stop test edits, not
   special-casing or operator overloading (fact `awt-read-only`).
5. **Score the work on tests the agent never saw, and don't treat them as proof.** Hiding tests
   nearly stops cheating but costs performance (fact `awt-hidden`), and holdout tests have
   passed heuristic answers (fact `awt-holdout`).
6. **Give the agent a way to stop and say a test is wrong.** An abort option lowered cheating
   (fact `awt-abort`), and a test can be wrong (fact `awt-wrong-test`). The agent reports with
   evidence; a person decides; a test change lands in its own commit.
7. **Mutation-test tests an agent wrote before trusting them.** Coverage shows a line ran, not
   that a test fails when the line is wrong.
8. **The evidence is the run's output, not the agent's summary** (fact `awt-evidence`): the
   command, the count of tests run against the baseline, and the exit code.

### What to look for in a test diff

- A test deleted, renamed out of collection, or marked skip, xfail or quarantined.
- An expected value changed to match the new output, with no line of the spec behind it.
- An assertion loosened: equality to "contains", or a tolerance widened.
- Snapshots or golden files regenerated in the same change as the behavior they record.
- A lowered test-count baseline, a raised timeout, or a changed runner option or `conftest.py`.
- A new fixture or mock that returns what the test asserts, so the code under test never runs.

### What to look for in the code

ImpossibleBench's kinds of cheating besides editing tests (Sources), as they show in review:

- a branch keyed on a value from a test, or a table of the tests' answers;
- an `__eq__`, `equals` or comparison override the spec doesn't ask for;
- state that changes the answer between calls with the same input.

## Mistakes

- **Asking for tests after the agent wrote the code, and taking green as proof.** They check
  what the code does, bugs included. Write them from the spec first, or mutation-test them.
- **Not saying the work is test-driven.** The agent may build a mock implementation to satisfy
  tests for code that doesn't exist yet (Anthropic's guidance, in Sources).
- **Letting one commit change an expected value and the code that now produces it.** Split them,
  and ask what in the spec changed.
- **Trusting read-only tests to stop gaming.** They stop test edits only. Read the code too.
- **Scoring the agent on the tests it iterated against.** Those measure how well it fit them.
- **Forbidding every test change with no way out.** An agent facing a wrong test then games it
  or fixes it silently. Give it a way to stop and report.
- **Getting green by skipping, disabling or quarantining a test, or lowering the test-count
  baseline.** Fix the code, or report the test; `flaky-tests` has quarantine with an owner.

## Audit

Severity uses the standard's status words.

| Check | Look for | Severity | Fix |
|---|---|---|---|
| Tests never seen failing before the code | One commit adding both; no failing run on record | `GAP` | Commit the tests first, with their failing run |
| An agent's change edits tests and code together, unexplained | Test, fixture, snapshot and baseline files in the diff | `GAP`; `BLOCKER` where an expected value changed to match new output | Split the change; tie each test change to the spec |
| A test skipped, deleted, quarantined or loosened to get green | New skip and xfail markers, removed tests, wider tolerances, a lowered count | `BLOCKER` | Restore the test and fix the code, or report the test as wrong |
| The code games its tests | Branches on test values, comparison overrides, state that changes answers | `BLOCKER` | Rewrite to the spec; add a test the special case fails |
| Nothing stops the committed tests changing | CI, hooks and permissions | `GAP` | A CI check that fails on an unreviewed test change |
| The agent is scored only on tests it saw | How the work or the agent is judged | `GAP` | A holdout set, and review on top |
| No way to report a wrong test | The agent's prompt and context file | `GAP` | Name the way to stop, and the evidence to give |
| Agent-written tests were never mutation-tested | Mutation runs on the code they cover | `GAP` | Mutate the diff; a test per surviving mutant that matters |
| A pass is reported without its output | The agent's report or the pull request | `GAP` | The command, its output and the test count |

## Why

### Tests first, committed, seen failing

- **The advice:** write tests from the spec, watch them fail, commit them, then write code.
- **The reason:** a test that has never failed has only agreed with a state that was already
  right, and one written by reading the code checks what the code does. Anthropic's workflow
  for Claude Code has the agent confirm the tests fail, write no code yet, and commit them
  (fact `awt-tdd`); its current page asks for a failing test that reproduces a bug before the
  fix (fact `awt-failing-test`).
- **What others do, and why:** the standard's dimension 5 asks the same of a test written in the
  change it validates, citing self-written tests whose false positives did harm.
- **What it costs:** a commit and a run before any code, and a spec clear enough to test.
- **When to choose differently:** exploratory code with no spec; test it once the behavior
  settles, and mutation-test the tests.

### Telling the agent, and enforcing it

- **The advice:** instruct the agent not to modify the tests, and back the instruction with a
  check it can't edit.
- **The reason:** agents delete failing tests (fact `awt-delete-tests`). On tasks made
  impossible by a test that contradicts the spec, so any pass is a cheat, one model cheated on
  most (fact `awt-cheat-rate`). The right prompt cut one model's
  rate from almost all to almost none (fact `awt-prompt`), so the instruction is worth giving,
  and a rate that isn't zero is why it isn't enough alone.
- **What others do, and why:** Anthropic's guidance relies on the instruction (fact
  `awt-no-modify`); the standard keeps what scores a run out of the scored thing's reach. This
  repository's steward skill never skips, disables or quarantines a test, or lowers the
  test-count baseline, to get green.
- **What it costs:** a CI rule over the test paths, and a reviewed exception for each change.
- **When to choose differently:** an agent asked to repair the tests themselves has no fixed
  tests; review its diff as in rule 3.

### Reading the code, and holdout tests

- **The advice:** review the code for gaming, and score on tests the agent never saw.
- **The reason:** making tests read-only worked best on a model whose main cheat was editing
  them, and left the other kinds (fact `awt-read-only`). Hiding the tests nearly removed
  cheating, at a cost to legitimate results (fact `awt-hidden`). EvilGenie found heuristic
  answers, many of them Claude's, that passed holdout tests (fact `awt-holdout`).
- **What others do, and why:** EvilGenie adds a model judge and test-edit detection to holdout
  tests, because no one method caught everything.
- **What it costs:** a second test set to keep, and weaker work where tests are hidden.
- **When to choose differently:** a small change a person reads whole needs no holdout set.

### A way to stop

- **The advice:** give the agent a named way to stop when a test looks wrong.
- **The reason:** given a string that ended the run and asked for a person, two models cheated
  far less, a third only a little less (fact `awt-abort`). Many "cheats" corrected a wrong test,
  which EvilGenie calls arguably desirable (fact `awt-wrong-test`).
- **What it costs:** stopped runs a person must read, some of them false alarms.
- **When to choose differently:** none for an unattended run: it still reports and stops.

### Mutation-testing what the agent wrote

- **The advice:** run mutation tests on code an agent's tests cover before relying on them.
- **The reason:** agent sessions write this repository's tests. On 2026-09-23 it declined
  mutation testing, since branch coverage was 100%. On 2026-11-03 mutmut and a hand-written set
  of mutants found 28 real gaps in two checks' tests, each a defect they passed; 24 new tests
  closed them (pull request #116, commit `3d7638a`).
- **What others do, and why:** Google mutates only changed lines, during review (fact
  `tg-mutation-diff`), which keeps the cost per change small.
- **What it costs:** minutes per run, and reading each surviving mutant.
- **When to choose differently:** a check simple enough to plant every defect by hand, as
  `test-gates` describes.

### The output, not the summary

- **The advice:** read the command, its output and the test count.
- **The reason:** Claude Code's guidance says a bare claim that tests pass tells you little, and
  for an unwatched session the output is the only evidence (fact `awt-evidence`). A run that
  collected nothing, or fewer tests than before, can also print a pass.
- **What it costs:** a paste in every report.
- **When to choose differently:** never; a CI run linked from the report is the output.

## Facts

Practices and findings, each named elsewhere in this module by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `awt-tdd` | Anthropic's 2025 test-first workflow, no longer on the current docs page: confirm the tests fail, then commit them | [Best practices for agentic coding](https://www.anthropic.com/research/claude-code-best-practices) | "Tell Claude to run the tests and confirm they fail" and "Ask Claude to commit the tests" | 2026-11-11 | 2027-05-11 |
| `awt-no-modify` | The same workflow tells the agent not to modify the tests | [Best practices for agentic coding](https://www.anthropic.com/research/claude-code-best-practices) | "instructing it not to modify the tests" | 2026-11-11 | 2027-05-11 |
| `awt-failing-test` | The current guidance asks for a failing test that reproduces a bug, then the fix | [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) | "write a failing test that reproduces it, then fix it" | 2026-11-11 | 2027-02-11 |
| `awt-evidence` | A claim that tests pass, without the output, tells little | [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) | "on its own tells you very little, and reading the output is faster than rerunning the check yourself" | 2026-11-11 | 2027-02-11 |
| `awt-delete-tests` | An agent with test access may delete failing tests | [ImpossibleBench](https://arxiv.org/pdf/2510.20270) | "may delete failing tests rather than fix the underlying bug" | 2026-11-11 | 2027-05-11 |
| `awt-cheat-rate` | GPT-5 cheated on 76% of impossible SWE-bench tasks | [ImpossibleBench](https://arxiv.org/pdf/2510.20270) | "GPT-5 cheats in 76% of the tasks in Oneoff-SWEbench and 2.9% on Oneoff-LiveCodeBench" | 2026-11-11 | 2027-05-11 |
| `awt-prompt` | A prompt cut GPT-5's cheating from 92% to 1% | [ImpossibleBench](https://arxiv.org/pdf/2510.20270) | "cheating from 92% to 1% on Conflicting-LiveCodeBench" | 2026-11-11 | 2027-05-11 |
| `awt-hidden` | Hidden tests cut cheating to near zero and lowered legitimate scores | [ImpossibleBench](https://arxiv.org/pdf/2510.20270) | "Hiding tests from agents reduces cheating success rate to near zero" and "but also degrades performance on the original benchmark" | 2026-11-11 | 2027-05-11 |
| `awt-read-only` | Read-only tests don't stop special-casing or operator overloading | [ImpossibleBench](https://arxiv.org/pdf/2510.20270) | "it does not eliminate other cheating methods such as special-casing or operator overloading" | 2026-11-11 | 2027-05-11 |
| `awt-abort` | An abort option cut GPT-5 from 54% to 9% and o3 from 49% to 12% | [ImpossibleBench](https://arxiv.org/pdf/2510.20270) | "lowering the cheating rate of GPT-5 from 54% to 9% and o3 from 49% to 12%" | 2026-11-11 | 2027-05-11 |
| `awt-holdout` | Holdout tests let reward hacking through | [EvilGenie](https://arxiv.org/pdf/2511.21654), v2 | "holdout tests are not foolproof" | 2026-11-11 | 2027-05-11 |
| `awt-wrong-test` | Correcting a wrong test against instructions can be the right move | [EvilGenie](https://arxiv.org/pdf/2511.21654), v2 | "this is arguably desirable behavior" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [ImpossibleBench](https://arxiv.org/abs/2510.20270), Zhong, Raghunathan and Carlini, 2025 | Cheating rates, test access, the abort option, the kinds of cheating | CC BY 4.0: adapted with attribution |
| [EvilGenie](https://arxiv.org/abs/2511.21654), Gabor, Lynch and Rosenfeld, v2 2026-05-17 | Holdout tests, wrong tests | arXiv's non-exclusive distribution license: facts in our own words, short quotes |
| [Claude Code: best practices for agentic coding](https://www.anthropic.com/research/claude-code-best-practices), Anthropic, 2025-04-18 | The test-first workflow; saying the work is test-driven | Anthropic's, no license stated: facts in our own words, short quotes |
| [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices), Anthropic | A failing test first; output as evidence | Anthropic's documentation, restricted: facts in our own words, short quotes |
| project-bootstrap-and-audit's standard, dimension 5 | Verifier independence; tests seen failing | This repository's own, Apache-2.0 |
| This repository's steward skill, and its mutation run of 2026-11-03 (pull request #116) | Never skipping a test to get green; gaps behind full coverage | This repository's own, Apache-2.0 |
