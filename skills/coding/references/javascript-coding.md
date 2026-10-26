# JavaScript and TypeScript coding

Read this for TypeScript or JavaScript on Node.js: tsconfig, ES modules, Node versions and
built-ins, type stripping, promises, and lint and format.

Untrusted input (`eval`, shells, prototype pollution, paths, ReDoS, SQL) is the
javascript-security module's; HTML and CSS the html-coding module's; browser and DOM security the
web-security module's; tests the planned testing skill's; packages and lockfiles the planned
supply-chain-security module's and the project-bootstrap-and-audit standard's. React isn't
covered.

## Rules

1. **Type-check everything with TypeScript in strict mode,** and run `tsc` in CI. Use `unknown`
   at the edges, not `any`.
2. **Write ES modules:** `"type": "module"`, `node:` specifiers, and full file extensions.
3. **Run on a Node line in LTS, and use its built-ins before a package:** `fetch`, `node:test`,
   `--env-file`, `util.parseArgs`, and type stripping for TypeScript.
4. **Every promise is awaited, returned, or handled,** and a type-aware lint rule checks it.
5. **One lint and format setup, run in CI,** chosen by the standard. ESLint takes only its flat
   config.

### Types and `tsconfig.json`

TypeScript 6.0 made `strict` the default and stopped loading every `@types` package (fact
`js-ts6-defaults`); set both anyway. Add `noUncheckedIndexedAccess` (fact
`js-ts-unchecked-index`). Options 6.0 deprecated (fact `js-ts6-deprecations`) are errors in 7.0
(fact `js-ts7-errors`): use `nodenext`, or `bundler` under a bundler. For code Node runs, Node's
config (fact `js-strip-types`) plus strict checks:

```json
{
  "compilerOptions": {
    "target": "esnext",
    "module": "nodenext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "verbatimModuleSyntax": true,
    "erasableSyntaxOnly": true,
    "rewriteRelativeImportExtensions": true,
    "types": ["node"],
    "noEmit": true
  },
  "include": ["src"]
}
```

### Modules

State `"type": "module"` in every `package.json` (fact `js-type-field`). Relative imports carry
their extension, `./http.ts` (fact `js-esm-extensions`), and built-ins the `node:` prefix.
CommonJS can `require()` an ES module with no top-level `await` (fact `js-require-esm`), so a
library can ship ES modules only.

### Node versions and built-ins

The standard's *Language toolchains* names the Node line; Node advises LTS only in production
(fact `js-node-lts-only`). Set `engines` to the lowest version the code needs, and test on it.

| Instead of | Use | Fact |
|---|---|---|
| `ts-node`, or a build step to run TypeScript | Type stripping (`node src/main.ts`) | `js-strip-types` |
| `node-fetch`, `axios` for plain requests | `fetch`, with `AbortSignal.timeout` | `js-fetch` |
| `dotenv` | `node --env-file=.env` | `js-env-file` |
| `minimist`, `yargs` for a small CLI | `util.parseArgs` | `js-parseargs` |
| A test framework for unit tests | `node:test`, `node:assert/strict` | `js-node-test` |

```json
{
  "name": "example-tool",
  "private": true,
  "type": "module",
  "engines": { "node": ">=24.12" },
  "scripts": {
    "start": "node --env-file=.env src/main.ts",
    "test": "node --test",
    "typecheck": "tsc"
  }
}
```

- **Type stripping** doesn't type-check, ignores `tsconfig.json` (use subpath imports, not
  `paths`), needs `import type`, and skips `node_modules`, so packages publish JavaScript (fact
  `js-strip-types`).
- **`--env-file` doesn't override** a variable already set (fact `js-env-file`).
- **`fetch` resolves on HTTP errors:** check `response.ok` (fact `js-fetch-status`), with a
  timeout:

```typescript
export async function getJson(url: string, timeoutMs = 10_000): Promise<unknown> {
  const response = await fetch(url, { signal: AbortSignal.timeout(timeoutMs) });
  if (!response.ok) {
    throw new Error(`GET ${url} failed: HTTP ${response.status}`);
  }
  return response.json();
}
```

### Promises and async code

- **Mark a deliberate fire-and-forget** with `void` and a `.catch`.
- **`Promise.all` rejects on the first failure** (fact `js-promise-all`), and the rest keeps
  running; `Promise.allSettled` returns every result.
- **`return await` inside `try`:** without it, a rejection skips the `catch` (fact
  `js-return-await`).
- **Lint for floating promises** with types: typescript-eslint's or oxlint's
  `no-floating-promises`, or Biome's `noFloatingPromises` (facts `js-floating-tseslint`,
  `js-oxlint-type-aware`, `js-floating-biome`).

### Lint and format

The standard's *Language toolchains* picks Biome, or ESLint with Prettier where plugins exist.
ESLint 10 reads only `eslint.config.*`; ESLint 9 is past its end of life (fact `js-eslint9-eol`).
TypeScript 7 has no compiler API and typescript-eslint stops below 6.1 (facts `js-ts7-api`,
`js-tseslint-ts-range`), so keep 6.0 beside 7.0 through Microsoft's `@typescript/typescript6`
alias. oxlint builds on TypeScript 7.

## Mistakes

- **`.eslintrc.json`, `/* eslint-env node */` or `"moduleResolution": "node"`** from old
  examples, which ESLint 10 and TypeScript 7.0 reject (facts `js-eslint10-eslintrc`,
  `js-ts7-errors`).
- **`Cannot find name 'process'` after an upgrade.** Add `"types": ["node"]` (fact
  `js-ts6-defaults`), not `any`.
- **`require`, `module.exports` or `__dirname` in an ES module,** which throw. Use `import`,
  `export` and `import.meta.dirname` (fact `js-esm-dirname`).
- **Enums, `namespace` with values, or parameter properties in code Node runs,** which type
  stripping rejects: set `erasableSyntaxOnly`, and use string-literal unions or `as const`.
- **`items.forEach(async (item) => { await save(item); })`,** which returns before any save ends
  (fact `js-foreach-async`). Use `for...of`, or `Promise.all(items.map(save))`.
- **An `async` call with no `await`,** often a logger or cache write: its rejection ends the
  process (fact `js-unhandled-rejections`).
- **`as User` on parsed JSON or a caught error,** a guess. Type it `unknown`, then narrow or
  validate it.
- **Targeting Node 20 or older because an example does.** It ended 2026-04-30 (fact
  `js-node20-eol`).

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Strict types | `"strict": false`, no `tsc` in CI, `any` or `as` at input | `GAP` | Rule 1 |
| Options 7.0 removes | `node` or `node10` resolution, `baseUrl`, `es5`, `ignoreDeprecations` | `DRIFT` | `nodenext` or `bundler` |
| Module type | No `"type"`, or `require` and `import` mixed | `GAP` | `"type": "module"` |
| Node line | `engines`, `.nvmrc` or CI past end of life | `GAP` | The standard's line |
| Type stripping | `.ts` run without `erasableSyntaxOnly` or `verbatimModuleSyntax`, or with `paths` | `DRIFT` | The config above |
| Replaced packages | `dotenv`, `node-fetch`, `minimist`, `ts-node` | `OVER` | The built-in |
| Floating promises | No type-aware rule, or `forEach(async` | `GAP` | Rule 4 |
| Old ESLint config | `.eslintrc.*`, `.eslintignore`, `eslint-env` on ESLint 10 | `DRIFT` | `eslint.config.js` |
| Typed lint on 7.0 | typescript-eslint with `typescript` 7 and no 6.0 alias | `DRIFT` | The alias |

## Why

### Strict TypeScript

- **The advice:** strict mode and `noUncheckedIndexedAccess`, in CI.
- **The reason:** otherwise `null` and missed lookups pass, then throw at runtime.
- **What others do, and why:** JSDoc types with `checkJs`, to skip a build step.
- **What it costs:** annotations, narrowing, a gradual migration.
- **When to choose differently:** a short script that never grows.

### The module format

- **The advice:** ES modules, with `"type"` and extensions.
- **The reason:** without `"type"`, Node guesses each file's format, which costs time.
  Browsers run ES modules too.
- **What others do, and why:** many libraries ship both formats; `require(esm)` makes one enough.
- **What it costs:** ES module forms of `__dirname`; CommonJS-only tools go.
- **When to choose differently:** a library whose users run Node without `require(esm)`.

### Built-ins before packages

- **The advice:** the runtime's built-in before a package.
- **The reason:** a package is code to review and trust, and a way in for a compromised
  release.
- **What others do, and why:** larger projects keep frameworks for snapshots or subcommands.
- **What it costs:** the built-ins do less: no enums, no help text from `util.parseArgs`.
- **When to choose differently:** when a built-in lacks what the project needs.

### Promises

- **The advice:** every promise handled, proved by a type-aware lint rule.
- **The reason:** a floating rejection ends the process, on a failure path tests rarely take.
- **What others do, and why:** typescript-eslint leads; oxlint has 59 of its 61 typed rules, and
  Biome's rule is experimental.
- **What it costs:** slower linting, to build types.
- **When to choose differently:** untyped JavaScript, where review is what's left.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `js-node-lts-only` | Production on LTS only | [Node](https://nodejs.org/en/about/previous-releases) | "should only use Active LTS or Maintenance LTS releases" | 2026-10-26 | 2027-10-26 |
| `js-node20-eol` | Node 20 ended 2026-04-30 | [schedule](https://raw.githubusercontent.com/nodejs/Release/main/schedule.json) | "\"end\": \"2026-04-30\"" | 2026-10-26 | 2027-10-26 |
| `js-ts6-defaults` | 6.0: `strict` on, `types` empty | [TS 6.0](https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/) | "strict is now true by default" and "the default types value will be []" | 2026-10-26 | 2027-10-26 |
| `js-ts6-deprecations` | Deprecated in 6.0 | [TS 6.0](https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/) | "node10) is deprecated" and "baseUrl is deprecated" and "target: es5 option is deprecated" | 2026-10-26 | 2027-10-26 |
| `js-ts7-errors` | 7.0 errors on those | [TS 7.0](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/) | "hard errors in the face of any flags and constructs deprecated" | 2026-10-26 | 2027-10-26 |
| `js-ts7-api` | 7.0 has no API | [TS 7.0](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/) | "it does not ship with an API" | 2026-10-26 | 2027-04-26 |
| `js-tseslint-ts-range` | Below 6.1.0 | [typescript-eslint](https://typescript-eslint.io/users/dependency-versions/) | "The version range of TypeScript currently supported is" | 2026-10-26 | 2027-04-26 |
| `js-ts-unchecked-index` | Lookups gain `undefined` | [TSConfig](https://www.typescriptlang.org/tsconfig/) | "will add undefined to any un-declared field" | 2026-10-26 | 2027-10-26 |
| `js-strip-types` | Stable in v24.12.0; the limits above | [Node](https://nodejs.org/api/typescript.html) | "Type stripping is now stable." and "no type checking is performed" and "Node.js ignores tsconfig.json files" and "the type keyword is necessary" and "refuses to handle TypeScript files inside folders under a node_modules" | 2026-10-26 | 2027-04-26 |
| `js-type-field` | State `"type"` | [Node](https://nodejs.org/api/packages.html) | "should always include the \"type\" field" | 2026-10-26 | 2027-10-26 |
| `js-esm-extensions` | Imports need extensions | [Node](https://nodejs.org/api/esm.html) | "A file extension must be provided" | 2026-10-26 | 2027-10-26 |
| `js-esm-dirname` | `import.meta.dirname` | [Node](https://nodejs.org/api/esm.html) | "can be replicated via import.meta.filename and import.meta.dirname" | 2026-10-26 | 2027-10-26 |
| `js-require-esm` | `require(esm)` unflagged in v22.12.0 | [Node](https://nodejs.org/api/modules.html) | "contains no top-level await" | 2026-10-26 | 2027-04-26 |
| `js-node-test` | Stable since v20.0.0 | [Node](https://nodejs.org/api/test.html) | "The test runner is now stable." | 2026-10-26 | 2027-10-26 |
| `js-fetch` | Stable since v21.0.0 | [Node](https://nodejs.org/api/globals.html) | "A browser-compatible implementation of the fetch() function." | 2026-10-26 | 2027-10-26 |
| `js-fetch-status` | No rejection on HTTP errors | [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch) | "does not reject if the server responds with HTTP status codes" | 2026-10-26 | 2027-10-26 |
| `js-env-file` | Stable from v22.21.0; the environment wins | [Node](https://nodejs.org/api/cli.html) | "The --env-file flag is no longer experimental." and "the value from the environment takes precedence." | 2026-10-26 | 2027-04-26 |
| `js-parseargs` | Stable since v20.0.0 | [Node](https://nodejs.org/api/util.html) | "The API is no longer experimental." | 2026-10-26 | 2027-10-26 |
| `js-unhandled-rejections` | Throws since v15.0.0 | [Node](https://nodejs.org/api/cli.html) | "Changed default mode to throw." | 2026-10-26 | 2027-10-26 |
| `js-foreach-async` | `forEach` doesn't wait | [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach) | "it does not wait for promises." | 2026-10-26 | 2027-10-26 |
| `js-promise-all` | First rejection rejects | [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all) | "rejects when any of the input's promises rejects" | 2026-10-26 | 2027-10-26 |
| `js-return-await` | `catch` sees it | [typescript-eslint](https://typescript-eslint.io/rules/return-await/) | "allows the promise's rejection to be caught" | 2026-10-26 | 2027-10-26 |
| `js-floating-tseslint` | Needs types | [typescript-eslint](https://typescript-eslint.io/rules/no-floating-promises/) | "This rule requires type information to run" | 2026-10-26 | 2027-10-26 |
| `js-floating-biome` | In Biome's nursery | [Biome](https://biomejs.dev/linter/rules/no-floating-promises/) | "This rule is part of the nursery group." | 2026-10-26 | 2027-04-26 |
| `js-oxlint-type-aware` | TypeScript 7; 59 of 61 | [Oxc](https://oxc.rs/blog/2026-07-22-type-aware-linting-stable) | "tracks TypeScript v7.0.2" and "59 of typescript-eslint's 61 type-aware rules" | 2026-10-26 | 2027-04-26 |
| `js-eslint10-eslintrc` | ESLint 10 removed eslintrc | [ESLint](https://eslint.org/blog/2026/02/eslint-v10.0.0-released/) | "the eslintrc config system has been completely removed" | 2026-10-26 | 2027-10-26 |
| `js-eslint9-eol` | ESLint 9 ended 2026-08-06 | [ESLint](https://eslint.org/version-support/) | "ESLint v9.x reached end-of-life on 2026-08-06" | 2026-10-26 | 2027-10-26 |

## Sources

Our own words, with brief, attributed quotes.

| Source | Used for | License |
|---|---|---|
| [Node.js](https://nodejs.org/api/) | Node | MIT |
| [nodejs/Release](https://github.com/nodejs/Release) | End of life | None found: a date |
| [TypeScript](https://devblogs.microsoft.com/typescript/) | TypeScript | Microsoft's terms; CC BY 4.0 |
| [ESLint](https://eslint.org/blog/) | ESLint | Apache-2.0 |
| [typescript-eslint](https://typescript-eslint.io/), [Biome](https://biomejs.dev/) | Lint rules | MIT |
| [Oxc](https://oxc.rs/blog/) | oxlint | None found |
| [MDN](https://developer.mozilla.org/) | Promises, `fetch` | CC BY-SA 2.5+, Mozilla Contributors |
