# Skill builder

Read this for designing, writing, testing or tuning an Agent Skill, in any repository: the
frontmatter's fields and limits, a description that loads the skill when it should, splitting a
long skill into a router and modules, dated facts, examples that run, trigger evaluations with
near misses, measuring a skill against no skill, fixing one that loads too rarely or too often,
and shipping it in a plugin, a marketplace or a claude.ai upload.

Whether a line belongs in `AGENTS.md`, `CLAUDE.md` or a rule file instead of a skill, and hiding
a skill with `skillOverrides`, are `agent-context-files`. Vetting someone else's skill before you
install it, and hidden Unicode, are `ai-agent-security`. The prose is `house-style`'s. The
standard's *4. Agent configuration* rates installed skills in an audit.

## Rules

1. **Start from a task that fails without the skill, and from real material:** runbooks,
   incidents, the corrections you gave (facts `sb-evals-first`, `sb-real-expertise`).
2. **Use only the spec's six frontmatter fields, within their limits** (fact `sb-spec-fields`):
   `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. A claude.ai
   upload fails on any other (fact `sb-upload-fields`), so Claude Code's own fields, such as
   `disable-model-invocation`, stay out of a skill meant for both.
3. **The description decides whether the skill loads.** Main use first, then when to use it, in
   the third person, in the words people use for the situations it covers (facts
   `sb-desc-burden`, `sb-third-person`). Keep it short: listings cut and drop descriptions
   (fact `sb-listing`).
4. **Keep `SKILL.md` a router, with modules one level deep** (fact `sb-spec-disclosure`). It
   holds what applies everywhere and a table of which module to read for which request; each
   module stands alone and sends the reader to no other file.
5. **Say in the router that its rules summarize the modules,** and that the model reads the one
   that fits before answering.
6. **Every fact that can go stale carries its source, a quote, the date checked and a date to
   check again,** and the text names it by an ID instead of restating it.
7. **Every code example runs** under its language's own tool in CI; one wrong on purpose is
   marked so.
8. **Test triggering with realistic requests and near misses, several runs each,** and hold some
   back to check that a fix generalizes (facts `sb-desc-burden`, `sb-trigger-runs`).
9. **Measure the skill against no skill on the same cases,** on each model it will run on
   (facts `sb-eval-arms`, `sb-evals-first`).
10. **Tune from misses by concept, never by pasting a missed request's words** (fact
    `sb-trigger-runs`).
11. **A skill's name is public interface:** people type it and skills name it. Name what it's
    for.
12. **Treat Anthropic's `skill-creator` as a reference,** copying text only under its license
    (fact `sb-creator-license`).

### Splitting a skill

- One skill per kind of situation; new coverage is a module, so the listing stays small.
- Put the gotchas a model would get wrong in the router, where it reads them first.
- Keep each module small enough to be read whole. claude.ai's file viewer dropped the middle of
  a long file, cutting a module's last sections, so this repository holds modules to 16,000
  characters (its own test, 2026-10-26).

### Testing

- **Trigger evaluations:** requests, each marked whether the skill should load. Vary wording and
  detail; the best positives need the skill without naming it, and the negatives are near
  misses, sharing its words but belonging elsewhere.
- **Output evaluations:** a realistic prompt, what a good result holds, and graders: a regex, a
  tool called, a file made, or a rubric a judge model scores. Grade the result and the steps.
- **In a plugin,** `claude plugin eval` runs both against a no-plugin arm, and a `tool_used:
  Skill` grader shows whether the skill was chosen (fact `sb-eval-arms`).
- **A worked example:** this catalog's repository, rmccann-hub/claude-code-skills, runs each
  step with `skillcheck`. `--new` and `--new-module` scaffold, marking each unwritten part, and
  the check fails until it's written; `--examples` runs every code block; `--verify` finds each
  fact's quote at its source; `--triggers` asks Claude Code each trigger evaluation and checks
  the right module was read; `--tries` lists requests for a person to try on claude.ai.

### Tuning from misses

| What happened | Fix |
|---|---|
| The skill didn't load | Description: name the situation the request stands for |
| It loaded for a near miss | Description: say what it covers, and name the neighbor |
| It answered from the router | Router: say its rules summarize, and to read the module |
| It read the wrong module | Router: the table row's request words |
| Same score with and without | Content: cut what the model knows, add what it got wrong |

### Shipping it

- **A plugin in a marketplace:** `.claude-plugin/marketplace.json` lists each plugin and its
  skills. Run `claude plugin validate`, then install too: a missing path passes validation
  (fact `sb-validate-path`).
- **A claude.ai upload:** a ZIP whose root is the skill's folder, on an account with code
  execution on (fact `sb-upload-zip`).

## Mistakes

- **"Helps with PDFs", or a description in the first or second person.** Say what and when, in
  the third person (fact `sb-third-person`).
- **Pasting a missed request's words into the description.** It passes that request and no
  other (fact `sb-trigger-runs`).
- **A router whose rules answer the question.** In this repository's trigger reruns on
  2026-11-11, two of four misses loaded the right skill and answered from its summary rules
  without reading a module. Each router now says its rules summarize.
- **Asking a model to write a skill from what it already knows.** It writes generic advice;
  feed it your own material (fact `sb-real-expertise`).
- **Facts with no source, and examples never run.** None of the older skills this repository
  rebuilds had either, so nothing was copied from them.
- **Rules in capitals instead of reasons.** A reason lets the model handle the case the rule
  missed.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A field outside the spec, in a skill for claude.ai or other agents | Frontmatter keys | `BLOCKER` | Remove it, or keep a Claude Code-only copy |
| `name` breaks the spec or differs from its directory | Fact `sb-spec-fields` | `BLOCKER` | Rename, as a breaking change |
| The description says what but not when, or isn't third person | The description | `GAP` | Main use, then when |
| `SKILL.md` over 500 lines, or a file that sends the reader on | `wc -l`; links in `references/` | `DRIFT` | Split into modules that name, not link |
| No trigger evaluations, or no near misses | The evaluation files | `GAP` | Add both kinds |
| Scores with no baseline | No without-skill score | `GAP` | Run both arms (fact `sb-eval-arms`) |
| The same score with and without the skill | Each case's two scores | `OVER` | Cut what the model knows |
| A version, date or default with no source or check date | Numbers in the text | `GAP` | Add the fact row, or cut the claim |
| A code example that fails its tool | Each block under its tool | `DRIFT` | Fix or mark it |
| A catalog path that doesn't exist | Each path in the marketplace | `BLOCKER` | Fix it; install to prove it |

## Why

### Starting from a failure

**Why.** A skill that restates what the model knows costs context on every load and changes no
result (fact `sb-evals-first`). **Cost:** a session of plain prompting, its failures written
down. **Choose differently** for a skill that only packages a script or a template.

### The description

**Why.** It's all a model sees before it loads anything (fact `sb-desc-burden`). This
repository's first trigger run found none of four requests loading the skill they belonged to,
and descriptions were tuned before any rebuild.

**What others do.** The agentskills.io guide phrases it as an instruction, "Use this skill
when", and urges it to be pushy, as `skill-creator` does, since models tend to under-use
skills. Anthropic's platform guide asks for the third person, because it goes into the system
prompt (fact `sb-third-person`). Both fit: "Does X. Use when Y."

**Cost.** A pushy one loads for near misses, and a long one is cut or dropped (fact
`sb-listing`). This repository caps each at 250 characters, its own choice, so about 20 skills
list whole. **Choose differently** for a skill people only call by name: it needs little.

### A router and modules

**Why.** The name and description load at startup, the router when the skill is chosen, a
module only when needed, so coverage costs nothing until read. A module that names no other
file moves to another skill whole. **Cost:** an extra read, and a router that can answer
instead of routing. **Choose differently** for a skill short enough to read whole.

### Facts, examples and evaluations

**Why.** A stale version or a broken example is followed as confidently as a right one. One model run says little (fact `sb-trigger-runs`), and a score
with no baseline can't tell the skill's work from the model's (fact `sb-eval-arms`).

**Cost.** A check date per fact, and a weekly check; a tool per language; a paid model call
per evaluation run (fact `sb-eval-arms`), so this repository runs trigger tests by hand.
**Choose differently** while iterating on graders: run one arm, then confirm with both.

### Names and `skill-creator`

- **Names:** when a name misleads, rename it as a breaking change, and record the old one.
- **`skill-creator`** drafts a skill, runs evaluations with and without it, and tunes its
  description. Text taken from it keeps its Apache-2.0 notice and marks its changes (fact
  `sb-creator-license`). This repository takes its method, not its text.

## Facts

Checked 2026-11-11.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `sb-spec-fields` | `name` 1 to 64, its directory's; `description` 1,024; `compatibility` 500; `allowed-tools` experimental | [Agent Skills spec](https://agentskills.io/specification) | "Must be 1-64 characters" and "Must match the parent directory name" and "Max 1024 characters. Non-empty." and "Must be 1-500 characters if provided" and "Experimental." | 2026-11-11 | 2027-05-11 |
| `sb-spec-disclosure` | `SKILL.md` under 500 lines; references one level deep | [Agent Skills spec](https://agentskills.io/specification) | "Keep your main SKILL.md under 500 lines." and "Keep file references one level deep from SKILL.md" | 2026-11-11 | 2027-05-11 |
| `sb-upload-fields` | A claude.ai upload fails on a field outside the spec | [Claude Code: skills](https://code.claude.com/docs/en/skills) | "If you include any field the spec doesn't allow, packaging or upload fails with a hard error instead of ignoring the field" | 2026-11-11 | 2027-02-11 |
| `sb-listing` | Claude Code cuts a description at 1,536 characters, and past a budget drops the least-used skills' | [Claude Code: skills](https://code.claude.com/docs/en/skills) | "is truncated at 1,536 characters in the skill listing" and "The budget scales at 1% of the model's context window." and "drops descriptions starting with the skills you invoke least" | 2026-11-11 | 2027-02-11 |
| `sb-third-person` | Descriptions in the third person | [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | "Always write in third person" and "inconsistent point-of-view can cause discovery problems" | 2026-11-11 | 2027-05-11 |
| `sb-evals-first` | Evaluations before the skill, on every model it runs on | [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | "Create evaluations BEFORE writing extensive documentation." and "Test your Skill with all the models you plan to use it with." | 2026-11-11 | 2027-05-11 |
| `sb-real-expertise` | Build from real expertise; gotchas are worth most | [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) | "Effective skills are grounded in real expertise." and "The highest-value content in many skills is a list of gotchas" | 2026-11-11 | 2027-05-11 |
| `sb-desc-burden` | The description alone decides loading; near misses are the best negatives | [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) | "the description carries the entire burden of triggering" and "queries that share keywords or concepts with your skill but actually need something different" | 2026-11-11 | 2027-05-11 |
| `sb-trigger-runs` | Several runs per request; don't paste missed words | [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) | "Run each query multiple times (3 is a reasonable starting point)" and "Avoid adding specific keywords from failed queries" | 2026-11-11 | 2027-05-11 |
| `sb-eval-arms` | `claude plugin eval` runs each case with and without the plugin, each run paid; a failing `Skill` grader means it wasn't chosen | [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals) | "Each case runs three times with your plugin and three times without it, so one case is six runs." and "If a case scores 1.0 both with and without the plugin, the plugin isn't what made it pass." and "which means Claude isn't choosing your skill on natural phrasing" and "Every eval run and every judge grader is a real model call on your account" | 2026-11-11 | 2027-02-11 |
| `sb-validate-path` | A missing plugin path passes `claude plugin validate` | [Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces) | "A path to a directory that doesn't exist" and "claude plugin validate passes" | 2026-11-11 | 2027-02-11 |
| `sb-upload-zip` | claude.ai skills need code execution; the ZIP's root is the skill's folder | [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) | "This feature requires code execution to be enabled" and "The ZIP should contain the skill folder as its root (not a subfolder)." | 2026-11-11 | 2027-02-11 |
| `sb-creator-license` | `skill-creator` is under Apache-2.0 | [skill-creator LICENSE.txt](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/LICENSE.txt) | "Apache License" and "Version 2.0, January 2004" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Agent Skills](https://agentskills.io/): spec, best practices, descriptions | Fields, loading, trigger tests | CC BY 4.0: short quotes, attributed |
| Anthropic: Claude Code docs, platform guide, support article | Listing, uploads, evals, marketplaces | All rights reserved: short quotes, our own words |
| [anthropics/skills](https://github.com/anthropics/skills): `skill-creator` | Its method, and its license | Apache-2.0: no text adapted |
| This repository's trigger runs, rebuilds and size test | Router misses, old skills, the size limit | Apache-2.0 |
