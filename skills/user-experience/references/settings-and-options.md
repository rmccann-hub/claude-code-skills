# Settings and options

Read this for designing or reviewing a program's settings: defaults, presets, advanced options
a step away, each setting in one place under one name, the control for a choice, whether a page
has too many options, and an inventory of every setting.

A heuristic review of a whole interface is `usability-review`'s; a settings dialog's behavior as
a window is `windows-and-dialogs`'; automated tests are `gui-testing`'s. Contrast, screen-reader
labels and keyboard reach are the `accessibility` module of the `visual-design` skill; this
module asks only that a disabled control says why.

## Rules

1. **Give every setting a default good enough that most people never open the settings** (fact
   `uxs-nng-defaults`). A setting with no default makes everyone decide.
2. **Offer presets for the combinations people set together, and keep every option behind them
   reachable.** A preset shows the values it sets, and changing one turns it into "Custom".
3. **Show the common options first and the advanced ones one step away** (fact
   `uxs-nng-disclosure`). An advanced option sits in the group it qualifies, behind an expander.
   An "Advanced" page is the fallback for what fits no group.
4. **Give each setting one place and one name, and each label one meaning.** A shortcut, such as
   a toolbar toggle, changes the same stored value under the same words. No primary source
   states this; it's this repository's practice from audits, and follows from Nielsen's fourth
   heuristic (fact `uxs-nng-consistency`).
5. **Show an option's effect where it's set, and disable, rather than hide, an option that does
   nothing in the current mode,** with the reason beside it, such as "Needs a second drive".
   This repository's practice: a hidden option reads as a missing one.
6. **Treat a long list of options as a design problem, not a count problem.** Choice overload is
   conditional (facts `uxs-choice-meta-2010`, `uxs-choice-moderators`). What hurts is no
   default, no clear grouping, and settings scattered across places.
7. **Never remove a useful option from a power-user program to cut the count.** Use defaults,
   presets, grouping and disclosure (the owner's ruling, 2026-11-10).
8. **Pick each control by how its setting applies and how many choices it has,** from the
   platform's guidelines. KDE's are below (facts `uxs-kde-switch`, `uxs-kde-choices`); on GNOME,
   macOS or Windows, follow that platform's.
9. **A setting the CLI and the GUI both expose is one setting:** one name, one default, one
   stored value, with the flag named in the GUI's help. This repository's practice.
10. **Review a settings surface from an inventory of every setting,** below.

### Controls, by KDE's guidelines

| The setting | The control |
|---|---|
| On or off, taking effect at once | Switch |
| On or off, applied with the dialog's button, or an item in a list | CheckBox |
| One of 3 or fewer short choices, with room to stack them | Radio buttons |
| One of up to 10, or short of space | ComboBox |
| One of more than 10 | A scrollable list |

### The inventory

List every setting from the code that reads it, not from the dialog, so one only a flag, a
config key or an environment variable reaches still gets a row. For each: its label or name in
every place it's reached, its default, the modes where it does nothing, and the test that sets
it. Then look for a setting with two places or two names, two labels a person could take for
one another, a blank default, an option that silently does nothing, and an option no test sets.

## Mistakes

- **Adding a toggle instead of choosing a default,** a habit this repository's reviews watch
  for in AI-written code. Choose the default; add the option only if people need both.
- **Two controls of different meaning with similar labels.** An audited desktop application's
  console had two file pickers like that. Name each by what the file is for, such as "Source
  image" and "Output folder", or make them one picker if they're one setting.
- **Citing "more choice always hurts" as a law,** or the jam study as settled proof. The
  meta-analyses say it depends.
- **An "Advanced" page as a drawer for everything,** far from what each option qualifies, or
  options cut because a dialog "has too many". Group them, with defaults, the rare ones a step
  away.
- **A preset that keeps its name after a change,** or overwrites custom values unannounced.
- **One setting as `--out-dir`, "Destination" and `target`** in the CLI, the GUI and the config
  file, or a toolbar toggle with a stored value of its own. One name, one value.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| No inventory of settings | A list built from the code that reads settings | `GAP` | Build it from the code |
| A setting with no default | The inventory; the first-run path | `GAP` | The value most would pick |
| One setting in two places, names or stored values | The inventory's places and names | `GAP`; `BLOCKER` where two values can disagree | One stored value and name; other places are shortcuts |
| Two labels of different meaning that read alike | Labels side by side, such as file pickers | `GAP` | Name each by what it's for |
| An option hidden in some mode | Code that hides a control on a mode change | `GAP` | Disable it, with the reason |
| An option that does nothing in any mode | The inventory, and the code that reads it | `GAP` | Wire it up, or remove it with a record |
| A useful option removed to shorten a page | Removals in the history with no replacement | `GAP` | Restore it behind disclosure |
| A preset that hides its values or keeps its name after a change | Pick a preset, then change one option | `GAP` | Show its values; "Custom" on a change |
| A control that doesn't fit its setting | Switches applied on OK; over 3 radio buttons; combo boxes over 10 items | `GAP` | The control from the table above |
| A CLI flag and its GUI setting differ in name or default | Help output beside the dialog | `GAP` | One name and default |
| A setting no test sets | The inventory's tests | `GAP` | A test per setting that changes behavior |
| All of the above hold | The inventory and the checks | `OK` | Nothing |

## Why

### Defaults and presets

- **The advice:** a default for every setting, and presets for common combinations.
- **The reason:** NN/g counts good defaults among the ways to prevent slips (fact
  `uxs-nng-defaults`). Two of the moderators that bring choice overload on, preference
  uncertainty and an effort-minimizing goal (fact `uxs-choice-moderators`), are what a default
  and a preset answer. That presets help is this repository's practice; the research found no
  primary guidance on them.
- **What it costs:** a default is a decision someone owns, and a preset is a set of values to
  keep right as options change.
- **When to choose differently:** where no value is safe for most people, such as a target
  disk, ask, and remember the answer.

### Progressive disclosure

- **The advice:** common options first, advanced ones a step away, beside what they qualify.
- **The reason:** NN/g reports it improves learnability, efficiency of use and error rate (fact
  `uxs-nng-disclosure`), and it keeps every option, which a power-user program needs.
- **What it costs:** a step for those who need an advanced option, and a line between common
  and advanced sometimes drawn wrong.
- **When to choose differently:** a tool experts use all day may show everything, grouped.

### One place, one name, one meaning

- **The advice:** one place and one name per setting, one meaning per label, the CLI's and
  the GUI's included.
- **The reason:** an audited desktop application's console had two file pickers of different
  meaning and similar labels. A setting with two homes can hold two values, and nobody can tell
  which counts. Nielsen's fourth heuristic says people
  shouldn't have to wonder whether different words mean the same thing (fact
  `uxs-nng-consistency`). No primary source states the one-place rule; it's this repository's
  practice from audits, and the owner asked for no "options in many places" (2026-11-10).
- **What it costs:** a rename touches the CLI, the GUI, the config file and the docs at once.
- **When to choose differently:** a per-project override of a global setting is a second
  setting; name it as one, such as "This project only".

### Disabled rather than hidden

- **The advice:** effects shown where set; an inactive option disabled, with the reason.
- **The reason:** the owner asked that programs not "hide things" (2026-11-10). A control that
  vanishes with a mode looks gone; a disabled one with a reason says what to change. This
  repository's practice; no primary source in the research states it.
- **What it costs:** room for controls that can't be used now.
- **When to choose differently:** options for a plugin or hardware not installed at all may be
  left out, with one line saying what adds them.

### How many choices is too many

- **The advice:** fix grouping, defaults and scattering, not the count.
- **The reason:** a 2010 meta-analysis found a mean choice-overload effect of virtually zero
  (fact `uxs-choice-meta-2010`). A 2015 one found it significant once four moderators are
  counted (fact `uxs-choice-moderators`): task difficulty, a complex set,
  preference uncertainty and a wish to spend little effort. Grouping lowers the complexity;
  defaults and presets answer the rest. The studies measured satisfaction, regret, deferral and
  switching, not errors in software settings (fact `uxs-choice-measures`), so no number of
  options is a proven limit.
- **What others do, and why:** cutting options trades power for a shorter page, which can suit
  occasional users and fails a tool's power users.
- **What it costs:** a larger surface to group, document and test.
- **When to choose differently:** an option the inventory shows has no caller and no test can
  go, with the removal recorded.

### Controls and the inventory

- **Controls:** a Switch says the change happens now, a CheckBox that it waits for the dialog's
  button (fact `uxs-kde-switch`). KDE's counts pick the control, radio buttons, combo box or
  list (fact `uxs-kde-choices`); they size the control, not the page. Guidelines come from
  platforms, not toolkits: KDE writes its own for its Qt and Kirigami controls (fact
  `uxs-kde-qt`), and GNOME, Apple and Microsoft publish theirs.
- **The inventory:** each fault above shows up as a row, and a review that reads only the dialog
  misses what only a flag or a config key reaches. It costs upkeep as settings change.

## Facts

Guidelines and research, each named elsewhere in this module by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `uxs-nng-defaults` | NN/g: good defaults prevent slips | [10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | "Avoid slips by providing helpful constraints and good defaults." | 2026-11-10 | 2027-05-10 |
| `uxs-nng-consistency` | Nielsen's fourth heuristic: one word, one meaning | [10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | "Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions." | 2026-11-10 | 2027-05-10 |
| `uxs-nng-disclosure` | NN/g (2006-12-03): progressive disclosure improves learnability, efficiency and error rate | [Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/) | "Progressive disclosure thus improves 3 of usability's 5 components: learnability, efficiency of use, and error rate." | 2026-11-10 | 2027-05-10 |
| `uxs-choice-meta-2010` | Scheibehenne, Greifeneder and Todd (2010), 50 experiments, N = 5,036: mean effect virtually zero | [Scheibehenne et al. 2010](https://scheibehenne.com/ScheibehenneGreifenederTodd2010.pdf) | "The overall mean effect size across 63 conditions from 50 experiments in our meta-analysis was virtually zero." | 2026-11-10 | 2027-05-10 |
| `uxs-choice-moderators` | Chernev, Böckenholt and Goodman (2015), 99 observations, N = 7,202: four moderators make the effect significant | [Chernev et al. 2015](https://chernev.com/wp-content/uploads/2017/02/ChoiceOverload_JCP_2015.pdf) | "higher levels of decision task difficulty, greater choice set complexity, higher preference uncertainty, and a more prominent, effort-minimizing goal facilitate choice overload." and "when moderating variables are taken into account the overall effect of assortment size on choice overload is significant" | 2026-11-10 | 2027-05-10 |
| `uxs-choice-measures` | The 2015 analysis measured satisfaction or confidence, regret, deferral and switching, not errors in software | [Chernev et al. 2015](https://chernev.com/wp-content/uploads/2017/02/ChoiceOverload_JCP_2015.pdf) | No short quote: the paper's list of measures, checked by hand | 2026-11-10 | 2027-05-10 |
| `uxs-kde-switch` | KDE: a Switch for settings that apply at once, a CheckBox otherwise | [KDE HIG: Getting input](https://develop.kde.org/hig/getting_input/) | "Use a Switch for \"instant apply\" controls that take effect immediately. Use a CheckBox for everything else" | 2026-11-10 | 2027-05-10 |
| `uxs-kde-choices` | KDE: radio buttons for 3 or fewer, a ComboBox up to 10, a list above 10 | [KDE HIG: Getting input](https://develop.kde.org/hig/getting_input/) | "For 3 or fewer options with short text where vertical space is plentiful, use RadioButtons. For up to 10 items, or where vertical space is limited, use a ComboBox. For more than 10 options, use a scrollable list view." | 2026-11-10 | 2027-05-10 |
| `uxs-kde-qt` | KDE's guidelines name its Kirigami and Qt Quick controls | [KDE HIG: Getting input](https://develop.kde.org/hig/getting_input/) | "Kirigami.PromptDialog" and "QtQuick.Controls.TextField" | 2026-11-10 | 2027-05-10 |

## Sources

| Source | Used for | License |
|---|---|---|
| [NN/g, 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) and [Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/) | Defaults, consistency, disclosure | All rights reserved: facts in our own words, short quotes |
| [Scheibehenne et al. 2010](https://scheibehenne.com/ScheibehenneGreifenederTodd2010.pdf) | The mean choice-overload effect | Not stated in the copy read: short quotes only |
| [Chernev et al. 2015](https://chernev.com/wp-content/uploads/2017/02/ChoiceOverload_JCP_2015.pdf) | The moderators, and the measures | All rights reserved: facts in our own words, short quotes |
| [KDE HIG: Getting input](https://develop.kde.org/hig/getting_input/) | Controls for a setting | CC BY-SA 4.0: brief quotes with attribution, our own words otherwise |
| The owner's rulings (2026-11-10), and an audited desktop application, unnamed here | Nothing useful removed, hidden or in many places; two pickers alike | Observed practice, in our own words |
