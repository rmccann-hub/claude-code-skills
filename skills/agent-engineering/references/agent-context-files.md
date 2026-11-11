# Agent context files

Read this for writing, trimming or fixing `AGENTS.md`, `CLAUDE.md` or another agent's
instruction file: what earns a line, what belongs in a rule, a skill, a hook, a permission rule
or CI instead, `@` imports and path-scoped rules, Claude Code's settings and `skillOverrides`,
subagents' tools, project MCP servers, parallel helper agents, and pointing Cursor, Copilot,
Codex or Gemini at one `AGENTS.md`.

The standard sets the budgets, the one-line shim, the starter files and what an audit rates on
its dimension 4; this module cites those by section and covers how to write and keep the files.
Injected instructions, vetting MCP servers, skills and plugins, and how far deny rules hold are
`ai-agent-security`. Agents reviewing each other are `review-loops`.

## Rules

1. **A line earns its place when a session would otherwise get it wrong:** exact commands with
   their flags, conventions that differ from the tools' defaults, and what has gone wrong
   before. Leave out what the model knows, what two files show, and what a linter or formatter
   enforces (facts `acf-derivable`, `acf-cursor`).
2. **Make each line checkable:** a command, a path or a named check, as the standard's *Starter
   file contents* asks. "Run `uv run pytest` before committing", not "test your changes".
3. **Add a line the second time a session makes a mistake, and cut it when its cause goes.**
   Of two lines that contradict, a session picks either (fact `acf-upkeep`).
4. **What must always happen goes in a hook; what must never happen, in a deny rule with CI or
   branch protection behind it; only judgment goes in prose** (facts `acf-not-enforced`,
   `acf-hooks-always`). A blocking hook exits 2 and sets `"onFailure": "block"` (fact
   `acf-hook-exit`).
5. **Scope what applies to part of the tree** in a nested `AGENTS.md` (fact
   `acf-agents-nearest`) or a `.claude/rules/` file with `paths` (fact `acf-rule-paths`), and
   put a procedure of several steps in a skill.
6. **Import with `@path`, knowing an import costs what inline text costs** (fact
   `acf-imports`).
7. **Commit the team's settings in `.claude/settings.json`; personal ones stay in
   `.claude/settings.local.json`,** where approvals and the `/skills` menu write (facts
   `acf-local-writes`, `acf-skill-overrides`). Move an entry across to share it. Personal
   instructions go in a gitignored `CLAUDE.local.md`.
8. **Give each subagent the fewest tools its job needs, and the rules it must keep in its
   prompt.** One with no `tools` list inherits them all (fact `acf-subagent-tools`).
9. **Split parallel helpers by files and number ranges, and run the full gate once, on the
   combined tree.**
10. **Commit `.mcp.json` only for servers every contributor needs, each secret a `${VAR}`**
    (fact `acf-mcp-project`), and justify each, as the standard's dimension 4 asks.
11. **Keep one source:** every other tool reads `AGENTS.md`, or a file pointing at it, never a
    copy. The standard's *Any agent, any tool* holds the table.

### Parallel helpers

- Each helper owns named files, and a range for anything numbered: tasks, rows, decisions.
- Helpers run the tests for what they touched. One integrator runs the suite and the gate on
  the combined tree, and cherry-picks with `-x`, so each commit's citation survives.

## Mistakes

- **A directory tree, a dependency list or an overview in `AGENTS.md`.** Sessions read them
  from the code, and the copy drifts (fact `acf-derivable`).
- **Style rules a formatter enforces.** Put them in its config (fact `acf-cursor`).
- **A hook that exits 1 to block.** The call goes ahead (fact `acf-hook-exit`).
- **Cursor's `globs` or `alwaysApply` in a `.claude/rules/` file.** Claude Code ignores them, and
  YAML that doesn't parse loads the rule everywhere (fact `acf-rule-paths`).
- **A rule file past the on-demand limit:** Claude reads only its start (fact
  `acf-ondemand-limit`).
- **A SessionStart hook that prints `AGENTS.md`,** a second copy, or a `CLAUDE.local.md` where
  no shim imports `AGENTS.md`, which stops Claude Code reading it (fact
  `acf-agents-workarounds`).
- **Shared rules in `AGENTS.override.md`.** Codex reads it in place of that directory's
  `AGENTS.md`; Claude Code never reads it (fact `acf-override-files`).
- **A "read-only" subagent that keeps Bash.** A shell writes files.
- **`syncClaudeAiSkills: false` in the committed settings,** where it's ignored (fact
  `acf-sync-project`). Hide a synced skill with `skillOverrides`, and a plugin's skill by
  turning the plugin off.
- **`AGENTS.md` copied into `.github/copilot-instructions.md`.** Copilot reads `AGENTS.md`
  (fact `acf-copilot-agents`); keep that file for Copilot-only lines, or delete it.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Derivable content | Trees, dependency lists, overviews, formatter rules in always-loaded files | `OVER` | Cut, or move to the tool's config |
| A must-never rule in prose only | A "never" line with no deny rule, hook or CI check behind it | `GAP` | Add one |
| Rule frontmatter | Fields other than `paths`, or YAML that doesn't parse | `DRIFT` | `paths` only; `claude --debug` shows the error |
| On-demand size | `wc -m` on rules and nested files, against the limit | `DRIFT` | Split them |
| Duplicate load | A SessionStart hook that prints a context file | `OVER` | Remove it |
| Copies | Another tool's file repeating `AGENTS.md` | `DRIFT` | Point at it, or delete |
| Subagent tools | No `tools` list, or Bash where it should only read | `GAP` | List its tools |
| Inert settings | `syncClaudeAiSkills` in `.claude/settings.json`; `skillOverrides` for a plugin's skill | `DRIFT` | Replace them |
| Contradictions | Two lines that disagree, in any of the files | `DRIFT` | Keep one; `/doctor prompt-audit` finds them (fact `acf-upkeep`) |

## Why

### What earns a line

- **The advice:** commands, conventions the code doesn't show, and past failures.
- **The reason:** context files raised cost by over 20% without raising success in general;
  repository overviews didn't help, and non-standard practices were worth stating (fact
  `acf-gloaguen`). Anthropic's trim cuts what Claude can derive (fact `acf-derivable`), and
  Cursor says to use a linter (fact `acf-cursor`).
- **What others do, and why:** Anthropic's list of what to include names project layout, for
  layouts the code doesn't explain.
- **What it costs:** a session explores more, in reads it often makes anyway.
- **When to choose differently:** a generated or unusual layout two files don't explain.

### Hooks and rules over prose

- **The advice:** enforce with a hook, a deny rule or CI; write prose for judgment.
- **The reason:** a context file isn't enforced (fact `acf-not-enforced`); a hook runs every
  time (fact `acf-hooks-always`), but blocks only when written to (fact `acf-hook-exit`).
- **What others do, and why:** Cursor and Copilot have no enforced layer, so the standard's
  *Any agent, any tool* moves the guarantee to CI and the server.
- **What it costs:** a hook is code to test and audit, and one that misfires blocks work.
- **When to choose differently:** where no hook runs, such as a session holding several
  repositories, which the standard's *Facts with an expiry date* records.

### Scope, imports and settings

- **The advice:** scope by path, import knowing the cost, share settings in the committed file.
- **The reason:** a path-scoped rule loads when a matching file is read (fact
  `acf-rule-paths`); an import loads at launch (fact `acf-imports`). Approvals and the `/skills`
  menu write the local file (facts `acf-local-writes`, `acf-skill-overrides`), which never
  reaches a colleague. A clone can't approve its own MCP servers (fact `acf-mcp-project`).
- **What it costs:** a scoped rule is unseen until its file is read, so a rule needed before
  that, such as where a new file goes, stays unscoped.
- **A working example:** this skill's repository. Each convention in its `AGENTS.md` names its
  check or says nothing checks it; `CLAUDE.md` imports it and adds only lines about synced
  skills; `.claude/rules/python.md` scopes four lines to `src/` and `tests/`; and its settings
  turn off, by name, each skill its cloud hook installs.

### Subagents and parallel helpers

- **The advice:** narrow tools, rules in the prompt, files and numbers split, one integrator.
- **The reason:** Explore and Plan start without `CLAUDE.md` (fact `acf-subagent-tools`), so a
  rule they must keep goes in the prompt. Parallel helpers' read-only audits found real
  defects, but seven full suites on four cores pushed one past its limit (L39). Helpers on one
  record took the same task number and duplicated rows, and a failure showed only on the
  combined tree (L57).
- **What it costs:** the final gate runs once, through one integrator.
- **When to choose differently:** one helper on a machine with room can run its own suite.

### One source across tools

- **The advice:** one `AGENTS.md`, read directly or through a pointer.
- **The reason:** Copilot (fact `acf-copilot-agents`), Cursor (fact `acf-cursor`) and Gemini
  CLI (fact `acf-gemini-filename`) read it, and Codex reads an override first (fact
  `acf-override-files`). A copy drifts from its source.
- **What it costs:** a tool's own feature, such as Copilot's `applyTo`, keeps its own file.
- **When to choose differently:** check Gemini CLI's successor before relying on it there
  (fact `acf-gemini-filename`).

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `acf-derivable` | `/doctor` trims what Claude can derive | [Memory](https://code.claude.com/docs/en/memory) | "it cuts content Claude can derive from the codebase, such as directory layouts, dependency lists, and architecture overviews" | 2026-11-11 | 2027-02-11 |
| `acf-upkeep` | Add on a repeated mistake; of two that contradict, either wins; an audit finds them | [Memory](https://code.claude.com/docs/en/memory) | "Claude makes the same mistake a second time" and "Claude may pick one arbitrarily" and "/doctor prompt-audit requires Claude Code v2.1.283 or later" | 2026-11-11 | 2027-02-11 |
| `acf-not-enforced` | A context file isn't enforced | [Memory](https://code.claude.com/docs/en/memory) | "not a hard enforcement layer" | 2026-11-11 | 2027-02-11 |
| `acf-imports` | Imports load at launch, to four hops | [Memory](https://code.claude.com/docs/en/memory) | "imported files load together with the CLAUDE.md that imports them" and "a maximum depth of four hops" | 2026-11-11 | 2027-02-11 |
| `acf-rule-paths` | A rule reads only `paths`; bad YAML loads it unscoped | [Memory](https://code.claude.com/docs/en/memory) | "any other field is ignored without an error" and "loads the rule as if it had no paths" | 2026-11-11 | 2027-02-11 |
| `acf-ondemand-limit` | On-demand files are cut at 40,000 characters, at 200K context | [Memory](https://code.claude.com/docs/en/memory) | "Claude receives only the start of it" and "200K context window: 40,000 characters" | 2026-11-11 | 2027-02-11 |
| `acf-agents-workarounds` | A hook printing `AGENTS.md` duplicates it; `CLAUDE.local.md` stops native reading | [Memory](https://code.claude.com/docs/en/memory) | "the hook adds a second copy to the context" and "stops Claude from reading AGENTS.md for you" | 2026-11-11 | 2027-02-11 |
| `acf-override-files` | Claude Code skips `AGENTS.override.md`; Codex reads it first | [Memory](https://code.claude.com/docs/en/memory), [Codex](https://developers.openai.com/codex/guides/agents-md) | "Not read: AGENTS.local.md, AGENTS.override.md" and "it checks for AGENTS.override.md, then AGENTS.md" | 2026-11-11 | 2027-02-11 |
| `acf-hooks-always` | Hooks run every time | [Hooks guide](https://code.claude.com/docs/en/hooks-guide) | "certain actions always happen rather than relying on the LLM to choose to run them" | 2026-11-11 | 2027-02-11 |
| `acf-hook-exit` | Exit 2 blocks; a failing hook lets calls through unless `onFailure` blocks | [Hooks](https://code.claude.com/docs/en/hooks) | "If your hook is meant to enforce a policy, use exit 2." and "A policy hook with a wrong path or a crashing script then lets everything through." | 2026-11-11 | 2027-02-11 |
| `acf-local-writes` | Standing approvals go to the local file | [Permissions](https://code.claude.com/docs/en/permissions) | "Claude Code saves the rule to .claude/settings.local.json" | 2026-11-11 | 2027-02-11 |
| `acf-skill-overrides` | `/skills` saves locally; plugin skills are out of reach | [Skills](https://code.claude.com/docs/en/skills) | "then Esc to save to .claude/settings.local.json" and "Plugin skills are not affected by skillOverrides." | 2026-11-11 | 2027-02-11 |
| `acf-sync-project` | Committed settings can't stop the skill sync | [Settings](https://code.claude.com/docs/en/settings) | "a false in .claude/settings.json is ignored" | 2026-11-11 | 2027-02-11 |
| `acf-subagent-tools` | No `tools` inherits all; Explore and Plan skip `CLAUDE.md` | [Subagents](https://code.claude.com/docs/en/sub-agents) | "Inherits every tool available to subagents if omitted." and "Explore and Plan start without your CLAUDE.md files" | 2026-11-11 | 2027-02-11 |
| `acf-mcp-project` | `.mcp.json` expands variables; a clone can't approve its servers | [MCP](https://code.claude.com/docs/en/mcp) | "environment variable expansion in .mcp.json files" and "A cloned repository can't approve its own servers" | 2026-11-11 | 2027-02-11 |
| `acf-agents-nearest` | The nearest `AGENTS.md` wins | [AGENTS.md](https://agents.md/) | "closest AGENTS.md to the edited file wins" | 2026-11-11 | 2027-05-11 |
| `acf-copilot-agents` | Copilot's cloud agent reads `AGENTS.md` | [GitHub Docs](https://docs.github.com/en/copilot/reference/custom-instructions-support) | "Agent instructions (using AGENTS.md, CLAUDE.md or GEMINI.md files)" | 2026-11-11 | 2027-02-11 |
| `acf-cursor` | Cursor: rules are `.mdc`, `AGENTS.md` at any depth, a linter for style | [Cursor](https://cursor.com/docs/context/rules) | "Project rules must use the .mdc extension." and "Cursor supports AGENTS.md in the project root and subdirectories." and "Use a linter instead." | 2026-11-11 | 2027-02-11 |
| `acf-gemini-filename` | Gemini CLI reads other names by setting; Antigravity CLI replaced it for some users | [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/) | "use the context.fileName property" and "Gemini CLI was replaced by Antigravity CLI on June 18th, 2026." | 2026-11-11 | 2027-02-11 |
| `acf-gloaguen` | Context files: no general gain, over 20% cost, overviews unhelpful (Gloaguen et al.) | [arXiv](https://arxiv.org/abs/2602.11988) | "increasing inference cost by over 20% on average" and "repository overviews, although popular and recommended by model providers, are not helpful" and "useful for specifying non-standard coding practices" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| Anthropic, Claude Code docs | Loading, rules, hooks, settings, subagents, MCP | All rights reserved: short quotes, our own words |
| AGENTS.md; OpenAI, Cursor, Gemini CLI docs | Other tools' files | Not stated: short quotes, our own words |
| GitHub Docs | Copilot | CC BY 4.0: short quotes, attributed |
| arXiv: Gloaguen et al. | What helps | CC BY 4.0: quoted, attributed |
| This repository's lessons and files, other repositories unnamed | Helpers, the example | Apache-2.0 |
