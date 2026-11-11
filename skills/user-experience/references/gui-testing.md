# GUI testing

Read this for testing a desktop or web interface by machine: choosing a driver for Qt, GTK, the
web, Electron or Windows, writing tests that catch a window or dialog at the wrong time, a stale
status or a view that keeps a removed device, and running them in CI with no display. Read it too
for testing with people: task-based sessions, think-aloud and the System Usability Scale (SUS).

A review against heuristics is `usability-review`. What a window or dialog should do is
`windows-and-dialogs`, and settings are `settings-and-options`; this module tests that the program
does it. General test design (doubles, flaky tests, gates) belongs to the planned testing skill,
and accessibility itself to the accessibility module of the planned visual-design skill: here the
accessibility interfaces are a way in.

## Rules

1. **Drive the interface through the toolkit's test helper or the platform's accessibility
   interface,** whichever reaches what the person uses.
2. **Give each classic failure a test of its own:** a window or dialog that appears unasked,
   appears before its data is ready, hides behind another or stays open; a status that outlives
   its job; a view that keeps a removed device.
3. **Assert on what the person sees:** visible text, accessible names and roles, which windows are
   open. Not on a model's fields or a private flag.
4. **Wait on a condition, never for a fixed time.**
5. **Run headless in CI where the toolkit allows it, and know what headless can't show:**
   stacking, focus and real modality need a window manager.
6. **Prove each test can fail:** plant the defect once and watch the test go red.
7. **Test with people too:** a few task-based sessions with think-aloud, then SUS. Never a survey
   alone.

### Choosing the driver

| Interface | Driver | Note |
|---|---|---|
| Qt, C++ | Qt Test, whose mouse and keyboard simulation Qt calls basic (fact `uxt-qt-test-gui`) | Both Qt drivers see widgets, not the window manager |
| PyQt, PySide | pytest-qt's `qtbot` (fact `uxt-pytest-qt`) on pytest (fact `uxt-pytest`) | |
| GTK 4 | dogtail, through AT-SPI, on Xorg or Wayland GNOME (fact `uxt-dogtail`) | GTK 4's own test functions can't click or type (fact `uxt-gtk4-test-api`); use them in-process for accessibility assertions, after `gtk_test_init` (fact `uxt-gtk4-test-init`) |
| Web | Playwright (fact `uxt-playwright`), its assertions waiting for the condition (fact `uxt-playwright-wait`) | Find elements by role and name |
| Electron | Playwright, whose support is experimental (fact `uxt-playwright-electron`) | It doesn't see native dialogs: stub them in the main process, and test the real ones by hand |
| Windows | pywinauto from Python (fact `uxt-pywinauto`), FlaUI from .NET (fact `uxt-flaui`) | Pin pywinauto's stable release; try the pre-release on a branch |

### Tests for the classic failures

Each reached users of an audited desktop application:

- **Unasked:** start the program, do nothing, and assert no dialog opens. A file picker there
  opened by itself, under the next dialog.
- **Before it's ready:** assert that the window's first visible state holds real data, not a
  placeholder or a value never measured. A start-up estimate there showed a speed it had never
  measured. This one is this repository's practice; no platform states it.
- **Hidden or left open:** after each flow, assert no modal window is open, including one behind
  the main window, and that each dialog's parent is the window it serves. Each update offer there
  left a modal behind the main window, blocking input.
- **Stale status:** finish a job, start the next, and assert the old verdict is gone. A status
  line there kept "Passed" through the next job.
- **Removed device:** simulate removal with a fake device source, and assert the device leaves
  every view. The main window there kept showing an unplugged device.

```python
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QListWidget, QPushButton

from myapp import MainWindow  # the application under test
from myapp.testing import FakeBus  # stands in for the hardware


def shown(qtbot, bus):
    window = MainWindow(bus=bus)
    qtbot.addWidget(window)
    window.show()
    qtbot.waitExposed(window)
    return window


def open_modals():
    return [w for w in QApplication.topLevelWidgets() if w.isVisible() and w.isModal()]


def test_an_unplugged_device_leaves_the_list(qtbot):
    bus = FakeBus(devices=["Drive A", "Drive B"])
    devices = shown(qtbot, bus).findChild(QListWidget, "devices")

    bus.unplug("Drive A")

    def rows():
        return [devices.item(i).text() for i in range(devices.count())]

    qtbot.waitUntil(lambda: rows() == ["Drive B"])  # a condition, never a sleep
    assert open_modals() == []  # none left open, even behind the main window


def test_the_last_verdict_goes_when_the_next_job_starts(qtbot):
    bus = FakeBus(devices=["Drive A"])
    window = shown(qtbot, bus)
    status = window.findChild(QLabel, "status")
    start = window.findChild(QPushButton, "start")

    qtbot.mouseClick(start, Qt.MouseButton.LeftButton)
    bus.finish(ok=True)
    qtbot.waitUntil(lambda: status.text() == "Passed")

    qtbot.mouseClick(start, Qt.MouseButton.LeftButton)
    qtbot.waitUntil(lambda: "Passed" not in status.text())
```

Under `QT_QPA_PLATFORM=offscreen`, both pass against a correct window and each fails with its
defect planted.

### Headless in CI

Qt ships an `offscreen` platform plugin (fact `uxt-qt-headless`), and `QT_QPA_PLATFORM=offscreen`
runs widget tests with no display. Tools that need a real session, such as dogtail, run under a
virtual X server or a nested compositor, with a session bus. These setups are this repository's
practice. None shows real stacking or focus: test those on a desktop.

### Testing with people

Give a few people real tasks, such as "export last week's results", not "click Start". Ask them
to think aloud, and watch without helping. Then they fill in SUS, whose average is 68 (fact
`uxt-sus-average`): average, not a pass. The score compares; what you watched says what to fix.
The session count and think-aloud are this repository's practice; its research didn't cover them.

## Mistakes

- **`time.sleep(2)` before an assertion.** Too short on a slow runner, wasted on a fast one. Wait
  on the condition (`qtbot.waitUntil`, Playwright's waiting assertions).
- **Asserting on the model.** `window.model.devices` can be right while the list still shows the
  drive. Read the list's rows.
- **"The dialog exists" as the whole test.** A modal behind the main window exists and is visible
  to the toolkit. Assert it was asked for, has the right parent, and is closed when the flow ends.
- **Clicking through GTK 4's test API.** `gtk_test_widget_click` is GTK 3's, and deprecated; GTK 4
  has none (facts `uxt-gtk3-click`, `uxt-gtk4-test-api`). Drive it through AT-SPI.
- **A test never seen red.** It may assert on the wrong widget, or on a condition that always
  holds. Plant the defect, see it fail, restore the fix.
- **Mocking the window away.** A test of a double proves the double. Double the hardware and
  the network, not the interface under test.
- **Reading a SUS of 68 as a pass,** or sending a survey instead of watching anyone.
- **Pinning pywinauto 1.0.0b1 as the highest version.** It's a pre-release (fact `uxt-pywinauto`).

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A GUI no test drives | Tests that only call the model | `GAP` | Add a driver from the table, and one test per classic failure |
| A classic failure with no test | Search for start-up, removal, next-job and leftover-modal cases | `GAP` | Add it, and plant its defect once |
| Fixed sleeps | `sleep(`, `waitForTimeout(`, `qWait(` before an assertion | `GAP` | Wait on the condition |
| Assertions on internal state | Asserts on model fields where the view shows the value | `ADVISORY` | Assert on the visible text or accessible name |
| A GUI test never seen to fail | No planted-defect run in the pull request or its record | `ADVISORY` | Plant the defect, record the red run, restore |
| GUI tests skipped in CI for lack of a display | A skip on `DISPLAY`, or no GUI job | `GAP` | Offscreen, a virtual display or a nested compositor |
| A usability claim from a survey alone | SUS or a questionnaire with no observed tasks | `ADVISORY` | Watch a few task-based sessions |

## Why

**Drivers.** The toolkit helper is fastest and sees widget state; the accessibility interface
sees what assistive technology sees, across processes, and catches a control with no name.
GTK 4 removed click synthesis from its test API (fact `uxt-gtk4-test-api`), so AT-SPI is its way
in. Cost: accessibility-interface tests need a desktop session. Choose the toolkit helper when a
test is about one widget's logic.

**Classic failures.** Each reached users of an audited desktop application, and a test per
failure keeps a fixed one fixed. Cost: a fake device source or a hook to finish a job, which the
program may lack. Where adding one is out of reach, put a manual check in the release steps.

**What the person sees.** A view can drop a model's update, as the unplugged device showed, and
only an assertion on the view catches it. Cost: tests break when a label's wording changes. Find
elements by object name or role, and assert on text only where the text is the point.

**Conditions, not sleeps.** A sleep is a guess about timing that the next runner breaks. A
condition with a timeout passes as soon as it holds, and fails with a reason.

**Headless.** CI with no display still runs most widget tests. Stacking and focus belong to
the window manager, so they need a real session or people.

**Planted defects.** A test that has never failed may test nothing. This repository plants each
defect once before trusting a check. Cost: one extra run per new test.

**People.** Machine tests protect behavior once it's defined; they don't find that a task is
confusing. Watching people does, and SUS gives a number to compare across releases, not a
verdict. Choose differently only for a change with no visible effect.

## Facts

Versions, defaults and figures, each named elsewhere in this module by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `uxt-qt-test-gui` | Qt Test's GUI support is basic: mouse and keyboard simulation | [Qt Test overview](https://doc.qt.io/qt-6/qtest-overview.html) | "Basic GUI testing" and "Qt Test offers functionality for mouse and keyboard simulation." | 2026-11-10 | 2027-02-10 |
| `uxt-qt-headless` | Qt's platform plugins include `offscreen`, and `minimal`, which runs where there's no GUI | [QGuiApplication](https://doc.qt.io/qt-6/qguiapplication.html) | "offscreen" and "you can use the plugin to run GUI applications in environments without a GUI, such as servers" | 2026-11-10 | 2027-02-10 |
| `uxt-pytest-qt` | pytest-qt 4.5.0, 2025-07-01, for PyQt and PySide | [PyPI](https://pypi.org/pypi/pytest-qt/json) | "pytest support for PyQt and PySide applications" and "4.5.0" and "2025-07-01T17:24:38" | 2026-11-10 | 2027-02-10 |
| `uxt-pytest` | pytest 9.2.0, 2026-10-27 | [PyPI](https://pypi.org/pypi/pytest/json) | "9.2.0" and "2026-10-27T21:30:19" | 2026-11-10 | 2027-02-10 |
| `uxt-gtk4-test-api` | GTK 4's test functions cover set-up, type registration, waiting for a draw and accessibility assertions, with no click or key synthesis | [GTK 4 reference](https://docs.gtk.org/gtk4/index.html) | "test_widget_wait_for_draw" and "test_accessible_assert_role" | 2026-11-10 | 2027-02-10 |
| `uxt-gtk3-click` | GTK 3's click helper is deprecated since 3.20, in favor of reftests | [gtk_test_widget_click](https://docs.gtk.org/gtk3/func.test_widget_click.html) | "Deprecated since: 3.20" and "This testing infrastructure is phased out in favor of reftests." | 2026-11-10 | 2027-02-10 |
| `uxt-gtk4-test-init` | `gtk_test_init` makes the test environment deterministic | [gtk_test_init](https://docs.gtk.org/gtk4/func.test_init.html) | "This is done to make test program environments as deterministic as possible." | 2026-11-10 | 2027-02-10 |
| `uxt-dogtail` | dogtail 2.1.2, 2026-10-26, drives applications through AT-SPI on Xorg and Wayland GNOME | [PyPI](https://pypi.org/pypi/dogtail/json) | "uses Accessibility (AT-SPI) technologies" and "Dogtail supports both **Xorg** and **Wayland GNOME** environments." and "2026-10-26T13:40:27" | 2026-11-10 | 2027-02-10 |
| `uxt-playwright` | Playwright 1.65.0; the Python package came out 2026-11-09 | [PyPI](https://pypi.org/pypi/playwright/json) | "1.65.0" and "2026-11-09T21:09:30" | 2026-11-10 | 2027-02-10 |
| `uxt-playwright-wait` | Playwright's web assertions wait until their condition holds | [Assertions](https://playwright.dev/docs/test-assertions) | "Playwright also includes web-specific async matchers that will wait until the expected condition is met." | 2026-11-10 | 2027-02-10 |
| `uxt-playwright-electron` | Playwright's Electron support is experimental, and doesn't intercept native dialogs | [Electron](https://playwright.dev/docs/api/class-electron) | "Playwright has experimental support for Electron automation." and "Playwright does not intercept the native Electron dialog API" | 2026-11-10 | 2027-02-10 |
| `uxt-pywinauto` | pywinauto 0.6.9 (2025-01-06) is stable; 1.0.0b1 (2026-10-15) is a pre-release | [PyPI](https://pypi.org/pypi/pywinauto/json) | "A set of Python modules to automate the Microsoft Windows GUI" and "2025-01-06T11:29:55" and "2026-10-15T16:32:42" | 2026-11-10 | 2027-02-10 |
| `uxt-flaui` | FlaUI.UIA3 5.0.0, 2025-02-25 | [NuGet](https://api.nuget.org/v3/registration5-semver1/flaui.uia3/index.json) | "Library to use FlaUI with UIA3." and "2025-02-25T12:34:06" | 2026-11-10 | 2027-02-10 |
| `uxt-sus-average` | The mean SUS score across 500 studies is 68; above 80.3 is an A | [MeasuringU](https://measuringu.com/sus/) | "The average SUS score from all 500 studies is a 68." and "You'd need to score above an 80.3 to get an A (the top 10% of scores)" | 2026-11-10 | 2027-05-10 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Qt documentation](https://doc.qt.io/qt-6/) | Qt Test's scope, platform plugins | GFDL 1.3: short quotes with attribution, our own words otherwise |
| [GTK documentation](https://docs.gtk.org/) | GTK 4's and GTK 3's test functions | LGPL-2.1-or-later: short quotes, our own words otherwise |
| [PyPI](https://pypi.org/) and [NuGet](https://www.nuget.org/) package data | Versions, dates and summaries | pytest-qt, pytest MIT; dogtail GPL-2.0; pywinauto BSD-3-Clause; Playwright Apache-2.0: metadata quoted, no code |
| [Playwright documentation](https://playwright.dev/docs/intro) | Waiting assertions, Electron | Not checked: short quotes only |
| [MeasuringU, SUS](https://measuringu.com/sus/) | The SUS average and grades | No license seen: short quotes only |
| An audited desktop application, unnamed | The classic failures | Observed practice, in our own words |
