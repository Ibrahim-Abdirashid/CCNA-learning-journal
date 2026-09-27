# IPv6 Addressing

> **Qaybta:** 02-ip-addressing · **Xaaladda:** 📝 Draft — waa la saxayaa (qoraalka waa qabyo, labs-ku waa diyaar)
> **Labs la xiriira:** [Lab 13 — IPv6 Addressing](../labs/13-ipv6-addressing/README.md) · [Lab 14 — Static Routing IPv4 iyo IPv6](../labs/14-static-routing-ipv4-ipv6/README.md) · [Lab 20 — Lab Activity 1 (dual-stack)](../labs/20-lab-activity-1-vlsm-dhcp-ssh/README.md)

## Topics we'll address

1. Maxaa IPv6 loogu baahday
2. Qaabka cinwaanka iyo sida loo soo gaabiyo
3. Noocyada cinwaannada: global unicast, link-local, unique local, multicast
4. Prefix /64 — network iyo interface ID
5. Sida host-ku IPv6 u helo: manual, SLAAC, DHCPv6
6. Configuration router iyo PC
7. Verification

---

## 1. Maxaa IPv6 loogu baahday?

IPv4 = 32 bit = ~4.3 bilyan cinwaan; way dhammaadeen (NAT ayaa ilaa hadda na badbaadinaya — eeg [casharka NAT](../06-ip-services/01-nat.md)). IPv6 = **128 bit** = 340 undecillion (3.4 × 10³⁸) — dunida oo dhan atom walba IP ayaa la siin karaa. Faa'iidooyin kale: NAT looma baahna, header ka fudud, autoconfiguration (SLAAC), IPsec ku dhex jira, broadcast ma jiro.

---

## 2. Qaabka cinwaanka

128 bit waxaa loo qoraa **8 kooxood (hextets) oo 16-bit ah**, mid walba **4 xaraf hexadecimal** (0–9, A–F), oo `:` kala qaybiyo:

```
2001:0DB8:0000:0000:0000:0000:0000:0001
```

Hexadecimal: 0 1 2 3 4 5 6 7 8 9 A(10) B(11) C(12) D(13) E(14) F(15). Xaraf walba = 4 bit, 4 xaraf = 16 bit, 8 × 16 = 128 ✔.

### Laba xeer oo lagu soo gaabiyo

**Xeerka 1 — eber-yada hore ee kooxda ka saar** (leading zeros):

```
2001:0DB8:0000:0000:0000:0000:0000:0001
2001: DB8:   0:   0:   0:   0:   0:   1
```

**Xeerka 2 — kooxo eber ah oo isku xiga hal `::` ku beddel — hal mar keliya**:

```
2001:DB8:0:0:0:0:0:1   →   2001:DB8::1
```

Tusaalooyin:

| Buuxa | La soo gaabiyay |
|---|---|
| 2001:0DB8:ACAD:0001:0000:0000:0000:0001 | 2001:DB8:ACAD:1::1 |
| FE80:0000:0000:0000:0260:2FFF:FE16:6A6B | FE80::260:2FFF:FE16:6A6B |
| 2001:0DB8:0000:0001:0000:0000:0000:0001 | 2001:DB8:0:1::1 (`::` meesha ugu dheer, hal mar) |
| 0000:0000:0000:0000:0000:0000:0000:0001 | ::1 (loopback) |
| 0000:…:0000 | :: (unspecified, sida 0.0.0.0) |

> ⚠️ `2001:DB8::1::5` waa **khalad** — laba `::` ma oggola maxaa yeelay lama garanayo inta eber ee mid walba.

---

## 3. Noocyada cinwaannada

| Nooc | Prefix | Micnaha | U dhigma IPv4 |
|---|---|---|---|
| **Global Unicast (GUA)** | 2000::/3 (bilaabma 2 ama 3) | Public, internet-ka lagu gudbiyaa | Public IP |
| **Link-Local (LLA)** | FE80::/10 | Interface walba **si toos ah** ayuu u helaa; xadhigga keliya ayuu ka shaqeeyaa, lama route gareeyo. Routing protocols (OSPFv3) iyo default gateway ayaa isticmaala | 169.254.x.x (laakiin muhiim!) |
| **Unique Local (ULA)** | FC00::/7 (badanaa FD00::/8) | Private, gudaha keliya | 10.x, 192.168.x |
| **Multicast** | FF00::/8 | Koox: FF02::1 = dhammaan nodes, FF02::2 = dhammaan routers | 224.x (broadcast ma jiro IPv6!) |
| **Loopback** | ::1/128 | naftaada | 127.0.0.1 |
| **Unspecified** | ::/128 | "IP ma lihi weli" | 0.0.0.0 |
| **Documentation** | 2001:DB8::/32 | Tusaalooyinka buugaagta iyo labs-ka | 192.0.2.x |

Interface walba IPv6 ka shidan wuxuu leeyahay **ugu yaraan laba** cinwaan: hal link-local (mar walba) + hal ama in ka badan GUA/ULA. Lab 13: R1 g0/0/0 = `2001:DB8:1::1/64` + `FE80::...`.

---

## 4. Prefix /64

IPv6 subnet mask ma laha — **prefix length** keliya (`/64`). Qaabka caadiga ah:

```
2001:0DB8:ACAD:0001 : 0000:0000:0000:0001
|<-- 64 bit ------>| |<-- 64 bit ------>|
   Network prefix        Interface ID
   (global routing  +    (host-ka)
    subnet ID)
```

- ISP-gu shirkad wuxuu siiyaa /48 (tusaale `2001:DB8:ACAD::/48`).
- Shirkaddu 16 bit ayay subnet u haysataa (hextet-ka 4aad) = **65,536 subnet** oo /64 ah: `2001:DB8:ACAD:0001::/64`, `2001:DB8:ACAD:0002::/64`, …
- Subnet walba host-yo 2⁶⁴ — xisaab looma baahna. Subnetting IPv6 = hextet-ka 4aad tiri: 1, 2, 3 … A, B, … FFFF.

Lab 20: LAN1 = `2001:DB8:ACAD:1::/64`, LAN2 = `2001:DB8:ACAD:2::/64`, LAN3 = `2001:DB8:ACAD:3::/64`. Gateway walba `::1`.

---

## 5. Sida host-ku IPv6 u helo

| Hab | Sida | Waxa uu helo |
|---|---|---|
| **Manual** | Gacanta (sida IPv4) | IP + prefix + gateway |
| **SLAAC** (Stateless Address Autoconfiguration) | Router-ku wuxuu diraa **RA** (Router Advertisement, FF02::1); PC-gu prefix-ka ayuu ka qaataa, interface ID isagaa sameeya (EUI-64 ama random) | IP + prefix + gateway (link-local-ka router-ka). DNS ma helo (RA option la'aan) |
| **SLAAC + stateless DHCPv6** | RA (O flag) | IP SLAAC, DNS DHCPv6 |
| **Stateful DHCPv6** | RA (M flag) + DHCPv6 server | Dhammaan server-ka (sida DHCPv4) |

Router-ku RA **ma** diro ilaa `ipv6 unicast-routing` la shido — sababta amarkaas uu muhiim u yahay.

**EUI-64**: MAC-ka 48-bit → interface ID 64-bit: MAC-ka kala jar badhtamaha, `FFFE` dhex geli, bit-ka 7aad ee octet-ka 1aad rog. Tusaale MAC `0060.2F16.6A6B` → `0260:2FFF:FE16:6A6B` (Lab 02 PC0 link-local waa `FE80::260:2FFF:FE16:6A6B` — waa EUI-64!).

**Default gateway-ga PC-ga IPv6** badanaa waa **link-local-ka router-ka** (`FE80::1`), ma aha GUA-ga. Sidaas darteed engineers-ku router-ka link-local fudud ayay gacanta u dhigaan:

```
R1(config-if)# ipv6 address fe80::1 link-local
```

---

## 6. Configuration

### Router (Lab 13 / Lab 20)

```
R1(config)# ipv6 unicast-routing                 ← 1) routing + RA shid (khasab)
R1(config)# interface g0/0/0
R1(config-if)# ipv6 address 2001:DB8:1::1/64     ← GUA
R1(config-if)# ipv6 address fe80::1 link-local   ← (optional) link-local fudud
R1(config-if)# no shutdown
R1(config)# interface g0/0/1
R1(config-if)# ipv6 address 2001:DB8:2::1/64
R1(config-if)# no shutdown
```

Interface-ka **dual-stack** (IPv4 + IPv6 isku mar — Lab 14, Lab 20):

```
R-LAN1(config-if)# ip address 192.168.1.1 255.255.255.0
R-LAN1(config-if)# ipv6 address 2000:ABC:1::1/64
```

### Static route IPv6 (Lab 14)

```
R-LAN1(config)# ipv6 route 2000:ABC:2::/64 200:1::2          ← next-hop GUA
R-LAN1(config)# ipv6 route 2000:ABC:3::/64 g0/1 fe80::2       ← link-local: interface waa khasab
R-LAN1(config)# ipv6 route ::/0 200:1::2                       ← default route
```

### PC (Packet Tracer)

Desktop → IP Configuration → IPv6: **Automatic** (SLAAC, router-ku RA dirayo) ama **Static**: `2001:DB8:1::10/64`, gateway `2001:DB8:1::1` (ama `FE80::1`).

### Switch (management keliya)

```
S1(config)# sdm prefer dual-ipv4-and-ipv6 default    ← 2960: reload kadib
S1(config)# interface vlan 1
S1(config-if)# ipv6 address 2001:DB8:1::2/64
```

---

## 7. Verification

| Amar | Waxa uu tusayo |
|---|---|
| `show ipv6 interface brief` | Interface walba: link-local + GUA, up/down |
| `show ipv6 interface g0/0` | Faahfaahin: multicast groups (FF02::1, FF02::2, solicited-node), RA |
| `show ipv6 route` | `C` connected, `L` local (/128 interface-ka), `S` static, `O` OSPFv3 |
| `show ipv6 neighbors` | Miiska deriska (u dhigma ARP table — IPv6 ARP ma laha, **NDP** ayuu isticmaalaa) |
| `ping 2001:DB8:2::1` / `ping ipv6 …` | Isku xirnaanta |
| PC: `ipconfig /all` (Windows) | IPv6, link-local, gateway |

Muuqaalka `show ipv6 route` — interface walba **laba** sadar:

```
C   2001:DB8:1::/64 [0/0]   via GigabitEthernet0/0/0, directly connected
L   2001:DB8:1::1/128 [0/0] via GigabitEthernet0/0/0, receive
```

---

## Koobid

```
128 bit = 8 hextet × 4 hex      ──►  2001:DB8:ACAD:1::1
Soo gaabin                      ──►  eber-yada hore ka saar; kooxo eber ah → :: (hal mar)
GUA 2000::/3 | LLA FE80::/10 | ULA FD00::/8 | Multicast FF00::/8 | ::1
/64                             ──►  64 network + 64 interface ID; subnet = hextet 4aad
ipv6 unicast-routing            ──►  khasab: routing + RA (SLAAC)
SLAAC                           ──►  RA → PC isagaa IP sameeya; gateway = link-local router
NDP                             ──►  ARP-ka IPv6 (show ipv6 neighbors)
```

---
_Qayb ka mid ah [CCNA Learning Journal — Af-Soomaali](../README.md). Khalad ama hagaajin: fur Issue ama Pull Request._
