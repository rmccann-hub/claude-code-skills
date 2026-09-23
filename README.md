# claude-code-skills

The reference for setting up, auditing and keeping repositories current with Claude Code:
installable skills, the checks behind them, and the research they rest on.

## Install

In Claude Code:

```
/plugin marketplace add rmccann-hub/claude-code-skills
/plugin install standards@rmccann-skills
```

## Skills

| Skill | Plugin | What it does |
|---|---|---|
| `project-bootstrap-and-audit` | `standards` | Sets up a new repository, or audits an existing one, against the PROJECT-BOOTSTRAP-AND-AUDIT standard (v0.36.0) |

More arrive one at a time, each through the review in
[docs/authoring-a-skill.md](docs/authoring-a-skill.md). [ROADMAP.md](ROADMAP.md) lists every skill
that is planned, with its status.

## Development

You need [uv](https://docs.astral.sh/uv/) 0.12 or later, which installs the Python version named
in `.python-version`. You also need Node.js, to run Claude Code's own catalog validator.

```
uv sync --locked
uv run pytest
uv run ruff check
uv run ruff format --check
uv run skillcheck .
npm ci
npx --no-install claude plugin validate --strict .
```

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
2. **Merge it, then tag the release** from the Releases page. Aim the tag at the merge commit,
   not at the branch.
3. **Reach the copies already installed.**
   - **claude.ai:** delete or replace the uploaded skill under Customize, then Skills. If an
     admin uploaded it for an organization, an admin removes it.
   - **Plugin installs:** a third-party marketplace updates automatically only if the user
     turned that on. Ask users to run these in a terminal:

     ```
     claude plugin marketplace update rmccann-skills
     claude plugin update <plugin>@rmccann-skills
     ```

     If the plugin itself was removed, ask them to run
     `claude plugin uninstall <plugin>@rmccann-skills` instead.
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
