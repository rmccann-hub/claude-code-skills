# Verification: R15 (2026-10-26)

Checked by the receiving session on 2026-10-26. Nothing in this report changes a file yet, so
no claim was checked. Each is a lead until `bash-coding` or an `operations` module relies on it.

| Claim | Status | Checked against |
|---|---|---|
| Everything in the report | not yet checked | checked when the modules that rely on it are built (`research/README.md`) |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R15 · FORM: research-result v1
Save as: R15-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R15: Shell, configuration formats, containers, Kubernetes, IaC, Linux, networking and cloud — research result (26 October 2026)

Most of the "What we believe" items are right in substance, but several are out of date as of 26 October 2026: Docker Engine 29 is the only current line (not "28 or 29"), Podman 6 replaced Podman 5 in June 2026, Kubernetes 1.34 reaches end of life tomorrow (27 October 2026), Fedora 45 is due this week, OpenTofu is on 1.13 and Terraform on 1.16, and the POSIX.1-2024 list needs `timeout` added and `find -print0`/`xargs -0` re-sourced. The search budget for this run ran out before Questions 2 (beyond TOML), 3 (Dockerfile practice and base images), 8, 9 and most of 10 could be sourced; those are listed under "Not found, contested, not covered" rather than guessed.

## 1. Summary

- **Kubernetes 1.34 reaches upstream end of life on 27 October 2026 (tomorrow).** kubernetes.io's patch-release page says "The End of Life date for Kubernetes 1.34 is Oct 27, 2026."\[1\] Supported upstream minors after that are 1.35, 1.36 and 1.37.\[2\]
- **Docker Engine 29 is the current line**; Docker's release notes page (updated 20 October 2026) lists 29.9.0 at the top.\[3\] Engine 29.0.0 made the containerd image store the default for fresh installs, removed Docker Content Trust from the CLI, and added experimental nftables support.\[4\]\[5\]\[6\]
- **Podman 6.0.0 was released on 24 June 2026** and removes cgroups v1, slirp4netns, CNI, iptables support and the BoltDB backend. Treat any guidance written for Podman 5 as needing review.
- **ingress-nginx is retired (March 2026)**; existing deployments keep running but get no fixes. The Ingress API itself is not retired.\[7\]\[8\] Gateway API v1.5 (27 February 2026) moved ListenerSet, TLSRoute, CORS and client-certificate validation to Standard.\[9\]
- **Helm 4.0.0 shipped on 12 November 2025.** Helm 3 bug fixes ended with the final feature release on 9 September 2026 and Helm 3 security fixes end on 10 February 2027 — inside the 12-month window.\[10\]\[11\]
- **Bash 5.3 was announced on 5 July 2025**, adding in-process command substitution `${ cmd; }` and `${| cmd; }`, `GLOBSORT`, `source -p`, `read -E`, and a `printf %q` alternate form that forces single quoting.\[12\]\[13\]\[14\]
- **POSIX.1-2024 (Issue 8) confirms** `$'...'` dollar-single-quotes, `set -o pipefail`, and the new utilities `readlink`, `realpath` and `timeout` (plus `gettext`, `msgfmt`, `ngettext`, `xgettext`).\[15\]\[16\] dash only supports `pipefail` from version 5.13.\[17\]
- **ShellCheck v0.11.0 (3 August 2025) is still the latest release**, and it removed SC3013 because `-ot`/`-nt`/`-ef` are now in POSIX.1-2024.\[18\]\[19\]
- **TOML 1.1.0 is real and recent** (changelog dated 18 December 2025): multi-line inline tables with trailing commas, `\e` and `\xHH` escapes, and optional seconds in times.\[20\]\[21\] Parsers must opt in; do not assume TOML 1.1 support.
- **OpenTofu 1.13.0 shipped on 30 September 2026** (1.13.1 on 1 October); it removes WinRM provisioners and is the last series with 32-bit builds.\[22\]\[23\]\[24\] Terraform's current line is 1.16 (1.16.0 on 26 August 2026, 1.16.6 on 14 October 2026), still under the Business Source License.\[25\]\[26\]\[27\]
- **Distribution status:** Debian 13 "trixie" point release 13.7 (12 September 2026); Ubuntu 26.04 LTS shipped 23 April 2026; RHEL 10.2 went GA on 19 May 2026; Fedora 45 slipped from 20 October to a 27 October target, and Fedora 43 reaches end of life on 9 December 2026 per endoflife.date (versio.io says 28 November 2026).
- **Suricata 7 is end of life** (7.0.17 in July 2026 was the last); Suricata 8.0.7 (15 September 2026) is current. Snort 2 is formally end of life; Snort 3.12.4.0 is current.\[28\]\[29\]\[30\]
- **Zeek 9.0.0 is the current LTS (14 September 2026)**, Pi-hole is at FTL v6.8 / Web v6.6.1 / Core v6.5\[31\] (17 October 2026), and CIS Controls v8.1 remains the current version, with v9 only "being worked on".\[31\]\[32\]\[33\]\[34\]
- **Docker Hardened Images became free and Apache-2.0 licensed in December 2025** (announced 17 December 2025), confirming the belief.\[35\]\[36\]
- **systemd 260 (released 17 March 2026) removed support for SysV service scripts**: its GitHub release page says "Support for System V service scripts has been removed." systemd 262 is reported as the latest stable (secondary).\[37\] Native unit files are now mandatory.

## 2. Corrections

| # | What we believed | Status | Correct fact | Source |
|---|---|---|---|---|
| C1 | "Docker Engine 28 or 29 is current" | **Out of date** | Only Engine 29 is current; the release notes page lists 29.9.0 as the newest entry (page updated 2026-10-20).\[3\] Engine 28 is superseded. | https://docs.docker.com/engine/release-notes/29/ |
| C2 | "Podman 5's status" (implying Podman 5 is current) | **Out of date** | Podman 6.0.0 was released on 24 June 2026 and removes slirp4netns, cgroups v1 and the BoltDB backend.\[38\]\[39\] | https://lwn.net/Articles/1079600/ ; https://fedoraproject.org/wiki/Changes/Podman6 |
| C3 | POSIX.1-2024 added `$'...'`, `set -o pipefail`, `find -print0`, `xargs -0`, `readlink`, `realpath` | **Partly confirmed, incomplete** | Confirmed from the standard: `$'...'` (section 2.2.4), `-o pipefail` (Austin Group Defect 789), `readlink`, `realpath`. The list omits `timeout`, `gettext`, `msgfmt`, `ngettext` and `xgettext`, which are also new.\[15\]\[16\] `find -print0` appears only in a secondary source;\[40\] `xargs -0` was not verified in this run. | https://pubs.opengroup.org/onlinepubs/9799919799/xrat/V4_xcu_chap01.html ; https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html ; https://sortix.org/blog/posix-2024/ (secondary) |
| C4 | "Kubernetes … 1.37 about August 2026" | **Confirmed, now past** | 1.37 shipped upstream in August 2026; 1.34 enters end of life on 27 October 2026.\[1\]\[41\] | https://kubernetes.io/releases/patch-releases/ ; https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions |
| C5 | "ingress-nginx … retired in March 2026 in favour of the Gateway API" | **Partly wrong** | Retirement in March 2026 is correct. But the project recommends migrating to Gateway API *or another Ingress controller*, and the Ingress API is not retired.\[7\]\[42\] | https://kubeace.com/blog/nginx-ingress-retirement-2026/ (secondary, quoting the official announcement) ; https://www.herodevs.com/blog-posts/ingress-nginx-end-of-life-2026-migration-and-support (secondary) |
| C6 | "Fedora 44 in 2026" | **Confirmed, but incomplete** | Fedora 44 shipped on 28 April 2026 (secondary). Fedora 45 is now due: the 20 October target slipped to 27 October 2026.\[43\]\[44\] | https://linuxiac.com/fedora-linux-45-delayed-new-release-date-set-for-october-27/ (secondary) |
| C7 | "RHEL 10 in May 2025" | **Confirmed, incomplete** | RHEL 10 shipped in May 2025, and the current minor release is RHEL 10.2, GA on 2026-05-19.\[45\]\[46\] | https://access.redhat.com/articles/red-hat-enterprise-linux-release-dates |
| C8 | "TOML 1.1 was released in 2025" | **Confirmed, with a date conflict** | The changelog dates 1.1.0 to 2025-12-18; the GitHub release object is dated 24 December.\[20\]\[21\] | https://github.com/toml-lang/toml/blob/main/CHANGELOG.md ; https://github.com/toml-lang/toml/releases/tag/1.1.0 |
| C9 | "Bash 5.3 was released in July 2025" | **Confirmed** | The release announcement is dated Sat, 05 Jul 2025.\[12\] | https://www.mail-archive.com/bug-bash@gnu.org/msg34422.html |
| C10 | "ShellCheck 0.11 … current" | **Confirmed** | v0.11.0, dated 2025-08-03, is still the latest release.\[18\] | https://github.com/koalaman/shellcheck/releases |
| C11 | "Docker made its Hardened Images free in December 2025" | **Confirmed** | Free and Apache-2.0 licensed, announced 17 December 2025.\[35\]\[47\] | https://www.docker.com/products/hardened-images/ ; https://www.techtarget.com/searchitoperations/news/366636656/Free-Docker-Hardened-Images-challenge-Chainguard (secondary) |
| C12 | "Debian 13 (trixie) was released in August 2025" | **Confirmed** | Released 9 August 2025 (secondary); the current point release is 13.7, from 12 September 2026.\[48\]\[49\] | https://www.debian.org/News/2026/20260912 |
| C13 | "Ubuntu 26.04 LTS in April 2026" | **Confirmed** | Released 23 April 2026.\[50\] | https://canonical.com/blog/canonical-releases-ubuntu-26-04-lts-resolute-raccoon |
| C14 | "OpenTofu is the open-source (MPL) fork of Terraform, which moved to the BSL in 2023" | **Confirmed** | OpenTofu is MPL 2.0; Terraform is under Business Source License v1.1, relicensed in August 2023 (both from secondary sources).\[27\]\[51\] | https://en.wikipedia.org/wiki/OpenTofu (secondary) ; https://en.wikipedia.org/wiki/Terraform_(software) (secondary) |
| C15 | "Suricata 8 was released in 2025" | **Confirmed** | Suricata 8.0.0 was released on 8 July 2025. Suricata 7 is now end of life.\[29\]\[52\] | https://suricata.io/2025/07/08/suricata-8-0-0-released/ ; https://suricata.io/2026/07/09/suricata-8-0-6-and-7-0-17-released/ |
| C16 | "CIS Controls v8.1 is current" | **Confirmed** | v8.1 is still current; CIS says it is "already working on ideas for Version 9".\[32\]\[33\] | https://www.cisecurity.org/controls ; https://www.cisecurity.org/insights/blog/ongoing-evolution-cis-critical-security-controls |
| C17 | "Kubernetes ships three minor versions a year" | **Confirmed** (dates 1.34 Aug 2025, 1.35 Dec 2025, 1.36 Apr 2026, 1.37 Aug 2026) | Matches the upstream column of the AKS calendar.\[41\] | https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions |
| C18 | macOS ships Bash 3.2 and defaults to zsh; shfmt 3.x and bats-core 1.x are current; YAML 1.2.2 and JSON Schema 2020-12 are current; the Compose `version` key is obsolete; BuildKit is the default builder | **Not verified in this run** | See section 9. | — |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| 1 | Bash 5.3 release | Announced 5 Jul 2025\[12\] | https://www.mail-archive.com/bug-bash@gnu.org/msg34422.html | "The first public release of bash-5.3 is now available"\[12\] | 2025-07-05 |
| 2 | Bash 5.3 in-process command substitution | `${ command; }` / `${\|command;}` | same | "New form of command substitution: ${ command; } or ${\|command;} to capture the output of COMMAND without forking a child process and using pipes." | 2025-07-05 |
| 3 | Bash 5.3 `printf %q` | Alternate form forces single quotes | same | "`printf' uses the `alternate form' for %q and %Q to force single quoting." | 2025-07-05 |
| 4 | Bash 5.3 incompatibility | `test` parsing and job notifications | same | "There are a few incompatible changes between bash-5.2 and bash-5.3." | 2025-07-05 |
| 5 | Bash 5.3 build | C23; no K&R compilers\[13\]\[14\] | same | "The source code has been updated for C23 conformance. This means that bash will no longer compile with K&R-style C compilers."\[12\] | 2025-07-05 |
| 6 | POSIX.1-2024 new utilities | gettext, msgfmt, ngettext, readlink, realpath, timeout, xgettext | https://pubs.opengroup.org/onlinepubs/9799919799/xrat/V4_xcu_chap01.html | "The utilities first introduced in Issue 8 (over the Issue 7 base document) are as follows"\[16\] | read 2026-10-26 |
| 7 | POSIX.1-2024 pipefail | Added | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | "Austin Group Defect 789 is applied, adding -o pipefail."\[15\] | read 2026-10-26 |
| 8 | POSIX.1-2024 `$'...'` | Added (incl. `\e`, `\xXX`) | same | "A sequence of characters starting with a <dollar-sign> immediately followed by a single-quote ($') shall preserve the literal value of all characters up to an unescaped terminating single-quote" | read 2026-10-26 |
| 9 | dash pipefail | From dash 5.13 | https://www.shellcheck.net/wiki/SC3040 | "dash version 5.13 included pipefail along with other POSIX.1-2024 features."\[17\] | read 2026-10-26 |
| 10 | ShellCheck latest | v0.11.0 | https://github.com/koalaman/shellcheck/releases | "v0.11.0 - 2025-08-03" | 2025-08-03 |
| 11 | ShellCheck SC3013 removed | POSIX.1-2024 alignment\[19\] | https://newreleases.io/project/github/koalaman/shellcheck/release/v0.11.0 (secondary mirror of release notes) | "SC3013: removed since the operators -ot/-nt/-ef are specified in POSIX.1-2024" | 2025-08-03 |
| 12 | TOML 1.1.0 | 2025-12-18 | https://github.com/toml-lang/toml/blob/main/CHANGELOG.md | "1.1.0 / 2025-12-18" | 2025-12-18 |
| 13 | TOML 1.1 inline tables | Newlines and trailing commas\[20\] | https://github.com/toml-lang/toml/releases/tag/1.1.0 | "Allow newlines and trailing commas in inline tables (#904)." | 2025-12-24 |
| 14 | Docker Engine current line | 29 (29.9.0 top entry)\[3\] | https://docs.docker.com/engine/release-notes/29/ | "Docker Engine version 29 release notes" / "29.9.0" | page updated 2026-10-20 |
| 15 | Docker 29.0.0 removed DCT | Docker Content Trust removed from CLI\[4\] | https://matsuand.github.io/docker.docs-ja/engine/release-notes/29/ (mirror of Docker docs) | "Docker Content Trust was removed from the Docker CLI." | 2025-11 |
| 16 | Docker 29 containerd store | Default for fresh installs\[5\] | https://en.wikipedia.org/wiki/Docker_(software) (secondary) | "The release made the containerd image store the default for fresh installations" | read 2026-10-26 |
| 17 | Docker 29.5.0 rootless networking | gvisor-tap-vsock default\[53\] | https://github.com/Delphoa/study-docker-docs/blob/main/content/manuals/engine/release-notes/29.md (mirror of Docker docs) | "Rootless: gvisor-tap-vsock is now the new default rootless network driver and should be preferred over slirp4netns" | 2026 |
| 18 | Docker Hardened Images | Free, Apache 2.0\[47\] | https://www.docker.com/products/hardened-images/ | "Docker Hardened Images are now free and open source under Apache 2.0." | read 2026-10-26 |
| 19 | DHI free date | 17 Dec 2025\[54\] | https://siliconangle.com/2025/12/17/docker-open-sources-entire-catalog-hardened-images-making-free-everyone/ (secondary) | "making its entire catalog of more than 1,000 Docker Hardened Images available entirely for free, under the open-source Apache 2.0 license" | 2025-12-17 |
| 20 | Podman 6.0 | Released | https://lwn.net/Articles/1079600/ (secondary) | "Version 6.0.0 of the Podman container-management tool has been released."\[55\] | 2026-06-25 |
| 21 | Podman 6 removals | slirp4netns, cgroups v1, BoltDB | https://fedoraproject.org/wiki/Changes/Podman6 | "This release finalizes the removal of support for slirp4netns, cgroups v1, and the BoltDB database backend."\[39\] | updated 2026-03-11 |
| 22 | Kubernetes 1.34 EOL | 27 Oct 2026 | https://kubernetes.io/releases/patch-releases/ | "The End of Life date for Kubernetes 1.34 is Oct 27, 2026." | read 2026-10-26 |
| 23 | Kubernetes 1.34 maintenance | From 27 Aug 2026\[1\] | same | "Kubernetes 1.34 entered maintenance mode on Aug 27, 2026" | read 2026-10-26 |
| 24 | AKS 1.34 EOL | Nov 2026 (LTS to Nov 2027)\[41\] | https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions | "1.34 \| Aug 2025 \| Oct 2025 \| Nov 2025 \| Nov 2026" | read 2026-10-26 |
| 25 | ingress-nginx retirement | March 2026 | https://opensource.googleblog.com/2026/02/the-end-of-an-era-transitioning-away-from-ingress-nginx.html (secondary, quoting Kubernetes blog) | "there will be no further releases, no bugfixes, and no updates to resolve any security vulnerabilities that may be discovered." | 2026-02-12 |
| 26 | Gateway API v1.4.0 | 6 Oct 2025 | https://kubernetes.io/blog/2025/11/06/gateway-api-v1-4/ | "Released on October 6, 2025, version 1.4.0 reinforces the path"\[56\] | 2025-11-06 |
| 27 | Gateway API v1.5 | 27 Feb 2026 | https://kubernetes.io/blog/2026/04/21/gateway-api-v1-5/ | "Released on February 27, 2026, version 1.5 is our biggest release yet"\[9\] | 2026-04-21 |
| 28 | Helm 4.0.0 | 12 Nov 2025\[11\] | https://helm.sh/blog/helm-4-released/ | "On Wednesday November 12th, during the Helm 4 presentation at KubeCon + CloudNativeCon, Helm v4.0.0 was released." | 2025-11-17 |
| 29 | Helm 3 security fixes end | 10 Feb 2027 | https://helm.sh/blog/helm-v3-end-of-life/ | "Security fixes end February 10th, 2027 (extended from November 2026)." | 2026-06-02 |
| 30 | OpenTofu 1.13.0 | 30 Sep 2026 | https://github.com/opentofu/opentofu/releases/tag/v1.13.0 | "We're proud to announce that OpenTofu 1.13.0 is now officially available!" | 2026-09-30 |
| 31 | OpenTofu 1.13 WinRM | Removed | https://opentofu.org/blog/opentofu-1-13-0/ | "v1.13.0 completes that process by completely removing support for using the WinRM protocol with the remote-exec and file provisioners." | 2026-09-29 |
| 32 | OpenTofu 32-bit | 1.13 is last series\[22\] | same | "OpenTofu v1.13 will be the last series that includes official releases for the affected platforms" | 2026-09-29 |
| 33 | Terraform 1.16.0 | 26 Aug 2026\[25\] | https://github.com/hashicorp/terraform/releases/tag/v1.16.0 | "1.16.0 (August 26, 2026)" | 2026-08-26 |
| 34 | Terraform latest patch | 1.16.6 | https://github.com/hashicorp/terraform/releases | "1.16.6 (October 14, 2026)" | 2026-10-14 |
| 35 | Ubuntu 26.04 LTS | 23 Apr 2026 | https://canonical.com/blog/canonical-releases-ubuntu-26-04-lts-resolute-raccoon | "Today Canonical announced the release of Ubuntu 26.04 LTS, codenamed “Resolute Raccoon,”" | 2026-04-23 |
| 36 | Ubuntu 26.04 kernel | Linux 7.0 | same | "Ubuntu 26.04 LTS is built on Linux 7.0" | 2026-04-23 |
| 37 | Debian 13.7 | 12 Sep 2026 | https://www.debian.org/News/2026/20260912 | "The Debian project is pleased to announce the seventh update of its stable distribution Debian 13 (codename trixie)." | 2026-09-12 |
| 38 | RHEL 10.2 GA | 2026-05-19 | https://access.redhat.com/articles/red-hat-enterprise-linux-release-dates | "RHEL 10.2 \| 2026-05-19"\[45\] | read 2026-10-26 |
| 39 | Fedora 45 | Target 27 Oct 2026\[43\] | https://linuxiac.com/fedora-linux-45-delayed-new-release-date-set-for-october-27/ (secondary) | "The Fedora Project pushed the release back one week, setting October 27 as the new target" | 2026-10-17 |
| 40 | Suricata 8.0.0 | 8 Jul 2025\[52\] | https://suricata.io/2025/07/08/suricata-8-0-0-released/ | "this is the first stable release of Suricata 8" | 2025-07-08 |
| 41 | Suricata latest | 8.0.7 | https://suricata.io/2026/09/15/suricata-8-0-7-released/ | "We are pleased to announce the release of Suricata 8.0.7. This is a security release" | 2026-09-15 |
| 42 | Suricata 7 EOL | July 2026 | https://suricata.io/2026/07/09/suricata-8-0-6-and-7-0-17-released/ | "Suricata 7 has reached EOL. This means that the latest Suricata 7.0.17 will be the last one in this series." | 2026-07-09 |
| 43 | CIS Controls | v8.1 current\[33\] | https://www.cisecurity.org/controls | "Download CIS Controls v8.1" | read 2026-10-26 |
| 44 | Pi-hole | FTL v6.8 / Web v6.6.1 / Core v6.5 | https://pi-hole.net/blog/2026/10/17/pi-hole-ftl-v6-8-web-v6-6-1-and-core-v6-5-released/ | "Pi-hole FTL v6.8, Web v6.6.1 and Core v6.5 are now available. This release fixes a number of security advisories" | 2026-10-17 |
| 45 | Zeek LTS | 9.0.0 | https://zeek.org/get-zeek/ | "CURRENT LTS RELEASE / Zeek 9.0.0 / September 14, 2026" | 2026-09-14 |
| 46 | Snort 3 | 3.12.4.0; Snort 2 EOL\[30\] | https://blog.snort.org/2026/10/end-of-life-announcement-for-open.html | "All versions of the open-source Snort2 engine have now formally reached its end-of-life (EOL) and end-of-support (EOS)" | 2026-10-21 |
| 47 | systemd 260 | Released 17 Mar 2026 | https://github.com/systemd/systemd/releases/tag/v260 | "CHANGES WITH 260:"\[57\] | 2026-03-17 |
| 48 | systemd 260 SysV | Removed | https://github.com/systemd/systemd/releases/tag/v260 ; https://www.phoronix.com/news/systemd-260-Released (secondary) | "Support for System V service scripts has been removed." | 2026-03-17 |

## 4. Findings

### 4.1 Shell

**Bash 5.3.** The announcement (Chet Ramey, 5 July 2025) lists "a new form of command substitution that executes the command in the current shell execution context", `GLOBSORT`, `compgen -V varname`, `read -E`, and `source -p PATH`.\[12\]\[13\]\[14\]\[58\] It also flags two incompatibilities: `test` with parenthesised subexpressions and more than four arguments now parses like coreutils, and interactive shells defer job notifications while sourcing.\[12\] For scripts, the practical gains are `${ cmd; }` (no fork, so no subshell variable loss) and `printf %#q` forcing single quotes. Neither is portable, so guard them with a version check (`BASH_VERSINFO`) if a script may meet older Bash. Bash 5.3's end-of-support date: not found; GNU does not publish one.

**POSIX.1-2024.** The standard's own rationale lists the new utilities as gettext, msgfmt, ngettext, readlink, realpath, timeout and xgettext.\[16\] The Shell Command Language chapter defines dollar-single-quotes (including `\e` and `\xXX`) and adds `-o pipefail` via Austin Group Defect 789.\[15\] Our list was right on `$'...'`, `pipefail`, `readlink` and `realpath`, but missed `timeout`. The secondary Sortix summary lists `find -print0` (along with `-iname` and `-mount`);\[40\] `xargs -0` was not verified in this run. Conformance in practice lags: ShellCheck's wiki notes dash only gained `pipefail` in 5.13.\[17\] A `#!/bin/sh` script therefore still cannot assume `pipefail` on older Debian/Ubuntu dash. Use the subshell probe ShellCheck documents: `(set -o pipefail 2>/dev/null) && set -o pipefail`.\[17\]

**GNU vs BSD portability.** Not sourced in this run (see section 9). Our position, unsourced: prefer the POSIX.1-2024 forms above, and test on macOS before claiming portability.

**`set -euo pipefail` pitfalls.** No primary source fetched this run beyond the POSIX `pipefail` definition. That definition says the exit status is derived "from the exit statuses of all of the commands in the pipeline, not just the last".\[15\] One consequence follows directly: a pipeline whose producer receives SIGPIPE (e.g. `cmd | head -1`) can fail under `pipefail`. Fuller pitfalls are listed as not covered.

**Tool versions.** ShellCheck v0.11.0 (3 August 2025) is still the latest, and it adds SC2327–SC2335 (secondary changelog).\[18\]\[59\] shfmt and bats-core versions: not found in this run.

**When to stop writing shell.** Not sourced in this run. Repository position (judgment, not a sourced fact): move to Python once a script needs structured data (JSON/YAML parsing), arrays of records, non-trivial error handling, or must run on Windows.

### 4.2 Configuration formats

**TOML 1.1.0** (changelog 2025-12-18; GitHub release object 24 December 2025) changes:
- inline tables may span lines and end with a trailing comma;
- adds `\xHH` and `\e` escapes;
- makes seconds optional in datetime and time values;
- clarifies that comments never affect the tables produced, how dotted keys define tables, and that parsers may support any int/float size.\[20\]\[21\]

Downstream support arrived gradually: smol-toml added it in v1.6.0, whose GitHub release notes say "As of this version, smol-toml now supports the newly released TOML 1.1.0 specification!", and TomlJ added it in a release dated 18 October. A file using 1.1 syntax can therefore fail in a 1.0-only parser. Skills should tell authors to stay with 1.0 syntax unless the consuming parser is known to support 1.1.

YAML 1.2.2 pitfalls, JSONC/JSON5, JSON Schema 2020-12, SchemaStore, yamllint, taplo, EditorConfig: not found in this run.

### 4.3 Containers

**Docker Engine.** Docker's release-notes page for version 29 (updated 2026-10-20) lists 29.9.0 at the top; a secondary tracker reports 29.9.2 on 20 October 2026.\[3\]\[60\] Changes in Engine 29.0.0 (November 2025):
- the containerd image store is the default for fresh installs;
- Docker Content Trust was removed from the CLI;
- the minimum API version was raised to 1.44 (secondary);
- nftables rules are experimental;
- "When dynamically linked, the Docker daemon now depends on libnftables."\[4\]\[5\]\[6\]\[53\]

29.5.0 makes gvisor-tap-vsock the default rootless network driver and stops packaging slirp4netns.\[53\] End of support for Engine 29: not found (VersionLog says "TBD", secondary).\[60\]

**Docker Hardened Images.** DHI is free and open source under Apache 2.0, with more than 1,000 images built on Debian and Alpine. A paid DHI Enterprise tier remains. Each image ships with an SBOM and SLSA Build Level 3 provenance (SecurityWeek, secondary).\[54\]\[61\]\[62\]

**Podman.** 6.0.0 was released on 24 June 2026; Wikipedia (secondary) lists 6.1.3 on 29 September 2026.\[38\]\[63\] Fedora's change page confirms the removal of slirp4netns, cgroups v1 and BoltDB, with Pasta as the rootless network default.\[39\] Secondary sources add the removal of CNI and iptables, the end of Intel-Mac and Windows 10 support, libkrun as the default on macOS, and AMD GPU support for `--gpus`.\[64\]\[65\]

Compose version, Dockerfile practice (multi-stage, non-root, digests, `.dockerignore`, secret/cache mounts, `COPY --link`, heredocs), distroless/Chainguard/Alpine/Debian slim/Ubuntu images, and Scout/Trivy/Grype/cosign: not found in this run.

### 4.4 Linux administration

**systemd.** v260 was released on 17 March 2026 (GitHub release page; Phoronix, 17 March 2026). Its release notes say "Support for System V service scripts has been removed." Phoronix (secondary) also reports `systemd-mstack`, `FANCY_NAME=` in os-release, and OCI image download in `systemd-importd`. Wikipedia (secondary) lists 262 (22 September 2026) as the latest stable release, and a secondary Fedora 45 review reports systemd 262 in Fedora 45.\[37\]\[66\] Timers vs cron, hardening options, cgroups v2, SELinux/AppArmor, firewalld/nftables, journald: not sourced in this run. The ecosystem is moving off iptables, though: Docker 29 depends on libnftables, and Podman 6 removed iptables support (secondary).\[65\]

**Distribution release and support dates**

| Distribution | Current | Released | End of support | Next release (≤6 months) | Flag (EOL ≤12 months) |
|---|---|---|---|---|---|
| Debian 13 trixie | 13.7 (12 Sep 2026)\[48\] | 9 Aug 2025 (secondary)\[49\] | Security 9 Aug 2028; LTS 30 Jun 2030; ELTS 30 Jun 2035 (Wikipedia, secondary)\[67\] | Point releases roughly every two months (13.5 May, 13.6 Jul, 13.7 Sep)\[48\]\[68\]\[69\] | No (Debian 12 regular security ended 10 Jun 2026, LTS to 30 Jun 2028, secondary)\[67\] |
| Ubuntu 26.04 LTS | 26.04.1 (27 Aug 2026, secondary)\[70\] | 23 Apr 2026 | Standard support to April 2031 (secondary); **contested**: Hackster says "through to May 2031"\[70\]\[71\] | 26.10 shipped 15 Oct 2026 (Wikipedia, secondary)\[72\] | No |
| RHEL 10 | 10.2 (GA 2026-05-19) | May 2025 | Full support to 31 May 2030; maintenance to 31 May 2035 (endoflife.date, secondary) | not found (Red Hat "does not generally disclose future release schedules") | RHEL 10.0 minor EOL 31 May 2027 (versio.io, secondary) |
| Fedora 44 | 44 | 28 Apr 2026 (secondary)\[44\] | not found | Fedora 45 target 27 Oct 2026 (secondary); release party 30 Oct 2026 (fedoraproject.org)\[43\]\[73\] | **Fedora 43 EOL 9 December 2026** (endoflife.date and Wikipedia; contested: versio.io says 28 November 2026) |

RHEL rebuilds (AlmaLinux, Rocky), Fedora Atomic, bootc, rpm-ostree, Universal Blue and Bazzite: not found in this run.

### 4.5 Network security

- **Suricata.** 8.0.0 was released on 8 July 2025, and 8.0.7 (15 September 2026, a security release) is current. Suricata 7 reached end of life in July 2026; 7.0.17 was the last 7.x release.\[28\]\[29\]\[52\]
- **Snort.** Snort 3.12.4.0 is current (21 October 2026). Every open-source Snort 2 release, including 2.9.20, is end of life.\[30\]\[74\]
- **Zeek.** 9.0.0 is the current LTS (14 September 2026); zeek.org's "Introducing Zeek 9" says "the Zeek 9.0.x series will see security fixes and relevant backports for a bit over a year." The previous LTS, 8.0.10 (19 August 2026), keeps getting patches "until 9.1.0 is released". The same post says 8.0.x "will stop receiving updates when we release 9.1 in about four months", and Zeek Newsletter Issue 65 places 9.1 "at the end of the year".
- **Pi-hole.** FTL v6.8 / Web v6.6.1 / Core v6.5 (Docker tag 2026.10.0) shipped on 17 October 2026 and "fixes a number of security advisories".\[31\] Update now.
- **CIS Controls.** v8.1 is still current and v9 is only in development. The v8.1 date (June 2024) was seen only on a third-party mirror.\[32\]\[33\]\[75\]

RFC 4890, NIST SP 800-207, WireGuard, WPA3/6 GHz/802.11w, and DoH/DoT/DNSSEC guidance: not found in this run.

### 4.6 Kubernetes

The upstream cadence of three minors a year holds (1.34 Aug 2025, 1.35 Dec 2025, 1.36 Apr 2026, 1.37 Aug 2026, per the AKS calendar's upstream column).\[41\] After 27 October 2026, upstream supports 1.35, 1.36 and 1.37. Secondary sources give their end-of-life dates as 28 Feb 2027, 28 Jun 2027 and 28 Oct 2027.\[2\] Managed services run on their own calendars: AKS 1.34 ends in Nov 2026, with LTS to Nov 2027.\[41\] On EKS, AWS's own extended-support pricing post says a cluster costs "$0.10 per cluster per hour" in standard support and "$0.60 per cluster per hour" in extended support. The 2 Dec 2026 end of EKS 1.34 standard support comes only from secondary sources.

**Ingress and the Gateway API.**
- ingress-nginx: the retirement was announced on 11 November 2025 and took effect in March 2026, with a Steering/SRC statement on 29 January 2026. The repository is archived (secondary).\[7\]\[76\]\[77\]
- Gateway API v1.4.0 (6 October 2025) promoted BackendTLSPolicy, GatewayClass `supportedFeatures` and named route rules to Standard.
- Gateway API v1.5 (27 February 2026) promoted ListenerSet, TLSRoute, the HTTPRoute CORS filter, client-certificate validation, certificate selection for gateway TLS origination, and ReferenceGrant. v1.5.1 followed.

**Helm.** 4.0.0 shipped on 12 November 2025. Helm 3's final feature release was 9 September 2026, and its security fixes end on 10 February 2027. The helm.sh docs show 4.3.1 and 3.22.1 as current (subagent finding from helm.sh).\[10\]\[11\]

Pod Security Standards, sidecar containers, the CIS Kubernetes Benchmark and the NSA/CISA guide: not found in this run.

### 4.7 Infrastructure as code

- **OpenTofu 1.13.0** (30 September 2026, with 1.13.1 on 1 October): Windows ARM64 support; new `assume…` functions that reduce unknowns at plan time; experimental built-in linting and symbol libraries; WinRM removed; changed `base64gzip` output; macOS 13 minimum; last series with 32-bit builds. A secondary source says the 1.13 series is supported until August 2027, and that 1.11.14 (19 August 2026) was the final 1.11 patch.\[23\]\[78\]\[79\]\[80\]
- **OpenTofu 1.12.0** (14 May 2026) added dynamic `prevent_destroy` and import by resource identity.\[24\]\[81\]\[82\]
- **Terraform 1.16.0** (26 August 2026): import blocks inside modules, a `terraform_data` `store` block for ephemeral and sensitive values, `lifecycle { destroy = false }`, and Mermaid output from `terraform graph`. 1.16.6 (14 October 2026) fixes an HTTP/2 resource-exhaustion issue (CVE-2026-78669). The licence is BSL 1.1 (secondary).\[25\]\[26\]\[27\]\[83\]
- **Not found in this run:** Pulumi, Bicep, AWS CDK, tflint, checkov, trivy config, `terraform test` and state security. OpenTofu's state encryption is mentioned only by secondary sources.

### 4.8 Cloud baselines

Not found in this run. The only related finding is the EKS/AKS/GKE Kubernetes support calendars in 4.6.

### 4.9 Linux gaming

Not found in this run (Proton, Proton-GE, Bazzite, handhelds, anti-cheat tracking, ntsync).

### 4.10 Untrusted text and downloads

Sourced in this run:
- Bash 5.3's `printf` "uses the `alternate form' for %q and %Q to force single quoting".\[12\] Use `printf '%q'` (or `%#q` in 5.3) to show untrusted strings with control characters and escape sequences made visible.
- POSIX `$'...'` now standardises `\e`.\[15\] Escape sequences are trivially constructible, which is exactly why raw `echo "$untrusted"` to a terminal is unsafe.
- Docker Hardened Images ship SLSA Build Level 3 provenance and SBOMs (secondary).\[61\] That provenance is the verification route, not a checksum published next to the download.
- Docker removed Docker Content Trust from the CLI in 29.0.0, so `DOCKER_CONTENT_TRUST=1` is no longer a signature check.\[4\]

Not found in this run: the documentation for `cosign verify`, `gh attestation verify` and minisign, hidden-Unicode guidance, and a primary source on refusing `curl | sh`. The repository's position (judgment, unsourced here): verify by signature or provenance from a separate trust root, and never by a checksum fetched from the same origin as the artifact.

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| Bash | Shell | 5.3 | 2025-07-05 | not sourced | `~/.bashrc` (not sourced) | https://www.mail-archive.com/bug-bash@gnu.org/msg34422.html |
| ShellCheck | Shell linter (GPL-3.0) | v0.11.0 | 2025-08-03 | `mise use shellcheck@latest` (mise page, secondary)\[84\] | `.shellcheckrc` (not sourced) | https://github.com/koalaman/shellcheck/releases |
| Docker Engine | Container runtime | 29.9.x | 29.9.0 top of notes, page updated 2026-10-20\[3\] | not sourced | `/etc/docker/daemon.json` (not sourced) | https://docs.docker.com/engine/release-notes/29/ |
| Podman | Daemonless containers | 6.1.3 (secondary) | 2026-09-29 (6.0.0: 2026-06-24) | not sourced | `containers.conf` (secondary) | https://lwn.net/Articles/1079600/ |
| Helm | Kubernetes packages | 4.3.1 (Helm 3: 3.22.1)\[10\] | 4.0.0: 2025-11-12\[11\] | not sourced | — | https://helm.sh/blog/helm-4-released/ |
| OpenTofu | IaC (MPL-2.0) | 1.13.1 | 2026-10-01 | `brew install opentofu` (secondary)\[85\] | `*.tf`, `*.tofu` | https://github.com/opentofu/opentofu/releases/tag/v1.13.0 |
| Terraform | IaC (BSL 1.1) | 1.16.6 | 2026-10-14 | not sourced | `*.tf` | https://github.com/hashicorp/terraform/releases |
| systemd | Init/service manager | 262 (secondary); 260 confirmed | 262: 2026-09-22 (secondary) | — | unit files | https://github.com/systemd/systemd/releases/tag/v260 |
| Suricata | IDS/IPS | 8.0.7 | 2026-09-15 | not sourced | `suricata.yaml` (not sourced) | https://suricata.io/2026/09/15/suricata-8-0-7-released/ |
| Zeek | Network monitoring | 9.0.0 LTS\[34\] | 2026-09-14 | not sourced | — | https://zeek.org/get-zeek/ |
| Snort | IDS/IPS | 3.12.4.0 | 2026-10-21 | not sourced | — | https://blog.snort.org/2026/10/end-of-life-announcement-for-open.html |
| Pi-hole | DNS filtering | FTL 6.8 / Web 6.6.1 / Core 6.5\[31\] | 2026-10-17 | Docker tag `2026.10.0`\[31\] | `pihole.toml` (not sourced) | https://pi-hole.net/blog/2026/10/17/pi-hole-ftl-v6-8-web-v6-6-1-and-core-v6-5-released/ |

## 6. Changing in the next 12 months

| Date | Change | Source |
|---|---|---|
| **27 Oct 2026** | Kubernetes 1.34 upstream end of life\[1\] | https://kubernetes.io/releases/patch-releases/ |
| 27 Oct 2026 (target) | Fedora 45 release (slipped from 20 Oct; fallback 3 Nov, secondary)\[43\]\[86\] | https://linuxiac.com/fedora-linux-45-delayed-new-release-date-set-for-october-27/ |
| Nov 2026 | AKS 1.34 end of life\[41\] | https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions |
| 2 Dec 2026 | EKS 1.34 standard support ends (secondary);\[87\] afterwards extended support costs $0.60 instead of $0.10 per cluster per hour (AWS extended-support pricing post) | https://dev.to/skyhook-radar/kubernetes-134-end-of-life-what-actually-happens-on-eks-gke-and-aks-g8e |
| 9 Dec 2026 | Fedora 43 end of life (endoflife.date; contested: versio.io says 28 Nov 2026) | https://www.linuxcompatible.org/story/fedora-45-final-freeze-october-20-release-date-set-as-trackers-clear/ |
| End of 2026 / ~Jan 2027 | Zeek 9.1 expected ("in about four months" per zeek.org "Introducing Zeek 9"); 8.0 LTS patches stop when 9.1 ships | zeek.org "Introducing Zeek 9"; Zeek Newsletter Issue 65 |
| **10 Feb 2027** | Helm 3: no further releases of any kind\[10\] | https://helm.sh/blog/helm-v3-end-of-life/ |
| 28 Feb 2027 | Kubernetes 1.35 end of life (secondary, citing kubernetes.io)\[2\] | https://www.nihardaily.com/posts/kubernetes-134-reaches-end-of-life-on-october-27 |
| 31 May 2027 | RHEL 10.0 minor-release support ends (secondary) | https://www.versio.io/en/product-release-end-of-life-eol-red-hat-red-hat-enterprise-linux.html |
| 28 Jun 2027 | Kubernetes 1.36 end of life (secondary)\[2\]\[88\] | same as 28 Feb row |
| Aug 2027 | OpenTofu 1.13 series support ends (secondary)\[79\] | https://dev.to/saaro_net/opentofu-113-symbol-libraries-linting-experiment-and-fewer-unknowns-in-planning-ce |
| Next OpenTofu series (1.14) | No official 32-bit (386, arm) builds\[22\] | https://opentofu.org/blog/opentofu-1-13-0/ |
| Already happened, act now | Suricata 7 EOL (Jul 2026); Snort 2 EOL; ingress-nginx retired (Mar 2026); Docker Content Trust removed (Engine 29.0.0); Podman 6 removed cgroups v1, slirp4netns, BoltDB | sources in section 3 |

## 7. Common mistakes

1. **Treating `set -o pipefail` as non-POSIX, or as universally available in `/bin/sh`.** It is POSIX.1-2024, but dash only supports it from 5.13.\[17\] Source: https://www.shellcheck.net/wiki/SC3040
2. **Saying POSIX lacks `readlink`, `realpath` or `timeout`.** All three are new utilities in Issue 8.\[16\] Source: https://pubs.opengroup.org/onlinepubs/9799919799/xrat/V4_xcu_chap01.html
3. **Writing TOML 1.1 syntax (multi-line inline tables, trailing commas, `\e`) for parsers that only support 1.0.**\[20\] Source: https://github.com/toml-lang/toml/releases/tag/1.1.0
4. **Recommending `DOCKER_CONTENT_TRUST=1` for image signing.** Docker Content Trust was removed from the CLI in Engine 29.0.0.\[4\] Source: https://matsuand.github.io/docker.docs-ja/engine/release-notes/29/
5. **Generating Podman instructions with slirp4netns, CNI, cgroups v1 or iptables.** Podman 6 removed them.\[89\] Source: https://fedoraproject.org/wiki/Changes/Podman6
6. **Scaffolding new clusters with ingress-nginx annotations (`nginx.ingress.kubernetes.io/*`).** The controller is retired; use Gateway API or a maintained controller.\[8\]\[42\] Source: https://opensource.googleblog.com/2026/02/the-end-of-an-era-transitioning-away-from-ingress-nginx.html (secondary)
7. **Pinning Kubernetes 1.34 or earlier in new manifests or CI kind clusters.** 1.34 reaches end of life on 27 Oct 2026.\[1\] Source: https://kubernetes.io/releases/patch-releases/
8. **Assuming Helm 3 is supported indefinitely.** Its final release window closes on 10 Feb 2027.\[10\] Source: https://helm.sh/blog/helm-v3-end-of-life/
9. **Calling Terraform "open source".** It is under the Business Source License 1.1; OpenTofu is the MPL-2.0 fork.\[27\]\[51\] Sources: https://en.wikipedia.org/wiki/Terraform_(software) and https://en.wikipedia.org/wiki/OpenTofu (secondary)
10. **Using WinRM provisioners or 32-bit builds with OpenTofu.** WinRM was removed in 1.13, and 32-bit builds end after 1.13.\[22\] Source: https://opentofu.org/blog/opentofu-1-13-0/
11. **Recommending Snort 2 rules or Suricata 7 deployments.** Both are end of life.\[29\]\[30\] Sources: https://blog.snort.org/2026/10/end-of-life-announcement-for-open.html ; https://suricata.io/2026/07/09/suricata-8-0-6-and-7-0-17-released/
12. **Shipping SysV init scripts to modern systemd hosts.** systemd 260 dropped support for them.\[90\] Source: https://www.phoronix.com/news/systemd-260-Released (secondary)

AI-assistant-specific evidence (studies of assistant error rates in this area): not found in this run. Items 1–12 are the errors this run's corrections make most likely, inferred from the version changes above.

## 8. Sources and licences

Licences were not individually verified in this run unless stated. Where a source's licence is unverified, the safe default for an Apache-2.0 repository is: quote briefly (a sentence) with a link, paraphrase freely with a link, and do not copy code examples until the licence is confirmed.

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| pubs.opengroup.org (POSIX.1-2024) | Copyright IEEE and The Open Group ("Copyright © 2001-2024 The IEEE and The Open Group");\[16\] not open-licensed | Brief only | Yes | No | Cite standard, section, URL |
| bug-bash announcement (mail-archive.com) | not verified | Brief | Yes | No | Author (Chet Ramey), date, URL |
| GitHub release pages (ShellCheck GPL-3.0; OpenTofu MPL-2.0; Terraform BSL 1.1; TOML spec repo) | Project licence applies to code; release-note text licence not verified | Brief | Yes | Only per project licence (GPL-3.0 code must not be copied into Apache-2.0 files) | Project, version, URL |
| shellcheck.net wiki | not verified | Brief | Yes | Short snippets only after licence check | URL |
| docs.docker.com / docker.com | not verified | Brief | Yes | Not until verified | URL, date |
| kubernetes.io (blog, releases) | not verified in this run | Brief | Yes | Not until verified | URL, date |
| helm.sh blog | not verified | Brief | Yes | Not until verified | URL, date |
| opentofu.org blog | not verified | Brief | Yes | Not until verified | URL, date |
| canonical.com, documentation.ubuntu.com | not verified | Brief | Yes | No | URL, date |
| debian.org news | not verified | Brief | Yes | No | URL, date |
| access.redhat.com | Red Hat copyright (not open-licensed, not verified) | Brief | Yes | No | URL |
| fedoraproject.org wiki | not verified | Brief | Yes | No | URL |
| learn.microsoft.com (AKS) | not verified | Brief | Yes | No | URL |
| suricata.io, zeek.org, blog.snort.org, pi-hole.net, cisecurity.org | not verified (CIS Controls have their own terms of use, not checked) | Brief | Yes | No | URL, date |
| Secondary: Wikipedia | CC BY-SA 4.0 (general knowledge; not verified this run) | Brief | Yes | No (share-alike incompatible with Apache-2.0 for copied text) | Article, URL |
| Secondary: LWN, Phoronix, linuxiac, dev.to, Medium, SiliconANGLE, TechTarget, SecurityWeek, computingforgeeks, versio.io, endoflife.date, mise | not verified | Brief | Yes | No | Publication, URL, date |

## 9. Not found, contested, not covered

**Contested**
- **TOML 1.1.0 date:** CHANGELOG says 2025-12-18; the GitHub release object is dated 24 December.\[20\]\[21\]
- **Bash 5.3 date:** the announcement is dated 5 Jul 2025; Wikipedia (secondary) says 3 July 2025.\[12\]\[91\]
- **Ubuntu 26.04 standard support end:** "April 2031" (computingforgeeks) vs "through to May 2031" (Hackster), both secondary.\[70\]\[71\]
- **Ubuntu 26.04.1 date:** scheduled 6 August 2026 (LinuxConfig) vs released 27 August 2026 (computingforgeeks), both secondary.\[70\]\[92\]
- **Latest Docker Engine 29 patch:** 29.9.0 is the top entry confirmed on Docker's page; 29.9.2 on 20 Oct 2026 per VersionLog (secondary); Wikipedia (secondary) lists 29.8.2 (30 Sep 2026).\[3\]\[5\]\[60\]
- **ingress-nginx "in favour of the Gateway API":** the official recommendation is Gateway API *or* another Ingress controller.\[42\]

**Not found (this run)**
- Exact day of Suricata 7 EOL (only "July 2026").
- Publication date of CIS Controls v8.1 on cisecurity.org (a third-party mirror shows June 2024).
- End-of-support dates for Bash 5.3, Docker Engine 29 and Podman 6.

**Not covered (search budget exhausted; carry into a follow-up run)**
- Q1: GNU vs BSD tool differences; macOS Bash 3.2/zsh; the full `set -e` pitfall list; shfmt and bats-core versions; `xargs -0` in POSIX.1-2024 (primary); `find -print0` (primary).
- Q2: YAML 1.2.2 (Norway problem, anchors), JSONC/JSON5, JSON Schema 2020-12, SchemaStore, yamllint, taplo, EditorConfig.
- Q3: Compose version and the `version` key/`compose.yaml`; BuildKit default; Dockerfile best practices; base images (distroless, Chainguard/Wolfi, Debian 13 slim, Alpine, Ubuntu 26.04); Docker Scout, Trivy, Grype, cosign; rootless Docker.
- Q4: timers vs cron; systemd hardening options; cgroups v2; SELinux/AppArmor; firewalld/nftables/iptables status; journald; RHEL rebuilds; Fedora Atomic, bootc, rpm-ostree, Universal Blue, Bazzite.
- Q5: RFC 4890; NIST SP 800-207; WireGuard; WPA3/6 GHz/802.11w; DoH/DoT/DNSSEC.
- Q6: Pod Security Standards; sidecar containers; CIS Kubernetes Benchmark; NSA/CISA hardening guide.
- Q7: Pulumi, Bicep, AWS CDK; tflint, checkov, trivy config, `terraform test`; state security.
- Q8: all items.
- Q9: all items.
- Q10: cosign, `gh attestation verify`, minisign, distribution package signatures, hidden-Unicode detection, `curl | sh` refusal sources.

## Sources

1. [Patch Releases](https://kubernetes.io/releases/patch-releases/)
2. [Kubernetes 1.34 reaches end of life on October 27](https://www.nihardaily.com/posts/kubernetes-134-reaches-end-of-life-on-october-27)
3. [Docker Engine version 29 release notes](https://docs.docker.com/engine/release-notes/29/)
4. [Docker Engine version 29 release notes](https://matsuand.github.io/docker.docs-ja/engine/release-notes/29/)
5. [Docker (software)](<https://en.wikipedia.org/wiki/Docker_(software)>)
6. [Docker Engine 29: Containerd Becomes Default, Experimental nftables Support](https://linuxiac.com/docker-engine-29-containerd-becomes-default-experimental-nftables-support/)
7. [Ingress NGINX End of Life (March 2026): Risks, Migration Paths, and Support Options](https://www.herodevs.com/blog-posts/ingress-nginx-end-of-life-2026-migration-and-support)
8. [The End of an Era: Transitioning Away from Ingress NGINX](https://opensource.googleblog.com/2026/02/the-end-of-an-era-transitioning-away-from-ingress-nginx.html)
9. [Gateway API v1.5: Moving features to Stable](https://kubernetes.io/blog/2026/04/21/gateway-api-v1-5/)
10. [Helm 3 End of Life | Helm](https://helm.sh/blog/helm-v3-end-of-life/)
11. [Helm 4 Released | Helm](https://helm.sh/blog/helm-4-released/)
12. [Bash-5.3-release available](https://www.mail-archive.com/bug-bash@gnu.org/msg34422.html)
13. [Bash 5.3 Released With Many Improvements - Phoronix](https://www.phoronix.com/news/GNU-Bash-5.3)
14. [Bash 5.3 Now Available - admin](https://www.admin-it.io/bash-5-3-now-available/)
15. [2\. Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html)
16. [Rationale for Shell and Utilities](https://pubs.opengroup.org/onlinepubs/9799919799/xrat/V4_xcu_chap01.html)
17. [ShellCheck: SC3040](https://www.shellcheck.net/wiki/SC3040)
18. [Releases · koalaman/shellcheck · GitHub](https://github.com/koalaman/shellcheck/releases)
19. [koalaman/shellcheck v0.11.0 on GitHub](https://newreleases.io/project/github/koalaman/shellcheck/release/v0.11.0)
20. [Release Release 1.1.0 · toml-lang/toml · GitHub](https://github.com/toml-lang/toml/releases/tag/1.1.0)
21. [toml/CHANGELOG.md at main · toml-lang/toml · GitHub](https://github.com/toml-lang/toml/blob/main/CHANGELOG.md)
22. [OpenTofu v1.13.0](https://opentofu.org/blog/opentofu-1-13-0/)
23. [OpenTofu 1.13: What's New and What Terraform Still Doesn't Have - DEV Community](https://dev.to/amareswer/opentofu-113-whats-new-and-what-terraform-still-doesnt-have-4g49)
24. [opentofu](https://mise-versions.jdx.dev/tools/opentofu)
25. [Release v1.16.0 · hashicorp/terraform · GitHub](https://github.com/hashicorp/terraform/releases/tag/v1.16.0)
26. [Releases · hashicorp/terraform · GitHub](https://github.com/hashicorp/terraform/releases)
27. [Terraform (software)](<https://en.wikipedia.org/wiki/Terraform_(software)>)
28. [Suricata 8.0.7 released! - Suricata](https://suricata.io/2026/09/15/suricata-8-0-7-released/)
29. [Suricata 8.0.6 and 7.0.17 Released - Suricata](https://suricata.io/2026/07/09/suricata-8-0-6-and-7-0-17-released/)
30. [End-of-Life Announcement for Open-Source Snort2 and Strategic Security Updates for Snort3](https://blog.snort.org/2026/10/end-of-life-announcement-for-open.html)
31. [Pi-hole FTL v6.8, Web v6.6.1 and Core v6.5 released – Pi-hole](https://pi-hole.net/blog/2026/10/17/pi-hole-ftl-v6-8-web-v6-6-1-and-core-v6-5-released/)
32. [The Ongoing Evolution of the CIS Critical Security Controls](https://www.cisecurity.org/insights/blog/ongoing-evolution-cis-critical-security-controls)
33. [CIS Controls](https://www.cisecurity.org/controls)
34. [Get Zeek – Zeek Network Security Monitor](https://zeek.org/get-zeek/)
35. [Free Docker Hardened Images challenge Chainguard](https://www.techtarget.com/searchitoperations/news/366636656/Free-Docker-Hardened-Images-challenge-Chainguard)
36. [Docker Hardened Images Are Now Free: A Container Security Game Changer • William OGOU Cybersecurity Blog](https://blog.ogwilliam.com/post/docker-hardened-images-free-open-source)
37. [Systemd](https://en.wikipedia.org/wiki/Systemd)
38. [Latest features of Podman 6.0.0 and Podman Desktop 1.28: Come and discover them!](https://en.ubunlog.com/podman-desktop-new-features-2026/)
39. [Changes/Podman6 - Fedora Project Wiki](https://fedoraproject.org/wiki/Changes/Podman6)
40. [POSIX 2024 Changes - Sortix](https://sortix.org/blog/posix-2024/)
41. [Supported Kubernetes Versions in Azure Kubernetes Service (AKS) - Azure Kubernetes Service](https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions)
42. [NGINX Ingress Controller Retirement: Your Complete Migration Guide for March 2026](https://kubeace.com/blog/nginx-ingress-retirement-2026/)
43. [Fedora Linux 45 Delayed, New Release Date Set for October 27](https://linuxiac.com/fedora-linux-45-delayed-new-release-date-set-for-october-27/)
44. [Fedora Linux](https://en.wikipedia.org/wiki/Fedora_Linux)
45. [Red Hat Enterprise Linux Release Dates - Red Hat Customer Portal](https://access.redhat.com/articles/red-hat-enterprise-linux-release-dates)
46. [Red Hat Enterprise Linux](https://endoflife.date/rhel)
47. [Hardened Images](https://www.docker.com/products/hardened-images/)
48. [Debian -- News -- Updated Debian 13: 13.7 released](https://www.debian.org/News/2026/20260912)
49. [Debian](https://en.wikipedia.org/wiki/Debian)
50. [Canonical releases Ubuntu 26.04 LTS Resolute Raccoon](https://canonical.com/blog/canonical-releases-ubuntu-26-04-lts-resolute-raccoon)
51. [OpenTofu](https://en.wikipedia.org/wiki/OpenTofu)
52. [Suricata 8.0.0 released - Suricata](https://suricata.io/2025/07/08/suricata-8-0-0-released/)
53. [study-docker-docs/content/manuals/engine/release-notes/29.md at main · Delphoa/study-docker-docs · GitHub](https://github.com/Delphoa/study-docker-docs/blob/main/content/manuals/engine/release-notes/29.md)
54. [Docker makes its entire catalog of security-hardened container images free for everyone - SiliconANGLE](https://siliconangle.com/2025/12/17/docker-open-sources-entire-catalog-hardened-images-making-free-everyone/)
55. [Podman 6.0 released \[LWN.net\]](https://lwn.net/Articles/1079600/)
56. [Gateway API 1.4: New Features](https://kubernetes.io/blog/2025/11/06/gateway-api-v1-4/)
57. [Release systemd v260 · systemd/systemd · GitHub](https://github.com/systemd/systemd/releases/tag/v260)
58. [x-cmd blog (daily)](https://www.x-cmd.com/blog/250722/)
59. [ShellCheck changelog — v0.11.0, Aug 4, 2025 · What's New](https://whatsnew.fyi/product/shellcheck)
60. [Docker Engine 29 - What's New, Support Lifecycle & EOL — VersionLog](https://versionlog.com/docker-engine/29/)
61. [Docker Makes 1,000 Hardened Images Free and Open Source - SecurityWeek](https://www.securityweek.com/docker-makes-1000-hardened-images-free-and-open-source/)
62. [Docker makes hardened images free open and transparent for everyone - Help Net Security](https://www.helpnetsecurity.com/2025/12/22/free-open-docker-hardened-images/)
63. [Podman](https://en.wikipedia.org/wiki/Podman)
64. [Podman 6.0 Lands with Breaking Changes, AMD GPUs Support](https://linuxiac.com/podman-6-0-lands-with-breaking-changes-amd-gpus-support/)
65. [Podman 6.0 Is Here, and It Rips Out a Lot of Legacy Networking — Read This Before You Upgrade - H2S Media](https://www.how2shout.com/news/podman-6-0-networking-overhaul-breaking-changes.html)
66. [Fedora 45 Features: GNOME 51, Podman 6, rpm Changes](https://computingforgeeks.com/what-is-new-in-fedora-45/)
67. [Debian release version history](https://en.wikipedia.org/wiki/Debian_release_version_history)
68. [Debian -- News -- Updated Debian 13: 13.5 released](https://www.debian.org/News/2026/20260516)
69. [Debian -- News -- Updated Debian 13: 13.6 released](https://www.debian.org/News/2026/20260711)
70. [Ubuntu 26.04 LTS Features: Kernel 7.0, GNOME 50](https://computingforgeeks.com/ubuntu-2604-lts-features/)
71. [Canonical Launches Ubuntu 26.04 LTS "Resolute Raccoon," Its Latest Long-Term Support Linux Distro - Hackster.io](https://www.hackster.io/news/canonical-launches-ubuntu-26-04-lts-resolute-raccoon-its-latest-long-term-support-linux-distro-60bb7ff5e086)
72. [Ubuntu Budgie](https://en.wikipedia.org/wiki/Ubuntu_Budgie)
73. [Fedora Linux 45 Release Party Schedule - Fedora Project Wiki](https://fedoraproject.org/wiki/Fedora_Linux_45_Release_Party_Schedule)
74. [Cisco Security Advisory: Multiple Cisco Products Snort 3 Security Hardening Release: October 2026](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-hardening-snort3-ybgmhTQe)
75. [CIS Controls: Complete Guide \[2026\]](https://www.saltycloud.com/blog/cis-controls/)
76. [Nginx Ingress Is Dead: Your Complete Guide to What Comes Next :: ABGEO's Personal website](https://www.abgeo.dev/blog/nginx-ingress-retirement/)
77. [Posts in 2026](https://www.kubernetes.io/blog)
78. [OpenTofu Release Notes - October 2026 Latest Updates - Releasebot](https://releasebot.io/updates/opentofu)
79. [OpenTofu 1.13: Symbol Libraries, Linting Experiment, and Fewer Unknowns in Planning - DEV Community](https://dev.to/saaro_net/opentofu-113-symbol-libraries-linting-experiment-and-fewer-unknowns-in-planning-ce)
80. [OpenTofu 1.13 Re-Encodes base64gzip and Drops WinRM. We Upgraded the Same State to See What Breaks - DEV Community](https://dev.to/devopsdaily/opentofu-113-re-encodes-base64gzip-and-drops-winrm-we-upgraded-the-same-state-to-see-what-breaks-12bh)
81. [Release v1.12.0 · opentofu/opentofu · GitHub](https://github.com/opentofu/opentofu/releases/tag/v1.12.0)
82. [OpenTofu 1.12.0-beta1 is now available](https://opentofu.org/blog/help-us-test-opentofu-1-12-0-beta1/)
83. [terraform/CHANGELOG.md at v1.16.0 · hashicorp/terraform · GitHub](https://github.com/hashicorp/terraform/blob/v1.16.0/CHANGELOG.md)
84. [shellcheck](https://mise-versions.jdx.dev/tools/shellcheck)
85. [What Is OpenTofu? 2026 Guide to the Open-Source Terraform Fork](https://scalr.com/learning-center/what-is-opentofu)
86. [Fedora 45 Final Freeze: October 20 Release Date Set as Trackers Clear](https://www.linuxcompatible.org/story/fedora-45-final-freeze-october-20-release-date-set-as-trackers-clear/)
87. [Kubernetes 1.34 End of Life: What Actually Happens on EKS, GKE, and AKS - DEV Community](https://dev.to/skyhook-radar/kubernetes-134-end-of-life-what-actually-happens-on-eks-gke-and-aks-g8e)
88. [Kubernetes End of Life (EOL) Dates and End of Support (EOS) Dates](https://eosl.date/eol/product/kubernetes/)
89. [Podman 6 Is Here, But Treat It Like a Migration](https://medium.com/@u.mair/podman-6-is-here-but-treat-it-like-a-migration-4a8d1be8e3b4)
90. [systemd 260 Released: mstack, SysV Service Scripts Removed & AI Agents Documentation - Phoronix](https://www.phoronix.com/news/systemd-260-Released)
91. [Bash (Unix shell)](<https://en.wikipedia.org/wiki/Bash_(Unix_shell)>)
92. [Ubuntu 26.04: Release Date and New Features in Resolute Raccoon - LinuxConfig](https://linuxconfig.org/ubuntu-26-04-release-date-and-new-features-in-resolute-raccoon)
