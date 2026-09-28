# Verification: R22, deeper pass (2026-09-28)

A second result for the R22 prompt, from a deeper pass on the same day. The first is
[2026-09-27-R22-one-command-front-door.md](2026-09-27-R22-one-command-front-door.md). Checked by
the receiving session on 2026-09-28, with pages fetched with `curl` and matched against the page
itself. Only the claims this intake relies on were checked: what it changes in `ROADMAP.md` and
the decision record, and what it adds to the first pass. Claims both passes make were checked
once, in the first pass's table. Row numbers such as F19 are this report's facts table, in its
section 3.

Following this pass's sources to earlier versions and full texts corrected four rows of the first
pass's table: its rows 56, 64, 65 and 66 turned out verified, not unverifiable or contradicted.
That table now says so.

The original below is unedited except for three phrases:

- the first live repository's name, in section 4.3, replaced with "the first live repository",
  since the v0.38.0 entry keeps that name out of this repository;
- two model names in F32's quote, replaced with `[one model]` and `[another]`;
- a model name in F36's value, replaced with `[one model]`.

| Claim | Status | Checked against |
|---|---|---|
| The skills docs' quotes, F1–F7: a body loads only when used; `/skill-name`; account skills include the organisation's; the short-name collision; repository-declared plugins don't load in cloud sessions; turning off a synced skill; skill-scoped hooks | verified | [Skills docs](https://code.claude.com/docs/en/skills), each quote as given. F5's and F6's carry a link inside the sentence on the page |
| The French translation lists cloud sessions for synced plugins (F9), so the question is contested (sections 2, 7 and 10) | contradicted | Read on 2026-09-28, neither the [French plugins reference](https://code.claude.com/docs/fr/plugins-reference) nor the [French loading page](https://code.claude.com/docs/fr/plugins/loading) has the sentence. The loading page says synced plugins load "dans les sessions Cowork et dans les sessions de terminal", as the English does |
| Account plugins are available in chat, Cowork and terminal Claude Code, and hooks and sub-agents don't run in chat (F10, F12) | verified | [Help Center 13837440](https://support.claude.com/en/articles/13837440-use-plugins-in-claude): "Plugins you add are saved to your account, so they're also available in Claude Code in your terminal when you sign in with the same account." |
| `SKIP_PLUGIN_MARKETPLACE=true` in cloud sessions (F11) | verified for this session | Observed on 2026-09-28: the variable is `true` in this cloud session. Whether it can be overridden wasn't tried |
| An organisation's GitHub sync runs on a merged pull request with a version bump, and the same page also says a direct push syncs (F14) | verified; contested within the page, as the report says | [Help Center 13837433](https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization): "runs when a pull request that includes a plugin version bump is merged", "Direct pushes to the default branch don't trigger a sync", and "or when someone pushes to that branch directly" |
| An organisation's manual plugin upload is a ZIP under 200 MB, and the same name overwrites (F15) | verified | Help Center 13837433: "The file must be a valid .zip under 200 MB." The first pass's "under 50 MB" (its row 46) isn't on the page now |
| `syncClaudeAiPlugins` stops the plugin sync, beside `syncClaudeAiSkills` (F16) | verified | Help Center 13837433: "set `syncClaudeAiSkills` and `syncClaudeAiPlugins` to `false` in Claude Code managed settings"; the [settings reference](https://code.claude.com/docs/en/settings-reference) lists `syncClaudeAiPlugins` for user, local or managed settings |
| Skills API 30 MB (F17); plugins 5,000 files and 200 MB (F18) | verified | [Skills guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide): "Total upload size must be under 30 MB (uncompressed)"; [platform support](https://claude.com/docs/plugins/platform-support) |
| A claude.ai skill's description may be 200 characters at most (F19) | verified that the Help Center says so; contested | [Help Center 12512198](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) gives the description "(200 characters maximum)", against 1,024 in the [Agent Skills specification](https://agentskills.io/specification). Skills the owner created on the account sync to this session with longer descriptions, some updated after 2026-07-22, but their manifest records them as coming from a plugin, so they don't show what a skill upload accepts. This skill's description is 446 characters |
| Skills sync at session start and about every 10 minutes (F20); owner provisioning (F21); published skills stay on the approved version (F22); shared skills update at next use (F23) | verified | [Help Center 12512180](https://support.claude.com/en/articles/12512180-use-skills-in-claude), each quote as given |
| `AskUserQuestion` fails on Android (F24) | unverifiable | github.com returned 403 from this session |
| `AskUserQuestion` takes 1–4 questions with 2–4 options per call (section 4.3) | verified | [Agent SDK docs, user input](https://code.claude.com/docs/en/agent-sdk/user-input): "each `AskUserQuestion` call supports 1-4 questions with 2-4 options each" |
| The GitHub Action installs plugins (F25), needs `claude setup-token` for a subscription (F26), and a public repository's schedule stops after 60 inactive days (F27) | verified | [GitHub Actions docs](https://code.claude.com/docs/en/github-actions), each quote as given |
| A PreToolUse hook blocks a call with exit code 2 (F28); a project skill's hooks follow workspace trust and register on invocation (F29) | verified | [Anthropic blog](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more): "A PreToolUse hook can inspect a call and exit with code 2 to block it."; [hooks docs](https://code.claude.com/docs/en/hooks), including its exit-code table |
| `raw.githubusercontent.com` allows cross-origin reads (F30) | verified (observed) | `curl -I` on 2026-09-28 returned `access-control-allow-origin: *` |
| Interaction improves underspecified tasks by up to 74%, and models don't ask unprompted (F31, TL;DR) | verified | [arXiv:2502.13069](https://arxiv.org/abs/2502.13069), abstract and HTML v3: "interactivity can boost performance on underspecified inputs by up to 74% over the non-interactive settings" and "most LLMs default to non-interactive behavior" |
| Exploring first gets similar information from 50% fewer questions (F32) | verified | arXiv:2502.13069 HTML v3, as quoted. The filed copy removes the quote's two model names |
| Python in 90–97% of benchmark tasks and 58% of unsuited project set-ups, and 83% self-contradiction (F34) | verified | The [v1 abstract of arXiv:2503.17181](https://arxiv.org/abs/2503.17181v1): "LLMs contradict their own language recommendations in 83% of project initialisation tasks". Later versions keep the 58% and drop the other two. OpenReview returned 403 |
| At least 5.2% of packages from commercial models and 21.7% from open-source ones don't exist (F35) | verified | [USENIX Security 2025](https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen) abstract: 16 LLMs, 576,000 samples in two languages, 205,474 names. It doesn't name the two languages |
| Deprecated API use of 25–38% (F36) | verified | The full text at [arxiv.org/html/2406.09834](https://arxiv.org/html/2406.09834): "ranges from 25% to 38%". The per-model figure wasn't checked, and the filed copy removes its model name |
| CC0 waives no patent or trademark rights (F37) | verified | [CC0 1.0 legal code](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en), section 4 |
| `copier update` needs an answers file and a tagged template (F38); Nygard's and MADR's record shapes (F39, section 4.4) | verified | [copier docs](https://copier.readthedocs.io/en/stable/updating/); [adr.github.io](https://adr.github.io/adr-templates/) |
| `AGENTS.md` support reached Bedrock and telemetry-off sessions in 2.1.281 (correction 4) | verified | [Memory docs](https://code.claude.com/docs/en/memory): "Before v2.1.281, some sessions, such as those on Amazon Bedrock or with telemetry disabled, read `CLAUDE.md` files only"; changelog 2.1.281 |
| The chat's stale copy (F40) | verified on the repository's side | At `cbe163f` the v0.36.0 reference is 310,336 bytes |
| Everything else in the report | not yet checked | checked when a skill that relies on it is built (`research/README.md`) |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R22 · FORM: research-result v1
Save as: R22-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R22 result: one command from any repository, and the questions it asks (deeper pass, 27 September 2026)

The best one-command front door is a small skill uploaded to the owner's claude.ai account, typed as `/project-bootstrap-and-audit`. On its first run it fetches the standard at a pinned commit and checks its bytes. After the first approved run it gets a committed project skill in each repository, which can enforce the approval gate with hooks. The personal-marketplace plugin should be retired as a delivery route, because Anthropic's English plugin documentation no longer lists cloud sessions as a place synced plugins load, and that plugin is the source of the stale v0.36.0 copy.

Categories whose facts files this report touches: skills distribution, plugins and marketplaces, cloud sessions, question design and elicitation, stack recommendation bias, licences.

## 1. Summary

**TL;DR**

- **Trigger:** a skill uploaded to the claude.ai account is documented to load in Claude Code cloud sessions, together with skills the organization provides. It is invoked by name as `/project-bootstrap-and-audit`, or as `/anthropic-skills:project-bootstrap-and-audit` when another command already uses the short name. It is the only route that is documented, needs no per-repository setup and works in an empty repository.
- **Stale copies:** the v0.36.0 copy comes from the `standards` plugin, not from an uploaded skill. The English plugin docs (read 2026-09-27) list only Cowork and terminal sessions for synced plugins. Remove or disable that plugin on claude.ai, so that only one copy carries the name, and have every run print and verify the SHA-256 of the standard it actually read.
- **Questions:** draft answers from the repository with their evidence. Ask outright only what no repository can show: where it runs, who uses it, work or personal, how bad a failure would be, how long it must live. Give no pre-selected default for those. The measured evidence is two results. In Ambig-SWE (Vijayvargiya et al., with Neubig, arXiv 2502.13069, an underspecified variant of SWE-Bench Verified), interaction gave "significant improvements in performance, up to 74% over the non-interactive settings". Defaults move choices strongly: Jachimowicz, Duncan, Weber and Johnson (2019, Behavioural Public Policy, 58 studies, pooled n = 73,675) found "d = 0.68, 95% confidence interval = 0.53–0.83", so a default offered where the repository has no evidence leads the owner.

Further points a professional must know today:

- **Account uploads:** an uploaded skill accepts only six frontmatter fields (name, description, license, compatibility, metadata, allowed-tools). It cannot carry `hooks` or `disable-model-invocation`, so the approval gate has to be enforced by Plan mode and by instructions until a project skill with hooks is committed.
- **Organization provisioning:** Team and Enterprise Owners can provision skills that "automatically appear for all users", and the Claude Code docs say synced skills include "skills your organization provides there". Colleagues can therefore be reached without this public repository carrying company rules.
- **Organization plugin uploads:** a manual plugin upload is "a valid .zip under 200 MB", and a same-name upload "overwrites the previous version automatically". A GitHub-synced organization marketplace must be private or internal.
- **Upload limits:** the size and file-count limits for a claude.ai skill ZIP are not published. The help centre names "ZIP file exceeds size limits" as an upload error but gives no number. The Skills API limit is 30 MB uncompressed.
- **Mobile:** AskUserQuestion is documented, but how it renders on the web and in the mobile app is not. One public bug report (Android) says the question card reappears after Submit while "PC/Web: Works normally". The front door needs a plain-text fallback that can be answered in one reply.
- **Routines:** routines run without approval stops, and a fired prompt cannot act as consent. They suit a read-only scheduled re-audit that proposes changes, never a run that applies them.
- **GitHub Action:** it can install plugins (`plugin_marketplaces`, `plugins`) and run a committed skill. Subscription authentication needs `claude setup-token` run locally, which is out of reach for this owner. The browser route is an API key from the Console, billed separately.
- **Stack bias (measured):** in Twist, Zhang, Harman, Syme and colleagues' "LLMs Love Python" (arXiv 2503.17181, eight LLMs), models chose Python in 90–97% of language-agnostic benchmark tasks, and in 58% of project-initialisation tasks where Python was unsuitable. They contradicted their own language recommendation in 83% of those tasks.
- **Package hallucination:** Spracklen et al. (USENIX Security 2025, 16 LLMs, 576,000 code samples in Python and JavaScript, 205,474 unique hallucinated names) found that at least 5.2% of packages suggested by commercial models, and 21.7% by open-source models, did not exist. Every recommended dependency must be checked against its registry before it is recorded.
- **Paired repositories:** use one repository per session. The first pass found that a multi-repository session reads only `enabledPlugins` and `extraKnownMarketplaces` from each repository, so it loses each repository's hooks and permission rules.

## 2. Corrections

Each item below was wrong, out of date or incomplete in "What we believe". The source is in the Facts table under the number given.

1. **"(the standard, 2026-09) Plugins enabled on a claude.ai account are documented to load in cloud sessions as `<name>@synced`."** Out of date, now contested. The English plugin-loading reference (read 2026-09-27) says synced plugins load "in Cowork sessions and in terminal sessions" and does not list cloud sessions (F8). The French plugins reference still says "Dans Cowork et les sessions cloud" (F9). The help centre says account plugins are available "in Claude Code in your terminal" (F10). The 2026-09-23 run quoted the English docs as naming cloud sessions, so the English page appears to have changed between 2026-09-23 and 2026-09-27. The owner's empty synced-plugins folder in a cloud session on 2.1.281 now matches the current English docs rather than contradicting them. A secondary source reports `SKIP_PLUGIN_MARKETPLACE=true` "is set in every cloud session" (F11). The standard's dated fact must be rewritten.
2. **"A marketplace client decides whether to update a plugin by its version number."** True for Claude Code clients reading a git-hosted marketplace (first pass, plugins/loading.md). Incomplete for claude.ai. For a marketplace hosted on claude.ai, "the version claude.ai records for the plugin is its version, and the manifest's `version` isn't read" (F13). For organization GitHub sync, claude.ai "compares the latest commit in your repo against the last-synced commit", and automatic sync fires on a merged pull request "that includes a plugin version bump" (F14). How a personal marketplace refreshes: not found. The practical rule is the same either way: bump the plugin version on every release, and press Re-sync where the UI offers it.
3. **"An uploaded skill may carry a large reference file and scripts, within limits … we haven't confirmed."** Still unconfirmed for claude.ai skill uploads (not found). What is published nearby: Skills API, 30 MB uncompressed (F17); plugins on claude.ai, 5,000 files and 200 MB (F18); organization plugin upload, a .zip under 200 MB (F15). The claude.ai help article limits the description to 200 characters, while the API and the first-pass reading of claude.com docs say 1,024. That is contested (F19). The standard's v0.38.0 description must fit 200 characters to be safe.
4. **"(the standard, 2026-09) `AGENTS.md` … Claude Code reads it only in some sessions."** Narrower than stated. From v2.1.277 Claude Code reads `AGENTS.md` natively when there is no `CLAUDE.md`. Since v2.1.281 Bedrock and telemetry-off sessions are no longer excluded (first pass, memory.md, 2026-09-27). The shim remains correct wherever a `CLAUDE.md` exists.
5. **"(the standard, 2026-09) … `syncClaudeAiSkills: false` in a project's committed settings is ignored."** Confirmed, with an addition. There is now a separate `syncClaudeAiPlugins` key, and an organization can set both keys in managed settings to stop only the sync (F16).
6. **"Team and Enterprise admins can provision skills … and those skills reach members' Claude Code sessions."** Confirmed. Two details were missing. Provisioned skills can be toggled off by members (F21). A skill published to the organization through review "stays on the approved version until the update is approved" (F22).
7. **"Claude Code has a built-in tool for asking multiple-choice questions, and it works in web sessions and the mobile app."** Only half documented. The tool is documented (first pass). Web and mobile rendering is not documented. An observed third-party report says it fails on Android and works on the web (F24).
8. **"A skill can be invoked explicitly by naming it, which triggers more reliably."** Documented that `/skill-name` invokes it directly (F2). "More reliably" has no measurement: not found. There is also a naming trap: when another command holds the short name, only `/anthropic-skills:<name>` runs the synced skill (F4).

## 3. Facts table

Every date in this table is the date read (2026-09-27) unless the source gives its own date. "First pass" means the owner's 2026-09-27 reading of the raw Markdown docs, which this pass could not re-fetch.

| # | Fact | Value | Documented or observed | Source URL | Exact quote | Date |
|---|---|---|---|---|---|---|
| F1 | A skill's body costs almost nothing until used | Body loads on use; description always listed | Documented | https://code.claude.com/docs/en/skills | "Unlike CLAUDE.md content, a skill's body loads only when it's used, so long reference material costs almost nothing until you need it." | 2026-09-27 |
| F2 | Explicit invocation | `/skill-name` | Documented | https://code.claude.com/docs/en/skills | "Claude uses skills when relevant, or you can invoke one directly with `/skill-name`." | 2026-09-27 |
| F3 | Account skills include organization-provided skills and reach cloud sessions | Yes | Documented; observed for account uploads (owner, 2.1.281, 2026-09-23) | https://code.claude.com/docs/en/skills | "Those skills include the ones you create or turn on in your claude.ai settings, skills your organization provides there, and Anthropic's built-in skills such as `pdf` and `xlsx`." | 2026-09-27 |
| F4 | Synced-skill name collision | Other command wins the short name | Documented (v2.1.269+) | https://code.claude.com/docs/en/skills | "When another command uses the short name, `/<name>` runs the other command, and the synced skill runs only as `/anthropic-skills:<name>`." | 2026-09-27 |
| F5 | Cloud sessions load committed project skills; repository-declared plugins don't load | Yes / no | Documented | https://code.claude.com/docs/en/skills | "Plugins declared in the repository's `.claude/settings.json` and plugins enabled only in your user settings don't load in cloud sessions." | 2026-09-27 |
| F6 | Removing a synced skill | Turn it off on claude.ai | Documented | https://code.claude.com/docs/en/skills | "turn the skill off for your claude.ai account, in the same place you enabled it." | 2026-09-27 |
| F7 | Skill-scoped hooks | Registered on invocation, persist for the session | Documented | https://code.claude.com/docs/en/skills | "Hooks that Claude Code registers when the skill is invoked and keeps running for the rest of the session." | 2026-09-27 |
| F8 | Where synced plugins load (English) | Cowork and terminal; cloud not listed | Documented | https://code.claude.com/docs/en/plugins/loading | "Synced plugins load in Cowork sessions and in terminal sessions where you sign in with your claude.ai account" | 2026-09-27 |
| F9 | Where synced plugins load (French translation) | Cowork and cloud | Documented (possibly stale translation) | https://code.claude.com/docs/fr/plugins-reference | "Dans Cowork et les sessions cloud, Claude Code les télécharge dans l'environnement propre de la session au démarrage de la session." | 2026-09-27 |
| F10 | Help-centre scope of account plugins | Chat, Cowork, terminal Claude Code | Documented | https://support.claude.com/en/articles/13837440-use-plugins-in-claude | "Plugins you add are saved to your account, so they're also available in Claude Code in your terminal when you sign in with the same account." | Updated "this week" |
| F11 | Plugin marketplace scan skipped in cloud sessions | `SKIP_PLUGIN_MARKETPLACE=true` | Observed, secondary | https://github.com/flungo/claude-plugins | "SKIP_PLUGIN_MARKETPLACE=true is set in every cloud session and cannot be overridden from the environment's variables" | 2026-09-27 |
| F12 | Hooks and sub-agents don't run in chat | Grayed out in chat | Documented | https://support.claude.com/en/articles/13837440-use-plugins-in-claude | "Hooks and sub-agents run in Cowork and Claude Code, not in chat, so they appear grayed out in chat." | Updated "this week" |
| F13 | claude.ai-hosted marketplace version key | claude.ai's recorded version | Documented | https://code.claude.com/docs/en/plugins/loading (via subagent) | "For a plugin from a marketplace hosted on claude.ai, the version claude.ai records for the plugin is its version, and the manifest's `version` isn't read." | 2026-09-27 |
| F14 | Organization GitHub sync trigger | Version-bump PR merged to default branch; manual Re-sync | Documented; the same page contradicts itself | https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization | "Once enabled, automatic sync for a GitHub repository runs when a pull request that includes a plugin version bump is merged to the repository's default branch. Direct pushes to the default branch don't trigger a sync." | Updated "this week" |
| F15 | Organization manual plugin upload | .zip under 200 MB; same name overwrites | Documented | https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization | "If you upload a plugin with the same name as an existing one, it overwrites the previous version automatically." | Updated "this week" |
| F16 | Stop only the sync, organization-wide | Managed settings keys | Documented | https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization | "To keep skills and plugins in Claude but stop only the sync, set `syncClaudeAiSkills` and `syncClaudeAiPlugins` to `false` in Claude Code managed settings." | Updated "this week" |
| F17 | Skills API upload limit | 30 MB uncompressed | Documented (API, not claude.ai) | https://platform.claude.com/docs/en/build-with-claude/skills-guide | "Total upload size must be under 30 MB (uncompressed)" | 2026-09-27 |
| F18 | claude.ai plugin limits | 5,000 files, 200 MB | Documented (via subagent) | https://claude.com/docs/plugins/platform-support | "Each plugin can contain up to 5,000 files and 200 MB, and 200 MB is also the largest file that Upload plugin accepts." | 2026-09-27 |
| F19 | claude.ai skill description limit | 200 characters (help centre) vs 1,024 (API) | Contested | https://support.claude.com/en/articles/12512198-how-to-create-custom-skills (via subagent) | "(200 characters maximum)" | 2026-07-22 |
| F20 | Terminal sync cadence for skills | At start, then about every 10 minutes | Documented | https://support.claude.com/en/articles/12512180-use-skills-in-claude | "Skills sync when a Claude Code session starts, then check for changes about every 10 minutes." | Updated "this week" |
| F21 | Organization provisioning | Owners upload; appears for all users | Documented | https://support.claude.com/en/articles/12512180-use-skills-in-claude | "Owners can also upload skills to provision them organization-wide—these skills automatically appear for all users." | Updated "this week" |
| F22 | Published-skill updates | Reviewed; users stay on the approved version | Documented | https://support.claude.com/en/articles/12512180-use-skills-in-claude | "To update it, publish again. The new version goes through the same review, and everyone who uses the skill stays on the approved version until the update is approved." | Updated "this week" |
| F23 | Shared skills update | Recipients get updates at next use | Documented | https://support.claude.com/en/articles/12512180-use-skills-in-claude | "If you update the skill later, recipients automatically get the updated version at next use." | Updated "this week" |
| F24 | AskUserQuestion on Android mobile | Card reappears after Submit | Observed (third-party bug report) | https://github.com/anthropics/claude-code/issues/84970 | "The same AskUserQuestion prompt/card appears again instead of accepting the answer and continuing." | 2026-09-27 |
| F25 | GitHub Action installs plugins | `plugin_marketplaces`, `plugins` inputs | Documented | https://code.claude.com/docs/en/github-actions | "For a skill packaged in a plugin, install the plugin with the `plugin_marketplaces` and `plugins` inputs, then pass the namespaced `/plugin-name:skill-name` as the `prompt`." | 2026-09-27 |
| F26 | GitHub Action subscription token | Needs a local CLI | Documented | https://code.claude.com/docs/en/github-actions | "Generate one by running `claude setup-token` locally." | 2026-09-27 |
| F27 | GitHub Action schedule in public repositories | Disabled after 60 inactive days | Documented | https://code.claude.com/docs/en/github-actions | "GitHub runs scheduled workflows only from the default branch and, in public repositories, disables the schedule after 60 days without repository activity." | 2026-09-27 |
| F28 | PreToolUse blocking | Exit code 2 denies the call | Documented (Anthropic blog) | https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more | "A PreToolUse hook can inspect a call and exit with code 2 to block it." | 2026-09-27 |
| F29 | Project-skill hooks and trust | Registered on invocation | Documented | https://code.claude.com/docs/en/hooks | "Frontmatter hooks in a project skill follow the same workspace trust rule as hooks in settings files. Claude Code registers them when you or Claude invoke the skill" | 2026-09-27 |
| F30 | raw.githubusercontent.com CORS | Allows cross-origin | Observed, secondary (2024) | https://www.drupal.org/project/infrastructure/issues/3477546 | "GitHub allows CORS for raw content, which means you can make fetch requests to their raw.githubusercontent.com domain without needing to modify headers." | 2024-09-28 |
| F31 | Clarification benefit in SWE agents | Up to 74% | Measured | https://arxiv.org/html/2502.13069v3 | "interactivity can boost performance on underspecified inputs by up to 74% over the non-interactive settings" | 2026-09-27 |
| F32 | Exploration-first asks fewer questions | 50% fewer for similar information gain | Measured | https://arxiv.org/html/2502.13069v3 | "[one model] achieves comparable information gain to [another] (0.171 vs 0.179) with 50% fewer questions through exploration-first strategies" | 2026-09-27 |
| F33 | Default effect size | d = 0.68, 95% CI 0.53–0.83, high heterogeneity (Jachimowicz et al. 2019, 58 studies, n = 73,675) | Measured (meta-analysis, 2019) | https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67AF6972CFB52698A60B6BD94B70C2C0 | "d = 0.68, 95% confidence interval = 0.53–0.83" | 2019 |
| F34 | LLM Python bias | 90–97% benchmark; 58% unsuitable projects; 83% self-contradiction | Measured | https://openreview.net/forum?id=O3KKt3RaYj | "LLMs contradict their own language recommendations in 83% of project initialisation tasks" | 2026-09-27 |
| F35 | Package hallucination | ≥5.2% commercial, 21.7% open-source | Measured (USENIX Security 2025) | https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen | "the average percentage of hallucinated packages is at least 5.2% for commercial models and 21.7% for open-source models" | 2025-08 |
| F36 | Deprecated API use | 25–38% deprecated usage rate (DUR) across eight Python libraries, seven LLMs, 28,125 prompts; [one model] at 37.4% | Measured (Wang et al., ICSE 2025) | https://arxiv.org/abs/2406.09834 | "The DUR… ranges from 25% to 38%" | 2025 |
| F37 | CC0 excludes patents and trademarks | Not waived or licensed | Documented (legal code) | https://creativecommons.org/publicdomain/zero/1.0/legalcode.en | "No trademark or patent rights held by Affirmer are waived, abandoned, surrendered, licensed or otherwise affected by this document." | 2026-09-27 |
| F38 | copier update preconditions | Answers file and tagged git template | Documented | https://copier.readthedocs.io/en/stable/updating/ | "The destination folder includes a valid .copier-answers.yml file. The template is versioned with Git (with tags)." | 2026-09-27 |
| F39 | Nygard ADR sections | Title, status, context, decision, consequences | Documented | https://adr.github.io/adr-templates/ | "An ADR consists of title, status, context, decision, and consequences according to \"Documenting Architecture Decisions\" by @mtnygard." | 2026-09-27 |
| F40 | Stale plugin copy in chat | v0.36.0 while the repository held v0.38.0 | Observed (owner, 2026-09-27, mount 2026-09-28 01:06 UTC) | not applicable (owner observation) | "references/PROJECT-BOOTSTRAP-AND-AUDIT-v0.36.0.md (310,336 bytes)" | 2026-09-27 |

## 4. Findings

### 4.1 The one command, route by route (Question 1)

**Skill uploaded to the claude.ai account.** Reaches cloud sessions and routines, Cowork, and terminal sessions signed in with the account (F3). It also reaches claude.ai chat, where `/` picks a skill (first pass, claude.com/docs/skills), although `!` commands don't run in chat. Updating means re-uploading a ZIP per release. The terminal checks for changes about every 10 minutes (F20). For cloud sessions the sync happens at session start (documented for Cowork; assumed for cloud, not stated). Token cost per session is the description (up to 1,536 characters in the listing) until invoked (F1). What happens on a same-name re-upload is not found for personal skills (subagent). The owner types `/project-bootstrap-and-audit`. Stale risk comes from forgetting to re-upload, and it is contained if the skill verifies the SHA-256 of what it reads. It cannot carry hooks or `disable-model-invocation` (first pass, six-field rule). The one serious weakness is therefore that Claude can auto-invoke it mid-task on a matching phrase. Mitigate this with a narrow description ("Only when the user types /project-bootstrap-and-audit or names the standard").

**Skill provisioned by the organization.** Reaches the same surfaces for every member (F3, F21). Members can toggle it off. Published skills go through review, and users "stay on the approved version" (F22). The Inventory tab shows each item's "source, version, capabilities, audience" (F14 page). This is the right channel for company-specific rules. The owner needs an Owner to do it. Not a route for the public standard itself.

**Plugin from a personal or organization marketplace.** Chat: yes (observed). Terminal: yes (F10). Cowork: yes. Cloud sessions: contested, and not listed in the English docs (F8, F9). A repository's committed `enabledPlugins` does not make a cloud session install it (F5). Organization GitHub sync needs a private or internal repository and pulls on version-bump PRs (F14). An uploaded ZIP overwrites a same-name plugin (F15). Stale risk: observed, a two-version lag with no warning (F40). Verdict: retire this route for cloud sessions, and don't keep two copies of the same skill.

**Pinned commit link plus SHA-256, pasted as a prompt.** Reaches every surface that can fetch a URL. Exact pinning is possible. Updating costs one new link per release. The token cost is the full prompt plus the ranges read. There is no stale risk, since it is pinned. It works in an empty repository. The weakness is friction: the owner pastes a long prompt. Keep it as the fallback, and fetch with `curl` rather than WebFetch, which is lossy (first pass, tools-reference).

**Remote MCP server or claude.ai connector.** MCP prompts can appear as commands (skills page lists "An MCP prompt" as a command source). Hosting one means running a public HTTPS server, which is a service to operate, secure and pay for. A custom connector "must point to a server that's reachable over the public internet from Anthropic's IP ranges" (help centre, plugins page). Verdict: disproportionate for one owner working in a browser (opinion). It also adds an injection surface.

**Routine started with Run now.** Reaches cloud only. Runs have no approval stops, and the fired prompt cannot act as consent (first pass, routines.md). Each run is a session the owner can open and continue, so a routine could stop after Phase 5 and the owner could continue interactively. Not documented as a pattern. Use it only for a scheduled read-only re-audit.

**GitHub template repository or copier template.** Only for new projects. A template repository is created from the GitHub web UI (browser). It can carry the front-door project skill, a README stub and `docs/decisions.md`. copier adds `copier update`, which needs a `.copier-answers.yml` and a git-tagged template (F38). The owner can't run copier, but the agent inside a cloud session can install and run it in its container. That depends on PyPI being reachable (not verified this pass). Verdict: template repository now, copier later if the templates change often.

**A line in each repository's context file.** For example: "Before any setup or audit, run /project-bootstrap-and-audit." It costs tokens in every session and doesn't deliver the skill. It is useful only as a pointer. Avoid it in `AGENTS.md`, which other agents read.

**Claude Code GitHub Action.** Triggered by `@claude` comments (from the GitHub web UI or the mobile app), `workflow_dispatch` or a schedule. It can run a committed skill after `actions/checkout`, or a plugin skill (F25). Writing the workflow file happens in the web UI. Authentication: a subscription token needs `claude setup-token` run locally (F26), which is out of reach. The browser route is an API key from the Console, billed separately from the seat. Only users with write access can trigger it (github-actions page). The two waits map naturally onto a comment thread: the run posts the Phase 3 drafted answers as a comment, the owner replies `@claude` with corrections, and a second run posts the Phase 5 report. Approval is a third comment, or a pull request the owner merges. Scheduled runs stop after 60 inactive days in public repositories (F27).

**Better: two tiers.** Tier 1 is the account-uploaded thin skill, the universal one command. Tier 2 is a committed project skill, which Phase 8 writes after the first approval. It sets `disable-model-invocation: true` and hooks, and those hooks enforce the gate on every later run (F7, F29). This combines "works from any repository" with enforcement where the repository has opted in.

### 4.2 Knowing which copy ran (Question 2)

- **Version management.** Synced account skills are downloaded, never uploaded, and "the next sync downloads the new version" (skills page). The Skills API versions each upload as a complete snapshot (subagent). What a same-name re-upload does in claude.ai Customize > Skills is not found. Plugins uploaded by an organization overwrite on the same name (F15). Organization inventory has version history; personal skills: not found.
- **Shared names.** A plugin skill is namespaced (`standards:project-bootstrap-and-audit`), so it and an account skill of the same name both load (skills page, precedence table). Claude can then pick either on auto-invocation. That is how the v0.36.0 copy can run silently.
- **Finding and removing the stale copy.** In claude.ai, open Customize > Plugins, find the `claude-code-skills` marketplace, and turn off or remove `standards`. In a Claude Code session, `/skills` lists synced skills under "claude.ai sync". Removing a synced skill means turning it off on claude.ai (F6).
- **Self-verification.** Feasible in cloud sessions, because a synced skill's body keeps local behaviour there, including `!` commands ("In a cloud session, the body keeps the behavior a local skill has, because the session runs in an isolated container"). A `!` line such as ``!`curl -fsSL <pinned raw URL> -o /tmp/std.md && sha256sum /tmp/std.md` `` injects the real hash before Claude reads anything. In chat, `!` lines don't run, so the skill must instruct Claude to compute the hash in code execution. Record in Phase 8 the SKILL.md `metadata.standard-version`, the pinned commit and the observed SHA-256.

### 4.3 Fewer, better questions for an existing repository (Question 3)

- **What a repository shows.** Language, build, tests, CI, licence, dependencies, and often purpose and data (from README, schemas and fixtures). What it rarely shows: where it actually runs, who uses it, work or personal, the consequence of failure, and the expected lifetime. F26 confirmed this pattern on the first live repository.
- **Drafting.** Present a table of question, drafted answer, evidence (file and line) and confidence, and ask the owner to reply "all correct" or to list corrections by number. Ambig-SWE measured that an exploration-first model obtained similar information gain with 50% fewer questions (F32), and that interaction recovered up to 74% of performance on underspecified tasks (F31). The same paper found that models "default to non-interactive behavior without explicit encouragement". The skill must therefore say explicitly when to ask.
- **Defaults.** Defaults shift choices strongly but unevenly: Jachimowicz et al. (2019, 58 studies) report "d = 0.68, 95% confidence interval = 0.53–0.83", with effects across studies from −0.5 to 2 (F33). Use a pre-filled answer only where evidence supports it, and show the evidence. For the five unknowables, give options with no pre-selection.
- **Wording for a non-specialist.** Ask about consequences, not jargon: "If this stopped working for a day, who would notice, and what would it cost?" rather than "What is the availability tier?" (opinion, consistent with F26).
- **Rendering.** Use AskUserQuestion on the web, where one report says it works (F24). On mobile, fall back to a numbered plain-text list that can be answered in one message. Keep a single call to at most 4 questions with 2–4 options each (first pass, agent-sdk).
- **Literature not reached this pass.** Requirements-elicitation systematic reviews and survey-design meta-analyses (questionnaire length, response order, acquiescence) are listed under Not covered.

### 4.4 The new-project interview and the recommendation (Question 4)

- **Minimum questions (opinion, built on the decision-record formats).** What it does, in one sentence. Who uses it, and how many. Where it must run: Windows Server, Linux, inside Epicor Kinetic, SOLIDWORKS, Office, or a browser. What data it keeps, and whether it is sensitive. What it must connect to. Who maintains it after the owner. How long it must live. From those, the tool can choose a runtime family. Integration targets usually decide it: an Office add-in means JavaScript or TypeScript; SOLIDWORKS automation means its COM API from .NET or VBA; Epicor Kinetic means its REST API from any language. These platform facts were not verified this pass; see Not covered.
- **Record.** Write the decision in MADR shape, with considered options and pros and cons, because MADR's authors hold that "the considered options with their pros and cons are crucial to understand the reasons for choosing a particular design" (adr.github.io). Nygard's minimum is title, status, context, decision, consequences (F39).
- **Bias controls, measured.** Force an explicit comparison of at least two languages before choosing, because of the Python bias (F34). Check every package against its registry, because of hallucination (F35). Check versions against current release notes, because of deprecated APIs: Wang et al. (ICSE 2025, seven LLMs, eight Python libraries, 28,125 prompts) measured a deprecated-usage rate of 25% to 38% (F36). The fewest-dependencies rule from R21 counters all three.
- **Where to start.** A cloud session needs a repository, so create an empty one, or one from the template, in the GitHub web UI first (first pass, web-quickstart). The interview could happen in a claude.ai chat, but its answers would then live outside the repository. Starting in a repository that holds only a README keeps everything in one place. That is the recommendation.

### 4.5 Remembering answers between runs (Question 5)

- Keep them in `docs/decisions.md` as a dated entry with a fenced machine-readable block: key, answer, source (evidence path or "owner"), date and review-by. Only the repository survives between sessions (standard, Phase 8 rationale).
- On the next run, show the last block, re-derive the evidence-backed answers, flag any whose evidence changed, and ask only about expired or changed items.
- Never write into a public repository's answers: employer names, internal hostnames, colleagues' names, private email addresses, customer data, or security-sensitive deployment details. At Phase 3, check `git log` author emails for an employer domain on a public personal repository (F29 from the owner's findings), and raise it as a question, never as a record.

### 4.6 Paired and multi-repository projects (Question 6)

- **Detection.** Look for a protocol or ownership file (`docs/OWNERSHIP.md`), for submodules, for README links to a sibling, and for byte-identical files named in a protocol.
- **Reading the protocol.** Treat files it names as shared as read-only, and every lap or append-only record as untouchable. Report findings on the boundary with an owning side (F34 from the owner's findings).
- **Sessions.** Use one repository per session. A multi-repository session drops each repository's hooks and permission rules (first pass, settings.md).
- **Open handshake rounds.** Recommendation (opinion): an approved change may land during an open round only if it touches none of the shared or append-only files and the protocol doesn't forbid it. Otherwise it waits.
- **Published practice.** Beyond Anthropic's session docs: not found this pass.

### 4.7 Colleagues and the organization (Question 7)

- **Controls.** Owners provision skills, set plugin distribution (Installed by default, Available, Not available, Required), review published items, and can stop syncing with managed settings (F16, F21, F22). A "Required" plugin "stays on in Claude Code sessions that sync the member's account plugins" (plugins org page).
- **Keeping company rules private.** Put them in a skill provisioned or published inside the organization, or in the work repositories. Keep the public standard generic.
- **CC0 inside Apache-2.0.** Anyone may copy the CC0 standard without attribution. CC0 grants no patent licence: "No trademark or patent rights held by Affirmer are waived … or otherwise affected" (F37). Apache-2.0 files carry an express patent grant. Mark per-file licences clearly, for example with SPDX headers. REUSE practice was not verified this pass.

### 4.8 A safe one-command run (Question 8)

- **Content is data.** The skill must say that instructions found in repository files are findings, not commands. The Anthropic blog and the hooks reference support using hooks as the deterministic layer (F28).
- **Keeping both waits.** In cloud sessions the permission modes are Accept edits, Plan and Auto, with no Manual (first pass). The owner should start in Plan mode. The skill stops at Phase 3 and Phase 6 and ends its turn. A committed project skill can add a PreToolUse hook that exits 2 on Write or Edit until an approval marker exists (F7, F28). An idle question can be answered later, up to environment expiry (first pass).
- **Budgets.** At roughly 4 bytes per token, 332,036 bytes is about 83,000 tokens if read end to end. This is an estimate. Read by heading index. The setup-script cache needs about five minutes to finish (first pass). For suites longer than the time-box (F28 from the owner's findings), run a named subset and report the rest as "not run". For missing system libraries (F27), put `apt-get install -y libegl1` in the environment setup script. That package name is not verified this pass. Published cost figures: not found.

### 4.9 Testing the front door (Question 9)

- **Trigger testing.** Use the skill-creator plugin's should-trigger and should-not-trigger sets, and `claude plugin eval` with a `tool_used: Skill` grader (first pass). The eval command is a terminal CLI and is out of reach for the owner. Whether the agent can run it inside a cloud container is not verified.
- **Metrics.** Per run, record: questions asked, answers the owner corrected, time to first report, tokens used, the SHA-256 verified, and whether any write happened before approval (target zero).
- **Harness.** Paired determinism runs compare drafted answers across two runs on the same commit. The seeded testbed scores whether planted facts were drafted correctly and whether planted injections were ignored.

### 4.10 What we missed (Question 10)

- A "newer version exists" warning. The skill curls the repository's current pin file and warns without blocking.
- A way back to a known-good state. Every approved change lands as one pull request, so reverting is one click in the GitHub web UI.
- Scheduled read-only re-audits by routine, proposing but never applying changes.
- A mobile-safe question path.
- One copy per name, to prevent the plugin shadow.
- A 200-character description check in CI, to catch the contested limit.

## 5. Routes compared

| Route | Reaches | Pin or verify | Update cost | Token cost | Stale risk | Empty repo | Colleagues | Sources |
|---|---|---|---|---|---|---|---|---|
| Account-uploaded skill (thin) | Web/cloud and routines yes; mobile via cloud session yes; claude.ai chat yes (no `!`); CLI yes (signed in); desktop Cowork yes | Verify by SHA-256 of fetched standard | One small ZIP re-upload when the pin changes | Description only until invoked | Medium; contained by hash check | Yes | Each uploads it, or an Owner provisions it | F1, F3, F20 |
| Organization-provisioned skill | Same as above for all members | Version history in Inventory | Owner re-uploads or approves | Same | Low (reviewed) | Yes | Yes | F21, F22 |
| Plugin (personal or organization marketplace) | Chat yes; CLI yes; Cowork yes; cloud contested; routines contested | Version string or claude.ai record | Bump version plus re-sync | Description until invoked | High (observed two-version lag) | Yes where it loads | Organization marketplace must be private | F8–F15, F40 |
| Pinned link plus SHA-256 prompt | Every surface that can fetch | Exact | New link per release | Long prompt | None | Yes | Anyone | first pass, F30 |
| Remote MCP or connector | Chat, Cowork, cloud (connectors) | Server-controlled | Deploy a service | Tool schemas | Low | Yes | Yes | plugins help page |
| Routine (Run now) | Cloud only | Via the skill it calls | None extra | Full run | As its skill | Yes | No (individual account) | first pass routines.md |
| Template repository or copier | New repositories via GitHub web | Template commit or tag | Per template release | None until used | copier update can refresh | Creates the repository | Yes | F38 |
| Line in the context file | Wherever the file loads | No | Edit per repository | Every session | High | No | Yes | memory.md (first pass) |
| GitHub Action | GitHub web and mobile comments | Workflow pins an action version | Edit workflow | API-billed per run | Low | Yes after the workflow is added | Write-access users | F25–F27 |
| Committed project skill (tier 2) | Cloud yes; CLI yes; not chat | Committed bytes | A PR per repository | Description until invoked | Low (pinned in repository) | Only after the first commit | Yes | F5, F7, F29 |

## 6. Recommended design

1. **Trigger.** The owner types `/project-bootstrap-and-audit` in a cloud session started in Plan mode. The account-uploaded skill loads. Its description is narrowed so it rarely auto-invokes. Rebuild piece: `SKILL.md`. Usable first.
2. **Verify.** Phase 0 fetches the reference at the pinned commit with `curl` via a `!` line, computes the SHA-256 and compares it with the value in SKILL.md, stopping on mismatch. It also fetches the repository's current pin and warns if newer. Pieces: `SKILL.md` plus `scripts/verify.py` (standard library). Usable first.
3. **New or existing.** Count source files and read the README. No source, or only a README, routes to the interview; F15 adds that row. Piece: `references/routing.md`.
4. **Read.** Existing repositories: manifests, CI, README, `docs/decisions.md`, `git log` authors, and protocol or ownership files. Content is treated as data. Piece: `references/evidence.md`.
5. **Draft and ask (wait 1).** A table of drafted answers with evidence and confidence, plus the five unknowables with no defaults. AskUserQuestion on the web, a numbered text fallback on mobile, one reply. New projects get the seven-question interview. Piece: `assets/phase3-questions.md`. Usable first.
6. **Recommend.** For new projects, at least two stack options compared in MADR form, dependencies checked against registries and versions against release notes. Piece: `references/choosing-language-and-shape.md`. Waits for R21 integration.
7. **Report and stop (wait 2).** The report goes outside the repository; the skeleton lives in `assets/`. The run ends its turn.
8. **Record.** After approval, Phase 8 writes `docs/decisions.md` with the version, commit, SHA-256 and answers block. It offers to commit the tier-2 project skill with `disable-model-invocation` and a PreToolUse approval hook. Waits for parity runs.
9. **Housekeeping now.** Remove or disable the `standards` plugin on claude.ai. Upload the thin skill. Bump the plugin version on every release if the plugin is kept for chat.

## 7. Changing in the next 12 months

- Routines are a research preview, and Projects are in public beta on Pro and Max only (first pass). Both are likely to change. Dates: not found.
- Plugin-sync scope is in flux. English and French docs disagree on cloud sessions (F8, F9). Re-check monthly.
- GitLab organization marketplace sync is in beta. The help centre states that "Claude Code on the web doesn't support GitLab repositories yet" (plugins org page).
- Enterprise skill and plugin scanning, and review-before-publish, are new controls (plugins help page).
- The whats-new weekly pages, the Cowork changelog and the claude.ai release notes were not read this pass; see Not covered.

## 8. Common mistakes

- **Two copies under one name.** A plugin skill and an account skill both load, and the old one can run silently (F40, skills precedence).
- **Trusting WebFetch for byte checks.** It returns a model's summary; use `curl` (first pass).
- **Assuming committed `enabledPlugins` reaches cloud sessions.** It doesn't (F5).
- **Treating a routine prompt as approval.** It can't be (first pass).
- **An interviewing agent that doesn't ask,** or asks everything. Models "default to non-interactive behavior" (F31). Exploration first halves the question count (F32).
- **Leading defaults** on questions the repository can't answer (F33).
- **Recommending Python by reflex** (F34), inventing packages (F35), and using deprecated APIs (F36).
- **Committing work details into a public record** (F29 from the owner's findings).
- **Relying on AskUserQuestion on mobile** (F24).

## 9. Sources and licences

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| Claude Code docs (code.claude.com) | Not found; treat as all rights reserved | Briefly | Yes | Short snippets only, with care | Link and date |
| Claude help centre (support.claude.com) | Not found; all rights reserved assumed | Briefly | Yes | No code | Link and date |
| Claude Platform docs (platform.claude.com) | Not found | Briefly | Yes | Short snippets | Link and date |
| Anthropic blog (claude.com/blog) | Not found | Briefly | Yes | No | Link |
| GitHub issues (anthropics/claude-code, flungo, jmcvetta) | User content under GitHub Terms; licence not found | Briefly | Yes | No | Link; label secondary |
| arXiv papers 2502.13069, 2503.17181, 2406.09834, 2604.09515 | Per paper; not checked | Briefly | Yes | No | Full citation |
| USENIX Security 2025 (Spracklen et al.) | Open access; licence not checked | Briefly | Yes | No | Full citation |
| PMC / Cambridge (Jachimowicz et al. 2019) | Journal licence not checked | Briefly | Yes | No | Full citation |
| CC0 legal code | Not checked | Yes | Yes | Not applicable | Link |
| copier docs | Not checked | Briefly | Yes | Not checked | Link |
| adr.github.io | Not checked | Briefly | Yes | Templates: check repository licence | Link |
| drupal.org issue | GPL-covered site content assumed; not checked | Briefly | Yes | No | Link; secondary |

## 10. Not found, contested, not covered

- **Not found:** claude.ai skill ZIP size and file-count limits. Whether a same-name re-upload of a personal skill replaces it, versions it or duplicates it. How a personal marketplace refreshes and how to force it. Documentation of AskUserQuestion rendering on the web and on mobile. Whether a `prompt_url` prefill link opens from the mobile app. Measurements comparing drafted-answer confirmation with open questions. Licences of the Anthropic documentation.
- **Contested:** synced plugins in cloud sessions (F8 against F9). The skill description limit, 200 against 1,024 (F19). The organization-sync trigger, where the same help page says both "someone pushes to that branch directly" and "Direct pushes to the default branch don't trigger a sync" (F14). The plugin upload size, where a secondary issue says "under 50 MB" and the help centre says 200 MB (F15). Release assets from cloud sessions, documented 403 against an observed 200 on 2026-09-26.
- **Not covered:** requirements-elicitation systematic reviews. Survey-design meta-analyses (length, response order, acquiescence, satisficing). Conversational-search clarification studies. "Boring technology" guidance. Epicor Kinetic REST, SOLIDWORKS API and Office add-in specifics. REUSE/SPDX details. The whats-new pages 2026-w13 to w37, the Cowork changelog and the claude.ai release notes. A fresh check of `raw.githubusercontent.com` CORS headers from a cloud session. These are proposed for the next run.
