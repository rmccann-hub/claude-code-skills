# HTML and CSS coding

Read this for writing, reviewing or fixing HTML and CSS: semantic markup, the accessibility basics
every page needs, forms, and modern CSS with dark mode and reduced motion.

Browser-side security, such as escaping output, `innerHTML`, sanitizing, Content Security
Policy, Trusted Types, Subresource Integrity and `noopener`, is `web-security`'s. JavaScript and
TypeScript are `javascript-coding`'s. A full accessibility audit with assistive technology
belongs to a planned accessibility module, and design tokens to a planned visual-design skill.
Pinning versions, lockfiles and CI are the project-bootstrap-and-audit standard's *Language
toolchains*. HTML email isn't covered.

## Rules

1. **Use the HTML element that means what you need,** and ARIA only where HTML has nothing.
2. **Meet WCAG 2.2 level AA's basics on every page:** language, text alternatives, labels,
   headings, visible focus, contrast and target size.
3. **Label every form control,** give it its real `type` and `autocomplete`, give every button a
   `type`, and validate again on the server.
4. **Style with custom properties, grid and flex,** honor `prefers-color-scheme` and
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
- **A form that changes state needs CSRF protection on the server,** such as a token checked
  with each request, where the session rides in a cookie (fact `web-owasp-csrf`). The check is
  server code; this module marks where a form needs it.

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

- **`outline: none` on focus** with nothing in its place, a placeholder as the only label (fact
  `web-placeholder`), or a `<div>` as a button (fact `web-aria-promise`).
- **A Cancel button in a form with no `type`,** which submits the form (fact `web-button-submit`).
- **`alt` text that repeats the file name or says "image of".** Describe the purpose, or use
  `alt=""` for decoration.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Text alternatives and language | `<img>` with no `alt`; icon-only buttons with no name; `<html>` without `lang` | `GAP` | Facts `web-wcag-alt`, `web-alt-empty`, `web-wcag-lang` |
| Labels and buttons | Controls with no `<label>`; a form's `<button>` with no `type` | `GAP` | Facts `web-placeholder`, `web-button-submit` |
| Focus and contrast | `outline: none` with no `:focus-visible` style; colors below the ratios in either scheme | `GAP` | Facts `web-wcag-focus-visible`, `web-wcag-contrast` |
| Clickable non-controls | `onclick` on `<div>` or `<span>`, `role="button"` without key handlers | `GAP` | A `<button>` (fact `web-aria-promise`) |
| Motion | Animations outside a reduced-motion query | `GAP` | Fact `web-media-prefs` |

## Why

### Semantic markup before roles

**The advice.** Native elements first; ARIA only for what HTML can't express, such as a tree view,
with the keyboard pattern the ARIA Authoring Practices Guide gives.

**Why.** A `<button>` gets focus, Enter, Space and its role from the browser. ARIA changes only
what assistive technology is told, so each keyboard behavior is hand-written and maintained.
W3C's guide to ARIA opens with that warning (fact `web-aria-promise`).

### The accessibility floor

**The advice.** Meet level AA of WCAG 2.2 on every page, starting with the basics above.

**Why.** W3C advises 2.2, and content meeting it meets 2.0 and 2.1 (fact `web-wcag22`), so it
satisfies a rule naming an older version. The basics are cheap to write and costly to retrofit. **The cost:** some brand colors fail contrast, and small
icon buttons need padding.

### Forms and styles that adapt to the user

**Why.** A label is what a screen reader announces and what a click on the text focuses, and
`autocomplete` lets browsers fill fields correctly (fact `web-wcag-input-purpose`). Browser
validation can be bypassed (fact `web-owasp-validation`). Users choose a dark scheme or reduced
motion for comfort or for medical reasons, such as vestibular motion disorders, and both queries
are widely available (fact `web-media-prefs`).

## Facts

Each named above, or in `web-security`, by its ID. Checked 2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `web-wcag22` | A W3C Recommendation (2024-12-12), advised, and meeting 2.0 and 2.1 | [WCAG](https://www.w3.org/TR/WCAG22/) | "W3C Recommendation 12 December 2024" and "W3C advises the use of WCAG 2.2" and "also conforms to WCAG 2.0 and WCAG 2.1" | 2026-10-26 | 2027-04-26 |
| `web-wcag-new` | 2.2 added 2.4.11 and 2.5.8, both AA | [WCAG](https://www.w3.org/TR/WCAG22/) | "2.4.11 Focus Not Obscured (Minimum) (AA)" and "2.5.8 Target Size (Minimum) (AA)" | 2026-10-26 | 2027-10-26 |
| `web-wcag-contrast` | Text contrast is 4.5:1, large text 3:1 (1.4.3) | [WCAG](https://www.w3.org/TR/WCAG22/) | "a contrast ratio of at least 4.5:1" and "Large-scale text and images of large-scale text have a contrast ratio of at least 3:1" | 2026-10-26 | 2027-10-26 |
| `web-wcag-nontext` | Controls: 3:1 against neighbors (1.4.11) | [WCAG](https://www.w3.org/TR/WCAG22/) | "have a contrast ratio of at least 3:1 against adjacent color(s)" | 2026-10-26 | 2027-10-26 |
| `web-wcag-target` | Targets 24 by 24 CSS pixels (2.5.8) | [WCAG](https://www.w3.org/TR/WCAG22/) | "at least 24 by 24 CSS pixels" | 2026-10-26 | 2027-10-26 |
| `web-wcag-focus-visible` | Keyboard focus is visible (2.4.7) | [WCAG](https://www.w3.org/TR/WCAG22/) | "the keyboard focus indicator is visible." | 2026-10-26 | 2027-10-26 |
| `web-wcag-lang` | The page states its language (3.1.1) | [WCAG](https://www.w3.org/TR/WCAG22/) | "default human language of each web page can be programmatically determined" | 2026-10-26 | 2027-10-26 |
| `web-wcag-alt` | Text alternatives (1.1.1) | [WCAG](https://www.w3.org/TR/WCAG22/) | "non-text content that is presented to the user has a text alternative" | 2026-10-26 | 2027-10-26 |
| `web-wcag-input-purpose` | Fields about the user state their purpose (1.3.5) | [WCAG](https://www.w3.org/TR/WCAG22/) | "purpose of each input field collecting information about the user" | 2026-10-26 | 2027-10-26 |
| `web-alt-empty` | A redundant image has `alt=""` | [HTML, images](https://html.spec.whatwg.org/multipage/images.html) | "its value must be the empty string" | 2026-10-26 | 2027-10-26 |
| `web-aria-promise` | Roles give no keyboard behavior or styling | [APG](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) | "No ARIA is better than Bad ARIA" and "ARIA roles do not cause browsers to provide keyboard behaviors or styling" | 2026-10-26 | 2027-10-26 |
| `web-aria-redundant` | Don't restate implicit roles | [ARIA in HTML](https://www.w3.org/TR/html-aria/) | "NOT RECOMMENDED for authors to set the ARIA role and aria-* attributes to values that match the implicit ARIA semantics" | 2026-10-26 | 2027-10-26 |
| `web-placeholder` | A placeholder isn't a label | [HTML, input](https://html.spec.whatwg.org/multipage/input.html) | "should not be used as an alternative to a label" | 2026-10-26 | 2027-10-26 |
| `web-button-submit` | A `<button>` with no `type` submits | [HTML, forms](https://html.spec.whatwg.org/multipage/form-elements.html) | "missing value default and invalid value default are both the Auto state" and "in the Auto state, both the command and commandfor content attributes are not present" | 2026-10-26 | 2027-10-26 |
| `web-owasp-validation` | Browser validation can be bypassed | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) | "Client-side validation is bypassable" | 2026-10-26 | 2027-10-26 |
| `web-owasp-csrf` | CSRF tokens where cookies carry the session | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) | "CSRF tokens are still essential for web applications that rely on cookies" | 2026-10-26 | 2027-10-26 |
| `web-baseline` | Widely available: 30 months on | [web.dev](https://web.dev/baseline) | "30 months have passed since the newly interoperable date" | 2026-10-26 | 2027-10-26 |
| `web-media-prefs` | Both queries widely available since January 2020; vestibular disorders | [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion), [prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme) | "It's been available across browsers since January 2020." and "vestibular motion disorders" | 2026-10-26 | 2027-10-26 |
| `web-color-scheme` | Widely available since January 2022 | [color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme) | "It's been available across browsers since January 2022." | 2026-10-26 | 2027-10-26 |
| `web-focus-visible` | Widely available since March 2022 | [:focus-visible](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-visible) | "It's been available across browsers since March 2022." | 2026-10-26 | 2027-10-26 |
| `web-whatwg-license` | The HTML Standard is CC BY 4.0 | [HTML](https://html.spec.whatwg.org/multipage/acknowledgements.html) | "Creative Commons Attribution 4.0 International License" | 2026-10-26 | 2027-10-26 |
| `web-w3c-license` | CSP, SRI, ARIA in HTML: permissive license; WCAG: document use rules | [CSP Level 3](https://www.w3.org/TR/CSP3/), [WCAG](https://www.w3.org/TR/WCAG22/) | "permissive document license rules apply" and "document use rules apply." | 2026-10-26 | 2027-10-26 |
| `web-webdev-license` | web.dev's text is CC BY 4.0, its code Apache 2.0 | [web.dev](https://web.dev/articles/strict-csp) | "Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License" | 2026-10-26 | 2027-10-26 |

## Sources

Rules are in this module's own words. Share-alike sources, MDN and OWASP, are quoted briefly,
with attribution, each quote a dated fact.

| Source | Used for | License |
|---|---|---|
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [ARIA in HTML](https://www.w3.org/TR/html-aria/), [APG](https://www.w3.org/WAI/ARIA/apg/) | Criteria, and when to use ARIA | W3C document licenses (fact `web-w3c-license`): short quotes |
| [HTML Standard](https://html.spec.whatwg.org/multipage/) | Images, forms, buttons | CC BY 4.0 (fact `web-whatwg-license`): short quotes, with attribution |
| [Baseline](https://web.dev/baseline) (web.dev) | Baseline's stages | CC BY 4.0, code Apache 2.0 (fact `web-webdev-license`): short quotes, with attribution |
| [MDN](https://developer.mozilla.org/) by Mozilla Contributors | Baseline statuses | CC BY-SA 2.5 or later: short quotes, with attribution |
| OWASP: [Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html), [CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) | Server validation, CSRF tokens | CC BY-SA 4.0: short quotes, with attribution |
