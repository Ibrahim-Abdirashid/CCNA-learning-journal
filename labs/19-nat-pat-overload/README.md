# Lab 19 — NAT — PAT / Overload (hal IP, PC badan)

| | |
|---|---|
| **Faylka Packet Tracer** | [`19-nat-pat-overload.pkt`](19-nat-pat-overload.pkt) |
| **Heerka** | Dhexe |
| **Casharka la xiriira** | [01-nat](../../06-ip-services/01-nat.md) |
| **Qalabka** | 3 PC, 1 Switch (L2), 1 Router, 1 Server |

## 🎯 Ujeeddada

PAT (Port Address Translation, *overload*) wuxuu dhammaan PC-yada gudaha ku tarjumaa **hal** IP dibadda ah (IP-ga interface g0/1 = 209.165.201.1) isagoo kala saara *port numbers*. Waa habka guryaha iyo shirkadaha yaryar ku galaan internet-ka.

## 🗺️ Topology

![Topology](topology.svg)

_Sawirkan si toos ah ayaa faylka `.pkt` looga soo saaray; fur faylka Packet Tracer si aad u aragto qaabka rasmiga ah._

## 🔢 Jadwalka IP-yada (IP Addressing Table)

| Qalab | Nooc | Interface | IP Address | Subnet Mask | Default Gateway |
|---|---|---|---|---|---|
| PC0 | PC | NIC | 192.168.10.10 | 255.255.255.0 | 192.168.10.1 |
| PC1 | PC | NIC | 192.168.10.11 | 255.255.255.0 | 192.168.10.1 |
| PC2 | PC | NIC | 192.168.10.12 | 255.255.255.0 | 192.168.10.1 |
| NAT (`R1`) | Router | GigabitEthernet0/0 | 192.168.10.1 | 255.255.255.0 | — |
| NAT (`R1`) | Router | GigabitEthernet0/1 | 209.165.201.1 | 255.255.255.0 | — |
| Server | Server | NIC | 209.165.201.200 | 255.255.255.0 | 209.165.201.1 |

## 🔌 Xiriirinta (Cabling)

| Qalab A | Port | ⟷ | Qalab B | Port |
|---|---|---|---|---|
| PC0 | FastEthernet0 | ⟷ | SW | FastEthernet0/1 |
| PC1 | FastEthernet0 | ⟷ | SW | FastEthernet0/2 |
| PC2 | FastEthernet0 | ⟷ | SW | FastEthernet0/3 |
| SW | GigabitEthernet0/1 | ⟷ | NAT | GigabitEthernet0/0 |
| NAT | GigabitEthernet0/1 | ⟷ | Server | FastEthernet0 |

## ⚙️ Tallaabooyinka Configuration-ka

**1. Inside / outside**

```
R1(config)# interface g0/0
R1(config-if)# ip nat inside
R1(config)# interface g0/1
R1(config-if)# ip nat outside
```

**2. ACL-ka LAN-ka**

```
R1(config)# access-list 1 permit 192.168.10.0 0.0.0.255
```

**3. PAT: interface-ka outside isticmaal (overload)**

```
R1(config)# ip nat inside source list 1 interface g0/1 overload
```

**4. PC0, PC1, PC2 → ping Server 209.165.201.200 isku mar**

## ✅ Sida loo xaqiijiyo (Verification)

- `show ip nat translations` — dhammaan *Inside global* = 209.165.201.1 laakiin port-yo kala duwan (tusaale :1024, :1025)
- `show ip nat statistics` — *Dynamic mappings ... overload*

## 📝 Fiiro gaar ah

- ⚠️ **Faylkan `.pkt` NAT weli laguma habayn** — waxaa ku jira topology-ga iyo IP-yada oo keliya (router-ka `router rip` bannaan ayaa ku jira). Tallaabooyinka kore adigu ku dhammaystir, kadib faylka kaydi.
- Halkii interface, pool-na waa loo isticmaali karaa: `ip nat inside source list 1 pool NAT-POOL overload`.

## 🧾 Amarrada muhiimka ah ee ku jira faylka

_Waxaa laga soo saaray `running-config`-ga qalab walba (waxaa laga saaray sadarrada caadiga ah). Config-ga oo dhammaystiran: folder-ka [`configs/`](configs/)._

<details><summary><b>SW — hostname `Switch`</b> (2960-24TT)</summary>

```
hostname Switch
line con 0
line vty 0 4
 login
line vty 5 15
 login
```

</details>

<details><summary><b>NAT — hostname `R1`</b> (2911)</summary>

```
hostname R1
interface GigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 duplex auto
 speed auto
interface GigabitEthernet0/1
 ip address 209.165.201.1 255.255.255.0
 duplex auto
 speed auto
interface GigabitEthernet0/2
 duplex auto
 speed auto
router rip
line con 0
line vty 0 4
 login
```

</details>

## 📂 Faylasha

- [`19-nat-pat-overload.pkt`](19-nat-pat-overload.pkt) — faylka Packet Tracer (fur PT 8.2+ / 9)
- [`topology.svg`](topology.svg) — sawirka topology-ga
- [`configs/`](configs/) — running-config qalab walba (.txt)

---
_Qayb ka mid ah [CCNA Learning Journal — Af-Soomaali](../../README.md). Su'aal ama sax: fur Issue._
