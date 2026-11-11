---
name: architecture
description: "Lays out and structures software projects: where each file and folder goes, layouts by ecosystem, naming, tests' places, monorepo or several repositories, and moving files safely. Use when starting, reorganizing or splitting a codebase."
license: Apache-2.0
metadata:
  reviewed: "2026-11-11"
---

# Architecture

How a codebase is arranged so the next person can find things and change them: its layout,
where each kind of file goes, and when to split or merge repositories. The standard rules on a
repository's root files and layouts by project shape (*Project shapes and layout*); this skill
cites it and covers the choices it leaves. API design, legacy modernization and design
principles are planned modules (`api-patterns`, `legacy-modernization`,
`architecture-and-design`), waiting for research.

## What applies to every module

1. **Follow the ecosystem's own layout first,** and the standard's for the project's shape;
   invent structure only where neither decides.
2. **Name things for what they are,** in the ecosystem's case convention, and keep names
   stable once others depend on them.
3. **Move files in a commit of their own,** with `git mv`, so history follows them.

## Modules

Read the module that fits the request, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources.

| Module | Read it for |
|---|---|
| [`repo-structure`](references/repo-structure.md) | Layouts by project type and ecosystem, where tests and each kind of file go, feature or layer folders, naming files and folders, monorepo or several repositories, and moving files without losing history |

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
