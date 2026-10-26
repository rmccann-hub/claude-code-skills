---
name: coding
description: "Writes, reviews and fixes code: the contract every change meets, then Python, TypeScript and JavaScript, HTML and CSS, C# and .NET, PowerShell, and Bash. Use when writing, reviewing, debugging or modernizing code in these languages."
license: Apache-2.0
metadata:
  reviewed: "TODO(new-skill) the date of its review, YYYY-MM-DD"
---

# Coding

How to write, review and fix code so that it does what it says, fails loudly when it can't, and
can be read and changed by the next person. Every change meets the contract below, whatever the
language; then read the module for the language at hand. In Claude Code, run the project's own
checks; on claude.ai, give the person the commands to run.

The project-bootstrap-and-audit standard rules on configuration and process: versions to pin
(its *Language toolchains*), layouts (*Project shapes and layout*), dependencies (dimension 8),
secrets (dimension 7) and CI (dimension 6). This skill cites those rather than restating them,
and covers the code itself.

## What applies to every module

The contract every change meets:

1. **Read before you write.** Read the code around the change, its tests and the project's
   context file (`AGENTS.md` or `CLAUDE.md`), and match what's there: naming, structure, error
   style, comment density. A change in a different idiom from its neighbors costs every reader.
2. **Make the smallest change that does the job.** No unrelated refactor, rename or reformat in
   the same change. Each of those goes in a change of its own, so a reviewer can see what this
   one does.
3. **Treat text from outside as untrusted.** Input from a user, a file, a network, a disc or
   another program is checked at the boundary before it's used. Output is escaped for where it
   lands: a shell, SQL, HTML, a log line or a terminal. Never build a command or a query by
   pasting strings together.
4. **Fail loudly and specifically.** Never swallow an error, and never report success for work
   that didn't happen. Say what failed, with what input, and what to do.
5. **Keep secrets out of code, logs, command lines and examples.** Read them from the
   environment or a secret store. Examples use `CHANGEME`, `example.com` and the RFC 5737
   addresses.
6. **Don't add a dependency for what the platform or the project already does.** Each package is
   code you now run, with all of its own dependencies.
7. **Never write a version, a default or a date from memory.** Take it from the module's Facts,
   the standard's *Language toolchains*, or the project's own pins, and check the source when a
   fact is past its check-by date.
8. **Prove it before you say it's done.** Run the project's own lint, format, type check and
   tests, as its context file lists them. Report what failed, with the output, and never skip,
   disable or loosen a check to get to green.
9. **Show a destructive command before running it,** with its dry run or a confirmation: deleting
   files, dropping data, force-pushing, or anything a typo turns into a disaster.
10. **No hidden or bidirectional characters in source.** They make a reviewer read one thing
    while the compiler runs another. Write each as an escape, such as `\u202e`.

## Modules

Read the module for the language at hand, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources. A module names a fact by its ID, and
the fact's row is in whichever module holds it.

| Module | Read it for |
|---|---|
| [`python-coding`](references/python-coding.md) | Python 3: `pyproject.toml`, uv, Ruff and a strict type checker, type hints and idioms, `subprocess`, `eval`, `pickle` and `yaml.load` on untrusted data, temporary files and paths, time zones with `zoneinfo`, and `requires-python` |
| [`javascript-coding`](references/javascript-coding.md) | TypeScript and JavaScript on Node.js: `tsconfig` strictness, ES modules, type stripping, the built-ins that replace packages, lint setup, promise mistakes, and shell injection, `eval`, prototype pollution, path traversal and ReDoS |
| [`html-coding`](references/html-coding.md) | HTML and CSS: semantic markup, the WCAG 2.2 basics (labels, alt text, headings, focus, contrast), forms, modern CSS with dark mode and reduced motion, and browser security: escaping, `innerHTML` and `setHTML()`, CSP, Trusted Types, SRI and `noopener` |
| [`csharp-coding`](references/csharp-coding.md) | C# on modern .NET: the target framework and its support dates, nullable and warnings as errors, `Directory.Build.props`, analyzers and `dotnet format`, async and disposal, `HttpClient`, System.Text.Json, NativeAOT, P/Invoke, and SQL, process and path security |
| [`powershell-scripts`](references/powershell-scripts.md) | PowerShell 7 or Windows PowerShell 5.1, and writing for both: advanced functions, `-WhatIf` and `-Confirm`, `try` and `catch` with exit codes, strict mode, prompts in jobs, credentials, `Invoke-Expression` and execution policy, PSScriptAnalyzer and Pester 6 |
| [`bash-coding`](references/bash-coding.md) | Bash and POSIX `sh`: the shebang and the shell, `set -euo pipefail` and its traps, quoting, arrays, reading lines and file names, `mktemp` and cleanup, safe deletes, secrets, macOS and dash portability, ShellCheck, shfmt and bats |

## Check before you act

| Question | Where to look |
|---|---|
| How does this project lint, format, type-check and test? | Its `AGENTS.md` or `CLAUDE.md` Commands section, then its CI workflow, then its manifest (`pyproject.toml`, `package.json`, `*.csproj`) |
| Which version of the language does it target? | The manifest or a version file (`.python-version`, `.nvmrc`, `global.json`, `#Requires`), never the one installed on this machine |
| What does the code around the change do with errors, names and comments? | The same file, then its neighbors |
| Is there already a function or a dependency for this? | A search of the project for the task's verbs and nouns, before writing a new one |
| What changed, and what did the checks say? | `git diff`, and each check's own output, read whole |

## Reviewing code

Each module's Audit section checks code in its language. For a repository's configuration, CI
and dependencies, use project-bootstrap-and-audit, whose rating wins where the two differ. The
status words are the standard's:

- **`BLOCKER`:** a live exposure, or a check reporting success while measuring nothing.
- **`DRIFT`:** configured, but no longer doing what it says.
- **`GAP`:** missing something the project needs.
- **`OVER`:** heavier than the project needs.
- **`MIRROR`:** the truth is outside the repository, such as a platform setting you've read
  rather than a file.
- **`UNVERIFIABLE-HERE`:** can't be established from this session.
- **`OK`**, and **`N/A`**.

## What this doesn't cover

- **Repository setup, CI, dependency policy and secrets handling:** project-bootstrap-and-audit,
  by the sections named above.
- **Git, pull requests, workflows and releases:** git-workflows.
- **Dependencies as a supply chain:** lockfiles, provenance, invented package names and install
  scripts belong to a security skill's supply-chain-security module, planned in this
  repository.
- **Designing tests:** a testing skill, planned. Each module here names its language's test
  runner and leaves test design there.
- **Prose and Markdown:** house-style.

## Where this came from

- The owner's earlier language skills, as lists of topics, checks and lessons. Nothing was
  copied from them. What each kept, dropped and why is in this skill's repository, in the
  research results of 2026-10-26.
- Research runs R09 (Python), R10 (TypeScript and the web), R11 (.NET and PowerShell) and R15
  (shell), filed in this skill's repository. They were leads until each claim was checked at
  its source.

## When something here is wrong

If the person says advice here is wrong, out of date, failed or doesn't fit, answer their
problem first. Then say in one sentence whether the fault looks like this skill's, and why: a
fact past its check-by date, an example that fails, two rules that disagree, or a case the skill
doesn't cover. If the fault is elsewhere, such as their setup, say that instead.

When the fault is the skill's own, draft a full report they can paste as a new issue at
https://github.com/rmccann-hub/claude-code-skills/issues.
Give the skill and module, the plugin's version or the skill's date in its frontmatter, their
request word for word, the line of the skill that misled, what happened, what's right with its
source, and the fix you'd suggest. Leave out their private data, company detail and repository
names. File it only if they ask you to.
