# Decisions

Append-only. Supersede by adding a new entry that points at the old one; never edit history.

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
