# Facts: Vale, and what other style guides say

Read this when a version, a tool's behavior, or another guide's rule matters. The other files
here name a fact by its ID, such as `vale-current`, instead of repeating it. Each fact carries
its source, a short quote, the date it was checked and a date to check it again by.

Checked 2026-10-05.

## Vale

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `vale-current` | Vale's newest release is v3.24.0 | `git ls-remote --tags https://github.com/vale-cli/vale` | `refs/tags/v3.24.0` | 2026-10-05 | 2027-01-05 |
| `vale-module` | Vale installs with `go install`, from the module `github.com/vale-cli/vale/v3` | [go.mod at v3.24.0](https://raw.githubusercontent.com/vale-cli/vale/v3.24.0/go.mod) | "module github.com/vale-cli/vale/v3" | 2026-10-05 | 2027-04-05 |
| `vale-license` | Vale is under the MIT license | [LICENSE at v3.24.0](https://raw.githubusercontent.com/vale-cli/vale/v3.24.0/LICENSE) | "MIT License" | 2026-10-05 | 2027-04-05 |
| `vale-packages` | A package is a ZIP holding one folder named for it. `.vale.ini` lists it by URL under `Packages`, and `vale sync` installs it | [Packages](https://vale.sh/docs/keys/packages) | "A URL to a .zip archive." and "the archive has to hold one folder with that name" and "Packages lists what vale sync installs into the StylesPath" | 2026-10-05 | 2027-04-05 |
| `vale-layers` | A package's configuration is overridden by later packages, and by the project's own | [Packages](https://vale.sh/docs/keys/packages) | "the first package is overridden by the second, and local configuration overrides both" | 2026-10-05 | 2027-04-05 |
| `vale-sections` | In `.vale.ini`, a later section matching the same files replaces the earlier list of styles | [.vale.ini](https://vale.sh/docs/vale-ini) | "A later matching section replaces the list rather than adding to it." | 2026-10-05 | 2027-04-05 |
| `vale-exceptions` | Capitalization and substitution rules take a list of exceptions, and accept the project's vocabularies unless told not to | [capitalization](https://vale.sh/docs/checks/capitalization) | "An array of strings to be ignored." and "If false, disables all active vocabularies for this rule (default: true)." | 2026-10-05 | 2027-04-05 |

## Other style guides

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `google-sentence-case` | Google's developer documentation style guide puts headings in sentence case | [Headings and titles](https://developers.google.com/style/headings) | "Use sentence case for headings and titles." | 2026-10-05 | 2027-04-05 |
| `ms-sentence-case` | Microsoft's style guide uses sentence-style capitalization: the first word and proper nouns | [Capitalization](https://learn.microsoft.com/en-us/style-guide/capitalization) | "Microsoft style uses sentence-style capitalization." | 2026-10-05 | 2027-04-05 |
| `google-just` | Google's word list calls "just" usually filler, and asks writers to try cutting "simply" | [Word list](https://developers.google.com/style/word-list) | "Usually, just is a filler word that you can delete without affecting your meaning." and "Try eliminating this word from the sentence because usually the same meaning can be conveyed without it." | 2026-10-05 | 2027-04-05 |
| `google-leverage` | Google's word list avoids "leverage" where it means "use" | [Word list](https://developers.google.com/style/word-list) | "Avoid using if you mean use." | 2026-10-05 | 2027-04-05 |
| `google-license` | Google's developer documentation is under CC BY 4.0, and its code samples under Apache 2.0 | [Google developer documentation style guide](https://developers.google.com/style) | "licensed under the Creative Commons Attribution 4.0 License" | 2026-10-05 | 2027-04-05 |
| `govuk-avoid` | GOV.UK makes plain English mandatory, and lists "leverage" and "robust" among the words to avoid | [Style guide, A to Z](https://www.gov.uk/guidance/style-guide/a-to-z) | "Plain English is mandatory for all of GOV.UK" and "leverage (unless in the financial sense)" and "robust (unless talking about a sturdy object)" | 2026-10-05 | 2027-04-05 |
