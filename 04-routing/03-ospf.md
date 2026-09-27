# OSPF — Open Shortest Path First

> **Qaybta:** 04-routing · **Xaaladda:** 📝 Draft — waa la saxayaa (qoraalka waa qabyo, labs-ku waa diyaar)
> **Labs la xiriira:** [Lab 15 — OSPF Single Area](../labs/15-ospf-single-area/README.md) · [Lab 16 — OSPF Multi-Area (Hargeysa, Boorama, Burco, Berbera)](../labs/16-ospf-multi-area-somaliland/README.md)

## Topics we'll address

1. Waa maxay dynamic routing, maxaase OSPF looga baahan yahay static routing ka dib
2. Sida OSPF u shaqeeyo: Hello, neighbors, LSA, LSDB, SPF
3. Router ID, Area, Wildcard mask
4. DR iyo BDR
5. Configuration — single area iyo multi-area
6. Verification iyo troubleshooting

---

## 1. Maxaan OSPF ugu baahannahay?

Casharkii [Static Routing](02-static-routing.md) waxaan ku aragnay in engineer-ku isagu router walba gacanta ugu sheego network walba oo fog. Tan waxay ku fiican tahay 2–3 router. Laakiin hadday shirkadu leedahay 20 router oo 60 network ah:

- Router walba waxaad ku qoraysaa ilaa 59 `ip route` — khalad yar ayaa network-ka oo dhan hakiya.
- Haddii xadhig go'o, router-ku **ma ogaanayo** in waddadii ay xirantay; fariimaha waa la tuurayaa ilaa adiga aad wax beddesho.
- Network cusub markii la daro, dhammaan router-rada waa la wada taabanayaa.

**Dynamic routing protocol** (sida OSPF, EIGRP, RIP, BGP) wuxuu router-rada u ogolaadaa inay iyagu:

- isku sheegaan networks-ka ay leeyihiin,
- xisaabiyaan waddada ugu fiican (best path),
- si otomaatig ah isu cusboonaysiiyaan marka xadhig go'o ama network cusub yimaado.

OSPF waa protocol-ka **link-state** ee ugu caansan, waa **open standard** (qalab kasta ayaa taageera, ma aha Cisco keliya), waana kan imtixaanka CCNA ugu culus.

---

## 2. Sida OSPF u shaqeeyo (fikradda)

Ka fikir OSPF sidan: router walba wuxuu helayaa **khariidad dhammaystiran** oo network-ka oo dhan ah, kadibna isagu wuxuu xisaabinayaa waddada ugu gaaban ee uu meel walba ku gaari karo. Tallaabooyinka:

### a) Hello — deriska garasho (neighbor discovery)

Router walba interface-kiisa OSPF ka shidan wuxuu ka diraa fariin **Hello** 10 ilbiriqsi kasta (Ethernet). Marka laba router oo isku xadhig ah ay Hello iska helaan oo ay isku waafaqaan qodobbadan, waxay noqonayaan **neighbors**:

| Waa inay isku mid noqdaan | Waa inay kala duwan noqdaan |
|---|---|
| Area ID | Router ID |
| Subnet iyo subnet mask (isku network) | |
| Hello timer (10s) iyo Dead timer (40s) | |
| Authentication (haddii la isticmaalo) | |
| Stub area flag | |

> 💡 **Xusuusnow:** Marka neighbor uusan soo bixin, 90% waxay ka timaaddaa mid ka mid ah qodobbada tiirka bidix.

### b) LSA iyo LSDB — khariidadda

Router walba wuxuu deriskiisa u diraa **LSA** (Link-State Advertisement): "anigu waxaan leeyahay interface-yadan, networks-kan, cost-kan". Derisku isna wuu sii gudbiyaa (flooding). Dhammaadka, router walba wuxuu haystaa **LSDB** (Link-State Database) — isku mid ah router-rada area-da oo dhan. Taasi waa khariidadda.

### c) SPF — waddada ugu gaaban

Router walba wuxuu LSDB-ga ku shaqaaleeyaa **algorithm-ka Dijkstra (SPF)**: naftiisa ayuu xididka ka dhigaa, kadibna wuxuu xisaabiyaa network walba **cost**-ka ugu yar. Natiijadu waxay gashaa **routing table** iyadoo calaamad `O` leh.

### d) Cost

OSPF cost = `reference bandwidth / interface bandwidth`. Reference bandwidth-ka caadiga ah waa 100 Mbps:

| Interface | Bandwidth | Cost |
|---|---|---|
| Serial (T1) | 1.544 Mbps | 64 |
| FastEthernet | 100 Mbps | 1 |
| GigabitEthernet | 1000 Mbps | 1 (!) |

> ⚠️ FastEthernet iyo GigabitEthernet labaduba cost 1 ayay leeyihiin — OSPF ma kala garanayo. Shabakad casri ah: `auto-cost reference-bandwidth 10000` router **walba** ku qor si Gig = 10, 10Gig = 1 loo helo.

---

## 3. Erayada muhiimka ah

### Router ID

Waa lambar 32-bit oo IP u eg (tusaale `1.1.1.1`) oo router walba OSPF ku aqoonsado. Sida loo doorto (siday u kala horreeyaan):

1. `router-id x.x.x.x` haddii gacanta lagu qoray ← **habka la isticmaalo**
2. IP-ga ugu sarreeya ee **loopback** interface
3. IP-ga ugu sarreeya ee interface *up* ah

```
R1(config)# router ospf 1
R1(config-router)# router-id 1.1.1.1
```

> Haddii OSPF hore u shaqaynayay, router-id cusubku wuxuu qaadanayaa `clear ip ospf process` (wuu dib u bilaabayaa neighbors-ka!).

### Process ID

`router ospf **1**` — lambarka 1 waa **process ID**, wuxuu ku kooban yahay router-ka gudihiisa. Router-rada isku shabakad ah **isku mid ma ahaan karo** — Lab 15 R1 wuxuu isticmaalaa 10, R2 20, R3 30, weliba way wada shaqeeyaan. Laakiin caado ahaan isku mid ayaa la dhigaa si looga fogaado wareer.

### Area

OSPF wuxuu network-ka u qaybiyaa **areas**. Area walba LSDB gaar ah ayay leedahay, sidaas darteed SPF-gu wuu yaraadaa. Xeerarka:

- **Area 0** = backbone. Waa inay jirtaa.
- Area kasta oo kale waa inay **toos** u taabataa area 0.
- Router-ka laba area ku jira waa **ABR** (Area Border Router).

Shabakad yar (ilaa 50 router) hal area (area 0) ayaa ku filan = **single area**. Lab 15 waa single area, Lab 16 waa multi-area (Hargeysa area 0, Boorama 1, Burco 2, Berbera 3).

### Wildcard mask

Amarka `network` OSPF wuxuu isticmaalaa **wildcard mask**, ma aha subnet mask. Wildcard = `255.255.255.255 − subnet mask`:

| Subnet mask | Wildcard | Micnaha |
|---|---|---|
| 255.255.255.0 (/24) | 0.0.0.255 | 3-da octet ee hore waa inay saxan yihiin, kan dambe wax kasta |
| 255.255.255.252 (/30) | 0.0.0.3 | |
| 255.0.0.0 (/8) | 0.255.255.255 | |
| 255.255.255.255 (/32) | 0.0.0.0 | hal IP oo keliya (interface gaar ah) |

`0` = "waa inuu la mid yahay", `255` = "waxba ha ka eegin".

---

## 4. DR iyo BDR

Network-ka **Ethernet** (multi-access) haddii 5 router isku switch ku xiran yihiin, router walba oo 4-ta kale la neighbor-noqda = 10 xiriir, LSA-yaduna way batayaan. OSPF wuxuu doortaa:

- **DR** (Designated Router) — dhammaan router-radu isaga ayay LSA-yada u diraan, isna dhammaan ayuu u sii faafiyaa.
- **BDR** (Backup DR) — haddii DR-ku dumo isagaa beddelaya.
- Inta kale = **DROTHER**.

Doorashada: **priority**-ga ugu sarreeya (caadi 1, `ip ospf priority 0–255`), haddii isku mid — **router-id**-ga ugu sarreeya. Marka DR la doorto, router cusub oo priority sarreeya haddii yimaado **ma qaadanayo** ilaa DR-ku dumo (non-preemptive).

Lab 16: afarta router ee L3 switch-ka isku yimaada waxay dooranayaan DR/BDR — `show ip ospf neighbor` ku eeg tiirka *State*: `FULL/DR`, `FULL/BDR`, `FULL/DROTHER`. Link-yada **point-to-point** (serial, Lab 15) DR/BDR ma jiraan — `FULL/ -`.

---

## 5. Configuration

### Single area (Lab 15)

```
R1(config)# router ospf 1
R1(config-router)# router-id 1.1.1.1
R1(config-router)# network 192.168.1.0 0.0.0.255 area 0
R1(config-router)# network 192.168.10.0 0.0.0.255 area 0
R1(config-router)# passive-interface g0/0
```

- `network 192.168.1.0 0.0.0.255 area 0` = "interface kasta oo IP-giisu ku jiro 192.168.1.x, OSPF ka shid oo area 0 geli". Wuxuu sameeyaa **laba** shay: interface-ka Hello ayuu ka diraa, network-kiisana wuu xayaysiiyaa.
- `passive-interface g0/0` = interface-ka LAN-ka (PC-yadu ku xiran yihiin) network-kiisa **wuu xayaysiinayaa**, laakiin Hello **kama** dirayo — PC-yadu OSPF ma hadlaan, amni ahaana ma fiicna.

Habka labaad (casri): interface-ka toos ka shid, `network` la'aan:

```
R1(config)# interface g0/0
R1(config-if)# ip ospf 1 area 0
```

### Multi-area (Lab 16) — ABR

```
R2-Borama(config)# router ospf 1
R2-Borama(config-router)# router-id 2.2.2.2
R2-Borama(config-router)# network 192.168.1.0 0.0.0.255 area 0     ← lugta backbone
R2-Borama(config-router)# network 10.0.0.0 0.255.255.255 area 1    ← lugta Boorama
```

R2 wuxuu noqonayaa ABR: `show ip ospf` waxaa ku qoran *It is an area border router*. Router-rada area kale networks-ka Boorama waxay ku arkayaan `O IA` (inter-area).

### Default route la faafiyo

Router-ka internet-ka (ISP) ku xiran (Lab 16: R1-Hargaisa → TELESOM-ISP) wuxuu default route-ka dhammaan router-rada kale u sheegi karaa hal amar:

```
R1-Hargaisa(config)# ip route 0.0.0.0 0.0.0.0 <IP-ga ISP>
R1-Hargaisa(config)# router ospf 1
R1-Hargaisa(config-router)# default-information originate
```

Router-rada kale: `O*E2 0.0.0.0/0` ayaa routing table-ka ku soo baxaya.

### Timers, priority, cost (haddii loo baahdo)

```
R1(config-if)# ip ospf hello-interval 10
R1(config-if)# ip ospf dead-interval 40
R1(config-if)# ip ospf priority 100      ← DR noqo
R1(config-if)# ip ospf cost 50           ← waddadan ka fogee
R1(config-router)# auto-cost reference-bandwidth 10000
```

---

## 6. Verification

| Amar | Waxa uu tusayo |
|---|---|
| `show ip ospf neighbor` | Deriska, State (FULL = fiican), DR/BDR, interface |
| `show ip route ospf` | Networks-ka OSPF keenay (`O`, `O IA`, `O*E2`) |
| `show ip protocols` | Router ID, networks-ka la xayaysiiyay, passive interfaces |
| `show ip ospf` | Process ID, router ID, areas, ABR/ASBR |
| `show ip ospf interface brief` | Interface walba: area, cost, state, neighbors |
| `show ip ospf database` | LSDB-ga (khariidadda) |

Muuqaalka routing table:

```
O    192.168.3.0/24 [110/65] via 192.168.10.2, 00:05:12, Serial0/0/0
     ^                ^   ^
     OSPF             |   cost (metric)
                      administrative distance (OSPF = 110)
```

---

## 7. Troubleshooting — neighbor ma soo baxo?

Hubi siday u kala horreeyaan:

1. `show ip interface brief` — interface-yadu ma *up/up* yihiin?
2. `ping` — deriska ma gaartaa?
3. `show ip protocols` — network-ka saxda ah ma lagu xayaysiiyay (`network` iyo wildcard)? Interface-ku ma *passive* yahay?
4. Area — labada dhinac isku mid?
5. Subnet mask — isku network?
6. Hello/Dead timers — `show ip ospf interface g0/0`
7. Router ID — laba router oo isku router-id ah **ma** neighbor-noqdaan.
8. ACL ma jirto oo OSPF (protocol 89, multicast 224.0.0.5/6) xiraysa?

---

## Koobid

```
Dynamic routing  ──►  router-radu iyagaa isku sheega networks-ka
OSPF             ──►  link-state, open standard, AD 110, cost = bandwidth
Neighbor         ──►  Hello isku area, isku subnet, isku timers, router-id kala duwan
Area 0           ──►  backbone; area kasta waa inay taabato; ABR = laba area
DR/BDR           ──►  Ethernet keliya; priority kadib router-id
network x w area ──►  wildcard = 255.255.255.255 − mask
passive-interface──►  LAN-ka: xayaysii laakiin Hello ha dirin
```

---
_Qayb ka mid ah [CCNA Learning Journal — Af-Soomaali](../README.md). Khalad ama hagaajin: fur Issue ama Pull Request._
