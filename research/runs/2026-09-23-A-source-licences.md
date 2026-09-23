# Verification: A-source-licences (2026-09-23)

Checked by the receiving session on 2026-09-23 for the licences the authoring review relies on.

| Claim | Status | Checked against |
|---|---|---|
| OWASP Cheat Sheet Series is CC BY-SA 4.0 | verified | github.com/OWASP/CheatSheetSeries README badge and licence link |
| Agent Skills: documentation CC BY 4.0, code Apache 2.0 | verified | github.com/agentskills/agentskills README: "Code in this repository is licensed under Apache 2.0"; "Documentation is licensed under CC-BY-4.0" |
| PowerShell-Docs: documentation under Creative Commons, code under MIT | verified | github.com/MicrosoftDocs/PowerShell-Docs README, Licenses section |
| Epicor and SOLIDWORKS terms | unverifiable | terms pages refused the fetch; treated as restricted, which is the safe reading |
| All other rows | not yet checked | each is checked before a skill relies on it |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: A-source-licences · FORM: research-result v1 · DATE: 2026-09-23 · BY: Claude Code subagent with web tools

# Licences of reference sources: research result

## Summary table

| Source | Licence | Quote | Paraphrase | Adapt code | Attribution needed | Confidence |
|---|---|---|---|---|---|---|
| L1 Epicor (epicor.com terms, Kinetic help, EpicCare, Learning Center) | Proprietary. No public licence found. The Terms of Use page could not be read (HTTP 403) | No permission found | Not addressed by any source read | No public code examples found. Naming tables, fields, BOs or REST routes is not addressed | n/a | Low |
| L2 SOLIDWORKS API Help and Dassault Systemes terms | Proprietary. API sample code: royalty-free, non-exclusive licence for licensed SOLIDWORKS users (search-index wording only) | No permission found. Site terms (search index) limit use to personal, informational, noncommercial purposes | Not addressed | Licence found only for licensed users building SOLIDWORKS-related applications. Confidentiality provisions of the SOLIDWORKS licence apply. No grant to publish found | No notice wording found | Low |
| L3 github/gitignore | CC0 1.0 Universal | Yes | Yes | Yes | None required | High |
| L4 Keep a Changelog | MIT (site footer) | Yes | Yes | Yes | MIT copyright and permission notice (copyright line not read) | Medium |
| L5 Conventional Commits | Spec page: CC BY 3.0. Site repository: MIT | Yes | Yes | Yes | CC BY 3.0 §4(b) credit. MIT notice for repository code | Medium |
| L5 Semantic Versioning | CC BY 3.0 | Yes | Yes | Yes | CC BY 3.0 §4(b) credit | High |
| L6 markdownlint rule docs | MIT | Yes | Yes | Yes | "Copyright (c) David Anson" plus the MIT permission notice | High |
| L7 Rust book | LICENSE-MIT and LICENSE-APACHE (Apache 2.0) in the repository root | Yes | Yes | Yes | MIT notice. Apache 2.0 §4 conditions | Medium |
| L8 Google style guides | CC BY 3.0 | Yes | Yes | Yes | CC BY 3.0 §4(b) credit | High |
| L9 Google OR-Tools | Docs text: CC BY 4.0. Code samples and repository: Apache 2.0 | Yes | Yes | Yes | Credit Google and link back. CC BY 4.0 §3(a). Apache 2.0 §4 | High |
| L10 GOV.UK Design System | Docs: Open Government Licence v3.0. Code, including sample code in the docs: MIT | Yes | Yes | Yes | OGL attribution (licence text not read). MIT notice | High |
| L11 Arch Wiki | GFDL 1.3 or later (indirect: the wiki denied the fetch tool) | Under GFDL conditions | Under GFDL conditions | Under GFDL conditions, "unless otherwise noted" | GFDL conditions (licence text not read) | Medium |
| L11 Bazzite docs | None stated. No licence file in the docs repository. Nav item "License" links to the Bazzite OS repository's Apache 2.0 LICENSE | Not stated | Not stated | Not stated | Not stated | Medium |
| L11 Universal Blue | Website repository: GPL-3.0. Archived "Website and documentation" repository: CC BY-SA 4.0 | Yes, under licence conditions | Copyleft or ShareAlike applies | Copyleft or ShareAlike applies | GPL-3.0 or CC BY-SA 4.0 conditions | Medium |
| L11 ProtonDB | Not found (search index only: report data exports under ODbL) | Not found | Not found | n/a | Not found | Low |
| L11 PCGamingWiki | Not found (search index only: CC BY-NC-SA, version not shown) | Not found | Not found | Not found | Not found | Low |
| L12 OWASP Cheat Sheet Series | CC BY-SA 4.0 | Yes, with attribution | ShareAlike applies to adaptations | ShareAlike applies to adaptations | CC BY-SA 4.0 §3(a) and §3(b) | High |
| L13 MDN Web Docs | Prose: CC BY-SA 2.5 or any later version. Code added on or after 2010-08-20: CC0. Older code: MIT | Yes, with attribution | ShareAlike applies to adaptations | Yes | Prose: title, link, "Mozilla Contributors", changes described. CC0 code: none | High |
| L14 PowerShell docs (Microsoft Learn, PowerShell-Docs) | Docs: CC BY 4.0. Code: MIT. Follows the CC BY 4.0 / MIT split | Yes | Yes | Yes | CC BY 4.0 §3(a). "Copyright (c) Microsoft Corporation" plus MIT notice | High |
| L15 Python docs | Text: PSF License Version 2. Code (from 3.8.6): PSF License Version 2 and Zero-Clause BSD | Yes, PSF conditions | Yes, PSF conditions | Yes, under 0BSD | Text: keep PSF licence and copyright notice, summarise changes. 0BSD code: none | High |
| L15 pytest docs | MIT | Yes | Yes | Yes | "Copyright (c) 2004 Holger Krekel and others" plus MIT notice | High |
| L16 Agent Skills specification | Docs, including the specification: CC BY 4.0. Code: Apache 2.0 | Yes | Yes | Yes | CC BY 4.0 §3(a). Apache 2.0 §4 | High |
| L17 Anthropic docs (platform.claude.com, code.claude.com) | No licence stated. "All rights reserved" | No permission found | Not addressed | Not addressed | n/a | Medium |

## Findings

### L1. Epicor: epicor.com terms of use, Kinetic application help, EpicCare knowledge base, Epicor Learning Center
- **Licence:** Proprietary. No public licence for Epicor documentation was found. Epicor's Terms of Use page exists, but it and the other www.epicor.com pages tried returned HTTP 403 to the fetch tool (one PDF link there returned 404), so its text was not read.
- **Reuse:** (a) quote and (b) paraphrase: no permission found in any source read. (c) adapt code: no public Epicor code examples were found. Is the documentation described as confidential or licensed only to customers? No page read calls it confidential. The Kinetic online help says access "requires an active Epicor ERP session". EpicCare and the Kinetic developer portal are login pages. One ERP 10.2 help topic can be read without a session and carries only a copyright footer. Can a public document name Epicor tables, fields, business objects and REST API routes, and include short original code examples against them? No source read addresses this. For an unverified search-index lead on the Terms of Use wording, see Not found.
- **Sources:**
  - [Unable to Load Online Help (Kinetic help)](https://help.epicor.com/Kinetic/112400/ENU/Standard/ModuleHeaders/GettingStartedwithEpicorERP.html): "Access to online help requires an active Epicor ERP session. Please launch help from within the application."; footer "Epicor ERP - Epicor Software Corporation ©" (read 2026-09-23)
  - [Unable to Load Online Help (ERP 10.2.700 help overview)](https://help.epicor.com/erp/102700/enu/standard/ModuleHeaders/SystemOvrvw.html): "Access to online help requires an active Epicor ERP session. Please launch help from within the application." (read 2026-09-23)
  - [Material Backflush Hierarchy for Labor Entry Process](https://help.epicor.com/erp/102700/enu/standard/FeaturesSupplyChain/inv_materialbackflush.html?Version=3.2.700.0): the topic body was readable without a session, and no licence or confidentiality statement was seen. Footer: "Epicor ERP 10.2 - Epicor Software Corporation © 2020" (read 2026-09-23)
  - [EpicCare Login - EpicCare](https://epiccare.epicor.com/epiccare): page title "EpicCare Login - EpicCare". The body loads in the browser, and the fetch tool saw no terms (read 2026-09-23)
  - [Epicor Kinetic - Login](https://kinetic.developer.epicor.com/): "© 2018 Epicor Software Corporation". The sign-in is for Epicor ISV partners or Epicor employees (read 2026-09-23)
  - [Terms | Epicor](https://www.epicor.com/en-us/company/compliance/terms/): not read, HTTP 403. The en-au, en-uk and /en/ variants and [Epicor Legal Information](https://www.epicor.com/en-us/company/legal/) also returned 403 (attempted 2026-09-23)
  - [Epicor Learning Center](https://learncenter.epicor.com/learn): not read. The page returned only "Loading" (attempted 2026-09-23)
- **Confidence:** Low. The central terms page could not be read.

### L2. SOLIDWORKS API Help (help.solidworks.com) and Dassault Systemes terms
- **Licence:** Proprietary. The search engine's index of the API Help Welcome pages shows these terms for sample code: licensed SOLIDWORKS users get a royalty-free, non-exclusive licence to the samples for building SOLIDWORKS-related applications, intellectual property stays with SOLIDWORKS, and the SOLIDWORKS licence's confidentiality provisions apply. The fetch tool received only the portal shell of every help.solidworks.com topic, and www.solidworks.com/terms-use returned HTTP 503. None of this wording was read directly.
- **Reuse:** (a) quote and (b) paraphrase: no permission found for public reuse of help text. The site Terms of Use, per the search index, limit materials to personal, informational and noncommercial use. (c) adapt examples: the only licence found is for licensed SOLIDWORKS users, "in connection with building applications related to SOLIDWORKS", and confidentiality provisions apply. No grant to publish adapted examples in a public repository was found, and no notice wording was found.
- **Sources:**
  - [SOLIDWORKS Web Help](https://help.solidworks.com/): footer link "Terms of Use" goes to https://www.solidworks.com/terms-use and "Privacy Policy" goes to https://discover.3ds.com/privacy-policy (read 2026-09-23)
  - [Welcome - 2024 - SOLIDWORKS Design Help (API)](https://help.solidworks.com/2024/English/api/sldworksapiprogguide/Welcome.htm): the topic body was not returned to the fetch tool. Exact-phrase search queries returned this URL for "in connection with building applications related to SOLIDWORKS", "royalty-free, non-exclusive license for these samples, or parts thereof", "is only intended to demonstrate ways of using the SOLIDWORKS API", "Intellectual property rights of the samples remain with" and "Any confidentiality provisions of the SOLIDWORKS license apply to the samples" (searched 2026-09-23)
  - [Terms of Use | SOLIDWORKS](https://www.solidworks.com/terms-use): not read, HTTP 503 on three attempts. The exact-phrase query "for your personal, informational, and noncommercial purposes" returned this URL first (searched 2026-09-23)
  - [Legal Notices - 2025 - SOLIDWORKS Help](https://help.solidworks.com/2025/English/SolidWorks/sldworks/c_copyright_solidworks.htm): the topic body was not returned to the fetch tool (attempted 2026-09-23)
- **Confidence:** Low. The wording comes from search-index matches, not direct reads.

### L3. GitHub gitignore templates (github.com/github/gitignore)
- **Licence:** CC0 1.0 Universal.
- **Reuse:** The licence permits (a) quoting, (b) paraphrasing and (c) adapting. CC0 waives copyright and related rights as far as the law allows and has a public licence fallback. It requires no attribution.
- **Sources:**
  - [github/gitignore LICENSE](https://github.com/github/gitignore/blob/main/LICENSE): "CC0 1.0 Universal"; "To the greatest extent permitted by, but not in contravention of, applicable law, Affirmer hereby overtly, fully, permanently" (read 2026-09-23)
  - [github/gitignore](https://github.com/github/gitignore): About sidebar licence "CC0-1.0" (read 2026-09-23)
- **Confidence:** High.

### L4. Keep a Changelog (keepachangelog.com)
- **Licence:** MIT, per the site footer. No separate licence is stated for the text or the template.
- **Reuse:** MIT permits (a), (b) and (c). Its condition is that the copyright notice and permission notice be included in all copies or substantial portions (MIT wording quoted under L6). The project's own copyright line was not read (see Not found).
- **Sources:**
  - [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/): "Keep a Changelog is MIT licensed", linking to https://choosealicense.com/licenses/mit/ (read 2026-09-23)
  - [Keep a Changelog 1.0.0](https://keepachangelog.com/en/1.0.0/): "Keep a Changelog is MIT licensed" (read 2026-09-23)
- **Confidence:** Medium. Only the footer was read.

### L5a. Conventional Commits specification (conventionalcommits.org)
- **Licence:** The specification page states CC BY 3.0. The website repository's LICENSE file is MIT.
- **Reuse:** CC BY 3.0 permits (a), (b) and (c) with credit. §4(b) requires keeping copyright notices intact and, for an adaptation, "a credit identifying the use of the Work in the Adaptation" (clause text quoted under L8 from the same licence). Code in the site repository is MIT.
- **Sources:**
  - [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/): under the heading "License", the link text "Creative Commons - CC BY 3.0" points to https://creativecommons.org/licenses/by/3.0/. The dash is as rendered by the fetch tool (read 2026-09-23)
  - [conventionalcommits.org LICENSE](https://github.com/conventional-commits/conventionalcommits.org/blob/master/LICENSE): "MIT License"; "Copyright (c) 2018 Conventional Changelog" (read 2026-09-23)
- **Confidence:** Medium. The page and the repository state different licences.

### L5b. Semantic Versioning (semver.org)
- **Licence:** CC BY 3.0.
- **Reuse:** Permits (a), (b) and (c) with credit under CC BY 3.0 §4(b) (clause text under L8).
- **Sources:**
  - [Semantic Versioning 2.0.0](https://semver.org/): heading "License", "Creative Commons ― CC BY 3.0", linking to https://creativecommons.org/licenses/by/3.0/ (read 2026-09-23)
  - [semver/semver semver.md](https://github.com/semver/semver/blob/master/semver.md): "Creative Commons ― CC BY 3.0" (read 2026-09-23)
  - [semver/semver CITATION.cff](https://github.com/semver/semver/blob/master/CITATION.cff): `license: "CC-BY-3.0"` (read 2026-09-23)
- **Confidence:** High.

### L6. markdownlint rule documentation (github.com/DavidAnson/markdownlint)
- **Licence:** MIT. The rule documentation (doc/Rules.md, doc/md001.md and so on) is in the same repository, and the MIT grant covers "this software and associated documentation files".
- **Reuse:** Permits (a), (b) and (c). The copyright notice and permission notice must be included in all copies or substantial portions.
- **Sources:**
  - [markdownlint LICENSE](https://github.com/DavidAnson/markdownlint/blob/main/LICENSE): "The MIT License (MIT)"; "Copyright (c) David Anson"; "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software." (read 2026-09-23)
  - [markdownlint README](https://github.com/DavidAnson/markdownlint/blob/main/README.md): "See Rules.md for more details." (read 2026-09-23)
- **Confidence:** High.

### L7. The Rust Programming Language book (doc.rust-lang.org/book, github.com/rust-lang/book)
- **Licence:** The repository root holds LICENSE-MIT and LICENSE-APACHE (Apache License 2.0), and GitHub shows "Apache-2.0, MIT licenses found". The README has no licence statement. No source read says how the prose and the code listings (the listings/ directory) are each licensed, or whether the two licences apply together or as alternatives. A print edition is sold by No Starch Press.
- **Reuse:** Permits (a), (b) and (c) under the repository licence files. MIT requires the copyright and permission notice. Apache 2.0 §4 requires a copy of the licence, notices on modified files, and retained notices (§4 text quoted under L9).
- **Sources:**
  - [rust-lang/book LICENSE-MIT](https://github.com/rust-lang/book/blob/main/LICENSE-MIT): "Copyright (c) 2010 The Rust Project Developers" (read 2026-09-23)
  - [rust-lang/book LICENSE-APACHE](https://github.com/rust-lang/book/blob/main/LICENSE-APACHE): "Apache License"; "Version 2.0, January 2004" (read 2026-09-23)
  - [rust-lang/book](https://github.com/rust-lang/book): "Apache-2.0, MIT licenses found". The README has no licence section (read 2026-09-23)
  - [Title page](https://doc.rust-lang.org/book/title-page.html): "This text is available in paperback and ebook format from No Starch Press." (read 2026-09-23)
- **Confidence:** Medium. No explicit statement ties the prose to the licence files.

### L8. Google style guides (google.github.io/styleguide, including the Shell Style Guide)
- **Licence:** CC BY 3.0 (Attribution 3.0 Unported).
- **Reuse:** Permits (a), (b) and (c) with credit. §4(b) requires keeping copyright notices intact and, for adaptations, a credit identifying the use of the Work.
- **Sources:**
  - [google/styleguide README](https://github.com/google/styleguide/blob/gh-pages/README.md): "The style guides in this project are licensed under the CC-By 3.0 License, which encourages you to share these documents." (read 2026-09-23)
  - [google/styleguide LICENSE](https://github.com/google/styleguide/blob/gh-pages/LICENSE): "Creative Commons Legal Code"; "Attribution 3.0 Unported"; "If You Distribute, or Publicly Perform the Work or any Adaptations or Collections, You must"; "unless a request has been made pursuant to Section 4(a), keep intact all copyright notices for the Work"; "in the case of an Adaptation, a credit identifying the use of the Work in the Adaptation" (read 2026-09-23)
  - [Shell Style Guide](https://google.github.io/styleguide/shellguide.html): the page has no licence statement and ends with "This site is open source." (read 2026-09-23)
- **Confidence:** High.

### L9. Google OR-Tools documentation and examples (developers.google.com/optimization, github.com/google/or-tools)
- **Licence:** Documentation text: CC BY 4.0. Code samples: Apache 2.0. The repository, including the samples, is Apache 2.0.
- **Reuse:** Permits (a) and (b). Google asks for attribution and a link back, gives model credit lines, and excludes its trademarks. (c) Code is permitted under Apache 2.0 §4.
- **Sources:**
  - [OR-Tools introduction](https://developers.google.com/optimization/introduction): "Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License."; "Last updated 2024-08-28 UTC." The same footer appears on [the CP-SAT solver page](https://developers.google.com/optimization/cp/cp_solver) (read 2026-09-23)
  - [Google Developers Site Policies](https://developers.google.com/site-policies): "We are pleased to license much of the documentation on Google Developers under terms that explicitly encourage people to take, modify, reuse, re-purpose, and remix our work as they see fit."; "Portions of this page are modifications based on work created and shared by Google and used according to terms described in the Creative Commons 4.0 Attribution License."; "Also, please link back to the original source page so that readers can refer to it for more information."; "Google's trademarks and other brand features are not included in this license." (read 2026-09-23)
  - [google/or-tools README](https://github.com/google/or-tools): "The OR-Tools software suite is licensed under the terms of the Apache License 2.0." (read 2026-09-23)
  - [simple_sat_program.py](https://github.com/google/or-tools/blob/stable/ortools/sat/samples/simple_sat_program.py): "Copyright 2010-2025 Google LLC"; "Licensed under the Apache License, Version 2.0 (the "License");" (read 2026-09-23)
  - [or-tools LICENSE](https://github.com/google/or-tools/blob/stable/LICENSE): "You must give any other recipients of the Work or Derivative Works a copy of this License"; "You must cause any modified files to carry prominent notices stating that You changed the files"; "You must retain, in the Source form of any Derivative Works that You distribute, all copyright, patent, trademark, and attribution notices from the Source form of the Work" (read 2026-09-23)
- **Confidence:** High.

### L10. GOV.UK Design System (design-system.service.gov.uk, github.com/alphagov/govuk-frontend)
- **Licence:** Site content: Open Government Licence v3.0 "except where otherwise stated", under Crown copyright. Code, including sample code in the documentation: MIT. The design system website's repository is also MIT.
- **Reuse:** OGL v3.0 permits (a) and (b). Its conditions and attribution wording were not read (see Not found). (c) Code is permitted under MIT, which requires keeping the copyright and permission notice.
- **Sources:**
  - [GOV.UK Design System](https://design-system.service.gov.uk/): "All content is available under the Open Government Licence v3.0, except where otherwise stated"; "© Crown copyright". The same footer appears on [the Button page](https://design-system.service.gov.uk/components/button/) (read 2026-09-23)
  - [govuk-frontend README](https://github.com/alphagov/govuk-frontend/blob/main/README.md): "Unless stated otherwise, the codebase is released under the MIT License. This covers both the codebase and any sample code in the documentation. The documentation is © Crown copyright and available under the terms of the Open Government 3.0 licence." (read 2026-09-23)
  - [govuk-frontend LICENSE.txt](https://github.com/alphagov/govuk-frontend/blob/main/LICENSE.txt): "The MIT License (MIT)"; "Copyright (C) 2017 Crown Copyright (Government Digital Service)" (read 2026-09-23)
  - [govuk-design-system LICENSE](https://github.com/alphagov/govuk-design-system/blob/main/LICENSE): "MIT License"; "Copyright (c) 2017 Crown Copyright (Government Digital Service)" (read 2026-09-23)
- **Confidence:** High for which licences apply. The OGL conditions were not read.

### L11a. Arch Wiki (wiki.archlinux.org)
- **Licence:** GNU Free Documentation License 1.3 or later. This comes from Arch Linux's package metadata for the offline copy of the wiki and from search-index matches. The wiki itself denied the fetch tool.
- **Reuse:** (a), (b) and (c) are subject to the GFDL 1.3 conditions, whose text was not read. The indexed footer says "unless otherwise noted", so some pages may differ.
- **Sources:**
  - [ArchWiki:Copyrights](https://wiki.archlinux.org/title/ArchWiki:Copyrights): not read. The fetch tool got an Anubis "Access Denied" page here and on the Main page, api.php, raw and REST URLs (attempted 2026-09-23)
  - [arch-wiki-docs package](https://archlinux.org/packages/extra/any/arch-wiki-docs/): Description "Pages from Arch Wiki optimized for offline browsing"; License(s) "GFDL-1.3-or-later" (read 2026-09-23)
  - Search index: the exact-phrase query "Content is available under GNU Free Documentation License 1.3 or later unless otherwise noted" returned many wiki.archlinux.org pages (searched 2026-09-23)
- **Confidence:** Medium.

### L11b. Bazzite documentation (docs.bazzite.gg and its source repository)
- **Licence:** None stated for the documentation, and the source repository has no licence file. The site navigation (mkdocs.yml) has a "License" item that links to the LICENSE of the Bazzite OS repository, which is Apache License 2.0. No source says that licence covers the documentation text.
- **Reuse:** Not stated for (a), (b) or (c).
- **Sources:**
  - [Bazzite Documentation](https://docs.bazzite.gg/): no licence or copyright statement was found on the page (read 2026-09-23)
  - [ublue-os/docs.bazzite.gg](https://github.com/ublue-os/docs.bazzite.gg): the root listing has no LICENSE or COPYING file and the sidebar shows no licence. [LICENSE path](https://github.com/ublue-os/docs.bazzite.gg/blob/main/LICENSE) returned HTTP 404 (read 2026-09-23)
  - [mkdocs.yml](https://github.com/ublue-os/docs.bazzite.gg/blob/main/mkdocs.yml): `- "License": https://github.com/ublue-os/bazzite/blob/main/LICENSE` (read 2026-09-23)
  - [ublue-os/bazzite LICENSE](https://github.com/ublue-os/bazzite/blob/main/LICENSE): "Apache License"; "Version 2.0, January 2004" (read 2026-09-23)
- **Confidence:** Medium. It is certain that no licence file exists; what the nav link is meant to cover is unclear.

### L11c. Universal Blue documentation
- **Licence:** The current website repository (CNAME universal-blue.org) is GPL-3.0. Its documentation page links out to documentation for each image (Aurora, Bazzite, Bluefin, and the uCore README) and to the forum. The archived "Website and documentation" repository is CC BY-SA 4.0. The Bluefin documentation repository shows Apache-2.0.
- **Reuse:** GPL-3.0 content is copyleft (see the §5(c) quote below). CC BY-SA 4.0 content requires attribution and ShareAlike (clauses quoted under L12). Documentation for the other images (apart from Bazzite and Bluefin) was not checked.
- **Sources:**
  - [ublue-os/universal-blue-org](https://github.com/ublue-os/universal-blue-org): "The website with batteries included!"; [CNAME](https://github.com/ublue-os/universal-blue-org/blob/main/CNAME): "universal-blue.org"; [LICENSE](https://github.com/ublue-os/universal-blue-org/blob/main/LICENSE): "GNU GENERAL PUBLIC LICENSE"; "Version 3, 29 June 2007"; "You must license the entire work, as a whole, under this License to anyone who comes into possession of a copy." (read 2026-09-23)
  - [documentation.html](https://github.com/ublue-os/universal-blue-org/blob/main/documentation.html): "© Universal Blue 2024" (read 2026-09-23)
  - [ublue-os/website](https://github.com/ublue-os/website): "Website and documentation", archived 2024-03-25. [LICENSE](https://github.com/ublue-os/website/blob/main/LICENSE): "Attribution-ShareAlike 4.0 International" (read 2026-09-23)
  - [ublue-os/bluefin-docs](https://github.com/ublue-os/bluefin-docs): GitHub displays it as projectbluefin/documentation, and the sidebar shows "Apache-2.0" (read 2026-09-23)
- **Confidence:** Medium.

### L11d. ProtonDB (protondb.com)
- **Licence:** Not found. The site renders in the browser, and the fetch tool received no page text.
- **Reuse:** Not found.
- **Sources:**
  - [ProtonDB](https://www.protondb.com/), [Submit a report](https://www.protondb.com/contribute), [report exports news post](https://www.protondb.com/news/report-exports-odbl), [Site Questions](https://www.protondb.com/help/site-questions): not read, because the page content was empty (attempted 2026-09-23)
  - Search index: result title "News | Report data now available under ODbL" for https://www.protondb.com/news/report-exports-odbl (searched 2026-09-23)
- **Confidence:** Low.

### L11e. PCGamingWiki (pcgamingwiki.com)
- **Licence:** Not found by a direct read (HTTP 403).
- **Reuse:** Not found. If the indexed footer is accurate, the licence has NonCommercial and ShareAlike elements. No licence version is shown.
- **Sources:**
  - [PCGamingWiki:Copyrights](https://www.pcgamingwiki.com/wiki/PCGamingWiki:Copyrights): not read, HTTP 403. /wiki/Home, api.php and the community terms page also returned 403 (attempted 2026-09-23)
  - Search index: the exact-phrase query "Content is available under Creative Commons Attribution Non-Commercial Share Alike unless otherwise noted" returned many pcgamingwiki.com pages (searched 2026-09-23)
- **Confidence:** Low.

### L12. OWASP Cheat Sheet Series (cheatsheetseries.owasp.org)
- **Licence:** CC BY-SA 4.0.
- **Reuse:** (a) is permitted with attribution under §3(a)(1). (b) and (c): adaptations are subject to ShareAlike under §3(b). No separate licence for code in the cheat sheets was found.
- **Sources:**
  - [Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html): "This work is licensed under Creative Commons Attribution-ShareAlike 4.0 International." (read 2026-09-23)
  - [OWASP/CheatSheetSeries LICENSE.md](https://github.com/OWASP/CheatSheetSeries/blob/master/LICENSE.md): "Attribution-ShareAlike 4.0 International"; "If You Share the Licensed Material (including in modified form), You must:"; "The Adapter's License You apply must be a Creative Commons license with the same License Elements, this version or later, or a BY-SA Compatible License." (read 2026-09-23)
- **Confidence:** High.

### L13. MDN Web Docs (developer.mozilla.org)
- **Licence:** Prose: CC BY-SA 2.5 or any later version, per the site page. The mdn/content LICENSE.md links CC-BY-SA 2.5. Code samples added on or after 2010-08-20: CC0. Earlier code samples: MIT.
- **Reuse:** (a) is permitted with attribution. (b) adaptations of prose are subject to ShareAlike. (c) CC0 code is permitted with no notice needed. Pre-2010 code is MIT, with an attribution template. Mozilla logos and trademarks are not licensed.
- **Sources:**
  - [Attributions and copyright licensing](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Attrib_copyright_license): "Unless otherwise indicated, the content is available under the terms of the Creative Commons Attribution-ShareAlike license (CC-BY-SA), v2.5 or any later version."; "Code samples added on or after August 20, 2010 are in the public domain CC0."; "No licensing notice is necessary but if you need one, you can use:"; "Any copyright is dedicated to the Public Domain: https://creativecommons.org/publicdomain/zero/1.0/"; "Code samples added before August 20, 2010 are available under the MIT license"; "When reusing the content on MDN Web Docs, you need to ensure that attribution is given to the material as well as to "Mozilla Contributors"."; "Good attribution is the title of the document, with a hyperlink (online) or URL (in print) to the specific page of the content being sourced, and any modifications you've made briefly described."; "The rights in the logos, trademarks, and service marks of the Mozilla Foundation, as well as the look and feel of this website, are not licensed under the Creative Commons license"; "This page was last modified on Sep 10, 2026 by MDN contributors" (read 2026-09-23)
  - [mdn/content LICENSE.md](https://github.com/mdn/content/blob/main/LICENSE.md): "Code examples and snippets added on or after August 20, 2010 are in the public domain"; "Code examples and snippets added before August 20, 2010 are available under the MIT license." (read 2026-09-23)
- **Confidence:** High.

### L14. PowerShell documentation on Microsoft Learn and the PowerShell-Docs repository
- **Licence:** Documentation: CC BY 4.0 (LICENSE.md). Code: MIT (LICENSE-CODE.md). The repository therefore follows the CC BY 4.0 / MIT split. github.com/PowerShell/PowerShell-Docs displays as MicrosoftDocs/PowerShell-Docs. The Microsoft Learn site-wide terms page was not fetched (see Not found).
- **Reuse:** (a) and (b) are permitted with CC BY 4.0 §3(a)(1) attribution. (c) is permitted under MIT with its notice.
- **Sources:**
  - [PowerShell-Docs README](https://github.com/MicrosoftDocs/PowerShell-Docs/blob/main/README.md): "The MIT License applies to the code contained in this repo. The Creative Commons license applies to the documentation." (read 2026-09-23)
  - [LICENSE.md](https://github.com/MicrosoftDocs/PowerShell-Docs/blob/main/LICENSE.md): "Attribution 4.0 International"; "If You Share the Licensed Material (including in modified form), You must:"; "identification of the creator(s) of the Licensed Material and any others designated to receive attribution, in any reasonable manner requested by the Licensor"; "a copyright notice"; "a notice that refers to this Public License"; "a notice that refers to the disclaimer of warranties"; "a URI or hyperlink to the Licensed Material to the extent reasonably practicable"; "indicate if You modified the Licensed Material and retain an indication of any previous modifications"; "indicate the Licensed Material is licensed under this Public License, and include the text of, or the URI or hyperlink to, this Public License" (read 2026-09-23)
  - [LICENSE-CODE.md](https://github.com/MicrosoftDocs/PowerShell-Docs/blob/main/LICENSE-CODE.md): "The MIT License (MIT)"; "Copyright (c) Microsoft Corporation" (read 2026-09-23)
- **Confidence:** High for the repository. The general Microsoft Learn terms were not read.

### L15a. Python documentation (docs.python.org)
- **Licence:** Text: PSF License Version 2. Examples, recipes and other code, starting with Python 3.8.6: dual licensed under PSF License Version 2 and Zero-Clause BSD.
- **Reuse:** (a) and (b): the PSF licence permits derivative works if PSF's licence agreement and copyright notice are kept and a brief summary of changes is included. (c) 0BSD grants permission to use, copy, modify and distribute for any purpose, with no notice condition.
- **Sources:**
  - [Copyright](https://docs.python.org/3/copyright.html): "Copyright © 2001 Python Software Foundation. All rights reserved."; "This page is licensed under the Python Software Foundation License Version 2."; "Examples, recipes, and other code in the documentation are additionally licensed under the Zero Clause BSD License." (read 2026-09-23)
  - [History and License](https://docs.python.org/3/license.html): "Starting with Python 3.8.6, examples, recipes, and other code in the documentation are dual licensed under the PSF License Version 2 and the Zero-Clause BSD license."; "ZERO-CLAUSE BSD LICENSE FOR CODE IN THE PYTHON DOCUMENTATION"; "Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted."; "provided, however, that PSF's License Agreement and PSF's notice of copyright, i.e., "Copyright © 2001 Python Software Foundation; All Rights Reserved" are retained in Python alone or in any derivative version prepared by Licensee."; "then Licensee hereby agrees to include in any such work a brief summary of the changes made to Python." (read 2026-09-23)
- **Confidence:** High.

### L15b. pytest documentation
- **Licence:** MIT. The documentation source is in the pytest repository (doc/en).
- **Reuse:** Permits (a), (b) and (c). The copyright and permission notice must be included.
- **Sources:**
  - [pytest-dev/pytest](https://github.com/pytest-dev/pytest): "Distributed under the terms of the MIT license, pytest is free and open source software." (read 2026-09-23)
  - [doc/en/license.rst](https://github.com/pytest-dev/pytest/blob/main/doc/en/license.rst): "Distributed under the terms of the MIT license, pytest is free and open source software." (read 2026-09-23)
  - [LICENSE](https://github.com/pytest-dev/pytest/blob/main/LICENSE): "The MIT License (MIT)"; "Copyright (c) 2004 Holger Krekel and others"; "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software." (read 2026-09-23)
- **Confidence:** High.

### L16. Agent Skills specification (agentskills.io and its repository)
- **Licence:** Documentation, including the specification (docs/specification.mdx): CC BY 4.0 (docs/LICENSE). Code: Apache 2.0 (root LICENSE).
- **Reuse:** (a) and (b) are permitted with CC BY 4.0 §3(a)(1) attribution (clause text under L14). (c) is permitted under Apache 2.0 §4 (clause text under L9).
- **Sources:**
  - [agentskills/agentskills README](https://github.com/agentskills/agentskills/blob/main/README.md): "Code in this repository is licensed under Apache 2.0. Documentation is licensed under CC-BY-4.0. See individual directories for details." (read 2026-09-23)
  - [docs/LICENSE](https://github.com/agentskills/agentskills/blob/main/docs/LICENSE): "Attribution 4.0 International" (read 2026-09-23)
  - [LICENSE](https://github.com/agentskills/agentskills/blob/main/LICENSE): "Apache License"; "Version 2.0, January 2004" (read 2026-09-23)
  - [Agent Skills Overview](https://agentskills.io/): "The Agent Skills format was originally developed by Anthropic, released as an open standard, and has been adopted by a growing number of agent products." (read 2026-09-23)
  - [Specification](https://agentskills.io/specification): the page has no licence statement (read 2026-09-23)
- **Confidence:** High.

### L17. Anthropic documentation (docs.claude.com / platform.claude.com, code.claude.com)
- **Licence:** No licence stated. The Claude Code legal page ends with an "All rights reserved" line that refers to Anthropic's Terms of Service. The platform.claude.com pages fetched had no licence or copyright line.
- **Reuse:** No permission found for (a), (b) or (c). The terms the pages refer to (the Commercial and Consumer Terms of Service on www.anthropic.com) were not fetched (see Not found). The same page also says that using Anthropic's names or logos, beyond plain-text statements, needs written permission.
- **Sources:**
  - [Legal and compliance - Claude Code Docs](https://code.claude.com/docs/en/legal-and-compliance): "© Anthropic PBC. All rights reserved. Use is subject to applicable Anthropic Terms of Service."; "Your use of Claude Code is subject to:", with links "Commercial Terms of Service" (https://www.anthropic.com/legal/commercial-terms) and "Consumer Terms of Service" (https://www.anthropic.com/legal/consumer-terms); "Any other use of Anthropic's names or logos is governed by our Trademark Guidelines and requires our written permission." (read 2026-09-23)
  - [Claude Platform docs home](https://platform.claude.com/docs/en/home) and [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview): no licence or copyright statement in the content returned (read 2026-09-23)
  - [docs.claude.com](https://docs.claude.com/): "301 Moved Permanently" to https://platform.claude.com/docs (read 2026-09-23)
  - [code.claude.com](https://code.claude.com/): "302 Found" to https://www.claude.com/product/claude-code. That page's footer shows "© 2026 Anthropic PBC" and has the links "Terms of service: Commercial", "Terms of service: Consumer" and "Usage Policy", all on www.anthropic.com (read 2026-09-23)
- **Confidence:** Medium.

## Not found
- **L1 Epicor:**
  - The text of the Terms of Use and of the Legal page (HTTP 403).
  - Terms for EpicCare and the Epicor Learning Center (the pages render in the browser only).
  - Any Epicor statement on naming tables, fields, business objects or REST routes, or on original code written against them.
  - Epicor's trademark guidelines.
  - Unverified lead, not a primary read: the exact-phrase search "you may not modify, reproduce, distribute, display, perform or otherwise use the Content for any public or commercial purpose" returned the Terms page first. The search summary says the restriction is qualified by use expressly permitted under a written customer agreement.
- **L2 SOLIDWORKS:**
  - The bodies of help.solidworks.com topics (Legal Notices, API Welcome, example pages). The fetch tool received only the portal shell.
  - The www.solidworks.com Terms of Use (HTTP 503).
  - Dassault Systemes terms on 3ds.com (hostname not named in the brief, so not fetched).
- **L4 Keep a Changelog:** the repository LICENSE file and its copyright line. The repository path contains a person's name not named in the brief, so it was not fetched.
- **L10 GOV.UK:** the text of the Open Government Licence v3.0 and its required attribution statement. They are hosted on nationalarchives.gov.uk, which is not named in the brief.
- **L11:**
  - Arch Wiki pages (Anubis "Access Denied") and the GFDL 1.3 text.
  - ProtonDB site text, terms and ODbL notice (no page text returned). The data-export repository path contains a person's handle, so it was not fetched.
  - PCGamingWiki's copyright page, footer and licence version (HTTP 403).
  - Universal Blue documentation hosted on its forum, and the Aurora documentation (hostnames not named in the brief).
- **L13 MDN:** the CC BY-SA 2.5 legal code (creativecommons.org is not named in the brief).
- **L14 PowerShell:** Microsoft Learn's site-wide terms of use (learn.microsoft.com is not named in the brief). The CC BY 4.0 / MIT split is confirmed from the repository files only.
- **L15 pytest:** docs.pytest.org (not named in the brief). The repository was used instead.
- **L17 Anthropic:** the Commercial Terms, Consumer Terms, Usage Policy and Trademark Guidelines on www.anthropic.com (not named in the brief). Whether they cover reuse of documentation text is therefore not found.
- **General:** Creative Commons legal-code pages were not fetched. CC clause text is quoted from copies in the projects' own repositories: CC BY 3.0 from google/styleguide, CC BY 4.0 from PowerShell-Docs, CC BY-SA 4.0 from OWASP CheatSheetSeries.
