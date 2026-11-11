# Usability review

Read this for a heuristic review or UX audit of a program's interface, desktop or web: a status
line or progress display that misleads, labels that don't agree, a destructive action with no
way back, errors that don't say what to do, shortcuts for power users, rating how bad each
problem is, and what a review of the code alone can and can't judge.

When a window or dialog appears, modality, focus and stacking are `windows-and-dialogs`.
Defaults, presets, how many options and where each setting lives are `settings-and-options`.
Automated GUI tests and tests with people are `gui-testing`. Accessibility is the
`accessibility` module of the `visual-design` skill.

## Rules

1. **Status says what's true now.** When work starts, clear the last result or mark it as the
   last run's. Show attached things, such as devices, files and connections, as they are now,
   not as they were at start-up. Work that takes more than a moment shows progress, and what
   it's doing.
2. **A verdict comes from the same data as the detail beneath it,** and no verdict word ("OK",
   "Passed", "Done") sits over a failure. Never show a number the program hasn't measured:
   show "measuring" until it has one.
3. **One word for one thing.** An action keeps its label everywhere, two actions never share a
   label or a near one, and the platform's conventions win (fact `uxr-h4-consistency`).
4. **Prevent the error, then offer a way back, and confirm only what can't be undone.**
   Constraints and good defaults stop slips; undo beats a confirmation people click through.
   An error says what happened and what to do next, beside the thing it's about.
5. **Show, don't make people remember.** Current values stay visible, recent choices are
   offered, icons carry labels, and a value chosen on one screen carries to the next.
6. **Serve the expert, and take nothing away.** Give frequent actions shortcuts that novices
   needn't see (fact `uxr-h7-shortcuts`), shown beside their menu items. Never remove a useful
   option to tidy the screen: give it a default, group it, or put it in an advanced section.
7. **Run the review by the method:** independent evaluators, at least two passes each, lists
   merged once all finish, severity rated afterward on the 0 to 4 scale.
8. **From code alone, judge what code shows,** and mark the rest as needing a run.

### Running the review

- **Evaluators:** three to five, each alone (facts `uxr-evaluators`, `uxr-nng-howto`). One
  finds about a third of the problems (fact `uxr-single-evaluator`). An agent's review counts
  as one evaluator: this repository's practice, not a published figure.
- **Passes:** at least two (fact `uxr-two-passes`): the first for the flow, the second for each
  screen and control, against each heuristic in turn.
- **Merging:** nobody sees another's list until all are done (fact `uxr-independent`).
- **Each finding** names the heuristic it breaks, where (screen and control, or file and line),
  its severity and its fix.
- **Severity:** 0 is no problem and 4 a catastrophe to fix before release (fact
  `uxr-severity-scale`). Rate after the walk-through (fact `uxr-severity-after`), and take the
  mean of three or more raters (fact `uxr-severity-raters`). This repository maps 4 to
  `BLOCKER`, 2 or 3 to `GAP`, and lists 1 as a note.

### What a review of the code can and can't judge

- **It can read:** whether starting work resets the status; whether a summary and its detail
  come from the same data; a constant drawn as if measured; a device list filled once at
  start-up; delete, overwrite and format handlers with neither undo nor confirmation; label
  strings, for one action under two names or two under one; a dialog with no parent, or not
  opened by a user action; actions with no shortcut.
- **It can't judge:** timing, such as whether progress appears soon enough or a label flickers;
  look, such as layout, clutter, contrast and which window ends up on top; whether users
  understand a word; how often a problem happens. Mark these `UNVERIFIABLE-HERE`, and run the
  program or hand them to `gui-testing`.

## Mistakes

This repository's own observations, from audits and agents' work; no study documents them. The
first four come from one audited desktop application.

- **A status line kept the last job's "Passed" through the next job.** Reset it when work starts.
- **The main window kept showing a device after it was unplugged.** Listen for removal.
- **A start-up estimate showed a speed it had never measured ("at 1.0x").** Show "measuring".
- **Two file pickers had different meanings and similar labels.** Name each by its file's use.
- **An agent adds a toggle instead of choosing a default.** Choose one; keep the toggle too when
  someone needs the other behavior.
- **An agent builds only the happy path,** with no empty, loading or error state, or computes a
  summary verdict apart from its detail. Build every state from one result.
- **Removing options to simplify a power-user tool.** Default, group or disclose them instead.
- **"Five evaluators find 75%," quoted as Nielsen's.** NN/g's page says three to five.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A verdict over a failure | A summary label set from other data, or earlier, than its detail | `BLOCKER` | Compute both from one result |
| Status not reset when work starts | The start-job path: does it clear or mark the status? | `GAP`; `BLOCKER` where the stale word is a pass | Clear it, or label it as the last run's, with its time |
| A value shown before it's measured | A constant or default drawn as a measurement | `GAP` | "Measuring" until a sample exists |
| Attached things go stale | Device, file or connection lists filled only at start-up | `GAP` | Listen for changes |
| Long work shows nothing | An operation that can take seconds, with no progress or cancel | `GAP` | Progress, the current step, a cancel |
| An unguarded destructive action | Delete, overwrite or format with neither undo nor confirmation | `BLOCKER` | Undo; else confirm with a button naming the action |
| Labels disagree | One action under two names, or two under near-identical ones | `GAP` | One word per thing |
| An error leaves the user stuck | No cause or next step; a dialog for one field's validation | `GAP` | What happened and what to do, beside the field |
| Experts slowed | Frequent actions without shortcuts, or shortcuts hidden from menus | `GAP` in a power-user program | Add them and show them |
| Timing or look judged from code | A finding on delay, flicker, layout or stacking, unrun | `UNVERIFIABLE-HERE` | Run the program |
| A review that can't be acted on | One evaluator; findings missing heuristic, place, severity or fix | `GAP` | More evaluators; complete each finding |

## Why

### Status that's current

- **The reason:** the first heuristic asks the design to keep people informed in reasonable
  time (fact `uxr-h1-status`), and to take no action with consequences unannounced (fact
  `uxr-h1-consequences`). A stale "Passed" says something false about now, and people read
  the verdict, not the rows under it. No primary source forbids a verdict over a failure or a
  figure never measured; both rules are this repository's, from the audits above.
- **What others do:** Shneiderman scales feedback to the action, modest for frequent, minor ones
  and more for rare, major ones (fact `uxr-shneiderman-feedback`).
- **What it costs:** clearing a status loses the last result: keep it in a log. A display meant
  to show the last result says so, with its time.

### Consistency

- **The reason:** people shouldn't wonder whether two words mean one thing (fact
  `uxr-h4-consistency`). Two pickers with near labels send a file to the wrong place.
- **What it costs:** renaming retrains current users. **Choose differently** only to follow the
  platform, which the same heuristic asks for.

### Error prevention and recovery

- **The reason:** the fifth heuristic says remove error-prone conditions, or check and confirm
  (fact `uxr-h5-prevention`). GNOME, KDE and Apple go further and prefer undo, because people
  click through confirmations; `windows-and-dialogs` holds their words.
- **What it costs:** undo needs reversible actions: a trash, soft deletes, a history. A
  confirmation costs a click every time, and trains people not to read.
- **When to choose differently:** what can't be undone, such as formatting a disk or sending a
  message, gets a confirmation whose button names the action.

### Power users

- **The reason:** heuristic 7 asks for shortcuts that let one design serve novices and experts
  (fact `uxr-h7-shortcuts`). The owner builds tools for power users and asked that nothing
  useful be taken away (the owner, 2026-11-10).
- **What others do:** the research found no evidence on dense layouts for experts.
- **What it costs:** each shortcut and option is more to test and document. Showing shortcuts
  in menus and tooltips is how people find them.

### The method

- **The reason:** one evaluator misses most problems (fact `uxr-single-evaluator`), and lists
  kept apart until the end stay independent, which is where extra evaluators add. Severity
  rated in the session is unreliable (fact `uxr-severity-after`).
- **What it costs:** three to five people's time. Alone, do the passes on different days, add an
  agent's review as a second evaluator, and test with people.

## Facts

Each named elsewhere in this module by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `uxr-h1-status` | Heuristic 1: visibility of system status | [10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | "The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time." | 2026-11-10 | 2027-05-10 |
| `uxr-h1-consequences` | Heuristic 1's tip | [10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | "no action with consequences to users should be taken without informing them." | 2026-11-10 | 2027-05-10 |
| `uxr-h4-consistency` | Heuristic 4: consistency and standards | [10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | "Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions." | 2026-11-10 | 2027-05-10 |
| `uxr-h5-prevention` | Heuristic 5: error prevention | [10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | "Either eliminate error-prone conditions, or check for them and present users with a confirmation option before they commit to the action." | 2026-11-10 | 2027-05-10 |
| `uxr-h7-shortcuts` | Heuristic 7: shortcuts for experts | [10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | "Shortcuts — hidden from novice users — may speed up the interaction for the expert user so that the design can cater to both inexperienced and experienced users." | 2026-11-10 | 2027-05-10 |
| `uxr-evaluators` | Three to five evaluators | [Theory of heuristic evaluations](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/) | "My recommendation is normally to use three to five evaluators since one does not gain that much additional information by using larger numbers." | 2026-11-10 | 2027-05-10 |
| `uxr-independent` | Evaluators work alone, then merge | [Theory of heuristic evaluations](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/) | "Only after all evaluations have been completed are the evaluators allowed to communicate and have their findings aggregated." | 2026-11-10 | 2027-05-10 |
| `uxr-two-passes` | At least two passes | [Theory of heuristic evaluations](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/) | "A general recommendation would be that they go through the interface at least twice, however." | 2026-11-10 | 2027-05-10 |
| `uxr-single-evaluator` | One evaluator finds about a third | [Theory of heuristic evaluations](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/) | "Averaged over six of my projects, single evaluators found only 35 percent of the usability problems in the interfaces." | 2026-11-10 | 2027-05-10 |
| `uxr-nng-howto` | NN/g's current how-to: three to five, independent | [How to conduct a heuristic evaluation](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/) | "Ideally, three to five people should independently evaluate the same interface." | 2026-11-10 | 2027-05-10 |
| `uxr-severity-scale` | Severity runs 0 to 4 | [Severity ratings](https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/) | "4 = Usability catastrophe: imperative to fix this before product can be released" | 2026-11-10 | 2027-05-10 |
| `uxr-severity-raters` | The mean of three raters | [Severity ratings](https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/) | "using the mean of a set of ratings from three evaluators is satisfactory for many practical purposes." | 2026-11-10 | 2027-05-10 |
| `uxr-severity-after` | Rate severity after the session | [Severity ratings](https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/) | "It is difficult to get good severity estimates from the evaluators during a heuristic evaluation session" | 2026-11-10 | 2027-05-10 |
| `uxr-shneiderman-feedback` | Shneiderman's rule 3: feedback scaled to the action | [Eight golden rules](https://www.cs.umd.edu/~ben/goldenrules.html) | Checked by hand, as the server's certificate chain is incomplete: “For frequent and minor actions, the response can be modest, whereas for infrequent and major actions, the response should be more substantial.” | 2026-11-10 | 2027-05-10 |

## Sources

| Source | Used for | License |
|---|---|---|
| NN/g: [10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [theory](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/), [how-to](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/), [severity](https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/) | The heuristics, the method, severity | All rights reserved: facts in our own words, short quotes |
| [Shneiderman's eight golden rules](https://www.cs.umd.edu/~ben/goldenrules.html) | Feedback scaled to the action | Not stated on the page: short quotes only |
| [GNOME dialogs](https://developer.gnome.org/hig/patterns/feedback/dialogs.html), [KDE getting input](https://develop.kde.org/hig/getting_input/), [Apple alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) | Undo over confirmation, in our own words | GNOME: not stated; KDE: CC BY-SA 4.0; Apple: all rights reserved. Not quoted here |
| One audited desktop application, unnamed | Mistakes, status rules | Observed, in our own words |
