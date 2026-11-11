# RESEARCH RUN R23c: Human factors, what R23 and R23b didn’t reach

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 11 November 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 11 November 2026.

This run informs these categories: human-factors (both modules), and optimization-and-scheduling where people meet the plan.

## What this run is for

A second follow-up. R23 built the `human-factors` skill and R23b its `studying-work` module
(contextual inquiry, hierarchical task analysis, Simon, Polanyi, Reason, sunk cost, the measured
dip after a new system). Both are filed and checked. This run takes what R23b couldn't find.
Don't repeat their findings; where one has changed since, say so.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R23c · FORM: research-result v1
Save as: R23c-RESULT.md
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

- Cognitive task analysis is traced to Klein's Critical Decision Method and to Crandall, Klein
  and Hoffman's *Working Minds* (2006).
- Status quo bias, habit formation and trust in automation have been replicated outside Western
  samples, with smaller or different effects.
- Breaking a familiar interface costs users time for weeks after a redesign.
- Hick (1952) and Hyman (1953) are the primary sources of the Hick-Hyman law.

## Questions

### Priority

1. **How universal:** cross-cultural replications of status quo bias, habit formation and
   trust in automation, with sample sizes, countries and effect sizes, from the papers.
2. **Cognitive task analysis:** its primary sources (the Critical Decision Method, *Working
   Minds*, and others), what each method produces, what it costs, and when it beats
   hierarchical task analysis or contextual inquiry.
3. **What shortens the dip after a new system:** any controlled or field study comparing
   training, phased rollout, parallel running or super-users, in health, ERP, manufacturing or
   public services, with measured effects; and the cost in hours of each study method above.
4. **Plans that assumed people are deterministic, in their own words:** the findings of Schultz,
   Juran, Boudreau, McClain and Thomas (1998) and Schultz, McClain and Thomas (2003), and
   published cases of full-utilization plans on a shop floor.

### Standard

5. **Familiarity in redesigns:** studies measuring the cost of changing a familiar interface
   (time, errors, recovery period), and Hick (1952) and Hyman (1953) from the primary papers.
6. **Neutral retrieval:** any standards body, regulator or peer-reviewed guidance on keeping an
   AI system's fact-finding free of the user's framing or leading questions.
7. **ISO 6385's review:** the outcome of its 2026 review, and ISO 10075-3's next stage.
