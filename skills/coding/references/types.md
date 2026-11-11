# Types

Read this for adding types to an untyped codebase, how strict a type checker should be and
what each strict mode turns on, `any`, `dynamic`, casts and ignore comments, typing data from
outside, and type checkers in CI.

It holds what every typed language shares. Each language's setup, versions and syntax are its
language module's: `python-coding` for mypy, Pyrefly and ty, `javascript-coding` for
`tsconfig`, `csharp-coding` for nullable and warnings as errors. What to accept from outside,
and escaping it on the way out, is `input-handling`'s; a configuration file's schema is
`configuration`'s.

## Rules

1. **Type every new function's parameters and return, and check them in CI** with the checker
   at its strict setting. The check is a gate that fails the build, never an editor hint.
2. **Type an existing codebase gradually, behind a ratchet.** The checker runs in CI from the
   first day over what it covers; new and finished modules run strict; the list of exempt ones
   only shrinks.
3. **Know what strict turns on, and pin the checker.** Strict is a family of checks that grows
   with releases, so an upgrade is a change of its own.
4. **Treat `any`, `Any`, `dynamic`, casts and ignore comments as escape hatches.** Each is as
   narrow as it can be, names its error code and says why, and a lint rule counts them.
5. **Types don't check data at run time: parse it at the boundary, then type what was parsed.**
   Outside data enters as `unknown` or `object`, and a parser returns the typed value or fails.

### Strict modes

| Language | Strict setting | Add, or know |
|---|---|---|
| TypeScript | `"strict": true`, a family that grows (fact `types-ts-strict`) | `noUncheckedIndexedAccess` is outside it (fact `js-ts-unchecked-index`) |
| mypy | `strict = true`, whose flags may change (fact `py-mypy-untyped`) | It skips unannotated bodies |
| pyright | `"typeCheckingMode": "strict"`, or `strict` paths (fact `types-pyright-modes`) | The default is `standard` |
| C# | `<Nullable>enable</Nullable>`, nullable warnings as errors (fact `cs-warnaserror`) | Compile-time only (fact `types-cs-nullable`) |

ty is in beta (fact `py-ty-beta`): run it beside a stable checker, such as mypy or Pyrefly
(fact `py-pyrefly-stable`), never alone.

### The ratchet

Make strict the default and list the exceptions, so a new file is strict unasked. In mypy,
exempt the legacy packages, and delete each line once that package passes (fact
`types-mypy-existing`):

```toml
[tool.mypy]
strict = true

[[tool.mypy.overrides]]
module = ["billing.legacy.*", "reports.*"]
ignore_errors = true
```

In C#, set `<Nullable>enable</Nullable>` and put `#nullable disable` atop each file not yet
migrated (fact `types-cs-nullable-migrate`). In TypeScript, turn the family on and switch off
a flag still failing until it passes (fact `types-ts-strict`). Annotate the most imported
modules first: their types reach every caller.

### At the boundary

JSON, environment variables, files, requests, database rows and untyped libraries hand over
values no checker has seen. Decode to `unknown` or `object`, and parse:

```python
from dataclasses import dataclass


class OrderError(ValueError):
    """Decoded data that isn't an order."""


@dataclass(frozen=True)
class Order:
    id: int
    email: str


def parse_order(raw: object) -> Order:
    if not isinstance(raw, dict):
        raise OrderError(f"order: expected an object, got {type(raw).__name__}")
    order_id, email = raw.get("id"), raw.get("email")
    if not isinstance(order_id, int) or isinstance(order_id, bool):
        raise OrderError(f"order.id: expected an integer, got {order_id!r}")
    if not isinstance(email, str):
        raise OrderError(f"order.email: expected text, got {email!r}")
    return Order(order_id, email)
```

A schema library does the same in less code: pydantic (fact `types-pydantic-output`), or Zod,
whose schema gives the type (fact `types-zod-infer`). C#'s `System.Text.Json` ignores nullable
annotations unless `RespectNullableAnnotations` is set, and lets a missing property through
even then (fact `types-stj-nullable`): mark it `required` too.

## Mistakes

- **A cast on decoded data:** `JSON.parse(body) as User`, `cast(User, json.loads(body))`,
  `Deserialize<User>(json)!`. Each is a claim nothing checks (facts `types-ts-assertion`,
  `types-py-runtime`). Parse instead.
- **Widening to `any` to make an error go away.** `Any` spreads to everything it touches (fact
  `types-mypy-any`). Narrow the value, or type it `unknown` or `object` (fact
  `types-ts-unknown`).
- **A blanket ignore:** `# type: ignore` with no code, `@ts-ignore`, `@ts-nocheck`, a file-wide
  `#pragma warning disable`. Name the code, give the reason, and let the checker report it once
  it's unused (facts `types-mypy-ignore`, `types-tseslint-any`).
- **A schema and a hand-written type for the same data,** which drift. Derive one from the other.
- **Upgrading the checker in the same change as the code.** Its new errors hide among the
  change's own.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Type check in CI | No checker step, or one allowed to fail | `GAP` | A required check, by the standard's dimension 6 |
| Strict setting | Strict off project-wide, or no list of exemptions | `GAP` | The ratchet |
| Exemption list | Lines added to it since the last release | `DRIFT` | Fix that code, remove them |
| Casts at the boundary | `as`, `cast(`, `!` or `<T>` on parsed JSON, `os.environ`, request bodies | `GAP` | A parser or schema |
| Blanket ignores | `type: ignore` without `[code]`, `@ts-ignore`, `@ts-nocheck`, `#nullable disable` in new files | `DRIFT` | Narrow, with a reason |
| Explicit `any` | `: any`, `Any` in signatures, `dynamic`, and no lint rule on them | `GAP` | `no-unsafe-*`, `ANN401` (facts `types-tseslint-any`, `types-ruff-any`) |
| Checker version | The checker unpinned, or upgraded in a feature change | `DRIFT` | Pin it by the standard's *Language toolchains* |
| Sole gate in beta | ty, or another pre-1.0 checker, alone | `DRIFT` | Add a stable checker |

## Why

### Gradual typing with a ratchet

- **The advice:** run the checker in CI at once over a small subset, strict where finished.
- **The reason:** a checker that waits for the whole codebase never ships, and one outside CI
  lets new errors in. mypy's guide and Microsoft's nullable guide both work this way (facts
  `types-mypy-existing`, `types-cs-nullable-migrate`).
- **What others do, and why:** some turn everything on and suppress each existing error in a
  baseline file: one setting everywhere, at the price of a long suppression list.
- **What it costs:** two settings for a while, and a list someone keeps shrinking.
- **When to choose differently:** a small codebase goes strict in one change.

### Strict, pinned

- **The advice:** the strict family, stated explicitly, at a pinned checker version.
- **The reason:** lenient modes let through a `None` where a value is needed, and implicit `any`. Strict grows with releases (facts `types-ts-strict`,
  `py-mypy-untyped`), so an unpinned checker fails a build no change caused.
- **What others do, and why:** pyright defaults to `standard` (fact `types-pyright-modes`), for
  fewer false alarms on code it can't fully infer.
- **What it costs:** more annotations, and narrowing where a lenient mode guesses.
- **When to choose differently:** generated code, or a thin wrapper over an untyped library,
  runs lenient by path.

### Escape hatches, counted

- **The advice:** `unknown` or `object` over `any`; a cast or ignore names its code and reason.
- **The reason:** `any` turns the checker off for every value it reaches (fact
  `types-mypy-any`), and a blanket ignore hides the next error on its line too (fact
  `types-ruff-any`). A lint rule shows each one in review.
- **What others do, and why:** typescript-eslint allows `@ts-expect-error` with a description
  and reports `@ts-ignore` (fact `types-tseslint-any`): the former fails once its error is gone.
- **What it costs:** a type guard where a cast was one word.
- **When to choose differently:** a test that builds a wrong value on purpose may cast, with a
  comment.

### Parse at the boundary

- **The advice:** decode to `unknown`, parse into a type, and pass only the typed value on.
- **The reason:** annotations and casts vanish at run time (facts `types-py-runtime`,
  `types-ts-assertion`, `types-cs-nullable`), so a wrong shape travels on until something far
  away fails. A parser fails at the edge, naming the field. Alexis King's "Parse, don't
  validate" puts it as getting data "into the most precise representation you need as quickly
  as you can".
- **What others do, and why:** many check with a boolean function and keep the untyped
  value, which every later reader then has to trust.
- **What it costs:** a schema per input, and a dependency where the platform has none.
- **When to choose differently:** a value forwarded untouched, such as an opaque ID, needs its
  type checked, not its contents.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked 2026-11-11.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `types-ts-strict` | `strict` turns on a family; later releases add to it | [TSConfig](https://www.typescriptlang.org/tsconfig/) | "equivalent to enabling all of the strict mode family options" and "Future versions of TypeScript may introduce additional stricter checking" | 2026-11-11 | 2027-02-11 |
| `types-ts-unknown` | `unknown` is the checked `any` | [TypeScript 3.0](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-0.html) | "unknown is the type-safe counterpart of any" | 2026-11-11 | 2027-05-11 |
| `types-ts-assertion` | An `as` assertion has no run-time check | [Everyday types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) | "there is no runtime checking associated with a type assertion" | 2026-11-11 | 2027-05-11 |
| `types-mypy-existing` | mypy: a subset first, CI early, finished modules strict | [Existing codebase](https://mypy.readthedocs.io/en/stable/existing_code.html) | "get mypy to run successfully only on this subset at first" and "run mypy as part of your Continuous Integration (CI) system" and "enable disallow_untyped_defs for modules which you've completed annotations for" | 2026-11-11 | 2027-05-11 |
| `types-mypy-any` | `Any` spreads; `object` is checked | [Dynamic typing](https://mypy.readthedocs.io/en/stable/dynamic_typing.html) | "Any types may propagate through your program, making type checking less effective" and "only operations valid for all types are accepted" | 2026-11-11 | 2027-05-11 |
| `types-mypy-ignore` | mypy: ignores need a code; unused ones fail | [Optional error codes](https://mypy.readthedocs.io/en/stable/error_code_list2.html) | "Warn when a # type: ignore comment does not specify any error codes" and "mypy generates an error if you don't use a # type: ignore comment" | 2026-11-11 | 2027-02-11 |
| `types-ruff-any` | Ruff's `ANN401` flags `Any`; `PGH003`, blanket ignores | [ANN401](https://docs.astral.sh/ruff/rules/any-type/), [PGH003](https://docs.astral.sh/ruff/rules/blanket-type-ignore/) | "annotated with a more specific type than Any" and "Suppressing all warnings can hide issues in the code" | 2026-11-11 | 2027-02-11 |
| `types-pyright-modes` | pyright's modes; `standard` by default; strict by path | [Configuration](https://raw.githubusercontent.com/microsoft/pyright/main/docs/configuration.md) | "Specifies the default rule set to use" and "In strict mode, most type-checking rules are enabled" | 2026-11-11 | 2027-02-11 |
| `types-tseslint-any` | typescript-eslint flags `any` and unexplained ignores; TypeScript reports an unneeded `@ts-expect-error` | [no-unsafe-assignment](https://typescript-eslint.io/rules/no-unsafe-assignment/), [ban-ts-comment](https://typescript-eslint.io/rules/ban-ts-comment/), [TypeScript 3.9](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-9.html) | "Disallow assigning a value with type any to variables and properties" and "@ts-expect-error is allowed when it includes a description. @ts-ignore and @ts-nocheck are reported" and "if there's no error, TypeScript will report that" | 2026-11-11 | 2027-02-11 |
| `types-py-runtime` | Python enforces no annotation; `cast` checks nothing | [typing](https://docs.python.org/3/library/typing.html) | "The Python runtime does not enforce function and variable type annotations" and "at runtime we intentionally don't check anything" | 2026-11-11 | 2027-05-11 |
| `types-cs-nullable` | Nullable is compile-time only; `!` overrides it | [Nullable reference types](https://learn.microsoft.com/dotnet/csharp/nullable-references) | "Nullable reference types are entirely a compile-time feature" and "declares that an expression is not-null, even when the analysis says otherwise" | 2026-11-11 | 2027-05-11 |
| `types-cs-nullable-migrate` | Enable by default, disable unmigrated files | [Migration strategies](https://learn.microsoft.com/dotnet/csharp/nullable-migration-strategies) | "add #nullable disable at the top of every file you haven't migrated yet" and "the migration backlog can only shrink" | 2026-11-11 | 2027-05-11 |
| `types-stj-nullable` | `RespectNullableAnnotations`: opt-in from .NET 9; missing values pass | [Nullable annotations](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/nullable-annotations) | "implemented as an opt-in flag in .NET 9" and "doesn't extend enforcement to unspecified JSON values" | 2026-11-11 | 2027-02-11 |
| `types-pydantic-output` | pydantic guarantees its output's types | [Models](https://docs.pydantic.dev/latest/concepts/models/) | "Pydantic guarantees the types and constraints of the output, not the input data" | 2026-11-11 | 2027-02-11 |
| `types-zod-infer` | Zod gives the static type from the schema | [Basics](https://zod.dev/basics) | "Zod infers a static type from your schema definitions" | 2026-11-11 | 2027-02-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [TypeScript documentation](https://www.typescriptlang.org/docs/) | Strict, `unknown`, assertions | CC BY 4.0: short quotes, credited, our own words otherwise |
| [Microsoft Learn, .NET](https://learn.microsoft.com/dotnet/) | Nullable, its migration, `System.Text.Json` | CC BY 4.0: short quotes, credited, our own words otherwise |
| [Python documentation](https://docs.python.org/3/library/typing.html) | Annotations at run time, `cast` | PSF License 2.0: short quotes |
| [mypy](https://mypy.readthedocs.io/), [pyright](https://github.com/microsoft/pyright/blob/main/docs/configuration.md), [Ruff](https://docs.astral.sh/ruff/rules/), [typescript-eslint](https://typescript-eslint.io/rules/), [pydantic](https://docs.pydantic.dev/), [Zod](https://zod.dev/) | Each tool's settings and behavior | MIT: short quotes |
| [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/), Alexis King | Parsing at the boundary | All rights reserved: one short quote, our own words otherwise |
