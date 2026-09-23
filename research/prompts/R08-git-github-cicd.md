# RESEARCH RUN R08: Git, GitHub, code review, and CI/CD

For the repository rmccann-hub/claude-code-skills · Prompt version 2 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: git-and-review, ci-cd, and the standard's CI, dependency and security dimensions.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R08 · FORM: research-result v1
Save as: R08-RESULT.md
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

- Git 3.0 is planned to default to SHA-256 and to the branch name "main"; Git 2.5x is current.
- (the standard, 2026-09) Classic branch protection and rulesets are available for public repositories on a free plan, and for private ones on a paid plan, where GitHub Pro is enough for a personal account. Push rulesets need an organisation plan.
- (the standard, 2026-09) Secret scanning and push protection are free and on by default for public repositories. GitHub's own pages disagree on the default for push protection, so settle it.
- GitHub changed how pull_request_target runs in late 2025, so that workflows run from the default branch.
- zizmor is a static analyzer for GitHub Actions security, actionlint checks workflow correctness, and StepSecurity Harden-Runner monitors runners.
- pre-commit (4.x) is the standard hook framework; prek is a newer, faster compatible implementation; lefthook is an alternative.

## Questions

### Priority

1. Branching and merging for a solo maintainer and for small teams: trunk-based development versus GitHub Flow versus Git Flow, from current authoritative sources (for example trunkbaseddevelopment.com, DORA research). Also merge strategies (squash, rebase, merge commits), linear history, and merge queues.
2. Commits and pull requests:
   - Conventional Commits, and commit message guidance (the Git project's SubmittingPatches, widely cited rules)
   - research on pull request size, review checklists, Conventional Comments
   - signed commits (SSH signing, Sigstore gitsign) and GitHub's vigilant mode
3. GitHub settings for a public repository today, saying for each whether it is free on a personal account, whether it is on by default, and its menu path:
   - rulesets (required checks, blocking force pushes and deletion, required reviews with one maintainer)
   - secret scanning and push protection, and private vulnerability reporting
   - Dependabot alerts and security updates, and code scanning's default setup
   - CODEOWNERS, immutable releases, merge queue availability
4. GitHub Actions security hardening:
   - GitHub's official hardening guide
   - permissions (least privilege, `permissions: {}`) and `persist-credentials`
   - pinning actions to commit SHAs, and the policy that enforces it
   - the risks of `pull_request_target` and `workflow_run`, and the 2025 changes
   - OIDC for cloud credentials, artifact attestations, self-hosted runner risks
   - script injection through `${{ }}` expressions
   - tools, with current versions: zizmor, actionlint, Harden-Runner, OpenSSF Scorecard
5. The current major versions and full 40-character commit SHAs of actions/checkout, actions/setup-python, actions/setup-node, actions/setup-go, actions/setup-dotnet, actions/cache, actions/upload-artifact, actions/download-artifact, astral-sh/setup-uv and github/codeql-action. Also any deprecations: Node.js runtimes for actions, artifact v3 removal, cache service changes.

### Standard

6. Hooks: the pre-commit framework (current version), prek, lefthook, Husky. What belongs in local hooks and what belongs in CI?
7. CI design:
   - caching, matrix builds, concurrency groups
   - path filters (the rules for `paths` and `paths-ignore`), and required checks under path filters (the skipped-check problem)
   - reusable workflows and composite actions
   - environments and deployment protection
8. Code review practice: Google's engineering practices guide, Microsoft's research on code review, what reviewers should look at first; AI code review tools (for example GitHub Copilot code review) and how teams use them responsibly.
9. Git hygiene: .gitignore templates (github/gitignore), .gitattributes (line endings, binary files, linguist), large files (Git LFS), removing secrets from history (git filter-repo, BFG), `git check-ignore -v`.
10. Git 3.0 plans, and notable user-facing features of recent Git releases.
