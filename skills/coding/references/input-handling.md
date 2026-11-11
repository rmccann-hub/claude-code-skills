# Input handling

Read this for checking data from outside where it enters, in any language: allow-lists, parsing
into types, canonical paths, Unicode and URLs, size and depth limits, rejecting bad input, and
escaping output for where it lands: HTML, SQL, a shell, a log, a terminal, a CSV file, a GUI
label or an issue.

This module holds the practice every language shares. Each language's calls are in
`python-security`, `javascript-security`, `csharp-security`, `powershell-security`,
`bash-security` and `c-security`, and `web-security` takes HTML, URLs in pages and sanitizers.
Designing the types that hold parsed values is `types`'s; parser settings for YAML, JSON, TOML
and XML are `config-formats`'s. What to log is the planned `logging-and-observability` module's,
and hidden characters in files an agent reads the planned `ai-agent-security`'s.

## Rules

1. **Validate where data crosses a trust boundary, on the side that relies on it:** the server,
   not the browser. Internal services, queues, stored records and files an earlier run wrote
   are outside too.
2. **Say what you accept, and reject the rest.** An allow-list of values, ranges, lengths and
   whole-value patterns, never a list of strings you fear.
3. **Parse into a type once, check its meaning, and pass the parsed value on.** A number isn't
   yet a valid quantity, nor a date a valid end date.
4. **Decode and canonicalize before you check, and use the form you checked.**
5. **Limit size, count and depth before you parse.** A check after the parser ran out of memory
   comes too late.
6. **Reject, don't repair.** Refuse the whole input with an error naming the field; never strip
   what looks dangerous and carry on.
7. **Encode output for where it lands, at the point it lands.** Validation can't make text safe
   for every place it may go; that place's encoder can.
8. **Escape outside text that a person or an agent reads:** in a terminal, a log line, an issue
   or a GUI label.

### Canonicalizing paths, Unicode and URLs

- **Paths.** Make the path absolute, resolve `..` and links, then check it's inside the base
  directory (fact `js-cwe22`). Better, accept one allow-listed name and build the path yourself.
- **Unicode.** Decode with one declared encoding, and reject malformed bytes. Pick a
  normalization form per compared field, and apply it before validation, storage and comparison
  alike (fact `input-owasp-unicode`). NFKC folds look-alikes: fine for identifiers, wrong for
  prose (fact `input-uax15-nfkc`).
- **Character classes.** Python's `\d` matches other scripts' digits (fact `input-py-digit`):
  check what your engine's classes match. Write `[0-9]` or set the ASCII flag, and match the
  whole value.
- **URLs.** Parse once, check the scheme against an allow-list (fact `web-owasp-url`) and the
  host on the parsed result, and use the URL built from that result: parsers disagree on odd
  input (fact `input-py-urlsplit`).

### Where output lands

| It lands in | Do | Not |
|---|---|---|
| HTML | Template auto-escaping, `textContent` (fact `web-owasp-text`) | String-built markup, `innerHTML` |
| SQL | Parameters; table and column names from a fixed set (fact `js-sql-params`) | Escaping by hand |
| A process | Program plus argument array, no shell, `--` before operands (fact `input-owasp-cmd`) | A command string, `shell=True`, `system()` |
| A log line | A structured format, or CR, LF and the delimiter escaped (facts `input-owasp-log`, `csec-output`) | Rejected input logged whole |
| A terminal | Control and format characters escaped, as below | Raw outside names |
| A CSV file | Cells starting `=`, `+`, `-`, `@`, tab, CR or LF neutralized, then quoted (fact `input-csv`) | Quoting alone |
| A GUI label | Plain-text mode set explicitly (fact `input-qt-autotext`) | A widget that guesses the format |
| Markdown an agent reads | A fence longer than any backtick run inside, escaped and capped | A server's reply pasted raw |

### Escaping for a terminal or a log line

Escape control and format characters, bidirectional overrides among them, line separators, and
the backslash, so the result reads back unambiguously. Leave other scripts alone.

```python
import unicodedata

UNSAFE = {"Cc", "Cf", "Zl", "Zp"}


def printable(text: str) -> str:
    """Return text that prints on one line and can't drive a terminal."""
    out = []
    for ch in text:
        if ch == "\\":
            out.append("\\\\")
        elif unicodedata.category(ch) in UNSAFE:
            code = ord(ch)
            out.append(f"\\u{code:04x}" if code <= 0xFFFF else f"\\U{code:08x}")
        else:
            out.append(ch)
    return "".join(out)


assert printable("caf\u00e9\x1b[2J\n\u202e") == "caf\u00e9\\u001b[2J\\u000a\\u202e"
```

## Mistakes

- **One `sanitize()` at the entrance, trusted everywhere.** Assistants write it often. It strips
  what some sinks need, misses what others fear, and escapes for none (fact
  `input-owasp-allowlist`). Validate at entry; encode at each sink.
- **Stripping `../` once.** `....//` becomes `../` after one pass. Reject the input.
- **Quoting for the shell and calling `system()`.** A quoted value can still be an option, such
  as `--output`, to the program (fact `input-owasp-cmd`). Use an argument array and `--`.
- **`re.match` or an unanchored pattern as a validator.** It passes a valid prefix with anything
  after it. Use `fullmatch` or whole-string anchors.
- **Removing escape sequences from what's shown, then acting on the raw value.** The person
  approves one name and the program uses another (fact `input-ansi-dialog`).
- **Taking parameterized log calls as escaping.** CR and LF still pass (fact `input-owasp-log`).
- **Pasting a remote error into an issue, a pull request or a prompt** as if it were the
  program's own text (L52).

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Commands built from strings | `system(`, `shell=True`, `Invoke-Expression`, `bash -c "$x"` fed by input | `BLOCKER` if input reaches it, else `GAP` | Argument array, no shell, `--` (fact `input-owasp-cmd`) |
| SQL built from strings | Concatenation, f-strings or template literals in a query | `BLOCKER` if input reaches it, else `GAP` | Parameters (fact `js-sql-params`) |
| Deny-lists and strippers | `replace` or a regex removing `'`, `<`, `../` or `;` from input | `GAP` | An allow-list that rejects (fact `input-owasp-allowlist`) |
| Validation only in the client | Form rules with no matching server check | `GAP` | The same rules on the server (fact `web-owasp-validation`) |
| Checked before canonicalized | A path or URL string tested before it's resolved or parsed | `BLOCKER` where it guards a file or host, else `GAP` | Canonicalize, check, use that form (fact `input-cwe180`) |
| No limits | A body, upload, array or nesting read with no maximum | `GAP` | Limits before parsing (facts `input-owasp-parse`, `input-json-limits`) |
| Raw outside text shown | Names, errors and replies printed, logged or posted as received | `GAP` | Escape for that output (L52; fact `csec-output`) |
| CSV export of user data | Cells written with no first-character check | `GAP` | Neutralize and quote (fact `input-csv`) |

## Why

### Boundaries and allow-lists (rules 1 and 2)

- **The reason:** a check the sender runs can be skipped (fact `web-owasp-validation`), and a
  queue or a table doesn't vouch for what's in it (fact `input-owasp-boundary`). A deny-list has
  to know every attack, and blocking `'` turns away real names without making a query safe (fact
  `input-owasp-allowlist`).
- **What it costs:** each field needs written rules, and a strict one refuses some real input.
  A free-text field's allow-list can be any text up to a length.

### Parsing into types (rule 3)

- **The reason:** a string checked and passed on gets parsed again later, perhaps differently.
  An integer establishes a type, not an acceptable quantity, and partly checked input must stop
  the request (fact `input-owasp-parse`).
- **What it costs:** a type, or at least a parsing function, per kind of value; `types` has
  the design.

### Canonicalizing first (rule 4)

- **The reason:** a check on one spelling passes a value that means something else once
  resolved: `/safe/../etc` starts with `/safe/` (fact `input-cwe180`). Decoding twice undoes a
  check the same way (fact `input-owasp-parse`).
- **What it costs:** NFKC changes what a person typed: keep the original for display, and
  compare the normalized copy.

### Limits and rejection (rules 5 and 6)

- **The reason:** a huge body or deep nesting exhausts memory or the stack before any schema
  runs; JSON's standard lets a parser limit nesting (fact `input-json-limits`). Stripping changes
  what's left and escapes for no sink (fact `input-owasp-allowlist`); an error tells the sender
  what to fix.
- **What it costs:** a limit refuses some large, honest input: set it from real data, and name
  it in the error.
- **When to choose differently:** HTML a person wrote to be rendered goes through a maintained
  sanitizer, which does repair (`web-security`). A file name built from outside values can't be
  refused, so map each unsafe character, as `c-security` shows.

### Encoding at each sink (rules 7 and 8)

- **The reason:** text safe in one place is dangerous in another, and only the sink's own
  mechanism knows its syntax. Terminals obey escape sequences in any output (fact
  `csec-output`); a spreadsheet runs a cell starting `=` (fact `input-csv`). One checker put a
  remote server's error text, unescaped, into a weekly issue that agents read (L52).
- **What others do:** for CSV, OWASP offers a leading single quote, which Excel can drop on
  save, or a tab inside the quoted cell, which changes the data for programs that import it.
  It says no fix suits every reader (fact `input-csv`).
- **What it costs:** escaped text is harder to read, and a joined emoji shows its joiner.
- **When to choose differently:** a CSV only programs read needs CSV quoting, not formula
  guards; output with no outside text in it needs no terminal escaping.

## Facts

Guidance and behavior, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `input-owasp-boundary` | Internal sources are validated at a boundary | [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) | "Validate data from internal APIs, partner feeds, queues, and stored records when it crosses a trust boundary." | 2026-11-11 | 2027-05-11 |
| `input-owasp-allowlist` | Accept what's defined; stripping isn't escaping | [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) | "Do not try to recognize every malicious string." and "Removing suspicious characters can change meaning and still does not provide query parameterization or output encoding." | 2026-11-11 | 2027-05-11 |
| `input-owasp-parse` | Limits first; a type isn't a valid value; decode once; stop on failure | [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) | "Apply request size limits before buffering or parsing input" and "Converting text to an integer only establishes a type" and "avoid decoding it again downstream" and "do not continue with partially validated data" | 2026-11-11 | 2027-05-11 |
| `input-owasp-unicode` | One normalization policy; it isn't sanitization | [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) | "define and apply the same policy before validation, storage, and comparison" and "Normalization is not sanitization" | 2026-11-11 | 2027-05-11 |
| `input-uax15-nfkc` | NFKC and NFKD erase distinctions | [UAX #15](https://www.unicode.org/reports/tr15/) | "Normalization Forms KC and KD must not be blindly applied to arbitrary text." | 2026-11-11 | 2027-05-11 |
| `input-cwe180` | Validating before canonicalizing is a weakness | [CWE-180](https://cwe.mitre.org/data/definitions/180.html) | "The product validates input before it is canonicalized." | 2026-11-11 | 2027-05-11 |
| `input-py-digit` | Python's `\d` matches all Unicode decimal digits | [Python `re`](https://docs.python.org/3/library/re.html) | "Matches any Unicode decimal digit" and "and also many other digit characters" | 2026-11-11 | 2027-05-11 |
| `input-py-urlsplit` | Python's URL parsers don't validate | [Python `urllib.parse`](https://docs.python.org/3/library/urllib.parse.html) | "APIs do not perform validation of inputs" and "might not be considered URLs elsewhere" | 2026-11-11 | 2027-05-11 |
| `input-json-limits` | JSON parsers may limit nesting | [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html) | "An implementation may set limits on the maximum depth of nesting." | 2026-11-11 | 2027-05-11 |
| `input-owasp-cmd` | Avoid OS commands; quoting leaves argument injection | [OWASP OS Command Injection Defense](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html) | "The primary defense is to avoid calling OS commands directly." and "Every OS Command Injection is also an Argument Injection." | 2026-11-11 | 2027-05-11 |
| `input-owasp-log` | Parameterized logging passes CR and LF | [OWASP Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | "Parameterized logging alone does not prevent CR/LF log injection" | 2026-11-11 | 2027-05-11 |
| `input-ansi-dialog` | A dialog stripped escapes, showing the wrong file | [CWE-150](https://cwe.mitre.org/data/definitions/150.html) | "removes ANSI escape sequences in a dialog that asks permission for a particular file" | 2026-11-11 | 2027-05-11 |
| `input-csv` | Formula cells; Excel can undo quoting; no universal fix | [OWASP CSV Injection](https://community.owasp.org/attacks/CSV_Injection) | "any cells starting with = will be interpreted by the software as a formula" and "Microsoft Excel may remove quotes or escape characters from CSV cells" and "There is no universal CSV sanitization strategy" | 2026-11-11 | 2027-05-11 |
| `input-qt-autotext` | `QLabel` guesses plain or rich text | [QLabel](https://doc.qt.io/qt-6/qlabel.html) | "QLabel tries to guess whether it displays the text as plain text or as rich text" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) and [OWASP CSV Injection](https://community.owasp.org/attacks/CSV_Injection) | Validation, commands, logs, CSV | CC BY-SA 4.0: brief quotes with attribution, our own words otherwise |
| [MITRE CWE](https://cwe.mitre.org/) (CWE-150, CWE-180) | Canonical order, escape sequences | CWE Terms of Use, copyright MITRE: short quotes, with attribution |
| [Unicode UAX #15](https://www.unicode.org/reports/tr15/) | Normalization forms | Unicode Terms of Use: facts in our own words, a short quote |
| [Python documentation](https://docs.python.org/3/library/) | Digit classes, URL parsing | PSF License Version 2: short quotes, with attribution |
| [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html) | Parser limits | IETF Trust Legal Provisions: short quotes, with attribution |
| [Qt documentation](https://doc.qt.io/qt-6/qlabel.html) | Rich text in labels | GNU FDL 1.3: a short quote, our own words otherwise |
| This repository's own audits | Outside text in an issue agents read (L52) | Observed practice, in our own words |
