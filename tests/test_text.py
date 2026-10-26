"""Text from outside the repository is printed with its control and hidden characters shown."""

from skillcheck import skills_hook
from skillcheck.core.text import HIDDEN, printable


def test_escape_sequences_and_forged_lines_are_spelled_out():
    assert printable("\x1b[2Jcleared\rover\nforged") == "\\x1b[2Jcleared\\x0dover\\x0aforged"
    assert printable("\x9b31m") == "\\x9b31m"  # the one-byte C1 escape


def test_hidden_characters_are_named_and_ordinary_text_is_left_alone():
    assert printable("a\u202eb\u200bc\U000e0041") == "a<U+202E>b<U+200B>c<U+E0041>"
    assert printable("Tab\tand café, 5 × 3 — fine.") == "Tab\tand café, 5 × 3 — fine."


def test_the_install_hook_holds_the_same_hidden_characters():
    assert skills_hook.HIDDEN.pattern == HIDDEN.pattern
