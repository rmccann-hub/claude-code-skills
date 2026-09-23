# RESEARCH RUN R01: Agent context files, Claude Code configuration, and AI agent security

For the repository rmccann-hub/claude-code-skills · Prompt version 2 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: agent-context-files, ai-agent-security, project-bootstrap-and-audit, skill-builder.

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
   PROJECT-BOOTSTRAP-AND-AUDIT v0.35.0, in its section of dated facts. Checking them also
   checks that standard, so say plainly when one is wrong.

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R01 · FORM: research-result v1
Save as: R01-RESULT.md
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

- Claude Code reads CLAUDE.md from the user level (~/.claude/CLAUDE.md), the project (./CLAUDE.md or ./.claude/CLAUDE.md) and CLAUDE.local.md; it supports @path imports and path-scoped rules in .claude/rules/*.md with a `paths` frontmatter field.
- Claude Code reads AGENTS.md natively from v2.1.277 when no CLAUDE.md exists (not on Bedrock or other providers, with telemetry off, or in the first session after an install); a CLAUDE.md containing @AGENTS.md works everywhere and never loads it twice.
- AGENTS.md (agents.md) is an open format read by OpenAI Codex, GitHub Copilot's coding agent, Cursor, Gemini CLI (when configured) and others; its stewardship moved to the Linux Foundation's Agentic AI Foundation in December 2025, alongside MCP.
- GitHub Copilot reads .github/copilot-instructions.md and .github/instructions/*.instructions.md (with `applyTo` globs); Cursor uses .cursor/rules/*.mdc; Gemini CLI uses GEMINI.md.
- The current MCP specification revision is 2025-11-25, and its authorization is based on OAuth 2.1.
- OWASP publishes a Top 10 for LLM Applications (2025 edition, LLM01 is Prompt Injection) and, since December 2025, a Top 10 for Agentic Applications.
- Attacks shown in 2025 hid instructions for coding agents in rules files using invisible Unicode characters.
- (the standard, 2026-09) AGENTS.md is read directly by twenty-odd agent tools. Gemini CLI needs `{"context": {"fileName": "AGENTS.md"}}` in .gemini/settings.json, and Aider needs `read: AGENTS.md` in .aider.conf.yml.
- (the standard, 2026-09) At least one agent tool silently truncates its context file past about 32 KiB.
- (the standard, 2026-09) A controlled study (Gloaguen et al., 2026, arXiv:2602.11988) found repository context files gave no significant gain in task success while raising inference cost by over 20%. A follow-up (Lulla et al., 2026) found curated files cut runtime and tokens on focused changes. Adherence to written instructions falls by about 5.6% in odds for each additional function generated (arXiv:2605.10039).
- (the standard, 2026-09) Security audits of public skill marketplaces in early 2026 found roughly a third of published skills flawed, and confirmed coordinated malicious campaigns.

## Questions

### Priority

1. Anthropic's current guidance for CLAUDE.md: recommended length or budget, structure, what to include and leave out, imports, rules files, and how to keep them current. Quote it, including any line or token target.
2. The same for AGENTS.md and for the GitHub Copilot, Cursor and Gemini CLI instruction files: names, locations, precedence, size limits. Which tools read AGENTS.md natively today? How do teams keep one source of truth across agents (AGENTS.md plus shims, symlinks, imports)?
3. Claude Code's settings and safety features today: permission modes, allow and deny rule syntax, sandboxing, managed settings, hooks (events, blocking behaviour, risks), subagents, skills, plugins, MCP configuration (.mcp.json), and how cloud (web) sessions differ. What does Anthropic recommend committing to a repository versus keeping local?
4. Prompt injection against coding agents: documented attacks through repository files, issues, pull request text, web pages, dependencies and MCP tool results, and the mitigations vendors and OWASP recommend. Cite incidents and CVEs from 2025-2026 that involve coding agents or MCP servers.
5. The OWASP Top 10 for LLM Applications (2025) and the OWASP Top 10 for Agentic Applications: each list, and the controls in each that apply to coding agents.
6. MCP security: the specification's security best practices and authorization requirements; known attack classes (tool poisoning, rug pulls, confused deputy, token passthrough); how to vet an MCP server; the official MCP Registry.
7. Skills and plugins as a supply chain: what a malicious skill or plugin can do in Claude Code, which controls exist (marketplace allow-lists such as strictKnownMarketplaces, review, pinning to a commit), and any published analyses.

### Standard

8. Hidden-text attacks: invisible Unicode (tag characters U+E0000-U+E007F, zero-width characters, bidirectional overrides as in Trojan Source, CVE-2021-42574) and homoglyphs. How are they detected in CI (tools, patterns, GitHub's own warnings)?
9. Secrets and agents: how agents leak secrets (logs, commits, prompts, tool calls) and the recommended controls (deny rules for .env files, secret scanning, short-lived credentials).
10. Testing agent instructions: how to check that an agent follows a context file (evaluations, checks), and the signs that a file is too long or ignored.
11. Government guidance on AI agents or AI-generated code that software teams should know (for example NIST AI 100-2, NIST's generative AI profile of the AI RMF, CISA guidance), briefly.
12. What professional teams put in agent context files (commands, architecture, conventions, "do not" lists, verification steps). Cite real public examples from well-known open-source repositories with AGENTS.md or CLAUDE.md.
