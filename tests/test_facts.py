import email.message
import subprocess
from datetime import date

import pytest

from skillcheck.cli import main
from skillcheck.core import facts
from skillcheck.core.checks import check_repository

FACTS_MD = "skills/facts-skill/references/facts.md"
HEADER = "| ID | Fact | Source | Quote | Checked | Check by |\n|---|---|---|---|---|---|\n"
FIRST_ROW = 5  # after the title, a blank line, the header and its rule


def row(
    ident: str = "`one`",
    source: str = "[Docs](https://example.com/docs)",
    quote: str = '"a quote"',
    checked: str = "2026-01-01",
    check_by: str = "2026-06-30",
) -> str:
    return f"| {ident} | A fact | {source} | {quote} | {checked} | {check_by} |\n"


def facts_skill(repo, table: str, body: str = "Body.\n"):
    skill_dir = repo.skill("facts-skill", body=body)
    (skill_dir / "references" / "facts.md").write_text(f"# Facts\n\n{table}", encoding="utf-8")
    repo.catalog(repo.plugin("example", "./skills/facts-skill"))
    return skill_dir


def findings(repo) -> list[tuple[str, str, str]]:
    return [(f.path, f.rule, f.message) for f in check_repository(repo.root).findings]


def test_well_formed_facts_pass_and_are_counted(repo):
    table = (
        HEADER
        + row()
        + row("`two-links`", "[A](https://example.com/a), [B](https://example.com/b)")
        + row("`escaped`", quote='"the \\"area: \\" prefix"')
        + row(
            "`tag-sha`",
            "`git ls-remote --tags https://example.com/repo`",
            "`0123abcd refs/tags/v1.0.0`",
        )
        + row("`by-hand`", quote="version 1.2.3, uploaded 2026-01-01")
        + "\nProse between two tables.\n\n"
        + HEADER
        + row("`later`")
    )
    facts_skill(repo, table, body="Named: fact `one`, and facts `two-links` and `later`.\n")
    report = check_repository(repo.root)
    assert report.findings == []
    assert report.facts == 6
    by_id = {fact.id: fact for fact in facts.collect(repo.root)}
    assert list(by_id) == ["one", "two-links", "escaped", "tag-sha", "by-hand", "later"]
    assert by_id["one"] == facts.Fact(
        FACTS_MD, FIRST_ROW, "one", ("https://example.com/docs",), ("a quote",), date(2026, 6, 30)
    )
    assert by_id["two-links"].sources == ("https://example.com/a", "https://example.com/b")
    assert by_id["escaped"].quotes == ('the "area: " prefix',)
    assert by_id["tag-sha"].sources == ("git ls-remote --tags https://example.com/repo",)
    assert by_id["tag-sha"].quotes == ("0123abcd refs/tags/v1.0.0",)
    assert by_id["by-hand"].quotes == ()
    assert by_id["later"].line == 15


@pytest.mark.parametrize(
    ("bad_row", "message"),
    [
        (
            "| `one` | A fact | [Docs](https://example.com) |\n",
            "a fact row has 6 cells, not 3",
        ),
        (row(ident="One"), "the ID is not one lowercase, hyphenated name in backticks"),
        (row(ident="`one_two`"), "the ID is not one lowercase, hyphenated name in backticks"),
        (
            row(source="PyPI"),
            "the source is neither an https link nor `git ls-remote --tags <https URL>`",
        ),
        (
            row(source="[Docs](http://example.com)"),
            "the source is neither an https link nor `git ls-remote --tags <https URL>`",
        ),
        (row(quote=""), "the quote is empty"),
        (row(checked="30/09/2026"), "the dates are not both YYYY-MM-DD"),
        (row(check_by="20261231"), "the dates are not both YYYY-MM-DD"),
        (row(check_by="2026-02-30"), "the dates are not both YYYY-MM-DD"),
        (
            row(checked="2026-06-30", check_by="2026-06-30"),
            "the check-by date is not after the checked date",
        ),
        (
            row(ident="`Bad`", quote=""),
            "the ID is not one lowercase, hyphenated name in backticks; the quote is empty",
        ),
    ],
)
def test_malformed_row_fires_alone(repo, bad_row, message):
    facts_skill(repo, HEADER + bad_row)
    assert findings(repo) == [(FACTS_MD, "facts", f"line {FIRST_ROW}: {message}")]
    assert check_repository(repo.root).facts == 0


def test_an_id_defined_twice_fires(repo):
    facts_skill(repo, HEADER + row() + row(checked="2026-02-01"))
    assert findings(repo) == [
        (FACTS_MD, "facts", f"line {FIRST_ROW + 1}: `one` is already defined above")
    ]


def test_a_table_with_other_columns_fires_and_its_rows_are_skipped(repo):
    facts_skill(repo, "| Name | Value |\n|---|---|\n| `x` | y |\n")
    assert findings(repo) == [
        (
            FACTS_MD,
            "facts",
            "line 3: a table here has the columns Name, Value; a fact table has ID, Fact, "
            "Source, Quote, Checked, Check by",
        )
    ]


def test_a_named_fact_that_is_not_defined_fires(repo):
    skill_dir = facts_skill(repo, HEADER + row(), body="See fact `missing-one`.\n")
    (skill_dir / "references" / "other.md").write_text(
        "Facts `one` and `gone`, and a fact `NOT-AN-ID` in prose.\n", encoding="utf-8"
    )
    # The facts file itself isn't searched: its rows describe facts, they don't name them.
    (skill_dir / "references" / "facts.md").write_text(
        f"# Facts\n\nSee fact `nowhere`.\n\n{HEADER}{row()}", encoding="utf-8"
    )
    assert findings(repo) == [
        (
            "skills/facts-skill/SKILL.md",
            "facts",
            "line 6 names fact `missing-one`, which references/facts.md doesn't define",
        ),
        (
            "skills/facts-skill/references/other.md",
            "facts",
            "line 1 names fact `gone`, which references/facts.md doesn't define",
        ),
    ]


def test_a_named_fact_in_a_skill_with_no_facts_file_fires(repo):
    repo.skill("plain-skill", body="As fact `node20` says.\n")
    repo.catalog(repo.plugin("example", "./skills/plain-skill"))
    assert findings(repo) == [
        (
            "skills/plain-skill/SKILL.md",
            "facts",
            "line 6 names fact `node20`, which references/facts.md doesn't define",
        )
    ]


def test_a_skill_without_its_rationale_fires_alone(repo):
    repo.skill("bare-skill", rationale=False)
    repo.catalog(repo.plugin("example", "./skills/bare-skill"))
    assert findings(repo) == [
        (
            "skills/bare-skill/SKILL.md",
            "rationale",
            "SKILL.md doesn't link references/why.md, which says why the skill advises what it "
            "does, what others do instead, and the trade-offs",
        )
    ]


def test_a_rationale_link_to_a_missing_file_is_a_broken_link(repo):
    repo.skill("bare-skill", body="[Why](references/why.md#the-merge-strategy)\n", rationale=False)
    repo.catalog(repo.plugin("example", "./skills/bare-skill"))
    assert findings(repo) == [
        (
            "skills/bare-skill/SKILL.md",
            "reference",
            "links to references/why.md, which does not exist",
        )
    ]


def fact(ident: str, *sources: str, quotes: tuple[str, ...] = ("a quote",)) -> facts.Fact:
    return facts.Fact(FACTS_MD, 1, ident, sources, quotes, date(2026, 6, 30))


def test_verify_finds_quotes_however_the_page_sets_them():
    pages = {
        "https://example.com/a": "The  “Latest” release is `2.56.0`, as SHOWN here.",
        "https://example.com/b": "append a line that says (cherry picked from commit abc) to it",
    }
    calls = []

    def fetch(source: str) -> str:
        calls.append(source)
        return pages[source]

    checked = [
        fact("typography", "https://example.com/a", quotes=('the "latest" release is 2.56.0',)),
        fact("elided", "https://example.com/b", quotes=("says (cherry picked from commit …)",)),
        fact("same-page", "https://example.com/a", quotes=("as shown here",)),
        fact("by-hand", "https://example.com/unfetched", quotes=()),
    ]
    assert list(facts.verify(checked, fetch)) == []
    assert calls == ["https://example.com/a", "https://example.com/b"]


def test_verify_reports_a_missing_quote_and_an_unreadable_source():
    def fetch(source: str) -> str:
        if source == "https://example.com/down":
            raise OSError("HTTP Error 404: Not Found")
        return "the words that are there"

    checked = [
        fact("gone", "https://example.com/up", quotes=("the words that are there", "and gone")),
        fact("elided-gone", "https://example.com/up", quotes=("the words … never were",)),
        fact("unreadable", "https://example.com/down"),
        fact(
            "one-of-two",
            "https://example.com/down",
            "https://example.com/up",
            quotes=("words that are",),
        ),
    ]
    assert [(f.id, problem) for f, problem in facts.verify(checked, fetch)] == [
        ("gone", 'the quote is no longer at its source: "and gone"'),
        ("elided-gone", 'the quote is no longer at its source: "the words … never were"'),
        ("unreadable", "https://example.com/down could not be read (HTTP Error 404: Not Found)"),
    ]


class FakeResponse:
    def __init__(self, body: bytes, content_type: str) -> None:
        self.body = body
        self.headers = email.message.Message()
        self.headers["Content-Type"] = content_type

    def read(self) -> bytes:
        return self.body

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *exc: object) -> None:
        return None


def test_fetch_reads_a_page_as_its_visible_text(monkeypatch):
    html = (
        "<html><head><style>p { color: red }</style><script>var x = '<p>hidden</p>';</script>"
        "</head><body><h1>Title</h1><p>One <code>paths</code> and <b>more</b>.</p></script>"
        "<li>Item&nbsp;two</li></body></html>"
    )
    seen = {}

    def urlopen(request, timeout):
        seen["agent"], seen["timeout"] = request.get_header("User-agent"), timeout
        return FakeResponse(html.encode("latin-1"), "text/html; charset=latin-1")

    monkeypatch.setattr(facts.urllib.request, "urlopen", urlopen)
    assert facts.fetch_text("https://example.com/page") == (" Title One paths and more. Item two")
    assert seen == {"agent": facts.USER_AGENT, "timeout": facts.TIMEOUT_SECONDS}


def test_fetch_returns_other_content_as_it_came(monkeypatch):
    body = '{"version": "4.6.2", "note": "café"}'
    monkeypatch.setattr(
        facts.urllib.request,
        "urlopen",
        lambda request, timeout: FakeResponse(body.encode(), "application/json"),
    )
    assert facts.fetch_text("https://example.com/api") == body


def test_fetch_runs_ls_remote_for_a_tag_source(monkeypatch):
    runs = []

    def run(args, **kwargs):
        runs.append(args)
        return subprocess.CompletedProcess(args, 0, stdout="0123abcd\trefs/tags/v1.0.0\n")

    monkeypatch.setattr(facts.subprocess, "run", run)
    source = "git ls-remote --tags https://example.com/repo"
    assert facts.fetch_text(source) == "0123abcd\trefs/tags/v1.0.0\n"
    assert runs == [["git", "ls-remote", "--tags", "https://example.com/repo"]]


def test_a_failed_or_slow_ls_remote_is_an_unreadable_source(monkeypatch):
    def failing(args, **kwargs):
        return subprocess.CompletedProcess(args, 128, stdout="", stderr="fatal: not found\n")

    monkeypatch.setattr(facts.subprocess, "run", failing)
    with pytest.raises(OSError, match="git ls-remote exited 128: fatal: not found"):
        facts.fetch_text("git ls-remote --tags https://example.com/repo")

    def slow(args, **kwargs):
        raise subprocess.TimeoutExpired(args, kwargs["timeout"])

    monkeypatch.setattr(facts.subprocess, "run", slow)
    with pytest.raises(OSError, match="git ls-remote took over 30 seconds"):
        facts.fetch_text("git ls-remote --tags https://example.com/repo")


def dated_skill(repo):
    table = HEADER + row("`soon`", check_by="2026-06-30") + row("`later`", check_by="2027-06-30")
    table += row("`broken`", quote="")  # malformed, so neither mode counts it
    facts_skill(repo, table)


def test_due_lists_the_facts_to_check_again_by_a_date(repo, capsys):
    dated_skill(repo)
    assert main([str(repo.root), "--due", "2026-06-30"]) == 1
    assert capsys.readouterr().out == (
        f"{FACTS_MD}:{FIRST_ROW}: due: `soon` was to be checked again by 2026-06-30\n"
        "skillcheck: 2 fact(s), 1 due by 2026-06-30\n"
    )
    assert main([str(repo.root), "--due", "2026-06-29"]) == 0
    assert capsys.readouterr().out == "skillcheck: 2 fact(s), 0 due by 2026-06-29\n"


def test_due_without_a_date_counts_from_today(repo, capsys):
    facts_skill(repo, HEADER + row(checked="2000-01-01", check_by="2000-01-02"))
    assert main([str(repo.root), "--due"]) == 1
    assert capsys.readouterr().out.endswith(f"1 due by {date.today()}\n")


def test_due_refuses_a_date_it_cannot_read(repo, capsys):
    with pytest.raises(SystemExit) as exited:
        main([str(repo.root), "--due", "30/09/2026"])
    assert exited.value.code == 2
    assert "'30/09/2026' is not a YYYY-MM-DD date" in capsys.readouterr().err


def test_verify_prints_each_fact_it_could_not_confirm(repo, capsys, monkeypatch):
    dated_skill(repo)
    monkeypatch.setattr(facts, "fetch_text", lambda source: "nothing like it")
    assert main([str(repo.root), "--verify"]) == 1
    assert capsys.readouterr().out == (
        f'{FACTS_MD}:{FIRST_ROW}: verify: `soon`: the quote is no longer at its source: "a quote"\n'
        f"{FACTS_MD}:{FIRST_ROW + 1}: verify: `later`: the quote is no longer at its source: "
        '"a quote"\n'
        "skillcheck: 2 fact(s), 2 with a quote to look for, 2 not confirmed\n"
    )
    monkeypatch.setattr(facts, "fetch_text", lambda source: "Here is a quote.")
    assert main([str(repo.root), "--verify"]) == 0
    assert capsys.readouterr().out == (
        "skillcheck: 2 fact(s), 2 with a quote to look for, 0 not confirmed\n"
    )
