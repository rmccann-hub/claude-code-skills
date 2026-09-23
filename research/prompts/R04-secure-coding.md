# RESEARCH RUN R04: Secure coding, input handling, threat modelling, authentication and cryptography

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: secure-coding, input-handling, configuration, and the security file of every skill.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R04 · FORM: research-result v1
Save as: R04-RESULT.md
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

- OWASP Top 10:2025 was published in late 2025, replacing the 2021 list. OWASP ASVS 5.0 was released in May 2025. MITRE and CISA published a 2025 CWE Top 25.
- NIST SP 800-63B-4 (Digital Identity Guidelines, revision 4) was finalized in 2025.
- OWASP's Password Storage Cheat Sheet recommends Argon2id first, with stated minimum parameters.
- RFC 9700 (OAuth 2.0 Security Best Current Practice) was published in January 2025. OAuth 2.1 is still an Internet-Draft and requires PKCE for all clients. RFC 8725 is the JWT Best Current Practice.
- NIST published FIPS 203 (ML-KEM), 204 (ML-DSA) and 205 (SLH-DSA) in August 2024 and selected HQC in March 2025. NIST IR 8547 proposes deprecating quantum-vulnerable algorithms by 2030 and disallowing them by 2035. Hybrid X25519MLKEM768 key exchange is on by default in major browsers and in OpenSSL 3.5.
- Under CISA's Secure by Design pledge and CISA/NSA memory-safety guidance, manufacturers were asked for memory-safety roadmaps by 1 January 2026.

## Questions

### Priority

1. OWASP Top 10:2025: the list, what changed from 2021, and the key prevention guidance for each. OWASP ASVS 5.0: its structure and levels. The current CWE Top 25 list.
2. Input handling: the authoritative distinction between validation, sanitization and output encoding; allow-listing; canonicalization. Give the correct technique for each context, citing OWASP cheat sheets:
   - SQL (parameterized queries)
   - HTML (contextual encoding, Trusted Types, the Sanitizer API's status), JavaScript, CSS, URLs
   - shell and process execution
   - file paths (traversal) and file uploads
   - XML (XXE) and deserialization
   - regular expressions (ReDoS)
   - LDAP, templates (SSTI), and logs (log injection)
3. Authentication and sessions:
   - NIST SP 800-63B-4's current rules for passwords: length, composition, rotation, breached-password checks
   - passkeys and WebAuthn Level 3 status; session management; MFA; account recovery
   - OAuth 2.0 and 2.1 best practice (RFC 9700, PKCE, no implicit grant, DPoP or mTLS) and OpenID Connect
   - JWT pitfalls (RFC 8725 and any update)
4. Password storage: current recommended parameters for Argon2id, scrypt, bcrypt and PBKDF2 (OWASP, NIST), peppers, and migrating legacy hashes.
5. Cryptography: current guidance on algorithms and key sizes, TLS 1.3 settings, random numbers and authenticated encryption. Post-quantum migration: FIPS 203/204/205, NIST IR 8547, and hybrid key exchange status in browsers, OpenSSL, Go, Java and .NET. What should application developers do now?

### Standard

6. Threat modelling for developers: STRIDE, the Threat Modeling Manifesto, OWASP's threat modelling cheat sheet, attack trees, abuse cases, lightweight methods for small teams, and tools (OWASP Threat Dragon, Microsoft Threat Modeling Tool).
7. Secrets:
   - storage: vaults, OS keychains, cloud secret managers, and the limits of environment variables
   - rotation, and short-lived credentials (OIDC workload identity)
   - detection: gitleaks, TruffleHog, GitHub secret scanning
   - what to do after a leak
8. Security tooling per language, with current versions and which are free for public repositories:
   - SAST: CodeQL, Semgrep
   - linters' security rules: ruff S or bandit, eslint-plugin-security, Roslyn security analyzers, PSScriptAnalyzer, gosec, cargo-deny and cargo-audit, Brakeman, PHPStan and Psalm taint analysis, SpotBugs with FindSecBugs
   - DAST: OWASP ZAP
   - the dependency audit command for each ecosystem
9. Secure HTTP configuration: security headers (CSP Level 3, HSTS, COOP and COEP, Permissions-Policy), cookies (SameSite, Secure, HttpOnly, partitioned cookies/CHIPS), CORS, rate limiting.
10. Security of AI-generated code: published studies from 2024-2026 on vulnerabilities in AI-generated code, "slopsquatting" (hallucinated package names), and mitigations.
11. Memory safety guidance (CISA/NSA and others) and what it asks of teams using C and C++.
