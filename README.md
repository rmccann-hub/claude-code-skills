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
| `project-bootstrap-and-audit` | `standards` | Sets up a new repository, or audits an existing one, against the PROJECT-BOOTSTRAP-AND-AUDIT standard (v0.35.0) |

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

## Security

See [SECURITY.md](SECURITY.md).

## License

Apache-2.0; see [LICENSE](LICENSE). The standard keeps its own CC0-1.0 dedication, stated in its
file.
