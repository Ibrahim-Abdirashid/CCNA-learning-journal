# Lab 10 — EtherChannel — PAgP (desirable / auto)

| | |
|---|---|
| **Faylka Packet Tracer** | [`10-etherchannel-pagp.pkt`](10-etherchannel-pagp.pkt) |
| **Heerka** | Dhexe |
| **Casharka la xiriira** | [11-etherchannel](../../03-switching/11-etherchannel.md) |
| **Qalabka** | 2 Switch (L2) |

## 🎯 Ujeeddada

PAgP (Port Aggregation Protocol) waa protocol Cisco u gaar ah oo si otomaatig ah EtherChannel u sameeya. SW-1 = `desirable` (wuu codsadaa), SW-2 = `auto` (wuu aqbalaa laakiin ma codsado). Isku-darka shaqeeya: desirable+desirable, desirable+auto. auto+auto **ma** shaqeeyo.

## 🗺️ Topology

![Topology](topology.svg)

_Sawirkan si toos ah ayaa faylka `.pkt` looga soo saaray; fur faylka Packet Tracer si aad u aragto qaabka rasmiga ah._

## 🔢 Jadwalka IP-yada (IP Addressing Table)

_Faylkan IP laguma dhigin qalabka (lab Layer 2 ah)._

## 🔌 Xiriirinta (Cabling)

| Qalab A | Port | ⟷ | Qalab B | Port |
|---|---|---|---|---|
| SW-1 | FastEthernet0/1 | ⟷ | SW-2 | FastEthernet0/1 |
| SW-1 | FastEthernet0/2 | ⟷ | SW-2 | FastEthernet0/2 |
| SW-1 | FastEthernet0/3 | ⟷ | SW-2 | FastEthernet0/3 |
| SW-1 | FastEthernet0/4 | ⟷ | SW-2 | FastEthernet0/4 |

## ⚙️ Tallaabooyinka Configuration-ka

**1. SW-1: desirable**

```
SW-1(config)# interface range fa0/1-4
SW-1(config-if-range)# channel-group 1 mode desirable
SW-1(config-if-range)# switchport mode trunk
SW-1(config)# interface port-channel 1
SW-1(config-if)# switchport mode trunk
```

**2. SW-2: auto**

```
SW-2(config)# interface range fa0/1-4
SW-2(config-if-range)# channel-group 1 mode auto
SW-2(config-if-range)# switchport mode trunk
SW-2(config)# interface port-channel 1
SW-2(config-if)# switchport mode trunk
```

## ✅ Sida loo xaqiijiyo (Verification)

- `show etherchannel summary` — Protocol: **PAgP**
- `show pagp neighbor`
- `show interfaces trunk`

## 📝 Fiiro gaar ah

- PAgP waxaa loo isticmaalaa keliya switch Cisco ↔ Cisco. Qalab kale (HP, Juniper…) LACP isticmaal (Lab 11).

## 🧾 Amarrada muhiimka ah ee ku jira faylka

_Waxaa laga soo saaray `running-config`-ga qalab walba (waxaa laga saaray sadarrada caadiga ah). Config-ga oo dhammaystiran: folder-ka [`configs/`](configs/)._

<details><summary><b>SW-1</b> (2960-24TT)</summary>

```
hostname SW-1
interface Port-channel1
 switchport mode trunk
interface FastEthernet0/1
 switchport mode trunk
 channel-group 1 mode desirable
interface FastEthernet0/2
 switchport mode trunk
 channel-group 1 mode desirable
interface FastEthernet0/3
 switchport mode trunk
 channel-group 1 mode desirable
interface FastEthernet0/4
 switchport mode trunk
 channel-group 1 mode desirable
line con 0
line vty 0 4
 login
line vty 5 15
 login
```

</details>

<details><summary><b>SW-2</b> (2960-24TT)</summary>

```
hostname SW-2
interface Port-channel1
 switchport mode trunk
interface FastEthernet0/1
 switchport mode trunk
 channel-group 1 mode auto
interface FastEthernet0/2
 switchport mode trunk
 channel-group 1 mode auto
interface FastEthernet0/3
 switchport mode trunk
 channel-group 1 mode auto
interface FastEthernet0/4
 switchport mode trunk
 channel-group 1 mode auto
line con 0
line vty 0 4
 login
line vty 5 15
 login
```

</details>

## 📂 Faylasha

- [`10-etherchannel-pagp.pkt`](10-etherchannel-pagp.pkt) — faylka Packet Tracer (fur PT 8.2+ / 9)
- [`topology.svg`](topology.svg) — sawirka topology-ga
- [`configs/`](configs/) — running-config qalab walba (.txt)

---
_Qayb ka mid ah [CCNA Learning Journal — Af-Soomaali](../../README.md). Su'aal ama sax: fur Issue._
