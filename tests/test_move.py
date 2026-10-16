"""`skillcheck --move MODULE SKILL`: a module changes home in one command, or nothing changes."""

from datetime import date

import pytest

from skillcheck import move
from skillcheck.cli import main
from skillcheck.core import modules
from skillcheck.core.checks import check_repository

DAY = date(2026, 10, 16)


@pytest.fixture
def two(repo):
    """Skills `one` (modules `first`, `second`) and `two` (module `third`), all shipped."""
    repo.modular_skill("one", "first", "second")
    repo.modular_skill("two", "third")
    repo.catalog(repo.plugin("p", "./skills/one", "./skills/two"))
    repo.roadmap(
        {"one": "shipped", "two": "shipped"},
        {"first": ("one", "shipped"), "second": ("one", "shipped"), "third": ("two", "shipped")},
    )
    return repo


def snapshot(root):
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_a_move_updates_every_place_and_the_repository_still_passes(two):
    changed = move.move(two.root, "first", "two", DAY)
    assert changed == [
        "moved skills/one/references/first.md to skills/two/references/first.md",
        "moved the router row from one to two",
        "set module `first`'s skill to `two` in ROADMAP.md",
        "recorded the move in docs/module-moves.md",
    ]
    assert not (two.root / "skills/one/references/first.md").exists()
    assert "[`first`]" in (two.root / "skills/two/SKILL.md").read_text(encoding="utf-8")
    assert "[`first`]" not in (two.root / "skills/one/SKILL.md").read_text(encoding="utf-8")
    assert "| `first` | `two` | shipped |" in (two.root / "ROADMAP.md").read_text(encoding="utf-8")
    record = (two.root / move.RECORD).read_text(encoding="utf-8")
    assert record.startswith(move.RECORD_HEADER)
    assert record.endswith("| 2026-10-16 | `first` | `one` | `two` |\n")
    assert check_repository(two.root).findings == []


def test_a_move_that_empties_a_skill_says_so(two):
    changed = move.move(two.root, "third", "one", DAY)
    assert changed[-1] == "two has no modules left: remove it, or route another module"


def test_later_moves_add_to_the_record(two):
    move.move(two.root, "first", "two", DAY)
    path = two.root / move.RECORD
    path.write_text(path.read_text(encoding="utf-8").rstrip("\n"), encoding="utf-8")
    move.move(two.root, "first", "one", DAY)
    rows = [line for line in path.read_text(encoding="utf-8").splitlines() if "2026" in line]
    assert rows == [
        "| 2026-10-16 | `first` | `one` | `two` |",
        "| 2026-10-16 | `first` | `two` | `one` |",
    ]


def test_a_move_without_a_roadmap_row_still_moves(two):
    (two.root / "ROADMAP.md").unlink()
    changed = move.move(two.root, "first", "two", DAY)
    assert "ROADMAP.md" not in " ".join(changed[:3])
    assert (two.root / "skills/two/references/first.md").is_file()


def test_a_roadmap_without_the_modules_row_is_left_alone(two):
    (two.root / "ROADMAP.md").write_text("# Roadmap\n\n| `first` | not a skill |\n", "utf-8")
    changed = move.move(two.root, "first", "two", DAY)
    assert not any("ROADMAP.md" in line for line in changed)
    assert "not a skill" in (two.root / "ROADMAP.md").read_text(encoding="utf-8")


def test_the_date_defaults_to_today(two):
    move.move(two.root, "first", "two")
    record = (two.root / move.RECORD).read_text(encoding="utf-8")
    assert f"| {date.today().isoformat()} | `first` |" in record


def plain_skill(repo, name):
    repo.skill(name)


@pytest.mark.parametrize(
    ("name", "target", "prepare", "message"),
    [
        ("ghost", "two", None, "no skill routes a module `ghost`"),
        ("first", "one", None, "`first` is already in `one`"),
        (
            "first",
            "nowhere",
            None,
            "there's no skill `nowhere`; make it with `skillcheck --new nowhere` first",
        ),
        ("first", "plain", "plain", "`plain` has no Modules section to route `first`"),
        ("first", "two", "taken", "skills/two/references/first.md already exists"),
        ("first", "two", "missing", "`first` has no file at skills/one/references/first.md"),
        ("first", "two", "twice", "`first` is routed by one, two; fix that first"),
    ],
)
def test_a_refused_move_changes_nothing(two, name, target, prepare, message):
    root = two.root
    if prepare == "plain":
        two.skill("plain")
    elif prepare == "taken":
        (root / "skills/two/references/first.md").write_text("# Taken\n", encoding="utf-8")
    elif prepare == "missing":
        (root / "skills/one/references/first.md").unlink()
    elif prepare == "twice":
        modules.add_row(root / "skills/two/SKILL.md", "| [`first`](references/first.md) | again |")
    (root / "skills" / "stray").mkdir()
    before = snapshot(root)
    with pytest.raises(move.MoveError) as error:
        move.move(root, name, target, DAY)
    assert str(error.value) == message
    assert snapshot(root) == before


def test_the_command_moves_and_says_what_comes_next(two, capsys):
    assert main([str(two.root), "--move", "first", "two"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0] == "moved skills/one/references/first.md to skills/two/references/first.md"
    assert out[-1].startswith("skillcheck: moved first to two.")


def test_the_command_refuses_and_exits_one(two, capsys):
    assert main([str(two.root), "--move", "ghost", "two"]) == 1
    assert capsys.readouterr().out == "move: no skill routes a module `ghost`\n"
