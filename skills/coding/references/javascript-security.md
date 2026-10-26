# JavaScript security

Read this for JavaScript or TypeScript on Node.js that handles untrusted input: `eval` and
`new Function`, child processes and shells, prototype pollution, path traversal, ReDoS, and SQL
parameters.

The javascript-coding module takes the rest of the language: tsconfig, ES modules, Node versions
and built-ins, type stripping, promises, and lint and format. Browser and DOM security, such as
`innerHTML` and CSP, is the web-security module's, and HTML and CSS the html-coding module's.
Which packages to trust, lockfiles and secrets are the planned supply-chain-security module's, in
the security skill, and the project-bootstrap-and-audit standard's.

## Rules

1. **Never run text as code:** no `eval`, `new Function`, or string `setTimeout`.
2. **Never build a shell command from a string:** `execFile` or `spawn` with an argument array
   and no shell.
3. **Treat keys from input as hostile.** Look them up in a `Map`, or with `Object.hasOwn`, and
   never deep-merge input into an object.
4. **Resolve a path from input and check it stays inside its root.**
5. **Keep regular expressions that see input free of nested quantifiers,** and cap the input's
   length.
6. **Pass SQL values as parameters,** never in the query's text.

### Code from strings

`eval`, `new Function` and a string passed to `setTimeout` each run text as code with the
caller's rights (fact `js-eval`). Parse data with `JSON.parse`, and pick behavior from a lookup
table.

### Shells and child processes

`exec` and `execSync` run a shell, and Node's docs say never to give them unsanitized input (fact
`js-exec-shell`). `spawn` or `execFile` with `shell: true` and an argument array doesn't escape
the arguments either (fact `js-dep0190`). Pass an array with no shell, and put `--end-of-options`
or `--` before input that could look like an option:

```typescript
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export async function showCommit(ref: string): Promise<string> {
  const { stdout } = await execFileAsync("git", ["show", "--stat", "--end-of-options", ref]);
  return stdout;
}
```

### Prototype pollution

A key such as `__proto__` or `constructor` in parsed input, merged into an object, changes every
object in the process (fact `js-proto-node`).

- Use a `Map` or `Set` for keyed data (fact `js-proto-owasp`), and `Object.create(null)` where it
  must be an object.
- Check `Object.hasOwn(handlers, name)` before `handlers[name]` (fact `js-hasown`).
- Validate request bodies against a schema, and don't deep-merge them.
- `node --disable-proto=delete` removes `__proto__`, as a second layer (fact `js-disable-proto`).

### Path traversal

Resolve the path, then check that it's still under its root. Where the tree can hold symbolic
links, resolve both with `fs.realpath` first (fact `js-cwe22`):

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

### Slow regular expressions

One slow regular expression blocks every request on the event loop. Avoid nested quantifiers
such as `(a+)*`, alternatives that overlap, and backreferences on input; use `includes` or
`indexOf` for a plain substring, and cap input length first (fact `js-redos`).

### Database queries

Pass values through the driver's placeholders, such as
`db.prepare("SELECT * FROM t WHERE id = ?").get(id)`, never a template string with input in it
(fact `js-sql-params`). Pick table and column names from a fixed set, since placeholders take
values only.

## Mistakes

- **`` exec(`convert ${file} out.png`) ``,** which runs a shell on a file name. Use `execFile`
  with an array (fact `js-exec-shell`).
- **`spawn(cmd, args, { shell: true })`, trusting the array to quote its items.** It joins them
  with spaces, unescaped (fact `js-dep0190`). Drop `shell: true`.
- **`` db.query(`SELECT … WHERE name = '${name}'`) ``,** which lets the input rewrite the query.
  Pass it as a parameter (fact `js-sql-params`).
- **`obj[key]` with a key from input,** which finds `toString` and `constructor` on every plain
  object. Check `Object.hasOwn` first, or use a `Map` (fact `js-hasown`).
- **A recursive merge of a request body into defaults or config,** which lets `__proto__` reach
  `Object.prototype` (fact `js-proto-node`). Validate the body, then copy the known fields.
- **`target.startsWith(base)` with no separator,** which lets `/srv/data-old` pass for
  `/srv/data`. Compare against `base + path.sep`, as `resolveInside` does.

## Audit

Severity uses the standard's status words: `BLOCKER`, `DRIFT`, `GAP`, `OVER`, `MIRROR`,
`UNVERIFIABLE-HERE`, `OK` and `N/A`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Code from strings | `eval(`, `new Function(`, `setTimeout("` reachable from input | `BLOCKER` | Parse data; use a lookup table (fact `js-eval`) |
| Shell commands | `exec(`, `execSync(`, or `shell: true` with input in the command | `BLOCKER` where input reaches it, else `GAP` | `execFile` or `spawn` with an array (facts `js-exec-shell`, `js-dep0190`) |
| Prototype pollution | Deep merges or `Object.assign` of parsed input; `obj[key]` lookups with input keys | `BLOCKER` where request input reaches it, else `GAP` | `Map`, `Object.hasOwn`, schema validation (facts `js-proto-node`, `js-hasown`) |
| Path traversal | `path.join` or `path.resolve` on input with no containment check | `BLOCKER` | `resolveInside` above (fact `js-cwe22`) |
| SQL from strings | Template strings or `+` building a query passed to a database call | `BLOCKER` where input reaches it, else `GAP` | Placeholders (fact `js-sql-params`) |
| ReDoS | Regular expressions with nested quantifiers run on input | `GAP` | Rewrite the pattern, cap the input length (fact `js-redos`) |

## Why

### No shell, no `eval`

- **The advice:** run programs with an argument array and no shell, and never run text as code.
- **The reason:** a shell reads `;` and `$()` in a file name as commands (facts
  `js-exec-shell`, `js-dep0190`), and `eval` runs whatever reaches it (fact `js-eval`).
- **What others do, and why:** some projects quote arguments for the shell by hand, which one
  missed character undoes.
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

### SQL parameters

- **The advice:** every value through a placeholder, and identifiers from a fixed set.
- **The reason:** input in the query's text can end the string and add its own clauses (fact
  `js-sql-params`).
- **What others do, and why:** query builders and ORMs pass values as parameters themselves, but
  their raw-query calls take text, and need the same care.
- **What it costs:** a query whose shape changes, such as a sort column, needs an allowlist.
- **When to choose differently:** never for values; a query with no input in it needs no
  parameters.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked 2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
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
| [Node.js API documentation](https://nodejs.org/api/) | `child_process`, deprecations, `--disable-proto` | MIT (the nodejs/node repository): facts in our own words, with short quotes |
| [Node.js website](https://nodejs.org/en/learn/) (security best practices, the event loop guide) | Prototype pollution, ReDoS | MIT (the nodejs/nodejs.org repository): facts in our own words, with short quotes |
| [MDN Web Docs](https://developer.mozilla.org/) | `eval`, `Object.hasOwn` | Prose CC BY-SA 2.5 or later, by Mozilla Contributors: short quotes, with attribution |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | Prototype pollution, SQL parameters | CC BY-SA 4.0: short quotes, with attribution |
| [MITRE CWE-22](https://cwe.mitre.org/data/definitions/22.html) | Canonicalizing paths | CWE terms of use, copyright The MITRE Corporation: a short quote, with attribution |
