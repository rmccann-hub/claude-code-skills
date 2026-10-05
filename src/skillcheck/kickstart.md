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
| Workflow permissions | Read repository contents and packages permissions, with Allow GitHub Actions to create and approve pull requests unticked | Actions, General | Every repository with workflows |
| SHA-pinned actions | Require actions to be pinned to a full-length commit SHA, once every action, and every action those call, is pinned | Actions, General, Actions permissions | Every repository with workflows |
| Fork pull requests | Require approval for all external contributors | Actions, General, Approval for running fork pull request workflows from contributors | Public |
| Secret scanning and push protection | On | Advanced Security | Public. On private, a paid add-on |
| Dependabot | Alerts on. Security updates on where someone merges their pull requests | Advanced Security | Every repository |
| Code scanning | CodeQL's default setup | Advanced Security, CodeQL analysis, Set up, Default | Public. On private, an organisation's repository with GitHub Code Security |
| Private vulnerability reporting | On, with `SECURITY.md` pointing to it | Advanced Security | Public |

Secret scanning's validity checks and generic patterns exist only for an organisation's
repositories on GitHub Team with Secret Protection, so don't list them as missing anywhere else.

Four more settings belong to the person's account, not the repository, and go in the same list
as one action, once. In the account's Settings: Code security, with Enable all and on for new
repositories; Push protection for yourself, on; Repositories, with the default branch name
`main`; and Applications, Installed GitHub Apps, then Configure beside the Claude app, whose
repository access must include this repository for a session to reach it.
