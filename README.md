# claude-code-skills

The owner's master reference for Claude Code, for Claude skills, and for coding practice in
general: installable skills for setting up, auditing and keeping repositories current, the
checks behind them, and the research they rest on.

## Install

In Claude Code:

```text
/plugin marketplace add rmccann-hub/claude-code-skills
/plugin install standards@claude-code-skills
/plugin install engineering@claude-code-skills
```

Before 0.1.1 the marketplace was called `rmccann-skills`. If you added it under that name,
run `/plugin marketplace remove rmccann-skills`, then add it again as above.

## Start another repository

Attach the latest release's
[`KICKSTART.md`](https://github.com/rmccann-hub/claude-code-skills/releases/latest/download/KICKSTART.md)
to a Claude Code session in that repository, with no message. It reads the repository, asks
only what it can't find out, and stops twice for answers before it changes anything. It also
reads the repository's GitHub settings, and lists each one to change with where it is. The
same release's `ruleset-default-branch.json` and `ruleset-release-tags.json` import under
Settings, Rules, Rulesets, from the New ruleset menu.

## Skills

| Skill | Plugin | What it does |
|---|---|---|
| `project-bootstrap-and-audit` | `standards` | Sets up a new repository, or audits an existing one, against the PROJECT-BOOTSTRAP-AND-AUDIT standard (v0.40.0) |
| `git-workflows` | `engineering` | Commit messages, pull requests, the merge strategy, branch deletion, GitHub Actions CI, hooks, `.gitignore`, release tags, changelogs and backports, with the reasons for each and what other projects do |

More arrive one at a time, each through the review in
[docs/authoring-a-skill.md](docs/authoring-a-skill.md). [ROADMAP.md](ROADMAP.md) lists every skill
that is planned, with its status.

## Development

You need [uv](https://docs.astral.sh/uv/) 0.12 or later, which installs the Python version named
in `.python-version`. You also need Node.js, to run Claude Code's own catalog validator.

```sh
uv sync --locked
uv run pytest
uv run ruff check
uv run ruff format --check
uv run skillcheck .
npm ci
npx --no-install claude plugin validate --strict .
```

Each skill's dated facts carry their source and a date to check them again by.
`uv run skillcheck --due` lists the facts that are due, and `uv run skillcheck --verify` looks
for each quote at its source, over the network. The Freshness workflow runs both every Monday,
with the dependency map's check below, and keeps one issue open while anything is due.

[docs/dependencies.md](docs/dependencies.md) maps what the repository is built from, runs on
and relies on: its languages, runtimes, tools, packages at their exact versions, GitHub Actions,
services, and the sources its facts cite. [bom.json](bom.json) holds the same map in CycloneDX
1.7, for other tools to read. `uv run skillcheck --bom` writes both, and
`uv run skillcheck --bom-check` names one that no longer matches. Pull requests don't run that
check, because a Dependabot update can't rebuild the map. The Freshness and Release workflows
run it.

Parity runs check how the skill behaves on sample repositories, before and after a change.
[docs/testing-the-skill.md](docs/testing-the-skill.md) says how to run one.

## Releasing

1. In the pull request, set the new version in every catalog entry, and add its section to
   `CHANGELOG.md`.
2. Once it merges and CI passes on `main`, run the Release workflow from the Actions tab, with
   the version and the merge commit's full SHA.
3. Then a session re-checks this repository against the standard, with the new release's
   kickstart file, and sends the owner its report. What it raises waits for the owner's
   answers, as in any other run, and the release doesn't wait for it.

## Operations: withdrawing a bad skill

If a skill here gives wrong or harmful instructions, take it out of circulation in this order.

1. **Stop new installs.** In one pull request, fix the skill or remove it.
   - To remove it:
     - delete `skills/<name>/`;
     - remove its path from `.claude-plugin/marketplace.json`. If it was its plugin's only
       skill, remove the whole plugin entry, because an entry whose paths all miss loads every
       skill;
     - remove its row from the skill table above;
     - set its status in `ROADMAP.md` to `building`.
   - Either way:
     - bump `version` in every catalog entry, because installed copies update only when the
       version changes. A fix is a patch release. A removal is a breaking change, and under
       0.x a breaking change is a minor release;
     - add a changelog entry under Fixed, Removed or Security.

   `skillcheck` fails the pull request if the catalog, the roadmap, the README and `skills/`
   disagree.
2. **Merge it, then release it.** Run the Release workflow from the Actions tab, with the new
   version and the merge commit's full SHA, not a branch, before a later commit changes a
   workflow. It checks the version, the changelog and CI, and makes the annotated tag. Then it
   publishes the release page, with the kickstart file, each skill packaged for claude.ai, the
   ruleset files and the dependency map attached.
3. **Reach the copies already installed.**
   - **claude.ai:** delete or replace the uploaded skill under Customize, then Skills. If an
     admin uploaded it for an organization, an admin removes it.
   - **Plugin installs:** a third-party marketplace updates automatically only if the user
     turned that on. Ask users to run these in a terminal:

     ```sh
     claude plugin marketplace update claude-code-skills
     claude plugin update <plugin>@claude-code-skills
     ```

     If the plugin itself was removed, ask them to run
     `claude plugin uninstall <plugin>@claude-code-skills` instead.
   - **Committed copies:** each repository with a copy in `.claude/skills/` removes or replaces
     it.
4. **If it was a security problem,** publish a security advisory from the Security tab, naming
   the affected versions. Rotate anything the skill could have exposed.
5. **Record what happened** in `docs/decisions.md`.

## Security

See [SECURITY.md](SECURITY.md).

## License

Apache-2.0; see [LICENSE](LICENSE). The standard keeps its own CC0-1.0 dedication, stated in its
file.
