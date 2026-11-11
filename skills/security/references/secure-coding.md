# Secure coding

Read this for the security of a change as a whole: threat modeling it, signing users in and
keeping their sessions, checking what each user may do, choosing cryptography and random values,
logging security events without secrets, reviewing a change for security, and which editions of
the OWASP Top 10, the ASVS and the CWE Top 25 are current.

Validating input and encoding output belong to the coding skill's planned `input-handling`
module, and each language's dangerous calls to its security module: `python-security`,
`javascript-security`, `web-security`, `csharp-security`, `powershell-security`,
`bash-security` and `c-security`. Which dependencies to trust is `supply-chain-security`,
planned in this skill. Where secrets live and how they reach code is the
project-bootstrap-and-audit standard's dimension 7, *Secrets, security and data classification*.

## Rules

1. **Cite the current editions, with the edition beside each number:** OWASP Top 10:2025 (fact
   `sec-top10`), ASVS 5.0.0 (fact `sec-asvs`), the 2025 CWE Top 25 (fact `sec-cwe-top25`).
2. **Threat-model each change that moves a trust boundary** with four questions (fact
   `sec-four-questions`), answered in the pull request.
3. **Use the platform's authentication, never your own** (fact `sec-premade-auth`).
4. **Hash passwords with Argon2id at OWASP's minimums or above** (fact `sec-pw-hash`), and set
   password rules by NIST SP 800-63B-4 (fact `sec-nist-passwords`).
5. **Offer MFA, and require it for administrators** (fact `sec-mfa`).
6. **Keep sessions on the server,** with a new ID at sign-in and every privilege change, and
   timeouts the server enforces (fact `sec-sessions`).
7. **Check authorization on every request, on the server, deny by default,** for the object
   asked for, not only its type (facts `sec-a01`, `sec-authz`).
8. **Use a vetted library's high-level cryptography; never design or assemble your own**
   (fact `sec-crypto`).
9. **Take every security value from a CSPRNG:** tokens, keys, IVs, session IDs, reset links
   (fact `sec-csprng`).
10. **Log security events, never the secrets in them** (fact `sec-logging`).
11. **Review each change for security by what it touches,** before it merges.

### Threat modeling a change

A change moves a trust boundary when it adds an endpoint, outside input, stored data or a third
party, or changes sign-in, permissions or cryptography.

- **What are we working on?** Who calls it, what it stores, where trusted meets untrusted.
- **What can go wrong?** STRIDE's six categories as prompts at each boundary: spoofing,
  tampering, repudiation, information disclosure, denial of service, elevation of privilege.
- **What are we going to do about it?** For each threat, a control and a test, or an accepted
  risk with who accepted it.
- **Did we do a good enough job?** Review checks that each threat has an answer.

### Authentication, sessions and authorization

- **Sign-in, password reset, MFA and sessions come from the framework or an identity
  provider,** with no default credentials shipped.
- **Passwords:** Argon2id; else scrypt; bcrypt for legacy systems, with its 72-byte input limit
  enforced; PBKDF2 only where FIPS-140 is required. Store the parameters with each hash, and
  re-hash at the user's next sign-in when they rise.
- **Password rules:** at least 15 characters where the password is the only factor, no
  composition rules, no forced periodic change, and a blocklist check that says why a password
  was refused.
- **Sessions:** renew the ID after sign-in and any privilege change, keep it out of URLs, and
  enforce idle and absolute timeouts on the server.
- **Authorization:** one central check. Scope each lookup to what the caller may reach, such as
  the owner's ID in the query, and test that a second user is refused. A URL the server fetches
  for a user is access control too: the 2025 Top 10 puts SSRF in A01 (fact `sec-a01`).

### Cryptography, randomness and secrets

- **A library's high-level API** picks the mode, IV and padding: authenticated encryption such
  as AES-GCM. No MD5 or SHA-1 for security, and no IV reused with a key (fact `sec-a04`).
- **TLS at the platform's defaults.** A hard-coded list of groups or cipher suites keeps out what
  later releases improve: Go's hybrid post-quantum key exchange is on by default only where no
  curve list is set (fact `sec-go-mlkem`).
- **CSPRNG per language:** `secrets` in Python (fact `py-secrets`), `crypto.randomBytes()` in
  Node.js, `RandomNumberGenerator` in .NET, `SecureRandom` in Java, `crypto/rand` in Go. Trust a
  UUID's randomness only where its library documents a CSPRNG.
- **Secrets** reach code as the standard's dimension 7 says, and go no further: not into logs,
  errors or URLs.

### Logging and review

Log sign-in successes and failures, authorization and session failures, and administrators'
actions, and alert on repeated failures. Leave out passwords, session IDs (hash one to tie
events together), access tokens, keys and connection strings. Escaping text for a log is
`input-handling`'s; logging in general is the planned `logging-and-observability` module's.

Review a change by what it touches: a new endpoint, a server-side check and a second-user test;
outside input, `input-handling` and the language's module; sign-in, rules 3 to 6; cryptography,
rules 8 and 9; a dependency, `supply-chain-security`. An operation that fails partway fails
closed, rolling all of it back (fact `sec-a10`).

## Mistakes

- **Citing 2021 numbers,** such as A06 for outdated components or A10 for SSRF. Name the
  category with its edition: A03:2025 Software Supply Chain Failures.
- **Loading any invoice by the ID in the URL** once the user may read invoices. Scope the lookup.
- **Work factors from an old copy of the cheat sheet.** They rise; use fact `sec-pw-hash`.
- **Logging the whole request,** `Authorization` header and cookies included.
- **A threat model written once and never again.** Model each change.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Passwords in plain text or a fast hash | The call that stores a password: none, MD5, SHA-1, SHA-256 | `BLOCKER` | Argon2id, re-hashed at next sign-in |
| Hand-written sign-in, session tokens or reset links | Token and cookie code of its own | `GAP`; `BLOCKER` where a flaw is found | The framework's or an identity provider's |
| A handler with no server-side check, or a lookup by ID not scoped to the caller | Routes against the authorization layer; queries by ID | `BLOCKER` | A central check, deny by default, a second-user test |
| No MFA for administrators | Admin sign-in | `GAP` | Require it (fact `sec-mfa`) |
| Session ID kept across sign-in, or timeouts only in the client | Session setup and expiry | `GAP` | Renew the ID; time out on the server |
| A non-cryptographic generator for security values | `Math.random`, `random.`, `System.Random`, `math/rand` near a token or key | `BLOCKER` | The CSPRNG |
| Hand-assembled or deprecated cryptography | ECB, MD5 or SHA-1 for integrity, a constant IV | `BLOCKER` | The library's authenticated encryption |
| TLS groups or cipher suites hard-coded | `CurvePreferences`, cipher lists | `DRIFT` | The platform's defaults |
| Secrets in logs | Log calls given headers, bodies or tokens | `BLOCKER` | Log without them; rotate what leaked |
| Sign-in and authorization failures not logged | Those two paths | `GAP` | Log them |

## Why

### Threat modeling each change

- **The reason:** the flaws a model finds sit in what a change adds, and a system-wide model goes
  stale with the next change. The 2025 Top 10 asks for threat modeling in refinement.
- **What others do:** STRIDE workshops on a whole system's data flow diagrams, at hours each.
- **What it costs:** minutes per change, and a reviewer who reads the answers.
- **When to choose differently:** a new system, or one handling payments or health data, earns a
  full model first.

### The platform's authentication, and Argon2id

- **The reason:** Authentication Failures stay at A07:2025, with session fixation and
  hard-coded credentials among its causes. A fast hash lets a stolen table be guessed at GPU
  speed; a memory-hard one makes each guess costly.
- **What others do:** NIST asks for a salted, approved one-way function, not a memory-hard one,
  so PBKDF2 meets it; OWASP prefers Argon2id.
- **What it costs:** a provider is a dependency; Argon2id spends memory per sign-in, so
  rate-limit sign-in.
- **When to choose differently:** PBKDF2 where FIPS-140 rules.

### Authorization on every request

- **The reason:** Broken Access Control is A01:2025, and an attacker needs only one missed check
  (fact `sec-authz`).
- **What others do:** role checks per route, which miss another user's object.
- **What it costs:** a check per request, and a policy that names every route.
- **When to choose differently:** public resources are named public, never open by default.

### Vetted cryptography and a CSPRNG

- **The reason:** OWASP's whole advice on custom algorithms is "Don't do this." (fact
  `sec-crypto`), and weak random generators are among A04:2025's most common CWEs. Libraries
  choose modes and IVs, and improve defaults, as Go's TLS did.
- **What it costs:** the library's choices, and keeping up with its releases.
- **When to choose differently:** never for the algorithm. A protocol no library offers needs a
  cryptographer's review.

### Logging without secrets

Without logs and alerts a breach goes unseen; with secrets in them, anyone who reads the logs
holds the keys. A09:2025 names both. The cost is storage, and a review of each log call.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `sec-top10` | The current Top 10 is 2025's | [OWASP](https://owasp.org/www-project-top-ten/) | "The most current released version is the OWASP Top 10 2025" | 2026-11-11 | 2027-02-11 |
| `sec-asvs` | The latest ASVS is 5.0.0 | [OWASP](https://owasp.org/www-project-application-security-verification-standard/) | "Get the latest stable version of the ASVS (5.0.0)" | 2026-11-11 | 2027-02-11 |
| `sec-cwe-top25` | The current CWE Top 25 is 2025's | [MITRE](https://cwe.mitre.org/top25/) | "Welcome to the 2025 Common Weakness Enumeration" | 2026-11-11 | 2027-02-11 |
| `sec-four-questions` | The four questions | [Manifesto](https://www.threatmodelingmanifesto.org/) | "What are we working on?" and "What can go wrong?" and "What are we going to do about it?" and "Did we do a good enough job?" | 2026-11-11 | 2027-05-11 |
| `sec-premade-auth` | Use a premade authentication system | [A07:2025](https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/) | "Ideally, use a premade, well-trusted system to handle authentication, identity, and session management." | 2026-11-11 | 2027-05-11 |
| `sec-pw-hash` | Argon2id: 19 MiB, t=2, p=1; PBKDF2: 600,000 | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) | "Use Argon2id with a minimum configuration of 19 MiB of memory, an iteration count of 2, and 1 degree of parallelism." and "use PBKDF2 with a work factor of 600,000 or more" | 2026-11-11 | 2027-05-11 |
| `sec-nist-passwords` | 15 characters alone; no composition rules or periodic change | [NIST](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/) | "to be a minimum of 15 characters in length" and "Other composition requirements for passwords SHALL NOT be imposed." and "SHALL NOT require subscribers to change passwords periodically" | 2026-11-11 | 2027-05-11 |
| `sec-mfa` | MFA for administrators | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html) | "Require MFA for administrative or other high privileged users." | 2026-11-11 | 2027-05-11 |
| `sec-sessions` | New ID at privilege changes; server-side timeouts | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | "after any privilege level change" and "Session timeout management and expiration must be enforced server-side." | 2026-11-11 | 2027-05-11 |
| `sec-a01` | Deny by default; log failures; SSRF in A01 | [A01:2025](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) | "Except for public resources, deny by default." and "Log access control failures" and "CWE-918 Server-Side Request Forgery (SSRF)" | 2026-11-11 | 2027-05-11 |
| `sec-authz` | Check every request | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | "Validating permissions correctly on just the majority of requests is insufficient." | 2026-11-11 | 2027-05-11 |
| `sec-crypto` | No custom algorithms; authenticated modes | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html) | "Don't do this." and "Where available, authenticated modes should always be used." | 2026-11-11 | 2027-05-11 |
| `sec-a04` | Weak generators; no MD5 or SHA1; no IV reuse | [A04:2025](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/) | "the use of a weak pseudo-random number generator" and "such as MD5, SHA1" and "the IV should never be used twice for a fixed key" | 2026-11-11 | 2027-05-11 |
| `sec-go-mlkem` | Go's hybrid TLS default needs no curve list | [Go 1.24](https://go.dev/doc/go1.24) | "enabled by default when Config.CurvePreferences is nil." | 2026-11-11 | 2027-02-11 |
| `sec-csprng` | A PRNG is never for security | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html) | "they must not be used for anything security critical" | 2026-11-11 | 2027-05-11 |
| `sec-logging` | What to log, and leave out | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | "Authentication successes and failures" and "Access tokens" and "Authentication passwords" | 2026-11-11 | 2027-05-11 |
| `sec-a10` | Fail closed | [A10:2025](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/) | "also known as failing closed" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [OWASP Top 10:2025](https://owasp.org/Top10/2025/) | The edition, six categories | CC BY 3.0: our own words, short quotes with attribution |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | Most rules | CC BY-SA 4.0: brief quotes with attribution, our own words otherwise |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | The version | CC BY-SA 4.0: as above |
| [MITRE CWE Top 25](https://cwe.mitre.org/top25/) | The list | CWE Terms of Use, royalty-free with MITRE's notice: short quotes |
| [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/) | Password rules | NIST publication: our own words, short quotes |
| [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) | The four questions | CC BY 4.0: quoted with attribution |
| [Go 1.24 release notes](https://go.dev/doc/go1.24) | Hybrid key exchange | Not stated on the page: a short quote |
