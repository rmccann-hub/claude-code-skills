# Authoring a skill

Every new or rebuilt skill passes this review, one skill per change. Record the outcome in
`docs/decisions.md`: the skill, what it was built from, the sources it rests on, and anything
reused under another licence.

The owner's old claude.ai skills are a list of topics, checks and lessons. Nothing is copied from
them.

**The standard covers configuration and process; these skills cover code.** The standard says it
doesn't judge code, and the category skills are what does. Where the standard already rules,
cite its section instead of restating it. That applies to budgets, layouts, versioning, secrets
and dependencies. A second version of a published rule drifts from the first.

1. **Whose work it is.** Everything here is public. Work written on an employer's account or time
   needs the owner's recorded permission to publish (the gate answers, part A). Without it, the
   skill stays out.
2. **Sources.** Every fact comes from a primary source: official documentation, a standard, or
   the project's own release notes. Each one carries its URL and the date it was checked. Put
   facts that can go stale (versions, support dates, defaults) in `references/facts.md`, each
   with a check-by date. Research results are leads until each claim is checked against its
   source.
3. **Licences.** Quote, paraphrase or adapt a source only as its licence allows. The licences of
   common sources are in `research/runs/2026-09-23-A-source-licences.md`. Broadly:
   - **Adaptable with a notice:** CC0, MIT, Apache-2.0, BSD, CC BY, OGL and PSF sources. Examples
     are the GitHub gitignore templates, the Agent Skills spec, Microsoft's PowerShell docs, the
     Python docs, Google's style guides, SemVer and Keep a Changelog.
   - **Share-alike** (OWASP, MDN prose, the Arch Wiki): quote briefly with attribution, and
     write everything else in our own words. An adaptation would carry their licence.
   - **Restricted** (Epicor's help, SOLIDWORKS API samples, Anthropic's documentation): state
     facts in our own words and link to the source. Copy nothing beyond a short quote.
   - Material under another licence comes in with its notice: name the licence in the `license`
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

   Under decision H2 (a), the skill must also work on claude.ai.
6. **Frontmatter.** Spec fields only, and the name matches the directory. The description says
   what the skill does and when to use it, in the third person, with distinctive trigger words
   rather than a keyword list, in 1,024 characters or fewer.
7. **Shape.** `SKILL.md` is a router under 500 lines: scope, the rules that matter most, how to
   check, how to audit, and where to go next. Detail goes in `references/`, one level deep: a
   reference never sends the reader on to another reference. Each reference stands alone:
   - a title that says what it is, and one line on when to read it;
   - a table of contents once it passes 300 lines;
   - a checked date if it holds facts.

   A category skill uses these references, keeping only the ones it needs:

   | File | Holds |
   |---|---|
   | `facts.md` | Versions, support dates and defaults, each with its source, quote, checked date and check-by date |
   | `setup.md` | Starting a project: structure, config files, toolchain commands |
   | `style.md` | Naming, formatting, comments and docstrings, types |
   | `security.md` | The threats in this area, and the safe pattern for each |
   | `testing.md` | Frameworks, patterns, commands |
   | `audit.md` | Every check: what to look for, its severity (the standard's status words), and the fix |
   | `mistakes.md` | Common mistakes, including those AI assistants make |
   | `modernization.md` | Moving off older versions and idioms |
   | `sources.md` | Every source, with its licence |
8. **Every link resolves and every example works.** Each code example compiles, lints or runs
   under its language's own tools.
9. **Trigger evaluations.** Write `tests/fixtures/skills/<name>.json` with requests that should
   and should not activate the skill. Include near misses that belong to a neighbouring skill.
10. **Catalog, roadmap, README.** List the skill in exactly one plugin entry. Set its
    `ROADMAP.md` row to `shipped`, and add it to the README's skill table. Then run
    `uv run skillcheck .` and `npx --no-install claude plugin validate --strict .`.
11. **Record it.** Add a line under `[Unreleased]` in `CHANGELOG.md` and set `metadata.reviewed`
    to today's date.
12. **The old copy.** Once the new version is delivered, turn off or replace the claude.ai copy,
    so sessions don't load two versions of one skill.
