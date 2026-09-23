# RESEARCH RUN R14: Data and SQL

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: data-and-sql, epicor-kinetic (SQL Server), excel (data connections).

## Rules

1. **Primary sources first:** official documentation, specifications and standards bodies, and
   each project's own release notes, changelogs and security advisories. Use secondary sources
   (respected books, well-known engineering blogs, surveys) only where no primary source covers
   the point, and label them "secondary".
2. **Cite every fact:** the URL, the exact sentence you relied on in quotation marks, and a date
   (the source's own date, otherwise the date you read it).
3. **Never guess.** Write "not found" when you can't source something. Write "contested" when good
   sources disagree, and give each side with its source.
4. **Versions:** for every product, give
   - the current stable version and its release date;
   - its end-of-support date;
   - any release due within 6 months, with the expected date and its source.

   Flag anything that reaches end of support within 12 months.
5. **"What we believe" is my current understanding and may be wrong or out of date.** Confirm or
   correct every item, each with a source. The corrections are the most valuable part of this run.
6. **Licences:** for each source, name its licence and say what an Apache-2.0 repository may do
   with it: quote briefly, paraphrase, or adapt its code examples, and with what attribution.
7. **Depth over breadth.** Finish the Priority questions fully. If you run out of room, list the
   rest under "Not covered".

## Output

Write one Markdown report. Its first three lines must be exactly:

```text
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R14 · FORM: research-result v1
Save as: R14-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.
```

Then these sections, in this order:

1. **Summary:** at most 15 bullets a professional must know today.
2. **Corrections:** every "What we believe" item that was wrong or out of date, with the right
   fact and its source.
3. **Facts table:** `| # | Fact | Value | Source URL | Exact quote | Date |`
4. **Findings:** one section per question below, numbered to match.
5. **Tools:** `| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |`
6. **Changing in the next 12 months:** deprecations, end-of-support dates, announced breaking
   changes.
7. **Common mistakes,** including those AI coding assistants make in this area, with sources.
8. **Sources and licences:** `| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |`
9. **Not found, contested, not covered.**

## What we believe (confirm or correct each)

- SQL Server 2025 became generally available in late 2025, with a native vector type, a native JSON type, regular expression functions and optimized locking.
- SQL Server 2016 reached end of extended support in July 2026; SQL Server 2017 ends in October 2027.
- SQL Server 2022 added IS [NOT] DISTINCT FROM, GREATEST and LEAST, DATE_BUCKET, the WINDOW clause, DATETRUNC and GENERATE_SERIES.
- Microsoft ODBC Driver 18 encrypts connections by default, and Microsoft.Data.SqlClient replaces System.Data.SqlClient.
- PostgreSQL 18 was released in September 2025 (asynchronous I/O, uuidv7(), virtual generated columns, OAuth authentication); PostgreSQL 19 is due around September 2026; PostgreSQL 13 reached end of life in November 2025.
- SQLFluff is the common SQL linter; Flyway, Liquibase, Alembic and EF Core migrations are common migration tools.

## Questions

### Priority

1. SQL Server:
   - supported versions and end dates, and SQL Server 2025's features (confirm the list)
   - T-SQL features modern code should use, with the version each needs: STRING_AGG, TRIM, CONCAT_WS, the JSON functions, IS DISTINCT FROM, GREATEST and LEAST, DATE_BUCKET, WINDOW, GENERATE_SERIES, the regex functions
   - deprecated features to avoid: text, ntext and image; old outer-join syntax; SET ROWCOUNT for DML; deprecated system tables
   - window frame rules: is RANGE with offsets supported?
2. Connecting safely:
   - current versions and encryption defaults of ODBC Driver 18 and Microsoft.Data.SqlClient
   - parameterized queries in each language: Python (pyodbc, and Microsoft's newer driver), .NET, PowerShell (Invoke-Sqlcmd and the SqlServer module's current version), Node (mssql, tedious)
   - SQL injection prevention, least-privilege logins, Always Encrypted's status
3. Query performance: sargability; indexing strategy (covering, filtered, columnstore); statistics; parameter sniffing and Parameter Sensitive Plan optimization; Query Store; reading execution plans; intelligent query processing features by version.
4. PostgreSQL: supported versions, the features of 18 and 19, recommended practice (uuidv7, identity columns, JSONB, indexing), and tools (psql, pgAdmin, pg_stat_statements).
5. SQL style and linting: authoritative style guides (for example sqlstyle.guide, GitLab's SQL style guide, Mozilla's), SQLFluff's current version and T-SQL support, and formatting conventions (keyword case, leading commas, CTE use).

### Standard

6. Migrations and schema change: Flyway, Liquibase, Alembic, EF Core migrations, DbUp, sqitch, and SSDT/SqlPackage (SDK-style sqlproj), with current versions; practice for idempotent, reversible, zero-downtime changes.
7. Transactions and concurrency: isolation levels, RCSI, deadlocks, optimistic concurrency, SERIALIZABLE versus snapshot, and optimized locking in SQL Server 2025.
8. Data formats and tooling:
   - SQLite (current version, when to use it) and DuckDB (current)
   - Parquet and Arrow
   - CSV pitfalls: RFC 4180, encodings, Excel
   - JSON Schema 2020-12; data validation (Pydantic, Great Expectations, Pandera)
9. ORMs: EF Core 10, SQLAlchemy 2.x, Prisma, Drizzle and Dapper, with current versions, and guidance on raw SQL versus an ORM.
10. SQL mistakes AI assistants make (for example non-sargable predicates, wrong window frames, a missing tenant or company filter in multi-tenant schemas), with sources.
