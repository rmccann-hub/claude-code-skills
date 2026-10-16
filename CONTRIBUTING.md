# Contributing

This repository is public, and anyone may use, test or improve it. It's maintained by its owner,
[@rmccann-hub](https://github.com/rmccann-hub), who reviews and merges every change, decides
what's planned, and cuts the releases. This file says what the skills can and can't do, how to
try them, how to report a problem, and how to send a change.

## What's here

- **Skills** for Claude Code and claude.ai, shipped as two plugins. A skill is a set of
  instructions Claude loads when a request matches what it's for:
  - `project-bootstrap-and-audit` (plugin `standards`) sets up a new repository, or audits an
    existing one, against the PROJECT-BOOTSTRAP-AND-AUDIT standard;
  - `git-workflows` (plugin `engineering`) covers commits, branches, pull requests, GitHub
    Actions, hooks, leaked secrets, `.gitignore` and releases;
  - `house-style` (plugin `engineering`) is one style for prose and Markdown, with a Vale
    check.
- **`skillcheck`**, the Python tool that checks the skills, the catalog and the records.
- **Research:** the prompts, and the dated results the skills' facts come from.
- **The plan,** in [ROADMAP.md](ROADMAP.md): every skill and module, shipped or planned.

## What the skills can do

- **Set up or audit a repository.** The standard's skill reads the repository, asks only what it
  can't find out, and stops twice for answers before it changes anything. It lists the GitHub
  settings to change, and where each one is.
- **Guide Git, GitHub and writing work,** with each rule's reason, what other projects do
  instead, and what each choice costs, so you can decide whether a rule fits.
- **Name their sources.** Every version, date and default carries its source, a quote, the
  date it was checked and a date to check it again by. A weekly job looks for each quote at its
  source again.
- **Check themselves.** CI runs the tests, `skillcheck`, the prose check, a secret scan and
  Claude Code's own validator on every pull request.

## What they can't do

- **They don't replace review.** A skill guides an agent, and the agent can still be wrong. Read
  what it proposes before you accept it.
- **They don't change settings for you.** The standard's skill lists GitHub settings to change;
  you change them.
- **They assume GitHub and GitHub Actions.** Other forges have the same ideas under other names,
  which the skills don't spell out.
- **Most planned skills don't exist yet.** Coding, testing, security, operations and the rest are
  in [ROADMAP.md](ROADMAP.md) as `planned`. Until they ship, Claude answers those requests
  without them.
- **On claude.ai they can't run commands.** A skill gives you the commands to run instead. Custom
  skills there need code execution turned on in the account's settings.
- **They hold nothing company-specific.** A company's names, hosts and templates belong in that
  company's own repositories.

## Use it

The three shipped skills are ready for real work. Use them the way you'd work anyway, and
report what goes wrong.

1. Install the plugins, as the README's [Install](README.md#install) section says, in Claude
   Code, on claude.ai, or both.
2. Use them on your own repositories and writing. Some requests that load them:
   - "Set up this repository" or "audit this repository", which load the standard's skill;
   - "write the commit message", "why is my required check stuck", "cut the 1.2.0 release" or
     "I pushed a secret", which load `git-workflows`;
   - "tidy this README", or "add a prose check to CI", which load `house-style`.
3. To test one area on purpose, use the sample requests in
   [tests/fixtures/skills/](tests/fixtures/skills/) and
   [tests/fixtures/modules/](tests/fixtures/modules/). Each request says whether it should reach
   that skill or module (`"should_trigger": true`), or is a near miss that belongs elsewhere.

## Report a problem

The quickest way is to tell Claude, in the same chat, that something it said is wrong or
didn't work. Every skill tells it to answer your problem first, then to say in one sentence
whether the fault looks like the skill's, and why. When it is the skill's, Claude drafts a full
report for you to paste as an issue here. Check the draft before you post it.

To write one yourself, open an issue on this repository. Say:

- what you asked, word for word;
- where: Claude Code or claude.ai, and the plugin's version (`/plugin` in Claude Code lists it);
- what loaded and what it said;
- what you expected instead, and why, with a source where a fact is wrong. A fact's ID, such as
  `node20`, is in the module that holds it.

A security problem goes through the Security tab instead, as [SECURITY.md](SECURITY.md) says.
Please don't open a public issue for one.

## Send a change

### Set up

1. Fork the repository, and clone your fork.
2. Install what the README's [Development](README.md#development) section lists, and run its
   commands once, to see them pass before you change anything.
3. Make a branch named `<kind>/<topic>`, such as `fix/gitignore-example`.

### Make the change

- **Know where it goes.** [AGENTS.md](AGENTS.md) says where each kind of content belongs. New
  coverage is a module of an existing skill. Only a new kind of situation gets a new skill.
  `uv run skillcheck --new-module <module> <skill>` writes a module's starting files, marked
  where they still need writing.
- **Follow the review.** Every new or rebuilt skill or module passes the review in
  [docs/authoring-a-skill.md](docs/authoring-a-skill.md).
- **Propose a change to the standard first.** Open an issue for any change to
  `skills/project-bootstrap-and-audit/references/`. It's applied on its own, once the owner
  approves it.

### What CI checks

| Rule | How to check it yourself |
|---|---|
| Commit subjects read "area: summary", such as `git-workflows: fix the hook example` | Read `git log --oneline` |
| Prose follows the house style | `vale sync`, then `git ls-files -z '*.md' \| xargs -0 vale` |
| Skills, modules, the catalog, the roadmap and every fact row agree | `uv run skillcheck .` |
| The tests pass, at 100% coverage, and none went missing | `uv run pytest` |
| Code is linted and formatted | `uv run ruff check`, `uv run ruff format --check` |
| The dependency map is current | `uv run skillcheck --bom`, then commit what it changed |
| The catalog is valid for Claude Code | `npx --no-install claude plugin validate --strict .` |

### What nothing checks, so please keep to it

- **This repository is public.** Commit nothing owned by an employer, and no company's internal
  names, hosts or templates. Don't name a private repository you tried a skill on.
- **Other people's material comes in only under its license,** named in the skill and recorded
  in `docs/decisions.md`. Nothing comes from Anthropic's source-available document skills.
- **A fact that can go stale carries its source and the date you checked it.** Don't write a
  version or a date from memory.
- **The plan lives only in `ROADMAP.md`.** No progress or handoff files.
- **A new Markdown file says, in its commit message, which existing files you considered for
  it,** and why none fit.

### Open the pull request

Open it against `main` from your fork. Say what changes and why, how you tested it with the
commands and what they showed, and what you left out. GitHub asks the owner to approve the
first workflow runs from a fork, so CI may wait for that. The owner reviews it and merges it
with a merge commit, the only method allowed, so your commits keep their IDs.

## Working with Claude Code

`AGENTS.md`, through `CLAUDE.md`, loads in every Claude Code session in this repository, so a
session follows the same rules you do. Ask it to run the checks above before it pushes, and read
its diff before you open the pull request. `.claude/settings.json` turns off the plugins' copies
of this repository's own skills, so a session works on the files here, not on an installed copy.

## License

Contributions are under the repository's license, as section 5 of [LICENSE](LICENSE) says:
Apache-2.0, or CC0-1.0 for the standard's own file.
