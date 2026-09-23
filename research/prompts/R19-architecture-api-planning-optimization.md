# RESEARCH RUN R19: Architecture, API design, planning, optimization and scheduling

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: architecture-and-design, api-design, optimization-and-scheduling.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R19 · FORM: research-result v1
Save as: R19-RESULT.md
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

- OpenAPI 3.2.0 was released in September 2025; OpenAPI 3.1.x is widely supported; AsyncAPI 3.0 and JSON Schema 2020-12 are current.
- RFC 9110 renamed status 422 "Unprocessable Content"; RFC 9457 defines problem details; IETF drafts cover the Idempotency-Key and RateLimit headers.
- OAuth 2.1 is a draft, RFC 9700 is the OAuth security BCP, and RFC 8725 is the JWT BCP.
- MADR 4.0 is the current ADR template; the C4 model and arc42 are common ways to document architecture.
- Google OR-Tools (v9.x) CP-SAT is the leading open-source constraint solver, and its Python API added PEP 8 (snake_case) method names; HiGHS is a leading open-source LP and MIP solver; Timefold succeeds OptaPlanner.
- Spec-driven development with AI agents (for example GitHub Spec Kit, 2025) is an emerging practice.

## Questions

### Priority

1. REST API design, from authoritative guidelines (Microsoft REST API Guidelines, Google AIP, Zalando):
   - resource naming, methods and idempotency, status codes under RFC 9110
   - pagination (cursor versus offset), filtering, versioning strategies, long-running operations
   - ETags and conditional requests
   - the status of the Idempotency-Key and RateLimit drafts; webhooks (the Standard Webhooks spec); error format (RFC 9457)
2. API specifications and tooling: what changed in OpenAPI 3.2 from 3.1, and tool support; AsyncAPI 3.x; JSON Schema 2020-12; linting (Spectral, Redocly CLI); code generation; contract testing; the current GraphQL spec edition and GraphQL security (depth and complexity limits); gRPC and Protobuf editions; Buf.
3. API security: the OWASP API Security Top 10 (2023 or newer), OAuth 2.1 and RFC 9700 practice, API keys versus OAuth, token storage in clients, CORS.
4. Architecture: current consensus on modular monoliths versus microservices, with sources; hexagonal and clean architecture; domain-driven design basics; decision records (MADR 4); the C4 model and arc42; architecture fitness functions; the pillars of the Well-Architected frameworks.
5. Planning and specification with AI agents: spec-driven development (GitHub Spec Kit and others), plan-then-execute practice, writing acceptance criteria (Given/When/Then, Gherkin), estimating and slicing work, and published evidence on how planning affects the quality of AI-generated code.

### Standard

6. Optimization and scheduling: OR-Tools' current version and CP-SAT Python API naming, HiGHS, SCIP (and its current licence), Pyomo, PuLP, Timefold; modelling business rules as constraints (hard versus soft, penalties); the job-shop and flow-shop examples in the official docs.
7. Human factors in scheduling: peer-reviewed or standards sources on fatigue and shift design, time-of-day effects, changeover and setup behaviour and learning curves, and how schedulers should account for them (for example ISO 10075, HSE guidance, the operations research literature). Label any unsourced heuristic as a heuristic.
8. Refactoring: the current web edition of Fowler's refactoring catalogue (second edition), a safe refactoring workflow, and tool support per language.
