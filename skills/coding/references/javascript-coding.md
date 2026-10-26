# JavaScript and TypeScript coding

Read this for writing, reviewing or fixing TypeScript or JavaScript, mostly on Node.js: tsconfig
strictness, ES modules, which Node features to rely on, the built-ins that replace packages, lint
and format, promise mistakes, and the injection, prototype pollution, path traversal and ReDoS
bugs that are particular to JavaScript.

HTML, CSS and browser DOM security are the html-coding module's. Test design is the planned
testing skill's. Which packages to trust, lockfiles and install settings are the planned
supply-chain-security module's, in the security skill, and the project-bootstrap-and-audit
standard's, whose *Language toolchains* also names the Node line and the linter. Frameworks such
as React aren't covered.

## Contents

- [Rules](#rules)
- [Mistakes](#mistakes)
- [Audit](#audit)
- [Why](#why)
- [Facts](#facts)
- [Sources](#sources)

## Rules

1. **Type-check everything with TypeScript in strict mode,** and run `tsc` in CI. Use `unknown`
   at the edges, not `any`.
2. **Write ES modules:** `"type": "module"`, `node:` specifiers, and full file extensions.
3. **Run on a Node line in LTS, and use its built-ins before a package:** `fetch`, `node:test`,
   `--env-file`, `util.parseArgs`, and type stripping for TypeScript.
4. **Every promise is awaited, returned, or handled,** and a type-aware lint rule checks it.
5. **One lint and format setup, run in CI,** chosen by the standard. ESLint takes only its flat
   config.
6. **Never build code or a shell command from a string.** No `eval` or `new Function`, and
   `execFile` or `spawn` with an argument array and no shell.
7. **Treat keys from input as hostile.** Look them up in a `Map`, or with `Object.hasOwn`, and
   never deep-merge input into an object.
8. **Bound what input can reach:** resolve a path and check it stays inside its root, and keep
   regular expressions that see input free of nested quantifiers.

### Types and `tsconfig.json`

- **Strict mode** is the default from TypeScript 6.0 (fact `js-ts6-defaults`); write it anyway,
  for older compilers. Add `noUncheckedIndexedAccess`, which `strict` doesn't include (fact
  `js-ts-unchecked-index`).
- **`"types": ["node"]`.** TypeScript 6.0 stopped loading every `@types` package by default, so
  `process` and `node:fs` go missing without it (fact `js-ts6-defaults`).
- **No deprecated options.** `moduleResolution` `node` (or `node10`), `baseUrl` and `target`
  `es5` are deprecated in 6.0 (fact `js-ts6-deprecations`), and errors in 7.0 (fact
  `js-ts7-errors`). Use `nodenext` when Node runs the code, and `bundler` when a bundler does.
- **A config for code that Node runs directly,** following Node's own recommendation (fact
  `js-strip-types`) with the strict checks added:

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

- **`"type": "module"` in every `package.json`** (fact `js-type-field`).
- **Relative imports carry their extension,** `./http.ts`, never `./http` (fact
  `js-esm-extensions`), and built-ins the `node:` prefix.
- **`import.meta.dirname` and `import.meta.filename`** replace `__dirname` and `__filename`,
  which ES modules don't have (fact `js-esm-dirname`).
- **CommonJS code can `require()` an ES module** that has no top-level `await` (fact
  `js-require-esm`), so a library can ship ES modules only.

### Node versions and built-ins

The standard's *Language toolchains* names the Node line for new work. Node's own advice is to
run production on LTS lines only (fact `js-node-lts-only`). Set `engines` to the lowest version
the code needs, and test on it. In the example, 24.12 is the first Node 24 release with stable
type stripping (fact `js-strip-types`).

| Instead of | Use | Since |
|---|---|---|
| `ts-node`, or a build step to run TypeScript | Node's type stripping (`node src/main.ts`) | Fact `js-strip-types` |
| `node-fetch`, `axios` for plain requests | Global `fetch`, with `AbortSignal.timeout` | Fact `js-fetch` |
| `dotenv` | `node --env-file=.env` | Fact `js-env-file` |
| `minimist`, `yargs` for a small CLI | `util.parseArgs` | Fact `js-parseargs` |
| A test framework for unit tests | `node:test` and `node:assert/strict` | Fact `js-node-test` |

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

- **Type stripping runs erasable syntax only** (fact `js-strip-types`). Enums, namespaces with
  values and parameter properties throw, so set `erasableSyntaxOnly`. It doesn't type-check and
  ignores `tsconfig.json`, so keep `tsc` in CI, and use subpath imports (`#lib/*`), not `paths`.
  Type-only imports need `import type`, which `verbatimModuleSyntax` enforces. Node won't strip
  types under `node_modules`, so a package publishes JavaScript.
- **`--env-file` doesn't override the environment:** a variable already set wins (fact
  `js-env-file`).
- **`fetch` resolves on HTTP errors.** Check `response.ok` (fact `js-fetch-status`), and give
  every request a timeout:

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

- **A promise nobody handles ends the process.** Node raises an unhandled rejection as an
  uncaught exception by default (fact `js-unhandled-rejections`). `await` it, `return` it, or
  attach a handler; mark a deliberate fire-and-forget with `void` and a `.catch`.
- **Don't pass an `async` callback to `forEach`.** It doesn't wait (fact `js-foreach-async`). Use
  `for...of` with `await` for steps in order, or `Promise.all` over `map` for work at once.
- **`Promise.all` rejects on the first failure** (fact `js-promise-all`), and the other work
  keeps running. Use `Promise.allSettled` when every result is needed, failures included.
- **`return await` inside `try`.** Without the `await`, a rejection skips the `catch` (fact
  `js-return-await`).
- **Lint for floating promises:** typescript-eslint's `no-floating-promises`, oxlint's
  `typescript/no-floating-promises`, or Biome's `noFloatingPromises`. Each needs type information
  (facts `js-floating-tseslint`, `js-oxlint-type-aware`, `js-floating-biome`).

### Lint and format

The standard's *Language toolchains* picks the tools: Biome for a new project, ESLint with
Prettier where plugins already exist. This is what each choice means for the checks above.

- **ESLint 10 reads only flat config** (`eslint.config.js`, or `.mjs`, `.cjs`, `.ts`). It
  ignores `.eslintrc.*` and `.eslintignore`, and reports `/* eslint-env */` comments as errors
  (fact `js-eslint10-eslintrc`). ESLint 9 is past its end of life (fact `js-eslint9-eol`).
- **TypeScript 7 and typed lint rules.** TypeScript 7.0 ships no compiler API, and
  typescript-eslint supports TypeScript below 6.1 (facts `js-ts7-api`, `js-tseslint-ts-range`).
  A project on 7.0 that keeps typescript-eslint installs 6.0 beside it, through the
  `@typescript/typescript6` alias Microsoft documents. oxlint's type-aware engine builds on
  TypeScript 7 (fact `js-oxlint-type-aware`).

### Security

- **No `eval`, `new Function`, or string `setTimeout`.** Each runs text as code with the
  caller's rights (fact `js-eval`). Parse data with `JSON.parse`, and pick behavior from a
  lookup table.
- **No shell.** `exec` and `execSync` run a shell, and Node's docs say never to give them
  unsanitized input (fact `js-exec-shell`). `spawn` or `execFile` with `shell: true` and an
  argument array doesn't escape the arguments (fact `js-dep0190`). Pass an array, and put
  `--end-of-options` or `--` before input that could look like an option:

```typescript
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export async function showCommit(ref: string): Promise<string> {
  const { stdout } = await execFileAsync("git", ["show", "--stat", "--end-of-options", ref]);
  return stdout;
}
```

- **Prototype pollution.** A key such as `__proto__` or `constructor` in parsed input, merged
  into an object, changes every object in the process (fact `js-proto-node`). Use a `Map` or
  `Set` for keyed data (fact `js-proto-owasp`), `Object.create(null)` where it must be an
  object, and `Object.hasOwn(handlers, name)` before `handlers[name]` (fact `js-hasown`).
  Validate request bodies against a schema, and don't deep-merge them.
  `node --disable-proto=delete` removes `__proto__` as a second layer (fact `js-disable-proto`).
- **Path traversal.** Resolve the path, then check that it's still under its root. Where the
  tree can hold symbolic links, resolve both with `fs.realpath` first (fact `js-cwe22`):

```typescript
import path from "node:path";

export function resolveInside(root: string, untrusted: string): string {
  const base = path.resolve(root);
  const target = path.resolve(base, untrusted);
  if (target !== base && !target.startsWith(base + path.sep)) {
    throw new Error(`Path escapes ${base}: ${untrusted}`);
  }
  return target;
}
```

- **SQL takes parameters.** Pass values through the driver's placeholders, such as
  `db.prepare("SELECT * FROM t WHERE id = ?").get(id)`, never a template string with input in
  it (fact `js-sql-params`). Pick table and column names from a fixed set.
- **ReDoS.** One slow regular expression blocks every request on the event loop. Avoid nested
  quantifiers such as `(a+)*`, alternatives that overlap, and backreferences on input; use
  `includes` or `indexOf` for a plain substring, and cap input length first (fact `js-redos`).

## Mistakes

- **`.eslintrc.json`, `/* eslint-env node */`, or `"moduleResolution": "node"`,** copied from
  old examples. ESLint 10 and TypeScript 7.0 reject them (facts `js-eslint10-eslintrc`,
  `js-ts7-errors`).
- **`Cannot find name 'process'` after upgrading TypeScript.** Add `"types": ["node"]` (fact
  `js-ts6-defaults`), rather than `any` or a `declare`.
- **`require`, `module.exports` or `__dirname` in an ES module,** which throw. Use `import`,
  `export` and `import.meta.dirname` (fact `js-esm-dirname`).
- **Enums, `namespace` with values, or parameter properties in code that Node runs,** which fail
  under type stripping. Use a union of string literals or an object `as const`.
- **`items.forEach(async (item) => { await save(item); })`,** which returns before any save ends
  (fact `js-foreach-async`). Use `for...of`, or `Promise.all(items.map(save))`.
- **A call to an `async` function with no `await`,** often a logger or a cache write. A
  rejection there ends the process (fact `js-unhandled-rejections`).
- **`` exec(`convert ${file} out.png`) ``,** which runs a shell on a file name. Use `execFile`
  with an array (fact `js-exec-shell`).
- **`` db.query(`SELECT … WHERE name = '${name}'`) ``,** which lets the input rewrite the query.
  Pass it as a parameter (fact `js-sql-params`).
- **`obj[key]` with a key from input,** which finds `toString` and `constructor` on every plain
  object. Check `Object.hasOwn` first, or use a `Map` (fact `js-hasown`).
- **`as User` on parsed JSON or a caught error,** which tells the compiler a guess. Type it
  `unknown`, then narrow it or validate it against a schema.
- **Targeting Node 20 or older because an example does.** Node 20 reached its end of life on
  2026-04-30 (fact `js-node20-eol`).

## Audit

Severity uses the standard's status words: `BLOCKER`, `DRIFT`, `GAP`, `OVER`, `MIRROR`,
`UNVERIFIABLE-HERE`, `OK` and `N/A`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Strict type-checking | `"strict": false`, no `tsc` step in CI, or `any` and `as` at input boundaries | `GAP` | Turn `strict` on, add `noUncheckedIndexedAccess`, run `tsc` in CI |
| Options TypeScript 7 removes | `moduleResolution` `node` or `node10`, `baseUrl`, `target` `es5`, `ignoreDeprecations` | `DRIFT` | Facts `js-ts6-deprecations`, `js-ts7-errors` |
| Module type | A `package.json` without `"type"`, or `.js` files mixing `require` and `import` | `GAP` | Set `"type": "module"` (fact `js-type-field`) |
| Node line | `engines`, `.nvmrc`, or CI's Node version on a line past its end of life | `GAP`: no security fixes | Move to the line the standard's *Language toolchains* names (fact `js-node20-eol`) |
| Type stripping | Node runs `.ts` files, and `erasableSyntaxOnly` or `verbatimModuleSyntax` is off, or `paths` is used | `DRIFT` | The config under *Types*, and subpath imports (fact `js-strip-types`) |
| Packages the runtime replaces | `dotenv`, `node-fetch`, `minimist`, `ts-node` in `dependencies` | `OVER` | The built-in (facts `js-env-file`, `js-fetch`, `js-parseargs`, `js-strip-types`) |
| Floating promises | No type-aware rule for them in the lint config, or `forEach(async` in the code | `GAP` | Facts `js-floating-tseslint`, `js-oxlint-type-aware`, `js-floating-biome` |
| Lint config ESLint still reads | `.eslintrc.*`, `.eslintignore` or `eslint-env` with ESLint 10 | `DRIFT` | Move to `eslint.config.js` (fact `js-eslint10-eslintrc`) |
| Typed linting on TypeScript 7 | typescript-eslint installed beside `typescript` 7 with no 6.0 alias | `DRIFT` | Facts `js-ts7-api`, `js-tseslint-ts-range` |
| Code from strings | `eval(`, `new Function(`, `setTimeout("` reachable from input | `BLOCKER` | Parse data; use a lookup table (fact `js-eval`) |
| Shell commands | `exec(`, `execSync(`, or `shell: true` with input in the command | `BLOCKER` where input reaches it, else `GAP` | `execFile` or `spawn` with an array (facts `js-exec-shell`, `js-dep0190`) |
| Prototype pollution | Deep merges or `Object.assign` of parsed input; `obj[key]` lookups with input keys | `BLOCKER` where request input reaches it, else `GAP` | `Map`, `Object.hasOwn`, schema validation (facts `js-proto-node`, `js-hasown`) |
| Path traversal | `path.join` or `path.resolve` on input with no containment check | `BLOCKER` | `resolveInside` above (fact `js-cwe22`) |
| SQL from strings | Template strings or `+` building a query passed to a database call | `BLOCKER` where input reaches it, else `GAP` | Placeholders (fact `js-sql-params`) |
| ReDoS | Regular expressions with nested quantifiers run on input | `GAP` | Rewrite the pattern, cap the input length (fact `js-redos`) |

## Why

### Strict TypeScript

- **The advice:** TypeScript in strict mode, with `noUncheckedIndexedAccess`, checked in CI.
- **The reason:** without `strict`, `null` and `undefined` pass unchecked and untyped parameters
  become `any`. Without `noUncheckedIndexedAccess`, a lookup that may miss is typed as present
  (fact `js-ts-unchecked-index`). Both end as a `TypeError` at runtime.
- **What others do, and why:** TypeScript made `strict` the default in 6.0 (fact
  `js-ts6-defaults`). Some projects keep JavaScript with JSDoc types, checked by `tsc` with
  `checkJs`, to avoid a build step.
- **What it costs:** annotations and narrowing, and a migration for old code, file by file.
- **When to choose differently:** a short script that never grows can stay plain JavaScript.

### ES modules

- **The advice:** ES modules, the `"type"` field stated, and extensions on every relative import.
- **The reason:** without the field, Node guesses each file's type from its syntax, which costs
  time and would change with Node's default (fact `js-type-field`). ES modules are also the
  format browsers run.
- **What others do, and why:** many libraries still publish both formats. Now that CommonJS can
  `require()` ES modules (fact `js-require-esm`), one format is enough for most.
- **What it costs:** `__dirname` and `require.resolve` need their ES module forms, and a tool
  that only speaks CommonJS has to go.
- **When to choose differently:** a library whose users run Node lines without `require(esm)`
  keeps a CommonJS build.

### Built-ins before packages

- **The advice:** the runtime's `fetch`, `node:test`, `--env-file`, `util.parseArgs` and type
  stripping, before a package that does the same.
- **The reason:** each package is code to review, update and trust, and a way in for a
  compromised release. A built-in ships with the runtime, and gets its security releases.
- **What others do, and why:** larger projects keep a test framework, an HTTP client or a CLI
  framework for what the built-ins lack, such as snapshots or subcommands.
- **What it costs:** the built-ins do less: type stripping runs no enums (fact `js-strip-types`),
  and `util.parseArgs` writes no help text.
- **When to choose differently:** when a built-in lacks something the project needs.

### Promises

- **The advice:** every promise awaited, returned or handled, and a type-aware lint rule to
  prove it.
- **The reason:** a floating promise's rejection ends the process (fact
  `js-unhandled-rejections`), and only on the failure path, which tests rarely take.
- **What others do, and why:** typescript-eslint's rule is the one the others follow. oxlint's
  type-aware engine now covers 59 of its 61 typed rules (fact `js-oxlint-type-aware`), and
  Biome's rule is still in its experimental group (fact `js-floating-biome`).
- **What it costs:** type-aware linting is slower, since it builds the program's types (fact
  `js-floating-tseslint`).
- **When to choose differently:** untyped JavaScript gets no type-aware rules; review is what's
  left.

### No shell, no `eval`

- **The advice:** run programs with an argument array and no shell, and never run text as code.
- **The reason:** a shell reads `;` and `$()` in a file name as commands (facts
  `js-exec-shell`, `js-dep0190`), and `eval` runs whatever reaches it (fact `js-eval`).
- **What it costs:** pipes and globs are written in JavaScript, or as separate processes.
- **When to choose differently:** a constant command with no input in it is safe with `exec`.

### Keys, paths and patterns from input

- **The advice:** `Map` and `Object.hasOwn` for keys, a containment check for paths, and simple
  regular expressions with a length cap.
- **The reason:** a plain object inherits keys from `Object.prototype`, so input can reach them
  or change them for every object (fact `js-proto-node`). `../` in a file name walks out of a
  directory. Node runs every request's JavaScript on one event loop, so one slow match stalls
  the rest (fact `js-redos`).
- **What others do, and why:** Node's guide and OWASP add frozen prototypes and
  `--disable-proto=delete` (facts `js-proto-node`, `js-disable-proto`), as defense in depth only
  (fact `js-proto-owasp`).
- **What it costs:** a `Map` needs converting for `JSON.stringify`.
- **When to choose differently:** objects built only from the program's own constants can stay
  plain objects.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked 2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `js-node-lts-only` | Node's own advice is to run production on Active LTS or Maintenance LTS lines | [Node.js releases](https://nodejs.org/en/about/previous-releases) | "Production applications should only use Active LTS or Maintenance LTS releases." | 2026-10-26 | 2027-10-26 |
| `js-node20-eol` | Node 20 reached its end of life on 2026-04-30 | [nodejs/Release schedule.json](https://raw.githubusercontent.com/nodejs/Release/main/schedule.json) | "\"end\": \"2026-04-30\"" | 2026-10-26 | 2027-10-26 |
| `js-ts6-defaults` | TypeScript 6.0 (2026-03-23) made `strict` true by default and `types` an empty list | [Announcing TypeScript 6.0](https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/) | "strict is now true by default" and "In TypeScript 6.0, the default types value will be [] (an empty array)." | 2026-10-26 | 2027-10-26 |
| `js-ts6-deprecations` | TypeScript 6.0 deprecated `moduleResolution` `node` (`node10`), `baseUrl` and `target` `es5` | [Announcing TypeScript 6.0](https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/) | "In TypeScript 6.0, --moduleResolution node (specifically, --moduleResolution node10) is deprecated." and "In TypeScript 6.0, baseUrl is deprecated" and "the target: es5 option is deprecated" | 2026-10-26 | 2027-10-26 |
| `js-ts7-errors` | TypeScript 7.0 (2026-07-08) errors on every option 6.0 deprecated | [Announcing TypeScript 7.0](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/) | "provides hard errors in the face of any flags and constructs deprecated in TypeScript 6.0" | 2026-10-26 | 2027-10-26 |
| `js-ts7-api` | TypeScript 7.0 ships no compiler API; `@typescript/typescript6` provides 6.0's beside it | [Announcing TypeScript 7.0](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/) | "While TypeScript 7.0 is here, it does not ship with an API." | 2026-10-26 | 2027-04-26 |
| `js-tseslint-ts-range` | typescript-eslint supports TypeScript from 4.8.4 to below 6.1.0 | [Dependency versions](https://typescript-eslint.io/users/dependency-versions/) | "The version range of TypeScript currently supported is" | 2026-10-26 | 2027-04-26 |
| `js-ts-unchecked-index` | `noUncheckedIndexedAccess` adds `undefined` to index lookups | [TSConfig reference](https://www.typescriptlang.org/tsconfig/) | "Turning on noUncheckedIndexedAccess will add undefined to any un-declared field in the type." | 2026-10-26 | 2027-10-26 |
| `js-strip-types` | Node's type stripping is stable from v25.2.0 and v24.12.0. It runs erasable syntax only, doesn't type-check, ignores `tsconfig.json`, needs `import type` for types, and refuses files under `node_modules` | [Modules: TypeScript](https://nodejs.org/api/typescript.html) | "Type stripping is now stable." and "no type checking is performed" and "Node.js ignores tsconfig.json files and therefore" and "the type keyword is necessary to correctly strip type imports" and "Node.js refuses to handle TypeScript files inside folders under a node_modules" | 2026-10-26 | 2027-04-26 |
| `js-type-field` | Node's docs ask every package to state its `"type"` | [Modules: Packages](https://nodejs.org/api/packages.html) | "package authors should always include the \"type\" field" | 2026-10-26 | 2027-10-26 |
| `js-esm-extensions` | ES module imports need the file extension | [Modules: ECMAScript modules](https://nodejs.org/api/esm.html) | "A file extension must be provided when using the import keyword to resolve relative or absolute specifiers." | 2026-10-26 | 2027-10-26 |
| `js-esm-dirname` | `import.meta.dirname` (from v20.11.0) replaces `__dirname` in ES modules | [Modules: ECMAScript modules](https://nodejs.org/api/esm.html) | "__filename and __dirname use cases can be replicated via import.meta.filename and import.meta.dirname." | 2026-10-26 | 2027-10-26 |
| `js-require-esm` | `require()` loads an ES module with no top-level `await`; unflagged from v22.12.0 and v20.19.0, stable from v25.4.0 | [Modules: CommonJS modules](https://nodejs.org/api/modules.html) | "The module is fully synchronous (contains no top-level await)" | 2026-10-26 | 2027-04-26 |
| `js-node-test` | `node:test` has been stable since v20.0.0 | [Test runner](https://nodejs.org/api/test.html) | "The test runner is now stable." | 2026-10-26 | 2027-10-26 |
| `js-fetch` | Global `fetch` has been stable since v21.0.0, and `AbortSignal.timeout` exists from v17.3.0 | [Globals](https://nodejs.org/api/globals.html) | "A browser-compatible implementation of the fetch() function." and "Returns a new AbortSignal which will be aborted in delay milliseconds." | 2026-10-26 | 2027-10-26 |
| `js-fetch-status` | `fetch` doesn't reject on an HTTP error status | [MDN: Window.fetch()](https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch) | "A fetch() promise does not reject if the server responds with HTTP status codes that indicate errors" | 2026-10-26 | 2027-10-26 |
| `js-env-file` | `--env-file` is stable from v24.10.0 and v22.21.0, and the environment wins over the file | [Command-line options](https://nodejs.org/api/cli.html) | "The --env-file flag is no longer experimental." and "the value from the environment takes precedence." | 2026-10-26 | 2027-04-26 |
| `js-parseargs` | `util.parseArgs` has been stable since v20.0.0 | [Util](https://nodejs.org/api/util.html) | "The API is no longer experimental." | 2026-10-26 | 2027-10-26 |
| `js-unhandled-rejections` | Since v15.0.0 an unhandled rejection is thrown as an uncaught exception by default | [Command-line options](https://nodejs.org/api/cli.html) | "Changed default mode to throw. Previously, a warning was emitted." | 2026-10-26 | 2027-10-26 |
| `js-foreach-async` | `forEach` doesn't wait for promises | [MDN: Array.prototype.forEach()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach) | "forEach() expects a synchronous function — it does not wait for promises." | 2026-10-26 | 2027-10-26 |
| `js-promise-all` | `Promise.all` rejects on the first rejection | [MDN: Promise.all()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all) | "It rejects when any of the input's promises rejects, with this first rejection reason." | 2026-10-26 | 2027-10-26 |
| `js-return-await` | `return await` in `try` lets the `catch` see the rejection | [typescript-eslint: return-await](https://typescript-eslint.io/rules/return-await/) | "When the return statement is in try...catch, awaiting the promise allows the promise's rejection to be caught instead of leaving the error to the caller." | 2026-10-26 | 2027-10-26 |
| `js-floating-tseslint` | typescript-eslint's `no-floating-promises` needs type information | [typescript-eslint: no-floating-promises](https://typescript-eslint.io/rules/no-floating-promises/) | "This rule requires type information to run" | 2026-10-26 | 2027-10-26 |
| `js-floating-biome` | Biome's `noFloatingPromises` is in its experimental nursery group | [Biome: noFloatingPromises](https://biomejs.dev/linter/rules/no-floating-promises/) | "This rule is part of the nursery group." | 2026-10-26 | 2027-04-26 |
| `js-oxlint-type-aware` | oxlint's type-aware engine, tsgolint v7, is stable (2026-07-22), built on TypeScript 7, with 59 of typescript-eslint's 61 typed rules | [Type-aware linting stable](https://oxc.rs/blog/2026-07-22-type-aware-linting-stable) | "This release tracks TypeScript v7.0.2 and brings tsgolint to 59 of typescript-eslint's 61 type-aware rules." | 2026-10-26 | 2027-04-26 |
| `js-eslint10-eslintrc` | ESLint 10.0.0 removed eslintrc | [ESLint v10.0.0 released](https://eslint.org/blog/2026/02/eslint-v10.0.0-released/) | "the eslintrc config system has been completely removed in ESLint v10.0.0." | 2026-10-26 | 2027-10-26 |
| `js-eslint9-eol` | ESLint 9 reached its end of life on 2026-08-06 | [ESLint version support](https://eslint.org/version-support/) | "ESLint v9.x reached end-of-life on 2026-08-06" | 2026-10-26 | 2027-10-26 |
| `js-exec-shell` | Node's docs say never to pass unsanitized input to `exec` | [Child process](https://nodejs.org/api/child_process.html) | "Never pass unsanitized user input to this function." | 2026-10-26 | 2027-10-26 |
| `js-dep0190` | Arguments passed with `shell: true` aren't escaped (DEP0190, runtime-deprecated in v24.0.0) | [Deprecated APIs](https://nodejs.org/api/deprecations.html) | "the values are not escaped, only space-separated, which can lead to shell injection." | 2026-10-26 | 2027-10-26 |
| `js-eval` | MDN: never use direct `eval()` | [MDN: eval()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval) | "Never use direct eval()!" | 2026-10-26 | 2027-10-26 |
| `js-proto-node` | Node's mitigations for prototype pollution | [Node.js security best practices](https://nodejs.org/en/learn/getting-started/security-best-practices) | "Create Objects without prototype by using Object.create(null)." and "Avoid insecure recursive merges" | 2026-10-26 | 2027-10-26 |
| `js-proto-owasp` | OWASP: use `Map` or `Set` instead of object literals | [OWASP Prototype Pollution Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html) | "Developers should use new Set() or new Map() instead of using object literals" | 2026-10-26 | 2027-10-26 |
| `js-hasown` | `Object.hasOwn` works on null-prototype objects and overridden `hasOwnProperty` | [MDN: Object.hasOwn()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwn) | "It is recommended over Object.prototype.hasOwnProperty()" | 2026-10-26 | 2027-10-26 |
| `js-disable-proto` | `--disable-proto=delete` removes `Object.prototype.__proto__` | [Command-line options](https://nodejs.org/api/cli.html) | "Disable the Object.prototype.__proto__ property." | 2026-10-26 | 2027-10-26 |
| `js-redos` | Node's guide: nested quantifiers make a regular expression vulnerable | [Don't block the event loop](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop) | "Avoid nested quantifiers like (a+)*." | 2026-10-26 | 2027-10-26 |
| `js-sql-params` | OWASP: parameterized queries for data values | [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) | "Use parameterized queries for data values" | 2026-10-26 | 2027-10-26 |
| `js-cwe22` | CWE-22: canonicalize a path before checking it | [CWE-22](https://cwe.mitre.org/data/definitions/22.html) | "produces the canonical version of the pathname" | 2026-10-26 | 2027-10-26 |

## Sources

Every rule here is written in this module's own words. Sources are quoted only briefly, with
attribution, and each quote is a dated fact above.

| Source | Used for | License |
|---|---|---|
| [Node.js API documentation](https://nodejs.org/api/) | Type stripping, modules, built-ins, flags, `child_process`, deprecations | MIT (the nodejs/node repository): facts in our own words, with short quotes |
| [Node.js website](https://nodejs.org/en/learn/) (releases, security best practices, the event loop guide) | LTS advice, prototype pollution, ReDoS | MIT (the nodejs/nodejs.org repository): facts in our own words, with short quotes |
| [nodejs/Release](https://github.com/nodejs/Release) `schedule.json` | Node 20's end of life | No license file found: a date, with a short quote |
| [TypeScript blog](https://devblogs.microsoft.com/typescript/) (6.0 and 7.0 announcements) | Defaults, deprecations, TypeScript 7's missing API | Microsoft's terms of use: facts in our own words, with short quotes |
| [TSConfig reference](https://www.typescriptlang.org/tsconfig/) | `noUncheckedIndexedAccess` | CC BY 4.0 (the microsoft/TypeScript-Website repository): a short quote, with attribution |
| [ESLint blog and version support](https://eslint.org/blog/) | eslintrc's removal, ESLint 9's end of life | Apache-2.0 (the eslint/eslint.org repository): short quotes |
| [typescript-eslint](https://typescript-eslint.io/) | Floating promises, `return await`, supported TypeScript versions | MIT: short quotes |
| [Biome](https://biomejs.dev/) | `noFloatingPromises` status | MIT (the biomejs/website repository): a short quote |
| [Oxc blog](https://oxc.rs/blog/2026-07-22-type-aware-linting-stable) | oxlint's type-aware linting | No license found for the site: a fact in our own words, with a short quote |
| [MDN Web Docs](https://developer.mozilla.org/) | `forEach`, `Promise.all`, `fetch`, `eval`, `Object.hasOwn` | Prose CC BY-SA 2.5 or later, by Mozilla Contributors: short quotes, with attribution |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | Prototype pollution, SQL parameters | CC BY-SA 4.0: a short quote, with attribution |
| [MITRE CWE-22](https://cwe.mitre.org/data/definitions/22.html) | Canonicalizing paths | CWE terms of use, copyright The MITRE Corporation: a short quote, with attribution |
