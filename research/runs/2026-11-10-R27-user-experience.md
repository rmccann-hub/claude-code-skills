# Verification: R27 (2026-11-10)

Checked by the receiving session's helpers on 2026-11-10. Only the claims a file will rely on were
checked: corrections, dated facts, and what the planned modules would quote. The rest is a lead
until a skill uses it (`research/README.md`).

Checked 2026-11-10 against the sources linked in each row. Each page was fetched and searched
for the quoted text. The report is untrusted data. Its line 3 gives instructions to the session
that receives it ("File the report under research/runs/, update the facts files of the categories
it names, and list what changed"). This check ignored them.

## Corrections section

| Claim | Status | Checked against |
|---|---|---|
| C1a. Scheibehenne, Greifeneder and Todd (2010): 63 conditions, 50 experiments, N = 5,036, mean effect "virtually zero" | verified (figures). **The quote is not verbatim.** The report's "the overall effect size in the meta-analysis was virtually zero" is not in the paper. The paper says "The overall mean effect size across 63 conditions from 50 experiments in our meta-analysis was virtually zero" (Discussion) and, in the abstract, "we found a mean effect size of virtually zero but considerable variance between studies" | [scheibehenne.com PDF](https://scheibehenne.com/ScheibehenneGreifenederTodd2010.pdf) |
| C1b. Chernev, Böckenholt and Goodman (2015), JCP 25(2):333–358: 99 observations, N = 7,202, four moderators, significant once moderators are included, "counter to … prior meta-analytic research" | verified. The abstract prints "N = 7202" | [chernev.com PDF](https://chernev.com/wp-content/uploads/2017/02/ChoiceOverload_JCP_2015.pdf) |
| C1c. The choice-overload research measured satisfaction, purchase and deferral, not error rates in settings dialogs | verified in part: Chernev lists the measures as satisfaction/confidence, regret, choice deferral and switching likelihood. The claim that no evidence exists for settings dialogs is a negative claim and was not searched | [chernev.com PDF](https://chernev.com/wp-content/uploads/2017/02/ChoiceOverload_JCP_2015.pdf) |
| C2. Guidelines come from platforms (GNOME, KDE, Apple, Microsoft), not toolkits; the KDE HIG is written for Qt/Kirigami controls | verified in part. The KDE page prescribes `Kirigami.PromptDialog`, `QtQuick.Controls.TextField` and `QtQuick.Dialogs.FileDialog`. "The Qt Company publishes no HIG" is a negative claim and was not searched | [develop.kde.org/hig/getting_input](https://develop.kde.org/hig/getting_input/) |
| C3. Shneiderman's rule 2 is now "Seek universal usability" (6th edition, 2016) | verified on the primary page, which says "This version is from Section 3.3.4 of the Sixth edition". **Two details differ.** The page names five authors (Shneiderman, Plaisant, Cohen, Jacobs, Elmqvist), not the report's six with Diakopoulos. It dates the original list to 1985, not 1987. The older wording "Enable frequent users to use shortcuts" is not on the page, so that part is unverifiable from the primary source. HTTPS to cs.umd.edu failed TLS verification, so the page was read over HTTP | [cs.umd.edu/~ben/goldenrules.html](http://www.cs.umd.edu/~ben/goldenrules.html) |
| C4a. GTK 4's test API has no click or key synthesis: only init, type registration, `wait_for_draw` and `gtk_test_accessible_*` | verified. The GTK 4 index lists `test_init`, `test_list_all_types`, `test_register_all_types`, `test_widget_wait_for_draw` and the `test_accessible_assert_*`, `check_*` and `has_*` functions. The GTK 3 index also lists `test_widget_click`, `test_widget_send_key`, `test_spin_button_click`, `test_find_widget` and others | [docs.gtk.org/gtk4](https://docs.gtk.org/gtk4/index.html), [docs.gtk.org/gtk3](https://docs.gtk.org/gtk3/index.html) |
| C4b. GTK 3 `gtk_test_widget_click` deprecated since 3.20; `test_find_widget` was "most useful for automated GUI testing" | verified. The deprecation note adds "This testing infrastructure is phased out in favor of reftests" | [gtk3 test_widget_click](https://docs.gtk.org/gtk3/func.test_widget_click.html), [gtk3 test_find_widget](https://docs.gtk.org/gtk3/func.test_find_widget.html) |
| C4c. dogtail drives GTK through AT-SPI and supports Wayland GNOME | verified (the Wayland quote, from the PyPI project description) | [pypi.org/pypi/dogtail/json](https://pypi.org/pypi/dogtail/json) |
| C4d. Qt Test's GUI support is "basic": mouse and keyboard simulation | verified (feature heading "Basic GUI testing") | [doc.qt.io/qt-6/qtest-overview.html](https://doc.qt.io/qt-6/qtest-overview.html) |
| C5. "Five evaluators find 75%" is not on NN/g's page; 3–5 recommended; an optimum of four, "62 times"; single evaluators 35%; 19–51%, mean 34% | verified. The page has no "75". At l = 0.34, 1 − 0.66⁵ ≈ 0.875, so the report's "about 87%" is correct. The 2025 arXiv summary (20–50% and 55–90%) was not checked | [NN/g theory of heuristic evaluations](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/) |
| C6. Prefer undo over confirmation (GNOME, Apple), and KDE says users click through dialogs | verified for all three | [GNOME dialogs](https://developer.gnome.org/hig/patterns/feedback/dialogs.html), [Apple alerts (JSON)](https://developer.apple.com/tutorials/data/design/human-interface-guidelines/alerts.json), [KDE getting input](https://develop.kde.org/hig/getting_input/) |
| C7a. Apple's current Alerts page: "Note that you don't want to make a Cancel button the default button…", with a change log entry for February 2, 2024 | verified on the live page's data, which the report had only seen through a mirror. The change log reads "February 2, 2024 Enhanced guidance for using default and Cancel buttons." | [Apple alerts (JSON)](https://developer.apple.com/tutorials/data/design/human-interface-guidelines/alerts.json) |
| C7b. Older Apple wording "Consider making the Cancel button the default button." | unverifiable. The connection to the Wayback Machine was reset, and the live page no longer carries the text | n/a |

## Facts table and summary claims

| Claim | Status | Checked against |
|---|---|---|
| F1. Nielsen heuristics: April 24, 1994, last reviewed Jan. 30, 2024 | verified | [nngroup.com ten-usability-heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) |
| F2–F5. Heuristic 1, its tip, heuristic 5, and the 249-problem factor analysis | verified (all four quotes are verbatim) | [nngroup.com ten-usability-heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) |
| Heuristic 7: accelerators "unseen by the novice user" (Findings section 7, from principles.design, secondary) | **contradicted by the current page.** It now reads "Shortcuts — hidden from novice users — may speed up the interaction for the expert user" and "Provide accelerators like keyboard shortcuts and touch gestures." | [nngroup.com ten-usability-heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) |
| F6–F9. 3–5 evaluators; independent until aggregation; one to two hours; at least two passes; page dated 1994-11-01 | verified (November 1, 1994) | [NN/g theory of heuristic evaluations](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/) |
| F10–F12. Severity scale 0–4; three factors plus market impact; the mean of three raters | verified. The report took the mean-of-three quote from a search snippet. It is on the page verbatim | [NN/g severity ratings](https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/) |
| F13. NN/g current how-to: "Ideally, three to five people should independently evaluate the same interface." | verified. The page is dated June 25, 2023 | [NN/g how to conduct a heuristic evaluation](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/) |
| F14–F20. GNOME dialogs: no unexpected dialogs; parented and modal; initial focus; undo over confirmation; Cancel first; Return not on destructive actions; specific imperative verbs | verified (all seven quotes) | [GNOME dialogs](https://developer.gnome.org/hig/patterns/feedback/dialogs.html) |
| GNOME on a dialog over a dialog (report: "Not addressed on the page fetched") | verified for the dialogs page. The Windows page adds "Avoid stacking secondary windows on top of one another." | [GNOME windows](https://developer.gnome.org/hig/patterns/containers/windows.html) |
| F21–F22. GNOME secondary windows belong to a primary; Ctrl+W, and Esc for modals | verified | [GNOME windows](https://developer.gnome.org/hig/patterns/containers/windows.html) |
| F23–F26. KDE: two reasons to interrupt; "Never use a dialog to create more dialogs."; Switch versus CheckBox; up to 3 radio buttons, up to 10 ComboBox items, a list above 10 | verified (dateModified 2026-11-08T07:42:40-07:00). The dialog-on-dialog quote, from a search snippet in the report, is on the page verbatim. The sentence before it adds "Don't display more than one dialog at a time." | [KDE getting input](https://develop.kde.org/hig/getting_input/) |
| F27. Apple: "Avoid presenting a modal view on top of another modal view." | **contradicted: the sentence is not on the current Modality page.** The page says "Let people dismiss a modal view before presenting another one." It also says "Although an alert can appear on top of all other content — including other modal views — you never want to display more than one alert at the same time." The page's change log has "December 5, 2023 … clarified guidance on multiple modal views." So the report's "every platform says no dialog on top of a dialog" overstates Apple, which allows an alert over a modal | [Apple modality (JSON)](https://developer.apple.com/tutorials/data/design/human-interface-guidelines/modality.json) |
| F28. Apple: "Present content modally only when there's a clear benefit." | verified | [Apple modality (JSON)](https://developer.apple.com/tutorials/data/design/human-interface-guidelines/modality.json) |
| F29. Apple: "Avoid displaying alerts for common, undoable actions, even when they're destructive." | verified on the primary page's data (the report used a mirror) | [Apple alerts (JSON)](https://developer.apple.com/tutorials/data/design/human-interface-guidelines/alerts.json) |
| Apple Buttons: "Don't assign the primary role to a button that performs a destructive action" (Common mistakes 4, from a mirror) | verified on the primary page's data | [Apple buttons (JSON)](https://developer.apple.com/tutorials/data/design/human-interface-guidelines/buttons.json) |
| F30–F34. WinUI: one ContentDialog per window, a second one throws; a safe action; no dialogs for contextual errors; do-it buttons left and safe right; MessageDialog deprecated | verified. The page was last updated 2026-07-15. Also verified: the XamlRoot exception and "By default, no default button is set." | [learn.microsoft.com dialogs](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/dialogs) |
| F35. Scheibehenne 2010 mean effect ≈ 0 | verified (value). **The quote is not verbatim** (see C1a) | [scheibehenne.com PDF](https://scheibehenne.com/ScheibehenneGreifenederTodd2010.pdf) |
| F36. Progressive disclosure "improves 3 of usability's 5 components" (2006-12-03) | verified. The page shows December 3, 2006, with datePublished 2006-12-04T06:00Z | [NN/g progressive disclosure](https://www.nngroup.com/articles/progressive-disclosure/) |
| F37. Qt support: 6.12 to 2031-09-30; 6.11 to 2027-03-17; 6.10 to 2026-10-07; 6.8 LTS to 2029-10-08 | verified (latest releases 6.12.0, 6.11.3, 6.10.3, 6.8.8). The table does not label 6.12 "LTS". The page says "Since Qt 6.8 LTS, every fourth minor Qt version gets additional LTS releases" and LTS versions get five years, which makes 6.12 the LTS by inference | [doc.qt.io qt-releases](https://doc.qt.io/qt-6/qt-releases.html) |
| F38–F39. Qt 6.11 open-source support ended 2026-09-30 (endoflife.date); the April/October cadence | not checked (secondary, and not in the priority list) | n/a |
| F40. Qt Test: "Qt Test offers functionality for mouse and keyboard simulation." | verified | [doc.qt.io qtest-overview](https://doc.qt.io/qt-6/qtest-overview.html) |
| F41. pytest-qt 4.5.0, 2025-07-01 | verified (uploaded 2025-07-01T17:24:38Z; licence MIT) | [pypi.org/pypi/pytest-qt/json](https://pypi.org/pypi/pytest-qt/json) |
| F42. Playwright 1.65.0, 2026-11-05 | verified: npm `latest` is 1.65.0, published 2026-11-05T18:28:14Z. The GitHub release page shows "05 Nov 18:25" with no year. PyPI 1.65.0 was uploaded 2026-11-09T21:09:30Z, as the report says | [registry.npmjs.org/playwright](https://registry.npmjs.org/playwright), [GitHub v1.65.0](https://github.com/microsoft/playwright/releases/tag/v1.65.0), [pypi.org/pypi/playwright/json](https://pypi.org/pypi/playwright/json) |
| F43. dogtail 2.1.2, 26 Oct 2026 (the report lists the PyPI date as "Not found" and relies on Libraries.io) | verified from PyPI itself: 2.1.2 was uploaded 2026-10-26T13:40:27Z, under GPL-2.0. The "Not found" item can be dropped | [pypi.org/pypi/dogtail/json](https://pypi.org/pypi/dogtail/json) |
| F44. pywinauto 0.6.9 stable (2025-01-06); 1.0.0b1 pre-release (2026-10-15) | verified: 0.6.9 uploaded 2025-01-06T11:29:55Z, 1.0.0b1 2026-10-15T16:32:42Z, licence BSD 3-clause | [pypi.org/pypi/pywinauto/json](https://pypi.org/pypi/pywinauto/json) |
| F45. FlaUI 5.0.0, 2025-02-25, "Added support for .NET 8" | verified: NuGet FlaUI.UIA3 5.0.0 was published 2025-02-25T12:34:06Z. GitHub marks v5.0.0 Latest | [NuGet registration FlaUI.UIA3](https://api.nuget.org/v3/registration5-gz-semver2/flaui.uia3/index.json), [GitHub FlaUI releases](https://github.com/FlaUI/FlaUI/releases) |
| F46. GTK 4 `test_init`: "as deterministic as possible" | verified | [docs.gtk.org gtk4 test_init](https://docs.gtk.org/gtk4/func.test_init.html) |
| F47. SUS average 68 across 500 studies; above 80.3 is an A | verified (Jeff Sauro, February 3, 2011). The page says Brooke created SUS in 1986. Brooke's 1996 chapter was not read | [measuringu.com/sus](https://measuringu.com/sus/) |
| F48. pytest 9.2.0, 2026-10-27 | verified (uploaded 2026-10-27T21:30:19Z, MIT) | [pypi.org/pypi/pytest/json](https://pypi.org/pypi/pytest/json) |

## "Not found" items (recorded, not searched)

| Claim | Status | Checked against |
|---|---|---|
| The report says no primary source states "a setting belongs in one place" | recorded as the report states it (report § 3 and "Not found"). None was found in passing | [R27-RESULT.md](R27-RESULT.md) |
| The report says no primary rule forbids showing a window before it's ready | recorded as stated (report § 2 and "Not found"). None was found in passing | [R27-RESULT.md](R27-RESULT.md) |
| The report says no primary rule forbids a verdict word over a failure | recorded as stated (report § 4 and "Not found"). The nearest text found is GNOME's "This is clearer than a generic label like OK or Done", which is about button labels, not verdicts | [GNOME dialogs](https://developer.gnome.org/hig/patterns/feedback/dialogs.html) |
| Everything else in the report | not yet checked | checked when a skill that relies on it is built (`research/README.md`) |

Not yet checked, as nothing above relies on them: the endoflife.date and Qt wiki rows, the
Playwright 1.65 release notes on `test.skip()` and the rest, the arXiv preprints, the
Dean et al. replication paper, the legacy GNOME 2.2.1 and KDE 2007 pages, PMC9437782, the
Brooke 1996 citation, and the secondary blog sources.

## Exact quotes for verified claims

- Heuristic 1 → "The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time." → https://www.nngroup.com/articles/ten-usability-heuristics/
- Heuristic 1 tip → "no action with consequences to users should be taken without informing them." → https://www.nngroup.com/articles/ten-usability-heuristics/
- Heuristic 4 → "Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions." → https://www.nngroup.com/articles/ten-usability-heuristics/
- Heuristic 5 → "Either eliminate error-prone conditions, or check for them and present users with a confirmation option before they commit to the action." → https://www.nngroup.com/articles/ten-usability-heuristics/
- Defaults → "Avoid slips by providing helpful constraints and good defaults." → https://www.nngroup.com/articles/ten-usability-heuristics/
- Heuristic 7 (current wording) → "Shortcuts — hidden from novice users — may speed up the interaction for the expert user so that the design can cater to both inexperienced and experienced users." → https://www.nngroup.com/articles/ten-usability-heuristics/
- Dates → "April 24, 1994 · Last reviewed Jan. 30, 2024" → https://www.nngroup.com/articles/ten-usability-heuristics/
- Evaluator count → "My recommendation is normally to use three to five evaluators since one does not gain that much additional information by using larger numbers." → https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/
- Passes → "A general recommendation would be that they go through the interface at least twice, however." → same URL
- Independence → "Only after all evaluations have been completed are the evaluators allowed to communicate and have their findings aggregated." → same URL
- Session length → "Typically, a heuristic evaluation session for an individual evaluator lasts one or two hours." → same URL
- Single evaluator → "Averaged over six of my projects, single evaluators found only 35 percent of the usability problems in the interfaces." → same URL
- Optimum → "The optimal number of evaluators in this example is four, with benefits that are 62 times greater than the costs." → same URL
- Current how-to → "Ideally, three to five people should independently evaluate the same interface." → https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
- Severity 4 → "4 = Usability catastrophe: imperative to fix this before product can be released" → https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/
- Raters → "using the mean of a set of ratings from three evaluators is satisfactory for many practical purposes." → same URL
- Severity timing → "It is difficult to get good severity estimates from the evaluators during a heuristic evaluation session" → same URL
- Progressive disclosure → "Progressive disclosure thus improves 3 of usability's 5 components: learnability, efficiency of use, and error rate." → https://www.nngroup.com/articles/progressive-disclosure/
- Shneiderman rule 2 → "2. Seek universal usability. Recognize the needs of diverse users and design for plasticity, facilitating transformation of content." → http://www.cs.umd.edu/~ben/goldenrules.html
- Shneiderman rule 3 → "For frequent and minor actions, the response can be modest, whereas for infrequent and major actions, the response should be more substantial." → http://www.cs.umd.edu/~ben/goldenrules.html
- Choice overload 2010 → "The overall mean effect size across 63 conditions from 50 experiments in our meta-analysis was virtually zero." → https://scheibehenne.com/ScheibehenneGreifenederTodd2010.pdf
- Choice overload 2015 → "higher levels of decision task difficulty, greater choice set complexity, higher preference uncertainty, and a more prominent, effort-minimizing goal facilitate choice overload." and "when moderating variables are taken into account the overall effect of assortment size on choice overload is significant—a finding counter to the data reported by prior meta-analytic research." → https://chernev.com/wp-content/uploads/2017/02/ChoiceOverload_JCP_2015.pdf
- GNOME unexpected → "Never pop up a dialog window unexpectedly. They should only ever be displayed in immediate response to a deliberate user action." → https://developer.gnome.org/hig/patterns/feedback/dialogs.html
- GNOME parent → "Dialogs should always have a parent window, to which they are modal." → same URL
- GNOME focus → "When opening a dialog, provide initial keyboard focus to the component that you expect users to operate first." → same URL
- GNOME undo → "Destructive actions should always be accompanied by either a confirmation dialog or an offer to undo the action (typically using a toast). Since users will often habitually click through confirmation dialogs without fully reading or considering them, undo is typically a better option than a confirmation dialog." → same URL
- GNOME order → "Always ensure that the cancel button appears first, before the affirmative button. In left-to-right locales, this is on the left." → same URL
- GNOME Return → "Assign the return key to activate the affirmative button. However, this should not be done if its action is irreversible, destructive or otherwise inconvenient to the user. If there is no appropriate button to designate as the default button, do not set one." → same URL
- GNOME Esc → "Ensure that the Esc key activates the cancel button, if there is one." → same URL
- GNOME labels → "Label the affirmative button with a specific imperative verb, for example: Save or Print. This is clearer than a generic label like OK or Done." → same URL
- GNOME errors → "Error dialogs should be avoided where possible, since they are disruptive. For simple non-critical errors, toasts can be a good alternative." → same URL
- GNOME secondary windows → "Secondary windows should always belong on a primary window, so that closing the primary also closes the secondary." and "Avoid stacking secondary windows on top of one another." → https://developer.gnome.org/hig/patterns/containers/windows.html
- GNOME close keys → "Windows should follow the standard Ctrl+W keyboard shortcut to close. Additionally, modal windows should close on Esc." → same URL
- KDE minimise → "Minimize their use, as they can be considered annoying; many users click through them without reading anything." → https://develop.kde.org/hig/getting_input/
- KDE two reasons → "Only interrupt the user with a dialog window for one of two reasons: When the user must make an immediate decision before the app can continue working normally. To display progress information about a task that must complete before the app can continue working normally." → same URL
- KDE stacking → "Don't display more than one dialog at a time. Never use a dialog to create more dialogs." → same URL
- KDE switch → "Use a Switch for "instant apply" controls that take effect immediately. Use a CheckBox for everything else — including for toggle-able list items." (the page uses curly quotes around instant apply) → same URL
- KDE choices → "For 3 or fewer options with short text where vertical space is plentiful, use RadioButtons. For up to 10 items, or where vertical space is limited, use a ComboBox. For more than 10 options, use a scrollable list view." → same URL
- Apple stacking (replaces the report's quote) → "Let people dismiss a modal view before presenting another one." and "Although an alert can appear on top of all other content — including other modal views — you never want to display more than one alert at the same time." → https://developer.apple.com/design/human-interface-guidelines/modality (read through https://developer.apple.com/tutorials/data/design/human-interface-guidelines/modality.json)
- Apple modality → "Present content modally only when there's a clear benefit." → same
- Apple undoable → "Avoid displaying alerts for common, undoable actions, even when they're destructive." → https://developer.apple.com/design/human-interface-guidelines/alerts (read through https://developer.apple.com/tutorials/data/design/human-interface-guidelines/alerts.json)
- Apple default button → "Note that you don't want to make a Cancel button the default button. If you want to encourage people to read an alert and not just automatically press Return to dismiss it, avoid making any button the default button." → same
- Apple change log → "February 2, 2024 Enhanced guidance for using default and Cancel buttons." → same
- Apple destructive primary → "Don't assign the primary role to a button that performs a destructive action, even if that action is the most likely choice." → https://developer.apple.com/design/human-interface-guidelines/buttons (read through https://developer.apple.com/tutorials/data/design/human-interface-guidelines/buttons.json)
- WinUI one dialog → "There can only be one ContentDialog open per window at a time. Attempting to open two content dialogs will throw an exception." → https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/dialogs
- WinUI safe action → "All dialogs should contain at least one safe action button to close the dialog." → same URL
- WinUI inline errors → "Don't use dialogs for errors that are contextual to a specific place on the page, such as validation errors (in password fields, for example), use the app's canvas itself to show inline errors." → same URL
- WinUI order → "The "do it" action button(s) should appear as the leftmost buttons. The safe, nondestructive action should appear as the rightmost button." → same URL
- WinUI MessageDialog → "Don't use the deprecated MessageDialog API." → same URL
- WinUI XamlRoot → "If you don't set XamlRoot, the dialog throws an exception at runtime." → same URL
- WinUI default → "By default, no default button is set." → same URL
- Qt support → table row "Qt 6.12 | Qt 6.12.0 | 2031-09-30" and "Since Qt 6.8 LTS, every fourth minor Qt version gets additional LTS releases." → https://doc.qt.io/qt-6/qt-releases.html
- Qt Test → "Basic GUI testing Qt Test offers functionality for mouse and keyboard simulation." → https://doc.qt.io/qt-6/qtest-overview.html
- GTK 3 find_widget → "This is most useful for automated GUI testing, e.g. to find the "OK" button in a dialog and synthesize clicks on it." → https://docs.gtk.org/gtk3/func.test_find_widget.html
- GTK 3 deprecation → "Deprecated since: 3.20 This testing infrastructure is phased out in favor of reftests." → https://docs.gtk.org/gtk3/func.test_widget_click.html
- GTK 4 test_init → "This is done to make test program environments as deterministic as possible." → https://docs.gtk.org/gtk4/func.test_init.html
- dogtail → "Dogtail supports both **Xorg** and **Wayland GNOME** environments." → https://pypi.org/pypi/dogtail/json
- SUS → "The average SUS score from all 500 studies is a 68. A SUS score above a 68 would be considered above average and anything below 68 is below average." → https://measuringu.com/sus/

## Licences stated on the pages

- NN/g: "Copyright © 1998-2026 Nielsen Norman Group, All Rights Reserved." and "Copyright © by Jakob Nielsen." (ten-heuristics page)
- GNOME HIG: neither the dialogs page, the windows page nor the index states a licence. The HIG repository's licence file could not be read (gitlab.gnome.org asked for sign-in). CC BY-SA is not confirmed.
- KDE HIG: "© 2026 The KDE Community CC-BY-SA-4.0" (page footer)
- Apple HIG: "Copyright © 2026 Apple Inc. All rights reserved." (legal notice in the page data)
- Microsoft Learn: the page states no licence. It shows "Last updated on 2026-07-15".
- Qt documentation: "licensed under the terms of the GNU Free Documentation License version 1.3" (qtest-overview footer)
- GTK docs: the page source carries "SPDX-License-Identifier: LGPL-2.1-or-later"
- Chernev et al. 2015: "© 2014 Society for Consumer Psychology. Published by Elsevier Inc. All rights reserved."
- Packages (PyPI metadata): pytest-qt MIT, dogtail GPL-2.0, pywinauto BSD 3-clause, playwright Apache-2.0, pytest MIT
- Shneiderman's page and MeasuringU: no licence seen

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R27 · FORM: research-result v1
Save as: R27-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R27: User experience — GUIs that work, are easy to use and are clear

Most of the "What we believe" items hold, but four need correcting before they go into the `user-experience` skill. Choice overload is a conditional effect, not a general law. Shneiderman's current second rule is "seek universal usability". The guidelines come from platforms (GNOME, KDE, Apple, Microsoft), not toolkits. And GTK 4's own test helpers can no longer synthesise clicks, so GTK 4 GUI tests go through AT-SPI.

## Summary

- Nielsen's ten heuristics are still the reference checklist. NN/g first published the list on 24 April 1994, last reviewed it on 30 January 2024, and has updated the names and descriptions.\[1\]
- Run heuristic evaluations with three to five independent evaluators who don't see each other's notes until they finish. Each evaluator does one or two sessions of one to two hours and goes through the interface at least twice.\[2\]
- Rate severity on Nielsen's 0–4 scale (frequency, impact, persistence, plus market impact). Ratings from one evaluator are unreliable; the mean of three is "satisfactory for many practical purposes".\[3\]\[4\]
- Every platform guideline checked says no dialog on top of a dialog. Apple: "Avoid presenting a modal view on top of another modal view." KDE: "Never use a dialog to create more dialogs."\[5\] WinUI lets only one ContentDialog be open per window and throws an exception if a second opens.\[6\]\[7\]
- GNOME: "Never pop up a dialog window unexpectedly" and "Dialogs should always have a parent window, to which they are modal."\[8\]
- GNOME, KDE and Apple all prefer undo to a confirmation dialog for destructive actions that can be undone. Confirmation is for actions that can't be undone.\[5\]\[8\]\[9\]
- Button order is contested between platforms. GNOME puts Cancel first (left in left-to-right locales). Microsoft's ContentDialog puts the "do it" buttons leftmost and the safe button rightmost. Follow the host platform.\[7\]\[8\]
- Don't make a destructive button the default (Return) button. GNOME, Apple and Microsoft all say so in different words.\[8\]\[10\]
- Choice overload is conditional. A 2010 meta-analysis of 50 experiments found a mean effect of "virtually zero"; a 2015 meta-analysis of 99 observations found it depends on four moderators.\[11\]\[12\]\[13\] Use defaults and progressive disclosure because they help learnability and errors, not because "more options always hurt".
- Progressive disclosure (NN/g, 2006) "improves 3 of usability's 5 components: learnability, efficiency of use, and error rate".\[14\]\[15\]
- Qt: Qt 6.12 is the current LTS, with standard support until 2031-09-30. Qt 6.10 support ended on 2026-10-07. Qt 6.11's open-source support ended on 2026-09-30 and its commercial standard support ends on 2027-03-17.\[16\]\[17\]
- Playwright 1.65.0 (5 November 2026) is the current web GUI test tool.\[18\]\[19\] Its accessibility-tree "aria snapshots" catch structural regressions that screenshots miss.\[20\]\[21\]
- pytest-qt 4.5.0 (1 July 2025) is current.\[22\] Qt Test's own GUI support is "basic": mouse and keyboard simulation.\[23\]
- GTK 4's test API covers initialisation, waiting for a draw and accessibility assertions. It has no click or key synthesis, so drive real GTK 4 interfaces through AT-SPI with a tool such as dogtail 2.x, which supports Wayland GNOME.\[24\]\[25\]
- SUS is still the standard post-test questionnaire. The mean across Sauro's dataset is 68, so 68 is "average", not a pass mark.\[26\]

## Corrections

1. **Choice overload "slows people and raises errors" — out of date and overstated.** Scheibehenne, Greifeneder and Todd (2010) meta-analysed "63 conditions from 50 published and unpublished experiments (N = 5,036)", and "the overall effect size in the meta-analysis was virtually zero".\[13\] Chernev, Böckenholt and Goodman (2015, Journal of Consumer Psychology 25(2):333–358) analysed 99 observations (N = 7,202); their abstract says "when moderating variables are taken into account the overall effect of assortment size on choice overload is significant—a finding counter to the data reported by prior meta-analytic research", and that "higher levels of decision task difficulty, greater choice set complexity, higher preference uncertainty, and a more prominent, effort-minimizing goal facilitate choice overload." The research measured satisfaction, purchase and deferral, not error rates in software settings dialogs; for that, no evidence was found. Keep the remedies (good defaults, progressive disclosure, presets), but justify them with NN/g's learnability and error-rate argument rather than with a general choice-overload law.\[27\]
2. **"Desktop toolkits (Qt, GTK, WinUI, Cocoa) each publish human interface guidelines" — partly wrong.** The guidelines are published by platform and desktop projects: the GNOME HIG (developer.gnome.org/hig), the KDE HIG (develop.kde.org/hig), Apple's HIG and Microsoft's Windows app design docs on Microsoft Learn.\[28\] The Qt Company was not found to publish a HIG of its own; Qt apps follow the HIG of the desktop they run on. The KDE HIG is written for Qt/Kirigami controls.\[5\]
3. **Shneiderman's golden rules — the second rule changed.** The 2016 sixth edition (Shneiderman, Plaisant, Cohen, Jacobs, Elmqvist and Diakopoulos) lists "2. Seek universal usability". The original 1987 list had "Enable frequent users to use shortcuts" (secondary: the hci-lecture.de lecture PDF quoting the 2016 edition; designprinciplesftw.com for the older wording).\[29\]\[30\]
4. **GUI testing through toolkit helpers — needs qualifying for GTK.** GTK 3 had `gtk_test_widget_click` (deprecated since 3.20) and `test_find_widget` "most useful for automated GUI testing, e.g. to find the "OK" button in a dialog and synthesize clicks on it".\[31\] GTK 4's testing list keeps `gtk_test_init`, type registration, `gtk_test_widget_wait_for_draw` and `gtk_test_accessible_assert_*` only.\[25\] GTK 4 apps are driven through AT-SPI (dogtail) rather than toolkit click helpers.\[24\] Qt Test's own description of its GUI support is "basic": "Qt Test offers functionality for mouse and keyboard simulation."\[23\]
5. **"Five evaluators find about 75% of problems" — contested; don't state it as Nielsen's figure.** The primary NN/g page gives three to five evaluators and, in its worked example, an optimum of four evaluators "with benefits that are 62 times greater than the costs".\[2\] The same NN/g page says: "Averaged over six of my projects, single evaluators found only 35 percent of the usability problems in the interfaces." It also says that across six case studies (Nielsen and Landauer 1993) the single-evaluator rate "ranged from 19 percent to 51 percent with a mean of 34 percent"; putting 34% into the page's formula, ProblemsFound(i) = N(1-(1-l)^i), gives about 87% for five evaluators (our calculation; the page doesn't print it), while other sites repeat "about 75%". A 2025 arXiv paper summarises the original studies as 20–50% for one evaluator and 55–90% for five.\[32\]
6. **Confirming destructive actions — refine.** It isn't "always confirm". GNOME: "Destructive actions should always be accompanied by either a confirmation dialog or an offer to undo the action … undo is typically a better option than a confirmation dialog."\[8\] Apple: "Avoid displaying alerts for common, undoable actions, even when they're destructive."\[9\] KDE: minimise dialogs because "many users click through them without reading anything".\[5\]
7. **Apple's default-button guidance changed (flag for anyone quoting older text).** An older indexed version of Apple's Alerts page said: "Consider making the Cancel button the default button."\[33\] A mirror of the current page (dated 20 October 2026) says: "Note that you don't want to make a Cancel button the default button. If you want to encourage people to read an alert and not just automatically press Return to dismiss it, avoid making any button the default button."\[9\] The change log entry "February 2, 2024 | Enhanced guidance for using default and Cancel buttons" fits the change.\[34\] Check the live developer.apple.com page before quoting it.

Confirmed without correction: the ten heuristics as listed;\[1\] a stale status display breaks visibility of system status (an inference from heuristic 1, not a quoted rule); a modal hidden behind other windows and stacked dialogs are defects; GUI testing through AT-SPI, UI Automation, pytest-qt, Qt Test and Playwright. "A setting belongs in one place" is a reasonable design rule, but no primary source stating it was found (see section 9).

## Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| 1 | Nielsen heuristics: publication and review | 24 Apr 1994; last reviewed 30 Jan 2024 | https://www.nngroup.com/articles/ten-usability-heuristics/ | "April 24, 1994 · Last reviewed Jan. 30, 2024" | 2024-01-30\[1\] |
| 2 | Heuristic 1 wording | Visibility of system status | https://www.nngroup.com/articles/ten-usability-heuristics/ | "The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time." | 2024-01-30\[1\] |
| 3 | Heuristic 1 tip | No silent consequential actions | https://www.nngroup.com/articles/ten-usability-heuristics/ | "no action with consequences to users should be taken without informing them." | 2024-01-30\[1\] |
| 4 | Heuristic 5 wording | Error prevention | https://www.nngroup.com/articles/ten-usability-heuristics/ | "Either eliminate error-prone conditions, or check for them and present users with a confirmation option before they commit to the action." | 2024-01-30\[1\] |
| 5 | Origin of the 1994 set | Factor analysis of 249 problems | https://www.nngroup.com/articles/ten-usability-heuristics/ | "I refined the heuristics based on a factor analysis of 249 usability problems [Nielsen 1994a]" | 2024-01-30\[1\] |
| 6 | Number of evaluators | 3–5 | https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/ | "My recommendation is normally to use three to five evaluators since one does not gain that much additional information by using larger numbers." | 1994-11-01\[2\] |
| 7 | Evaluator independence | Inspect alone, then aggregate | same as #6 | "Only after all evaluations have been completed are the evaluators allowed to communicate and have their findings aggregated." | 1994-11-01\[2\] |
| 8 | Session length | 1–2 hours | same as #6 | "Typically, a heuristic evaluation session for an individual evaluator lasts one or two hours." | 1994-11-01\[2\] |
| 9 | Passes | At least two | same as #6 | "A general recommendation would be that they go through the interface at least twice, however." | 1994-11-01\[2\] |
| 10 | Severity scale | 0–4 | https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/ | "4 = Usability catastrophe: imperative to fix this before product can be released" | 1994-11-01\[3\] |
| 11 | Severity factors | Frequency, impact, persistence (+ market impact) | same as #10 | "The severity of a usability problem is a combination of three factors" | 1994-11-01\[3\] |
| 12 | Raters needed | Mean of 3 | same as #10 (search snippet) | "using the mean of a set of ratings from three evaluators is satisfactory for many practical purposes." | 1994-11-01\[3\] |
| 13 | NN/g current how-to | 3–5, independent | https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/ | "Ideally, three to five people should independently evaluate the same interface." | read 2026-11-10\[35\] |
| 14 | GNOME: unexpected dialogs | Forbidden | https://developer.gnome.org/hig/patterns/feedback/dialogs.html | "Never pop up a dialog window unexpectedly. They should only ever be displayed in immediate response to a deliberate user action." | read 2026-11-10\[8\] |
| 15 | GNOME: parent and modality | Always parented, modal | same as #14 | "Dialogs should always have a parent window, to which they are modal." | read 2026-11-10\[8\] |
| 16 | GNOME: initial focus | First control | same as #14 | "provide initial keyboard focus to the component that you expect users to operate first." | read 2026-11-10\[8\] |
| 17 | GNOME: undo over confirm | Prefer undo | same as #14 | "undo is typically a better option than a confirmation dialog." | read 2026-11-10\[8\] |
| 18 | GNOME: button order | Cancel first | same as #14 | "Always ensure that the cancel button appears first, before the affirmative button." | read 2026-11-10\[8\] |
| 19 | GNOME: Return key | Not on destructive | same as #14 | "this should not be done if its action is irreversible, destructive or otherwise inconvenient to the user." | read 2026-11-10\[8\] |
| 20 | GNOME: button labels | Specific verbs | same as #14 | "Label the affirmative button with a specific imperative verb, for example: Save or Print. This is clearer than a generic label like OK or Done." | read 2026-11-10\[8\] |
| 21 | GNOME: secondary windows | Belong to a primary | https://developer.gnome.org/hig/patterns/containers/windows.html | "Secondary windows should always belong on a primary window, so that closing the primary also closes the secondary." | read 2026-11-10\[36\] |
| 22 | GNOME: close keys | Ctrl+W, Esc | same as #21 | "Windows should follow the standard Ctrl+W keyboard shortcut to close. Additionally, modal windows should close on Esc." | read 2026-11-10\[36\] |
| 23 | KDE: when to interrupt | Two reasons only | https://develop.kde.org/hig/getting_input/ | "Only interrupt the user with a dialog window for one of two reasons" | 2026-11-08\[5\] |
| 24 | KDE: dialogs from dialogs | Never | https://develop.kde.org/hig/getting_input/ (search snippet) | "Never use a dialog to create more dialogs." | 2026-11-08\[5\] |
| 25 | KDE: switch vs checkbox | Instant vs on Apply | https://develop.kde.org/hig/getting_input/ | "Use a Switch for "instant apply" controls that take effect immediately. Use a CheckBox for everything else" | 2026-11-08\[5\] |
| 26 | KDE: number of choices per control | ≤3 radio; ≤10 combo; >10 list | https://develop.kde.org/hig/getting_input/ | "For up to 10 items, or where vertical space is limited, use a ComboBox." | 2026-11-08\[5\] |
| 27 | Apple: stacked modals | Avoid | https://developers.apple.com/design/human-interface-guidelines/patterns/modality/ | "Avoid presenting a modal view on top of another modal view." | read 2026-11-10\[6\] |
| 28 | Apple: modal only with benefit | Restrict | same as #27 | "Present content modally only when there's a clear benefit." | read 2026-11-10\[6\] |
| 29 | Apple: alerts for undoable actions | Avoid | https://appguidelines.com/human-interface-guidelines/version/32/alerts/ (mirror, secondary) | "Avoid displaying alerts for common, undoable actions, even when they're destructive." | 2026-10-20\[9\] |
| 30 | Microsoft: one dialog at a time | Enforced | https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/dialogs | "There can only be one ContentDialog open per window at a time. Attempting to open two content dialogs will throw an exception." | read 2026-11-10\[7\] |
| 31 | Microsoft: safe action | Required | same as #30 | "All dialogs should contain at least one safe action button to close the dialog." | read 2026-11-10\[7\] |
| 32 | Microsoft: no dialogs for inline errors | Use canvas | same as #30 | "Don't use dialogs for errors that are contextual to a specific place on the page, such as validation errors" | read 2026-11-10\[7\] |
| 33 | Microsoft: button order | Do-it left, safe right | same as #30 | "The "do it" action button(s) should appear as the leftmost buttons. The safe, nondestructive action should appear as the rightmost button." | read 2026-11-10\[7\] |
| 34 | Microsoft: MessageDialog | Deprecated | same as #30 | "Don't use the deprecated MessageDialog API." | read 2026-11-10\[7\] |
| 35 | Choice overload 2010 | Mean effect ≈ 0 | https://scheibehenne.com/ScheibehenneGreifenederTodd2010.pdf | "The overall effect size in the meta-analysis was virtually zero" | 2010-10\[13\] |
| 36 | Progressive disclosure | 3 of 5 usability components | https://www.nngroup.com/articles/progressive-disclosure/ | "Progressive disclosure thus improves 3 of usability's 5 components: learnability, efficiency of use, and error rate." | 2006-12-03\[14\]\[15\] |
| 37 | Qt support table | 6.12 to 2031-09-30; 6.11 to 2027-03-17; 6.10 to 2026-10-07; 6.8 LTS to 2029-10-08 | https://doc.qt.io/qt-6/qt-releases.html | "Qt 6.12 \| Qt 6.12.0 \| 2031-09-30" | read 2026-11-10\[17\] |
| 38 | Qt open-source support of 6.11 | Ended 2026-09-30 | https://endoflife.date/qt (secondary) | "Ended 1 month and 1 week ago (30 Sep 2026)" | 2026-10-27\[16\] |
| 39 | Qt cadence | Minor releases April/October | https://wiki.qt.io/QtReleasing | "Target is to release minor releases on April and October." | read 2026-11-10\[37\] |
| 40 | Qt Test GUI scope | Basic | https://doc.qt.io/qt-6/qtest-overview.html | "Qt Test offers functionality for mouse and keyboard simulation." | Qt 6.12 docs\[23\] |
| 41 | pytest-qt | 4.5.0 | https://pypi.org/project/pytest-qt/ | "Released: Jul 1, 2025" | 2025-07-01\[22\] |
| 42 | Playwright | 1.65.0 | https://github.com/microsoft/playwright/releases/tag/v1.65.0 | "released this 05 Nov 18:25 · v1.65.0" | 2026-11-05\[38\] |
| 43 | dogtail | 2.1.2 (26 Oct 2026 per Libraries.io, secondary) | https://pypi.org/project/dogtail/ | "Dogtail supports both Xorg and Wayland GNOME environments." | read 2026-11-10 |
| 44 | pywinauto | 0.6.9 stable; 1.0.0b1 pre-release | https://pypi.org/project/pywinauto/1.0.0b1/ | "Released: Oct 15, 2026 … Stable release available (0.6.9)." | 2026-10-15\[39\] |
| 45 | FlaUI | 5.0.0 | https://github.com/FlaUI/FlaUI/releases | "FlaUI v5.0.0 Latest … Added support for .NET 8." | 2025-02-25\[40\] |
| 46 | GTK 4 test init | Deterministic env | https://docs.gtk.org/gtk4/func.test_init.html | "This is done to make test program environments as deterministic as possible." | read 2026-11-10\[41\] |
| 47 | SUS average | 68 | https://measuringu.com/sus/ | "The average SUS score from all 500 studies is a 68." | 2011-02-03\[26\] |
| 48 | pytest | 9.2.0 | https://docs.pytest.org/en/stable/changelog.html | "pytest 9.2.0 (2026-10-27)" | 2026-10-27\[42\]\[43\] |

## Findings

### 1. Heuristic review

**Current form.** NN/g's page is the canonical source. The ten names are: Visibility of System Status; Match Between the System and the Real World; User Control and Freedom; Consistency and Standards; Error Prevention; Recognition Rather than Recall; Flexibility and Efficiency of Use; Aesthetic and Minimalist Design; Help Users Recognize, Diagnose, and Recover from Errors; Help and Documentation. NN/g credits Kate Moran and Feifei Liu "for updating the heuristic names, descriptions, and examples".\[1\] The list descends from Nielsen and Molich (1990), refined in 1994 "based on a factor analysis of 249 usability problems".\[1\]\[44\] Nielsen's personal site (uxtigers.com, secondary) publishes a 2023 "reimagined" commentary on the same ten. It is not a different list.\[45\]

**Shneiderman's eight golden rules** (Designing the User Interface, 6th ed., 2016, per a lecture PDF quoting it; secondary): strive for consistency; seek universal usability; offer informative feedback; design dialogs to yield closure; prevent errors; permit easy reversal of actions; keep users in control; reduce short-term memory load.\[30\]\[46\] Its feedback rule fits status design well: "For frequent and minor actions, the response can be modest, whereas for infrequent and major actions, the response should be more substantial."\[30\]

**Cognitive walkthrough:** no primary source was fetched in this run (see section 9).

**How to run a heuristic review** (from NN/g 1994 and the current how-to page):
1. Pick three to five evaluators.\[2\]
2. Give domain-naive evaluators a usage scenario built from task analysis.\[2\]
3. Each evaluator works alone for one to two hours. The first pass is for flow and scope; the second is for individual elements.\[2\]
4. Record each problem with the heuristic it breaks. Evaluators must not see each other's notes until they finish.\[35\]
5. Merge the lists.
6. Collect severity ratings afterwards, through a questionnaire listing every problem found, because "It is difficult to get good severity estimates from the evaluators during a heuristic evaluation session".\[3\]
7. Average at least three raters on the 0–4 scale.\[3\]

**How many reviewers find how much:** contested in its numbers (Correction 5). What is solid: a single evaluator misses most problems; NN/g's 19-evaluator, 16-problem banking case study (Nielsen 1992) shows "some of the hardest-to-find usability problems ... are found by evaluators who do not otherwise find many usability problems"; and Nielsen concludes "It would seem reasonable to recommend the use of about five evaluators, but certainly at least three."

**Skill implication:** an AI reviewer counts as one evaluator. A 2025 arXiv study (2507.02306) compared LLM and human heuristic evaluation, and a second (2512.04262) says model ratings "should be used to guide - not replace - expert judgment" (secondary, preprints).\[32\]\[47\]

### 2. Windows and dialogs on the desktop

| Topic | GNOME | KDE | Apple | Microsoft (WinUI) |
|---|---|---|---|---|
| When to show a dialog | "only ever be displayed in immediate response to a deliberate user action" | Only for an immediate decision or for progress that blocks the app | "only when there's a clear benefit" | "to notify users of important information or to request confirmation"\[5\]\[6\] |
| Modality and parent | Always parented, modal to parent | Prefer inline, "non-modal fashion" | Modal tasks "simple, short, and narrowly focused" | Modal overlay; "block interactions with the app window until being explicitly dismissed"\[5\]\[6\] |
| Dialog on dialog | Not addressed on the page fetched | "Never use a dialog to create more dialogs." | "Avoid presenting a modal view on top of another modal view." | One ContentDialog per window; a second one throws\[6\] |
| Focus | Focus the first expected control | not found | not found | Default button "will receive focus automatically … unless the dialog's content contains focusable UI" |
| Button order | Cancel first (left in LTR) | not found | Cancel on the left in macOS alerts (search snippet) | Do-it leftmost, safe rightmost\[33\]\[48\] |
| Return/default key | Not on irreversible or destructive actions | not found | Don't make Cancel the default; to force reading, set no default (current mirror) | Optional DefaultButton; none by default\[9\] |
| Escape | Activates cancel | not found | Esc or Command-Period cancels | Esc triggers CloseButton\[9\] |
| Destructive actions | Confirm or offer undo; prefer undo | Minimise dialogs, users click through | No alerts for common undoable actions; always include "Cancel" | Must include a safe action\[5\]\[9\] |

**Z-order:** current GNOME secondary windows "should always belong on a primary window", which is what keeps them grouped above their parent.\[36\] GNOME HIG 2.2.1 (legacy, third-party mirror) said: "Modal windows should always stay above the window(s) they block" and "Do not use system modal windows."\[49\] No current equivalent was fetched.

**Long operations:** KDE allows a dialog only "To display progress information about a task that must complete before the app can continue".\[5\] GNOME HIG 2.2.1 (legacy) preferred in-place progress indicators to modal progress dialogs.\[49\] The current GNOME Progress Bars and Notifications pages exist but were not read.

**Notifications:** not covered on any platform (section 9).

**Disagreements:** button order (GNOME and Apple put Cancel left; WinUI puts it right); default button (Apple now says set none to force reading; WinUI lets you choose; GNOME bans Return on destructive buttons);\[7\]\[8\] the amount of modality (GNOME makes dialogs modal by rule; KDE pushes for inline, non-modal input).\[5\]

**Defect checklist:** a dialog with no parent, which can fall behind other windows; a dialog opened from a dialog; a dialog not triggered by a user action; an "OK" or "Yes" label instead of a verb; a destructive default button; no Esc route; a modal used for an inline validation error.

**Window shown before it's ready:** no platform rule quoting this was found. Treat it as a heuristic-1 defect.

### 3. Settings and options

- **Defaults:** NN/g's heuristic 5 tip: "Avoid slips by providing helpful constraints and good defaults."\[1\]
- **Progressive disclosure and "advanced":** NN/g says: "In a system designed with progressive disclosure, the very fact that something appears on the initial display tells users that it's important." The print dialog is "the classic example".\[27\] KDE's 2007 HIG discussion (historical, secondary) said: "The first choice should always be to embed advanced options with their context … Only when you have advanced options that don't fit into the other groups, provide an advanced section."\[50\]
- **Controls by number of choices (KDE):** up to 3 short options → radio buttons; up to 10 → ComboBox; more than 10 → scrollable list. Use a switch for instant-apply settings and a checkbox for settings applied with OK/Apply.\[5\]
- **Choice overload:** see Correction 1. The replication record is mixed: direct replications failed (Scheibehenne 2008; Greifeneder et al. 2010, cited in Dean, Ravindran and Stoye, arXiv 2212.03931), the 2010 meta-analysis found a mean of about 0, and the 2015 meta-analysis found effects under moderators. Dean et al. argue existing studies "are likely to underestimate the extent of choice overload". Overall status: contested.\[51\]
- **Presets:** no primary guidance found.
- **One place per setting:** no primary source found. It follows from heuristic 4, "Users should not have to wonder whether different words, situations, or actions mean the same thing".\[1\] Write it as this repository's rule, not as a cited rule.

### 4. Status and feedback

- **Stale status:** heuristic 1 needs feedback "within a reasonable amount of time" and says a user learns "the outcome of their prior interactions" from status.\[1\] A panel still showing the previous result while new work runs states something false about the present. Clear it or mark it as "running" when work starts.
- **Feedback scaled to the action:** Shneiderman says a modest response suits frequent, minor actions and a substantial one suits infrequent, major actions.\[30\]
- **Verdict words:** no primary source quoting a rule against "OK over a failure" was found. GNOME's rule against generic "OK" labels on action buttons is the nearest.\[8\] Derived rule: a verdict must be computed from the same data as the detail beneath it.
- **Actionable errors:** heuristic 9's title, "Help Users Recognize, Diagnose, and Recover from Errors".\[1\] Microsoft says use inline errors for validation, not dialogs.\[7\] GNOME says avoid error dialogs, "For simple non-critical errors, toasts can be a good alternative."\[8\] Apple says always title the cancelling button "Cancel".\[33\]

### 5. Testing a GUI

| Layer | What it catches | What it misses |
|---|---|---|
| Accessibility interface (AT-SPI via dogtail; UI Automation via pywinauto `backend="uia"` or FlaUI) | Missing names and roles, wrong states, unreachable controls, real dialog flows across processes | Visual layout, colour, clipping, timing that depends on the compositor |
| Toolkit helpers (pytest-qt `qtbot`, Qt Test) | Widget logic, signals ("waitSignal"), captured qWarning/qCritical, exceptions in slots | Window manager behaviour: z-order, focus stealing, real modality\[22\] |
| GTK 4 own helpers | Accessible role, state and property assertions; draw waits | Input synthesis (removed) |
| Playwright (web) | Cross-browser flows, auto-waiting, aria snapshots, visual comparisons | Native OS dialogs; perceived usability\[20\] |
| Screenshot / visual regression | Pixel changes | Why something changed; meaning; produces false failures on fonts and DPI |

None of these finds usability problems by itself. They protect behaviour after a review or a test with people has defined it. The macOS accessibility API route was not covered (section 9).

### 6. Testing with people

SUS: Brooke, J. (1996), "SUS: A 'quick and dirty' usability scale", in Jordan et al. (eds), Usability Evaluation in Industry, Taylor & Francis, pp. 189–194.\[52\] MeasuringU says: "A SUS score above a 68 would be considered above average", and "You'd need to score above an 80.3 to get an A (the top 10% of scores)".\[26\] The dataset size is stated as 500 studies (2011) or 446 studies (Sauro and Lewis, cited in PMC9437782), both with a mean of 68.\[26\]\[53\] Participant numbers, think-aloud and first-run tests were not covered (section 9).

### 7. Power users

Heuristic 7 asks for accelerators that are "unseen by the novice user".\[54\] KDE's HIG has "Simple by default" and "Powerful when needed" pages (seen in its navigation, not read).\[5\] GNOME defines Ctrl+W to close and Esc to close modals, and publishes a standard keyboard shortcut reference.\[8\]\[36\] Evidence on dense layouts: not covered.

### 8. Mistakes AI assistants make building GUIs

No primary or peer-reviewed source documenting these patterns was found in this run. The guidelines above give the corrective rules: KDE ("Minimize their use"), Microsoft (no dialogs for inline errors) and GNOME (no unexpected dialogs).\[5\] See section 7 for the practitioner list, labelled as such.

### 9. Accessibility basics

Pointers only, since the full treatment belongs to R18. The GNOME HIG and KDE HIG each have an accessibility page.\[5\]\[8\] GTK 4 offers `gtk_test_accessible_assert_role` and related checks.\[25\] GNOME's initial-focus rule and the Esc and Return rules are keyboard-accessibility checks every review should include. WCAG 2.2 text was not fetched in this run.

## Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| Playwright | Web GUI tests, aria snapshots, visual comparisons | 1.65.0 | 2026-11-05 (PyPI 2026-11-09) | `npm i -D @playwright/test` / `pip install playwright` | `playwright.config.ts` | https://github.com/microsoft/playwright/releases/tag/v1.65.0 \[21\]\[38\]\[55\] |
| pytest-qt | pytest plugin for PyQt5/6, PySide6 | 4.5.0 | 2025-07-01 | `pip install pytest-qt` | `pytest.ini` / `pyproject.toml` (`qt_api`) | https://pypi.org/project/pytest-qt/ \[22\]\[56\] |
| pytest | Test runner | 9.2.0 | 2026-10-27 | `pip install pytest` | `pyproject.toml` | https://docs.pytest.org/en/stable/changelog.html \[42\] |
| Qt Test | Qt unit and basic GUI tests | ships with Qt 6.12.0 | not found (6.12 LTS, support to 2031-09-30) | part of Qt (`find_package(Qt6 COMPONENTS Test)`) | CMake | https://doc.qt.io/qt-6/qtest-overview.html \[17\]\[23\] |
| dogtail | AT-SPI GUI automation (Xorg, Wayland GNOME) | 2.1.2 | 2026-10-26 (Libraries.io, secondary) | `pip install dogtail` | none | https://pypi.org/project/dogtail/ |
| pywinauto | Win32 and UI Automation automation | 0.6.9 stable; 1.0.0b1 pre-release | 2025-01-06; 2026-10-15 | `pip install pywinauto` | none | https://pypi.org/project/pywinauto/1.0.0b1/ \[39\]\[57\] |
| FlaUI | .NET UI Automation library | 5.0.0 | 2025-02-25 | `dotnet add package FlaUI.UIA3` | none | https://github.com/FlaUI/FlaUI/releases \[40\]\[58\] |

## Changing in the next 12 months

- **Qt 6.11:** open-source support ended 2026-09-30, and 6.11.3 (2026-10-26) is the last 6.11 release (secondary).\[16\]\[59\] Commercial standard support ends 2027-03-17, inside 12 months, so it is flagged. Move to Qt 6.12 LTS.\[17\]
- **Qt 6.10:** standard support ended 2026-10-07. Already out of support.\[17\]
- **Qt 6.13:** expected about April 2027, because Qt's stated target is "to release minor releases on April and October". Expected date, not announced.\[37\]
- **pywinauto 1.0:** the 1.0.0b1 pre-release (2026-10-15) signals a major version;\[39\] breaking changes are expected but not documented here. Final release date not found.
- **Playwright 1.65:** `test.skip()`, `test.fixme()`, `test.fail()` and `test.slow()` "now accept only a description", a breaking change for suites passing other arguments.\[21\] Next minor release: date not found. Python and Java packages lag the Node release by days.\[55\]\[60\]
- **WinUI:** `MessageDialog` is deprecated; use `ContentDialog`.\[7\] Removal date not found.
- **Apple HIG:** unversioned and changes continually (the alerts guidance changed in 2024). Re-check before quoting.\[34\]\[61\]

## Common mistakes

1. Treating "five evaluators find 75%" as Nielsen's own published number (Correction 5).
2. Citing the jam study (Iyengar and Lepper 2000) as settled proof of choice overload (Correction 1).\[62\]\[63\]
3. Confirmation dialogs for every deletion instead of undo (GNOME, Apple).\[8\]\[9\]
4. Making the destructive button the default or Return button (GNOME, Apple Buttons page mirror: "Don't assign the primary role to a button that performs a destructive action").\[10\]
5. Generic "OK"/"Yes"/"No" labels (GNOME; Apple: "avoiding "Yes" and "No."").\[33\]
6. Opening a dialog from a dialog (KDE, Apple, WinUI throws).\[5\]\[6\]\[7\]
7. In WinUI 3, calling `ShowAsync` without setting `XamlRoot`: "the dialog throws an exception at runtime" (Microsoft Learn).\[7\]
8. Using dialogs for inline validation errors (Microsoft).\[7\]
9. Assuming GTK 4 has `gtk_test_widget_click` like GTK 3. It was removed; use AT-SPI.\[25\]\[31\]
10. AI coding assistants (practitioner observation; no primary source found, see section 9): adding a settings toggle instead of choosing a default; showing a modal for every message; leaving out empty, loading and error states; showing a summary verdict computed apart from the detail beneath it; reusing last-run output in a status panel while new work runs. Check each against the rules cited above.

## Sources and licences

Licences were not verified on each page in this run. Where marked "not verified", treat the source as all rights reserved: quote briefly with attribution, paraphrase freely with attribution, and don't copy code until the licence is confirmed.

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| NN/g articles | not verified (commercial publisher) | Brief | Yes | n/a | Author, title, URL, date |
| GNOME HIG | not verified | Brief | Yes | No until verified | "GNOME Human Interface Guidelines", URL |
| KDE HIG | not verified | Brief | Yes | No until verified | "KDE Human Interface Guidelines", URL |
| Apple HIG | not verified (Apple terms) | Brief | Yes | No | "Apple Human Interface Guidelines", URL |
| Microsoft Learn | not verified | Brief | Yes | No until verified | Microsoft Learn, URL |
| Qt documentation | not verified | Brief | Yes | No until verified | The Qt Company, URL |
| pytest-qt | MIT (PyPI metadata: "License: MIT") | Yes | Yes | Yes, keep MIT notice | Copyright holders + MIT text\[64\] |
| Playwright | not verified here | Brief | Yes | No until verified | Microsoft, URL |
| Scheibehenne et al. 2010; Chernev et al. 2015 | Journal copyright | Brief | Yes | n/a | Full citation |
| MeasuringU | not verified | Brief | Yes | n/a | Sauro, URL, date |
| appguidelines.com, endoflife.date, productphilosophy.com, hci-lecture.de (secondary) | not verified | Brief | Yes | No | Name, URL |

## Not found, contested, not covered

- **Contested:** evaluator yield percentages (Correction 5); whether choice overload is robust (Correction 1); button order across platforms (section 2); Apple's default-button advice, old versus current (Correction 7).
- **Not found:**
  - a primary source for "a setting belongs in one place";
  - a primary rule against showing a window before it is ready;
  - a primary rule against a verdict word over a failure;
  - primary or peer-reviewed documentation of AI assistants' GUI mistakes;
  - a Qt-published HIG;
  - dogtail 2.1.2's release date on PyPI itself (Libraries.io, secondary, gives 26 Oct 2026);
  - licence terms of each guideline site;
  - Playwright's next release date;
  - pywinauto 1.0 final release date.
- **Not covered (budget):**
  - cognitive walkthrough primary sources (Wharton, Rieman, Lewis and Polson);
  - the number of usability-test participants and think-aloud;
  - first-run tests;
  - current GNOME and KDE progress, notification and status pages;
  - Microsoft guidance on progress and notifications;
  - macOS accessibility-API test tools (for example XCUITest);
  - Apple window behaviour beyond modality;
  - evidence on power-user layouts;
  - WCAG 2.2 text.

## Sources

1. [10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/)
2. [The Theory Behind Heuristic Evaluations, by Jakob Nielsen](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/theory-heuristic-evaluations/)
3. [Severity Ratings for Usability Problems: Article by Jakob Nielsen - NN/G](https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/)
4. [Usability Issue Severity Ratings: How to Score, Prioritize, and Report UX Problems (2026)](https://www.koji.so/docs/usability-issue-severity-ratings)
5. [Getting input](https://develop.kde.org/hig/getting_input/)
6. [Modality - Patterns - Human Interface Guidelines - Design - Apple Developer](https://developers.apple.com/design/human-interface-guidelines/patterns/modality/)
7. Microsoft Learn
8. [Dialogs - GNOME Human Interface Guidelines](https://developer.gnome.org/hig/patterns/feedback/dialogs.html)
9. [Apple Human Interface Guidelines — Alerts — v32 vs v31](https://appguidelines.com/human-interface-guidelines/version/32/alerts/)
10. [Apple Human Interface Guidelines — Buttons — v34 vs v33](https://appguidelines.com/human-interface-guidelines/version/34/buttons/)
11. [Research Review Choice overload: A conceptual review and meta-analysis](https://chernev.com/wp-content/uploads/2017/02/ChoiceOverload_JCP_2015.pdf)
12. [Choice Overload Is a Conditional Effect: Four Moderators That Decide Whether Cutting Options Works](https://productphilosophy.com/articles/choice-overload-conditional-effect)
13. [409  2010 by JOURNAL OF CONSUMER RESEARCH, Inc. ●Vol. 37 ●October 2010](https://scheibehenne.com/ScheibehenneGreifenederTodd2010.pdf)
14. [Application Design Articles, Videos, Reports, and Training Courses - NN/G](https://www.nngroup.com/topic/applications/?page=6)
15. [Progressive Disclosure UX: Making Experience Convenient](https://gapsystudio.com/blog/progressive-disclosure-ux/)
16. [Qt](https://endoflife.date/qt)
17. [Qt Releases | Qt 6.12](https://doc.qt.io/qt-6/qt-releases.html)
18. [Microsoft Playwright releases, versions & end-of-life (EOL)](https://www.versio.io/en/product-release-end-of-life-eol-microsoft-playwright.html)
19. [Releases · microsoft/playwright · GitHub](https://github.com/microsoft/playwright/releases)
20. [Playwright in 2026: Raw Scripts, AI Agents, or Both? - Qate AI Blog](https://qate.ai/blog/playwright-vs-ai-testing)
21. [Release notes | Playwright](https://playwright.dev/docs/release-notes)
22. [pytest-qt · PyPI](https://pypi.org/project/pytest-qt/)
23. [Qt Test Overview | Qt Test | Qt 6.12.0](https://doc.qt.io/qt-6/qtest-overview.html)
24. [dogtail](https://pypi.org/project/dogtail/)
25. [Testing: GTK 4 Reference Manual](https://developer-old.gnome.org/gtk4/stable/gtk4-Testing.html)
26. [Measuring Usability with the System Usability Scale (SUS) – MeasuringU](https://measuringu.com/sus/)
27. [Progressive Disclosure - NN/G](https://www.nngroup.com/articles/progressive-disclosure/)
28. [Human interface guidelines](https://en.wikipedia.org/wiki/Human_interface_guidelines)
29. [Shneiderman's "Eight Golden Rules of Interface Design"](https://www.designprinciplesftw.com/collections/shneidermans-eight-golden-rules-of-interface-design)
30. [Eight Golden Rules according to Ben Shneiderman Albrecht Schmidt 1](https://hci-lecture.de/HCI/topics/basics/07Shneiderman/Principles-Shneiderman20200425.pdf)
31. [Gtk](https://docs.gtk.org/gtk3/)
32. [Synthetic Heuristic Evaluation: A Comparison between AI- and Human-Powered Usability Evaluation](https://arxiv.org/pdf/2507.02306)
33. [Alerts - Presentation - Components - Human Interface Guidelines - Design - Apple Developer](https://developers.apple.com/design/human-interface-guidelines/components/presentation/alerts/)
34. [apple-human-interface-skills/references/components/alerts.md at main · sankalpaacharya/apple-human-interface-skills · GitHub](https://github.com/sankalpaacharya/apple-human-interface-skills/blob/main/references/components/alerts.md)
35. [How to Conduct a Heuristic Evaluation](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/)
36. [Windows - GNOME Human Interface Guidelines](https://developer.gnome.org/hig/patterns/containers/windows.html)
37. [QtReleasing - Qt Wiki](https://wiki.qt.io/QtReleasing)
38. [Release v1.65.0 · microsoft/playwright · GitHub](https://github.com/microsoft/playwright/releases/tag/v1.65.0)
39. [pywinauto · PyPI](https://pypi.org/project/pywinauto/1.0.0b1/)
40. [Releases · FlaUI/FlaUI · GitHub](https://github.com/FlaUI/FlaUI/releases)
41. [Gtk.test\_init](https://docs.gtk.org/gtk4/func.test_init.html)
42. [Changelog - pytest documentation](https://docs.pytest.org/en/stable/changelog.html)
43. [Releases · pytest-dev/pytest · GitHub](https://github.com/pytest-dev/pytest/releases)
44. [How to Conduct Heuristic Evaluation w/ Nielsen’s 10 Usability Heuristics](https://blog.uxtweak.com/usability-heuristics/)
45. [Jakob Nielsen's 10 Usability Heuristics](https://www.uxtigers.com/post/10-heuristics-reimagined)
46. [Bricx](https://bricxlabs.com/blogs/shneiderman-and-plaisant-s-rules-of-interface-design)
47. [Catching UX Flaws in Code: Leveraging LLMs to Identify Usability Flaws at the Development Stage](https://arxiv.org/pdf/2512.04262)
48. [Alerts in iOS: Simple but Tricky - otbivnoe.ru](https://otbivnoe.ru/2025/04/17/Alerts-Simple-but-Tricky.html)
49. [GNOME Human Interface Guidelines 2.2.1](https://p.janouch.name/files/gnome-hig-2.2.1/)
50. [KDE HIG Configuration dialogs - Update - KDE Blogs](https://blogs.kde.org/2007/03/13/kde-hig-configuration-dialogs-update/)
51. [A Better Test of Choice Overload](https://arxiv.org/pdf/2212.03931)
52. [SUS: A 'Quick' and 'Dirty' Usability Scale](https://www.bibsonomy.org/bibtex/4a5f4235a71f70c4e3c03fb48f0beb91?lang=en)
53. [System Usability Scale Benchmarking for Digital Health Apps: Meta-analysis - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9437782/)
54. [10 Usability Heuristics for User Interface Design](https://principles.design/examples/10-usability-heuristics-for-user-interface-design)
55. [playwright · PyPI](https://pypi.org/project/playwright/)
56. [pytest-qt/CHANGELOG.rst at main · pytest-dev/pytest-qt · GitHub](https://github.com/pytest-dev/pytest-qt/blob/main/CHANGELOG.rst)
57. [pywinauto 0.6.9 on PyPI - Libraries.io - security & maintenance data for open source software](https://libraries.io/pypi/pywinauto)
58. [FlaUI latest version - Awesome .NET](https://dotnet.libhunt.com/flaui-latest-version)
59. [Move to Qt 6.12 LTS: Qt 6.10.3 and 6.11.1 have published CVEs and no more fixes · Issue #165 · nicolas-goyon/FinanceDashboard · GitHub](https://github.com/nicolas-goyon/FinanceDashboard/issues/165)
60. [\[Bug\]: python-playwright 1.65 · Issue #44004 · microsoft/playwright · GitHub](https://github.com/microsoft/playwright/issues/44004)
61. [Apple Human Interface Guidelines: Design Essentials](https://www.brilworks.com/blog/apple-human-interface-guidelines/)
62. [(PDF) Choice Overload: Is There Anything to It](https://www.researchgate.net/publication/255702128_Choice_Overload_Is_There_Anything_to_It)
63. [The Jam Study and Choice Overload: When the Moderators Matter More Than the Main Effect](https://atticusli.com/replication-crisis/choice-overload-jam-study/)
64. [pytest-qt 4.5.0 on PyPI - Libraries.io - security & maintenance data for open source software](https://libraries.io/pypi/pytest-qt)
