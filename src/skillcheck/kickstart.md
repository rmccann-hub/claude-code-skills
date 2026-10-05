> **About this file.** This is the kickstart file from release RELEASE_VERSION of
> REPOSITORY. It holds standard vSTANDARD_VERSION, whose full file has this SHA-256:
> `STANDARD_SHA256`
>
> The two sections no run reads are left out: *Validating a Change to This Standard* and
> *Provenance*. The standard's text is otherwise unchanged. Around it, this file adds its first
> lines, these run instructions, the frontmatter's `extract` and `run_file` lines, and the end
> marker. The routing table and a few sentences still name the two sections; a job that needs
> them needs the full file, from the same release.

**Run instructions.** They say which job to run and what holds throughout. The standard below
governs everything else.

**The job, chosen by what the repository holds.** If the person's message names a job, that job
wins. Otherwise:

- **No repository yet, or one that holds no source:** choose a language and a shape with the
  person, by the routing table's row for that job. Ask what the project is for, who runs it,
  where it runs and what it keeps, then recommend a language and a shape, each with a runner-up
  and what each choice costs. Stop at the Phase 3 wait. Nothing is chosen by default. Once the
  person picks, set the repository up by the row for setting up something new, and stop at the
  Phase 6 gate.
- **A repository with source, whose decision record has no entry from an earlier run of this
  standard:** audit it, through every phase, and stop at the Phase 6 gate.
- **A repository whose decision record has such an entry:** re-check it, as Phase 1 directs.
  Show each recorded answer and ask whether it still holds.

**What holds throughout.**

- Use no other copy of this standard. A copy installed as a plugin or synced from an account may
  be another version. Record this file's SHA-256, as received, in the self-check's
  `standard_sha256`, because an upload may rename it. If the last line isn't the end marker, the
  file arrived cut short: stop and say so.
- Write nothing to the repository and push nothing until the person has answered the Phase 6
  gate: no branch, commit, tag, release or setting.
- Keep the run report outside the repository, in the session's scratch space. At each stop, send
  it as a file and give its path.
- At the Phase 3 wait, draft each answer the repository supports, with its evidence, for the
  person to confirm. Production, dependents and where it runs are never drafted, so ask them
  outright.
- Write for readers other than the person running this. Everything proposed for the repository,
  from documentation and the decision record to commit messages and the pull request, is
  neutral and exact, with no personal or session detail and no shorthand a reader can't look up.
- After the gate, apply only what the person approved, on a branch, and open a pull request for
  it. Don't merge it or cut a release unless the person asks.

**The repository's settings.** They live on the forge, not in the repository, so read them on
their own. On GitHub:

- **Read what you can, with read-only calls:** `gh api repos/OWNER/REPO`, and its `rulesets`,
  `immutable-releases`, `private-vulnerability-reporting` and `code-scanning/default-setup`
  paths. A session often can't read the Actions settings. Ask for what you can't read at the
  Phase 3 wait, as the standard says, with the page's link: `settings/actions`,
  `settings/rules` or `settings/security_analysis`, after `https://github.com/OWNER/REPO/`.
- **Read the plan from a private repository.** A `rulesets` call that answers 403 and says to
  upgrade to GitHub Pro means the account is on GitHub Free.
- **Read the addresses on the person's own commits** in a public repository: those whose GitHub
  author is the person. A personal address there is public, and it stays on every commit
  already published. The account's email settings below keep it off the next one. Never
  propose rewriting published history to remove it, and name the address in the report only,
  never in the repository.
- **Change no setting yourself,** even after the gate, unless the person asks you to. A setting
  to change is an action only the person can take, in the gate's third list. Give one for each
  row below that differs or that you couldn't read, saying what it is now, what to set it to,
  and where. Leave out the rows that don't apply to the repository's visibility and plan.
- **The rulesets import.** Release RELEASE_VERSION carries `ruleset-default-branch.json` and
  `ruleset-release-tags.json`, on its page:
  https://github.com/REPOSITORY/releases/tag/vRELEASE_VERSION
  In Settings, Rules, Rulesets, the New ruleset menu has Import a ruleset. Then add the
  repository's CI jobs to the default-branch ruleset, under Require status checks to pass, by
  the names their checks report.

The paths are from GitHub's documentation, checked 2026-10-05. Where a page shows something
else, report what it shows.

| Setting | Set it to | Where, in the repository's Settings | Where it applies |
|---|---|---|---|
| Merge methods | Only the strategy the context file records | General, Pull Requests | Every repository |
| Automatically delete head branches | On | General, Pull Requests | Where merges are merge commits. Under squash or rebase-merge, only where nothing cites a branch's commits |
| Release immutability | On | General, Releases | Where releases are published |
| Wiki, Projects, Discussions | Off, unless something uses them | General, Features | Every repository |
| Default-branch ruleset | Deletion and force pushes blocked. A pull request required, with no approval for one maintainer and at least one for several. The CI checks required | Rules, Rulesets | Public, or private on a paid plan |
| Release-tag ruleset | `v*` tags can't be updated, deleted or force-pushed | Rules, Rulesets | Where releases are tagged: public, or private on a paid plan |
| Workflow permissions | Read repository contents and packages permissions, with Allow GitHub Actions to create and approve pull requests unticked | Actions, General | Every repository with workflows. A new one in a personal account starts this way |
| SHA-pinned actions | Require actions to be pinned to a full-length commit SHA, once every action, and every action those call, is pinned | Actions, General, Actions permissions | Every repository with workflows |
| Fork pull requests | Require approval for all external contributors | Actions, General, Approval for running fork pull request workflows from contributors | Public |
| Secret scanning and push protection | On | Advanced Security | Public. On private, a paid add-on |
| Dependabot | Alerts on. Security updates on, and grouped, where someone merges their pull requests. Dependabot on self-hosted runners off, unless a runner labelled for it exists: without one, its jobs wait, and fail after 24 hours | Advanced Security | Every repository |
| Code scanning | CodeQL's default setup | Advanced Security, CodeQL analysis, Set up, Default | Public. On private, an organisation's repository with GitHub Code Security |
| Private vulnerability reporting | On, with `SECURITY.md` pointing to it | Advanced Security | Public. On a fork that only sends changes upstream, off, so reports reach the upstream project |

Secret scanning's validity checks and generic patterns exist only for an organisation's
repositories on GitHub Team with Secret Protection, so don't list them as missing anywhere else.

The person's account has settings of its own, which go in the same list as one action, once.
A session can read few of them. Ask for a screenshot of the account's Code security page, and
whether the two email boxes below are ticked: a screenshot of the Emails page would show the
addresses themselves. Each setting is in the account's Settings, under the profile picture:

| Account setting | Set it to | Where |
|---|---|---|
| Private vulnerability reporting, dependency graph, Dependabot alerts, Dependabot security updates, grouped security updates | On for new repositories. For existing ones, Enable all for the dependency graph and Dependabot alerts, and the repository table decides the others | Code security |
| Dependabot on self-hosted runners | Off, unless the account has a runner labelled for it, as in the repository table | Code security |
| Push protection for yourself | On | Code security |
| Keep my email addresses private | On, so merges and edits made on GitHub carry the noreply address | Emails |
| Block command line pushes that expose my email | On, once every clone commits with the noreply address, set in `git config user.email` | Emails |
| Two-factor authentication | On | Password and authentication |
| Default branch name | `main` | Repositories |
| The Claude GitHub App's repository access | Includes this repository, or no session can reach it | Applications, Installed GitHub Apps, Configure |
| The plan | The person's choice. On GitHub Free, a private repository can have no ruleset or branch protection, and GitHub Pro adds both. A personal account's private repositories get no secret scanning or code scanning on either | Billing and licensing |
