# RESEARCH RUN R23: Human factors: habits that look wasteful and serve a purpose

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 16 October 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 16 October 2026.

This run informs these categories: human-factors, optimization-and-scheduling, and every skill
that designs, automates, optimizes or replaces work that people do.

## What this run is for

People share habits, notions and mindsets that look odd or wasteful to someone outside them,
and that serve a purpose. The owner's example: someone keeps a familiar, slower tool over a
faster one. A design, an automation or an optimization that removes such a habit without
knowing what it's for can make the work worse. The owner wants this to apply everywhere
something is built for people or changes what they do: software, interfaces, processes,
schedules, data migrations and documents.

The skill has a limit, and this run should test it too. Most agents gather information, and
they should stay unbiased: a human habit never bends a factual finding. Human factors count in
design and recommendation, and in questions that objective fact doesn't settle, such as
judgment, taste and trade-offs. Only a few agents should apply this skill at all.

Find the evidence for both halves. Where a habit is only a bias, or a drift that has become
dangerous, say so plainly: that is as useful as finding its purpose.

## Rules

1. **Primary sources first:** peer-reviewed studies, meta-analyses, standards bodies (ISO, NIST,
   HSE), and the original works of the people who named each idea. Use secondary sources
   (respected books, review articles, well-known practitioner writing) only where no primary
   source covers the point, and label them "secondary".
2. **Cite every fact:** the URL, the exact sentence you relied on in quotation marks, and a date
   (the source's own date, otherwise the date you read it).
3. **Never guess.** Write "not found" when you can't source something. Write "contested" when good
   sources disagree, and give each side with its source.
4. **Standards:** for each standard, give its current edition and year, and any revision due
   within 12 months, with its source.
5. **"What we believe" is my current understanding and may be wrong or out of date.** Confirm or
   correct every item, each with a source. The corrections are the most valuable part of this run.
6. **Licences:** for each source, name its licence and say what an Apache-2.0 repository may do
   with it: quote briefly, paraphrase, or adapt it, and with what attribution.
7. **Depth over breadth.** Finish the Priority questions fully. If you run out of room, list the
   rest under "Not covered".
8. **Strength of evidence:** label every claim with its kind of evidence: meta-analysis,
   controlled experiment, field study, case study, or opinion. Name the field it comes from.
   Flag any finding that failed to replicate.
9. **Measured over asserted.** Where a question asks what something costs or saves, give
   measurements: what was measured, on whom, when, and how large the effect was. Label an
   estimate or an opinion as one.

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R23 · FORM: research-result v1
Save as: R23-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.
```

Then these sections, in this order:

1. **Summary:** at most 15 bullets a professional must know today.
2. **Corrections:** every "What we believe" item that was wrong or out of date, with the right
   fact and its source.
3. **Facts table:** `| # | Fact | Value | Source URL | Exact quote | Date |`
4. **Findings:** one section per question below, numbered to match.
5. **The catalogue:** `| Habit | What it looks like | What it's for | Evidence and its strength | When it stops serving | Cost of removing it | Source |`
6. **Changing in the next 12 months:** standards under revision, and findings in dispute.
7. **Common mistakes,** including those AI assistants make in this area, with sources.
8. **Sources and licences:** `| Source | Licence | Quote? | Paraphrase? | Adapt? | Attribution |`
9. **Not found, contested, not covered.**

## What we believe (confirm or correct each)

- Chesterton's fence: don't remove a fence until you know why it was put up (G. K. Chesterton,
  *The Thing*, 1929).
- Work as imagined differs from work as done, and the workarounds people build often keep a
  system running (Hollnagel and resilience engineering, "Safety-II").
- People satisfice rather than optimize, and given the cost of deciding, that is often rational
  (Herbert Simon, bounded rationality).
- A familiar, slower tool can be faster in total: practice, shortcuts and muscle memory
  outweigh a new tool's speed until its learning curve is paid back. Productivity dips after a
  new system is introduced before it recovers, if it does.
- Status quo bias is real (Samuelson and Zeckhauser, 1988), but not every preference for the
  familiar is a bias.
- Redundant checks, paper backups and shadow spreadsheets guard against failures the system's
  designers didn't foresee, as in Reason's Swiss cheese model.
- Slack, buffers and padded estimates absorb variability. Queueing theory (Kingman's formula)
  shows waits growing without bound as utilization nears 100%.
- Automation that leaves people to watch it erodes the skills they need when it fails
  (Bainbridge, "Ironies of Automation", 1983). People misuse, disuse and abuse automation
  (Parasuraman and Riley, 1997).
- Much expertise is tacit: "we can know more than we can tell" (Polanyi, 1966), so the people
  who do the work can't always say why a habit matters.
- Habits form through repetition in a stable context; in one study the median time to
  automaticity was 66 days (Lally et al., 2010).
- Normalization of deviance (Vaughan, on the Challenger launch decision) is the counter-case: a
  habit can be a drift that has become dangerous.
- ISO 9241-210:2019 sets out human-centred design for interactive systems, ISO 6385:2016 the
  ergonomic principles of work systems, and ISO 10075 mental workload.
- Most behavioral findings come from WEIRD samples (Henrich, Heine and Norenzayan, 2010), so
  "universal" needs evidence from other populations.
- Language models tend to agree with a user's stated view even against the facts
  ("sycophancy"), and that tendency has been measured.

## Questions

### Priority

1. The catalogue: habits, notions and mindsets common to people that look inefficient from
   outside and serve a purpose.
   - Start with the owner's example, a familiar, slower tool kept over a faster one: switching
     costs, learning curves, the productivity dip after a change, and how long recovery takes.
   - Then the others the literature itself names, rather than a list of my own guesses. For
     each: what it looks like, what it's for, the evidence and its strength, when it stops
     serving, and what removing it costs.
   - Group them by the purpose they serve, for example guarding against error, absorbing
     variability, keeping skill, saving effort in deciding, and keeping trust between people.
2. Purpose or bias: how to tell a habit that serves a purpose from a cognitive bias or a
   drift.
   - Published methods: contextual inquiry, hierarchical and cognitive task analysis, studies of
     work as done, and asking the people who do the work.
   - The questions to ask, and what to observe, before removing a step that looks redundant.
   - Status quo bias, sunk cost and normalization of deviance as the counter-cases: how each
     shows itself.
3. Designing, automating and optimizing with these habits:
   - what ISO 9241-210, ISO 6385 and the HSE's guidance require or advise;
   - the evidence on tool migrations and new systems: adoption, the productivity dip, and what
     shortened it;
   - the ironies of automation, trust calibration, and keeping people in the loop;
   - when a design should keep a habit, change it gradually, or override it, as for safety.
4. The limit for AI agents:
   - the measured sycophancy of language models, and what reduces it;
   - evidence that AI systems reproduce human biases when they gather or summarize
     information;
   - published guidance on keeping factual retrieval neutral;
   - where a person's preferences rightly count (judgment, taste, values, trade-offs) and where
     only evidence counts; how a system should say which of the two it's giving.

### Standard

5. Optimizers and schedules: the operations research and ergonomics literature on models that
   treat people as deterministic, ignore their preferences, or plan to full utilization, and
   what happened when their plans met the shop floor. Leave fatigue and shift design to run
   R19, which already covers them.
6. Interfaces and software: the laws and heuristics with evidence behind them (Fitts, Hick and
   Hyman, Nielsen's heuristics, consistency, defaults), and what redesign studies show about the
   cost of breaking familiarity.
7. How universal: which of these habits hold across cultures and which are specific to one,
   with cross-cultural studies; where the evidence rests on WEIRD samples only, say so.
8. Common mistakes when engineers, consultants or AI assistants optimize human work, with
   documented cases: a rollout that failed, an automation incident, an efficiency drive that
   removed a safeguard.
