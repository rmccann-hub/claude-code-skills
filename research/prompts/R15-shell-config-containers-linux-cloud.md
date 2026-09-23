# RESEARCH RUN R15: Shell, configuration formats, containers, Kubernetes, infrastructure as code, Linux, networking and cloud

For the repository rmccann-hub/claude-code-skills · Prompt version 1 · Written 22 September 2026

Paste this whole file into a new chat with Research turned on. Nothing else is needed.

## Who this is for

A public repository that is the reference other code repositories are set up, audited and kept
current against. It holds Agent Skills for Claude Code (Markdown guidance plus small scripts), the
checks that test them, and research like this. Professional developers will judge it, so it must
be current, precise and sourced. Today is 22 September 2026.

This run informs these categories: shell, config-formats, containers, kubernetes, infrastructure-as-code, cloud, linux, networking-security, linux-gaming.

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
RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R15 · FORM: research-result v1
Save as: R15-RESULT.md
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

- Bash 5.3 was released in July 2025. POSIX.1-2024 (Issue 8) added features such as `$'...'` quoting, `set -o pipefail`, `find -print0`, `xargs -0`, `readlink` and `realpath`.
- macOS still ships Bash 3.2 and uses zsh as its default shell.
- ShellCheck 0.11, shfmt 3.x and bats-core 1.x are current.
- YAML 1.2.2 is current; TOML 1.1 was released in 2025; JSON Schema 2020-12 is current.
- Docker Engine 28 or 29 is current; the Compose Specification made the `version` key obsolete and prefers `compose.yaml`; BuildKit is the default builder; Docker made its Hardened Images free in December 2025.
- Debian 13 (trixie) was released in August 2025, Ubuntu 26.04 LTS in April 2026, RHEL 10 in May 2025, and Fedora 44 in 2026.
- Kubernetes ships three minor versions a year (1.34 in August 2025, 1.35 in December 2025, 1.36 in April 2026, 1.37 about August 2026). The ingress-nginx project was retired in March 2026 in favour of the Gateway API.
- OpenTofu is the open-source (MPL) fork of Terraform, which moved to the BSL in 2023.
- Suricata 8 was released in 2025, and CIS Controls v8.1 is current.

## Questions

### Priority

1. Shell: Bash 5.3 changes; POSIX.1-2024 additions (confirm the list); portability between GNU (Linux) and BSD (macOS) tools; the pitfalls of `set -euo pipefail`; current ShellCheck, shfmt and bats-core versions; and when to stop writing shell and use Python or PowerShell.
2. Configuration formats: YAML 1.2.2 pitfalls (the Norway problem, anchors), support for JSON with comments (JSONC) and JSON5, TOML 1.1 changes, schema validation (JSON Schema 2020-12, SchemaStore), linters (yamllint, taplo), and EditorConfig.
3. Containers:
   - current Docker Engine and Compose versions
   - Dockerfile practice from Docker's docs: multi-stage builds, non-root users, pinned digests, .dockerignore, BuildKit secret and cache mounts, `COPY --link`, heredocs
   - base images: official, distroless, Chainguard/Wolfi, Docker Hardened Images, Debian 13 slim, Alpine (current), Ubuntu 26.04
   - scanning (Docker Scout, Trivy, Grype) and signing (cosign); Podman 5's status; rootless mode
4. Linux administration:
   - systemd's current version and practice: units, timers versus cron, hardening options
   - cgroups v2, SELinux and AppArmor, firewalld and nftables (the status of iptables), journald
   - current releases and support dates for Debian, Ubuntu LTS, RHEL and its rebuilds, and Fedora
   - immutable (atomic) distributions: Fedora Atomic, bootc, the status of rpm-ostree, Universal Blue and Bazzite
5. Network security: current guidance on firewall rule design, ICMP filtering (RFC 4890), segmentation and zero trust (NIST SP 800-207), WireGuard, Wi-Fi (WPA3, 6 GHz, 802.11w), DNS (DoH, DoT, DNSSEC; Pi-hole v6), IDS and IPS (Suricata 8, Zeek, Snort 3), and CIS Controls v8.1.

### Standard

6. Kubernetes: supported versions, Pod Security Standards, the Gateway API's status and the ingress-nginx retirement, sidecar containers, security baselines (the CIS Kubernetes Benchmark, the NSA/CISA hardening guide), Helm 4.
7. Infrastructure as code: Terraform (current version, licence), OpenTofu (current version, features), Pulumi, Bicep, AWS CDK; testing and scanning (tflint, checkov, trivy config, terraform test); state security.
8. Cloud baselines, vendor-neutral where possible: the Well-Architected frameworks (AWS, Azure, Google Cloud); identity (workload identity federation, OIDC from GitHub Actions); secrets managers; least privilege; the CIS cloud benchmarks.
9. Linux gaming (a personal category): current Proton and Proton-GE, Steam on Linux, Bazzite (rpm-ostree versus bootc), handheld support, where anti-cheat status is tracked, and ntsync's status in the kernel and Wine.
