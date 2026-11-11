# Networking security

Read this for securing a home, small office or modest enterprise network: firewall rules
(nftables, Windows Defender Firewall) and changing them remotely without a lockout, VLANs for
IoT and guests, an IDS, a VPN, Wi-Fi, encrypted and filtering DNS, reaching a service from
outside without a port forward, and capturing traffic.

The host itself, its services and SSH, is `linux`; Windows Server roles and Group Policy are
`windows-admin`; container networks and published ports are `docker-containers`. Scripts are the
`coding` skill's shell and PowerShell modules. This module is defensive only: no scanning or
capture on networks you aren't authorized to inspect, and no attack tools.

## Rules

1. **Deny by default, and write each allow down.** Inbound is dropped unless a rule allows it.
   Each rule's comment names who needs it, its owner and its last review. Delete what nobody
   claims.
2. **Filter IPv4 and IPv6 together.** Use one nftables table of the `inet` family (fact
   `net-nft-inet`), and allow the ICMPv6 that IPv6 can't work without (fact `net-icmpv6`).
3. **On Linux, write rules in nftables** (fact `net-nftables`): one file, checked with `nft -c`
   (fact `net-nft-check`), loaded in one transaction with `nft -f` (fact `net-nft-atomic`). One
   tool owns each host's rules: nftables, firewalld or ufw.
4. **On Windows, keep Windows Defender Firewall on in every profile.** It blocks unsolicited
   inbound by default (fact `net-windows-default`). Scope each rule with `-RemoteAddress`, and
   deploy by Group Policy where there's a domain.
5. **Change a remote firewall with a way back that runs without you.**
6. **Segment by trust:** IoT, guests and management each on a VLAN, with traffic between them
   dropped unless a rule allows it.
7. **Never port-forward an admin interface.** Reach it over a VPN or a zero-trust access proxy
   (facts `net-bod-23-02`, `net-zta`), and turn off UPnP (fact `net-cisa-home`).
8. **For a VPN, WireGuard first** (fact `net-wireguard`); IPsec (IKEv2) or OpenVPN where a
   peer or the network needs them.
9. **Wi-Fi: WPA3, transition mode only where a device needs it, WPS off** (facts `net-wpa3`,
   `net-cisa-home`).
10. **DNS: one resolver that validates DNSSEC, encrypts upstream and can't be bypassed** (fact
    `net-sp800-81`).
11. **An IDS runs a supported release** (facts `net-suricata`, `net-zeek-lts`), in detection
    mode first.
12. **Capture only where you're authorized, with a filter, and treat the file as a secret.**

### A host rule set

<!-- example: unchecked, no nft checker here; passed nft -c -f (nftables 1.0.9), 2026-11-11 -->
```nft
#!/usr/sbin/nft -f
# Replaces this table only, in one transaction; other tables stay.
table inet host
delete table inet host

table inet host {
  chain input {
    type filter hook input priority filter; policy drop;
    iif "lo" accept
    ct state established,related accept
    ct state invalid drop
    # IPv6 fails without these (RFC 4890).
    icmpv6 type { destination-unreachable, packet-too-big, time-exceeded,
      parameter-problem, nd-router-solicit, nd-router-advert,
      nd-neighbor-solicit, nd-neighbor-advert, echo-request } accept
    icmp type { destination-unreachable, time-exceeded, echo-request } accept
    ip saddr 192.0.2.0/24 tcp dport 22 accept comment "SSH, mgmt; owner ops; 2026-11-11"
    limit rate 10/minute log prefix "host drop: "
  }
}
```

### Applying it remotely

Keep your session open. If the new rules cut you off, the timer restores the old ones.

```bash
sudo nft list ruleset | sudo tee /root/nftables.good >/dev/null
sudo nft -c -f /etc/nftables.conf
sudo systemd-run --unit=fw-rollback --on-active=5min \
  /bin/sh -c 'nft flush ruleset && nft -f /root/nftables.good'
sudo nft -f /etc/nftables.conf
# Open a NEW session now. Only once it works:
sudo systemctl stop fw-rollback.timer
```

With firewalld, try a rule in the runtime set with `--timeout` (fact `net-firewalld-timeout`),
then add it with `--permanent`. On Windows, run `New-NetFirewallRule` with `-WhatIf` first,
then for real, and test from a second session. Change a router from a wired management port.

### Segments

| Segment | May reach | Reached by |
|---|---|---|
| Management | Everything | Nothing |
| Trusted | Internet, printers, named servers | Management |
| IoT | Internet, its hub | Trusted, on the app's ports |
| Guest | Internet only | Nothing |

Casting across VLANs needs an mDNS reflector: a hole, so allow named devices only.

### VPN, Wi-Fi, DNS, IDS and capture

- **WireGuard:** generate each key on its device with `umask 077`, one key per device, and keep
  each peer's `AllowedIPs` to the addresses it owns.
- **Wi-Fi:** a long passphrase, PMF required, guests and WPA2-only devices each on their own
  SSID. With RADIUS, WPA3-Enterprise (802.1X).
- **DNS:** a local filtering resolver (Pi-hole, AdGuard Home, Unbound) forwarding over DNS over
  TLS or HTTPS to an upstream that validates DNSSEC. Block outbound 53 and 853 except from the
  resolver; DNS over HTTPS can't be blocked by port, so set managed browsers' DNS policy.
- **IDS:** Zeek logs connections, DNS and TLS; Suricata alerts on signatures, or blocks
  inline. Feed it a mirror port, or run it on the router.
- **Capture:** `sudo tcpdump -i eth0 -w /tmp/cap.pcap -C 100 -W 5 'host 192.0.2.10'`, read in
  Wireshark. A capture holds passwords and cookies: share only the filtered part, and delete it
  once answered.

## Mistakes

- **`flush ruleset` in a host's firewall file.** It deletes the rules Docker, libvirt or
  firewalld wrote. Replace your own table, as above.
- **`policy drop` on a `forward` chain on a container host.** A drop in any base chain is final,
  so every container goes dark. Leave forwarding to `docker-containers`.
- **Trusting ufw to guard a published container port.** Docker's rules route it first (fact
  `net-docker-ufw`). Bind the port to `127.0.0.1`.
- **Dropping all ICMP.** IPv6 loses neighbor discovery, and path MTU failures look like hung
  connections (fact `net-icmpv6`).
- **Forwarding a port to RDP, a NAS, a camera or the router's admin page,** "for now".
- **Recommending Snort 2 or Suricata 7.** Neither gets fixes (facts `net-snort2-eol`,
  `net-suricata7-eol`).
- **Leaving WPS on because nobody uses the PIN.** The router answers PIN guesses anyway (fact
  `net-cisa-home`).
- **One WireGuard key shared by several devices.** Revoking it cuts all of them off.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Admin interface on the internet | Router port forwards and UPnP table; your public address scanned from outside | `BLOCKER` | Remove it; use the VPN |
| Inbound default | Input chain policy; `Get-NetFirewallProfile` `Enabled`, `DefaultInboundAction` | `BLOCKER` where it accepts | `policy drop`; firewall on |
| IPv6 filtered | Only `ip`-family tables, on hosts with IPv6 addresses | `GAP` | One `inet` table |
| Rules nobody claims | No comment, owner or review date | `DRIFT` | Ask, then remove or document |
| Two tools own one host | iptables scripts beside nftables, or ufw beside firewalld | `DRIFT` | Pick one |
| IoT and guests unsegmented | One VLAN, or inter-VLAN traffic allowed | `GAP` | The segment table |
| Wi-Fi | WPA2-only, TKIP, WPS on, PMF off | `GAP` | WPA3, WPS off, PMF required |
| Resolver bypass | Outbound 53 or 853 open from clients | `GAP` | Allow only the resolver |
| IDS release | Suricata 7, Snort 2, Zeek out of support | `DRIFT` | Upgrade |

## Why

### Default deny, written down

- **The advice:** drop by default; each allow has a reason, an owner and a review date.
- **The reason:** an allow outlives its need, and with no owner nobody dares remove it.
- **What others do, and why:** Windows blocks unsolicited inbound and allows outbound (fact
  `net-windows-default`).
- **What it costs:** a new service fails until someone writes its rule.
- **When to choose differently:** outbound filtering on every host costs upkeep; start with IoT
  and servers, whose destinations are few.

### A way back that runs without you

- **The advice:** a timer restores the old rules unless you cancel it.
- **The reason:** `nft -f` is atomic, so a syntax error changes nothing, but a valid file with
  the wrong rule applies, and can cut the session that would fix it.
- **What others do, and why:** firewalld's `--timeout`; appliances' anti-lockout rule.
- **When to choose differently:** with an out-of-band console, the console is the way back.

### No port-forwarded admin interfaces

- **The advice:** take the interface off the internet, or put an access proxy in front of it,
  which CISA prefers for federal agencies (fact `net-bod-23-02`).
- **The reason:** a forward hands the device's login and its unpatched bugs to every scanner.
- **What others do, and why:** zero trust grants nothing for being on the network (fact
  `net-zta`) and checks the user and device each time. A VPN is the plain version: the gateway
  is the one exposed service.
- **What it costs:** a client per device, and a gateway to run.
- **When to choose differently:** a public website is exposed on purpose: patch and segment it.

### WireGuard first

- **The reason:** a small configuration and a code base small enough to audit (fact
  `net-wireguard`).
- **What it costs:** UDP only, and keys managed per device, with no user directory.
- **When to choose differently:** an appliance that speaks only IPsec, or users on networks that
  pass only TCP 443, where OpenVPN gets through.

### Wi-Fi, DNS and IDS

- **WPA3, no WPS:** WPA3 requires PMF (fact `net-wpa3`); the WPS PIN falls in halves (fact
  `net-cisa-home`). Transition mode lets WPA2 clients join without WPA3's protections, hence
  their own SSID.
- **One resolver:** filtering, logs and DNSSEC validation in one place, a defense in NIST's
  DNS guide (fact `net-sp800-81`). It's a single point of failure: run two.
- **IDS:** a small network learns more from DNS and firewall logs. Add one when someone reads
  its alerts; blocking before tuning drops legitimate traffic.

## Facts

Checked 2026-11-11, each named above by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `net-nftables` | nftables replaces iptables | [nftables](https://netfilter.org/projects/nftables/) | "nftables replaces the popular {ip,ip6,arp,eb}tables." | 2026-11-11 | 2027-05-11 |
| `net-nft-check` | `nft -c` checks without applying | [nft(8)](https://www.netfilter.org/projects/nftables/manpage.html) | "Check commands validity without actually applying the changes." | 2026-11-11 | 2027-05-11 |
| `net-nft-atomic` | `nft -f` swaps the rule set in one step | [Atomic rule replacement](https://wiki.nftables.org/wiki-nftables/index.php/Atomic_rule_replacement) | "there is no moment when the firewall is partially configured" | 2026-11-11 | 2027-05-11 |
| `net-nft-inet` | An `inet` table filters IPv4 and IPv6 | [Nftables families](https://wiki.nftables.org/wiki-nftables/index.php/Nftables_families) | "Tables of this family see both IPv4 and IPv6 traffic/packets" | 2026-11-11 | 2027-05-11 |
| `net-icmpv6` | Some ICMPv6 must never be dropped | [RFC 4890](https://www.rfc-editor.org/rfc/rfc4890.txt) | "Messages that must not be dropped" | 2026-11-11 | 2027-05-11 |
| `net-firewalld-timeout` | firewalld removes a `--timeout` rule itself | [firewall-cmd](https://firewalld.org/documentation/man-pages/firewall-cmd.html) | "will be removed automatically afterwards" | 2026-11-11 | 2027-05-11 |
| `net-windows-default` | Windows Firewall blocks unsolicited inbound, allows outbound | [Windows Firewall](https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/) | "block all incoming traffic, unless solicited or matching a rule" and "allow all outgoing traffic, unless matching a rule" | 2026-11-11 | 2027-05-11 |
| `net-docker-ufw` | Docker's published ports bypass ufw | [Docker firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/) | "Docker and ufw use firewall rules in ways that make them incompatible with each other." | 2026-11-11 | 2027-02-11 |
| `net-bod-23-02` | CISA: take admin interfaces off the internet, or, preferred, behind a separate access point | [BOD 23-02](https://www.cisa.gov/news-events/directives/binding-operational-directive-23-02) | "Remove the interface from the internet" and "a policy enforcement point separate from the interface itself (preferred action)" | 2026-11-11 | 2027-05-11 |
| `net-zta` | Zero trust grants no trust for location | [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) | "no implicit trust granted to assets or user accounts based solely on their physical or network location" | 2026-11-11 | 2027-05-11 |
| `net-wireguard` | WireGuard aims to be simpler than IPsec | [WireGuard](https://www.wireguard.com/) | "It aims to be faster, simpler, leaner, and more useful than IPsec" | 2026-11-11 | 2027-05-11 |
| `net-wpa3` | WPA3 requires PMF | [Wi-Fi Alliance](https://www.wi-fi.org/discover-wi-fi/security) | "Require use of Protected Management Frames (PMF)" | 2026-11-11 | 2027-05-11 |
| `net-cisa-home` | CISA: turn off WPS, and UPnP when not needed | [CISA: Home network security](https://www.cisa.gov/news-events/news/home-network-security) | "Disable Wi-Fi Protected Setup (WPS)." and "Disable Universal Plug and Play (UPnP) when not needed." | 2026-11-11 | 2027-05-11 |
| `net-sp800-81` | NIST SP 800-81r3 (March 2026) is the DNS guide | [SP 800-81r3](https://csrc.nist.gov/pubs/sp/800/81/r3/final) | "an additional layer of network security" | 2026-11-11 | 2027-05-11 |
| `net-suricata` | Suricata 8.0.8 is current | [Suricata](https://suricata.io/download/) | "Suricata (Stable) version 8.0.8 was released October 29, 2026" | 2026-11-11 | 2027-02-11 |
| `net-suricata7-eol` | Suricata 7 is end of life | [Suricata 7.0.17](https://suricata.io/2026/07/09/suricata-8-0-6-and-7-0-17-released/) | "Suricata 7 has reached EOL." | 2026-11-11 | 2027-05-11 |
| `net-zeek-lts` | Zeek 9.0.1 is the current LTS | [Get Zeek](https://zeek.org/get-zeek/) | "Zeek 9.0.1" | 2026-11-11 | 2027-02-11 |
| `net-snort2-eol` | Open-source Snort 2 is end of life | [Snort blog](https://blog.snort.org/2026/10/end-of-life-announcement-for-open.html) | "open-source Snort2 engine have now formally reached its end-of-life" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [netfilter.org](https://netfilter.org/projects/nftables/), [nftables wiki](https://wiki.nftables.org/) | nftables | Site not stated; wiki GFDL 1.3: short quotes, our own words |
| [firewalld](https://firewalld.org/documentation/) | `--timeout` | Not stated: short quotes |
| [Microsoft Learn](https://learn.microsoft.com/en-us/windows/security/) | Windows Firewall | CC BY 4.0: short quotes, attributed |
| [Docker docs](https://docs.docker.com/engine/network/packet-filtering-firewalls/) | Docker and ufw | All rights reserved: short quotes |
| [RFC 4890](https://www.rfc-editor.org/rfc/rfc4890.txt) | ICMPv6 | IETF Trust (BCP 78): short quotes |
| [CISA](https://www.cisa.gov/news-events/directives/binding-operational-directive-23-02), [NIST](https://csrc.nist.gov/) | Admin interfaces, WPS, UPnP, zero trust, DNS | US government work |
| [WireGuard](https://www.wireguard.com/), [Suricata](https://suricata.io/), [Zeek](https://zeek.org/), [Snort](https://blog.snort.org/) | VPN, IDS releases | Not stated: short quotes |
| [Wi-Fi Alliance](https://www.wi-fi.org/) | WPA3 | All rights reserved: short quotes |
