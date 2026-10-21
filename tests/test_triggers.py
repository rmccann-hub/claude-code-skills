"""Requests reach the right skill and module in Claude Code (triggers.py)."""

import json
import subprocess
from pathlib import Path

from skillcheck import triggers
from skillcheck.cli import main

SKILL_CASES = [
    {"query": "Write a commit message.", "should_trigger": True},
    {"query": "Audit this repository.", "should_trigger": False, "note": "audit"},
]
MODULE_CASES = [
    {"query": "Why is this file ignored?", "should_trigger": True},
    {"query": "Pin our actions | to SHAs.", "should_trigger": False, "note": "actions"},
]


def repository(root: Path) -> Path:
    files = {
        "skills/git-tools/SKILL.md": "---\nname: git-tools\n---\n",
        "skills/git-tools/references/ignore-rules.md": "# Ignore rules\n",
        "skills/notes.md": "not a skill folder\n",
        "skills/empty/README.md": "no SKILL.md\n",
        "tests/fixtures/skills/git-tools.json": json.dumps(SKILL_CASES),
        "tests/fixtures/modules/ignore-rules.json": json.dumps(MODULE_CASES),
    }
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    return root


def stream(*tools: tuple[str, dict], model: str = "test-model") -> str:
    events = [
        {"type": "system", "subtype": "init", "model": model},
        {"type": "user", "message": {"content": []}},
        {
            "type": "assistant",
            "message": {
                "content": [{"type": "text", "text": "Looking."}]
                + [{"type": "tool_use", "name": n, "input": i} for n, i in tools]
            },
        },
    ]
    return "\n".join(json.dumps(e) for e in events) + "\nnot json\n"


def answering(choose):
    """A stand-in for Claude Code that answers each request by `choose(query, cwd)`."""
    calls = []

    def run(command, **options):
        calls.append((command, options))
        query = command[command.index("-p") + 1]
        return subprocess.CompletedProcess(command, 0, stdout=choose(query, options["cwd"]))

    return run, calls


def test_cases_come_from_each_fixture_with_their_home_skill(tmp_path):
    found = triggers.cases(repository(tmp_path))
    assert [(c.kind, c.name, c.skill, c.should) for c in found] == [
        ("skill", "git-tools", "git-tools", True),
        ("skill", "git-tools", "git-tools", False),
        ("module", "ignore-rules", "git-tools", True),
        ("module", "ignore-rules", "git-tools", False),
    ]
    assert [c.name for c in triggers.cases(tmp_path, ["ignore-rules"])] == ["ignore-rules"] * 2


def test_every_case_passes_when_claude_code_reaches_what_it_should(tmp_path, monkeypatch):
    root = repository(tmp_path / "repo")

    installed = []

    def choose(query, cwd):
        installed.append(sorted(p.name for p in (Path(cwd) / ".claude/skills").iterdir()))
        module = f"{cwd}/.claude/skills/git-tools/references/ignore-rules.md"
        if query == "Write a commit message.":
            return stream(("Skill", {"skill": "git-tools"}))
        if query == "Why is this file ignored?":
            return stream(("Skill", {"skill": "git-tools"}), ("Read", {"file_path": module}))
        return stream(("Glob", {"pattern": "*"}))

    run, calls = answering(choose)
    lines, summary, code = triggers.run_all(root, run=run)
    assert (lines, code) == ([], 0)
    assert summary == "skillcheck: 4 trigger request(s) asked, 0 failed, on test-model"
    command, options = calls[0]
    assert command[:3] == list(triggers.CLAUDE)
    assert command[command.index("--permission-mode") + 1] == "dontAsk"
    assert command[command.index("--allowedTools") + 1] == triggers.TOOLS
    assert installed[0] == ["git-tools"]
    assert not Path(options["cwd"]).exists()


def test_each_way_a_case_fails_is_named(tmp_path):
    root = repository(tmp_path / "repo")

    def choose(query, cwd):
        elsewhere = "/home/me/.claude/skills/git-tools/references/ignore-rules.md"
        if query == "Why is this file ignored?":
            return stream(("Read", {"file_path": elsewhere}))
        if query == "Audit this repository.":
            return stream(("Skill", {"skill": "git-tools"}))
        if query == "Pin our actions | to SHAs.":
            module = f"{cwd}/.claude/skills/git-tools/references/ignore-rules.md"
            return stream(("Read", {"file_path": module}))
        return stream(model="")

    run, _ = answering(choose)
    lines, summary, code = triggers.run_all(root, run=run)
    assert lines == [
        "skill git-tools: should reach it: 'Write a commit message.': "
        "didn't reach it; invoked no skill",
        "skill git-tools: near miss for it: 'Audit this repository.': "
        "reached it; invoked git-tools",
        "module ignore-rules: should reach it: 'Why is this file ignored?': "
        "read another copy: /home/me/.claude/skills/git-tools/references/ignore-rules.md",
        "module ignore-rules: near miss for it: 'Pin our actions | to SHAs.': "
        "reached it; invoked no skill",
    ]
    assert summary.endswith("4 failed, on an unnamed model, test-model")
    assert code == 1


def test_claude_code_failing_to_run_fails_the_case(tmp_path):
    root = repository(tmp_path / "repo")

    def run(command, **_):
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="Not logged in\nmore")

    lines, _, code = triggers.run_all(root, ["git-tools"], run=run)
    assert lines[0].endswith("Claude Code failed: Not logged in")
    assert code == 1
    silent = triggers.ask("q", tmp_path, lambda c, **_: subprocess.CompletedProcess(c, 2, "", ""))
    assert silent.error == "exit 2"


def test_no_case_found_fails_rather_than_passing(tmp_path):
    lines, summary, code = triggers.run_all(repository(tmp_path), ["no-such-module"])
    assert (lines, code) == ([], 1)
    assert summary == "skillcheck: 0 trigger request(s) asked, 0 failed"


def test_the_claude_ai_list_has_one_request_and_one_near_miss_each(tmp_path):
    text = triggers.tries(repository(tmp_path))
    assert text.splitlines()[6:] == [
        "| skill `git-tools` | Write a commit message. | the `git-tools` skill loads |",
        "| skill `git-tools` | Audit this repository. | `git-tools` doesn't load; "
        "it's for `audit` |",
        "| module `ignore-rules` | Why is this file ignored? | `git-tools` loads and reads "
        "`references/ignore-rules.md` |",
        "| module `ignore-rules` | Pin our actions \\| to SHAs. | "
        "`references/ignore-rules.md` isn't read; it's for `actions` |",
    ]
    only_misses = tmp_path / "tests/fixtures/skills/git-tools.json"
    only_misses.write_text(json.dumps(SKILL_CASES[1:]), encoding="utf-8")
    assert "the `git-tools` skill loads" not in triggers.tries(tmp_path, ["git-tools"])


def test_the_commands_print_and_exit_by_what_they_found(tmp_path, capsys, monkeypatch):
    root = repository(tmp_path)
    monkeypatch.setattr(triggers, "run_all", lambda r, names: (["a failure"], "the summary", 1))
    assert main([str(root), "--triggers", "git-tools"]) == 1
    assert capsys.readouterr().out == "a failure\nthe summary\n"
    assert main([str(root), "--tries"]) == 0
    assert capsys.readouterr().out.startswith("# Requests to try on claude.ai")
