# Test gates

Read this for proving that a test, a CI gate, a checker, a scanner or an eval grader can fail
before you trust its pass: the parent commit, a planted defect, the "couldn't check" path,
mutating the checker, a grader that passes without the thing it grades, a test that pins
today's state, a local command that differs from CI's, or a regression test that misses the
wiring it was written for.

What a result is checked against, independent references and scoring a tool by its worst case
are `test-oracles`; a test that fails only some of the time is `flaky-tests`. CI triggers,
required checks, timeouts and the completion guard are `ci-workflows`, and how long CI takes is
`ci-speed`, both in the git-workflows skill. Test strategy, doubles, fixtures, coverage and
mutation-testing tools are the planned `testing-patterns` module.

## Rules

1. **A check you've only seen pass has only been seen agreeing with a state that was already
   right.** Before trusting a test, gate, checker, scanner or grader, watch it fail against the
   state it exists to catch, by the cases below.
2. **Every way it couldn't check is a failure.** Missing input, an unknown ref, an empty range
   or a tool not installed ends in a non-zero exit that names the cause, not a pass over
   nothing. A sweep over a population asserts a minimum count.
3. **It reads every value its input states, whole.** A value it never reads, or compares cut
   short, is decoration. It never compares a value with one derived from itself.
4. **Mutate the checker, not only the product.** A change to a gate, a grader or an assertion
   is tried with its key condition weakened, and each fix is reverted once to show its test
   fails.
5. **A grader that can't fail without the thing it grades doesn't count toward the score.**
   It's reported as a sign the thing ran, apart from the score.
6. **Assert the invariant, not today's state, on the path the rule governs.** A rule about
   releases runs where releases are made.
7. **Check the fact, not a symptom the failure path shares.** When one check is re-keyed onto
   the fact, re-key every sibling that reads the same symptom.
8. **The command typed locally matches CI's:** the same entry point, import path and compiler
   flags.
9. **A gate picks its subject by what the subject states, never by sort or directory order.**
10. **A scripted edit with several parts asserts that each part landed.**
11. **Find the call site before believing a documented capability, and test a wiring fix
    through the production entry point.**

### Cases to try on every check

- **The parent commit.** A check written in the same change as what it guards has never seen
  the state before that change. `git worktree add ../before HEAD~1`, run the check there, and
  it should fail. It's the cheapest case, and always available.
- **A planted defect.** Break what it guards three ways: remove it, reorder it so it runs too
  late, and disable it where it stands. The check should fail each time. One that matches text
  passes on a comment naming the thing, which the disabled case catches.
- **A check that ran and failed.** Feed it a record whose check ran and found a fault. A check
  that asks only whether a check ran passes the failure.
- **Couldn't check.** Take its input away: a missing file, an unknown ref, an empty range, the
  tool it calls not installed. It should fail, saying which.
- **Every value its input states.** Change each value in the checked record by one character,
  one at a time. Each change should fail.
- **A known change, for a summary or diff tool.** It must report one you made.

A planted defect proves something only once it landed: confirm the file changed and the build
succeeded before reading the check's result. Copy what you break first, and restore from the
copy, checked by its hash, not with `git checkout --`, which throws away uncommitted work.

### Four more ways a gate passed its defect

Each gets a planted test of its own (L56):

- **A mangled key in a header.** Plant one: the gate refuses it rather than reading the field
  as absent.
- **A pattern that matches its word inside an unrelated phrase.** Anchor the pattern, and plant
  the phrase.
- **A fixture holding a state the code can never reach.** Build fixtures from states the code
  produces.
- **A test-count baseline taken from a local run** whose collection CI's didn't match. Take the
  baseline from CI's own collection.

### Mutating the checker and the grader

Google mutates only changed code, during code review (fact `tg-mutation-diff`), and leaves out
lines that are uncovered or uninteresting, which it calls arid (fact `tg-arid-lines`). Do the
same to a check's own diff: turn `>=` into `>`, `all` into `any`, delete an assertion, compare
a value with itself. A test of the checker should fail on each. Tools for it are the planned
`testing-patterns` module's.

`claude plugin eval` runs each case with and without the plugin, and leaves out of the score a
grader that can't pass without it, such as one that the skill was invoked (fact
`tg-eval-unscored`). Ask the same of any grader: what does it score when the thing it grades is
absent? If it can only fail then, it's an indicator, not a score.

## Mistakes

- **Writing a gate and its subject in one commit and calling the green run proof.** Run it on
  the parent commit too.
- **A sweep over a computed list with no floor.** An empty list passes. Assert a minimum count.
- **Reading every non-zero exit from a tool the check calls as "nothing found".** Many tools
  exit one way for no match and another for an error. Mixing them up passes a missing file.
- **Comparing the first 16 characters of a hash,** or a cited file with its manifest row while
  never reading the hash beside the citation. A changed hash passes both. Compare every field,
  whole.
- **Comparing an input with the files written from it,** under an option that overwrites the
  field. The two always agree. Compare with what was passed.
- **Asserting today's count, version or file list where the rule is a property.** The test
  blocks unrelated commits and misses the case it's for.
- **Typing `python -m pytest` locally when CI runs `pytest`,** or a bare `gcc` when CI passes
  the project's flags. The local pass doesn't stand for CI's.
- **Taking "the newest file" as whatever a listing shows last.** Read the date or version the
  file states.
- **A regression test that hands the fixed value straight to the function that uses it.** It
  passes while nothing in the app passes the value on. Drive it from the entry point.
- **Believing documentation that a method exists and is used.** `git grep` for its call site.
- **Counting "the skill was invoked" toward an eval's score,** or any grader the without-arm
  can't pass.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A gate or checker has never been seen to fail | Its tests, for the parent commit, a planted defect, a check that ran and failed, and missing input | `GAP`; `BLOCKER` where a merge or release rests on it | A test per case in *Cases to try on every check* |
| The couldn't-check path passes | Run it with the input missing, an unknown ref or an empty range | `GAP`; `BLOCKER` once it has passed having checked nothing | Fail closed, naming what was missing |
| A sweep has no floor | Parameterized tests and loops over a computed list | `GAP` | Assert a minimum count |
| A stated value is never read, or compared cut short | Each field the record states, against what the checker reads | `GAP` | Compare every field, whole |
| A grader passes without the thing it grades, and counts | Each grader, run with the feature or plugin absent | `GAP` | Report it apart from the score (fact `tg-eval-unscored`) |
| A test pins today's state where the rule is an invariant | Asserted counts, versions and lists in tests of a rule | `DRIFT`; `GAP` where the rule's own path goes unchecked | Assert the property, on the path it governs |
| The documented local test command differs from CI's | The command in the context file or README, against the workflow's `run:` step | `GAP` | Make one the other |
| A gate picks its subject by order | `sorted(...)[-1]`, `ls \| tail -1`, an unsorted glob | `GAP` | Select by the date or version the subject states |
| A documented capability has no call site | `git grep` for each documented method | `GAP` | Wire it, or correct the documentation |

## Why

### Seeing it fail

- **The advice:** prove each check against the parent commit, a planted defect, a failed
  record, missing input and every stated value.
- **The reason:** in audited repositories, checks passed what they were built to stop (L31). A
  checker cut two hashes to 16 characters; another never read the hash a record wrote beside its
  citation; a diff tool said "unchanged" over the commit that added a flag, because a row filter
  skipped its row; two probes found tests that couldn't fail. L56 adds four more, listed under
  Rules. Each would have failed one case above.
- **What others do, and why:** project-bootstrap-and-audit's standard, in dimension 5,
  *Testing and verification*, rates gates this way in an audit: prove a gate by mutating what it
  guards, run it against the parent commit, and treat "couldn't check" as a third outcome that
  fails closed. This module is how to do it in the work itself.
- **What it costs:** a worktree checkout, a planted case per check, a count to keep current.
- **When to choose differently:** a check whose failure is plain to see, such as a formatter
  that rewrites the file, needs no planted test. One nothing counts on can wait until something
  does.

### Mutating the checker

- **The advice:** weaken a check's own condition and confirm its test fails.
- **The reason:** a planted defect in the product tests the check against one state; a mutant of
  the check tests whether its test notices the check getting weaker.
- **What others do, and why:** Google runs mutants on the lines a change touches, during review
  (fact `tg-mutation-diff`), and skips arid lines (fact `tg-arid-lines`), so a reviewer sees few
  mutants, each worth reading.
- **What it costs:** a run per mutant, which is why it stays on the diff.
- **When to choose differently:** a checker short enough to read whole, with a planted test per
  case, may skip it.

### Graders

- **The advice:** a grader the without-arm can't pass is reported, not scored.
- **The reason:** it would push the baseline toward zero and inflate the difference the eval
  exists to measure (fact `tg-eval-unscored`).
- **What it costs:** a lower, more honest score.
- **When to choose differently:** a grader that the thing did not happen can fail in either
  arm, so it counts in both.

### Invariants, release paths and symptoms

- **The advice:** assert the property, on the path it governs, and key a check on the fact.
- **The reason:** a unit test that pinned a release rule to the current state blocked every
  commit during a review round, and didn't run on the releases it was for (L7). An acceptance
  step passed an identification because rows had loaded, and they were the placeholders the app
  loads when a lookup finds nothing; a sibling check keyed on the identifier caught it (L1).
- **What it costs:** finding the property, and the release path, which is slower to run.
- **When to choose differently:** a snapshot test pins today's state on purpose, and is read as
  a record of change, not as a rule.

### Local commands, selection order and scripted edits

- **The advice:** run CI's command, choose a subject by what it states, and assert every part of
  an edit.
- **The reason:** `python -m pytest` adds the current directory to `sys.path` and the `pytest`
  script doesn't, and a bare `gcc` passed code the project's flags reject (L8). A gate took
  "the newest verification" from whichever file the directory listed last (L9). One assert
  covered one replacement of a scripted edit while the others did nothing (L10).
- **What it costs:** a slower local run, and an assertion per part.
- **When to choose differently:** a fast local subset is fine when it's named as one and the
  full command runs before a push.

### Call sites and entry points

- **The advice:** grep for the call before believing the documentation, and test a wiring fix
  through the entry point the app uses.
- **The reason:** four cancel methods were documented and never called (L6). Four releases
  claimed a fix whose test handed the value straight to the renderer, while nothing in the app
  passed it on (L5).
- **What it costs:** a slower test through more of the app.
- **When to choose differently:** a unit test of the renderer stays; it just isn't the
  regression test for the wiring.

## Facts

Practices and behavior, each named elsewhere in this module by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `tg-mutation-diff` | Google runs mutation testing on changed code only, during code review | [Practical Mutation Testing at Scale](https://arxiv.org/abs/2102.11378) | "Mutation testing is done incrementally, mutating only changed code during code review, rather than the entire code base" | 2026-11-10 | 2027-05-10 |
| `tg-arid-lines` | Google mutates only changed lines that are covered and not arid, meaning uninteresting | [State of Mutation Testing at Google](https://research.google.com/pubs/archive/46584.pdf) | "Only lines affected by the diff under review that are covered and are not arid are mutated." | 2026-11-10 | 2027-05-10 |
| `tg-eval-unscored` | In a two-arm `claude plugin eval` run, a grader that can't pass without the plugin is left out of the score in both arms | [Plugin evals](https://code.claude.com/docs/en/plugin-evals) | "A check like \"the skill was invoked\" can never pass without the plugin" and "Claude Code excludes such graders from the score in both arms" | 2026-11-10 | 2027-02-10 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Practical Mutation Testing at Scale](https://arxiv.org/abs/2102.11378), Petrović and others | Mutation testing on the diff, at review | arXiv's non-exclusive distribution license: facts in our own words, short quotes |
| [State of Mutation Testing at Google](https://research.google.com/pubs/archive/46584.pdf), Petrović and Ivanković, ICSE-SEIP 2018 | Arid lines | Copyright held by the authors: facts in our own words, short quotes |
| [Claude Code docs: plugin evals](https://code.claude.com/docs/en/plugin-evals) | Graders left out of the score | Anthropic's documentation, restricted: facts in our own words, short quotes |
| project-bootstrap-and-audit's standard, dimension 5 | How an audit rates gates | This repository's own, Apache-2.0 |
| Live repositories audited for this repository, unnamed here (L1, L5 to L10, L31, L56) | The cases behind each rule | Observed practice, in our own words |
