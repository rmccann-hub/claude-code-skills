# RESEARCH RUN R23b: Human factors, the questions R23 didn’t reach

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 11 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 11 November 2026.

This run informs these categories: human-factors, and optimization-and-scheduling where people meet the plan.

## What this run is for

A follow-up to R23 (filed 11 November 2026), which built the shipped `human-factors` skill. That
run listed what it couldn't source; this one finds it. Don't repeat R23's findings; where one has
changed since, say so.

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

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R23b · FORM: research-result v1
Save as: R23b-RESULT.md
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

- Herbert Simon introduced "satisficing" and bounded rationality.
- Michael Polanyi wrote "we can know more than we can tell" (*The Tacit Dimension*, 1966).
- James Reason's Swiss cheese model describes accidents as holes lining up in layered defences.
- Sunk-cost effects are documented in Arkes and Blumer (1985).
- Contextual inquiry (Beyer and Holtzblatt), hierarchical task analysis (Annett and Duncan) and
  cognitive task analysis are the standard methods for studying work as done.

## Questions

### Priority

1. **Methods for finding what a step is for:** contextual inquiry, hierarchical task analysis and
   cognitive task analysis, from their primary sources; what each produces, what it costs, and
   which suits a small team.
2. **The sources R23 couldn't find:** Simon on satisficing, Polanyi on tacit knowledge, Reason's
   Swiss cheese model, and sunk cost, each from its primary source with an exact quote.
3. **The size of the dip after a new system,** in measured units (days, percentage points), from
   field studies beyond McAfee (2002) and one non-recovery case; and the evidence on what
   shortens it (training, phased rollout, running old and new together).
4. **Models that treat people as deterministic:** the operations research and ergonomics
   literature on plans that assumed fixed task times or full utilization, and what happened on
   the shop floor, with the papers' own words.

### Standard

5. **Interfaces:** Fitts's law, the Hick-Hyman law and Nielsen's heuristics from their primary
   sources, and what redesign studies show about the cost of breaking familiarity.
6. **How universal:** cross-cultural replications of status quo bias, habit formation and trust
   in automation.
7. **Neutral retrieval:** guidance from a standards body or regulator (not a vendor) on keeping
   an AI system's fact-finding free of the user's framing.
8. **ISO 6385's 2026 review:** its outcome, and the revised ISO 10075-3's status.
