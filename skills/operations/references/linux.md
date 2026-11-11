# Linux

Read this for running or fixing a Linux host: choosing a distribution or planning an upgrade by
its support window, a service that won't start, a full disk, a slow host, updates and held
packages, sudo and SSH hardening, a permission or SELinux or AppArmor denial, a failed boot after
an update, clock drift, and backups.

Writing the scripts is coding's bash-coding and bash-security. Containers are docker-containers;
firewalls and VPNs are networking-security; Windows hosts are windows-admin. Deploying is
git-workflows' ci-cd. Gaming on Linux is linux-gaming, on request.

## Rules

1. **Know each host's support window, and upgrade before it ends.** Choose a release with years
   left, and move one release at a time with the distribution's own tool.
2. **Troubleshoot in order: what changed, the logs, then resources.** Read-only commands first.
   Change one thing at a time, and write down each change.
3. **Change a unit with `systemctl edit`, never in the vendor's file.** A drop-in survives
   package updates, and `systemctl revert` undoes it.
4. **Security updates install themselves; the rest is planned.** Hold a package only with a
   reason and a date to lift it.
5. **Test SSH and sudo configuration before it takes effect, with a session still open:** keys,
   no root login, no passwords.
6. **Fix a denial; never switch the control off.** Narrow permissions, never `chmod 777`. For
   SELinux or AppArmor, read the denial and fix the label, boolean or profile.
7. **Free disk space by finding what grew,** and delete nothing you haven't identified.
8. **Run one time-sync daemon.**
9. **A backup counts once it has been restored.**

### Support periods

| Distribution | Window | When it ends |
|---|---|---|
| Ubuntu LTS | Five years, more with Ubuntu Pro; interim releases nine months | 22.04 ends May 2027 (fact `linux-ubuntu`) |
| Debian | Three years, then two of LTS | 13 in 2030; 12, now in LTS, in 2028 (facts `linux-debian-13`, `linux-debian-12`) |
| RHEL | Ten years over three phases (fact `linux-rhel`) | Each rebuild publishes its own dates (fact `linux-alma`) |
| Fedora | About 13 months (fact `linux-fedora`) | Upgrade every release or every other one |

A rebuild such as AlmaLinux ends each minor release when the next ships: stay on the latest.
Before an upgrade, test a restore, read the release notes, and upgrade a copy first.

### Troubleshooting order

```bash
# Read-only. What changed, then logs, then resources.
less /var/log/apt/history.log      # or: dnf history list
systemctl --failed
journalctl -u nginx.service -b --no-pager | tail -n 50
journalctl -b -1 -p err --no-pager # the boot before this one
df -h; df -i                       # space and inodes
free -h; uptime                    # memory, load
sudo dmesg --level=err,warn | tail -n 30   # OOM kills, disk and driver errors
```

`journalctl -b -1` needs a persistent journal, which `auto` keeps only once `/var/log/journal`
exists (fact `linux-journal`). Create it before you need last night's boot.

### systemd

- `sudo systemctl edit nginx.service` writes a drop-in and reloads systemd (fact
  `linux-systemctl-edit`). `systemctl cat` shows the result.
- A service that keeps dying: `systemctl status` for its exit code, then its journal.
- Write a native unit, never a SysV init script: systemd 260 dropped them (fact `linux-sysv`).

```ini
# /etc/systemd/system/nginx.service.d/override.conf
[Service]
Restart=on-failure
RestartSec=5s
```

### Packages and updates

- Ubuntu installs security updates by default (fact `linux-unattended`). On Debian, install
  `unattended-upgrades`; on RHEL and Fedora, `dnf-automatic` set to security updates (fact
  `linux-dnf-automatic`).
- Preview before you apply: `apt list --upgradable`, `dnf check-update`.
- Hold with `sudo apt-mark hold <pkg>` or `sudo dnf versionlock add <pkg>` (a plugin on DNF 4).
  Record why and when it lifts: a held package gets no security fixes.

### Users, sudo and SSH

- One account per person, in the `sudo` or `wheel` group. Edit sudoers with `visudo`, which
  checks syntax before it saves; a broken file locks out sudo.
- Put SSH settings in a file under `/etc/ssh/sshd_config.d/`. The first value read wins (fact
  `linux-sshd`): where the main file includes the drop-ins at its top, they beat its own lines,
  and the first in sort order beats the rest:

```text
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
```

- Then `sudo sshd -t` to check, `sudo sshd -T` to read what applies (fact `linux-sshd-test`),
  and reload the service (`ssh` on Debian and Ubuntu, `sshd` elsewhere). Open a second session
  and log in before closing the first.

### Permissions, SELinux and AppArmor

- Fix ownership with `chown`, and grant the least mode that works: `640` for a secret file.
- SELinux: `ausearch -m avc -ts recent` shows the denial. Restore labels with `restorecon -Rv`,
  set a boolean with `setsebool -P`, and label a new path with `semanage fcontext`. Disabling it
  leaves new files unlabeled (fact `linux-selinux`).
- AppArmor: `aa-status`, and the denial in the journal. `aa-complain` logs instead of blocking,
  for one profile while you fix it; then `aa-enforce`.

### Disk full

```bash
sudo du -xh --max-depth=1 /var | sort -h | tail -n 15   # what grew
sudo lsof +L1                    # deleted files still held open
journalctl --disk-usage
sudo journalctl --vacuum-size=500M
```

A deleted file a process holds keeps its space until the process restarts. ext4 reserves 5% for
root (fact `linux-ext4`), so root can still log in and clean up. Full inodes look like a full
disk with space left: `df -i` tells them apart.

### Boot, time and backups

- Keep the previous kernel: if an update won't boot, choose it in the boot menu, then read
  `journalctl -b -1`. A driver built for the kernel, such as a GPU driver, loads under Secure
  Boot only once its key is enrolled with `mokutil`.
- Time: `timedatectl` should say the clock is synchronized. Ubuntu moved to chrony in 25.10 (fact
  `linux-chrony`), and an upgraded host may still run timesyncd; never run two daemons.
- Backups follow 3-2-1: three copies, two media, one off site. Restore one to a scratch
  directory on a schedule, and compare it with the source.

## Mistakes

- **"Just disable SELinux."** It hides the fault and drops the protection. Read the denial and
  fix the label or boolean; at most, make one domain permissive.
- **Reloading `sshd` without `sshd -t` and an open second session.** One typo locks everyone
  out of a remote host.
- **Editing `/usr/lib/systemd/system/*.service`.** The next package update overwrites it. Use
  `systemctl edit`.
- **`rm` on a log a process holds open.** The space stays used. Truncate it or restart the
  process, and fix rotation.
- **Rebooting or reinstalling before reading the logs.** That loses the evidence.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Release past its standard support | `/etc/os-release` against the facts | `BLOCKER` past it, `GAP` within a year | Upgrade, or buy extended support |
| SysV init scripts on systemd 260 or later | `ls /etc/init.d`, `systemctl --version` | `BLOCKER` | A native unit (fact `linux-sysv`) |
| Failed units | `systemctl --failed` | `GAP` | Fix the cause its journal names |
| Security updates not automatic | `systemctl list-timers` for `apt-daily-upgrade` or `dnf-automatic` | `GAP` | Turn them on (facts `linux-unattended`, `linux-dnf-automatic`) |
| Holds with no recorded reason | `apt-mark showhold`, `dnf versionlock list` | `DRIFT` | Record or lift each |
| Root or password SSH login | `sshd -T`, for `permitrootlogin` and `passwordauthentication` | `BLOCKER` when reachable from the internet | Keys only, root off |
| SELinux or AppArmor off | `getenforce`, `aa-status` | `GAP` | Re-enable, permissive first; fix denials |
| Disk or inodes past 90% | `df -h`, `df -i` | `GAP` | Find what grew; fix rotation |
| Clock unsynchronized | `timedatectl` | `GAP` | One daemon, enabled |
| Backups never restored | A dated restore record | `GAP` | Restore one and record it |

## Why

### Support periods

**The advice:** an LTS or stable release, upgraded before standard support ends. **The
reason:** past its end a release gets no security fixes, and skipping releases is untested.
**Others:** Fedora trades a 13-month life for new software; the rebuilds keep RHEL's ten years.
**Cost:** an LTS ships older software. **Choose differently** for a workstation or test host.

### Troubleshooting order

**The reason:** most outages follow a change, and the logs usually name it. A reboot or a guess
first destroys the evidence. **Cost:** minutes of reading during an outage. **Choose
differently** when data is at risk: stop the damage, then read.

### Drop-ins, updates and holds

A vendor file is replaced on update; a drop-in is the documented place for local changes.
Automatic security updates close a known hole within a day, at the risk of one that breaks,
which Ubuntu judges the smaller risk (fact `linux-unattended`). A hold reverses that trade for
one package, so it needs an end.

### SSH, sudo and mandatory access control

Keys can't be guessed, and with root login off every action has a named user. Test first,
because SSH is often the only way in; a lost key then needs the console. Fedora recommends
permissive over disabled SELinux (fact `linux-selinux`), because files made while it's off go
unlabeled. Permissive for one domain is the narrow exception while a policy is fixed.

### Disk, time and backups

A full disk stops writes, logs and logins at once, so finding the cause beats deleting. Two time
daemons fight, and a skewed clock breaks TLS, Kerberos and log order. A backup never restored
fails in ways that show only at restore: missing paths, lost keys. This is our own practice.

## Facts

Versions, dates and defaults, each named elsewhere by its ID. Checked 2026-11-11.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `linux-ubuntu` | Ubuntu LTS: five years; interims nine months; 22.04 ends May 2027 | [Ubuntu release cycle](https://ubuntu.com/about/release-cycle) | "LTS are released every two years and receive 5 years of standard security maintenance." and "with only 9 months of updates" and "Ubuntu 22.04 LTS Released: Apr 2022 Standard security maintenance May 2027" | 2026-11-11 | 2027-02-11 |
| `linux-debian-13` | Debian 13: full to 2028-08-09, LTS to 2030-06-30 | [Debian trixie](https://www.debian.org/releases/trixie/) | "the initial three years of full Debian support, until August 9th, 2028, and two years of Long Term Support (LTS), until June 30th, 2030" | 2026-11-11 | 2027-02-11 |
| `linux-debian-12` | Debian 12: full ended 2026-07-11, LTS to 2028-06-30 | [Debian bookworm](https://www.debian.org/releases/bookworm/) | "until July 11th, 2026, and two years of Long Term Support (LTS), until June 30th, 2028" | 2026-11-11 | 2027-02-11 |
| `linux-rhel` | RHEL 8, 9 and 10: ten-year life cycle | [RHEL life cycle](https://access.redhat.com/support/policy/updates/errata) | "Red Hat Enterprise Linux versions 8, 9, and 10 deliver a ten-year life cycle" | 2026-11-11 | 2027-02-11 |
| `linux-alma` | AlmaLinux 10: active to 2030-05-31, security to 2035-05-31; minors end at the next | [AlmaLinux release notes](https://wiki.almalinux.org/release-notes/) | "Version 10 will have active support until 31 May 2030, and security support until 31 May 2035." and "Each minor version reaches end of life when the new version is released." | 2026-11-11 | 2027-02-11 |
| `linux-fedora` | Fedora: about 13 months; release N ends four weeks after N+2 | [Fedora life cycle](https://docs.fedoraproject.org/en-US/releases/lifecycle/) | "for approximately 13 months" and "is supported until four weeks after the release of" | 2026-11-11 | 2027-02-11 |
| `linux-sysv` | systemd 260 removed SysV service scripts | [systemd NEWS, v260](https://raw.githubusercontent.com/systemd/systemd/v260/NEWS) | "Support for System V service scripts has been removed." | 2026-11-11 | 2027-02-11 |
| `linux-systemctl-edit` | `systemctl edit` writes a drop-in and reloads | [systemctl(1)](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) | "Edit or replace a drop-in snippet or the main unit file, to extend or override the definition of the specified unit." and "After the editing is finished, configuration is reloaded" | 2026-11-11 | 2027-05-11 |
| `linux-journal` | `Storage=auto` persists only if `/var/log/journal` exists | [journald.conf(5)](https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html) | "if the /var/log/journal directory exists" | 2026-11-11 | 2027-05-11 |
| `linux-sshd` | The first value wins; root login defaults to `prohibit-password` | [sshd_config(5)](https://man.openbsd.org/sshd_config.5) | "for each keyword, the first obtained value will be used." and "The default is prohibit-password" | 2026-11-11 | 2027-05-11 |
| `linux-sshd-test` | `sshd -t` checks; `sshd -T` prints the effective configuration | [sshd(8)](https://man.openbsd.org/sshd.8) | "Only check the validity of the configuration file and sanity of the keys." and "output the effective configuration to stdout" | 2026-11-11 | 2027-05-11 |
| `linux-unattended` | Ubuntu applies security updates by default | [Ubuntu automatic updates](https://ubuntu.com/server/docs/how-to/software/automatic-updates/) | "Ubuntu will apply security updates automatically, without user interaction." and "less than the risk of NOT applying a security update" | 2026-11-11 | 2027-05-11 |
| `linux-dnf-automatic` | `dnf-automatic` can apply security advisories only | [DNF Automatic](https://dnf.readthedocs.io/en/latest/automatic.html) | "security only those with an issued security advisory" | 2026-11-11 | 2027-05-11 |
| `linux-selinux` | Fedora recommends permissive over disabling SELinux | [Fedora: SELinux modes](https://docs.fedoraproject.org/en-US/quick-docs/selinux-changing-states-and-modes/) | "It is recommended to use permissive mode instead of permanently disabling SELinux." and "File-system objects created while SELinux is disabled are not labeled at all." | 2026-11-11 | 2027-05-11 |
| `linux-ext4` | ext4 reserves 5% for root by default | [mke2fs(8)](https://man7.org/linux/man-pages/man8/mke2fs.8.html) | "The default percentage is 5%." | 2026-11-11 | 2027-05-11 |
| `linux-chrony` | Ubuntu uses chrony by default since 25.10 | [Ubuntu: time synchronization](https://ubuntu.com/server/docs/explanation/networking/about-time-synchronisation/) | "Since Ubuntu 25.10 chrony is used to synchronize time by default." | 2026-11-11 | 2027-02-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Ubuntu](https://ubuntu.com/about/release-cycle) release cycle and server docs | Support, updates, time | © Canonical: our own words, short quotes |
| [Debian releases](https://www.debian.org/releases/) | Support dates | MIT (Expat) or GPL-2.0+: short quotes |
| [Red Hat](https://access.redhat.com/support/policy/updates/errata), [AlmaLinux](https://wiki.almalinux.org/release-notes/) | RHEL and rebuilds | © Red Hat; AlmaLinux not stated: short quotes |
| [Fedora Docs](https://docs.fedoraproject.org/) | Life cycle, SELinux | CC BY-SA 4.0: brief quotes with attribution |
| [systemd](https://www.freedesktop.org/software/systemd/man/latest/), [DNF](https://dnf.readthedocs.io/) | Units, journal, SysV, updates | Not stated on the page: short quotes |
| [OpenBSD](https://man.openbsd.org/sshd_config.5), [man7.org](https://man7.org/linux/man-pages/) manuals | SSH, ext4 | Each page's own terms: short quotes |
| This repository's practice | Troubleshooting order, restores, 3-2-1 | Our own words |
