---
name: operations
description: "Runs, troubleshoots and hardens systems: Windows Server and Active Directory, Linux hosts, Docker images and Compose, and networks (firewalls, VLANs, VPN, Wi-Fi, DNS). Use when administering, fixing or securing servers, containers or networks."
license: Apache-2.0
metadata:
  reviewed: "2026-11-11"
---

# Operations

How to run, troubleshoot and harden the systems code runs on: Windows Server and Active
Directory, Linux hosts, containers, and the networks between them. Scripting itself is
`coding`'s `powershell-scripts` and `bash-coding`, with their security modules; deploying from
CI is `git-workflows`' `ci-cd`; application security is `security`. Reading logs and crash
dumps is a planned module, `log-analysis`, waiting for research; Kubernetes, cloud baselines
and infrastructure as code are planned on request.

## What applies to every module

These summarize the modules; each module holds the commands, the checks and the reasons, so
read the one that fits before answering.

1. **Look before you change.** Read-only commands first: what changed, the logs, then the
   resources.
2. **Every change can be undone or was rehearsed:** a backup, a dry run, `-WhatIf`, a test
   command such as `sshd -t`, and a second session open before touching remote access.
3. **Run supported versions,** and plan each one's end of support a year ahead.
4. **Deny by default and grant the least access,** for accounts, ports, containers and
   networks alike.
5. **Never switch a protection off to make something work:** SELinux, AppArmor, the firewall,
   SMB signing. Find what it blocks and allow that.
6. **A backup counts once it has been restored.**

## Modules

Read the module that fits the request, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources.

| Module | Read it for |
|---|---|
| [`windows-admin`](references/windows-admin.md) | Windows Server and Active Directory: supported versions, tiered admin accounts, Protected Users, LAPS, Group Policy changes, DNS and DHCP, AD CS, file shares and SMB, updates, baselines, PowerShell Remoting and JEA |
| [`linux`](references/linux.md) | Linux hosts across distributions: support windows, troubleshooting in order, systemd units and the journal, updates, SSH and sudo, SELinux and AppArmor, disk full, time sync, and backups |
| [`docker-containers`](references/docker-containers.md) | Dockerfiles, Compose files and images: multi-stage builds, pinned bases, no secrets in layers, non-root and read-only containers, health checks, registries, signing and scanning, and debugging |
| [`networking-security`](references/networking-security.md) | Networks for an office or home: default-deny firewalls applied safely, VLAN segmentation, IDS, WireGuard and other VPNs, WPA3 Wi-Fi, encrypted DNS, exposing services, and packet capture |

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
