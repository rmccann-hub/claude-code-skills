# Windows and dialogs

Read this for when a window or dialog should appear, whether it's modal, where focus starts and
what Return does, a dialog over another or hidden behind its parent, confirmation against undo,
a window shown before it's ready or left open after its subject is gone, and long operations,
progress and notifications.

A heuristic review of a whole interface, and status lines in general, are `usability-review`'s;
where settings live, `settings-and-options`; testing dialogs, `gui-testing`. Keyboard access
and screen readers are the `accessibility` module's, in the `visual-design` skill; this module
covers only a dialog's focus and keys.

## Rules

Follow the host platform's guidelines (GNOME, KDE, Apple, Microsoft), not the toolkit's
habits. They differ on button order and the default button.

1. **A dialog appears only in answer to the person's own action, or when the app can't go on
   without an answer.** Never from a timer, a background check or finished work (facts
   `uxw-gnome-unexpected`, `uxw-kde-interrupt`). An update offer goes in the window: a banner,
   the status line or a notification.
2. **Every dialog has a parent window, and is modal to it only when it must be** (facts
   `uxw-gnome-parent`, `uxw-gnome-secondary`, `uxw-apple-modality`). The parent keeps it above
   its window and closes with it.
3. **One dialog at a time.** A dialog doesn't open another (facts `uxw-kde-one-dialog`,
   `uxw-gnome-secondary`). Apple lets one alert sit over a modal view, never two alerts (fact
   `uxw-apple-modality`); WinUI throws on a second ContentDialog (fact `uxw-winui-api`). When a
   second trigger fires, bring the open dialog forward, queue the request, or refuse it.
4. **Focus starts where the person acts first, and Return never runs a destructive action.**
   Return activates the affirmative button; on a destructive or irreversible one, set no
   default. Cancel isn't the default either, and Esc cancels. Every dialog has a safe way out,
   and the affirmative button is a verb, such as Save (facts `uxw-gnome-buttons`,
   `uxw-apple-alerts`, `uxw-apple-destructive-primary`, `uxw-winui-buttons`).
5. **Offer undo before a confirmation.** Confirm only what can't be undone, and name what will
   be lost (facts `uxw-gnome-undo`, `uxw-apple-alerts`). A field's error shows beside it (fact
   `uxw-winui-buttons`); a minor error can be a toast (fact `uxw-gnome-error-toast`).
6. **Show nothing before the state it shows is ready.** A window opens with its content loaded,
   or with a loading state nobody could take for data: no placeholder, last run's result or
   unmeasured estimate. This is this repository's practice, from audits; no platform guideline
   found states it.
7. **A window that outlives its subject is updated or closed.** When the device goes, the job
   ends or the file is deleted, the window says so and disables what no longer works, or
   closes. Also this repository's practice, from audits.
8. **Long work shows progress in the window, can be canceled, and says when it's done.** A
   modal progress dialog is only for work the app must finish first (fact
   `uxw-kde-interrupt`). Otherwise show progress in the window, with a Cancel that stops the
   work, and announce background work's end with a notification. Past KDE's rule, this is our
   practice; the platforms' progress and notification pages weren't read.

### Checking modality and stacking in code review

- List every place a window, dialog, message box or file picker is created and shown.
- Find each one's trigger. A timer, a thread, a network reply or start-up breaks rule 1.
- Find its parent: the parent argument, the transient-for setting, or WinUI's `XamlRoot`
  (fact `uxw-winui-api`). None is a finding.
- Ask what happens when its trigger fires twice, or two fire together, such as an update check
  ending as the person opens Settings. Count the dialogs.
- Check how it ends: closed, or only hidden. A hidden modal can still block input.

## Mistakes

- **A modal dialog with no parent.** In an audited desktop application, each update offer left
  one behind the main window, blocking input with nothing in sight. Parent every dialog, and
  put the offer in the window.
- **A dialog that opens itself.** There, a file picker opened when an earlier step finished,
  under the next dialog. Open a picker only on a click, parented to the window that asked.
- **Filling a window after showing it.** Its start-up estimate showed a speed it had never
  measured. Show a loading state until the value exists.
- **A window that keeps a gone subject.** Its main window kept showing an unplugged device.
  Handle the removal.
- **A confirmation for every delete,** which people click through. Delete, then offer undo.
- **A destructive default,** so Return deletes. Set no default there.
- **WinUI's `ShowAsync` without `XamlRoot`, or the deprecated `MessageDialog`** (fact
  `uxw-winui-api`).

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A modal dialog with no parent | No parent argument or transient-for | `BLOCKER` where it can block input unseen; `GAP` otherwise | Parent it to the window that asked |
| A dialog no user action opened | Dialogs shown from timers, threads, network replies or start-up | `GAP` | A banner, the status line or a notification |
| Two dialogs at once | A dialog that opens one; two triggers that can fire together | `BLOCKER` where it throws (fact `uxw-winui-api`); `GAP` otherwise | Bring forward, queue or refuse the second |
| A destructive default | Return or the default role on Delete, Overwrite or Discard | `GAP` | No default there |
| Confirming an undoable action | Confirm dialogs on deletes the app could undo | `OVER` | Undo instead |
| A window shown before its state | Values drawn before they're loaded or measured | `DRIFT` | A loading state |
| A window that outlives its subject | No handler for the subject's removal or end | `DRIFT` | Update it, disable its actions, or close it |
| Modal progress for work that needn't block | A progress dialog over work that could run beside other work | `OVER` | Progress in the window, with Cancel |
| Background work ends silently | Nothing shown when it finishes or fails | `GAP` | A notification, or a toast |

## Why

### Dialogs on request, parented, one at a time

- **The advice:** rules 1 to 3.
- **The reason:** a dialog nobody asked for takes focus from work in progress. Without a
  parent, it may land anywhere, and a modal one hidden behind its window blocks input with no
  sign why. Both audit findings began so.
- **What others do, and why:** GNOME allows only dialogs that answer an action (fact
  `uxw-gnome-unexpected`); KDE names two reasons to interrupt (fact `uxw-kde-interrupt`); Apple
  asks for a clear benefit, and dismissal before the next modal view (fact
  `uxw-apple-modality`). WinUI enforces one dialog per window (fact `uxw-winui-api`).
- **What it costs:** a banner, which is easier to miss, and code for a second request.
- **When to choose differently:** unsaved changes at close; an urgent alert over a modal view,
  as Apple allows. A Browse button's file picker breaks KDE's rule; parent it to that dialog
  so it opens above.

### Focus and the default button

- **The advice:** rule 4.
- **The reason:** Return pressed by habit, from the keyboard, shouldn't destroy work.
- **What others do, and why:** GNOME puts Cancel first (fact `uxw-gnome-buttons`); WinUI puts
  the safe button rightmost and sets no default unless asked (fact `uxw-winui-buttons`). Apple
  revised its advice in 2024: Cancel isn't the default either (fact `uxw-apple-alerts`). Quote
  the current page, not an older copy.
- **What it costs:** one more key press on a destructive dialog.
- **When to choose differently:** button order follows the host platform; no order suits all.

### Undo over confirmation

- **The advice:** rule 5.
- **The reason:** people click through confirmations by habit, so they protect little (facts
  `uxw-gnome-undo`, `uxw-kde-interrupt`). Apple avoids alerts for common undoable actions,
  even destructive ones (fact `uxw-apple-alerts`).
- **What it costs:** the deleted state is kept for a while.
- **When to choose differently:** an action nothing can reverse, such as erasing a disk.

### Ready before shown, closed when gone

- **The advice:** rules 6 and 7.
- **The reason:** a window states the present. An unplugged device, or a speed never measured,
  is false, and people act on it. The audited application showed both.
- **What others do, and why:** no platform guideline found states either rule. Nielsen's first
  heuristic, keeping people informed about what is going on, is the nearest.
- **What it costs:** loading states, and handlers for removal and completion.
- **When to choose differently:** a finished job's window kept as a record, marked finished.

### Long operations

- **The advice:** rule 8.
- **The reason:** a modal progress dialog stops all other work for a task that may not need it.
- **What others do, and why:** KDE keeps progress dialogs for work the app must finish first
  (fact `uxw-kde-interrupt`); GNOME uses toasts for minor errors (fact `uxw-gnome-error-toast`).
- **What it costs:** the app must stay usable while the work runs.
- **When to choose differently:** work everything depends on, such as a start-up migration.

## Facts

Guidelines, each named elsewhere in this module by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `uxw-gnome-unexpected` | GNOME: no unexpected dialogs | [GNOME: Dialogs](https://developer.gnome.org/hig/patterns/feedback/dialogs.html) | "Never pop up a dialog window unexpectedly." | 2026-11-10 | 2027-05-10 |
| `uxw-gnome-parent` | GNOME: a dialog is modal to its parent | [GNOME: Dialogs](https://developer.gnome.org/hig/patterns/feedback/dialogs.html) | "Dialogs should always have a parent window, to which they are modal." | 2026-11-10 | 2027-05-10 |
| `uxw-gnome-buttons` | GNOME: focus, button order, keys and labels | [GNOME: Dialogs](https://developer.gnome.org/hig/patterns/feedback/dialogs.html) | "provide initial keyboard focus to the component that you expect users to operate first." and "the cancel button appears first" and "Ensure that the Esc key activates the cancel button" and "this should not be done if its action is irreversible, destructive" and "Label the affirmative button with a specific imperative verb" | 2026-11-10 | 2027-05-10 |
| `uxw-gnome-undo` | GNOME: undo usually beats a confirmation | [GNOME: Dialogs](https://developer.gnome.org/hig/patterns/feedback/dialogs.html) | "users will often habitually click through confirmation dialogs" and "undo is typically a better option than a confirmation dialog." | 2026-11-10 | 2027-05-10 |
| `uxw-gnome-error-toast` | GNOME: toasts for minor errors | [GNOME: Dialogs](https://developer.gnome.org/hig/patterns/feedback/dialogs.html) | "For simple non-critical errors, toasts can be a good alternative." | 2026-11-10 | 2027-05-10 |
| `uxw-gnome-secondary` | GNOME: secondary windows close with the primary and don't stack | [GNOME: Windows](https://developer.gnome.org/hig/patterns/containers/windows.html) | "so that closing the primary also closes the secondary." and "Avoid stacking secondary windows on top of one another." | 2026-11-10 | 2027-05-10 |
| `uxw-kde-interrupt` | KDE: dialogs only for a decision or blocking progress | [KDE: Getting input](https://develop.kde.org/hig/getting_input/) | "many users click through them without reading anything." and "Only interrupt the user with a dialog window for one of two reasons" and "To display progress information about a task that must complete before the app can continue working normally." | 2026-11-10 | 2027-05-10 |
| `uxw-kde-one-dialog` | KDE: one dialog at a time | [KDE: Getting input](https://develop.kde.org/hig/getting_input/) | "Don't display more than one dialog at a time. Never use a dialog to create more dialogs." | 2026-11-10 | 2027-05-10 |
| `uxw-apple-modality` | Apple: when to be modal, and stacking | [Apple: Modality](https://developer.apple.com/tutorials/data/design/human-interface-guidelines/modality.json) | "Present content modally only when there's a clear benefit." and "Let people dismiss a modal view before presenting another one." and "you never want to display more than one alert at the same time." | 2026-11-10 | 2027-05-10 |
| `uxw-apple-alerts` | Apple: undo over alerts; Cancel not the default, revised 2024-02-02 | [Apple: Alerts](https://developer.apple.com/tutorials/data/design/human-interface-guidelines/alerts.json) | "Avoid displaying alerts for common, undoable actions, even when they're destructive." and "you don't want to make a Cancel button the default button." and "Enhanced guidance for using default and Cancel buttons." | 2026-11-10 | 2027-05-10 |
| `uxw-apple-destructive-primary` | Apple: a destructive button never takes the primary role | [Apple: Buttons](https://developer.apple.com/tutorials/data/design/human-interface-guidelines/buttons.json) | "Don't assign the primary role to a button that performs a destructive action" | 2026-11-10 | 2027-05-10 |
| `uxw-winui-buttons` | WinUI: safe action, button order, default, inline errors | [Microsoft: Dialogs](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/dialogs) | "at least one safe action button" and "The safe, nondestructive action should appear as the rightmost button." and "By default, no default button is set." and "Don't use dialogs for errors that are contextual to a specific place on the page" | 2026-11-10 | 2027-05-10 |
| `uxw-winui-api` | WinUI: what throws, and what's deprecated | [Microsoft: Dialogs](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/dialogs) | "Attempting to open two content dialogs will throw an exception." and "If you don't set XamlRoot, the dialog throws an exception at runtime." and "Don't use the deprecated MessageDialog API." | 2026-11-10 | 2027-05-10 |

## Sources

| Source | Used for | License |
|---|---|---|
| [GNOME HIG](https://developer.gnome.org/hig/): Dialogs, Windows | Dialogs, buttons, undo, stacking | None stated: facts in our own words, short quotes |
| [KDE HIG: Getting input](https://develop.kde.org/hig/getting_input/) | When to interrupt, one dialog at a time | CC BY-SA 4.0: brief quotes with attribution, our own words otherwise |
| [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/): Modality, Alerts, Buttons, read through each page's data | Modal views, alerts, buttons | All rights reserved: facts in our own words, short quotes |
| [Microsoft Learn: Dialogs](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/dialogs) | WinUI's ContentDialog | None stated: facts in our own words, short quotes |
| An audited desktop application, unnamed here | The audit evidence in Mistakes | Observed practice, in our own words |
