# HTML and CSS coding

Read this for writing, reviewing or fixing HTML and CSS: semantic markup, the accessibility basics
every page needs, forms, modern CSS, and browser-side security such as escaping output, sanitizing
HTML, Content Security Policy, Trusted Types and Subresource Integrity.

JavaScript and TypeScript as languages, such as types, modules and async code, are
`javascript-coding`'s. A full accessibility audit, with assistive technology testing, belongs to a
planned accessibility module, and design tokens and palettes to a planned visual-design skill.
Pinning versions, lockfiles, CI and dependency updates are the project-bootstrap-and-audit
standard's, in its *Language toolchains* and the dimensions that cite it. HTML email isn't covered.

## Contents

Rules (semantic markup and roles, accessibility basics, output into pages, untrusted markup,
content security policy, third-party files, forms, styles), Mistakes, Audit, Why, Facts, Sources.

## Rules

1. **Use the HTML element that means what you need,** and ARIA only where HTML has nothing.
2. **Meet WCAG 2.2 level AA's basics on every page:** language, text alternatives, labels,
   headings, visible focus, contrast and target size.
3. **Insert untrusted data as text, encoded for the context it lands in,** never by building
   HTML from strings.
4. **Send untrusted HTML through a sanitizer:** `setHTML()` where the browser has it, DOMPurify
   where it doesn't.
5. **Send a strict Content Security Policy,** built on nonces or hashes, and enforce Trusted
   Types where the code allows it.
6. **Self-host third-party files, or pin them with an integrity hash computed from the file.**
   Never write a hash you didn't compute.
7. **Label every form control,** give it its real `type` and `autocomplete`, give every button a
   `type`, and validate again on the server.
8. **Style with custom properties, grid and flex,** honor `prefers-color-scheme` and
   `prefers-reduced-motion`, and never remove a focus indicator without a replacement.

### Semantic markup and roles

- **A control is a `<button>`, a link is an `<a href>`.** ARIA roles add no keyboard behavior or
  styling (fact `web-aria-promise`), so `role="button"` on a `<div>` promises what the script
  must then build. Don't restate an element's own role either (fact `web-aria-redundant`).
- **Headings in order,** one `<h1>` for the page's subject and no level skipped, and landmarks
  (`<header>`, `<nav>`, `<main>`, `<footer>`) for the page's regions.
- **`lang` on `<html>`,** so a screen reader picks the right voice (fact `web-wcag-lang`), and
  `<meta charset="utf-8">` and a viewport `<meta>` in every page's `<head>`.

### Accessibility basics

WCAG 2.2 is the current W3C Recommendation, and W3C advises using it (fact `web-wcag22`). It
added criteria such as 2.4.11 Focus Not Obscured and 2.5.8 Target Size (fact `web-wcag-new`).
Every page meets these at level AA:

- **Text alternatives** for every image that carries meaning (fact `web-wcag-alt`), and `alt=""`
  for one that adds nothing the text doesn't say (fact `web-alt-empty`). An icon-only button
  takes an accessible name, such as visually hidden text or `aria-label`.
- **Contrast:** 4.5:1 for body text and 3:1 for large text (fact `web-wcag-contrast`); 3:1 for
  controls' boundaries and focus indicators against what's next to them (fact `web-wcag-nontext`).
- **Visible focus** for everything reachable by keyboard (fact `web-wcag-focus-visible`), not
  hidden under a sticky header (2.4.11).
- **Targets at least 24 by 24 CSS pixels,** or spaced as the criterion allows (fact
  `web-wcag-target`).

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
  patched (fact `web-owasp-dompurify`). Never re-insert sanitized output with `innerHTML` (fact
  `web-sethtml-tt`).
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
Content-Security-Policy: script-src 'nonce-{RANDOM}' 'strict-dynamic'; object-src 'none'; base-uri 'none'; frame-ancestors 'self'; require-trusted-types-for 'script'
```

- **A fresh nonce on every response,** from a secure random source (fact `web-csp-nonce`), on
  each `<script nonce>` the server writes. A cached page with a fixed nonce defeats it.
- **Inline event handlers and `javascript:` URLs stop working.** Move them to
  `addEventListener()`.
- **Send it as a header.** In a `<meta>` element, `frame-ancestors`, `sandbox` and `report-uri`
  are ignored (fact `web-csp-meta`).
- **Roll out with `Content-Security-Policy-Report-Only` first,** read the reports, then enforce.
  Add `require-trusted-types-for` last, once the code passes.

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

### Forms

- **Every control has a `<label>`,** tied by `for` and `id` or wrapping it. A placeholder isn't a
  label (fact `web-placeholder`). Related controls go in a `<fieldset>` with a `<legend>`.
- **The real `type` and an `autocomplete` token,** such as `email` or `new-password`, so phones
  show the right keyboard and password managers fill the right field (fact
  `web-wcag-input-purpose`).
- **Every `<button>` names its `type`.** In a form, one without it submits (fact
  `web-button-submit`).
- **Validate on the server too.** Browser checks are for the user's convenience (fact
  `web-owasp-validation`).

```html
<form action="/account/email" method="post">
  <fieldset>
    <legend>Contact details</legend>
    <label for="email">Email</label>
    <input id="email" name="email" type="email" autocomplete="email" required
           aria-describedby="email-hint">
    <p id="email-hint">We send receipts here.</p>
  </fieldset>
  <button type="submit">Save</button>
  <button type="button" id="cancel">Cancel</button>
</form>
```

### Styles

- **Custom properties for values that change together,** such as colors per scheme, with
  `color-scheme` so form controls and scrollbars follow (fact `web-color-scheme`).
- **Grid for two-dimensional layout, flex for one row or column,** and logical properties such
  as `margin-inline-start`, so right-to-left text works.
- **`prefers-color-scheme` and `prefers-reduced-motion`** are Baseline widely available (fact
  `web-media-prefs`). Put motion inside `prefers-reduced-motion: no-preference`, so it's opt-in.
- **Style `:focus-visible`** (fact `web-focus-visible`) rather than removing outlines.
- **Check a newer feature's Baseline status** on its MDN page. "Widely available" means 30 months
  across the core browsers (fact `web-baseline`); anything newer needs a fallback or a test.

```css
:root { color-scheme: light dark; --surface: #ffffff; --text: #1a1a1a; --focus: #0b57d0; }

@media (prefers-color-scheme: dark) {
  :root { --surface: #121212; --text: #ececec; --focus: #8ab4f8; }
}

body { background: var(--surface); color: var(--text); }

:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }

@media (prefers-reduced-motion: no-preference) {
  .card { transition: transform 150ms ease-out; }
}
```

By WCAG's formula, the text here is over 15:1 in both schemes, and the focus colors 6.4:1 and
8.9:1.

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
- **`outline: none` on focus** with nothing in its place, a placeholder as the only label (fact
  `web-placeholder`), or a `<div>` as a button (fact `web-aria-promise`).
- **A Cancel button in a form with no `type`,** which submits the form (fact `web-button-submit`).
- **`alt` text that repeats the file name or says "image of".** Describe the purpose, or use
  `alt=""` for decoration.
- **Reporting a missing `rel="noopener"` as a vulnerability** for current browsers (fact
  `web-blank-noopener`).

## Audit

Severity uses the standard's status words: `BLOCKER`, `DRIFT`, `GAP`, `OVER`, `MIRROR`,
`UNVERIFIABLE-HERE`, `OK` and `N/A`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Untrusted data in an HTML sink | `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `dangerouslySetInnerHTML`, `v-html` fed by input or a template string | `BLOCKER` where input reaches it | `textContent`, or `setHTML()` with DOMPurify as fallback |
| Template auto-escaping | Jinja's `Environment(` without `autoescape`, and `\|safe` or `Markup(` on input | `BLOCKER` where input reaches it, else `GAP` | Turn it on (fact `web-jinja-autoescape`) |
| URLs from input | `href`, `src` or `location` set from input with no scheme check | `GAP` | Allow `http:` and `https:` only (fact `web-owasp-url`) |
| Content Security Policy | None, report-only for good, or `'unsafe-inline'` with hosts and no nonce or hash | `GAP` | A strict policy (fact `web-csp-strict`) |
| CSP in `<meta>` with `frame-ancestors` | The page's `<meta http-equiv>` | `DRIFT`: ignored | A header (fact `web-csp-meta`) |
| Headers set outside the repository | A proxy or host sends the CSP | `MIRROR`, or `UNVERIFIABLE-HERE` | Read the live response headers |
| Third-party scripts and styles | Another origin's `<script src>` or stylesheet without `integrity` | `GAP` | Self-host, or a computed hash (fact `web-sri-openssl`) |
| Integrity hashes that fail | Console integrity errors, or a hash that doesn't match the file | `DRIFT` | Recompute from the file served |
| Text alternatives and language | `<img>` with no `alt`; icon-only buttons with no name; `<html>` without `lang` | `GAP` | Facts `web-wcag-alt`, `web-alt-empty`, `web-wcag-lang` |
| Labels and buttons | Controls with no `<label>`; a form's `<button>` with no `type` | `GAP` | Facts `web-placeholder`, `web-button-submit` |
| Focus and contrast | `outline: none` with no `:focus-visible` style; colors below the ratios in either scheme | `GAP` | Facts `web-wcag-focus-visible`, `web-wcag-contrast` |
| Clickable non-controls | `onclick` on `<div>` or `<span>`, `role="button"` without key handlers | `GAP` | A `<button>` (fact `web-aria-promise`) |
| Motion | Animations outside a reduced-motion query | `GAP` | Fact `web-media-prefs` |
| `noopener noreferrer` everywhere | `rel` on every `target="_blank"` link | `OVER` where the referrer is wanted | `target="_blank"` alone (fact `web-blank-noopener`) |

## Why

### Semantic markup before roles

**The advice.** Native elements first; ARIA only for what HTML can't express, such as a tree view,
with the keyboard pattern the ARIA Authoring Practices Guide gives for it.

**Why.** A `<button>` gets focus, Enter and Space, and its role, from the browser. ARIA changes
only what assistive technology is told, so every keyboard behavior is written and maintained by
hand. W3C's guide to ARIA opens with that warning (fact `web-aria-promise`).

### The accessibility floor

**The advice.** Meet level AA of WCAG 2.2 on every page, starting with the basics above.

**Why.** 2.2 is the version W3C advises, and content that meets it also meets 2.0 and 2.1 (fact
`web-wcag22`), so it satisfies a rule that names an older version. The basics are cheap at
writing time and expensive to retrofit. **The cost:** some brand colors fail contrast, and small
icon buttons need padding.

### Text by default, a sanitizer where HTML is needed

**The advice.** Set text as text, encode for the context, check URL schemes, and send user HTML
through `setHTML()` or DOMPurify, with Trusted Types enforced.

**Why.** Cross-site scripting is input that a parser reads as code. `textContent` and an
auto-escaping template take the parser out of the path (facts `web-owasp-text`,
`web-owasp-url`). A sanitizer built into the browser uses the browser's own parser, so there's
no second, different parse for a payload to change shape in, but Safari lacks it (fact
`web-sethtml`). Trusted Types turns a forgotten sink into an error instead of a hole.

**What others do.** React and similar frameworks escape text by default, and name their raw HTML
APIs as a warning, such as `dangerouslySetInnerHTML`. The risk moves to those and to URLs.

**The cost.** Enforcing Trusted Types breaks libraries that write strings to sinks, until they're
updated or wrapped in a policy. Where no user HTML is shown, skip the sanitizer.

### A strict policy

**The advice.** Nonce or hash based, with `'strict-dynamic'`, `object-src 'none'` and
`base-uri 'none'`.

**Why.** A host allowlist usually includes a host that serves something an attacker can use, so
web.dev calls such policies bypassable (fact `web-csp-strict`). A nonce ties execution to what
the server wrote.

**The cost.** Nonces generated per response, no inline handlers, and pages that can't be cached
whole. **When to choose differently:** a static site, with no server to make nonces, uses
hashes.

### Integrity hashes from the file

**Why.** A compromised CDN serves its code to every site that loads it, and a hash stops a
changed file from running (fact `web-sri-fail`). A guessed hash stops the right file too, which
is the failure assistants cause. **The cost:** a new hash for each upgrade. Self-hosting avoids
both.

### Forms and styles that adapt to the user

**Why.** A label is what a screen reader announces and what a click on the text focuses, and
`autocomplete` lets browsers fill fields correctly (fact `web-wcag-input-purpose`). Browser
validation can be bypassed (fact `web-owasp-validation`). Users choose a dark scheme or reduced
motion for comfort or for medical reasons, such as vestibular motion disorders, and both queries
are widely available (fact `web-media-prefs`).

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked 2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `web-wcag22` | WCAG 2.2 is a W3C Recommendation, last published 2024-12-12, W3C advises using it, and content that meets it meets 2.0 and 2.1 | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | "W3C Recommendation 12 December 2024" and "the W3C advises the use of WCAG 2.2 to maximize future applicability of accessibility efforts" and "Content that conforms to WCAG 2.2 also conforms to WCAG 2.0 and WCAG 2.1." | 2026-10-26 | 2027-04-26 |
| `web-wcag-new` | WCAG 2.2 added criteria including 2.4.11 Focus Not Obscured (Minimum) and 2.5.8 Target Size (Minimum), both AA | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | "The following success criteria are new in WCAG 2.2" and "2.4.11 Focus Not Obscured (Minimum) (AA)" and "2.5.8 Target Size (Minimum) (AA)" | 2026-10-26 | 2027-10-26 |
| `web-wcag-contrast` | Text contrast at AA is 4.5:1, and 3:1 for large text (1.4.3) | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | "The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following" and "Large-scale text and images of large-scale text have a contrast ratio of at least 3:1" | 2026-10-26 | 2027-10-26 |
| `web-wcag-nontext` | Controls and graphics need 3:1 against adjacent colors (1.4.11) | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | "have a contrast ratio of at least 3:1 against adjacent color(s)" | 2026-10-26 | 2027-10-26 |
| `web-wcag-target` | Pointer targets are at least 24 by 24 CSS pixels, with exceptions (2.5.8) | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | "The size of the target for pointer inputs is at least 24 by 24 CSS pixels" | 2026-10-26 | 2027-10-26 |
| `web-wcag-focus-visible` | Keyboard focus must be visible (2.4.7, AA) | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | "Any keyboard operable user interface has a mode of operation where the keyboard focus indicator is visible." | 2026-10-26 | 2027-10-26 |
| `web-wcag-lang` | The page's language must be programmatically determined (3.1.1) | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | "The default human language of each web page can be programmatically determined." | 2026-10-26 | 2027-10-26 |
| `web-wcag-alt` | Non-text content needs a text alternative (1.1.1) | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | "All non-text content that is presented to the user has a text alternative that serves the equivalent purpose" | 2026-10-26 | 2027-10-26 |
| `web-wcag-input-purpose` | The purpose of fields about the user must be programmatically determined (1.3.5, AA) | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | "The purpose of each input field collecting information about the user can be programmatically determined" | 2026-10-26 | 2027-10-26 |
| `web-alt-empty` | An image that only repeats the surrounding text has an empty `alt` | [HTML Standard, images](https://html.spec.whatwg.org/multipage/images.html) | "the alt attribute must be present but its value must be the empty string." | 2026-10-26 | 2027-10-26 |
| `web-aria-promise` | The APG opens with "No ARIA is better than Bad ARIA", and ARIA roles don't give an element keyboard behavior or styling | [ARIA Authoring Practices Guide, Read Me First](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) | "No ARIA is better than Bad ARIA" and "Unlike HTML input elements, ARIA roles do not cause browsers to provide keyboard behaviors or styling." | 2026-10-26 | 2027-10-26 |
| `web-aria-redundant` | ARIA in HTML, a W3C Recommendation, advises against restating an element's implicit role | [ARIA in HTML](https://www.w3.org/TR/html-aria/) | "It is NOT RECOMMENDED for authors to set the ARIA role and aria-* attributes to values that match the implicit ARIA semantics" | 2026-10-26 | 2027-10-26 |
| `web-placeholder` | A placeholder isn't a label | [HTML Standard, input](https://html.spec.whatwg.org/multipage/input.html) | "The placeholder attribute should not be used as an alternative to a label." | 2026-10-26 | 2027-10-26 |
| `web-button-submit` | A `<button>` with no `type`, no `command` or `commandfor`, and not in a `<select>` is a submit button | [HTML Standard, form elements](https://html.spec.whatwg.org/multipage/form-elements.html) | "The attribute's missing value default and invalid value default are both the Auto state." and "the type attribute is in the Auto state, both the command and commandfor content attributes are not present, and the parent node is not a select element" | 2026-10-26 | 2027-10-26 |
| `web-blank-noopener` | A link with `target="_blank"` opens with `noopener` unless it says `opener` | [HTML Standard, links](https://html.spec.whatwg.org/multipage/links.html) | "If element's link types do not include the opener keyword and target is an ASCII case-insensitive match for" | 2026-10-26 | 2027-10-26 |
| `web-owasp-text` | OWASP: HTML entity encoding for HTML contexts, and `textContent` for text set from JavaScript | [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | "use HTML entity encoding for that variable" and "When displaying text with JavaScript, assign it to the textContent property of an ordinary element" | 2026-10-26 | 2027-10-26 |
| `web-owasp-url` | OWASP: allow only http and https URLs from input, and encode parameters with `encodeURIComponent()` | [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | "Allow-list http and HTTPS URLs only" and "use encodeURIComponent() to encode each untrusted query parameter value" | 2026-10-26 | 2027-10-26 |
| `web-owasp-dompurify` | OWASP recommends DOMPurify, kept patched | [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | "OWASP recommends DOMPurify for HTML Sanitization." and "You must regularly patch DOMPurify or other HTML Sanitization libraries that you use." | 2026-10-26 | 2027-04-26 |
| `web-owasp-validation` | OWASP: browser validation can be bypassed, so the server validates too | [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) | "Client-side validation is bypassable; use it for immediate feedback." | 2026-10-26 | 2027-10-26 |
| `web-jinja-autoescape` | Jinja's `Environment` leaves auto-escaping off unless it's configured | [Jinja API](https://jinja.palletsprojects.com/en/stable/api/) | "However autoescaping is not yet enabled by default" | 2026-10-26 | 2027-04-26 |
| `web-innerhtml` | MDN calls `innerHTML` the most common XSS vector | [Element: innerHTML](https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML) | "The innerHTML property is probably the most common vector for cross-site scripting (XSS) attacks" | 2026-10-26 | 2027-10-26 |
| `web-sethtml` | `Element.setHTML()` isn't Baseline: Chrome 146 and Firefox 148 ship it, Safari doesn't | [Element: setHTML()](https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTML), [browser-compat-data](https://raw.githubusercontent.com/mdn/browser-compat-data/main/api/Element.json) | "This feature is not Baseline because it does not work in some of the most widely-used browsers." | 2026-10-26 | 2027-04-26 |
| `web-sethtml-tt` | `setHTML()` isn't gated by Trusted Types, and re-parsing its output with `innerHTML` is unsafe | [Element: setHTML()](https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTML) | "it is not secured or validated using the Trusted Types API" and "it is still not safe to serialize the HTML and re-parse it using innerHTML" | 2026-10-26 | 2027-04-26 |
| `web-trusted-types` | Trusted Types is Baseline, newly available since February 2026 | [Trusted Types API](https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API) | "Baseline 2026" and "Since February 2026, this feature works across the latest devices and browser versions." | 2026-10-26 | 2027-04-26 |
| `web-tt-enforce` | With `require-trusted-types-for`, a string assigned to a sink throws | [Trusted Types API](https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API) | "passing strings into injection sinks will result in a TypeError exception" | 2026-10-26 | 2027-10-26 |
| `web-dompurify-tt` | DOMPurify returns `TrustedHTML` with `RETURN_TRUSTED_TYPE: true` | [DOMPurify README](https://raw.githubusercontent.com/cure53/DOMPurify/main/README.md) | "it tries to return a `TrustedHTML` value instead of a string" | 2026-10-26 | 2027-04-26 |
| `web-csp-strict` | web.dev's strict CSP, and its finding that allowlist policies can be bypassed | [Mitigate XSS with a strict CSP](https://web.dev/articles/strict-csp) | "Content-Security-Policy: script-src 'nonce-{RANDOM}' 'strict-dynamic'; object-src 'none'; base-uri 'none';" and "This type of CSP is called an allowlist CSP. They require a lot of customization and can be bypassed by attackers." | 2026-10-26 | 2027-10-26 |
| `web-csp-nonce` | A nonce is new on every response | [CSP Level 3](https://www.w3.org/TR/CSP3/) | "the server MUST generate a unique value each time it transmits a policy" | 2026-10-26 | 2027-10-26 |
| `web-csp-meta` | A `<meta>` policy ignores `report-uri`, `frame-ancestors` and `sandbox` | [CSP Level 3](https://www.w3.org/TR/CSP3/) | "Neither are the report-uri, frame-ancestors, and sandbox directives." | 2026-10-26 | 2027-10-26 |
| `web-sri-fail` | A response that fails its integrity check isn't rendered or run | [Subresource Integrity](https://www.w3.org/TR/SRI/) | "The user agent will refuse to render or execute responses that fail an integrity check" | 2026-10-26 | 2027-10-26 |
| `web-sri-openssl` | The SRI spec computes a hash with OpenSSL: `openssl dgst -sha384 -binary`, then `openssl base64 -A` | [Subresource Integrity](https://www.w3.org/TR/SRI/) | "OpenSSL, for example, is quite commonly available." | 2026-10-26 | 2027-10-26 |
| `web-baseline` | Baseline "widely available" means 30 months after the core browsers all ship a feature | [Baseline, web.dev](https://web.dev/baseline) | "Widely available: 30 months have passed since the newly interoperable date." | 2026-10-26 | 2027-10-26 |
| `web-media-prefs` | `prefers-reduced-motion` and `prefers-color-scheme` are Baseline widely available, since January 2020; MDN names vestibular motion disorders as a reason to reduce motion | [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion), [prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme) | "It's been available across browsers since January 2020." and "vestibular motion disorders" | 2026-10-26 | 2027-10-26 |
| `web-color-scheme` | The `color-scheme` property is Baseline widely available, since January 2022 | [color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme) | "It's been available across browsers since January 2022." | 2026-10-26 | 2027-10-26 |
| `web-focus-visible` | `:focus-visible` is Baseline widely available, since March 2022 | [:focus-visible](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-visible) | "It's been available across browsers since March 2022." | 2026-10-26 | 2027-10-26 |
| `web-whatwg-license` | The HTML Standard is under CC BY 4.0 | [HTML Standard, acknowledgments](https://html.spec.whatwg.org/multipage/acknowledgements.html) | "This work is licensed under a Creative Commons Attribution 4.0 International License." | 2026-10-26 | 2027-10-26 |
| `web-w3c-license` | W3C's CSP, SRI and ARIA in HTML specs carry the permissive document license; WCAG 2.2 carries the document use rules | [CSP Level 3](https://www.w3.org/TR/CSP3/), [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | "liability, trademark and permissive document license rules apply" and "liability, trademark and document use rules apply." | 2026-10-26 | 2027-10-26 |
| `web-webdev-license` | web.dev's text is CC BY 4.0, and its code samples Apache 2.0 | [Mitigate XSS with a strict CSP](https://web.dev/articles/strict-csp) | "licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License" | 2026-10-26 | 2027-10-26 |

## Sources

Every rule here is in this module's own words. Share-alike sources, MDN prose and OWASP, are
quoted only briefly, with attribution, and each quote is a dated fact above.

| Source | Used for | License |
|---|---|---|
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Accessibility criteria and levels | W3C document use rules (fact `web-w3c-license`): short quotes, facts in our own words |
| [ARIA in HTML](https://www.w3.org/TR/html-aria/) and the [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) | When to use ARIA | W3C permissive document license: short quotes |
| [HTML Standard](https://html.spec.whatwg.org/multipage/) (WHATWG) | Images, links, forms and buttons | CC BY 4.0 (fact `web-whatwg-license`): short quotes, with attribution |
| [CSP Level 3](https://www.w3.org/TR/CSP3/) and [Subresource Integrity](https://www.w3.org/TR/SRI/) | Nonces, `<meta>` policies, integrity checks | W3C permissive document license: short quotes |
| [Mitigate XSS with a strict CSP](https://web.dev/articles/strict-csp) and [Baseline](https://web.dev/baseline) (web.dev) | The strict policy, and Baseline's stages | CC BY 4.0, code Apache 2.0 (fact `web-webdev-license`): short quotes, with attribution |
| [MDN Web Docs](https://developer.mozilla.org/) by Mozilla Contributors: innerHTML, setHTML(), Trusted Types API, color-scheme, prefers-reduced-motion, prefers-color-scheme, :focus-visible | Sinks, sanitizer and Trusted Types behavior, Baseline statuses | Prose CC BY-SA 2.5 or later: short quotes, with attribution; nothing adapted |
| [MDN browser-compat-data](https://github.com/mdn/browser-compat-data) | Which browsers ship `setHTML()` | CC0 1.0: a fact |
| [OWASP Cross Site Scripting Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) and [Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) cheat sheets | Encoding by context, URL checks, DOMPurify, server validation | CC BY-SA 4.0: short quotes, with attribution; nothing adapted |
| [DOMPurify README](https://github.com/cure53/DOMPurify) | `RETURN_TRUSTED_TYPE` | MPL-2.0 or Apache-2.0: a fact with a short quote |
| [Jinja API](https://jinja.palletsprojects.com/en/stable/api/) | Auto-escaping's default | BSD-3-Clause: a fact with a short quote |
