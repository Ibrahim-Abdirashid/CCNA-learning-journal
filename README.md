# CCNA Learning Journal — Af-Soomaali 🌐📚

> **Casharrada CCNA 200-301 iyo labs-ka Packet Tracer — oo dhammaan Af-Soomaali lagu qoray.**
>
> 🌐 Website (mobile-ka ka akhri): **<https://ibrahim-abdirashid.github.io/CCNA-learning-journal/>**
>
> Waxaan repo-gan u qoray dhalinyarada Soomaaliyeed ee baranaysa networking. Cashar walba waa sida aan naftayda u fahmay, oo aan ku sharaxay af fudud, iyadoo erayada farsamada (VLAN, subnet, trunk…) Ingiriisi lagu hayay si imtixaanka loo fahmo. Lab walba waxaad heli kartaa faylka `.pkt`, sawirka topology-ga, IP-yada, tallaabooyinka iyo `running-config`-ga.

[![License: CC BY-SA 4.0](https://img.shields.io/badge/Casharrada-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE.md)
[![Tools: MIT](https://img.shields.io/badge/Tools-MIT-blue.svg)](LICENSE.md)
![Casharro](https://img.shields.io/badge/Casharro-29-green)
![Labs](https://img.shields.io/badge/Labs%20Packet%20Tracer-27-orange)

---

## 🚀 Sida loo isticmaalo

1. **Bilow qaybta 01** oo hoos u sii soco — casharradu waa isku xigxig.
2. Cashar walba dhammaadkiisa waxaa ku qoran **labs-ka la xiriira** — fur faylka `.pkt` Packet Tracer (8.2 ama ka sare), akhri `README.md`-ga lab-ka, raac tallaabooyinka, kadibna `show` commands-ka ku xaqiiji.
3. Wax aad fahmi weyday ama khalad aad aragtay? **Fur Issue** — ama toos u sax oo Pull Request soo dir ([sida](CONTRIBUTING.md)).
4. Packet Tracer ma haysatid? Lab walba `configs/` waxaa ugu jira `running-config`-ga qalab walba — waad akhrin kartaa adigoon PT furin.

---

## 📁 Qaab-dhismeedka

```
CCNA-learning-journal/
├── 01-network-fundamentals/   Asaaska: IOS modes, config files, OSI, Layer 1
├── 02-ip-addressing/          IP addressing, subnetting, IPv6
├── 03-switching/              VLAN, trunk, VTP, inter-VLAN, STP, EtherChannel
├── 04-routing/                Routing, static routing, OSPF
├── 05-device-management/      Telnet, SSH, CDP/LLDP
├── 06-ip-services/            NAT iyo DHCP
├── labs/                      27 lab Packet Tracer (.pkt + README + topology + configs)
├── images/                    Sawirrada casharrada
└── tools/                     Scripts-ka repo-gan lagu dhisay (pkt → xml/svg, OneNote → md)
```

---

## 📖 Casharrada (Table of Contents)

### 🔷 01 — Asaaska Shabakadaha (Network Fundamentals)

| # | Casharka | Waxa uu ka hadlayo |
|---|---|---|
| 1 | [Cisco Command Hierarchy](01-network-fundamentals/01-cisco-command-hierarchy.md) | Mode-yada IOS: user EXEC, privileged, global config, sub-modes |
| 2 | [Configuration Files](01-network-fundamentals/02-configuration-files.md) | running-config iyo startup-config, `copy run start` |
| 3 | [Basic Configuration Commands](01-network-fundamentals/03-basic-configuration-commands.md) | hostname, passwords, banner, `no shutdown`, save |
| 4 | [OSI Model](01-network-fundamentals/04-osi-model.md) | 7-da lakab iyo shaqada mid walba |
| 5 | [Physical Layer / Layer 1](01-network-fundamentals/05-physical-layer.md) | Xadhkaha, ports, media |

### 🔷 02 — Cinwaannada IP (IP Addressing)

| # | Casharka | Waxa uu ka hadlayo |
|---|---|---|
| 1 | [IP Address Configuration on Network Devices](02-ip-addressing/01-ip-address-configuration.md) | IP-ga router, switch (SVI) iyo PC |
| 2 | [Configuring IP Addresses](02-ip-addressing/02-configuring-ip-addresses.md) | Tallaabo-tallaabo Packet Tracer |
| 3 | [Subnetting — Qaybta 1](02-ip-addressing/03-subnetting.md) | Subnet mask, network/broadcast, xisaabta |
| 4 | [Subnetting — Qaybta 2](02-ip-addressing/04-subnetting-part-2.md) | VLSM iyo tusaalooyin |
| 5 | [IPv6 Addressing](02-ip-addressing/05-ipv6-addressing.md) 📝 | Qaabka, soo gaabinta, GUA/link-local, /64, SLAAC |

### 🔷 03 — Switching

| # | Casharka | Waxa uu ka hadlayo |
|---|---|---|
| 1 | [LAN Switching](03-switching/01-lan-switching.md) | Sida switch-ku MAC table u dhiso |
| 2 | [VLAN — waxa ay tahay inaad fahanto](03-switching/02-vlan-introduction.md) | Access / trunk / dynamic ports, DTP |
| 3 | [VLANs](03-switching/03-vlans.md) | Abuurista VLAN-yada iyo access ports |
| 4 | [VLAN Trunking — Switch L2](03-switching/04-vlan-trunking.md) | 802.1Q, native VLAN |
| 5 | [VLAN Trunk — Layer 3 Switch](03-switching/05-vlan-trunk-layer3-switch.md) | Sababta trunk loo baahan yahay, dot1q encapsulation |
| 6 | [VTP — VLAN Trunking Protocol](03-switching/06-vtp.md) | Server / client / transparent, revision number |
| 7 | [Inter-VLAN Routing — guud](03-switching/07-intervlan-routing-overview.md) | ROAS vs Layer 3 switch |
| 8 | [Router on a Stick (ROAS)](03-switching/08-router-on-a-stick.md) | Sub-interfaces, `encapsulation dot1Q` |
| 9 | [Inter-VLAN — Layer 3 Switch](03-switching/09-intervlan-layer3-switch.md) | SVI, `ip routing` |
| 10 | [Spanning Tree Protocol & RSTP](03-switching/10-spanning-tree-rstp.md) | Loops, root bridge, port states |
| 11 | [EtherChannel — Layer 2](03-switching/11-etherchannel.md) | Static, PAgP, LACP |

### 🔷 04 — Routing

| # | Casharka | Waxa uu ka hadlayo |
|---|---|---|
| 1 | [Routing — Hordhac](04-routing/01-routing-introduction.md) | IPv4 header, routing table, best path, directly connected / static / dynamic |
| 2 | [Static Routing](04-routing/02-static-routing.md) | `ip route`, next-hop vs exit interface, default route |
| 3 | [OSPF](04-routing/03-ospf.md) 📝 | Neighbors, LSDB, router-id, area, wildcard, DR/BDR, single & multi-area |

### 🔷 05 — Maamulka Qalabka (Device Management)

| # | Casharka | Waxa uu ka hadlayo |
|---|---|---|
| 1 | [Telnet & SSH](05-device-management/01-telnet-and-ssh.md) | Local vs remote management, port 23 / 22 |
| 2 | [SSH (Secure Shell)](05-device-management/02-ssh.md) | RSA keys, `login local`, `transport input ssh` |
| 3 | [CDP iyo LLDP](05-device-management/03-cdp-lldp.md) 📝 | Deriska garasho, `show cdp neighbors`, amniga |

### 🔷 06 — Adeegyada IP (IP Services)

| # | Casharka | Waxa uu ka hadlayo |
|---|---|---|
| 1 | [NAT](06-ip-services/01-nat.md) 📝 | Inside/outside, static, dynamic, PAT overload |
| 2 | [DHCP](06-ip-services/02-dhcp.md) 📝 | DORA, router DHCP server, pools, `ip helper-address` |

📝 = **draft**: cashar la qoray oo weli dib loo eegayo — haddii aad khalad aragto Issue fur.

### ⏳ Casharro soo socda

ACL · Port Security · DHCP Snooping · Wireless · EIGRP · Network Automation.

---

## 🧪 Labs — Packet Tracer

Liiska buuxa iyo sharaxaadda: **[labs/README.md](labs/README.md)**

| # | Lab | Heerka |
|---|---|---|
| 01 | [Telnet](labs/01-telnet/README.md) | Bilow |
| 02 | [SSH](labs/02-ssh/README.md) | Bilow |
| 03 | [VLAN-yada iyo Access Ports](labs/03-vlan-access-ports/README.md) | Bilow |
| 04 | [VLAN Trunk (802.1Q)](labs/04-vlan-trunk/README.md) | Bilow |
| 05 | [VTP — Server iyo Client](labs/05-vtp-server-client/README.md) | Dhexe |
| 06 | [VTP — Server, Client iyo Transparent](labs/06-vtp-transparent/README.md) | Dhexe |
| 07 | [Inter-VLAN Routing — Layer 3 Switch](labs/07-intervlan-layer3-switch/README.md) | Dhexe |
| 08 | [Inter-VLAN L3 Switch — Practice 2](labs/08-intervlan-layer3-switch-practice-2/README.md) | Dhexe |
| 09 | [EtherChannel — Static](labs/09-etherchannel-static/README.md) | Dhexe |
| 10 | [EtherChannel — PAgP](labs/10-etherchannel-pagp/README.md) | Dhexe |
| 11 | [EtherChannel — LACP](labs/11-etherchannel-lacp/README.md) | Dhexe |
| 12 | [CDP iyo LLDP](labs/12-cdp-lldp/README.md) | Bilow |
| 13 | [IPv6 Addressing](labs/13-ipv6-addressing/README.md) | Dhexe |
| 14 | [Static Routing — IPv4 iyo IPv6](labs/14-static-routing-ipv4-ipv6/README.md) | Dhexe |
| 15 | [OSPF Single Area](labs/15-ospf-single-area/README.md) | Dhexe |
| 16 | [OSPF Multi-Area — Hargeysa, Boorama, Burco, Berbera](labs/16-ospf-multi-area-somaliland/README.md) | Sare |
| 17 | [NAT — Static](labs/17-nat-static/README.md) | Dhexe |
| 18 | [NAT — Dynamic](labs/18-nat-dynamic/README.md) | Dhexe |
| 19 | [NAT — PAT / Overload](labs/19-nat-pat-overload/README.md) | Dhexe |
| 20 | [CCNA2 Lab Activity 1 — VLSM, DHCP, SSH, IPv6](labs/20-lab-activity-1-vlsm-dhcp-ssh/README.md) | Sare |
| 21 | [CCNA2 Lab Activity 2 — VLANs, Trunk, VTP](labs/21-lab-activity-2-vlans-trunk-vtp/README.md) | Sare |
| 22 | [CCNA2 Lab Activity 3 — Inter-VLAN MLS](labs/22-lab-activity-3-intervlan-mls/README.md) | Sare |
| 23 | [Capstone — EtherChannel, VLANs, ROAS, DHCP, SSH, Static](labs/23-capstone-etherchannel-vlans-dhcp-ssh-static/README.md) | Sare |
| 24 | [IP Address Configuration — Router, Switch, PC (Day 10)](labs/24-ip-configuration-basics/README.md) | Bilow |
| 25 | [Routing Part 1 — Directly Connected (Day 12)](labs/25-routing-directly-connected/README.md) | Bilow |
| 26 | [Network Design — HQ, Servers, Burco + Static Routing](labs/26-network-design-static-routing/README.md) | Dhexe |
| 27 | [Daheeye University — EIGRP, ROAS, DHCP, EtherChannel, SSH (4 campus)](labs/27-eigrp-daheeye-university/README.md) | Sare |

Lab walba wuxuu leeyahay:

- `NN-magac.pkt` — faylka Packet Tracer
- `README.md` — ujeeddo, topology, jadwalka IP-yada, VLAN/VTP, xiriirinta, tallaabooyinka, xaqiijinta, fiiro gaar ah
- `topology.svg` — sawirka topology-ga (si toos ah ayaa faylka looga soo saaray)
- `configs/*.txt` — `running-config`-ga qalab walba

---

## 📋 Xaaladda (Status)

| Qaybta | Xaaladda |
|---|---|
| 01 — Network Fundamentals | ✅ 5 cashar |
| 02 — IP Addressing | ✅ 4 cashar + 1 draft (IPv6) |
| 03 — Switching | ✅ 11 cashar |
| 04 — Routing | ✅ 2 cashar + 1 draft (OSPF) |
| 05 — Device Management | ✅ 2 cashar + 1 draft (CDP/LLDP) |
| 06 — IP Services | 📝 2 draft (NAT, DHCP) |
| Labs | ✅ 27 lab |
| ACL, Port Security, Wireless | ⏳ Soo socda |

---

## 🤝 Ka qaybgal

Repo-gan waa mid furan. Haddii aad tahay arday Soomaali ah oo CCNA baranaya:

- **Akhri, tijaabi, su'aal weydii** — Issues-ka waa loo furan yahay su'aalaha.
- **Sax khaladaadka** — af ama farsamo, Pull Request soo dir.
- **Ku dar cashar ama lab** — eeg [CONTRIBUTING.md](CONTRIBUTING.md).
- **La wadaag** saaxiibbadaa iyo groups-ka IT-ga.

---

## ⚠️ Ogeysiis (Disclaimer)

- Qoraalladan waa **qoraallo barasho shakhsi ah**; waxay kaabayaan, kuma beddelayaan buugaagta rasmiga ah ee Cisco iyo koorsada NetAcad.
- Repository-gan **ma xidhna Cisco Systems, Inc.**, mana aha mid ay Cisco ansixisay. Cisco, IOS, Packet Tracer iyo CCNA waa calaamado ganacsi oo Cisco leedahay.
- Faylasha Cisco NetAcad (PDF-yada modules-ka, `.pka`) **laguma soo gelin** repo-gan sababo copyright ah.

## 📜 License

Casharrada iyo labs-ka: [CC BY-SA 4.0](LICENSE.md) — wadaag, wax ka beddel, laakiin magaca xus oo isla license-ka ku wadaag.
Scripts-ka `tools/`: [MIT](LICENSE.md).

## 📬 Xiriir

**Ibrahim Abdirashid** — arday CCNA. Su'aalo, talooyin, ama iskaashi: fur **Issue** GitHub-ka.

---

*Cusbooneysiinta ugu dambeysay: Sebtembar 2026 · CCNA 200-301 · Af-Soomaali*
