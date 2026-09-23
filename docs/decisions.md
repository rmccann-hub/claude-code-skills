# Decisions

Append-only. Supersede by adding a new entry that points at the old one; never edit history.

## 2026-09-23 — The standard moves to v0.37.0

- **Chosen:** eighteen fixes to the standard, applied together at the owner's request, so the
  one file can audit the owner's public repositories now and bring results back:
  - the nine findings from the parity baseline, F1-F9 in `ROADMAP.md`;
  - the set-up run's open amendments S2-S7 and S9-S11.

  Each had been proposed and was waiting for approval. They land in the standard file rather
  than piece by piece, and the rebuild's pieces move the fixed text.
- **Chosen:** 0.37.0, a minor bump. The new rules and fields are additive (`owner: mixed`,
  `recommended` and `pending` in the Phase 3 block, `shape_recommended`, `category_checks`), so
  older reports stay readable.
- **Not included:** S8, a Keep current mode for the standard. The roadmap's `keeping-current`
  skill covers it.
- **Checked:** the facts behind two new rules, against their primary sources on 2026-09-23.
  GitHub's workflow syntax says a `run` step with no `shell:` runs `bash -e {0}`, and naming
  `shell: bash` adds `-o pipefail`. Git's documentation says `GIT_OPTIONAL_LOCKS` set to false
  "will prevent git status from refreshing the index". Under `bash -e` with nothing collected,
  the old guard exited 1 and printed nothing; the new one names the failure.
- **Not checked here:** the current `actions/checkout` release. This session can't reach that
  repository, so v7.0.1 is the set-up run's reading, and the release this repository's
  Dependabot pins.
- **Deferred:** this repository's own CI guard copies the template's, and gets the same fix in
  a change of its own. *Trigger:* this change merges.

## 2026-09-23 — Release 0.1.1: the marketplace takes the repository's name

- **Chosen:** the marketplace is renamed from `rmccann-skills` to `claude-code-skills`, so that
  it matches the repository. The owner asked for the names to match. claude.ai shows a
  marketplace added from a repository by the repository's name, while Claude Code shows the
  catalog's `name`, so the two differed. This supersedes the marketplace name in the inception
  entry's H3. The plugin stays `standards`.
  - *Considered:* renaming the repository instead. That touches 36 files, among them the
    owner-file lines in `AGENTS.md` and dated research records.
  - *Risk:* Claude Code blocks marketplace names that impersonate official ones, and re-checks
    at every load. `claude-code-skills` isn't on the reserved list, and Claude Code 2.1.280's
    strict validator passes it (checked 2026-09-23). *Reopen when:* Claude Code rejects the
    name.
- **Chosen:** the rename ships as release 0.1.1, with standard v0.36.0. A version that reaches
  `main` is published, so a breaking change can't reach it under 0.1.0. And 0.1.0 already named
  two standards: v0.35.0 at its tag, and v0.36.0 on `main`. This settles the release that the
  v0.36.0 entry deferred. The owner chose 0.1.1 over 0.2.0: under 0.x anything may change
  (A13), and 0.2.0 stays the rebuild's release.
- **Chosen:** the catalog's plugin entry names its author and repository, as a plugin's own
  manifest does. Claude Code's strict validator asks a manifest for an author.

## 2026-09-23 — The plugin reaches the account, not cloud sessions

- **Found:** the plugin can be enabled for the owner's claude.ai account. The owner added this
  repository as a marketplace of their own, under Customize > Plugins > Personal plugins > Add
  marketplace > Add from a repository, and installed `standards` 0.1.0 with no error. claude.ai
  took the catalog as it stands, with the plugin defined in `marketplace.json`
  (`strict: false`) and no `plugin.json`. It names the marketplace after the repository,
  `claude-code-skills`, rather than the catalog's `rmccann-skills`.
- **Found:** cloud sessions don't load it.
  - A fresh session started a few minutes after the install, on Claude Code 2.1.281. Its
    folder for synced plugins was empty, and it had no `standards` skill.
  - About ten minutes after the install, a lookup of the account's enabled plugins still found
    none.
  - The working session that made the lookup had pulled in the account's skills when it
    started, but none of the Anthropic plugins listed on the account since the day before.

  Claude Code's plugins reference says cloud sessions download the plugins enabled for the
  account when they start (checked 2026-09-23). So either the product doesn't yet match its
  docs, or a condition applies that they don't state.
- **Found:** the organization route is closed to this repository. The Help Center says a
  GitHub-synced organization marketplace "must be private or internal" (checked 2026-09-23),
  and this repository is public. An organization could still take the plugin as an uploaded ZIP
  file, one upload per release.
- **Chosen:** H2 stands, and with it the six-field frontmatter rule: uploading the skill to
  claude.ai stays the route into cloud sessions. That answers the *To verify* item in the entry
  below. Nothing is lost yet, because the plugin carries only a skill. Hooks and subagents are
  what would need the plugin route.
  *Reopen when:* a cloud session's `~/.claude/plugins/synced/` holds the account's plugins, or
  a piece of the rebuild adds hooks or subagents.
- **Chosen:** sessions on this repository don't load an installed copy of the plugin, so a
  session rebuilding the skill, or a parity run, can't pick up an older one. `.claude/settings.json`
  turns off `standards@synced` and `standards@claude-code-skills`, which Claude Code's docs let a
  project do in its committed settings (checked 2026-09-23). A copy uploaded as a claude.ai
  skill can't be turned off from here, so `CLAUDE.md` says the file here wins, and a parity run
  needs it turned off on the account.

## 2026-09-23 — The standard is rebuilt into the skill

- **Chosen:** the standard stops being a separate document. Its content becomes the parts of the
  `project-bootstrap-and-audit` skill:
  - a procedure;
  - references by topic;
  - tested templates;
  - scripts;
  - a report schema.

  Its self-management goes: its own version, version history, test procedure and change
  process. This repository's history, changelog, decision record and tests already do that job.
  The owner approved a section-by-section map of where everything goes. Its pieces are in
  `ROADMAP.md`.
- **Chosen:** it lands in seven pieces, with the parity checks first. Each piece moves its
  sections out of the standard file in the same commit, and is checked against the version
  before it (`docs/testing-the-skill.md`). The file is deleted in the last piece, which is
  release 0.2.0.
- **Chosen:** built for Claude Code first, and kept usable with other AIs such as Gemini and
  ChatGPT without going out of the way (the owner's direction):
  - frontmatter stays at the six Agent Skills fields;
  - scripts use only Python's standard library;
  - each Claude Code-only feature is marked with what it does, so another tool can look for its
    own equivalent.
- **Chosen:** the owner works in cloud sessions, and those load only what's enabled on the
  owner's claude.ai account or committed to the repository being worked on (Claude Code's docs,
  checked 2026-09-23). So the claude.ai account stays the route into them, and H2 (below) stands.
  *To verify:* whether this repository's plugin can be enabled for that account. If it can, its
  hooks and subagents would reach cloud sessions.
- **Chosen:** the rebuilt skill is Apache-2.0, like the rest of the repository, from piece 6.
  The standard's versions up to v0.36.0 stay CC0-1.0 in git. From then on, this supersedes the
  inception entry's line that the standard keeps its own CC0-1.0 dedication.
- **Chosen:** parity runs happen in the working session, as fresh subagents.
  - *Deferred:* `claude plugin eval` in CI. *Trigger:* an Anthropic API key is stored as a
    repository secret.
  - *Open:* the report's format, Markdown with YAML blocks and a checker, or JSON. It's decided
    at piece 1.
- **Supersedes, from piece 6:** the inception entry's gate default that the standard ships as a
  skill (H6).

## 2026-09-23 — The standard moves to v0.36.0

- **Chosen:** nine of the standard's dated facts were corrected, each checked against its
  primary source (research R01, R02, R05 and R08). The maintainer approved the fixes, and they
  were applied on their own.
- **Chosen:** 0.36.0 rather than 0.35.1. One fix retires a rule: the `CLAUDE.md` shim no longer
  becomes `OVER` once Claude Code reads `AGENTS.md` natively, because native reading has
  conditions. The standard's versioning makes that a minor bump, since a patch changes no
  output.
- **Not included:** the other amendments to the standard from the set-up run (S2-S11). They
  stay open for the maintainer.
- **Deferred:** a release for it, at the maintainer's choice. The catalog stays at 0.1.0, so
  copies already installed at 0.1.0 keep v0.35.0: Claude Code updates an installed plugin only
  when its version changes. Until the next release, `main` and the `v0.1.0` tag carry different
  standards under the same version number. *Trigger:* the next release.

## 2026-09-23 — Hidden-character checks beyond skills

- **Chosen:** `skillcheck` checks `AGENTS.md`, `CLAUDE.md`, `.claude/` and `research/` for hidden
  and bidirectional characters, as it already did for skills (A30). Agents read these files as
  instructions or context, and research results are pasted in from outside the repository.
  R01 recommends this check for agent-instruction files. The owner approved it on taking in
  R01-R05 and R08.

## 2026-09-23 — Before the first merge: the 0.1.0 release, and a cost of SHA pins

- **Chosen:** the first merge to `main` is the 0.1.0 release (A29), because a version that
  reaches `main` is published, tag or no tag. The changelog's entries moved under `[0.1.0]`,
  and the README's Operations section says how to withdraw a bad skill. This settles the
  runbook that the inception entry below deferred until the first release.
- **Chosen:** keep A16's SHA pins, knowing a cost the gate didn't state. GitHub's secure-use
  reference (checked 2026-09-23) says "Dependabot only creates alerts for vulnerable actions
  that use semantic versioning and will not create alerts for actions pinned to SHA values."
  Weekly version updates still cover the pins, and their tag comments on the same line.
  *Reopen when:* GitHub raises alerts for SHA-pinned actions, or a vulnerability in a pinned
  action is found before an update for it reaches this repository.

## 2026-09-23 — Inception: set up against the standard

- **Standard:** PROJECT-BOOTSTRAP-AND-AUDIT v0.35.0. Job: set up; mode: greenfield. The run
  stopped at its Phase 6 gate, and the maintainer approved everything below there.
- **Tier:** T3 (blast radius B3, audience A3), rated on the imminent state. B3 on the output:
  skills from here load into sessions on work repositories whose output reaches production.
  A3: public users are intended. Both become current with the first consumer install.
- **Ownership and permission:** the sessions that produced this material ran on an
  organization's Claude plan, and under Anthropic's Commercial Terms (checked 2026-09-23) the
  organization owns their output. The maintainer holds the organization's written permission,
  from someone who can sign for it, to publish the generic, non-confidential skills and
  tooling here under Apache-2.0. The permission itself is kept privately. No copyright notice
  was added: none was named at the gate, and Apache-2.0 does not require one.
- **Chosen:** layout. Flat `skills/<name>/` in the Agent Skills layout, grouped into plugins only
  by `.claude-plugin/marketplace.json` entries (`source: "./"`, `strict: false`). Regrouping
  never moves files, and each skill directory can be uploaded to claude.ai or copied into
  another repository unchanged.
- **Chosen:** tooling in Python with uv; runner-up TypeScript. Python is present in cloud
  sessions and CI, most scripts in the old skills this library rebuilds from are Python, and
  `pwsh` is not installed in cloud sessions (re-checked 2026-09-23).
- **Chosen:** Apache-2.0 for the repository, replacing the CC0-1.0 file it was created with,
  before any content was added. The standard keeps its own CC0-1.0 dedication, and its skill's
  `license` field says so.
- **Chosen:** versioning (A13). Semantic Versioning, with one version for the whole repository,
  set in each catalog entry and bumped only on release. The changelog is written before the
  tag, and no pre-release labels are used.
  - *Major:* anything a consumer cannot take unchanged. That includes renaming or removing a
    skill, because a skill's name is public interface.
  - *0.x:* anything may change, and breaking changes are listed first in the changelog.
  - *1.0:* when the maintainer is ready to keep the skill names and the catalog's shape. That
    decision is recorded here when it is made.
  - A version that reaches `main` is published, tag or no tag.
- **Chosen, as the gate's defaults:**
  - released skills reach the maintainer's own sessions by upload to claude.ai (H2);
  - the marketplace is `rmccann-skills`, and the first plugin is `standards` (H3);
  - the standard ships as a skill (H6);
  - the skill-building toolkit is included (H7).
- **Chosen:** GitHub Actions pinned to full commit SHAs, each with its release tag in a comment
  (A16). A library that other repositories install from is part of their supply chain.
- **Chosen:** the plan lives in `ROADMAP.md`, not in issues (A28). This repository publishes its
  plan, and `skillcheck` fails whenever the roadmap, the README's skill table and `skills/`
  disagree.
- **Chosen:** the standard's own mechanical checks (its Test G) run in CI on every change (A27).
- **Declined:** A17, an OpenSSF Scorecard workflow. Its Code-Review and Contributors checks
  cannot pass with one maintainer. *Reopen when:* a second person commits.
- **Declined:** A18, a local pre-commit hook. Cloud sessions commit without it, and CI gates the
  same checks. *Reopen when:* a secret or a lint failure reaches a pushed branch.
- **Declined:** A19, mutation testing. Branch coverage is 100%, so every finding the checker can
  raise is raised by at least one test. *Reopen when:* a check is found letting through a
  defect its test says it catches.
- **Not applied:** S1-S11, changes to the standard itself. A run never edits the standard, and
  none was ticked at the gate. They are in the run report, for the maintainer.
- **Deferred:** A21, the `skill-builder` skill. *Trigger:* its turn in the build order.
- **Deferred:** a runbook for withdrawing a bad skill. *Trigger:* before the first release.
- **Deferred:** the upstream defect register, a `copier` template and reusable workflows.
  *Triggers:* in `ROADMAP.md`, under Repository.
- **Do not re-propose:** rewriting history to change the initial commit's author email. It would
  rewrite a published default branch.
- **Do not re-propose:** importing or adapting Anthropic's source-available document skills
  (docx, pdf, pptx, xlsx). Their licence forbids derivative works and copies outside Anthropic's
  services (checked 2026-09-23).
- **Alias:** the decision record here is `docs/decisions.md`.
