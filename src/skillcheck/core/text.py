"""Characters that show one thing and do another, and text from outside made safe to print."""

import re

# Characters that render as nothing or reorder the text around them, so what a reviewer sees
# differs from what an agent reads: zero-width characters and joiners, bidirectional controls
# (the Trojan Source attack, CVE-2021-42574), the byte-order mark, the soft hyphen, and Unicode
# tag characters, which can carry a whole hidden instruction. `skills_hook.py` holds a copy,
# since it runs without this package, and a test keeps the two the same.
HIDDEN = re.compile(
    "[\u00ad\u180e\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\U000e0000-\U000e007f]"
)
# Control characters a terminal, a log viewer or an issue acts on rather than shows: escape
# sequences, carriage returns that overwrite a line, and newlines that forge one. A tab is shown.
CONTROL = re.compile("[\x00-\x08\x0a-\x1f\x7f-\x9f]")


def printable(text: str) -> str:
    """Text from outside the repository, with its control and hidden characters spelled out.

    A server's error, a model's file path and an archive's entry name can each carry them, and
    each is printed, posted as an issue or read by an agent.
    """
    text = HIDDEN.sub(lambda m: f"<U+{ord(m.group()):04X}>", text)
    return CONTROL.sub(lambda m: f"\\x{ord(m.group()):02x}", text)
