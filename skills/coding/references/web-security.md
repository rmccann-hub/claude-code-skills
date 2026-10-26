# Web security

Read this for browser-side security: untrusted data in pages, attributes and URLs, `innerHTML`
and sanitizing with `setHTML()` or DOMPurify, Trusted Types, Content Security Policy, Subresource
Integrity, and `target="_blank"` with `noopener`.

Markup, accessibility, forms and CSS are `html-coding`'s. JavaScript and TypeScript are
`javascript-coding`'s, and their server-side security `javascript-security`'s. Pinning versions,
lockfiles and CI are the project-bootstrap-and-audit standard's *Language toolchains*.

## Rules

1. **Insert untrusted data as text, encoded for the context it lands in,** never by building
   HTML from strings.
2. **Send untrusted HTML through a sanitizer:** `setHTML()` where the browser has it, DOMPurify
   where it doesn't.
3. **Send a strict Content Security Policy,** built on nonces or hashes, and enforce Trusted
   Types where the code allows it.
4. **Self-host third-party files, or pin them with an integrity hash computed from the file.**
   Never write a hash you didn't compute.

### Output into pages, attributes and links

- **Text goes in as text.** In the DOM, assign `textContent`, which never parses HTML (fact
  `web-owasp-text`). On the server, check that the template engine's auto-escaping is on: Jinja's
  is off unless configured (fact `web-jinja-autoescape`).
- **Each context has its own encoding** (fact `web-owasp-text`): HTML entities for element
  content, attribute encoding inside a quoted attribute, and `encodeURIComponent()` for a URL
  parameter (fact `web-owasp-url`). Attribute encoding doesn't make a URL, a handler or a style
  safe.
- **A URL from input is checked before it's used,** allowing only `http:` and `https:` (fact
  `web-owasp-url`). Encoding alone leaves `javascript:` working.

### Untrusted markup

- **`innerHTML` with a string from input is the classic XSS sink** (fact `web-innerhtml`), as are
  `outerHTML`, `insertAdjacentHTML()`, `document.write()` and frameworks' escape hatches.
- **`setHTML()` sanitizes as it inserts,** always dropping script-capable content, but Safari
  hasn't shipped it (fact `web-sethtml`). Feature-detect it, and fall back to DOMPurify, kept
  patched (fact `web-owasp-dompurify`). DOMPurify's output goes into `innerHTML` once, straight
  from `sanitize()`. Never serialize `setHTML()`'s result and parse it again with `innerHTML`
  (fact `web-sethtml-tt`).
- **Trusted Types** is Baseline since February 2026 (fact `web-trusted-types`). With the CSP
  directive `require-trusted-types-for 'script'`, a plain string assigned to a sink throws (fact
  `web-tt-enforce`). `setHTML()` isn't gated, because it always sanitizes (fact `web-sethtml-tt`),
  and DOMPurify returns `TrustedHTML` when asked (fact `web-dompurify-tt`).

```javascript
// Text from a user: set as text, never parsed as HTML.
document.querySelector("#greeting").textContent = `Hello, ${userName}`;

// A link from a user: allow only http and https.
function safeHref(input) {
  try {
    const url = new URL(input, document.baseURI);
    return url.protocol === "https:" || url.protocol === "http:" ? url.href : null;
  } catch {
    return null;
  }
}
const href = safeHref(profileUrl);
if (href) document.querySelector("#homepage").href = href;

// HTML from a user that must keep its formatting.
const preview = document.querySelector("#preview");
if (typeof preview.setHTML === "function") {
  preview.setHTML(commentHtml);
} else {
  preview.innerHTML = DOMPurify.sanitize(commentHtml, { RETURN_TRUSTED_TYPE: true });
}
```

### Content security policy

A strict policy allows scripts by nonce or hash, not by host (fact `web-csp-strict`):

```text
Content-Security-Policy: script-src 'nonce-{RANDOM}' 'strict-dynamic'; object-src 'none'; base-uri 'none'; frame-ancestors 'self'
```

- **A fresh nonce on every response,** from a secure random source (fact `web-csp-nonce`), on
  each `<script nonce>` the server writes. A cached page with a fixed nonce defeats it.
- **Inline event handlers and `javascript:` URLs stop working.** Move them to
  `addEventListener()`.
- **Send it as a header.** In a `<meta>` element, `frame-ancestors`, `sandbox` and `report-uri`
  are ignored (fact `web-csp-meta`).
- **Roll out with `Content-Security-Policy-Report-Only` first,** read the reports, then enforce.
  Add `; require-trusted-types-for 'script'` last, on its own, once the code passes it in
  report-only mode: enforcing it breaks every library still writing strings to sinks.

### Third-party files and new windows

- **Self-host what you can.** A file from your own origin changes only when you deploy.
- **A file from another origin carries `integrity` and `crossorigin`.** A response that fails
  the check isn't run (fact `web-sri-fail`), so a wrong hash breaks the page. Compute the hash
  from the exact file (fact `web-sri-openssl`), and never write one from memory:

```sh
openssl dgst -sha384 -binary vendor/lib.min.js | openssl base64 -A
```

```html
<script src="https://cdn.example.com/lib/1.2.3/lib.min.js"
        integrity="sha384-OUTPUT-OF-THE-COMMAND-ABOVE"
        crossorigin="anonymous"></script>
```

- **`target="_blank"` already implies `noopener`** in the HTML standard (fact
  `web-blank-noopener`). Add `rel="noopener"` only for old browsers you still support, and
  `noreferrer` only to withhold the referring URL, a privacy choice rather than a fix.

## Mistakes

- **Building HTML from strings,** such as `` el.innerHTML = `<p>${name}</p>` ``, or a web
  component that interpolates its attributes into `shadowRoot.innerHTML`. Assistants write this
  often. Set `textContent`, or sanitize.
- **Escaping a URL as HTML and trusting it in `href`.** Check the scheme too.
- **`setHTML()` with no fallback,** which fails in Safari (fact `web-sethtml`).
- **An integrity hash written from memory,** or a placeholder left in. The browser refuses the
  file (fact `web-sri-fail`).
- **A CSP of `'unsafe-inline'` and a list of hosts** (fact `web-csp-strict`), `frame-ancestors`
  in a `<meta>` policy (fact `web-csp-meta`), or a nonce fixed in a template (fact
  `web-csp-nonce`).
- **Reporting a missing `rel="noopener"` as a vulnerability** for current browsers (fact
  `web-blank-noopener`).

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Untrusted data in an HTML sink | `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `dangerouslySetInnerHTML`, `v-html` fed by input or a template string | `BLOCKER` where input reaches it | `textContent`, or `setHTML()` with DOMPurify as fallback |
| Template auto-escaping | Jinja's `Environment(` without `autoescape`, and `\|safe` or `Markup(` on input | `BLOCKER` where input reaches it, else `GAP` | Turn it on (fact `web-jinja-autoescape`) |
| URLs from input | `href`, `src` or `location` set from input with no scheme check | `GAP` | Allow `http:` and `https:` only (fact `web-owasp-url`) |
| Content Security Policy | None, report-only for good, or `'unsafe-inline'` with hosts | `GAP` | A strict policy (fact `web-csp-strict`) |
| CSP in `<meta>` with `frame-ancestors` | The page's `<meta http-equiv>` | `DRIFT`: ignored | A header (fact `web-csp-meta`) |
| Headers set outside the repository | A proxy or host sends the CSP | `MIRROR`, or `UNVERIFIABLE-HERE` | Read the live response headers |
| Third-party scripts and styles | Another origin's `<script src>` or stylesheet without `integrity` | `GAP` | Self-host, or a computed hash (fact `web-sri-openssl`) |
| Integrity hashes that fail | Console integrity errors, or a hash not matching the file | `DRIFT` | Recompute from the file served |
| `noopener noreferrer` everywhere | `rel` on every `target="_blank"` link | `OVER` where the referrer is wanted | `target="_blank"` alone (fact `web-blank-noopener`) |

## Why

### Text by default, a sanitizer where HTML is needed

**The advice.** Text as text, encoded for its context, URL schemes checked, and user HTML through
`setHTML()` or DOMPurify, with Trusted Types enforced.

**Why.** Cross-site scripting is input that a parser reads as code. `textContent` and an
auto-escaping template take the parser out of the path (facts `web-owasp-text`,
`web-owasp-url`). A sanitizer built into the browser uses its own parser, so no second, different
parse lets a payload change shape, but Safari lacks it (fact `web-sethtml`). Trusted Types turns a forgotten sink into an error instead of a hole.

**What others do.** React and its peers escape text by default and name raw HTML APIs as a
warning, such as `dangerouslySetInnerHTML`; the risk moves to those and to URLs.

**The cost.** Enforcing Trusted Types breaks libraries that write strings to sinks, until updated
or wrapped in a policy. Where no user HTML is shown, skip the sanitizer.

### A strict policy

**The advice.** Nonce or hash based, with `'strict-dynamic'`, `object-src 'none'` and
`base-uri 'none'`.

**Why.** An allowlist usually includes a host serving something an attacker can use, so
web.dev calls such policies bypassable (fact `web-csp-strict`). A nonce ties execution to what
the server wrote.

**The cost.** Nonces per response, no inline handlers, and pages that can't be cached whole.
**When to choose differently:** a static site, with no server to make nonces, uses hashes.

### Integrity hashes from the file

**Why.** A compromised CDN serves its code to every site that loads it; a hash stops a changed
file from running (fact `web-sri-fail`). A guessed hash stops the right file too, the failure
assistants cause. **The cost:** a new hash for each upgrade. Self-hosting avoids
both.

## Facts

Each named above by its ID. The license facts are `html-coding`'s. Checked 2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `web-blank-noopener` | `_blank` implies `noopener` unless the link says `opener` | [HTML, links](https://html.spec.whatwg.org/multipage/links.html) | "do not include the opener keyword" | 2026-10-26 | 2027-10-26 |
| `web-owasp-text` | Entity encoding in HTML, `textContent` in JavaScript | [OWASP XSS](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | "use HTML entity encoding" and "assign it to the textContent property" | 2026-10-26 | 2027-10-26 |
| `web-owasp-url` | Allow http and https URLs only; encode parameters | [OWASP XSS](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | "Allow-list http and HTTPS URLs only" and "use encodeURIComponent()" | 2026-10-26 | 2027-10-26 |
| `web-owasp-dompurify` | DOMPurify, kept patched | [OWASP XSS](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | "OWASP recommends DOMPurify" and "regularly patch DOMPurify" | 2026-10-26 | 2027-04-26 |
| `web-jinja-autoescape` | Jinja's auto-escaping is off by default | [Jinja API](https://jinja.palletsprojects.com/en/stable/api/) | "autoescaping is not yet enabled by default" | 2026-10-26 | 2027-04-26 |
| `web-innerhtml` | `innerHTML` is the commonest XSS vector | [innerHTML](https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML) | "most common vector for cross-site scripting" | 2026-10-26 | 2027-10-26 |
| `web-sethtml` | Not Baseline: Chrome 146 and Firefox 148 ship it, Safari doesn't | [setHTML()](https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTML), [browser-compat-data](https://raw.githubusercontent.com/mdn/browser-compat-data/main/api/Element.json) | "does not work in some of the most widely-used browsers" | 2026-10-26 | 2027-04-26 |
| `web-sethtml-tt` | Not gated by Trusted Types; re-parsing its output is unsafe | [setHTML()](https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTML) | "not secured or validated using the Trusted Types API" and "not safe to serialize the HTML and re-parse it" | 2026-10-26 | 2027-04-26 |
| `web-trusted-types` | Baseline since February 2026 | [Trusted Types](https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API) | "Since February 2026, this feature works" | 2026-10-26 | 2027-04-26 |
| `web-tt-enforce` | Enforced, a string in a sink throws | [Trusted Types](https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API) | "injection sinks will result in a TypeError" | 2026-10-26 | 2027-10-26 |
| `web-dompurify-tt` | `RETURN_TRUSTED_TYPE` gives `TrustedHTML` | [DOMPurify README](https://raw.githubusercontent.com/cure53/DOMPurify/main/README.md) | "return a `TrustedHTML` value" | 2026-10-26 | 2027-04-26 |
| `web-csp-strict` | The strict CSP; allowlists can be bypassed | [web.dev, strict CSP](https://web.dev/articles/strict-csp) | "script-src 'nonce-{RANDOM}' 'strict-dynamic'; object-src 'none'; base-uri 'none';" and "can be bypassed by attackers." | 2026-10-26 | 2027-10-26 |
| `web-csp-nonce` | A nonce is new on every response | [CSP Level 3](https://www.w3.org/TR/CSP3/) | "generate a unique value each time it transmits a policy" | 2026-10-26 | 2027-10-26 |
| `web-csp-meta` | A `<meta>` policy ignores three directives | [CSP Level 3](https://www.w3.org/TR/CSP3/) | "Neither are the report-uri, frame-ancestors, and sandbox directives." | 2026-10-26 | 2027-10-26 |
| `web-sri-fail` | A file failing its integrity check isn't run | [SRI](https://www.w3.org/TR/SRI/) | "refuse to render or execute responses that fail an integrity check" | 2026-10-26 | 2027-10-26 |
| `web-sri-openssl` | SRI computes hashes with OpenSSL | [SRI](https://www.w3.org/TR/SRI/) | "OpenSSL, for example, is quite commonly available." | 2026-10-26 | 2027-10-26 |

## Sources

Rules are in this module's own words. Share-alike sources, MDN and OWASP, are quoted briefly,
with attribution, each quote a dated fact.

| Source | Used for | License |
|---|---|---|
| [HTML Standard](https://html.spec.whatwg.org/multipage/) | `noopener` | CC BY 4.0 (fact `web-whatwg-license`): short quotes, with attribution |
| [CSP Level 3](https://www.w3.org/TR/CSP3/) and [SRI](https://www.w3.org/TR/SRI/) | Nonces, `<meta>` policies, integrity | W3C permissive document license (fact `web-w3c-license`): short quotes |
| [web.dev, strict CSP](https://web.dev/articles/strict-csp) | The strict policy | CC BY 4.0, code Apache 2.0 (fact `web-webdev-license`): short quotes, with attribution |
| [MDN](https://developer.mozilla.org/) by Mozilla Contributors, and its [compat data](https://github.com/mdn/browser-compat-data) | Sinks, `setHTML()`, Trusted Types | Prose CC BY-SA 2.5 or later: short quotes, with attribution; data CC0 1.0 |
| [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | Encoding, URLs, DOMPurify | CC BY-SA 4.0: short quotes, with attribution |
| [DOMPurify](https://github.com/cure53/DOMPurify) | `RETURN_TRUSTED_TYPE` | MPL-2.0 or Apache-2.0: a short quote |
| [Jinja](https://jinja.palletsprojects.com/en/stable/api/) | Auto-escaping | BSD-3-Clause: a short quote |
