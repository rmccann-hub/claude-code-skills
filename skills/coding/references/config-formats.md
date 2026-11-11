# Config formats

Read this for choosing between YAML, JSON, TOML and XML, YAML that turned `NO` into false or
`3.10` into 3.1, loading YAML safely, duplicate keys, big numbers in JSON, JSON Schema, TOML
versions, untrusted XML, linting these files, and secrets in them.

It covers the file formats. How a program takes its settings is `configuration`. Each
language's loader rules are in its security module, such as `python-security`, and validating
outside input in general is `input-handling`.

## Rules

1. **Use the format the tool already reads; for a new file, choose by who writes it,** by the
   table below.
2. **Quote every YAML value that isn't plainly a string.** YAML 1.1 reads `no`, `on` and `y` as
   booleans (fact `cfmt-yaml-11-bool`), 1.2 doesn't (fact `cfmt-yaml-12`), and PyYAML is a 1.1
   parser (fact `cfmt-pyyaml`).
3. **Load YAML with the safe loader, and decide whether a file holds one document or many.**
   Never `yaml.load` on outside text (fact `py-yaml-load`). Cap the size of untrusted YAML and
   JSON before parsing (fact `cfmt-yaml-bomb`).
4. **Reject duplicate keys.** YAML and TOML forbid them and JSON says they should be unique, but
   common parsers keep the last one silently (facts `cfmt-yaml-12`, `cfmt-toml`,
   `cfmt-json-rfc`, `cfmt-py-json`).
5. **Send JSON integers past 2^53, IDs and money as strings** (fact `cfmt-json-rfc`).
6. **Validate config against a schema where one exists,** in CI: JSON Schema works for YAML and
   TOML data too (fact `cfmt-json-schema`).
7. **Write TOML 1.0 syntax unless every reader parses 1.1** (facts `cfmt-toml`, `cfmt-tomllib`).
8. **Parse untrusted XML with DTDs and XInclude off** (fact `cfmt-xxe`). In Python, defusedxml
   with `forbid_dtd=True`, and a current Expat (fact `cfmt-py-expat`).
9. **Lint each format in CI so that the rules that matter fail the build** (fact
   `cfmt-yamllint`).
10. **Comments say why a value is what it is; secrets never go in the file.** Commit an example
    file with `CHANGEME`, by the standard's dimension 7.

### Choosing a format

| Format | Choose it for | Its costs |
|---|---|---|
| JSON | Data between programs, API bodies, generated files | No comments; big numbers lose precision |
| TOML | Hand-edited settings: `pyproject.toml`, `Cargo.toml` | No null (fact `cfmt-toml`); deep nesting reads badly |
| YAML | Files a tool requires: CI workflows, Kubernetes, Compose | Implicit types, two versions in use |
| XML | SVG, MSBuild, Maven, Office files, SAML, feeds; text mixed with markup | Verbose; DTD and entity attacks |

### YAML values that change type

PyYAML reads the first document below as `False`, `True`, `1342`, `3.1` and `493`. The second
keeps each value as written, under YAML 1.1 or 1.2.

```yaml
country: NO
enabled: on
ports: 22:22
python: 3.10
mode: 0755
---
country: "NO"
enabled: true
ports: "22:22"
python: "3.10"
mode: "0755"
```

`yaml.safe_load` refuses that file, which holds two documents; `yaml.safe_load_all` reads each
(fact `cfmt-pyyaml`). ruamel.yaml and js-yaml parse 1.2 (fact `cfmt-yaml12-parsers`), but the
next tool may not. Quoting holds for every reader.

### Duplicate keys

Python's `json` keeps the last repeated key (fact `cfmt-py-json`). Refuse repeats in a file
that configures something:

```python
import json


def unique_keys(pairs):
    keys = [key for key, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError(f"duplicate keys in {keys}")
    return dict(pairs)


with open(path, encoding="utf-8") as handle:
    settings = json.load(handle, object_pairs_hook=unique_keys)
```

For YAML, yamllint's `key-duplicates` rule catches them.

### Lint and validate in CI

yamllint's defaults only warn on 1.1 booleans, skip octal values, and exit 1 only on errors
(fact `cfmt-yamllint`). This `.yamllint.yaml` makes both errors, and `check-keys: false` lets a
GitHub Actions workflow keep its `on:` key:

```yaml
extends: default
rules:
  truthy:
    level: error
    check-keys: false
  octal-values: enable
```

check-jsonschema checks JSON, YAML and TOML against a schema, its own or SchemaStore's (fact
`cfmt-json-schema`). tombi or taplo formats TOML (fact `cfmt-tombi`): check it reads the
file's TOML version.

```bash
yamllint --strict .
check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/*.yml
check-jsonschema --schemafile config.schema.json config.yaml
```

### XML from outside

defusedxml refuses entities and external references by default, but allows a DTD unless told
not to (fact `cfmt-xxe`):

```python
from defusedxml.ElementTree import parse

tree = parse(path, forbid_dtd=True)
```

In other languages, set the parser's own options by OWASP's XXE cheat sheet, DTDs off first.

## Mistakes

- **Trusting the last of two repeated keys.** An edit changes one copy and the parser picks the
  other, without a word. Lint for duplicates, or refuse them at load.
- **A 64-bit ID as a JSON number.** JavaScript's `JSON.parse` reads every number as a double and
  rounds it. Send it as a string.
- **`"_comment"` keys in JSON a schema checks.** They fail validation, or reach the program as
  settings. Use a format with comments.
- **An uploaded XML file parsed with a parser's defaults.** Depending on the language and
  version, they may resolve entities or load a DTD. Turn DTDs off.
- **A real token in `config.example.yaml`.** It's public once pushed. Use `CHANGEME`; rotate a
  token that reached a remote.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | Look for | Severity | Fix |
|---|---|---|---|
| Unsafe YAML load | `yaml.load(` without `SafeLoader`, `yaml.unsafe_load` | `BLOCKER` where outside text reaches it, else `GAP` | `yaml.safe_load` or `safe_load_all` |
| Untrusted XML with DTDs on | An XML parser on uploaded or fetched XML, with no DTD setting | `BLOCKER` where outside text reaches it | defusedxml with `forbid_dtd=True`, or the parser's own setting (fact `cfmt-xxe`) |
| Values YAML 1.1 retypes | Unquoted `yes`, `no`, `on`, `off`, versions, leading-zero numbers | `DRIFT` | Quote them; yamllint `truthy` and `octal-values` as errors |
| Duplicate keys allowed | No `key-duplicates` lint; JSON loaded with no `object_pairs_hook` check | `GAP` | Lint, or refuse at load |
| YAML lint passes on warnings | `yamllint` in CI without `--strict`, `truthy` still a warning | `DRIFT` | `--strict`, or the rules as errors (fact `cfmt-yamllint`) |
| No schema check | Config files with a schema, and no validation step | `GAP` | check-jsonschema in CI (fact `cfmt-json-schema`) |
| TOML 1.1 syntax, 1.0 reader | Multi-line inline tables, `\e`, times without seconds | `DRIFT` | 1.0 syntax, or every reader on 1.1 |
| Secret in a tracked config file | A password, token or key in committed YAML, JSON, TOML or XML | `BLOCKER` | Remove, rotate, read from the environment (standard, dimension 7) |

## Why

### Choosing a format

- **The reason:** a format the tool doesn't read needs a converter, and a second copy drifts.
  TOML has one way to write each type, and forbids repeated keys and empty values (fact
  `cfmt-toml`). Python and Rust chose it for project files; Kubernetes, Compose and GitHub
  Actions chose YAML, for nesting and comments.
- **When to choose differently:** YAML for deep structures people edit, with quoting and a
  linter.

### YAML's versions and its safe loader

- **The reason:** YAML 1.2 removed 1.1's surprising implicit types (fact `cfmt-yaml-12`), but
  PyYAML still parses 1.1 (fact `cfmt-pyyaml`), so tools read one file differently. `yaml.load` can construct any Python object (fact `py-yaml-load`). Aliases let a small
  file expand into a huge one: a crafted payload made the Kubernetes API server use excessive
  CPU or memory (fact `cfmt-yaml-bomb`).
- **What it costs:** quotes on values that look fine to a person.
- **When to choose differently:** a file only a known 1.2 parser reads can leave `NO` and `on`
  bare, but not `3.10` or `0755`.

### Duplicate keys and big numbers

- **The reason:** RFC 8259 says names should be unique, and only integers within 2^53 are
  interoperable (fact `cfmt-json-rfc`). An edit that changes one of two copies loses silently.
- **What it costs:** a check at load, and string IDs the reader converts.

### Validating with a schema

- **The reason:** a misspelled key parses and is ignored; a schema names it. JSON Schema
  2020-12 is current, and SchemaStore holds schemas for many tools (fact `cfmt-json-schema`).
- **What it costs:** a schema kept in step with the code.
- **When to choose differently:** a program that validates its own settings into typed objects
  at startup, as `configuration` describes, may skip a separate schema for that file.

### TOML's version

- **The reason:** TOML 1.1.0 allows multi-line inline tables, new escapes and times without
  seconds (fact `cfmt-toml`). Python's `tomllib` reads 1.1 only from 3.15, and never writes
  (fact `cfmt-tomllib`), so a 1.1 file breaks every older reader.
- **When to choose differently:** a project whose every reader parses 1.1.

### XML's dangers

- **The reason:** a DTD lets a document define entities that read local files or fetch URLs
  (XXE), or expand exponentially (billion laughs). OWASP's first advice is to disable DTDs (fact
  `cfmt-xxe`). Python's Expat fetches no external entities by default, but versions before
  2.7.2 may still suffer entity expansion (fact `cfmt-py-expat`).
- **What it costs:** a format that needs a DTD needs a parser set to allow only what it uses.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked
2026-11-11.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `cfmt-yaml-12` | YAML 1.2.2 is current; 1.2 removed 1.1's problem implicit types; mapping keys must be unique | [YAML 1.2.2](https://yaml.org/spec/1.2.2/) | "Revision 1.2.2 (2021-10-01)" and "removed many of the problematic implicit typing recommendations" and "each of the keys is unique" | 2026-11-11 | 2027-05-11 |
| `cfmt-yaml-11-bool` | YAML 1.1 reads yes/no, on/off and y/n as booleans | [YAML 1.1 bool](https://yaml.org/type/bool.html) | "Booleans are formatted as English words" and "may be abbreviated as a single character" | 2026-11-11 | 2027-05-11 |
| `cfmt-pyyaml` | PyYAML parses YAML 1.1; `safe_load_all` reads every document, standard types only | [PyYAML](https://pyyaml.org/wiki/PyYAML), [docs](https://pyyaml.org/wiki/PyYAMLDocumentation) | "PyYAML features a complete YAML 1.1 parser." and "safe_load_all recognizes only standard YAML tags" | 2026-11-11 | 2027-02-11 |
| `cfmt-yaml12-parsers` | ruamel.yaml and js-yaml parse YAML 1.2 | [ruamel.yaml](https://pypi.org/pypi/ruamel.yaml/json), [js-yaml](https://registry.npmjs.org/js-yaml) | "is a YAML 1.2 loader/dumper package for Python." and "YAML 1.2 parser and serializer for JavaScript." | 2026-11-11 | 2027-02-11 |
| `cfmt-yaml-bomb` | CVE-2019-11253: crafted YAML or JSON exhausted the Kubernetes API server | [NVD](https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2019-11253) | "malicious YAML or JSON payloads, causing the API server to consume excessive CPU or memory" | 2026-11-11 | 2027-05-11 |
| `cfmt-yamllint` | yamllint 1.38.0: `truthy` defaults to a warning, `octal-values` is off, and only errors exit 1 | [Rules](https://yamllint.readthedocs.io/en/stable/rules.html), [config](https://yamllint.readthedocs.io/en/stable/configuration.html) | "truthy: level: warning" and "octal-values: disable" and "exit with a return code 1 only when there is one or more error(s)" | 2026-11-11 | 2027-02-11 |
| `cfmt-json-rfc` | RFC 8259: names SHOULD be unique; integers interoperate only within 2^53 | [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.txt) | "The names within an object SHOULD be unique." and "are in the range [-(2**53)+1, (2**53)-1] are interoperable" | 2026-11-11 | 2027-05-11 |
| `cfmt-py-json` | Python's `json` keeps the last repeated key | [json](https://docs.python.org/3/library/json.html) | "it ignores all but the last name-value pair for a given name" | 2026-11-11 | 2027-05-11 |
| `cfmt-json-schema` | JSON Schema 2020-12 is current; check-jsonschema 0.39.0 ships SchemaStore schemas and reads TOML too | [Spec](https://json-schema.org/specification), [usage](https://check-jsonschema.readthedocs.io/en/stable/usage.html), [parsers](https://check-jsonschema.readthedocs.io/en/stable/optional_parsers.html) | "The current version is 2020-12!" and "vendored copies schemas from SchemaStore" and "the TOML parser is no longer optional" | 2026-11-11 | 2027-02-11 |
| `cfmt-toml` | TOML 1.1.0 (2025-12-18) allows multi-line inline tables; TOML has no null type, and keys can't repeat | [Changelog](https://raw.githubusercontent.com/toml-lang/toml/main/CHANGELOG.md), [TOML 1.1.0](https://toml.io/en/v1.1.0) | "1.1.0 / 2025-12-18" and "Allow newlines and trailing commas in inline tables" and "Values must have one of the following types." and "Defining a key multiple times is invalid." | 2026-11-11 | 2027-05-11 |
| `cfmt-tomllib` | `tomllib` read TOML 1.0 from Python 3.11, reads 1.1 from 3.15, and doesn't write | [tomllib](https://docs.python.org/3/library/tomllib.html) | "The module was added with support for TOML 1.0.0." and "Changed in version 3.15: Added TOML 1.1.0 support." and "This module does not support writing TOML." | 2026-11-11 | 2027-02-11 |
| `cfmt-tombi` | tombi 1.11.2 (2026-11-10) formats and lints TOML | [tombi](https://pypi.org/pypi/tombi/json) | "provides a Formatter, Linter, and Language Server" | 2026-11-11 | 2027-02-11 |
| `cfmt-xxe` | OWASP: DTDs off first, XInclude off; defusedxml allows a DTD by default | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html), [defusedxml](https://pypi.org/pypi/defusedxml/json) | "Disable document type definitions (DTDs) whenever possible." and "Keep XInclude disabled" and "forbid_dtd (default: False)" | 2026-11-11 | 2027-05-11 |
| `cfmt-py-expat` | Python's Expat fetches no external entities; before 2.7.2 it may suffer entity expansion | [XML modules](https://docs.python.org/3/library/xml.html) | "Expat itself does not access local files or create network connections." and "Expat versions lower than 2.7.2 may be vulnerable" | 2026-11-11 | 2027-02-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [YAML specifications](https://yaml.org/spec/1.2.2/) | Versions, booleans, keys | Copied only unmodified: short quotes |
| [PyYAML](https://pyyaml.org/wiki/PyYAML), ruamel.yaml, js-yaml | Parsers' YAML versions | MIT: short quotes |
| [yamllint](https://yamllint.readthedocs.io/) | Rules and defaults | GPL-3.0: our own words, short quotes, no code |
| [NVD](https://nvd.nist.gov/) | CVE-2019-11253 | US government work, public domain |
| [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) | JSON names and numbers | IETF Trust: short quotes |
| [Python documentation](https://docs.python.org/3/), [defusedxml](https://pypi.org/project/defusedxml/) | `json`, `tomllib`, XML | PSF License 2: short quotes |
| [JSON Schema](https://json-schema.org/specification), check-jsonschema | Version, schemas, file types | All rights reserved; Apache-2.0: short quotes |
| [TOML](https://toml.io/en/v1.1.0), tombi | TOML 1.1.0, its tools | MIT: short quotes |
| [OWASP XXE cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html) | DTDs, XInclude | CC BY-SA 4.0: short quotes, with attribution |
