# RESEARCH RUN R10: TypeScript, JavaScript, Node.js, HTML, CSS and the web front end

For the repository rmccann-hub/claude-code-skills · Prompt version 2 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: typescript-javascript, html-css, accessibility (web), visual-theme (CSS).

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R10 · FORM: research-result v1
Save as: R10-RESULT.md
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

- (the standard, 2026-09) Node 22 and 24 are both LTS. Biome 2.x suits a new project; ESLint plus Prettier fits where plugins already exist. Vitest suits new tests.
- Node.js 24 became Active LTS in October 2025; Node 22 is in maintenance until April 2027; Node 20 reached end of life in April 2026; Node 26 was released in April 2026 and becomes LTS in October 2026. Node.js has announced changes to its release schedule.
- TypeScript 6.0 was released as a bridge to TypeScript 7.0, the native compiler written in Go; 7.0's status today is to be confirmed.
- ECMAScript 2025 added iterator helpers, Set methods, import attributes and JSON modules, RegExp.escape, Float16Array and Promise.try. Temporal is shipping in browsers during 2025-2026.
- ESLint 9 made flat config the default and ESLint 10 removed eslintrc; Biome 2 and oxlint 1.0 are production-ready alternatives.
- Vite 7 was released in 2025, and Vite is moving to the Rolldown bundler.
- React 19 is current (19.2 in October 2025), React Compiler 1.0 was released in October 2025, and a critical React Server Components vulnerability (CVE-2025-55182) was disclosed in December 2025.
- Tailwind CSS v4 uses CSS-first configuration.
- The Sanitizer API (setHTML) and Trusted Types are shipping in browsers.
- The npm registry suffered worm-style supply-chain attacks in September and November 2025.

## Questions

### Priority

1. Runtimes: the Node.js release schedule and support dates today (confirm the list above and any schedule change), the status of Deno 2.x and Bun 1.x, which to target for new work, and the status of ESM versus CommonJS (is `require(esm)` stable?).
2. TypeScript: the current version, 6.0's deprecations, the status of 7.0 (the native compiler) and migrating to it, a recommended tsconfig for new projects (strict flags, `module: nodenext` or `preserve`, `verbatimModuleSyntax`, `erasableSyntaxOnly`), and the status of Node's built-in type stripping.
3. The JavaScript language: which ES2025 and ES2026 features change how code should be written (confirm the list), Temporal's status per browser and in Node, and the status of explicit resource management (`using`).
4. Tooling:
   - linters and formatters: ESLint (current major, flat config, typescript-eslint), Biome, oxlint, Prettier
   - package managers (npm 11, pnpm 10, Yarn 4) and their supply-chain settings: ignore-scripts, minimum release age, trusted publishing, provenance
   - bundlers: Vite, Rolldown, esbuild, Rspack, Turbopack
   - test runners: Vitest, Jest, node:test, Playwright
5. npm supply-chain incidents of 2025-2026, and the defences recommended for a project today.

### Standard

6. Frameworks, with current versions and the security advisories to know: React 19.x, React Compiler, Server Components and the December 2025 vulnerability, Next.js (current major), Angular, Vue 3.x (Vapor mode status), Svelte 5, Astro.
7. HTML: features that are now Baseline (dialog, popover, invoker commands, customizable select, the details name attribute, inert, `hidden=until-found`), deprecated patterns, and notable 2025-2026 additions to the WHATWG living standard.
8. CSS: Baseline status of nesting, :has(), container queries, @layer, @scope, anchor positioning, view transitions, `light-dark()` and `text-wrap`; Tailwind v4; methodology (utility-first, BEM, CSS modules).
9. Web security: CSP Level 3 (strict CSP with nonces or hashes), Trusted Types, the Sanitizer API's status, SRI, COOP and COEP, cookies (SameSite defaults, CHIPS, the status of third-party cookies in Chrome), Permissions-Policy.
10. Legacy web: jQuery 4.0's status, migration paths off AngularJS (end of life), CommonJS-to-ESM migration, and Internet Explorer-era patterns to remove.
