# Authoring a skill

Every new or rebuilt skill, and every new module, passes this review, one per change. Record the
outcome in `docs/decisions.md`: the skill or module, what it was built from, the sources it
rests on, and anything reused under another license. How skills and modules divide is in the
roadmap's [*How skills are structured*](../ROADMAP.md#how-skills-are-structured).

The owner's old claude.ai skills are a list of topics, checks and lessons. Nothing is copied from
them.

**Start from the skeleton:** `uv run skillcheck --new <skill>` writes a skill's `SKILL.md` with
an empty router, and `uv run skillcheck --new-module <module> <skill>` adds a module: its file,
its row in the router and its trigger evaluations, in the shape below. Each part still to be
written is marked `TODO(new-skill)`, and `skillcheck` fails a skill that still holds one, so a
half-written skill can't ship. `uv run skillcheck --move <module> <skill>` gives a module a new
home, and records it in [docs/module-moves.md](module-moves.md).

**The standard covers configuration and process; these skills cover code.** The standard says it
doesn't judge code, and the category skills are what does. Where the standard already rules,
cite its section instead of restating it. That applies to budgets, layouts, versioning, secrets
and dependencies. A second version of a published rule drifts from the first.

1. **Whose work it is.** Everything here is public. Work written on an employer's account or time
   needs the owner's recorded permission to publish (the gate answers, part A). Without it, the
   skill stays out.
2. **Sources.** Every fact comes from a primary source: official documentation, a standard, or
   the project's own release notes. Each one carries its URL and the date it was checked. Put
   facts that can go stale (versions, support dates, defaults, and what other projects do) in
   each module's Facts section, or in `references/facts.md` in a skill not yet made of modules,
   in tables with the columns ID, Fact, Source, Quote, Checked and Check by:
   - the source is an https link, or the `git ls-remote --tags <https URL>` command that shows
     the fact;
   - the quote is the source's own words in double quotes, or a command's output in backticks.
     A row with neither is checked by hand when it falls due;
   - other text names a fact by its ID, such as fact `node20`, rather than repeating it. An ID
     is defined once in the repository, and any file in any skill may name it, so a module
     that moves keeps every fact it names.

   `skillcheck` checks every row's shape and every fact a skill names. `skillcheck --due` lists
   the facts due to be checked again, and `skillcheck --verify` fetches each source and looks
   for its quote. The freshness workflow runs both each week, and keeps one issue open while
   anything is due. Research results are leads until each claim is checked against its source.
3. **Licenses.** Quote, paraphrase or adapt a source only as its license allows. The licenses of
   common sources are in `research/runs/2026-09-23-A-source-licences.md`. Broadly:
   - **Adaptable with a notice:** CC0, MIT, Apache-2.0, BSD, CC BY, OGL and PSF sources. Examples
     are the GitHub gitignore templates, the Agent Skills spec, Microsoft's PowerShell docs, the
     Python docs, Google's style guides, SemVer and Keep a Changelog.
   - **Share-alike** (OWASP, MDN prose, the Arch Wiki): quote briefly with attribution, and
     write everything else in our own words. An adaptation would carry their license.
   - **Restricted** (Epicor's help, SOLIDWORKS API samples, Anthropic's documentation): state
     facts in our own words and link to the source. Copy nothing beyond a short quote.
   - Material under another license comes in with its notice: name the license in the `license`
     field and keep a `THIRD-PARTY-NOTICES.md` in the skill's directory.
   - Anthropic's Apache-2.0 skills may be adapted, keeping their notice and marking the changes.
   - Nothing from Anthropic's source-available document skills (docx, pdf, pptx, xlsx).
4. **No secrets and no company detail.** Use placeholders:
   - `example.com` and its subdomains (RFC 2606) for hosts;
   - `192.0.2.0/24`, `198.51.100.0/24` and `203.0.113.0/24` (RFC 5737) for addresses;
   - `CHANGEME` for secrets. Never use a realistic fake, because secret scanners can't tell one
     from a real key.

   Company-specific versions of a skill live in that company's repositories, under
   `.claude/skills/`.
5. **Fits Claude Code.** Commands run on the user's machine. That means:
   - no `/mnt/user-data` or `/mnt/skills` paths, and no upload or artifact steps;
   - a destructive command is shown with a dry run or a confirmation first;
   - never fetch-and-run (`curl … | sh`).

   Claude Code comes first, and a skill works on claude.ai too, even where that takes some
   extra effort (the owner, 2026-10-15). That means spec fields only, which `skillcheck`
   enforces, a description that stands on its own, and steps that say what to do where no
   shell is available. Where a skill can't serve claude.ai at a fair cost, say so in its
   `compatibility` field. Skills load the same way on both: each description is always in the
   system prompt, and a skill's files are read with bash when it's triggered. For claude.ai:
   - say "read `references/<module>.md`", never "use the Read tool": Claude Code's own tools
     don't exist there;
   - the core guidance needs no network, which claude.ai may not allow, depending on the
     user's and the admin's settings;
   - custom skills there need code execution turned on, on Pro, Max, Team and Enterprise.

   Before it ships, the owner tries requests on claude.ai, each in a new chat, from a list the
   session gives them: for each changed module, a request worded as a person would ask, the
   skill and module it should reach, and what a pass looks like, plus one near miss it
   shouldn't take. `uv run skillcheck --tries <module>` writes the list from the module's
   trigger tests, and the results are recorded in `docs/decisions.md`. claude.ai can't be driven by a program, and the owner chose
   these tries over an API run that would cost money (2026-10-16).
6. **Frontmatter.** Spec fields only, and the name matches the directory. The description says
   when to load the skill and what it does, in the third person, its main use first, with
   distinctive trigger words rather than a keyword list, in 250 characters or fewer. It names
   the situations its modules cover, so a request for any of them loads it. Claude Code lists
   every skill's name and description within a budget, and past it the skills used least keep
   only their names, so the name says what the skill is for. `skillcheck` enforces the cap, and
   holds the whole listing to room for 20 skills: coverage grows by modules.
7. **Shape.** A skill is a router and its modules.
   - **`SKILL.md`,** under 500 lines: the situations it loads for, what applies to every module,
     and a section headed `Modules` with a table, `Module | Read it for`, one row per module,
     each starting with a link to `references/<module>.md`. It ends with the section every
     skill shares, `When something here is wrong`, which tells the model to say in a sentence
     whether a problem a person raises is the skill's fault, and to draft a full report when it
     is. The text lives once, in `src/skillcheck/core/reporting.py`; `--new` writes it.
   - **A module,** `references/<module>.md`, stands alone, and holds every part of its story
     under these headings, so it can move to another skill whole: `Rules`, `Mistakes`, `Audit`
     (each check, what to look for, its severity in the standard's status words, and the fix),
     `Why` (for each rule that matters, the advice, the reason, what other projects do and why,
     what each choice costs, and when to choose differently), `Facts` and `Sources` (each
     source with its license). It opens with one line on when to read it, and a table of
     contents once it passes 300 lines.
   - **One level deep:** a module never sends the reader on to another file, by link or by
     naming it. It names another module in words, by its name. Naming a fact by its ID is the
     one exception, because a fact is looked up, not read on to.
   - **One home:** a module's name is unique across the repository and never changes, and a
     skill made of modules holds no other Markdown in `references/`. Its `ROADMAP.md` row names
     its skill.

   `skillcheck` checks every part of this. Every skill is made of modules except the
   standard's, which keeps the standard in one versioned file.
8. **Every link resolves and every example works.** Each code example compiles, lints or runs
   under its language's own tools: `uv run skillcheck --examples`, which CI runs. A block that's
   wrong on purpose takes `<!-- example: unchecked, <reason> -->` on the line before it.
9. **Trigger evaluations.** Each module has `tests/fixtures/modules/<module>.json`, with requests
   that should reach it and near misses that belong to another module or skill. `skillcheck`
   requires both kinds. `uv run skillcheck --triggers <module>` asks Claude Code each one and
   names each that missed; each is a model call, so it runs by hand. These requests decide the
   boundaries: a module spins off into a skill
   of its own, two skills merge, or a module moves, by the rules in the roadmap.
10. **Catalog, roadmap, README.** List the skill in exactly one plugin entry. Set its
    `ROADMAP.md` row, and each built module's row, to `shipped`, and add the skill to the
    README's skill table. Then run
    `uv run skillcheck .` and `npx --no-install claude plugin validate --strict .`.
11. **Record it.** Add a line under `[Unreleased]` in `CHANGELOG.md` and set `metadata.reviewed`
    to today's date.
12. **The old copy.** A rebuilt skill keeps its old skill's name where the old name still fits
    its scope. Before the release that ships it, the session names the old copy on the owner's
    claude.ai account, and every skill there that depends on it, found by searching the synced
    copies under `~/.claude/skills/synced/` for its name, saying for each whether it would
    break or only names the old one. The owner deletes the old copy and decides which of those
    to delete too, since the owner's own settings delete an uploaded skill but can't turn it off
    (the owner, 2026-10-16). The owner deletes it in the organization library's inventory as
    well, since deleting their own copy left the library's installed for everyone, and
    colleagues get the successor from this repository's plugins. The release waits for their
    word. Otherwise the old copy loads
    beside the new one under a prefix, in chat and in cloud sessions.
