# RESEARCH RUN R26: Agents reviewing each other's work

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 10 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 10 November 2026.

This run informs: the `review-loops` module of the `agent-engineering` skill.

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
8. **Beliefs marked "(the standard, date)"** come from this repository's own standard,
   PROJECT-BOOTSTRAP-AND-AUDIT v0.49.0, in its section of dated facts. Checking them also
   checks that standard, so say plainly when one is wrong.

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R26 · FORM: research-result v1
Save as: R26-RESULT.md
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

- Two agent sessions, each owning one repository, that review each other's work in numbered
  messages ("laps") converge faster when the close condition is fixed in the round's first
  message and each side commits in advance to its next verdict.
- Rules about evidence (citations, released messages, verdicts tied to a named commit) pay for
  themselves; rules about choreography (envelopes, digests, ledgers, deadlines) cost more than
  they catch.
- Two writers can collide on one message number even with per-side numbering, unless the last
  message names whose turn is next.
- Agents can't supply time on hardware, a design both sides agree on, or acts only a person can
  do, and no number of messages stands in for them.
- An answer from one side isn't a settlement; a person's ruling is written down once, verbatim.

## Questions

### Priority

1. **Published practice on multi-agent review and debate:** what research and engineering
   reports (2023 to 2026) say about agents reviewing or critiquing each other's output: when it
   improves correctness, when it amplifies errors or produces agreement without checking, and
   how many rounds help. Name each study, its setup and its result.
2. **AI code review in practice:** how projects and vendors use AI reviewers on pull requests
   (Anthropic's Claude Code review, GitHub Copilot review, others), the documented failure
   modes, and the guidance on what a human must still decide.
3. **Human code review that carries over:** Google's code review guidelines, and other
   well-sourced practice, on review latency, small changes, what a reviewer checks, and how
   disagreements end. Which of it applies when both reviewer and author are agents?
4. **Protocols between two codebases that depend on each other:** consumer-driven contract
   testing (Pact), API compatibility checks, versioned interface specifications. What do they
   say about keeping two sides' assumptions in step, and when a shared written contract beats
   messages?
5. **Turn-taking and ownership:** how distributed or multi-agent systems avoid two writers
   doing the same work (leases, tokens, single-writer rules), stated for agent sessions.

### Standard

6. **Stopping rules:** evidence on when to stop a review loop: fixed round limits, convergence
   tests, escalation to a person.
7. **Where agents must stop for a person:** authority, approvals, releases, physical tests;
   Anthropic's and others' published guidance on agent autonomy and human checkpoints.
8. **Records:** what a loop should keep so an outside reviewer can audit it later.
