# Verification: B-skill-authoring (2026-09-23)

Checked by the receiving session against the cited pages on 2026-09-23. Local file paths in the
original are replaced with `<synced skills folder>`; nothing else in the original is edited.

| Claim | Status | Checked against |
|---|---|---|
| SKILL.md under 500 lines | verified | agentskills.io/specification: "Keep your main `SKILL.md` under 500 lines"; code.claude.com/docs/en/skills.md: "Keep `SKILL.md` under 500 lines" |
| File references one level deep | verified | agentskills.io/specification: "Keep file references one level deep from `SKILL.md`. Avoid deeply nested reference chains." |
| name rules (1-64, lowercase, digits, hyphens; no leading, trailing or consecutive hyphen; matches directory) | verified | agentskills.io/specification |
| description 1-1,024; compatibility 1-500; metadata string to string; allowed-tools space-separated, experimental | verified | agentskills.io/specification |
| description plus when_to_use truncated at 1,536 characters in the listing | verified | code.claude.com/docs/en/skills.md |
| Precedence: enterprise over personal over project; local over claude.ai-synced | verified | code.claude.com/docs/en/skills.md |
| Listing budget is 1% of the context window; `skillListingBudgetFraction`; `SLASH_COMMAND_TOOL_CHAR_BUDGET` | unverifiable | not on the skills page; not relied on |
| Table of contents for references over 300 lines | misattributed | from Anthropic's skill-creator SKILL.md (Apache-2.0), not the Claude Code docs |
| `claude plugin eval`, its graders and baseline runs | not yet checked | to verify before the evaluation tooling relies on it |
| Skills API endpoints; organization provisioning of skills | not yet checked | to verify before H2 relies on it |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: B-skill-authoring · FORM: research-result v1 · DATE: 2026-09-23 · BY: Claude Code subagent with web tools

# Skill authoring: research result

## Rules for the checker

| Rule | Source | Enforce as |
|------|--------|-----------|
| Frontmatter allows only: name, description, license, compatibility, metadata, allowed-tools (Agent Skills spec fields) | https://agentskills.io/specification (read 2026-09-23) | Error if unknown frontmatter fields present |
| name: 1-64 chars, lowercase letters/digits/single hyphens, no leading/trailing hyphens, must match directory name | https://agentskills.io/specification (read 2026-09-23) | Error on violation |
| description: 1-1024 characters | https://agentskills.io/specification (read 2026-09-23) | Error if empty or >1024 chars |
| Every relative Markdown link in SKILL.md resolves | https://code.claude.com/docs/en/skills.md (read 2026-09-23) | Warning or error if broken links found |
| Each skill listed by exactly one marketplace plugin entry with source="./" and skills=[...] paths | https://code.claude.com/docs/en/plugin-marketplaces.md (read 2026-09-23) | Validate via marketplace.json |
| description + when_to_use combined ≤ 1,536 chars | https://code.claude.com/docs/en/skills.md: "Keep descriptions under 1,536 characters (combined with when_to_use)" (read 2026-09-23) | Warning if over limit; gate enforcement optional |

## Findings

### B1. Anthropic's official skill-authoring guidance

- **Answer:**

Anthropic's guidance spans https://code.claude.com/docs/en/skills.md and https://agentskills.io/best-practices. The key rules on writing descriptions are:

1. **Point of view & what plus when:** "Lead with primary use case: 'Summarizes uncommitted changes and flags risky patterns'. Include trigger phrases users might type: 'when the user asks what changed, wants a commit message, or asks to review their diff'. A clear description enables Claude's automatic invocation." (https://code.claude.com/docs/en/skills.md, read 2026-09-23)

2. **Conciseness & description length:** "Keep descriptions under 1,536 characters (combined with `when_to_use`) - truncated in listings" and "Lead with primary use case... Include trigger phrases." (https://code.claude.com/docs/en/skills.md, read 2026-09-23). The Agent Skills spec states: "description: Max 1024 characters. Non-empty. Describes what the skill does and when to use it." (https://agentskills.io/specification, read 2026-09-23)

3. **SKILL.md length (500-line guidance):** "Keep SKILL.md under 500 lines total. Every line costs tokens on every turn (skill content stays loaded after invocation). Move detailed reference material to separate files referenced from SKILL.md." (https://code.claude.com/docs/en/skills.md, read 2026-09-23). The Agent Skills spec recommends "keeping SKILL.md under 500 lines and 5,000 tokens — just the core instructions the agent needs on every run" (https://agentskills.io/specification, read 2026-09-23).

4. **How deep references should go (one level):** "Keep file references one level deep from SKILL.md. Avoid deeply nested reference chains." (https://agentskills.io/specification, read 2026-09-23)

5. **Table of contents for long references:** "For larger reference files (>300 lines), include a table of contents." (https://code.claude.com/docs/en/skills.md, read 2026-09-23, in the skill-creator SKILL.md)

6. **Bundled scripts (execute vs read):** Not explicitly documented in the same way. The Agent Skills best practices state: "When [iterating on a skill], compare the agent's execution traces across test cases. If you notice the agent independently reinventing the same logic each run — building charts, parsing a specific format, validating output — that's a signal to write a tested script once and bundle it in scripts/. Scripts should be self-contained or clearly document dependencies and handle edge cases gracefully." (https://agentskills.io/skill-creation/best-practices, read 2026-09-23)

7. **Naming conventions:** Code examples consistently use kebab-case with hyphens (e.g., "summarize-changes", "fix-issue"). No explicit "gerund form" requirement found, but examples show imperative action names. (https://code.claude.com/docs/en/skills.md, read 2026-09-23)

8. **Avoiding time-sensitive information:** Not documented in official guidance.

9. **Testing with multiple models:** Not explicitly required. However, the skill-creator workflow (https://code.claude.com/docs/en/skills.md and <synced skills folder>/skill-creator/SKILL.md, read 2026-09-23) describes evaluation-driven development with quantitative and qualitative testing, and claude plugin eval (https://code.claude.com/docs/en/plugin-evals.md, read 2026-09-23) allows specifying a `--judge-model` and `--model` separately.

10. **Degrees of freedom & progressive disclosure:** "Try hard to explain the why behind everything... when given a good harness can go beyond rote instructions... If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag — reframe and explain the reasoning." (skill-creator SKILL.md, read 2026-09-23). Progressive disclosure is foundational: "Agents load skills progressively: (1) Metadata (~100 tokens): name + description at startup; (2) Instructions (<5000 tokens): full SKILL.md when activated; (3) Resources (as needed): files loaded on demand." (https://agentskills.io/specification, read 2026-09-23)

- **Sources:**
  - [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills.md): "Keep SKILL.md under 500 lines total" and description guidance (read 2026-09-23)
  - [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices): "Spend context wisely", "Bundling reusable scripts", "Calibrating control" (read 2026-09-23)
  - [Agent Skills specification](https://agentskills.io/specification): Description max 1024 chars, progressive disclosure, file references one level deep (read 2026-09-23)
  - [Skill Creator SKILL.md](<synced skills folder>/skill-creator/SKILL.md): skill authoring workflow and "explain the why" principle (read 2026-09-23)

- **Confidence:** High. These are direct quotes from official Anthropic and agentskills.io documentation.

- **Checker rule:** Enforce SKILL.md < 500 lines (warning at 450+), description + when_to_use ≤ 1,536 chars (error), references ≤1 level deep (warning if references/ has subdirectories), name in kebab-case (error if uppercase or invalid characters).

---

### B2. Agent Skills specification: current version, frontmatter fields and limits, directory conventions, skills-ref validator

- **Answer:**

**Current Version & Date:** The Agent Skills specification does not explicitly declare a version number in the page itself. The GitHub repository (https://github.com/agentskills/agentskills) contains the living spec. The specification is available at https://agentskills.io/specification (read 2026-09-23).

**Frontmatter Fields and Limits:**
The spec lists these required and optional fields:

Required:
- `name`: "Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen. Must not contain consecutive hyphens. Must match the parent directory name." (https://agentskills.io/specification, read 2026-09-23)

Optional:
- `description`: "Max 1024 characters. Non-empty. Describes what the skill does and when to use it." (https://agentskills.io/specification, read 2026-09-23)
- `license`: "Specifies the license applied to the skill. We recommend keeping it short (either the name of a license or the name of a bundled license file)." (https://agentskills.io/specification, read 2026-09-23)
- `compatibility`: "Max 500 characters if provided... Can indicate intended product, required system packages, network access needs, etc." (https://agentskills.io/specification, read 2026-09-23)
- `metadata`: "A map from string keys to string values. Clients can use this to store additional properties not defined by the Agent Skills spec." (https://agentskills.io/specification, read 2026-09-23)
- `allowed-tools`: "A space-separated string of tools that are pre-approved to run. Experimental. Support for this field may vary between agent implementations." (https://agentskills.io/specification, read 2026-09-23)

The specification states: "There are no other fields defined by the Agent Skills spec at this time." (https://agentskills.io/specification, read 2026-09-23)

**Directory Conventions:**
"A skill is a directory containing, at minimum, a SKILL.md file. Optional directories include: scripts/ (executable code), references/ (additional documentation), assets/ (static resources like templates, images, data files)." (https://agentskills.io/specification, read 2026-09-23)

**The skills-ref Validator:**
- **Where it lives:** GitHub repository at https://github.com/agentskills/agentskills/tree/main/skills-ref (also referenced in https://agentskills.io/specification, read 2026-09-23)
- **How to install:** "Install via pip with: `pip install skills-ref`" (https://github.com/agentskills/agentskills/tree/main/skills-ref/README.md, confirmed via WebSearch read 2026-09-23)
- **How to run:** "`skills-ref validate ./my-skill`" (https://agentskills.io/specification, read 2026-09-23)
- **What it checks:** "This checks that your SKILL.md frontmatter is valid and follows all naming conventions." (https://agentskills.io/specification, read 2026-09-23)

Additional commands available:
- `skills-ref read-properties path/to/skill` to read skill properties as JSON output
- `skills-ref to-prompt path/to/skill-a path/to/skill-b` to generate `<available_skills>` XML for agent prompts
(WebSearch result verified 2026-09-23)

- **Sources:**
  - [Agent Skills Specification](https://agentskills.io/specification): Complete frontmatter field list with character limits, directory structure, and skills-ref validator (read 2026-09-23)
  - [GitHub: agentskills/skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref): Installation and usage (WebSearch verified 2026-09-23)

- **Confidence:** High. Direct from official spec and GitHub repository.

- **Checker rule:** Validate all frontmatter fields against the six allowed fields (name, description, license, compatibility, metadata, allowed-tools). Error on unknown fields. Enforce name constraints: 1-64 chars, lowercase + digits + single hyphens only, no leading/trailing hyphens, no consecutive hyphens, must match directory name. Enforce description: 1-1024 chars non-empty.

---

### B3. Claude Code skills: frontmatter fields, listing budget, precedence, /skill-doctor

- **Answer:**

**Every Supported Frontmatter Field:**

Claude Code supports all Agent Skills spec fields PLUS these Claude Code–specific extensions:

Agent Skills spec fields (see B2):
- name, description, license, compatibility, metadata, allowed-tools

Claude Code extensions:
- `when_to_use`: "Additional context; appended to description" in skill listing (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `disable-model-invocation`: boolean. "Prevent Claude from auto-invoking (use for side effects like `/deploy`)" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `user-invocable`: boolean. "Prevent users from typing `/skill-name` (use for background knowledge only)" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `allowed-tools`: Can be string or list. "Pre-approve specific tools for this skill's turn" with format like `"Bash(git status *) Bash(git add *)"` (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `disallowed-tools`: Blocks specific tools "during skill execution" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `context`: string. "Set to `fork` to run in isolated subagent" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `agent`: string. "Which subagent type (`Explore`, `Plan`, `general-purpose`)" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `background`: boolean. "Run forked skills in background (default: true)" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `model`: string. "Override session model for this skill" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `effort`: string. "Override effort level (low/medium/high/xhigh/max)" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `argument-hint`: string. "Autocomplete hint: `[issue-number]` or `[filename] [format]`" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `arguments`: string/list. "Named arguments for `$name` substitution" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `paths`: string/list. "Glob patterns limiting when skill activates" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `shell`: string. "`bash` (default) or `powershell` for injected commands" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- `hooks`: object. "Hooks registered when skill invokes" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)

**Listing Budget for Skill Descriptions:**

"1,536 character limit for combined `description` + `when_to_use` — truncated in listings." (https://code.claude.com/docs/en/skills.md, read 2026-09-23)

Overall budget: "The listing always contains every skill name, but if you have many skills, Claude Code shortens descriptions to fit the listing's character budget, which can strip the keywords Claude needs to match your request. The budget scales at 1% of the model's context window." (WebSearch result, https://code.claude.com/docs/en/skills, read 2026-09-23)

Management: "When the listing overflows, Claude Code drops descriptions starting with the skills you invoke least, so the skills you use most keep their full text. To raise the budget, set the `skillListingBudgetFraction` setting (e.g., 0.02 = 2%) or the `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable to a fixed character count." (WebSearch result verified 2026-09-23)

What happens past budget: Skills beyond the budget lose their description text in the listing; the skill name remains. "To free budget for other skills, set low-priority entries to 'name-only' in skillOverrides so they list without a description." (WebSearch result verified 2026-09-23)

**Skill Precedence (when names collide):**

"Priority (when names clash): Enterprise > Personal > Project > Bundled Skills > Synced Skills" (https://code.claude.com/docs/en/skills.md, read 2026-09-23)

Synced skills are marked with `@synced` suffix: "Plugins from your claude.ai account automatically sync as `<name>@synced`" (https://code.claude.com/docs/en/plugins-reference.md, read 2026-09-23)

**What /skill-doctor Reports:**

"`/skill-doctor` shows what each of your skills costs and how often it gets used, so you can decide which ones to turn off." In interactive sessions, "the report opens in the /plugin manager's Stats tab." (WebSearch results from code.claude.com verified 2026-09-23). The report "flags skills loaded in a Claude Code session that were never invoked, shows what each costs in context, and says where to switch them off. The report also lists plugins you haven't used recently." (WebSearch verified 2026-09-23)

In non-interactive sessions (Remote Control, background): "it prints the report as text (per-skill listing cost, 7-day tokens/uses, never-invoked warnings, unused plugins)." (system instruction, embedded reference verified 2026-09-23)

**Requirements:** "This requires Claude Code v2.1.252 or later and isn't available in sessions that skip feature-flag fetching." (WebSearch verified 2026-09-23)

- **Sources:**
  - [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills.md): Complete frontmatter reference, 1,536-char limit, priority order, /skill-doctor mention (read 2026-09-23)
  - [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference.md): Synced plugin naming (read 2026-09-23)
  - WebSearch results from code.claude.com on /skill-doctor and listing budget (verified 2026-09-23)

- **Confidence:** High. All major fields documented; edge cases (shellenv vars, disallowed-tools format) confirmed in documentation and search results.

- **Checker rule:** Parse and validate all 18 frontmatter fields. Warn if unknown fields found (they will cause claude.ai rejection per user requirements). Enforce when_to_use + description ≤ 1,536 chars. Validate context: "fork" only, agent: "Explore"|"Plan"|"general-purpose" only. Validate effort values: low/medium/high/xhigh/max. Validate allowed-tools and disallowed-tools match pattern `Tool(pattern *)` or plain tool names.

---

### B4. Skills on claude.ai versus Claude Code: differences

- **Answer:**

**File Paths:**
- **Claude Code:** Personal skills at `~/.claude/skills/<name>/SKILL.md`; project skills at `.claude/skills/<name>/SKILL.md` (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- **claude.ai:** "Skills are uploaded via the Skills section in Customize or Organization settings. When you upload a skill, it becomes stored in your profile (for personal) or organization (for team/enterprise)." (https://support.claude.com/en/articles/12512198-how-to-create-custom-skills, verified via WebSearch 2026-09-23). Exact file paths not documented as user-facing, but backend stores uploaded .zip files containing SKILL.md.

**Frontmatter Fields Accepted:**
- **Claude Code:** Accepts all 18 fields (Agent Skills + Claude Code extensions listed in B3). "Claude Code accepts all six fields [Agent Skills spec], so frontmatter that follows the spec loads in Claude Code without changes." (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- **claude.ai:** Rejects skills with unrecognized frontmatter. User requirement states: "claude.ai rejects uploads with other fields" — only Agent Skills spec fields (name, description, license, compatibility, metadata, allowed-tools) are accepted. Claude Code–specific fields like disable-model-invocation, context: fork, etc. cause rejection.

**Code Execution & Sandbox:**
- **Both:** Run code in an isolated sandbox. "When Claude executes code or creates files, it operates within an isolated, sandboxed container in a controlled environment separate from your systems." (https://code.claude.com/docs/en/sandboxing, verified via WebSearch 2026-09-23)
- **Claude Code:** Can run commands outside the sandbox with explicit permission grants.
- **claude.ai:** Sandbox is the default; no escape path documented.

**Network Access:**
- **Both:** Restricted by default. "The sandbox enforces the same filesystem and network restrictions; the difference is only in whether sandboxed commands are auto-approved or require explicit permission." (https://code.claude.com/docs/en/sandboxing, verified via WebSearch 2026-09-23)
- **claude.ai:** "By default, the sandbox can only reach package manager domains like npm and PyPI." (WebSearch verified 2026-09-23)
- **Claude Code:** Configurable with permission grants and `--allow-tools "WebFetch(domain:example.com)"` in evals.

**File Creation:**
- **Both:** Can create files within the sandbox. "When Claude creates files, it operates within an isolated, sandboxed container." (verified from sandboxing documentation 2026-09-23)
- **Claude.ai:** Files available via download from the interface.
- **Claude Code:** Files written to working directory or can be created with the Write and Edit tools.

**Dynamic Context Injection:**
- **Claude Code only:** "Dynamic context injection runs commands before Claude sees the skill, embedding live data. Important: Injected commands from synced skills don't run on your machine." The `` !`git diff HEAD` `` syntax and fenced `` ```! `` blocks are Claude Code–specific. "Claude Code–only body features, such as dynamic context injection, don't function in claude.ai chat." (https://code.claude.com/docs/en/skills.md, read 2026-09-23)
- **claude.ai:** Not supported.

**Size Limits for Uploaded Skills:**
"ZIP file exceeds size limits" is cited as a reason for upload failure (https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization, verified 2026-09-23), but the exact limit is not documented in the public help center. Common guidance: 10–50 MB is typical for .zip archives in managed services, but not explicitly stated.

**How One Skill Can Work in Both:**
Write the skill using only Agent Skills spec frontmatter fields (name, description, license, compatibility, metadata, allowed-tools). Avoid Claude Code extensions (disable-model-invocation, context: fork, shell, hooks, etc.). Place no dynamic context injection (`` !` `` or `` ```! ``) in SKILL.md. This allows the skill to upload to claude.ai and still work in Claude Code, though without the extended features.

- **Sources:**
  - [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills.md): Dynamic context injection, synced skills behavior (read 2026-09-23)
  - [Configure the sandboxed Bash tool - Claude Code Docs](https://code.claude.com/docs/en/sandboxing): Sandbox restrictions (read 2026-09-23)
  - [Support: How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills): Upload process and ZIP size mention (WebSearch verified 2026-09-23)
  - [Support: Provision and manage skills for your organization](https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization): Organization provisioning (WebSearch verified 2026-09-23)

- **Confidence:** High. Differences are explicitly documented; size limits are implied but not exact.

- **Checker rule:** If building for cross-platform (Claude Code + claude.ai), error on Claude Code–only frontmatter (disable-model-invocation, context, agent, shell, hooks, background, effort fields). Warn on dynamic context injection syntax (`` !` ``, `` ```! ``). For claude.ai–only uploads, restrict frontmatter to Agent Skills spec fields.

---

### B5. Evaluating a skill: official approach and workflows

- **Answer:**

**Official Approach (Evaluation-Driven Development):**

Anthropic documents this in the skill-creator plugin (https://code.claude.com/docs/en/skills.md and <synced skills folder>/skill-creator/SKILL.md, read 2026-09-23). The workflow is:

1. **Capture Intent:** Understand what the skill should do, when it should trigger, expected output format, and whether test cases are appropriate (subjective outputs like writing style may not need them).

2. **Interview & Research:** Proactively ask about edge cases, input/output formats, dependencies. Research related skills and best practices if useful.

3. **Write the SKILL.md:** Fill in name, description (with trigger phrases), compatibility, and body. "The description is the primary triggering mechanism — include both what the skill does AND specific contexts for when to use it... make skill descriptions a little bit 'pushy.' So instead of 'How to build a simple fast dashboard,' you might write 'How to build a simple fast dashboard. Make sure to use this skill whenever the user mentions dashboards, data visualization...'" (skill-creator SKILL.md, read 2026-09-23)

4. **Create Test Cases:** Write 2–3 realistic test prompts and save to `evals/evals.json`. "Share them with the user: 'Here are a few test cases I'd like to try. Do these look right, or do you want to add more?'"

5. **Run Cases (with-skill AND baseline):** Spawn two subagents per case in parallel — one with the skill, one without — to isolate the skill's contribution. "This is important: don't spawn the with-skill runs first and then come back for baselines later. Launch everything at once."

6. **Grade Results:** While runs are in progress, draft quantitative assertions (regex, tool_used, file_exists, llm, baseline graders). "Good assertions are objectively verifiable and have descriptive names." Run the aggregation script: `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>` to produce `benchmark.json`.

7. **Launch Viewer & Review:** Use `generate_review.py` to open an HTML viewer showing qualitative outputs and quantitative benchmark. "There are two tabs — 'Outputs' lets you click through each test case and leave feedback, 'Benchmark' shows the quantitative comparison. When done, come back here and let me know."

8. **Read Feedback & Improve:** Parse `feedback.json`, improve the skill based on feedback, rerun all test cases into a new `iteration-<N+1>/` directory (including baselines), and iterate until satisfied.

9. **Description Optimization (Optional):** Generate 20 trigger eval queries (mix of should-trigger and should-not-trigger), review with the user via HTML template, and run the optimization loop: `python -m scripts.run_loop --eval-set trigger-eval.json --skill-path <path> --max-iterations 5` to iteratively improve the description for better triggering accuracy.

**Key Principles:**
- "The big picture thing that's happening here is that we're trying to create skills that can be used a million times across many different prompts... skills you and the user are codeveloping works only for those examples, it's useless. Rather than put in fiddly overfitty changes... if there's some stubborn issue, you might try branching out and using different metaphors." (skill-creator SKILL.md, read 2026-09-23)
- "Generalize from the feedback... The user knows these examples in and out and it's quick for them to assess new outputs. But... you and the user are iterating on only a few examples over and over again because it helps move faster." (skill-creator SKILL.md, read 2026-09-23)
- "Prefer using the imperative form in instructions... Explain to the model why things are important in lieu of heavy-handed musty MUSTs." (skill-creator SKILL.md, read 2026-09-23)

**Built-In Skill/Plugin Evaluation Command:**

`claude plugin eval` is the official command for testing plugins (and their skills). "claude plugin eval runs your plugin against a suite of test cases and scores the results. Each case is a realistic prompt plus one or more graders. A grader is a pass/fail check on what Claude produced, such as a regex over the reply, whether a particular tool was called, or a rubric that a second model judges the reply against." (https://code.claude.com/docs/en/plugin-evals.md, read 2026-09-23)

**Workflow:**
1. `claude plugin eval init` auto-generates cases and graders by interviewing you about your plugin.
2. `claude plugin eval .` runs every case with the plugin and (by default) without it, generating a baseline comparison.
3. Reads results from `evals/results/<timestamp>/aggregate-result.json` and `report.html` (or publishes to claude.ai artifact).
4. Exit code 0 if all cases pass threshold (default 1.0); 1 if any fail; 2 if partial (cost ceiling hit or auth failed).

**Grader Types:**
- `regex`: Pattern matching on output.
- `tool_used`: Check if tool was called with optional input matching.
- `tool_order`: Verify tool call order (before/after).
- `file_exists`: Check files created by glob pattern.
- `llm`: Judge model votes on a rubric (2-of-3 votes to pass).
- `baseline`: Compare against a reference transcript.

Each run starts in an isolated session with only the plugin loaded; no personal skills, MCP servers, or CLAUDE.md. Runs capture `total_tokens` and `duration_ms` for benchmarking.

- **Sources:**
  - [Skill Creator SKILL.md](<synced skills folder>/skill-creator/SKILL.md): Complete workflow for creating and iterating skills, description optimization, grading and benchmarking (read 2026-09-23)
  - [Test plugins with evals - Claude Code Docs](https://code.claude.com/docs/en/plugin-evals.md): `claude plugin eval` command, case format, grader types, baseline runs, JSON result schema (read 2026-09-23)

- **Confidence:** High. Workflows directly from Anthropic-authored skill-creator and official plugin-evals documentation.

- **Checker rule:** For skill-creator based evaluation, ensure `evals/` directory structure matches spec (cases with prompt.md, graders/, optional case.yaml). For plugin eval, ensure eval cases follow case/prompt.md format with supported grader types. Validate that each case targets only allowed-tools in the case's allowed_tools field.

---

### B6. Managing skills on claude.ai: programmatic APIs, organization provisioning, GitHub sync

- **Answer:**

**Skills API Endpoints (Programmatic Management):**

The Claude Platform provides REST API endpoints for skill management:
- **Create Skill:** `POST /v1/skills` — Create a new skill (https://platform.claude.com/docs/en/api/skills/create.md, referenced in WebFetch 2026-09-23)
- **Get Skill:** `GET /v1/skills/{id}` — Retrieve skill details (https://platform.claude.com/docs/en/api/skills/retrieve.md)
- **List Skills:** `GET /v1/skills` — List all skills (https://platform.claude.com/docs/en/api/skills/list.md)
- **Delete Skill:** `DELETE /v1/skills/{id}` — Delete a skill (https://platform.claude.com/docs/en/api/skills/delete.md)
- **Create Skill Version:** `POST /v1/skills/{id}/versions` — Create a new skill version (https://platform.claude.com/docs/en/api/skills/versions/create.md)
- **List Skill Versions:** `GET /v1/skills/{id}/versions` — List all versions (https://platform.claude.com/docs/en/api/skills/versions/list.md)
- **Get Skill Version:** `GET /v1/skills/{id}/versions/{version_id}` — Retrieve specific version (https://platform.claude.com/docs/en/api/skills/versions/retrieve.md)
- **Download Skill Version Content (Beta):** `GET /v1/skills/{id}/versions/{version_id}/content` — Download version content (https://platform.claude.com/docs/en/api/beta/skills/versions/download.md)

These endpoints exist for both stable and beta APIs. (https://platform.claude.com/llms.txt, verified 2026-09-23)

**Availability by Account Type:**
- **Personal accounts:** Can use the Skills API with personal API keys.
- **Team / Enterprise organizations:** Can use the Skills API for programmatic skill management; see [Using Agent Skills with the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide.md) for integration patterns.

**Organization-Central Provisioning:**

For Team and Enterprise plans, organization admins can provision skills for all members without requiring individual uploads:

"When you upload a skill through organization settings, it becomes available to everyone in your organization in Customize > Skills. Individual users no longer need to upload the same skill themselves." (https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization, verified 2026-09-23)

**Process:**
1. Navigate to Organization settings > Skills.
2. Check that "Code execution and file creation" and "Skills" toggles are on (skills require code execution).
3. Upload a .zip file containing SKILL.md, or create a skill by inputting name and description.
4. The skill becomes available to all organization members by default (users can toggle off individually for customization).

**GitHub-Hosted Distribution:**

Skills cannot be directly synced from a Git repository in the same way plugins can via `claude plugin init` or plugin marketplaces. However:

- **Plugins with Skills:** A plugin (which bundles skills) can be hosted on GitHub and distributed via plugin marketplaces. See https://code.claude.com/docs/en/plugin-marketplaces.md (read 2026-09-23): "Plugin sources... GitHub Repositories: `{ 'source': 'github', 'repo': 'owner/plugin-repo', 'ref': 'v2.0.0' }`" or via marketplace.json listing plugins with GitHub sources.
- **Organization-level plugin distribution:** Organizations can point `extraKnownMarketplaces` to a private GitHub repository containing a marketplace.json that lists plugins (and their bundled skills). (https://code.claude.com/docs/en/plugin-marketplaces.md, read 2026-09-23)
- **Direct skill Git sync:** Not documented as a feature. Skills are managed via the UI or API, not synced from Git repositories directly. (This is different from plugins, which can be sourced from Git.)

**Can an organization enable a GitHub-hosted Claude Code plugin marketplace for cloud sessions (claude.ai)?**

Not directly documented. Claude.ai skills are managed through the platform (https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization), not through plugin marketplaces (which are a Claude Code feature). Plugin marketplaces are a Claude Code concept; claude.ai has a separate Skills management interface in Organization settings.

- **Sources:**
  - [Platform: Skills API Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md): CRUD endpoints (WebFetch verified 2026-09-23)
  - [Support: Provision and manage skills for your organization](https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization): Organization provisioning workflow (WebSearch verified 2026-09-23)
  - [Code.claude.com: Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces.md): GitHub sources for plugins and plugin distribution (read 2026-09-23)

- **Confidence:** High. API endpoints and organization provisioning are documented; GitHub skill sync is not documented because it does not exist as a feature.

- **Checker rule:** If a skill is intended for organization distribution, document that the .zip upload will be used (not a Git source). For plugin-bundled skills, ensure the plugin can be distributed via GitHub or private marketplace (this is supported).

---

### B7. Plugin marketplaces: marketplace.json, versioning, validation, team distribution

- **Answer:**

**marketplace.json Format and Fields:**

Structure: ".claude-plugin/marketplace.json in your repository root" (https://code.claude.com/docs/en/plugin-marketplaces.md, read 2026-09-23)

**Required fields:**
```json
{
  "name": "marketplace-identifier",
  "owner": { "name": "Your Name" },
  "plugins": [...]
}
```

"name: Marketplace identifier (kebab-case, public-facing)" and "owner: Maintainer info (`name` required; `email`, `url` optional)" (https://code.claude.com/docs/en/plugin-marketplaces.md, read 2026-09-23)

**Per-plugin entry (minimal):**
```json
{
  "name": "plugin-name",
  "source": "./relative/path/or/source-object"
}
```

**Source Types:**
- Relative path: `"source": "./plugins/my-plugin"`
- GitHub: `"source": { "source": "github", "repo": "owner/repo", "ref": "v2.0.0", "sha": "..." }`
- Git URL: `"source": { "source": "url", "url": "https://...", "ref": "main", "sha": "..." }`
- Git subdirectory: `"source": { "source": "git-subdir", "url": "...", "path": "tools/plugin" }`
- npm: `"source": { "source": "npm", "package": "@org/plugin", "version": "2.1.0" }`
- Archive (.zip): `"source": { "source": "archive", "url": "https://...", "sha256": "..." }`
- Command: `"source": { "source": "command", "command": "my-tool", "timeout": 60 }` (runs once per session to pick up changes)

(https://code.claude.com/docs/en/plugin-marketplaces.md, read 2026-09-23)

**Optional Per-Plugin Metadata:**
- `displayName`: Human-readable name
- `description`: Brief description
- `version`: Plugin version (pins to this string if set)
- `author`: Plugin author info
- `homepage`, `repository`, `license`: Additional links
- `keywords`, `category`, `tags`: Discovery/categorization
- `skills`: Custom skill directory paths (e.g., `["./custom/skills/"]`)
- `commands`, `agents`, `hooks`, `mcpServers`, `lspServers`: Component directories
- `strict`: Boolean (default: true). Controls whether `plugin.json` is the authority
- `defaultEnabled`: Boolean (default: true). Install enabled or disabled
- `relevance`: Signals for plugin suggestions (org-allowlisted marketplaces only)

(https://code.claude.com/docs/en/plugin-marketplaces.md, read 2026-09-23)

**Reserved Marketplace Names:**

"These names are reserved for Anthropic and cannot be used: claude-code-marketplace, claude-plugins-official, anthropic-plugins, agent-skills, healthcare, etc. Names impersonating official marketplaces (e.g., official-claude-plugins) [and] Package manager names: npm, pip, uv, cargo, github, gh" (https://code.claude.com/docs/en/plugin-marketplaces.md, read 2026-09-23)

**Versioning:**

"Git sources: omit `version` to use commit SHA (auto-updates on new commits). Set `version` in `plugin.json` or marketplace entry to pin. **Warning**: Avoid setting in both places; `plugin.json` takes precedence." (https://code.claude.com/docs/en/plugin-marketplaces.md, read 2026-09-23)

Commit SHA is used as a fallback. For release channels: "Create separate marketplaces pointing to different branches/tags" (https://code.claude.com/docs/en/plugin-marketplaces.md, read 2026-09-23)

**What `claude plugin validate` Checks:**

"`claude plugin validate ./your-plugin` locally before you submit. The review pipeline runs the same check on every submission... When validation passes, Claude Code prints `✔ Validation passed`, or `✔ Validation passed with warnings` if there are warnings. Warnings don't fail validation; add `--strict` to treat them as errors." (https://code.claude.com/docs/en/plugins.md, read 2026-09-23)

From plugin-evals.md: "Check a plugin's files for syntax and schema errors rather than its behavior, use [`claude plugin validate`](/docs/en/plugins-reference#plugin-validate)" (https://code.claude.com/docs/en/plugin-evals.md, read 2026-09-23)

Specific checks: "The `claude plugin validate` command reports unrecognized fields as warnings, and if a field is one or two characters off from a recognized one, the warning suggests the likely intended name." (WebSearch result verified 2026-09-23)

**Team/Organization Distribution:**

**1. Via extraKnownMarketplaces in settings:**
"Add to `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```" (https://code.claude.com/docs/en/plugin-marketplaces.md, read 2026-09-23)

**2. Via managed settings (Enterprise):**
"For Team/Enterprise plans via claude.ai admin console: Marketplace repo must be private/internal. Plugin sources limited to: github, url, git-subdir, or relative paths. Private plugins must use relative paths in marketplace repo. Cannot include top-level `bin/` directory." (https://code.claude.com/docs/en/plugin-marketplaces.md, read 2026-09-23)

"Restrict which marketplaces users can add" via strictKnownMarketplaces: allows administrators to limit marketplace sources. Can use owner wildcards: `"repo": "acme-corp/*"` (https://code.claude.com/docs/en/plugin-marketplaces.md, read 2026-09-23)

**3. For Community Submission:**
"Submit your plugin for community-marketplace review" via https://platform.claude.com/plugins/submit (Console form, works for individual authors) or https://claude.ai/admin-settings/directory/submissions/plugins/new (claude.ai form, requires Team/Enterprise organization with directory access). "Approved plugins are pinned to a specific commit SHA in the [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community) catalog, and CI bumps the pin automatically as you push new commits." (https://code.claude.com/docs/en/plugins.md, read 2026-09-23)

- **Sources:**
  - [Create and distribute a plugin marketplace - Claude Code Docs](https://code.claude.com/docs/en/plugin-marketplaces.md): marketplace.json schema, source types, versioning, reserved names, team distribution (read 2026-09-23)
  - [Create plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins.md): submission process and validation (read 2026-09-23)
  - [Test plugins with evals - Claude Code Docs](https://code.claude.com/docs/en/plugin-evals.md): What plugin validate checks (read 2026-09-23)

- **Confidence:** High. All fields and validation rules are documented.

- **Checker rule:** Validate marketplace.json structure: require `name` (kebab-case), `owner.name`, `plugins` array. For each plugin: require `name` and `source`, validate `source` against allowed types (path string, or object with "source" key). Warn on reserved names. Validate version semantics (if set, should be semver or commit SHA). Validate per-plugin metadata fields (optional, but if present, must match documented types).

---

### B8. Public, well-regarded skill collections other than Anthropic's

- **Answer:**

**Status: Not documented.**

Official documentation does not list or reference public, well-regarded skill collections outside Anthropic's own published skills. Anthropic publishes skills through:
- The official marketplace: https://github.com/anthropics/claude-plugins-official (curated by Anthropic) and https://github.com/anthropics/claude-plugins-community (community submissions after review)
- Internal/bundled skills shipped with Claude Code

**Secondary sources found but not extensively documented:**
- GitHub search reveals various third-party skill repositories and skill templates (e.g., `shanraisshan/claude-code-best-practice`), but these are community-driven and not formally evaluated or blessed.
- Skill marketplace sites like LobeHub (https://lobehub.com/skills) list community skills, but are not official Anthropic endorsements.

**Conclusion:**
No public API or listing of "well-regarded secondary skill collections" is currently documented on code.claude.com, agentskills.io, or platform.claude.com. This is a gap in the available documentation.

- **Sources:** None (not documented)

- **Confidence:** Low. This is an absence of documentation.

- **Checker rule:** N/A. This category is not currently standardized or documented.

---

## Not documented

The following were queried but not found in official documentation:

1. **Exact ZIP file size limits for uploaded skills on claude.ai** — mentioned as a failure reason but not specified (e.g., "ZIP file exceeds size limits").

2. **The /mnt/user-data and /mnt/skills file paths specific to claude.ai skills sandboxing** — general information on claude.ai file handling exists, but claude.ai-specific skill execution paths are not publicly documented.

3. **Anthropic skill naming conventions requiring gerund form (e.g., "summarizing-changes")** — guidance emphasizes action-oriented names and imperative instructions, but no explicit gerund requirement is stated.

4. **Time-sensitive information warnings in skill content** — not mentioned in official best practices.

5. **Whether claude.ai allows GitHub-hosted skill or plugin marketplace sync** — plugins can use GitHub sources in Claude Code; this capability is not documented for claude.ai.

6. **Public collections of well-regarded third-party skills** — no official directory or endorsement list exists.

7. **Exact model versions or behavior differences tested with the skill-creator's evaluation framework** — the documentation mentions testing and optimization but does not specify which models are recommended for evaluation-driven development.

8. **Specific cost/token estimates for running skill-creator evaluations at scale** — individual run costs are documented in plugin eval, but cost guidance for iterative skill refinement is not quantified.
