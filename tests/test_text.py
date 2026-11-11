"""Text from outside the repository is printed with its control and hidden characters shown."""

import pytest

from skillcheck import skills_hook
from skillcheck.core.text import HIDDEN, printable

# Each run of code points HIDDEN names, first and last, written as numbers so this file holds
# none of them: the soft hyphen, the Mongolian vowel separator, zero-width characters and marks,
# bidirectional embeddings and overrides, invisible operators, bidirectional isolates, the
# variation selectors, the byte-order mark, the tag characters and the supplementary variation
# selectors.
HIDDEN_RUNS = [
    (0x00AD, 0x00AD),
    (0x180E, 0x180E),
    (0x200B, 0x200F),
    (0x202A, 0x202E),
    (0x2060, 0x2064),
    (0x2066, 0x2069),
    (0xFE00, 0xFE0F),
    (0xFEFF, 0xFEFF),
    (0xE0000, 0xE007F),
    (0xE0100, 0xE01EF),
]
# Every C0 control but the tab, DEL, and every C1 control.
CONTROLS = [*range(0x00, 0x09), *range(0x0A, 0x20), *range(0x7F, 0xA0)]


def test_escape_sequences_and_forged_lines_are_spelled_out():
    assert printable("\x1b[2Jcleared\rover\nforged") == "\\x1b[2Jcleared\\x0dover\\x0aforged"
    assert printable("\x9b31m") == "\\x9b31m"  # the one-byte C1 escape


def test_hidden_characters_are_named_and_ordinary_text_is_left_alone():
    assert printable("a\u202eb\u200bc\U000e0041") == "a<U+202E>b<U+200B>c<U+E0041>"
    assert printable("Tab\tand café, 5 × 3 — fine.") == "Tab\tand café, 5 × 3 — fine."


@pytest.mark.parametrize(("first", "last"), HIDDEN_RUNS, ids=lambda code: f"U+{code:04X}")
def test_every_hidden_character_is_matched_to_the_end_of_its_run(first, last):
    missed = [f"U+{code:04X}" for code in range(first, last + 1) if not HIDDEN.match(chr(code))]
    assert missed == []
    assert printable(chr(last)) == f"<U+{last:04X}>"


def test_every_control_character_but_the_tab_is_spelled_out():
    shown = {code: printable(chr(code)) for code in CONTROLS}
    assert shown == {code: f"\\x{code:02x}" for code in CONTROLS}
    assert printable("\t ~") == "\t ~"


def test_the_install_hook_holds_the_same_hidden_characters():
    assert skills_hook.HIDDEN.pattern == HIDDEN.pattern
