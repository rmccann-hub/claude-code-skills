# Test oracles

Read this for deciding what a result is checked against: a second implementation, a published
reference or a recorded real sample; whether two sources that agree count as two; trusting a
match with another tool; reading filed logs as evidence; tests that need outside data or a real
network response; scoring a tool that reports on its own output; and measuring an eval, a skill
or a plugin against a run without it.

Proving that a test, gate or grader can fail at all is `test-gates`; a test that passes and
fails with no change is `flaky-tests`. Test strategy, doubles, fixtures, coverage, and named
techniques such as differential and metamorphic testing belong to the planned
`testing-patterns` module, after more research. The standard's dimension 5, Testing and
verification, sets two rules this module builds on: whatever scores a run lives where the thing
scored can't edit it, and code that parses input it doesn't control gets damaged-input tests.

## Rules

1. **Check a result against an oracle the code under test doesn't control:** a second
   implementation, a published reference, or a recorded real-world sample. An expected value
   the same code or the same data produced agrees with every bug in it.
2. **Count two sources as two only when they're independent:** different upstream data, a
   different code path, and enough time between the checks that one fault can't reach both.
   Show a match's weight beside the dissent.
3. **Check a reference before a match with it counts as correct.** Check it against an
   independent authority, and read its settings from its own artifacts, not from a report
   about it.
4. **Read filed evidence as a set of claims, and check each one.** A log is evidence only once
   someone has read it.
5. **Pin or record the outside data a test needs,** and name the entry it expects, so a missing
   entry fails as the wrong input, not as a failed step.
6. **Test a parser that offline tests never reach against a recorded real sample.**
7. **Score a tool that reports on its own output by its worst case:** the outputs that are
   wrong and reported as fine. Never report only the pass rate.
8. **Measure against a baseline run without the thing under test.** Only the difference is what
   it contributed.
9. **Grade long output with a deterministic check.** Keep a model grader for short output, with
   concrete pass and fail conditions.

### Choosing an oracle

| Oracle | Catches | Misses |
|---|---|---|
| A second implementation, written apart | Every input where the two differ | A fault both share: the same misread spec, the same library |
| A published reference: test vectors, a checksum database, a spec's examples | Drift from what others accept | The reference's own errors, and a mismatch in its settings (rule 3) |
| A recorded real-world sample | Shapes real input takes that a hand-written fixture leaves out | Formats that changed since the recording, so date each one |
| Output of the code under test, saved | Nothing new: a later change, at best | Every bug present when it was saved |

A saved output is a regression snapshot, not an oracle. Check each value in it once against one
of the first three, and record which. Comparing implementations (differential testing) and
checking relations between the outputs of related inputs (metamorphic testing) are named
techniques for when no oracle exists; the planned `testing-patterns` module takes them up.

### When two sources only look independent

- **Same upstream data.** Two databases that mirror one feed, or two entries most likely
  submitted by one user, are one source.
- **Same code path.** A re-run, a retry or a "second read" through the same code with the same
  fault converges on the same wrong answer, and convergence reads as confirmation.
- **Same moment.** Checks dated on different days can be minutes apart, across midnight. Judge
  independence by the time between them and what changed in it, never by the date.
- **No weight.** One matching entry against many that disagree isn't corroboration. Show both
  counts, and never show a minority match as verified when the primary check rejects.

### Scoring by the worst case

Check every output against a source the tool doesn't control, and put each in one of three
bins: right; wrong and reported (the tool flagged it); wrong and reported as fine. Report the
third bin first, as a count beside the total. It's the one a user acts on, and no pass rate
shows it.

### Baselines and graders

- **Run the same cases without the thing under test.** `claude plugin eval` runs each case with
  the plugin and without it (fact `to-eval-arms`) and reports the difference as `Δ`. A case that
  scores the same both ways says nothing about the plugin (fact `to-eval-baseline`).
- **Leave presence checks out of the score.** A grader that can't pass without the plugin, such
  as "the skill was invoked", measures that the plugin loaded, not what it did, and inflates
  `Δ`; plugin eval scores neither arm on it (fact `to-eval-unscored`).
- **Grade long output with a pattern or a parser.** A model grader's verdict differs between
  runs, more so on long text (fact `to-llm-grader`). Use a `regex` grader over a generated
  file, and keep model graders for short replies with rubrics that state what passes and what
  fails.

## Mistakes

- **Calling a match with another tool "parity", or a re-read that converges on it "the feature
  working".** The other tool can be wrong. Check it against an independent authority first.
- **Writing an expected value by running the code and pasting its output.** The test then
  guards today's bugs. Check the value once against an outside source.
- **Stating a reference's settings from a report or from memory.** Read them from its logs,
  headers or recorded options.
- **Counting a secondary source as corroboration** without asking where its data came from,
  what code produced it and how long after the first check.
- **Summarizing filed logs instead of checking them.** List the claims each one makes, and check
  each against the code or a fresh run.
- **A test that looks up live outside data and fails as a failed step** when the entry is
  missing. Pin or record the data, and fail with "fixture missing: <entry>".
- **Testing a network parser only with hand-written fixtures.** Record a real response and test
  against it, with the damaged-input samples dimension 5 asks for.
- **Reporting a pass rate alone** for a tool that labels its own output.
- **Reporting an eval score with no baseline arm,** or grading a long generated file with a
  model grader.
- **What AI assistants get wrong:** they generate expected values by running the code, take
  agreement between two outputs as proof without asking whether the outputs share a source,
  and summarize evidence files rather than check the claims in them.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Expected values come from the code under test | Snapshots accepted without review; expected values with no recorded source; a test comparing two outputs of one function | `GAP`; `BLOCKER` where a release rests on it | Check each once against an independent oracle, and record which |
| Corroboration shares data, code or a moment | Where each source's data comes from, which code produced it, and the two checks' timestamps | `GAP` | Count it as one source, or find an independent one |
| A minority match shows as verified | A "verified" label from a secondary source where the primary check rejects | `BLOCKER` | Show the match's weight beside the dissent; let the primary rejection stand |
| A match with a reference counts as correct, unchecked | "Parity" or "matches X" claims; a reference's settings stated with no artifact cited | `GAP` | Check the reference against an independent authority; cite the artifact for each setting |
| Filed evidence nobody has read | Logs and evidence bundles in the tree or an issue, with no claim list or check | `GAP` | List each file's claims and check them |
| A test reads live outside data | Network calls or catalog lookups in tests, with no pin or recording | `GAP` | Pin or record it; name the expected entry in the failure |
| A parser for outside responses has no recorded-sample test | The parser's branch coverage; every test offline with hand-written fixtures | `GAP` | Add a recorded real response, dated |
| A tool that labels its own output is scored by pass rate | Its reports and release notes | `GAP`; `BLOCKER` where users act on "fine" | Score in three bins, and report wrong-and-fine first |
| An eval reports scores with no baseline | Reported scores with no without-arm or `Δ` | `GAP` | Run both arms before reporting (fact `to-eval-arms`) |
| A model grader judges long output | Rubric graders over generated files | `GAP` | A deterministic check (fact `to-llm-grader`) |

## Why

### Independent oracles and sources (rules 1 to 3)

- **The advice:** check against something the code didn't produce, count only independent
  sources, and check a reference before trusting a match.
- **The reason:** a check that shares the fault it looks for agrees with it. One project's test
  called matching another tool's output "parity"; on one item the reference was wrong, and
  the main checksum database disagreed at its highest confidence (L41). One app showed a green
  "verified" from a secondary database on 8 of 26 results whose primary check rejected a part:
  each match was one entry, most likely from the same user and a read with the same fault,
  while over a thousand entries disagreed (L42). Two checks on consecutive dates were 26
  minutes apart (L15). A report said a baseline had run without a two-pass mode, and every log
  in it carried the mode's second checksum (L47).
- **What others do:** the standard's dimension 5 keeps whatever scores a run where the thing
  scored can't edit it. This skill's own repository checks each fact's quote against the
  fetched source page, not against the text that cites it.
- **What it costs:** a second implementation or a reference takes work to find and keep
  current, and an independent source may not exist for new behavior.
- **When to choose differently:** where no oracle exists, a saved output still catches a later
  change. Label it a snapshot, not a correctness check.

### Filed evidence (rule 4)

- **The advice:** read each evidence file as claims, and check each one.
- **The reason:** two defects sat for weeks in logs both sides had filed and nobody had read
  (L14).
- **What it costs:** reading time, which grows with every file kept. Keep fewer, and read them.

### Outside data and recorded samples (rules 5 and 6)

- **The advice:** pin or record what a test reads from outside, name the entry it expects, and
  test a parser against a recorded real response.
- **The reason:** one acceptance rig made three runs in 40 minutes on two inputs the public
  catalog didn't know, and each read as a failed step, not the wrong input (L2). Tests that all
  ran offline left a network parser at 27% branch coverage, hiding three crashes (L12).
- **What others do:** dimension 5 asks for damaged-input tests on such code; a recorded real
  sample is the undamaged input those are cut from.
- **What it costs:** a recording goes stale when the service changes. Date it, and refresh it
  when a live call disagrees.
- **When to choose differently:** a scheduled job outside the required checks may call the live
  service, to notice the change a recording can't.

### Worst-case scoring (rule 7)

- **The advice:** score a self-reporting tool by the outputs that are wrong and reported as
  fine.
- **The reason:** one scoring of 178 outputs found 14 wrong, and 9 of those reported as fine, a
  figure no pass rate showed (L50). A user acts on "fine" unchecked.
- **What it costs:** an outside check for every output.
- **When to choose differently:** for a tool whose output nobody acts on unchecked, the pass
  rate may be enough.

### Baselines and graders (rules 8 and 9)

- **The advice:** run the cases without the thing under test, score only what it changed, and
  grade long output deterministically.
- **The reason:** a high score can come from the model alone, and a presence check passes
  whenever the plugin loads (facts `to-eval-baseline`, `to-eval-unscored`). A model grader's
  verdict moves between runs, more on long text (fact `to-llm-grader`).
- **What others do:** Anthropic's `claude plugin eval` runs both arms by default and reports
  `Δ` (fact `to-eval-arms`).
- **What it costs:** the baseline doubles the runs, and each is billed (fact `to-eval-billed`).
  A deterministic check sees only what its pattern names.
- **When to choose differently:** while iterating on a grader, one arm is enough; never report
  a score from it.

## Facts

Practices of a tool, each named elsewhere in this module by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `to-eval-arms` | `claude plugin eval` runs each case three times with the plugin and three times without it | [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals) | "Each case runs three times with your plugin and three times without it, so one case is six runs." | 2026-11-10 | 2027-05-10 |
| `to-eval-baseline` | A case that scores 1.0 in both arms didn't pass because of the plugin | [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals) | "If a case scores 1.0 both with and without the plugin, the plugin isn't what made it pass." | 2026-11-10 | 2027-05-10 |
| `to-eval-unscored` | A grader that can't pass without the plugin, such as a check that the skill was invoked, is left out of the score in both arms | [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals) | "Claude Code excludes such graders from the score in both arms" | 2026-11-10 | 2027-05-10 |
| `to-llm-grader` | A model grader's verdict varies between runs, more on longer text; long output is graded with `regex` | [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals) | "its answer can differ between runs, and it differs more the longer the text it has to read" and "which checks the whole file the same way every time" | 2026-11-10 | 2027-05-10 |
| `to-eval-billed` | Every eval run and judge grader is a billed model call | [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals) | "counted against your plan's usage or your API bill" | 2026-11-10 | 2027-05-10 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals) | The baseline arm, unscored graders, model graders, billing | Anthropic's terms: facts in our own words, short quotes, linked |
| Live repositories audited for this skill's owner, unnamed here (L2, L12, L14, L15, L41, L42, L47, L50) | Each rule's case | Observed practice, in our own words |
