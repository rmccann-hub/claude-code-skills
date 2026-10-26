# Verification: R10 (2026-10-26)

Checked by the receiving session on 2026-10-26. Only the claims this intake relies on were
checked: those behind proposed corrections to the standard. The rest is checked when
`javascript-coding` and `html-coding` are built.

| Claim | Status | Checked against |
|---|---|---|
| Node 26 becomes LTS on 2026-10-28; Node 22 ends 2027-04-30; Node 20 ended 2026-04-30 | verified; **the standard's "Node 22 and 24 both LTS" is out of date on 2026-10-28**. Node 24 entered maintenance on 2026-10-20, not 28 October as the report's secondary source has it | [nodejs/Release schedule](https://raw.githubusercontent.com/nodejs/Release/main/schedule.json) |
| The Tools table's Bun install command | **a fetch-and-run command**, quoted from Bun's site; this repository's skills never give one (`docs/authoring-a-skill.md`, step 5) | — |
| The report says it was written by an Anthropic model, and that Bun is Anthropic's | noted; its Bun facts are leads like the rest | — |
| Everything else in the report | not yet checked | checked when the modules that rely on it are built (`research/README.md`) |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R10 · FORM: research-result v1
Save as: R10-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R10 result: TypeScript, JavaScript, Node.js, HTML, CSS and the web front end (as of 26 October 2026)

## 1. Summary

The standard's runtime and toolchain facts are already stale: from 28 October 2026\[1\] the default Node.js target for new work is Node 26 LTS, TypeScript 7.0 (the Go-native compiler) has been stable since 8 July 2026, Vite 8 already runs on Rolldown, ESLint 10 has removed eslintrc, and Deno's runtime is being wound down after its team joined Cloudflare.

**TL;DR**

- Target Node 26 (Active LTS from 28 October 2026) for new work; Node 22 leaves support in April 2027 and Node moves to one release a year, every release LTS, starting with Node 27 (alpha from October 2026, stable April 2027).
- Use TypeScript 7.0 for `tsc` but keep TypeScript 6 side-by-side (via `@typescript/typescript6`) for tools that need the compiler API, such as typescript-eslint, until 7.1 ships its new API; clear every TypeScript 6.0 deprecation first, because 7.0 removes them.
- Turn on a minimum release age (npm 11.10+ `min-release-age`, pnpm 11's default of 1 day), block install scripts, and publish with trusted publishing; the 2025–2026 npm worms (Shai-Hulud, Shai-Hulud 2.0, "Mini Shai-Hulud") show that provenance alone does not prove a package is safe.

Further points a professional must know today:

- Deno: the runtime gets monthly 2.9.x LTS releases until about October 2027,\[2\] then Deno's own development ends; Deno Deploy shuts about six months after 9 October 2026.\[3\] Do not start new long-lived work on Deno.
- Bun 1.4.x (October 2026) is the first Bun written in Rust;\[4\]\[5\] Bun is owned by Anthropic since 2 December 2025.\[6\]
- Node's built-in type stripping is stable (v25.2.0 / v24.12.0) and runs only erasable TypeScript; Node 26 removed `--experimental-transform-types`.\[7\] `require(esm)` is no longer experimental (v25.4.0).\[8\]
- Temporal reached TC39 Stage 4 on 11 March 2026 and ships in Firefox 139+ and Chrome/Edge 144+, and is enabled by default in Node 26; Safari has it only in Technology Preview.\[9\] Whether it belongs to ES2026 or ES2027 is contested.\[10\]\[11\]
- ESLint 10.0.0 (February 2026) removed eslintrc entirely; ESLint 9 reached end of life on 6 August 2026; latest is v10.13.0 (16 October 2026).\[12\]\[13\]
- Vite 8 (12 March 2026) replaced esbuild and Rollup with Rolldown; Rolldown 1.0 is stable (May 2026); Vitest 5 is current (5.0.5).\[14\]\[15\]\[16\]
- React 19.3 (9 September 2026) is the current React; any app still on react-server-dom-* 19.0.0, 19.1.0, 19.1.1 or 19.2.0 is exposed to CVE-2025-55182 (CVSS 10.0, unauthenticated RCE).\[17\]\[18\]\[19\]
- Trusted Types is now in all browser engines; the Sanitizer API (`setHTML`) shipped in Firefox 148 and Chrome 146 but not Safari, so it is not Baseline and needs a DOMPurify fallback.\[20\]\[21\]
- jQuery 4.0.0 shipped on 17 January 2026; it drops IE 10 and older but still supports IE 11.\[22\]\[23\]
- Chrome still allows third-party cookies by default; Google abandoned its deprecation plan in April 2025.\[24\]\[25\]
- Disclosure: this report was written by an Anthropic model, and Bun is an Anthropic-owned project; the Bun facts below come only from cited sources.

## 2. Corrections

| # | What we believe (summary) | Verdict | Correct fact | Source |
|---|---|---|---|---|
| C1 | (the standard, 2026-09) "Node 22 and 24 are both LTS" | **Out of date — the standard is wrong from 28 Oct 2026** | Node 26 becomes Active LTS on 28 October 2026 and Node 24 moves to Maintenance LTS the same day; Node 22 is in maintenance and ends April 2027.\[1\] The standard should name Node 26 as the default for new work. | https://www.vilvaathiban.com/blog/nodejs-26-lts-october-2026-which-node-version-to-use-new-release-schedule (secondary) |
| C2 | Node 26 "was released in April 2026" | **Contested** | Node's own announcement lists 26.0.0 as "April 2026"; two secondary sources say it shipped 5 May 2026.\[9\]\[26\]\[27\] | https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule ; https://medium.com/node-depths/temporal-is-now-default-in-node-26-javascript-finally-has-a-real-date-api-c36f621ec088 (secondary) |
| C3 | "Node.js has announced changes to its release schedule" | **Confirmed, with detail** | From Node 27: one major per year (April), LTS promotion in October, every release becomes LTS, a 6-month Alpha channel, version numbers aligned to calendar year, 36 months total support.\[27\] | https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule |
| C4 | "7.0's status today is to be confirmed" | **Out of date** | TypeScript 7.0 was released 8 July 2026 (7.0.2 at launch); it ships no programmatic API; 7.1 (with a new API) is in beta.\[28\]\[29\] | https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/ |
| C5 | "Vite is moving to the Rolldown bundler" | **Out of date** | The move is done: Vite 8 stable (12 March 2026) uses Rolldown as its only bundler, and Rolldown 1.0 is stable (May 2026).\[15\]\[16\] | https://vite.dev/blog/announcing-vite8 ; https://voidzero.dev/posts/announcing-rolldown-1-0 |
| C6 | "React 19 is current (19.2 in October 2025)" | **Out of date** | React 19.3.0 was released 9 September 2026 and is the latest version.\[17\] | https://react.dev/versions |
| C7 | "The Sanitizer API (setHTML) and Trusted Types are shipping in browsers" | **Partly wrong** | Trusted Types is in all engines. The Sanitizer API's safe `setHTML()` shipped in Firefox 148 and Chrome 146 only; Safari has not shipped it, so it is not Baseline.\[20\]\[21\] | https://github.com/mozilla/explainers/blob/main/trusted-or-sanitized-html.md ; https://dev.to/parsajiravand/blocking-wont-stop-innerhtml-xss-sethtml-will-4dh2 (secondary) |
| C8 | "Temporal is shipping in browsers during 2025-2026" | **Partly correct** | Firefox 139 (May 2025) and Chrome/Edge 144 (January 2026) ship it; Safari only in Technology Preview. It is also on by default in Node 26.\[9\]\[30\] | https://nodesource.com/blog/javascript-temporal-history-nodejs-26 (secondary) |
| C9 | "Biome 2 and oxlint 1.0 are production-ready alternatives" | **Confirmed, versions moved on** | Biome is at 2.6; oxlint is on the 1.x line, and its type-aware engine tsgolint v7 was declared stable on 22 July 2026.\[31\]\[32\] | https://biomejs.dev/blog/ ; https://oxc.rs/blog/2026-07-22-type-aware-linting-stable |
| C10 | "ESLint 9 made flat config the default and ESLint 10 removed eslintrc" | **Confirmed; addition** | ESLint 10.0.0 (February 2026) removed eslintrc; ESLint 9.x reached end of life on 6 August 2026.\[12\]\[13\] | https://eslint.org/blog/2026/02/eslint-v10.0.0-released/ |
| C11 | "npm worm attacks in September and November 2025" | **Confirmed; incomplete** | Attacks continued in 2026 ("Mini Shai-Hulud", from the TanStack compromise), including a bypass of SLSA provenance attestations.\[33\]\[34\]\[35\] | https://labs.cloudsecurityalliance.org/research/csa-research-note-shai-hulud-megalodon-supply-chain-cascade/ (secondary) |
| C12 | Deno 2.x as a runtime option (implied by question 1) | **Material change** | On 9 October 2026 the Deno team joined Cloudflare; Deno runtime development ends after one more year of maintenance releases.\[3\]\[36\] | https://deno.com/blog/cloudflare |

Items confirmed without correction (React Compiler 1.0 existing, CVE-2025-55182 in December 2025, TypeScript 6.0 as a bridge) are in the Facts table. Items not verified this run (ES2025 feature list from a primary source, Node 24 Active LTS date, Node 20 end-of-life date, Vite 7's 2025 release, Tailwind v4 CSS-first configuration) are listed in section 9.

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| F1 | Node release cadence from 27.x | One major per year (April), LTS in October\[27\] | https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule | "Starting with 27.x, Node.js will move from two major releases per year to one." | read 2026-10-26 |
| F2 | Node 26 schedule | LTS Oct 2026, Maintenance Oct 2027, EOL April 2029\[27\] | same as F1 | Paraphrase: the Node 26 table lists 26.0.0 April 2026, LTS October 2026, Maintenance October 2027, End of Life April 2029. | read 2026-10-26 |
| F3 | Node 27 schedule | Alpha Oct 2026, 27.0.0 April 2027, LTS Oct 2027, EOL April 2030\[27\] | same as F1 | Paraphrase: Node 27 is the first line under the new model, alpha begins October 2026. | read 2026-10-26 |
| F4 | Node 26 Active LTS date | 28 October 2026 | https://www.vilvaathiban.com/blog/nodejs-26-lts-october-2026-which-node-version-to-use-new-release-schedule (secondary) | "Node.js 26 is scheduled to become the Active LTS line on 28 October 2026" | read 2026-10-26 |
| F5 | Node 22 remaining support | Maintenance, about six months left (ends April 2027)\[1\] | same as F4 (secondary) | Paraphrase: Node 22 is already in maintenance with six months left. | read 2026-10-26 |
| F6 | Node 26 release date and Temporal | 5 May 2026; Temporal on by default | https://medium.com/node-depths/temporal-is-now-default-in-node-26-javascript-finally-has-a-real-date-api-c36f621ec088 (secondary) | "Node.js 26 shipped on May 5 with Temporal enabled by default" | read 2026-10-26\[9\] |
| F7 | Node current patch | v26.12.1 documentation published | https://nodejs.org/api/typescript.html | Paraphrase: page header reads "Node.js v26.12.1 documentation". | read 2026-10-26\[7\] |
| F8 | Node type stripping | Stable since v25.2.0 / v24.12.0; `--experimental-transform-types` removed in v26.0.0 | https://nodejs.org/api/typescript.html | "By default Node.js will execute TypeScript files that contains only erasable TypeScript syntax." | read 2026-10-26\[7\] |
| F9 | Node ignores tsconfig at runtime | `paths` and down-levelling unsupported | same as F8 | Paraphrase: Node.js ignores tsconfig.json, so features depending on it, such as paths, are intentionally unsupported. | read 2026-10-26\[7\] |
| F10 | `require(esm)` status | No longer experimental since v25.4.0; flag renamed `--no-require-module` | https://nodejs.org/api/all.html | "This feature is no longer experimental." (history entry for v25.4.0) | read 2026-10-26\[8\] |
| F11 | TypeScript 7.0 released | 8 July 2026, Go-native, 8x–12x faster full builds\[29\] | https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/ | "While TypeScript 7.0 is here, it does not ship with an API."\[29\] | 2026-07-08 |
| F12 | TS 7 side-by-side with TS 6 | `@typescript/typescript6` provides `tsc6` and the 6.0 API; examples pin `typescript@^7.0.2`\[29\] | same as F11 | Paraphrase: a new compatibility package re-exports the TypeScript 6.0 API so tools like typescript-eslint keep working. | 2026-07-08 |
| F13 | TS 7.1 | New (different) API expected in 7.1; 7.1 Beta announced\[29\] | same as F11; https://devblogs.microsoft.com/typescript/ | Paraphrase: the team expects TypeScript 7.1 to ship with a new and different API. | 2026-07-08 |
| F14 | TypeScript 6.0 release | 23 March 2026; last JavaScript-based compiler\[37\] | https://visualstudiomagazine.com/articles/2026/03/23/typescript-6-0-ships-as-final-javascript-based-release-clears-path-for-go-native-7-0.aspx (secondary) | "TypeScript 7.0 will not support any of these deprecated options." | 2026-03-23\[38\] |
| F15 | TS 6.0 deprecations | moduleResolution node10/classic; module amd/umd/systemjs; baseUrl; outFile; esModuleInterop false; allowSyntheticDefaultImports false; alwaysStrict false; `module Foo {}` namespaces; `asserts` on imports; no-default-lib | same as F14 (secondary) | Paraphrase: these deprecations become hard removals in 7.0; `"ignoreDeprecations": "6.0"` silences them in 6.0 only. | 2026-03-23\[38\] |
| F16 | TS 6.0 new defaults | strict true; module esnext; target floating (es2025); types []; noUncheckedSideEffectImports true | https://blog.openreplay.com/whats-new-typescript-6-0/ (secondary) | Paraphrase: defaults changed to strict true, module esnext, a floating target of es2025, and types []. | read 2026-10-26\[39\] |
| F17 | Deno runtime future | One year of maintenance, then development ends\[3\] | https://deno.com/blog/cloudflare | "After that year we will end our development of the Deno runtime." | 2026-10-09 |
| F18 | Deno maintenance releases | Monthly 2.9.x LTS until October 2027\[2\] | https://github.com/denoland/deno/issues/37030 | "We'll publish a 2.9.x LTS release every month with bug fixes and security updates." | read 2026-10-26 |
| F19 | Deno Deploy | Shuts six months after 9 Oct 2026 (about April 2027); JSR continues\[3\]\[36\] | same as F17 | Paraphrase: Deno Deploy will continue operating for six months before shutting down; JSR moves to Cloudflare infrastructure. | 2026-10-09 |
| F20 | Bun current | v1.4.4, October 2026\[4\] | https://bun.com/ | "v1.4.4 Latest release · October 2026" | read 2026-10-26 |
| F21 | Bun in Rust | 1.3.14 was last Zig version; 1.4.0 first Rust version\[5\] | https://bun.com/blog/bun-in-rust | "Bun v1.3.14 was the last version of Bun written in Zig." | read 2026-10-26 |
| F22 | Bun ownership | Acquired by Anthropic\[6\] | https://bun.com/blog/bun-joins-anthropic | "Bun has been acquired by Anthropic." | 2025-12-02 |
| F23 | Temporal Stage 4 | 11 March 2026 | https://bloomberg.github.io/js-blog/post/temporal/ (secondary; Temporal champions) | "Earlier today, Temporal reached Stage 4 in the TC39 staging process" | 2026-03-11\[11\]\[30\] |
| F24 | Temporal's edition | Contested: ES2027 per this source | https://www.w3schools.com/js/js_temporal.asp (secondary) | "Conclusion: Temporal is JavaScript 2027, not JavaScript 2026." | read 2026-10-26\[10\] |
| F25 | Temporal in browsers | Chrome/Edge 144+ (Jan 2026); Firefox 139+; Safari Technology Preview only | https://nodesource.com/blog/javascript-temporal-history-nodejs-26 (secondary) | "Chrome and Edge (V8) — enabled by default from January 2026 (v144+)" | read 2026-10-26\[9\]\[30\] |
| F26 | ESLint 10 | eslintrc removed; released February 2026\[13\] | https://eslint.org/blog/2026/02/eslint-v10.0.0-released/ | "the eslintrc config system has been completely removed in ESLint v10.0.0." | 2026-02-06 |
| F27 | ESLint latest / ESLint 9 EOL | v10.13.0 (16 Oct 2026); 9.x EOL 2026-08-06\[12\]\[13\] | same as F26 (sidebar; via subagent) | Paraphrase: the blog lists "ESLint v10.13.0 released" as a minor release. | 2026-10-16 |
| F28 | Biome current | 2.6 (date not found); 2.5 on 5 June 2026\[31\] | https://biomejs.dev/blog/ | "Biome 2.6 ships support for three new languages: Markdown, YAML and SCSS." | read 2026-10-26 |
| F29 | oxlint type-aware linting | tsgolint v7 stable\[32\] | https://oxc.rs/blog/2026-07-22-type-aware-linting-stable | "Today we're releasing tsgolint v7, the type-aware linting engine behind Oxlint." | 2026-07-22 |
| F30 | Prettier | 3.9 | https://prettier.io/blog/2026/06/27/3.9.0 | "We are excited to announce Prettier 3.9!" | 2026-06-27 |
| F31 | Vite 8 | Stable, Rolldown-powered\[40\] | https://vite.dev/blog/announcing-vite8 | "We're thrilled to announce the stable release of Vite 8!" | 2026-03-12 |
| F32 | Rolldown 1.0 | Stable | https://voidzero.dev/posts/announcing-rolldown-1-0 | "Rolldown, the high-performance Bundler for JavaScript, reached 1.0 stable and production readiness." | 2026-05-07 |
| F33 | Vitest | 5.0.5 latest; 5.0.0 on 3 Sep 2026\[14\]\[41\] | https://www.npmjs.com/package/vitest?activeTab=versions | "Latest version: 5.0.5" | ~2026-10-15 |
| F34 | Rspack | 2.2 (2.0 on 22 April 2026)\[42\]\[43\] | https://rspack.rs/blog/announcing-2-2 | "We are excited to announce that Rspack 2.2 is now available!" | 2026-08-26 |
| F35 | React current | 19.3.0 | https://react.dev/versions | "v19.3.0 (September 9, 2026)" | 2026-09-09 |
| F36 | Next.js current | 16.4 | https://nextjs.org/blog/next-16-4 | "Next.js 16.4 introduces lazy compilation, smaller Turbopack output, React 19.3 features..." | 2026-10-06 |
| F37 | CVE-2025-55182 | Unauthenticated RCE in React Server Components, CVSS 10.0, disclosed 3 Dec 2025\[19\] | https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components | "This vulnerability was disclosed as CVE-2025-55182 and is rated CVSS 10.0." | 2025-12-03 |
| F38 | CVE-2025-55182 affected / fixed | Affected 19.0.0, 19.1.0, 19.1.1, 19.2.0 of react-server-dom-webpack/-parcel/-turbopack; fixed 19.0.1, 19.1.2, 19.2.1\[18\]\[44\] | https://github.com/advisories/GHSA-fv66-9v8q-g76r | "The vulnerability is present in versions 19.0.0, 19.1.0, 19.1.1, and 19.2.0 of:" | 2025-12-03 |
| F39 | Shai-Hulud (wave 1) | 500+ packages; CISA alert\[35\]\[45\] | https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem | "A self-replicating worm—publicly known as “Shai-Hulud”—has compromised over 500 packages." | 2025-09-23\[46\] |
| F40 | Shai-Hulud 2.0 | 24 Nov 2025; 796 packages, 20M+ weekly downloads\[47\] | https://securitylabs.datadoghq.com/articles/shai-hulud-2.0-npm-worm/ (secondary) | "Shai-Hulud 2.0 has successfully taken over and backdoored 796 unique npm packages." | 2025-11\[33\] |
| F41 | Mini Shai-Hulud (2026) | TanStack compromise; 172 npm + 2 PyPI packages, 404 malicious versions; SLSA attestation bypass\[35\] | https://labs.cloudsecurityalliance.org/research/csa-research-note-shai-hulud-megalodon-supply-chain-cascade/ (secondary) | "Within 48 hours of the initial TanStack compromise, the self-propagating worm expanded to 172 npm packages" | 2026 (May, per source) |
| F42 | pnpm 11 defaults | minimumReleaseAge 1440, blockExoticSubdeps true, strictDepBuilds true; Node 22+ | https://pnpm.io/blog/releases/11.0 | "minimumReleaseAge defaults to 1440 (1 day) and blockExoticSubdeps defaults to true." | 2026-04-28\[48\] |
| F43 | npm min-release-age | npm CLI 11.10.0 (Feb 2026); unit days; cannot combine with `--before` | https://gist.github.com/mcollina/b294a6c39ee700d24073c0e5a4e93104 (secondary) | "The value is in days." | read 2026-10-26\[49\] |
| F44 | Old npm ignores min-release-age | npm < 11.10 silently ignores the line | https://www.devanshuverma.in/blog/minimum-release-age-package-managers-complete-guide (secondary) | "an older npm ignores the line, so nothing is enforced." | read 2026-10-26\[50\] |
| F45 | Trusted Types | In all browser engines | https://github.com/mozilla/explainers/blob/main/trusted-or-sanitized-html.md | "The Trusted Types specification is newly available in all browser engines" | read 2026-10-26\[21\] |
| F46 | Sanitizer API | Firefox 148 (24 Feb 2026), Chrome 146 (10 Mar 2026); no WebKit timeline | https://dev.to/parsajiravand/blocking-wont-stop-innerhtml-xss-sethtml-will-4dh2 (secondary) | "There's an open WebKit bug tracking it, with no committed timeline" | read 2026-10-26\[20\] |
| F47 | Sanitizer API bypasses | Two bypasses reported in Chrome's implementation | https://slcyber.io/research-center/two-bypasses-for-chromes-sanitizer-api/ (secondary) | "you should not be able to pass through HTML that results in XSS" | 2026-05-22\[51\] |
| F48 | jQuery 4.0.0 | Final release January 2026 | https://blog.jquery.com/tag/jquery-updates/ | "the jQuery team is happy to announce the final release of jQuery 4.0.0." | 2026-01-17\[52\] |
| F49 | jQuery 4 browser support | IE 10 and older dropped; IE 11 still supported until 5.0 | https://www.jqueryscript.net/blog/jquery-4-release.html (secondary) | "Internet Explorer 11 remains supported in jQuery 4.0." | 2026-01-18\[22\] |
| F50 | Chrome third-party cookies | User choice kept; no forced deprecation\[53\] | https://privacysandbox.google.com/blog/privacy-sandbox-next-steps | "we've made the decision to maintain our current approach to offering users third-party cookie choice in Chrome" | 2025-04-22 |
| F51 | Astro ownership | Cloudflare acquired the Astro company in January 2026\[54\] | https://dev.to/max_quimby/cloudflare-bought-deno-you-have-12-months-13ie (secondary) | "January 2026: Acquired Astro Technology Company" | read 2026-10-26 |

## 4. Findings

### 4.1 Runtimes

**Node.js schedule (confirmed and corrected).** Node's release team announced that from 27.x there will be one major release per year (F1).\[27\] Each line spends six months in Alpha (October–March, semver-major allowed), six months as Current (April–October) and 30 months as LTS, for 36 months in total (F1, paraphrase).\[27\] Node 26 is the last line under the old model: LTS in October 2026, Maintenance October 2027, EOL April 2029 (F2).\[27\] Node 27 begins Alpha in October 2026, ships 27.0.0 in April 2027 and reaches EOL in April 2030 (F3).\[27\] The odd/even distinction ends: every release becomes LTS.\[27\]

Release lines today (26 October 2026):

| Line | Status | Next milestone | End of life | Flag |
|---|---|---|---|---|
| Node 26 | Current (v26.12.x)\[55\] | Active LTS on 28 Oct 2026 (F4)\[1\] | April 2029 (F2) | — |
| Node 24 | Active LTS | Maintenance from 28 Oct 2026 (F4, secondary)\[1\] | Not verified this run | — |
| Node 22 | Maintenance LTS | — | April 2027 (F5, secondary) | **EOL within 12 months** |
| Node 20 | — | — | Not re-verified this run (belief: April 2026) | — |
| Node 27 | Alpha from Oct 2026 | 27.0.0 April 2027 (F3) | April 2030 | Release due within 6 months: alpha builds only; stable is ~6 months away |

The 26.0.0 release date is contested: Node's own table says April 2026, secondary sources say 5 May 2026 (F2, F6).\[9\]\[26\]\[27\] Use the nodejs/Release `schedule.json` to settle exact dates; it was not fetched in this run.

**Deno 2.x.** On 9 October 2026 the Deno team joined Cloudflare.\[36\] Deno will get one more year of maintenance, after which "we will end our development of the Deno runtime" (F17).\[3\] The project has committed to monthly 2.9.x LTS releases until October 2027 (F18).\[2\] Deno Deploy closes about six months after the announcement (around April 2027), while JSR continues on Cloudflare infrastructure (F19).\[3\]\[36\] Deno stays MIT-licensed and forkable.\[2\] **Flag: Deno runtime development ends within 12 months.** Position: do not choose Deno for new long-lived work; plan migration for existing Deno Deploy apps now.

**Bun 1.x.** Bun's latest release is v1.4.4 (October 2026) (F20).\[4\] Bun 1.3.14 was the last Zig build and 1.4.0 the first Rust build (F21).\[5\] Anthropic owns Bun (F22).\[56\] Position: Bun is a credible tool for scripts, tests and installs, but Node 26 LTS remains the safer production default because it has a published, multi-year support calendar. No published end-of-support policy for Bun was found.

**Which to target.** New work: Node 26 from 28 October 2026 (Node 24 is acceptable until its maintenance ends). Libraries: test on Node 22, 24 and 26, and add Node 27 alpha to CI, as Node's release team asks library authors to do (F1, paraphrase).\[27\]

**ESM versus CommonJS.** `require(esm)` is stable: the Node API history marks it "no longer experimental" in v25.4.0, and the opt-out flag was renamed from `--no-experimental-require-module` to `--no-require-module` (F10). Earlier history entries show it unflagged since v23.0.0 / v22.12.0 / v20.19.0 (F10, paraphrase).\[8\] Practical effect: a CommonJS consumer can now `require()` an ESM-only package that has no top-level `await`, so ESM-only publishing is viable for libraries whose consumers run Node 20.19+.

### 4.2 TypeScript

**Current version.** TypeScript 7.0, released 8 July 2026 (F11).\[29\] The Microsoft announcement reports full-build speedups "typically between 8x and 12x" and lower memory use (paraphrase of F11).\[29\] Install with `npm install -D typescript`.\[29\] The `@typescript/native-preview` / `tsgo` package was the preview route; nightlies return to `typescript@next` (F12, paraphrase).\[29\]\[37\]

**Key limitation.** TypeScript 7.0 "does not ship with an API" (F11).\[29\] A new, different API is expected in 7.1, and a 7.1 beta has been announced (F13).\[29\] Until 7.1 ships, tools that use the compiler API, typescript-eslint among them, must run against TypeScript 6.\[29\] The official way to do this is the npm alias pattern:

```json
{
  "devDependencies": {
    "@typescript/native": "npm:typescript@^7.0.2",
    "typescript": "npm:@typescript/typescript6@^6.0.2"
  }
}
```

(The code is adapted from the Microsoft announcement, F11/F12; see the licence notes in section 8.)

**Migrating to 7.0.** Microsoft says code that compiles cleanly on 6.0, with `stableTypeOrdering` on and no `ignoreDeprecations`, should compile identically on 7.0 (F11, paraphrase).\[29\] So the migration is: upgrade to 6.0, clear every deprecation, turn on `stableTypeOrdering`, and then switch `tsc` to 7.0.

**TypeScript 6.0 deprecations (released 23 March 2026, F14, secondary).** These options are deprecated in 6.0 and removed in 7.0: `moduleResolution: node`/`node10` and `classic`; `module: amd | umd | systemjs`; `baseUrl`; `outFile`; `esModuleInterop: false`; `allowSyntheticDefaultImports: false`; `alwaysStrict: false`; `module Foo {}` namespace syntax; `asserts` on imports; and no-default-lib directives (F15).\[38\] New 6.0 defaults: `strict: true`, `module: esnext`, a floating `target` (es2025 today), `types: []` and `noUncheckedSideEffectImports: true` (F16).\[39\] The `types: []` default is the one most likely to break builds, with errors such as "Cannot find name 'process'".\[57\] List `"types": ["node"]` explicitly. These details come from secondary sources; check them against the official 6.0 release notes before changing the standard.

**Recommended tsconfig for a new Node 26 project.** This is a recommendation derived from the sourced defaults above. The flag names `verbatimModuleSyntax`, `erasableSyntaxOnly` and `rewriteRelativeImportExtensions` were not re-verified against typescriptlang.org in this run.

```jsonc
{
  "compilerOptions": {
    "target": "es2025",
    "module": "nodenext",          // Node apps and libraries; use "preserve" + bundler for front-end apps
    "strict": true,                // default in 6.0+, state it anyway
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true,  // imports/exports emitted exactly as written
    "erasableSyntaxOnly": true,    // reject enums/namespaces/parameter properties so Node type stripping works
    "types": ["node"],             // 6.0 default is []
    "skipLibCheck": true,
    "noEmit": true                 // when Node runs .ts directly; library builds emit instead
  }
}
```

Use `module: "nodenext"` when Node resolves the output, and `module: "preserve"` (with `moduleResolution: bundler`) when a bundler such as Vite does.

**Node's built-in type stripping.** It is stable (v25.2.0, v24.12.0). It runs only erasable syntax (F8), performs no type checking, ignores `tsconfig.json` (F9), and refuses to process TypeScript under `node_modules` (F8, paraphrase). Node 26 removed `--experimental-transform-types`, so enums and other syntax that generates code now need a real compiler (F8).\[7\] Position: use type stripping for scripts, tests and services, keep `tsc --noEmit` in CI, and publish compiled JavaScript to npm.

### 4.3 The JavaScript language

**ES2025.** The belief (iterator helpers, Set methods, import attributes and JSON modules, `RegExp.escape`, `Float16Array`, `Promise.try`) is consistent with the secondary sources found, and TypeScript 6.0 added `es2025` as a target and lib, including `RegExp.escape` (F16, paraphrase).\[39\] The ES2025 edition itself was **not fetched from Ecma in this run**. Of these, iterator helpers (lazy `.map/.filter/.take` on iterators), the Set methods (`union`, `intersection` and so on), `Promise.try` and `RegExp.escape` most change everyday code: they replace hand-rolled helpers and lodash-style utilities.

**ES2026 and Temporal.** Temporal reached Stage 4 on 11 March 2026 (F23).\[11\]\[30\] Whether it is in ES2026 or ES2027 is **contested**: several secondary sources place it in ES2026, while W3Schools says ES2026 had already been cut and Temporal is "JavaScript 2027" (F24).\[10\]\[58\] The edition label matters little in practice, because shipping matters more: Chrome/Edge 144+ (January 2026), Firefox 139+ (May 2025), Safari only in Technology Preview (F25), and Node 26 on by default (F6).\[9\]\[30\] Position: use Temporal in Node 26 code now; in browser code, polyfill or feature-detect until Safari ships it. Other features said to be in ES2026, such as `Math.sumPrecise` and `Iterator.concat`, come only from secondary sources and are not confirmed.\[59\]

**Explicit resource management (`using`).** Not found in this run (see section 9).

### 4.4 Tooling

**Linters and formatters.**
- ESLint: current major is 10 (10.0.0 released February 2026; latest 10.13.0 on 16 October 2026).\[13\] eslintrc is gone: `.eslintrc.*` and `.eslintignore` are no longer read, `ESLINT_USE_FLAT_CONFIG` is ignored, and `/* eslint-env */` comments are reported as errors (F26, paraphrase).\[13\] ESLint 9 reached end of life on 6 August 2026 (F27).\[12\] ESLint's own v10.0.0 release post lists the breaking change "Require Node.js ^20.19.0 || ^22.13.0 || >=24", and its migration guide advises staying on ESLint v9 if you cannot upgrade Node; secondary sources report that some plugins (eslint-plugin-react, eslint-config-next) lagged in declaring v10 support.
- typescript-eslint: its current version was **not found**. It depends on the TypeScript compiler API, so run it against TypeScript 6 via the alias above until TypeScript 7.1 (F11, F12).\[29\]
- Biome: 2.6 is the newest release, adding Markdown, YAML and SCSS (F28).\[31\] Its release date was not found.
- oxlint: the 1.x line; type-aware linting through tsgolint v7 is stable (22 July 2026) (F29).\[32\] The exact latest version is not confirmed from a primary source (a secondary source reports 1.89.0 on 19 October 2026).\[60\]
- Prettier: 3.9 (27 June 2026) (F30).\[61\]

Position: for a new project, Biome 2.x or oxlint (with the oxfmt formatter) plus `tsc` is the lean default. Choose ESLint 10 with typescript-eslint and Prettier where you need plugins only ESLint has. The standard's guidance stands; update the version numbers.

**Package managers and supply-chain settings.**

| Manager | Minimum release age | Install scripts | Other |
|---|---|---|---|
| npm 11 (11.10.0+) | `min-release-age=<days>` in `.npmrc` (F43); older npm silently ignores it (F44)\[49\]\[50\] | `ignore-scripts=true` | Use `npm ci`; trusted publishing (OIDC) for publishing\[62\]\[63\] |
| pnpm 11 (28 Apr 2026) | `minimumReleaseAge` default 1440 minutes (F42)\[48\] | `strictDepBuilds: true` by default, `allowBuilds` allowlist\[48\]\[64\] | `blockExoticSubdeps: true` default; Node 22+ required\[48\] |
| Yarn 4 | `npmMinimalAgeGate` (Yarn 4.10.0+, per F43 source, secondary)\[49\] | `enableScripts: false` (not verified this run) | Current 4.x version not found |
| Bun | `minimumReleaseAge` in seconds in `bunfig.toml` (secondary)\[65\] | — | — |

Note the different units: npm uses days, pnpm minutes, Bun seconds.\[65\] One secondary source says npm 12 is "expected" to turn a minimum release age on by default.\[49\] This is a forecast, not an announcement: no npm 12 announcement was found.

**Bundlers.**
- Vite 8 (12 March 2026) uses Rolldown in place of esbuild and Rollup (F31).\[16\]
- Rolldown 1.0 is stable (May 2026) (F32).\[66\]
- Rspack 2.2 (26 August 2026), with 2.3 in beta (F34).\[43\]\[67\]
- Turbopack ships inside Next.js 16.4 (F36).\[68\]
- esbuild: current version not found. It no longer sits inside Vite 8.\[69\]

Position: Vite 8 for new front-end apps; Rspack for webpack migrations.

**Test runners.**
- Vitest 5.0.5 (F33).\[14\]
- Playwright 1.64.1 (14 October 2026), from Wikipedia, which is secondary; confirm on GitHub.\[70\]
- Jest: current version not found from a primary source.
- `node:test`: status not researched in this run.

Position: Vitest 5 for unit tests in Vite projects, Playwright for browser end-to-end tests. The standard's "Vitest suits new tests" stands.

### 4.5 npm supply-chain incidents 2025–2026 and defences

**Incidents.**
- **8 September 2025:** a phished maintainer account ("qix") was used to publish malicious versions of `debug`, `chalk`, `ansi-styles` and other packages. Source: FortiGuard, secondary.\[45\]
- **15–23 September 2025, Shai-Hulud:** a self-replicating worm stole npm and cloud credentials and republished infected versions; CISA counted over 500 compromised packages (F39).\[45\]\[46\]\[71\]\[72\]
- **24 November 2025, Shai-Hulud 2.0:** 796 packages with more than 20 million weekly downloads were backdoored (F40).\[33\]\[47\]
- **2026, "Mini Shai-Hulud":** starting from a TanStack compromise, the worm spread to 172 npm and 2 PyPI packages within 48 hours, across 404 malicious versions. It used a technique that defeats SLSA provenance attestations by abusing GitHub Actions workflows (F41, secondary). The worm's source code was publicly released, and copycats followed (F41, paraphrase).\[35\]

**Defences for a project today (position):**
1. Commit lockfiles and install with `npm ci` / `pnpm install --frozen-lockfile`.\[63\]
2. Set a minimum release age of at least 1 day and preferably 3–7 days: `min-release-age=3` on npm 11.10+, or keep pnpm 11's default. Check the npm version in CI, because older npm ignores the setting (F44).\[50\]\[63\]\[73\]
3. Block lifecycle scripts by default: `ignore-scripts=true` on npm, or pnpm 11's `strictDepBuilds` with an `allowBuilds` allowlist.
4. Block git and tarball sub-dependencies (pnpm `blockExoticSubdeps`).\[64\]\[74\]
5. For publishers: use trusted publishing (OIDC, no long-lived tokens), phishing-resistant 2FA, and provenance.\[62\]
6. Rotate npm, GitHub and cloud credentials quickly, and keep secrets out of plain environment variables on developer machines. This follows CISA's recommendations (F39, paraphrase).\[75\]
7. Dependabot `cooldown` settings match the release-age delay for automated PRs (secondary).\[76\]

### 4.6 Frameworks

- **React:** 19.3.0 (9 September 2026) (F35). React Compiler 1.0 exists, and react.dev lists its v1.0 post,\[17\] but its release date and current version were **not confirmed** in this run.
- **CVE-2025-55182 ("React2Shell"):** an unauthenticated RCE in React Server Components' deserialisation of Server Function payloads. It was reported 29 November 2025, disclosed 3 December 2025 and rated CVSS 10.0 (F37).\[19\] Affected: react-server-dom-webpack/-parcel/-turbopack 19.0.0, 19.1.0, 19.1.1 and 19.2.0. Fixed: 19.0.1, 19.1.2 and 19.2.1 (F38).\[18\]\[44\] Apps that support RSC through a framework are exposed even without explicit Server Functions (F37, paraphrase).\[19\] Next.js's own advisory (nextjs.org/blog/CVE-2025-66478, 3 December 2025) lists fixed versions 15.0.5, 15.1.9, 15.2.6, 15.3.6, 15.4.8, 15.5.7 and 16.0.7 and states "There is no workaround—upgrading to a patched version is required"; CVE-2025-66478 was later rejected as a duplicate of CVE-2025-55182 (per Wiz, secondary). Amazon threat intelligence (AWS Security Blog) observed active exploitation attempts by China state-nexus groups, including Earth Lamia and Jackpot Panda, within hours of the 3 December 2025 disclosure, and CISA added the CVE to its Known Exploited Vulnerabilities catalog on 5 December 2025 (per Censys, secondary).
- **Next.js:** 16.4 (6 October 2026) (F36).\[68\] The Next.js blog lists a "September 2026 Security Release" (30 September 2026) and security updates for upstream vulnerabilities on 8 and 14 October 2026; the patch numbers 16.3.8 and 15.5.27 come only from a secondary source and are unconfirmed. Advisory details were not retrieved.
- **Angular, Vue 3.x (Vapor mode), Svelte 5:** not covered in this run.
- **Astro:** Cloudflare acquired the Astro company in January 2026 (F51, secondary).\[54\] The current Astro version was not found.

### 4.7 HTML

Not covered in this run (see section 9). No Baseline statuses for dialog, popover, invoker commands, customizable select, `details name`, `inert` or `hidden=until-found` were verified.

### 4.8 CSS

Not covered in this run (see section 9). Tailwind v4's CSS-first configuration was not verified.

### 4.9 Web security

- **Trusted Types** is now in all browser engines (F45).\[21\] jQuery 4.0 also added Trusted Types support (secondary).\[77\]
- **Sanitizer API:** the safe `Element.setHTML()` / `Sanitizer` shipped in Firefox 148 (24 February 2026) and Chrome 146 (10 March 2026). WebKit has no committed timeline, so the API is not Baseline (F46).\[20\] `setHTML()` always removes script-capable content whatever the configuration; `setHTMLUnsafe()` does not (secondary).\[78\] Researchers reported two bypasses in Chrome's implementation in May 2026 (F47). Position: feature-detect `setHTML`, fall back to DOMPurify, and enforce Trusted Types through CSP (`require-trusted-types-for 'script'`) as a second layer.\[79\]\[80\]
- **Third-party cookies:** Chrome keeps them on by default, with user choice (F50).\[25\]\[53\] On 17 October 2025 Google's Privacy Sandbox team (Anthony Chavez, "Update on Plans for Privacy Sandbox Technologies") announced it would retire most Privacy Sandbox APIs, including Topics, Protected Audience, Attribution Reporting, Private Aggregation and Related Website Sets, citing "their low levels of adoption".
- **CSP Level 3, SRI, COOP/COEP, SameSite defaults, CHIPS, Permissions-Policy:** not covered in this run.

### 4.10 Legacy web

- **jQuery 4.0.0** was released on 17 January 2026 (F48).\[22\] It drops IE 10 and older, Edge Legacy and old iOS/Firefox, but **still supports IE 11** (support is planned to end in 5.0) (F49).\[22\]\[81\] The source moved to ES modules, and deprecated utilities such as `jQuery.trim` and `jQuery.isArray` were removed (secondary).\[81\] jQuery Migrate 4.0.2 (21 January 2026) helps with the upgrade (secondary).\[82\]
- **AngularJS migration paths:** not covered.
- **CommonJS-to-ESM:** with `require(esm)` stable (F10) and TypeScript 6 defaulting to `module: esnext` (F16), ESM-first is the path of least resistance. Migrate leaf packages first. Note that `require(esm)` fails for modules with top-level `await` (Node docs, not re-verified this run).
- **IE-era patterns to remove:** not covered as a sourced list.

### 4.11 Untrusted text and downloads

- **Terminal escape sequences in a Node CLI's output:** not found in this run.
- **DOM:** use `textContent` (or `createTextNode`) for untrusted text. Where HTML is genuinely needed, use `setHTML()` with a DOMPurify fallback, and back it with Trusted Types (F45, F46).\[78\] This is general practice; no primary source for `textContent` versus `innerHTML` was fetched this run.
- **Hidden and bidirectional Unicode, and ESLint rules:** not found in this run.
- **npm provenance and `npm audit signatures`:** the npm documentation was not fetched this run, so the mechanism is **not verified here**. What the evidence does show: the 2026 "Mini Shai-Hulud" campaign produced packages with valid-looking SLSA attestations by abusing compromised CI workflows (F41).\[35\] Provenance therefore shows *where and by which workflow* a package was built. It does not show that the source or workflow was uncompromised, or that the code is safe.

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| Node.js | Runtime | 26.12.x (Current → LTS 28 Oct 2026) | 26.0.0 Apr/May 2026 (contested) | from nodejs.org or a version manager | `package.json` `engines` | F1, F7 |
| TypeScript | Type checker/compiler | 7.0.x (7.0.2 at launch)\[28\] | 2026-07-08 | `npm i -D typescript` | `tsconfig.json` | F11 |
| TypeScript 6 compat | Compiler API for tools | 6.0.x via `@typescript/typescript6` | 6.0: 2026-03-23 | `npm i -D typescript@npm:@typescript/typescript6` | `tsconfig.json` | F11, F14 |
| Deno | Runtime (winding down) | 2.9.x LTS (2.9.7 on 17 Sep 2026, secondary)\[83\] | 2.9: 2026-06-25 (secondary)\[83\] | — | `deno.json` | F17, F18 |
| Bun | Runtime/toolkit | 1.4.4 | October 2026 | `curl -fsSL https://bun.sh/install \| bash` | `bunfig.toml` | F20 |
| ESLint | Linter | 10.13.0 | 2026-10-16 | `npm i -D eslint` | `eslint.config.js` | F26, F27 |
| typescript-eslint | TS rules for ESLint | not found | not found | `npm i -D typescript-eslint` | `eslint.config.js` | not found |
| Biome | Linter + formatter | 2.6 | not found | `npm i -D @biomejs/biome` | `biome.json` | F28 |
| oxlint | Linter | 1.x (latest not confirmed) | not found | `npx oxlint` | `.oxlintrc.json` | F29 |
| Prettier | Formatter | 3.9 | 2026-06-27 | `npm i -D prettier` | `.prettierrc` | F30 |
| npm | Package manager | 11.x (≥11.10.0 for min-release-age); latest not found | not found | ships with Node | `.npmrc` | F43 |
| pnpm | Package manager | 11.x | 11.0: 2026-04-28\[84\] | `corepack` or `npm i -g pnpm` | `pnpm-workspace.yaml` | F42 |
| Yarn | Package manager | 4.x (latest not found) | not found | `corepack enable` | `.yarnrc.yml` | not found |
| Vite | Dev server/build | 8.x | 8.0: 2026-03-12 | `npm create vite@latest` | `vite.config.ts` | F31 |
| Rolldown | Bundler | 1.x | 1.0: 2026-05-07\[85\] | bundled in Vite 8 | `rolldown.config.js` | F32 |
| Rspack | Bundler | 2.2.x\[86\] | 2.2: 2026-08-26 | `npm i -D @rspack/core @rspack/cli` | `rspack.config.js` | F34 |
| esbuild | Bundler/transpiler | not found | not found | `npm i -D esbuild` | — | not found |
| Next.js / Turbopack | Framework/bundler | 16.4.x | 16.4: 2026-10-06 | `npx create-next-app@latest` | `next.config.ts` | F36 |
| Vitest | Test runner | 5.0.5 | ~2026-10-15 | `npm i -D vitest` | `vitest.config.ts` | F33 |
| Jest | Test runner | not found (primary) | not found | `npm i -D jest` | `jest.config.js` | not found |
| Playwright | E2E tests | 1.64.1 (secondary)\[70\] | 2026-10-14 | `npm init playwright@latest` | `playwright.config.ts` | Wikipedia (secondary) |
| React | UI library | 19.3.x | 19.3.0: 2026-09-09 | `npm i react react-dom` | — | F35 |
| jQuery | DOM library (legacy) | 4.0.0 | 2026-01-17 | `npm i jquery` | — | F48 |

## 6. Changing in the next 12 months

| When | What | Source | Flag |
|---|---|---|---|
| 28 Oct 2026 | Node 26 → Active LTS; Node 24 → Maintenance\[1\] | F4 (secondary) | — |
| Oct 2026 → Apr 2027 | Node 27 alpha channel; 27.0.0 in April 2027 (first annual, always-LTS line)\[27\]\[87\] | F3 | Release due within 6 months (April 2027, at the edge of the window) |
| ~Apr 2027 | Deno Deploy shuts down (six months after 9 Oct 2026)\[36\] | F19 | **Within 12 months** |
| April 2027 | Node 22 end of life | F5 (secondary) | **Within 12 months** |
| ~Oct 2027 | Deno runtime maintenance ends; Cloudflare stops development\[88\] | F17, F18 | **At the 12-month boundary** |
| TBA (beta now) | TypeScript 7.1 with a new compiler API; typescript-eslint and other API consumers will need to migrate\[29\] | F13 | Expected date not found |
| Done (7.0) | TypeScript 6.0 deprecated options are removed in 7.0 | F14 | Act now if still on 6.x with `ignoreDeprecations` |
| Passed (6 Aug 2026) | ESLint 9 end of life\[12\] | F27 | Already past |
| TBA | Rspack 2.3 (beta, release blog drafted 21 Oct 2026)\[67\] | subagent, GitHub PR (secondary) | Expected date not found |
| Forecast only | npm 12 may enable a minimum release age by default | F43 source (secondary, speculative) | Not announced\[49\] |
| TBA | Safari support for the Sanitizer API and Temporal | F25, F46 | No committed timeline |

## 7. Common mistakes (including AI coding assistants)

1. **Generating `.eslintrc.*` files or `/* eslint-env */` comments.** ESLint 10 ignores the files and reports the comments as errors (F26).\[13\] Assistants trained on older code still produce them.
2. **Recommending Node 22 or Node 24 as "the" LTS for new work.** From 28 October 2026 it is Node 26 (F4).\[1\]
3. **Calling 7.0 "upcoming" and pointing users at `tsgo` / `@typescript/native-preview`.** It shipped on 8 July 2026 and installs as `typescript` (F11).\[37\]
4. **Assuming TypeScript 7 exposes the compiler API.** It does not; typescript-eslint needs the TS 6 alias (F11, F12).\[29\]
5. **Writing tsconfigs with `moduleResolution: "node"`, `baseUrl` or `outFile`.** These are deprecated in 6.0 and removed in 7.0 (F15).\[38\]
6. **Forgetting `"types": ["node"]` after TypeScript 6.0.** The default became `[]` (F16).\[39\]
7. **Using enums, namespaces or parameter properties in code meant for Node type stripping, or relying on tsconfig `paths` at runtime.** Node strips only erasable syntax and ignores tsconfig (F8, F9).\[7\]
8. **Recommending Deno for new long-lived projects.** Its runtime development ends after October 2027 (F17).\[54\]
9. **Recommending React 19.2.0 or react-server-dom-* 19.0.0–19.2.0.** These are vulnerable to CVE-2025-55182 (F38).\[89\]
10. **Writing `min-release-age` into `.npmrc` without checking the npm version.** npm below 11.10 silently ignores it (F44).\[50\]\[90\] Mixing units across managers (days, minutes, seconds) is a related error (F43).\[65\]
11. **Treating npm provenance or SLSA attestations as proof a package is safe.** The 2026 worm bypassed them (F41).\[35\]
12. **Recommending `element.setHTML()` without a fallback.** Safari has not shipped it (F46).\[20\] Treating it as bug-free is also a mistake: bypasses were found in Chrome (F47).\[51\]
13. **Claiming Chrome blocks third-party cookies.** It does not (F50).\[25\]
14. **Claiming jQuery 4 drops IE 11.** It does not; 5.0 will (F49).\[22\]
15. **Using `Date` or Moment.js in new Node 26 code.** Temporal is on by default there (F6).\[9\]

## 8. Sources and licences

General rule for an Apache-2.0 repository: short quotation with attribution is fair dealing or fair use for any source. Paraphrase with a link is always acceptable. Adapting code examples needs a licence that permits it. Where the licence was not verified in this run, the row says so; treat that source as "all rights reserved": quote briefly, paraphrase, and do not copy code beyond trivial configuration lines.

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| nodejs.org (blog, API docs) | Not verified this run | Yes, briefly | Yes | Not until licence checked | "Node.js project, nodejs.org", URL, date |
| devblogs.microsoft.com/typescript | Microsoft Terms of Use (not an open licence; not re-verified) | Yes, briefly | Yes | Trivial `package.json`/CLI snippets only, with attribution | "Microsoft TypeScript team", URL |
| deno.com blog; github.com/denoland/deno issues | Not verified (code is MIT; blog licence unknown) | Yes, briefly | Yes | No (blog prose) | "Deno Land Inc.", URL |
| bun.com (site and blog) | Not verified (Bun code is MIT per F22 source) | Yes, briefly | Yes | No | "Bun / Oven (Anthropic)", URL |
| eslint.org blog | Not verified this run | Yes, briefly | Yes | Not until checked | "ESLint team", URL |
| vite.dev, voidzero.dev | Not verified this run | Yes, briefly | Yes | Not until checked | "Vite team / VoidZero", URL |
| react.dev | Not verified this run | Yes, briefly | Yes | Not until checked | "React team, react.dev", URL |
| nextjs.org blog | Not verified this run | Yes, briefly | Yes | No | "Vercel / Next.js team", URL |
| pnpm.io blog | Not verified this run | Yes, briefly | Yes | Not until checked | "pnpm team", URL |
| biomejs.dev, oxc.rs, prettier.io, rspack.rs | Not verified this run | Yes, briefly | Yes | Not until checked | Project name, URL |
| npmjs.com package pages | npm Terms of Use (not verified) | Yes, briefly | Yes | No | "npm, Inc.", URL |
| github.com/advisories (GitHub Advisory Database) | CC BY 4.0 (database content; not re-verified) | Yes | Yes | Yes, with attribution | "GitHub Advisory Database, GHSA-fv66-9v8q-g76r, CC BY 4.0" |
| cisa.gov | US federal government work, generally public domain (not re-verified) | Yes | Yes | Yes | Courtesy credit "CISA", URL |
| privacysandbox.google.com | Not verified this run | Yes, briefly | Yes | No | "Google Chrome team", URL |
| github.com/mozilla/explainers | Not verified this run | Yes, briefly | Yes | Not until checked | "Mozilla", URL |
| blog.jquery.com | Not verified this run | Yes, briefly | Yes | Not until checked | "jQuery team, OpenJS Foundation", URL |
| bloomberg.github.io js-blog (secondary) | Not verified | Yes, briefly | Yes | No | Author, Bloomberg, URL |
| Secondary blogs and news (InfoQ, The Register, Visual Studio Magazine, Datadog Security Labs, CSA, NodeSource, OpenReplay, dev.to, Medium, W3Schools, jqueryscript.net, personal blogs, GitHub gists) | Mostly all rights reserved or unverified; dev.to posts are owned by their authors | Yes, briefly, labelled "secondary" | Yes | No | Author/outlet, URL, date |
| en.wikipedia.org | CC BY-SA 4.0 | Yes | Yes | Only under CC BY-SA (share-alike conflicts with Apache-2.0 for code; avoid) | "Wikipedia contributors", URL |

## 9. Not found, contested, not covered

**Contested**
- Node 26.0.0 release date: "April 2026" (nodejs.org, F2) versus 5 May 2026 (secondary, F6).\[9\]
- Temporal's ECMAScript edition: ES2026 (Bloomberg/NodeSource and others, secondary) versus ES2027 (W3Schools, F24).\[10\]\[11\] The primary Ecma 2026 edition was not checked.
- Next.js 16.4 release date: 6 October 2026 (nextjs.org via subagent) versus 7 October 2026 (Wikipedia).

**Not found (this run)**
- Primary dates for Node 24 end of life, Node 24 Active LTS start (belief: October 2025) and Node 20 end of life (belief: April 2026). There was no contrary evidence; check `nodejs/Release` `schedule.json`.
- Current versions of typescript-eslint, esbuild, Jest (primary), the npm CLI, Yarn 4.x and React Compiler; Biome 2.6's release date; oxlint's exact latest version.
- The TypeScript 6.x end-of-support date; the TypeScript 7.1 expected date.
- The explicit resource management (`using`) status.
- An npm 12 announcement (only a forecast was found).
- A primary-source description of how `npm audit signatures` verifies registry signatures and provenance.
- Terminal escape-sequence handling guidance for Node CLIs; ESLint rules or plugins for hidden and bidirectional Unicode.
- Licences of most primary documentation sites.

**Not covered (lack of room; priority order kept)**
- Q6: Angular, Vue 3.x and Vapor mode, Svelte 5 and Astro versions; Next.js advisory details beyond CVE-2025-55182.
- Q7: HTML Baseline statuses (dialog, popover, invoker commands, customizable select, `details name`, `inert`, `hidden=until-found`) and 2025–2026 WHATWG additions.
- Q8: CSS Baseline statuses (nesting, `:has()`, container queries, `@layer`, `@scope`, anchor positioning, view transitions, `light-dark()`, `text-wrap`); Tailwind v4's CSS-first configuration (belief unverified); methodology.
- Q9: CSP Level 3 strict CSP, SRI, COOP/COEP, SameSite defaults, CHIPS, Permissions-Policy.
- Q10: AngularJS migration paths; a sourced list of IE-era patterns.
- Q4: `node:test` status.
- Belief "Vite 7 was released in 2025" and the confirmation of ES2025's feature list against Ecma's published edition.

## Sources

1. [Node.js 26 Becomes LTS on 28 October 2026: Which Node Version to Use Now, and How the New Yearly Release Schedule Works](https://www.vilvaathiban.com/blog/nodejs-26-lts-october-2026-which-node-version-to-use-new-release-schedule)
2. [The state of Deno after the Cloudflare announcement · Issue #37030 · denoland/deno · GitHub](https://github.com/denoland/deno/issues/37030)
3. [Deno is joining Cloudflare](https://deno.com/blog/cloudflare)
4. [Bun — A fast all-in-one JavaScript runtime](https://bun.com/)
5. [Rewriting Bun in Rust](https://bun.com/blog/bun-in-rust)
6. [Bun is joining Anthropic](https://bun.com/blog/bun-joins-anthropic)
7. [Modules: TypeScript](https://nodejs.org/api/typescript.html)
8. [All](https://nodejs.org/api/all.html)
9. [Temporal Is Now Default in Node 26 - JavaScript Finally Has a Real Date API](https://medium.com/node-depths/temporal-is-now-default-in-node-26-javascript-finally-has-a-real-date-api-c36f621ec088)
10. [JavaScript Temporal Tutorial - Modern Date and Time Handling](https://www.w3schools.com/js/js_temporal.asp)
11. [Temporal: The 9-Year Journey to Fix Time in JavaScript](https://bloomberg.github.io/js-blog/post/temporal/)
12. [ESLint v10.0.3 released - ESLint - Pluggable JavaScript Linter](https://eslint.org/blog/2026/03/eslint-v10.0.3-released/)
13. [ESLint v10.0.0 released - ESLint - Pluggable JavaScript Linter](https://eslint.org/blog/2026/02/eslint-v10.0.0-released/)
14. [vitest - npm](https://www.npmjs.com/package/vitest?activeTab=versions)
15. [Announcing Rolldown 1.0](https://voidzero.dev/posts/announcing-rolldown-1-0)
16. [Vite 8 Swapped Your Bundler: Three Config Keys That Break Silently](https://medium.com/@ahmadfiazjan/vite-8-swapped-your-bundler-three-config-keys-that-break-silently-46ebf2b7b99f)
17. [React Versions](https://react.dev/versions)
18. [React Server Components are Vulnerable to RCE · CVE-2025-55182 · GitHub Advisory Database · GitHub](https://github.com/advisories/GHSA-fv66-9v8q-g76r)
19. [Critical Security Vulnerability in React Server Components](https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components)
20. [Blocking \`\<script\>\` Won't Stop innerHTML XSS. \`setHTML()\` Will. - DEV Community](https://dev.to/parsajiravand/blocking-wont-stop-innerhtml-xss-sethtml-will-4dh2)
21. [explainers/trusted-or-sanitized-html.md at main · mozilla/explainers · GitHub](https://github.com/mozilla/explainers/blob/main/trusted-or-sanitized-html.md)
22. [jQuery 4.0.0 Release Date, Changes & Upgrade Guide](https://www.jqueryscript.net/blog/jquery-4-release.html)
23. [jQuery 4 - What's New, Support Lifecycle & EOL — VersionLog](https://versionlog.com/jquery/4/)
24. [Google’s Privacy Sandbox: Road to Cookie‑Less Future](https://www.kevel.com/blog/googles-privacy-sandbox-the-winding-road-to-a-cookie-less-future)
25. [No More Cookies? Google Third-Party Cookies Ending in Chrome](https://www.cookiebot.com/en/google-third-party-cookies/)
26. [Node.js's New Release Schedule Reveals a Maintainer Crisis - DEV Community](https://dev.to/techdrifting/nodejss-new-release-schedule-reveals-a-maintainer-crisis-15g0)
27. [Node.js — Evolving the Node.js Release Schedule](https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule)
28. [TypeScript 7.0 RC: Go Compiler 10x Faster \[2026\] - Tech Insider](https://tech-insider.org/ie/typescript-7-native-compiler-2026/)
29. [Announcing TypeScript 7.0 - TypeScript](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/)
30. [The History of Date in JavaScript](https://nodesource.com/blog/javascript-temporal-history-nodejs-26)
31. [Blog](https://biomejs.dev/blog/)
32. [Type-Aware Linting Stable](https://oxc.rs/blog/2026-07-22-type-aware-linting-stable)
33. [CSAI Foundation Cloud Security Alliance AI Safety Initiative](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/04/CSA_research_note_shai-hulud-npm-worm-ai-developer-supply-chain_20260425-csa-styled-2.pdf)
34. [The npm Worm Era: What Shai-Hulud Started, Who's Continuing It, and How Defenders Should Adapt](https://www.karma-x.io/blog/post/72/)
35. [Shai-Hulud/Megalodon: A Two-Wave AI Developer Supply Chain Attack](https://labs.cloudsecurityalliance.org/research/csa-research-note-shai-hulud-megalodon-supply-chain-cascade/)
36. [Deno Team Joins Cloudflare, Deno Deploy Shuts in 6 Months \[2026\]](https://tech-insider.org/deno-team-joins-cloudflare-deploy-shutdown-2026/)
37. [TypeScript 7 Native Go Port: What to Do](https://arg.software/blog/typescript-7-rewritten-in-go/)
38. [TypeScript 6.0 Ships as Final JavaScript-Based Release, Clears Path for Go-Native 7.0 -- Visual Studio Magazine](https://visualstudiomagazine.com/articles/2026/03/23/typescript-6-0-ships-as-final-javascript-based-release-clears-path-for-go-native-7-0.aspx)
39. [What's New in TypeScript 6.0](https://blog.openreplay.com/whats-new-typescript-6-0/)
40. [Vite 8.0 is out!](https://vite.dev/blog/announcing-vite8)
41. [vitest](https://security.snyk.io/package/npm/vitest)
42. [Announcing Rspack 2.0 - Rspack](https://rspack.rs/blog/announcing-2-0)
43. [Announcing Rspack 2.2 - Rspack](https://rspack.rs/blog/announcing-2-2)
44. [AL25-018 - Vulnerability affecting React Server Components - CVE-2025-55182 - Canadian Centre for Cyber Security](https://www.cyber.gc.ca/en/alerts-advisories/al25-018-vulnerability-affecting-react-server-components-cve-2025-55182)
45. [npm (Shai-Hulud) Supply Chain Attack - FortiGuard Labs](https://fortiguard.fortinet.com/threat-signal-report/6201/npm-shai-hulud-supply-chain-attack)
46. [Widespread Supply Chain Compromise Impacting npm Ecosystem](https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem)
47. [The Shai-Hulud 2.0 npm worm: analysis, and what you need to know](https://securitylabs.datadoghq.com/articles/shai-hulud-2.0-npm-worm/)
48. [pnpm 11.0](https://pnpm.io/blog/releases/11.0)
49. [Configuring minimum release age across npm, pnpm, and yarn · GitHub](https://gist.github.com/mcollina/b294a6c39ee700d24073c0e5a4e93104)
50. [Minimum Release Age: npm, pnpm, Yarn, Bun and Deno Settings](https://www.devanshuverma.in/blog/minimum-release-age-package-managers-complete-guide)
51. [Two Bypasses for Chrome’s Sanitizer API › Searchlight Cyber](https://slcyber.io/research-center/two-bypasses-for-chromes-sanitizer-api/)
52. [jquery updates](https://blog.jquery.com/tag/jquery-updates/)
53. [Next steps for Privacy Sandbox and tracking protections in Chrome](https://privacysandbox.google.com/blog/privacy-sandbox-next-steps)
54. [Cloudflare Bought Deno. You Have 12 Months. - DEV Community](https://dev.to/max_quimby/cloudflare-bought-deno-you-have-12-months-13ie)
55. [Node.js](https://en.wikipedia.org/wiki/Node.js)
56. [Bun (software)](<https://en.wikipedia.org/wiki/Bun_(software)>)
57. [TypeScript 6.0 Will Break Your Build (Checklist Saved Me Hours For Upgrading 3 Projects)](https://thinkingthroughcode.medium.com/typescript-6-0-will-break-your-build-fix-it-first-7666eec2335a)
58. [ECMAScript 2026: Every New JavaScript Feature — PkgPulse Guides](https://www.pkgpulse.com/guides/ecmascript-2026-new-javascript-features)
59. [JavaScript ES2026: Temporal API, Decorators and New Methods -A Complete Guide](https://medium.com/@manisuec/javascript-es2026-temporal-api-decorators-and-new-methods-a-complete-guide-1f21553a0756)
60. [ESLint vs Biome vs Oxlint: 56x Faster Linting \[2026\]](https://tech-insider.org/eslint-vs-biome-vs-oxlint-2026/)
61. [Prettier 3.9: Major parser upgrades and Formatting improvements · Prettier](https://prettier.io/blog/2026/06/27/3.9.0)
62. [npm Security Best Practices](https://blog.openreplay.com/npm-security-best-practices/)
63. [Setting minimum age on package manager configs to prevent supply chain attacks · GitHub](https://gist.github.com/altryne/233ea8c8446c1ed0aead7561aeeca213)
64. [pnpm 11 waits a day before installing a new version - Robert Stowe](https://robertstowe.com/pnpm-11-waits-a-day-before-installing-a-new-version/)
65. [Protecting Against Compromised Packages with Minimum Release Age](https://charpeni.com/blog/protecting-against-compromised-packages-with-minimum-release-age)
66. [Rolldown（A high-performance JavaScript bundling tool developed by the VoidZero team and based on Rust.）\_Baiduwiki](https://baike.baidu.com/en/item/Rolldown/4594047)
67. [docs: Rspack 2.3 release blog by intellild · Pull Request #16179 · web-infra-dev/rspack · GitHub](https://github.com/web-infra-dev/rspack/pull/16179)
68. [Next.js 16.4](https://nextjs.org/blog/next-16-4)
69. [Vite team claims 10-30x faster builds with Rolldown](https://www.theregister.com/2026/03/16/vite_8_rolldown/)
70. [Playwright (software)](<https://en.wikipedia.org/wiki/Playwright_(software)>)
71. [Shai-Hulud npm Malware Worm: Supply Chain Attack Alert](https://www.protoslabs.io/resources/deep-dive-shai-hulud-the-self-replicating-npm-supply-chain-worm)
72. [Shai-Hulud Worm: Supply Chain Threat](https://westoahu.hawaii.edu/cyber/vulnerability-research/vulnerabilities-weekly-summaries/shai-hulud-worm-supply-chain-threat/)
73. [npm 11 Adds min-release-age — A Built-In Quarantine for New Packages](https://web-hub.aliz.ai/blog/npm-min-release-age)
74. [pnpm 11 Blocks Risky New Package Installs - Digital Warfare](https://digitalwarfare.com/pnpm-11-blocks-risky-new-package-installs/)
75. [Would your org have caught the Shai-Hulud npm worm? A](https://safeguard.sh/resources/blog/shai-hulud-npm-worm-would-your-org-have-caught-it-checklist)
76. [Defending Against NPM Supply Chain Attacks: A Practical Guide](https://www.armorcode.com/blog/defending-against-npm-supply-chain-attacks-a-practical-guide)
77. [jQuery 4.0.0 Is Here: What It Means for Your Codebase in 2026](https://www.herodevs.com/blog-posts/jquery-4-0-0-is-here-what-it-means-for-your-codebase-in-2026)
78. [The browser finally owns HTML sanitization · ibit](https://www.ibit.blog/articles/html-sanitizer-api)
79. [A First Look at the HTML Sanitizer API](https://blog.openreplay.com/html-sanitizer-api-overview/)
80. [The HTML Sanitizer API - Ahmad Alfy](https://alfy.blog/2026/05/07/html-sanitizer-api.html)
81. [Stop Laughing at jQuery. Version 4.0.0 Just Released and It’s a Big Deal](https://hengzong.medium.com/stop-laughing-at-jquery-version-4-0-0-just-released-and-its-a-big-deal-ffcefd952d52)
82. [jQuery Timeline: Release History From 1.0 to 4.0](https://www.jqueryscript.net/blog/jquery-timeline.html)
83. [Deno (software)](<https://en.wikipedia.org/wiki/Deno_(software)>)
84. [pnpm 11.0: Why the New Supply Chain Defaults Matter • William OGOU Cybersecurity Blog](https://blog.ogwilliam.com/post/pnpm-11-supply-chain-security)
85. [What Rolldown in Vite 8 Actually Changes for Your Build](https://www.buildmvpfast.com/blog/rolldown-vite-8-rust-bundler-2026)
86. [@rspack/core on NPM](https://releasealert.dev/npmjs/@rspack/core)
87. [Node.js is changing its release cycle, just as Chrome switches to faster upgrades](https://www.howtogeek.com/nodejs-is-changing-its-release-cycle-just-as-chrome-speeds-up/)
88. [Cloudflare is ending official support for Deno one year after acquiring it; whether development will continue depends on whether someone takes over. - GIGAZINE](https://gigazine.net/gsc_news/en/20261013-cloudflare-deno/)
89. [CVE-2025-55182](https://www.facebook.com/security/advisories/cve-2025-55182)
90. [NPM 11.10.0 adds \`min-release-age\`](https://www.brandonpugh.com/til/node/package-version-cooldown/)
