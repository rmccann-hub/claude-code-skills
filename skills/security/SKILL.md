---
name: security
description: "Designs and reviews software for security: threat models, authentication and sessions, authorization, cryptography, secrets and security events, against OWASP and CWE. Use when building or reviewing anything that handles users, data or keys."
license: Apache-2.0
metadata:
  reviewed: "2026-11-11"
---

# Security

How to design and review software so that it holds up against someone trying to break it:
modeling threats, authenticating people, checking what each may do, using cryptography
correctly, and recording security events. Each language's dangerous calls are `coding`'s
language security modules, and validating input and encoding output is `coding`'s
`input-handling`; prompt injection and agent permissions are `agent-engineering`'s
`ai-agent-security`. The standard rules on secrets (dimension 7) and dependencies
(dimension 8); this skill cites those. Dependencies and the supply chain are a planned module,
`supply-chain-security`, waiting for research.

## What applies to every module

1. **Use the platform's or a vetted library's security features;** never write your own
   authentication, session handling or cryptography.
2. **Deny by default,** and check authorization on the server, on every request.
3. **Model the threats of a change before building it,** in proportion to what it exposes.
4. **Keep secrets out of code, logs, command lines and errors,** and rotate one that leaked.
5. **Name the standard each rule comes from,** with its edition, so a reviewer can check it.

## Modules

Read the module that fits the request, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources.

| Module | Read it for |
|---|---|
| [`secure-coding`](references/secure-coding.md) | Threat modeling a change, authentication, sessions and passwords, authorization, cryptography and randomness, security logging, and a security review, against the OWASP Top 10, ASVS and the CWE Top 25 |

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
