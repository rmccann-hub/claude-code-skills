# Verification: R01 (2026-09-23)

Checked by the receiving session on 2026-09-23. Only the claims this intake relies on were
checked: those behind proposed changes to the standard, anything touching this repository's
files, and dates that need action. The rest is a lead until a skill uses it.

| Claim | Status | Checked against |
|---|---|---|
| Claude Code reads `AGENTS.md` natively from 2.1.277, but not when a `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists in the working directory or above it, and not in these sessions: no feature flags (Bedrock, other providers, telemetry off), the first session after an install or upgrade, or the built-in `agents-md` plugin disabled | verified | [Claude Code memory docs](https://code.claude.com/docs/en/memory), section "When AGENTS.md support is unavailable"; [changelog](https://code.claude.com/docs/en/changelog) |
| Keeping `@AGENTS.md` in `CLAUDE.md` "never makes Claude read `AGENTS.md` twice" | verified | [Claude Code memory docs](https://code.claude.com/docs/en/memory) |
| `CLAUDE.md`: "target under 200 lines per CLAUDE.md file"; loaded in full up to 4 MiB; imports nest up to four hops; only `MEMORY.md` is cut off (first 200 lines or 25KB) | verified | [Claude Code memory docs](https://code.claude.com/docs/en/memory) |
| `paths` is the only field Claude Code reads from a rule file | verified | [Claude Code memory docs](https://code.claude.com/docs/en/memory). This repository's `.claude/rules/python.md` uses only `paths` |
| `CLAUDE.md` is "not a hard enforcement layer" | verified | [Claude Code memory docs](https://code.claude.com/docs/en/memory) |
| Claude Code 2.1.280 is current, with a 2,048-character cap on MCP tool descriptions | verified | [changelog](https://code.claude.com/docs/en/changelog); `package.json` pins 2.1.280 |
| Lulla et al. compare agents with and without an `AGENTS.md` on 10 repositories and 124 pull requests: lower median runtime (28.64%) and output tokens (16.58%). The paper says nothing about "curated" files or "focused changes" | verified; **the standard's description is contradicted** | [arXiv:2601.20404](https://arxiv.org/abs/2601.20404) abstract |
| McMillan: about 5.6% lower odds of compliance per step (OR 0.944), non-monotonic and found during analysis; the primary result is that no structural variable "produces a detectable contrast" | verified | [arXiv:2605.10039](https://arxiv.org/abs/2605.10039) abstract |
| Gloaguen et al.: context files do "not generally improve task success rates" and raise inference cost by "over 20%" | verified | [arXiv:2602.11988](https://arxiv.org/abs/2602.11988) abstract. The standard's "438 tasks" is not in the abstract and was not checked |
| Codex stops adding files once their combined size reaches `project_doc_max_bytes`, 32 KiB by default | verified | [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md). Per-file against combined, which the report calls contested, was not checked further |
| Snyk ToxicSkills: 3,984 skills, 36.82% with at least one flaw, 13.4% critical. Liu et al.: 42,447 skills, 26.1% with a vulnerability, 5.2% high-severity | verified | [Snyk](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/); [arXiv:2601.10338](https://arxiv.org/abs/2601.10338). The report's link for Liu et al. points at 2604.06550; the paper is 2601.10338 |
| The current MCP specification revision is 2026-07-28 | verified | [MCP blog, 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/) |
| OWASP published a Top 10 for LLM Applications 2026 | verified | [OWASP GenAI resource page](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/). The item ranking was not checked |
| Everything else in the report | not yet checked | checked when a skill that relies on it is built (`research/README.md`) |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R01 · FORM: research-result v1
Save as: R01-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R01: Agent context files, Claude Code configuration, and AI agent security (researched 23 September 2026)

Two of your beliefs are now out of date, and one of the standard's beliefs misdescribes its source. The current MCP specification is **2026-07-28**, not 2025-11-25. OWASP released a **2026 edition** of the LLM Top 10 in August 2026, replacing the 2025 edition. The "Lulla et al." belief says something the paper does not. Most other beliefs hold, with qualifications that matter. Claude Code's native AGENTS.md support has more exclusions than the belief lists. The "5.6%" adherence figure is an exploratory, non-monotonic side finding in a paper whose main result is that file size made **no detectable difference**. That result directly contests Anthropic's own "under 200 lines" rationale.

## 1. Summary

- **Claude Code 2.1.280 (22 September 2026) is current.** AGENTS.md is read natively from **2.1.277 (18 September 2026)**, but only when no CLAUDE.md, .claude/CLAUDE.md **or CLAUDE.local.md** exists in the working directory or any directory above it. It is also not read on Bedrock or other third-party providers, with telemetry off, in the first session after an install **or upgrade**, or if the built-in `agents-md` plugin is disabled.
- **`@AGENTS.md` inside CLAUDE.md is the portable pattern.** Anthropic's docs say keeping the import "never makes Claude read `AGENTS.md` twice". Prefer the import to a symlink on any repository that Windows users clone.
- **Anthropic's CLAUDE.md target is "under 200 lines per CLAUDE.md file."** Imports do not save context. Path-scoped `.claude/rules/*.md` files (`paths` frontmatter) and skills do. Claude Code skips any CLAUDE.md over 4 MiB. MEMORY.md, not CLAUDE.md, is the file with a hard 200-line / 25KB load cut-off.
- **CLAUDE.md is advice, not enforcement.** Anthropic says it is "not a hard enforcement layer". Use `permissions.deny`, sandboxing, PreToolUse hooks and managed settings for anything that must hold.
- **Permission rules are evaluated deny → ask → allow, and Bash rules are not a security boundary.** `Bash(curl *)` does not stop `/usr/bin/curl` or `sh -c 'curl …'`. `Read(./.env)` does not stop `grep -r`. The sandbox covers only Bash, PowerShell and Monitor subprocesses.
- **MCP's current revision is 2026-07-28 (released 28 July 2026).** It has a stateless core, RFC 9207 issuer validation, credentials bound to their issuer, and Dynamic Client Registration deprecated in favour of Client ID Metadata Documents. Roots, Sampling, Logging and legacy HTTP+SSE are deprecated with at least a 12-month window.
- **MCP security best practices use MUST language.** Proxy servers "MUST implement per-client consent", and servers "MUST NOT accept any tokens that were not explicitly issued for the MCP server". There is a new SSRF section for OAuth metadata discovery.
- **OWASP LLM Top 10 2026 was published in August 2026.** Prompt Injection stays LLM01. Excessive Agency rises to LLM03. System Prompt Leakage is replaced by "Hidden Context Exposure" (LLM08). The OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10) was announced on 9 December 2025.
- **AGENTS.md and MCP moved to the Linux Foundation's Agentic AI Foundation on 9 December 2025.** agents.md reports use by "over 60k open-source projects".
- **The evidence on context files is mixed.** Gloaguen et al. (ETH Zurich) found no general gain in task success and over 20% higher inference cost. Lulla et al. found lower median runtime (−28.64%) and fewer output tokens (−16.58%). McMillan found no detectable effect from file size (25–500 lines), position, split or conflicts. Recommendation: keep files minimal, and put in them only what an agent cannot derive.
- **Codex truncates AGENTS.md at `project_doc_max_bytes` (32 KiB by default).** Claude Code 2.1.280 added a 2,048-character cap on MCP tool descriptions (`CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH`).
- **Repository files have caused real, CVE-numbered compromises of Claude Code.** Examples are CVE-2025-59536 (code ran before the trust dialog), CVE-2026-21852 (API key exfiltration through project files) and CVE-2025-59041 (malicious git email). MCP tooling had critical RCEs: CVE-2025-6514 in mcp-remote (CVSS 9.6) and CVE-2025-49596 in MCP Inspector (CVSS 9.4).
- **Skills and plugins are a live supply chain.** Snyk's ToxicSkills scan (February 2026, 3,984 skills) found 36.82% with at least one flaw and 13.4% with a critical flaw. Koi Security found 341 malicious skills out of 2,857 on ClawHub, 335 of them from one campaign (ClawHavoc).
- **Claude Code's controls:** `strictKnownMarketplaces` (managed only; `[]` means lockdown), `blockedMarketplaces`, and git plugin sources pinned with `sha`. Anthropic warns that plugins "can execute arbitrary code on your machine with your user privileges".
- **Gemini CLI note:** "Gemini CLI was replaced by Antigravity CLI on June 18th, 2026" for unpaid-tier and Google One users. Re-check any GEMINI.md-only guidance for those users.

## 2. Corrections

| # | What we believed | Status | Correct fact | Source |
|---|---|---|---|---|
| C1 | "The current MCP specification revision is 2025-11-25" | **Wrong (out of date)** | Current revision is **2026-07-28**, released 28 July 2026. 2025-11-25 is now "the previous revision". The spec site labels "Version 2026-07-28 (latest)". | https://blog.modelcontextprotocol.io/posts/2026-07-28/ ; https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx |
| C2 | "its authorization is based on OAuth 2.1" | **Incomplete** | Still OAuth-based. The security best practices cite "OAuth 2.1 Section 1.5". 2026-07-28 adds: clients "must validate" the RFC 9207 `iss` parameter; "Client credentials are bound to the issuer that minted them"; "Dynamic Client Registration itself is now formally deprecated in favor of CIMD." | https://blog.modelcontextprotocol.io/posts/2026-07-28/ ; https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices |
| C3 | "OWASP publishes a Top 10 for LLM Applications (2025 edition, LLM01 is Prompt Injection)" | **Out of date** | The **2026 edition** is current. OWASP's resource page is dated 3 August 2026. The GitHub repository says "published August 4, 2026". The press release is dated 2 September 2026. LLM01 is still Prompt Injection. | https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/ ; https://github.com/owasp/www-project-top-10-for-large-language-model-applications ; https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/ |
| C4 | Native AGENTS.md is read "when no CLAUDE.md exists (not on Bedrock or other providers, with telemetry off, or in the first session after an install)" | **Incomplete** | (a) **CLAUDE.local.md and .claude/CLAUDE.md also block it.** "Because `CLAUDE.local.md` counts, adding one … stops Claude from reading `AGENTS.md`". (b) The first session after an install **or upgrade** is excluded. (c) It is off if the built-in `agents-md` plugin is disabled. (d) `~/.claude/CLAUDE.md` and managed CLAUDE.md do *not* count. (e) AGENTS.local.md, AGENTS.override.md and `.agents/` are "Not read". (f) Before v2.1.280, `/memory` and `/context` did not list a directly-read AGENTS.md. | https://code.claude.com/docs/en/memory (read 2026-09-23) |
| C5 | Standard: Lulla et al. "found curated files cut runtime and tokens on focused changes" | **Misdescribed** | The paper (arXiv:2601.20404) compares with vs without an existing AGENTS.md on "10 repositories and 124 pull requests". It reports "lower median runtime (Δ28.64%) and reduced output token consumption (Δ16.58%), while maintaining a comparable task completion behavior". It does not test "curated" files or "focused changes". Cite the arXiv ID in the standard. | https://arxiv.org/abs/2601.20404 |
| C6 | Standard: "Adherence … falls by about 5.6% in odds for each additional function generated (arXiv:2605.10039)" | **Correct figure, misleading framing** | The author (McMillan, 11 May 2026) calls it "approximately 5.6% lower odds of compliance per step (OR = 0.944)". He adds: "the relationship is non-monotonic rather than a constant per-step effect" and "it was identified during analysis rather than pre-specified". The paper's primary result is that none of file size, position, architecture or conflicts "produces a detectable contrast". | https://arxiv.org/abs/2605.10039 |
| C7 | Standard: Gloaguen et al. found "no significant gain in task success" | **Confirmed with nuance** | The abstract says "does not generally improve task success rates, while increasing inference cost by over 20% on average". The v1 HTML abstract says context files "tend to reduce task success rates". The authors conclude that "human-written context files should describe only minimal requirements." | https://arxiv.org/abs/2602.11988 ; https://arxiv.org/html/2602.11988v1 |
| C8 | "GitHub Copilot reads .github/copilot-instructions.md and .github/instructions/*.instructions.md" | **Incomplete** | Copilot also reads "AGENTS.md, CLAUDE.md or GEMINI.md files" as agent instructions. On GitHub.com, path-specific instructions "are only supported for Copilot cloud agent and Copilot code review". Code review reads instructions "from the head branch", so a PR can change the rules its own review uses. | https://docs.github.com/en/copilot/reference/custom-instructions-support ; https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot ; https://docs.github.com/en/copilot/tutorials/customize-code-review |
| C9 | "Gemini CLI uses GEMINI.md" | **Confirmed, with a product change** | GEMINI.md is still the default. However, "Unpaid tier and Google One users: Gemini CLI was replaced by Antigravity CLI on June 18th, 2026." How Antigravity CLI handles context files was not found. | https://geminicli.com/docs/cli/gemini-md/ |
| C10 | Standard: "At least one agent tool silently truncates its context file past about 32 KiB" | **Confirmed; "silently" is secondary; scope contested** | Codex "stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)". "Silently truncated" comes from a source-code comment quoted in openai/codex issue #7138 (secondary). Another official page says the limit is per file ("how much to read from each AGENTS.md file"), so per-file vs combined is **contested**. | https://developers.openai.com/codex/guides/agents-md ; https://github.com/openai/codex/issues/7138 |
| C11 | Standard: "roughly a third of published skills flawed" | **Confirmed for one audit; scope caveat** | Snyk: "36.82% of all skills (1,467 total) contain at least one security flaw, and 13.4% contain at least one critical-level issue". The sample was ClawHub and skills.sh (the OpenClaw ecosystem), not Anthropic's plugin marketplace. A separate study, Liu et al., "Agent Skills in the Wild" (arXiv:2601.10338, 15 January 2026), collected 42,447 skills from skills.rest and skillsmp.com and found "26.1% of skills contain at least one vulnerability" and "5.2% of skills exhibit high-severity patterns strongly suggesting malicious intent". | https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/ ; https://arxiv.org/html/2604.06550v1 |

Confirmed without correction: CLAUDE.md locations, @imports and `.claude/rules/` with `paths`. The Agentic AI Foundation (9 December 2025). The OWASP Agentic Top 10 (9 December 2025). The Rules File Backdoor (Pillar, 18 March 2025). The Gemini CLI `context.fileName` and Aider `read: AGENTS.md` configurations. AGENTS.md being read by twenty-odd tools. Details are in the Facts table.

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| F1 | Claude Code current version | 2.1.280 | https://code.claude.com/docs/en/changelog | "2.1.280 … September 22, 2026" | 2026-09-22 |
| F2 | AGENTS.md support added | 2.1.277 | https://code.claude.com/docs/en/changelog | "Added AGENTS.md support: in a project with no CLAUDE.md, Claude Code reads AGENTS.md instead; change it under \"Project instructions\" in `/config` (not yet on Bedrock, Vertex or Foundry)" | 2026-09-18 |
| F3 | CLAUDE.md size target | under 200 lines | https://code.claude.com/docs/en/memory | "**Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." | read 2026-09-23 |
| F4 | CLAUDE.md hard limit | 4 MiB | https://code.claude.com/docs/en/memory | "Claude Code loads a CLAUDE.md file of up to 4 MiB in full and skips a larger file." | read 2026-09-23 |
| F5 | MEMORY.md load limit | 200 lines or 25KB | https://code.claude.com/docs/en/memory | "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation." | read 2026-09-23 |
| F6 | Import depth | 4 hops | https://code.claude.com/docs/en/memory | "Imported files can recursively import other files, with a maximum depth of four hops." | read 2026-09-23 |
| F7 | Imports don't save context | — | https://code.claude.com/docs/en/memory | "Splitting into `@path` imports helps organization but doesn't reduce context, since imported files load at launch." | read 2026-09-23 |
| F8 | Only rule frontmatter field | `paths` | https://code.claude.com/docs/en/memory | "`paths` is the only field Claude Code reads from a rule; any other field is ignored without an error." | read 2026-09-23 |
| F9 | CLAUDE.md is not enforcement | — | https://code.claude.com/docs/en/memory | "CLAUDE.md instructions shape Claude's behavior but are not a hard enforcement layer." | read 2026-09-23 |
| F10 | Double-load safety | — | https://code.claude.com/docs/en/memory | "Keeping the import never makes Claude read `AGENTS.md` twice, whichever **Project instructions** value you use." | read 2026-09-23 |
| F11 | Project-instructions setting scope | user/managed/--settings only | https://code.claude.com/docs/en/memory | "Claude Code ignores it in project and local settings files." | read 2026-09-23 |
| F12 | HTML comments stripped | — | https://code.claude.com/docs/en/memory | "Block-level HTML comments (`<!-- maintainer notes -->`) in CLAUDE.md files are stripped before the content is injected into Claude's context." | read 2026-09-23 |
| F13 | Permission rule order | deny → ask → allow | https://code.claude.com/docs/en/permissions | "Rules are evaluated in order: deny, then ask, then allow." | read 2026-09-23 |
| F14 | Enforcement locus | client, not model | https://code.claude.com/docs/en/permissions | "Permission rules are enforced by Claude Code, not by the model." | read 2026-09-23 |
| F15 | Permission modes | default, acceptEdits, plan, auto, dontAsk, bypassPermissions | https://code.claude.com/docs/en/permissions | "Only use this mode in isolated environments like containers or VMs where Claude Code can't cause damage." (bypassPermissions) | read 2026-09-23 |
| F16 | Disabling risky modes | `permissions.disableBypassPermissionsMode`, `permissions.disableAutoMode` | https://code.claude.com/docs/en/permissions | "These are most useful in managed settings where they can't be overridden." | read 2026-09-23 |
| F17 | Bash rules are not a boundary | — | https://code.claude.com/docs/en/permissions | "a deny or ask rule covers the invocation Claude usually produces and isn't a security boundary around the program." | read 2026-09-23 |
| F18 | MCP tool description cap | 2,048 characters | https://code.claude.com/docs/en/changelog | "Added `CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH` to change the 2,048-character cap on MCP tool descriptions and server instructions" | 2026-09-22 |
| F19 | Marketplace lookalike names refused | 2.1.280 | https://code.claude.com/docs/en/changelog | "Changed plugin marketplaces whose name imitates a reserved marketplace name to be refused when added" | 2026-09-22 |
| F20 | Policy bug fixed | 2.1.277 | https://code.claude.com/docs/en/changelog | "Fixed one malformed `strictKnownMarketplaces` or `blockedMarketplaces` entry silently disabling the whole enterprise marketplace policy" | 2026-09-18 |
| F21 | strictKnownMarketplaces `[]` | lockdown | https://code.claude.com/docs/en/plugin-marketplaces | "Empty array `[]` \| Complete lockdown. Blocks every marketplace source, including the official Anthropic marketplace" | read 2026-09-23 |
| F22 | Plugin pinning | `sha` wins over `ref` | https://code.claude.com/docs/en/plugin-marketplaces | "When both `ref` and `sha` are set on any of them, the `sha` is the effective pin." | read 2026-09-23 |
| F23 | AAIF formation | 9 Dec 2025 | https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | "founding contributions of three leading projects …; Anthropic's Model Context Protocol (MCP), Block's goose, and OpenAI's AGENTS.md." | 2025-12-09 |
| F24 | AGENTS.md adoption | 60k+ projects | https://agents.md/ | "used by over 60k open-source projects" | read 2026-09-23 |
| F25 | AGENTS.md precedence | nearest file | https://agents.md/ | "The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything." | read 2026-09-23 |
| F26 | Gemini CLI config | `context.fileName` | https://agents.md/ | "Configure Gemini CLI to use AGENTS.md in `.gemini/settings.json`: { \"context\": { \"fileName\": \"AGENTS.md\" }, }" | read 2026-09-23 |
| F27 | Aider config | `read: AGENTS.md` | https://agents.md/ | "Configure Aider to use AGENTS.md in `.aider.conf.yml`: read: AGENTS.md" | read 2026-09-23 |
| F28 | Codex limit | 32 KiB | https://developers.openai.com/codex/guides/agents-md | "stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)" | read 2026-09-23 |
| F29 | MCP current revision | 2026-07-28 | https://blog.modelcontextprotocol.io/posts/2026-07-28/ | "Today, we're officially pushing the release button on the next version of the MCP specification, `2026-07-28`" | 2026-07-28 |
| F30 | MCP deprecations | Roots, Sampling, Logging; HTTP+SSE | https://blog.modelcontextprotocol.io/posts/2026-07-28/ | "They still work, and they'll keep working for at least twelve months." | 2026-07-28 |
| F31 | MCP token rule | — | https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices | "MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP server." | read 2026-09-23 |
| F32 | OWASP LLM Top 10 2026 | published | https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/ | "OWASP Top 10 for LLM Applications 2026 is the latest community-driven guide" | 2026-08-03 |
| F33 | OWASP Agentic Top 10 | announced | https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/ | "Hidden prompts turned copilots into silent exfiltration engines (ASI01 – Agent Goal Hijack, e.g EchoLeak)." | 2025-12-09 |
| F34 | Gloaguen et al. | no general gain, >20% cost | https://arxiv.org/abs/2602.11988 | "providing context files does not generally improve task success rates, while increasing inference cost by over 20% on average" | 2026-02-12 |
| F35 | Lulla et al. | −28.64% runtime, −16.58% output tokens | https://arxiv.org/abs/2601.20404 | "lower median runtime ($Δ28.64$%) and reduced output token consumption ($Δ16.58$%)" | 2026-01 (arXiv 2601) |
| F36 | McMillan | null on size | https://arxiv.org/abs/2605.10039 | "None of the four structural variables or three two-way interactions produces a detectable contrast after multiple-testing correction." | 2026-05-11 |
| F37 | Rules File Backdoor | Cursor, Copilot | https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents | "By exploiting hidden unicode characters and sophisticated evasion techniques in the model facing instruction payload, threat actors can manipulate the AI to insert malicious code" | 2025-03-18 |
| F38 | GitHub hidden-Unicode warning | 1 May 2025 | https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents | "GitHub implemented a new security feature that displays a warning when a file's contents include hidden Unicode text on github.com." | 2025-05-01 (per Pillar) |
| F39 | Snyk ToxicSkills | 3,984 skills | https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/ | "Unlike traditional packages that execute in isolated contexts, Agent Skills operate with the full permissions of the AI agent they extend." | 2026-02 |

## 4. Findings

### 4.1 Anthropic's CLAUDE.md guidance (Priority)

**Locations and load order.** The Anthropic memory page lists four scopes "in load order, from broadest scope to most specific":
- managed policy (`/Library/Application Support/ClaudeCode/CLAUDE.md`, `/etc/claude-code/CLAUDE.md`, `C:\Program Files\ClaudeCode\CLAUDE.md`);
- user (`~/.claude/CLAUDE.md`);
- project (`./CLAUDE.md` or `./.claude/CLAUDE.md`);
- local (`./CLAUDE.local.md`, "add to `.gitignore`").

"All discovered files are concatenated into context rather than overriding each other." Files in parent directories load at launch. Subdirectory files load "when Claude reads files in those subdirectories". Managed CLAUDE.md "cannot be excluded by individual settings". Organisations can also put the content inline with the managed-only `claudeMd` key.

**Budget and structure (quoted).**
- "**Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."
- "**Structure**: use markdown headers and bullets to group related instructions."
- "**Specificity**: write instructions that are concrete enough to verify", for example "Run `npm test` before committing" instead of "Test your changes".
- "**Consistency**: if two rules contradict each other, Claude may pick one arbitrarily."

No token target is given; the only numeric targets are lines (200) and the 4 MiB hard skip.

**Include / leave out.** Include: "build commands, conventions, project layout, 'always do X' rules". Move out anything that "is a multi-step procedure or only matters for one part of the codebase" into a skill or path-scoped rule. Add an entry when "Claude makes the same mistake a second time". `/doctor` "cuts content Claude can derive from the codebase, such as directory layouts, dependency lists, and architecture overviews, and keeps pitfalls, rationale, and conventions that differ from tool defaults". Note the tension: "project layout" appears in the include list, but `/doctor` trims directory layouts. The safe reading is to state only layout facts that are *not* derivable from the code.

**Imports.** `@path/to/import`, relative to the importing file, up to four hops. Imports inside code spans are skipped. An import that resolves outside the working directory triggers a one-time approval dialog: "Claude Code shows the dialog to protect you from files other people commit to a shared project."

**Rules files.** `.claude/rules/**/*.md` are discovered recursively. Without `paths` they load at launch "with the same priority as `.claude/CLAUDE.md`". With `paths` they "trigger when Claude reads files matching the pattern, not on every tool use". Invalid YAML makes the rule load as if unscoped. Symlinked rules pointing outside the repository need external-import approval.

**Keeping current.** "Review your CLAUDE.md files, nested CLAUDE.md files in subdirectories, and `.claude/rules/` periodically to remove outdated or conflicting instructions." Use `/init` (it suggests improvements to an existing file), `/doctor` trims (v2.1.206+), `/context` to check what loaded, and the `InstructionsLoaded` hook to log it. Use `claudeMdExcludes` for other teams' files in monorepos.

**Position.** Adopt Anthropic's 200-line target as a *cost and clarity* rule, not an adherence guarantee. The one controlled test of file size (McMillan, 25–500 lines) found no detectable adherence effect, with Bayes factors supporting the null for size. This is **contested**; see 4.10.

### 4.2 AGENTS.md, Copilot, Cursor, Gemini CLI; single source of truth (Priority)

**AGENTS.md** is plain Markdown with "No" required fields. For nested files, "the closest one takes precedence", and "explicit user chat prompts override everything". The agents.md carousel lists 23 tools (read 2026-09-23): Codex, Jules, Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin, UiPath, Junie, Amp, Cursor, RooCode, Gemini CLI, Kilo Code, Phoenix, Semgrep, GitHub Copilot coding agent, Ona, Windsurf and Augment Code. Claude Code joins them from 2.1.277. So the standard's "twenty-odd" is accurate. "Read directly" is too strong for Aider and Gemini CLI, which need the configuration shown in F26–F27.

**Claude Code.** See C4 and F2. There are three modes via `/config` → Project instructions or `pluginConfigs["agents-md@builtin"]`: `claude-md-or-agents-md` (default), `claude-md-and-agents-md` and `claude-md`. A fourth, `managed-only`, leaves out project, local and user CLAUDE.md, rules and every AGENTS.md.

**GitHub Copilot.** Repository-wide: `.github/copilot-instructions.md`. Path-specific: `.github/instructions/**/NAME.instructions.md` with `applyTo` glob frontmatter ("You can specify multiple patterns by separating them with commas"). Agent instructions: AGENTS.md, CLAUDE.md or GEMINI.md. Personal: `~/.copilot/copilot-instructions.md`. Copilot CLI "combines their instructions … but does not define a general precedence order". GitHub's code-review tutorial says "Shorter instruction files are more likely to be fully pr[ocessed]" (the quote is truncated in the search excerpt; no numeric size limit was found this run).

**Gemini CLI.** Default GEMINI.md, loaded hierarchically from `~/.gemini/GEMINI.md`, then from the current directory up to the project root. All found files are concatenated "with every prompt". `context.fileName` accepts a string or array, for example `["AGENTS.md", "CONTEXT.md", "GEMINI.md"]`. See C9 for the June 2026 Antigravity replacement.

**Cursor.** `.cursor/rules/*.mdc` format and precedence: **not verified this run** (see section 9). Anthropic's `/init` reads "Cursor rules in `.cursor/rules/` or `.cursorrules`", which confirms the path names only.

**Size limits.** Codex: 32 KiB (`project_doc_max_bytes`). Claude Code: 4 MiB skip, plus a 2,048-character cap on MCP descriptions. Copilot and Gemini CLI: not found.

**Single source of truth: recommended pattern for this repository's standard:**
1. AGENTS.md at the root holds the shared content.
2. CLAUDE.md contains `@AGENTS.md` followed by Claude-only additions. This works in every Claude Code session, including Bedrock and telemetry-off, and is never double-loaded.
3. `.gemini/settings.json` → `{"context":{"fileName":"AGENTS.md"}}`; `.aider.conf.yml` → `read: AGENTS.md`.
4. Copilot reads AGENTS.md directly. Keep `.github/copilot-instructions.md` only for Copilot-specific extras.
5. Avoid symlinks where Windows users clone: Git "checks a committed symlink out as a plain text file unless `core.symlinks` is enabled".
6. Remove any SessionStart hook that prints AGENTS.md; it "adds a second copy to the context".

### 4.3 Claude Code settings and safety features (Priority)

- **Permission modes:** see F15. `default` is labelled "Manual" from v2.1.200. `dontAsk` "Auto-denies every call that would otherwise prompt". `auto` uses a classifier; from 2.1.278 it defaults to a server-side classifier for API, Enterprise and cloud-provider users.
- **Rule syntax:** `Tool` or `Tool(specifier)`. For example, `Bash(npm run *)`, `Read(./.env)` and `WebFetch(domain:example.com)`. A bare `Bash` deny "removes the tool from Claude's context entirely". Put `*` after the subcommand. `Bash(git * main)` also matches `git -c core.fsmonitor=<script> diff main`. Compound commands are split on `&&`, `||`, `;`, `|`, `|&`, `&` and newlines. Read and Edit rules use gitignore syntax. A leading `/` "anchors at the settings source, not the filesystem root". MCP allow globs must start with a literal `mcp__<server>__`.
- **Saved approvals:** "Yes, and don't ask again" writes to `.claude/settings.local.json` at the repository root.
- **Sandboxing:** OS-level, and applies "only to Bash, PowerShell, and Monitor commands and their child processes". With `autoAllowBashIfSandboxed` true (the default), sandboxed Bash runs without prompting. Use sandboxing *and* permissions together: "sandbox restrictions still apply even if a prompt injection bypasses Claude's decision-making" (permissions page search excerpt).
- **Managed settings:** `permissions.deny`, `sandbox.enabled`, `env`, `forceLoginMethod`/`forceLoginOrgUUID`, `claudeMd`, `strictKnownMarketplaces`, `blockedMarketplaces`, `pluginTrustMessage` and `disableBypassPermissionsMode`. Anthropic's table: "Use settings for technical enforcement and CLAUDE.md for behavioral guidance."
- **Hooks:** Anthropic points to "a PreToolUse hook" to "block an action regardless of what Claude decides". Hooks "execute as shell commands at fixed lifecycle events". Events seen this run: PreToolUse, SessionStart, InstructionsLoaded, UserPromptSubmit and PermissionRequest (2.1.280: "an agent-type hook no longer runs there"). The full event list and blocking exit-code semantics were not verified (section 9). The main risk is that repository-supplied hooks are code that runs on open. Check Point's CVE-2025-59536 began as "the malicious hooks vulnerability" (GHSA-ph6w-f82w-28w6, 29 August 2025).
- **Subagents, skills, plugins:** subagents can have their own `memory` and do not inherit main auto memory (except forks). Skills "only load when you invoke them or when Claude determines they're relevant". Plugins bundle "skills, agents, hooks, MCP servers, or LSP servers". See 4.7.
- **MCP configuration:** `.mcp.json` details were not verified this run. Relevant verified facts: MCP deny rules `mcp__*`; `requiresUserInteraction` tools are denied in `dontAsk`; the 2,048-character description cap.
- **Cloud (web) sessions:** only changelog-level facts were verified this run. Auto memory "is machine-local … not shared across machines or cloud environments". The full differences are in section 9.
- **Commit vs local (Anthropic):**
  - Commit: CLAUDE.md or .claude/CLAUDE.md ("Team members via source control"), `.claude/rules/`, and `.claude/settings.json` ("You can check permission settings into version control").
  - Keep local: `CLAUDE.local.md` (gitignored), `.claude/settings.local.json` (saved approvals, and `claudeMdExcludes` "so the exclusion stays local"), and `~/.claude/` user files.
  - Managed: the Project-instructions choice ("ignores it in project and local settings files").

### 4.4 Prompt injection against coding agents (Priority)

**Documented vectors and incidents:**
- **Repository files:** the Rules File Backdoor (hidden Unicode in `.cursor/rules` and `copilot-instructions.md`; Cursor and GitHub both said users are responsible). Claude Code project-file CVEs: CVE-2025-59536 (fixed in 1.0.111; "allows malicious code execution before user consent is granted", per SentinelOne, secondary) and CVE-2026-21852 (API key exfiltration, published 21 January 2026 per Check Point's timeline). CVE-2025-59041 (malicious `git config user.email`; fixed 1.0.105; "Thank you to the NVIDIA AI Red Team").
- **Untrusted content in context:** GHSA-xq4m-mc3c-vvg3 ($IFS parsing bypass of read-only validation; "Reliably exploiting this requires the ability to add untrusted content into a Claude Code context window"). CVE-2025-54795 (echo command bypass of approval, GHSA-x56v-x2h6-7j34, 1 August 2025).
- **MCP:** CVE-2025-6514 (mcp-remote 0.0.5–0.1.15, command injection from a malicious `authorization_endpoint`; fixed 0.1.16). CVE-2025-49596 (MCP Inspector below 0.14.1, unauthenticated proxy reachable by DNS rebinding). CVE-2025-54136 "MCPoison" in Cursor (secondary; fixed in Cursor 1.3).
- **Issues, PR text, web pages:** OWASP's Agentic ASI01 cites EchoLeak (CVE-2025-32711), per secondary summaries. Copilot code review reads instructions from the PR head branch (C8), which is an injection path through PR content. A primary-source catalogue of issue and PR-body attacks on coding agents was not completed this run.

**Mitigations (vendor and OWASP):** run untrusted repositories only after the trust dialog, and keep Claude Code updated (advisories say auto-update delivers fixes). Enforce with deny rules, sandbox and managed settings. Review AI-configuration files "with the same scrutiny as executable code" (Pillar). Use OWASP "Least Agency" (secondary summaries of the Agentic Top 10).

### 4.5 OWASP lists (Priority)

**LLM Top 10 2026** (ranking from CSA Labs, secondary; the official PDF was not parsed): LLM01 Prompt Injection; LLM02 Sensitive Information Disclosure; LLM03 Excessive Agency; LLM04 Supply Chain; LLM05 Data and Model Poisoning; LLM06 Unbounded Consumption; LLM07 Misinformation; LLM08 Hidden Context Exposure; LLM09 Vector and Embedding Weaknesses; LLM10 Improper Output Handling. OWASP says the edition maps risks to "NIST, MITRE ATLAS, CWE, and the OWASP Top 10 for Agentic Applications".

**Agentic Top 10 2026** (names from secondary summaries): ASI01 Agent Goal Hijack; ASI02 Tool Misuse & Exploitation; ASI03 Agent Identity & Privilege Abuse; ASI04 Agentic Supply Chain; ASI05 Unexpected Code Execution; ASI06 Memory & Context Poisoning; ASI07 Insecure Inter-Agent Communication; ASI08 Cascading Agent Failures; ASI09 Human-Agent Trust Exploitation; ASI10 Rogue Agents.

**Controls that apply to coding agents:**

| OWASP risk | Claude Code control |
|---|---|
| LLM01 / ASI01 | Treat repository, issue and web content as untrusted; sandbox network egress |
| LLM03 / ASI02 / ASI03 | Deny rules, `dontAsk`/Manual modes, and disabling bypass in managed settings |
| LLM04 / ASI04 | Marketplace allow-lists and `sha` pins |
| ASI05 | Sandbox, and no `bypassPermissions` outside containers |
| ASI06 | Review auto memory and CLAUDE.md changes in PRs |
| LLM02 / LLM08 | Keep secrets out of context |
| ASI09 | Do not approve prompts you cannot read |

This mapping is this report's analysis, not OWASP text.

### 4.6 MCP security (Priority)

**Specification.** The 2026-07-28 changes are in C1 and C2. The best practices page covers:
- **Confused deputy:** proxies with a static client ID plus dynamic registration plus consent cookies. Proxies "MUST implement per-client consent". The consent page must name the client, scopes and `redirect_uri`, and use CSRF protection and anti-framing. Redirect URIs need "exact string matching". `state` must be single-use and set only after consent.
- **Token passthrough:** "explicitly forbidden".
- **SSRF during OAuth discovery:** enforce HTTPS, block private and link-local ranges including `169.254.169.254`, use egress proxies, and watch for DNS rebinding.
- Session hijacking is also covered, per secondary summaries; that section was not read in full.

**Tool poisoning and rug pulls:** Invariant Labs' "MCP Security Notification: Tool Poisoning Attacks" (invariantlabs.ai) shows that a malicious server can "hijack the agent's behavior and override instructions provided by other, trusted servers". Invariant's invariantlabs-ai/mcp-injection-experiments repository includes "a sleeper rug pull, i.e. an MCP server that changes its tool interface only on the second load to a malicious one."

**Vetting an MCP server (this report's checklist, drawn from the sources above):**
- Is it on the official registry, from a known publisher?
- Is the version pinned?
- Is remote transport HTTPS-only, with OAuth tokens audience-bound to that server?
- Does it avoid deprecated DCR, HTTP+SSE, Sampling and Roots?
- Are its tool descriptions within Claude Code's 2,048-character cap, and read before approval?
- Is it free of the known CVEs (mcp-remote ≥ 0.1.16, Inspector ≥ 0.14.1)?

**Official MCP Registry:** listed in the spec site navigation ("Registry"); status, date and moderation policy were **not verified** this run.

### 4.7 Skills and plugins as a supply chain (Priority)

**What a malicious plugin can do.** Anthropic's plugin page says: "Plugins and marketplaces are highly trusted components that can execute arbitrary code on your machine with your user privileges." (This sentence comes from a search excerpt of the official page and could not be confirmed in the fetched text; the confirmed warning is "Anthropic doesn't control what MCP servers, files, or other software are included in plugins and can't verify that they work as intended.") A plugin can ship hooks (code on lifecycle events), MCP and LSP servers (processes), skills (instructions that steer the agent) and agents.

**Controls:**
- `strictKnownMarketplaces` (managed only). Undefined means no restrictions; `[]` means lockdown; a list is an allow-list. It "matches the marketplace a plugin comes from, not the entries inside it". Use `disableCommandPluginSources` to block command sources. Plugins synced from claude.ai are not covered.
- `blockedMarketplaces`, with the owner-wildcard form `untrusted-org/*` (v2.1.223+). Both lists are enforced on "marketplace add and on plugin install, update, refresh, and auto-update".
- Pinning: git plugin sources take `sha` (a full 40-character commit), and `sha` wins over `ref`. Marketplace sources support `ref` but not `sha`. Archives take `sha256`. The community marketplace pins "Each plugin … to a specific commit SHA".
- 2.1.278 and 2.1.280 fixes: see F19–F20; also "`installed_plugins.json` keeping the install-time commit after updating".

**Published analyses:** Snyk ToxicSkills (C11; 76 confirmed malicious). Koi Security (1 February 2026): 341 of 2,857 malicious, 335 from ClawHavoc. Antiy CERT's own ClawHavoc report (5 February 2026) says it "identified 1,184 malicious skill packages within ClawHub's historical repository, attributed to 12 author IDs", and names the malware family Trojan/OpenClaw.PolySkill. OWASP's Agentic Skills Top 10 project (lead Ken Huang, CC BY-SA 4.0) released version 1.0 on 17 August 2026, according to the project lead's press release and Mend.io. The 27 April 2026 date reported by obot.ai is not supported.

### 4.8 Hidden-text attacks (Standard)

Pillar's payload used "bidirectional text markers and zero-width joiners" (SC Media, secondary). GitHub.com warns on hidden Unicode (F38). Claude Code 2.1.280 removes invisible characters from prompts. The VS Code extension now strips "invisible Unicode formatting and tag characters … from pasted text". A fix keeps ZWNJ for Persian and Arabic, so blanket stripping has false positives. The tag range U+E0000–U+E007F is cited by secondary sources (HackerDNA). Trojan Source (CVE-2021-42574), homoglyph detection and CI tools were **not covered** this run.

**Recommended CI pattern (this report's analysis):** fail when agent-instruction files (AGENTS.md, CLAUDE.md, `.claude/**`, `.cursor/rules/**`, `.github/*instructions*`, `SKILL.md`) contain code points in U+200B–U+200F, U+202A–U+202E, U+2066–U+2069, U+FEFF or U+E0000–U+E007F. Allow U+200C only by exception.

### 4.9 Secrets and agents (Standard)

Anthropic says Read and Edit deny rules cover built-in tools, recognised Bash file commands (`cat`, `head`, `tail`, `sed`, `tee`) and redirections. They do *not* cover "a command that reads files without naming them, such as `grep -r pattern .`" or "a Python or Node script that opens files itself". Hence: "For OS-level enforcement that blocks all processes from accessing a path, enable the sandbox." A secondary source (a GitHub issue citing Anthropic's sandbox docs) says the sandbox "grants read access to the entire machine except explicitly denied paths". Add deny-read for `~/.ssh`, `~/.aws` and `**/.env*`. Claude Code 2.1.280 keeps "renamed copies of key files, such as `id_rsa copy` or `kubeconfig (1).yaml`" local during `/ultrareview` uploads. CVE-2026-21852 shows API keys leaking through project configuration. Secret scanning and short-lived credential guidance from primary sources were **not covered**.

### 4.10 Testing agent instructions (Standard)

Anthropic-documented checks:
- `/context` (Memory files);
- `/memory` (lists AGENTS.md from v2.1.280);
- the `InstructionsLoaded` hook, which does not fire for a directly-read AGENTS.md;
- `/doctor` trims;
- `claude --debug` for rule YAML errors.

Signs of trouble: the file is missing from `/context`; there are conflicting rules; instructions are lost after `/compact` (nested files and path rules reload only on matching reads).

Evaluation method from the literature: McMillan measured compliance with "a trivial target annotation" across 1,650 sessions, using mixed-effects models. Replicate this cheaply by adding a canary convention and measuring the rate. Gloaguen found that context files "encouraged broader exploration" (secondary summary). **Position:** test adherence per task type and over long sessions, where drift appears, rather than tuning file length.

### 4.11 Government guidance (Standard)

**Not covered** in primary sources this run. The only verified link is indirect: OWASP LLM Top 10 2026 maps to "NIST AI 600-1 (Generative AI Profile), NIST AI RMF" (cybersecuritynews.com, secondary). See section 9.

### 4.12 What professional teams put in context files (Standard)

agents.md recommends "Project overview; Build and test commands; Code style guidelines; Testing instructions; Security considerations", plus PR and commit rules. Public examples it links: openai/codex, apache/airflow, temporalio/sdk-java and PlutoLang/Pluto. "The main OpenAI repo has 88 AGENTS.md files" (at time of writing). Anthropic adds verifiable commands, pitfalls and rationale, and says to leave out derivable layouts. The contents of those example files were not fetched this run.

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| Claude Code | Coding agent | 2.1.280 | 2026-09-22 | `claude update`; check with `claude --version` | `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`, managed-settings.json | https://code.claude.com/docs/en/changelog |
| MCP specification | Protocol | 2026-07-28 | 2026-07-28 | — | — | https://modelcontextprotocol.io/specification/2026-07-28 |
| MCP Inspector | MCP debugging UI | ≥ 0.14.1 required (current: not found) | fix 2025-06-13 (secondary) | not verified | — | https://thehackernews.com/2025/07/critical-mcp-remote-vulnerability.html |
| mcp-remote | Remote MCP proxy | ≥ 0.1.16 required (current: not found) | fix 2025-06-17 (secondary) | not verified | — | https://github.com/advisories/GHSA-6xpm-ggf7-wc3p |
| OpenAI Codex CLI | Coding agent | not found (0.154.0 observed, secondary) | not found | not verified | `config.toml` (`project_doc_max_bytes`) | https://developers.openai.com/codex/guides/agents-md |
| Gemini CLI | Coding agent | not found | not found | not verified | `.gemini/settings.json` | https://geminicli.com/docs/cli/gemini-md/ |
| Aider | Coding agent | not found | not found | not verified | `.aider.conf.yml` | https://agents.md/ |

## 6. Changing in the next 12 months

- **MCP deprecations (flag):** Roots, Sampling and Logging, plus the legacy HTTP+SSE transport, "keep working for at least twelve months" from 28 July 2026. Removal is possible from about late July 2027, just outside 12 months, but migrate now. DCR is deprecated and "will be removed in a future version". The next spec release date is not found (roadmap post, 22 August 2026).
- **Claude Code:** rolling releases; no end-of-support date found. AGENTS.md on Bedrock, Vertex and Foundry is described as "not yet", with no date found. The `/memory` listing of AGENTS.md changed in 2.1.280. Pro and Team Standard defaults changed to Opus. Opus 5.5 is the default Opus model.
- **Gemini CLI:** already replaced by Antigravity CLI for unpaid-tier and Google One users (18 June 2026). Status for paid users is not found.
- **OWASP:** LLM Top 10 2026 supersedes 2025. Update any "LLM06 Excessive Agency" references to LLM03, and "LLM07 System Prompt Leakage" to LLM08 Hidden Context Exposure.
- **AAIF:** Agent2Agent joined AAIF (announced 17 August 2026, per Forbes, secondary).

## 7. Common mistakes (including by AI coding assistants)

1. **Treating CLAUDE.md or AGENTS.md as a security control.** Anthropic: "not a hard enforcement layer".
2. **Adding CLAUDE.local.md to an AGENTS.md-only repository,** which silently switches Claude Code off AGENTS.md (C4).
3. **Believing imports shrink context.** "doesn't reduce context".
4. **Adding frontmatter fields other than `paths` to rules** (for example Cursor-style `globs` or `alwaysApply`), which are "ignored without an error".
5. **Writing `Bash(git * main)` or `Bash(devbox run *)` allow rules,** which match far more than intended.
6. **Relying on `Read(./.env)` alone.** `grep -r` and scripts bypass it; add the sandbox.
7. **Writing `mcp__server__tool(param)` rules in settings files.** Claude Code "skips any `mcp__` rule that has parentheses".
8. **Symlinking CLAUDE.md → AGENTS.md in a repository with Windows contributors.**
9. **Citing MCP 2025-11-25 or OWASP LLM 2025 as current.** AI assistants trained before mid-2026 will do this by default.
10. **Assuming a malformed `strictKnownMarketplaces` entry fails closed.** Before 2.1.277 it disabled the whole policy.
11. **Quoting "200 lines" as a CLAUDE.md truncation limit.** The truncation applies to MEMORY.md.
12. **Letting a PR edit `.github/*instructions*` and relying on Copilot code review of that same PR,** since review reads the head branch.

## 8. Sources and licences

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| code.claude.com docs (memory, permissions, changelog, plugin-marketplaces) | Not found (treat as all rights reserved) | Brief quotes only | Yes | No; write your own examples | "Anthropic, Claude Code Docs, <URL>, read 2026-09-23" |
| anthropics/claude-code advisories (GitHub) | Repository licence not verified | Brief | Yes | No | Advisory ID + URL |
| agents.md | LF Projects terms; content licence not verified | Brief | Yes | Trivial config snippets (factual) with attribution | "AGENTS.md, a Series of LF Projects, LLC" |
| Linux Foundation press release | Not found | Brief | Yes | n/a | LF + date |
| modelcontextprotocol.io spec, blog, best practices | Not verified (MCP.Directory, secondary, says contributions are Apache 2.0) | Brief | Yes | Only after verifying licence | "Model Context Protocol, <URL>" |
| GitHub Docs (Copilot) | Not verified this run | Brief | Yes | After verifying | GitHub Docs + URL |
| geminicli.com / gemini-cli repository | Not verified | Brief | Yes | After verifying | Google + URL |
| developers.openai.com Codex docs | Not found | Brief | Yes | No | OpenAI + URL |
| OWASP GenAI (LLM 2026, Agentic 2026) | CC BY-SA 4.0 ("all content on the site is Creative Commons Attribution-ShareAlike v4.0") | Yes | Yes | Adaptations must be CC BY-SA 4.0. Keep them out of Apache-2.0 files, or in a separately licensed file | "OWASP GenAI Security Project, CC BY-SA 4.0, <URL>" plus a changes note |
| arXiv:2602.11988 (Gloaguen et al.) | CC BY 4.0 | Yes | Yes | Yes, with attribution | Authors, title, arXiv ID, CC BY 4.0 |
| arXiv:2605.10039 (McMillan) | CC BY 4.0 (arXiv licence link) | Yes | Yes | Yes, with attribution | As above |
| arXiv:2601.20404 (Lulla et al.) | Not verified | Brief | Yes | No until verified | Authors + arXiv ID |
| Pillar Security blog | Proprietary (assumed; no licence found) | Brief | Yes | No | Pillar Security + URL + date |
| Snyk, Check Point, JFrog, SentinelOne blogs | Proprietary (no licence found) | Brief | Yes | No | Vendor + URL |
| Secondary summaries (CSA Labs, DeepTeam, Cycode, HackerDNA, devops.com, Forbes) | Proprietary | Brief | Yes, labelled secondary | No | Publisher + URL |

## 9. Not found, contested, not covered

**Contested**
- CLAUDE.md length and adherence. Anthropic: "Longer files consume more context and reduce adherence". McMillan (arXiv:2605.10039): no detectable effect of 25–500 lines, with Bayes factors supporting the null.
- Whether context files help. Gloaguen (arXiv:2602.11988): no general gain in success, and over 20% higher cost. Lulla (arXiv:2601.20404): faster and fewer output tokens, with comparable completion. These are different metrics; both can hold.
- Codex 32 KiB: combined size (AGENTS.md guide) vs per file (config-advanced page).
- OWASP LLM 2026 publication date: 3 August (OWASP resource page) vs 4 August (OWASP GitHub README) vs 2 September (press release).
- ASI04 name: "Agentic Supply Chain Vulnerabilities" vs "Agentic Supply Chain Compromise" in secondary sources.

**Not found**
- End-of-support dates for Claude Code, Codex, Gemini CLI and Aider.
- The next MCP spec date.
- Current versions of MCP Inspector, mcp-remote, Codex, Gemini CLI and Aider.
- Licences for Anthropic docs, MCP docs, GitHub Docs, agents.md and arXiv:2601.20404.
- Size limits for Copilot and Gemini instruction files.
- Antigravity CLI context-file behaviour.
- CVE-2025-53773 was resolved after the main pass. Microsoft MSRC lists it as "GitHub Copilot and Visual Studio Remote Code Execution Vulnerability": "command injection" that "allows an unauthorized attacker to execute code locally". It was fixed in the August 2025 Patch Tuesday. Embrace The Red reported it on 29 June 2025; the injection switches .vscode/settings.json into "YOLO mode".

**Not covered (ran out of budget)**
- Cursor `.mdc` rule format and precedence.
- Claude Code hooks: full event list, exit-code and blocking semantics.
- `.mcp.json` scopes and approval.
- Subagent and skill frontmatter.
- Claude Code on the web: differences and a primary-source security page.
- The official MCP Registry (status and vetting).
- Tool-poisoning and rug-pull research beyond Invariant Labs' notification and its mcp-injection-experiments repository.
- Trojan Source (CVE-2021-42574), homoglyph detection and CI tooling.
- Secret-scanning and short-lived-credential guidance.
- NIST AI 100-2, NIST AI 600-1 and CISA guidance.
- The content of named public AGENTS.md and CLAUDE.md examples.
- The official OWASP PDFs, whose per-item control text was not parsed.