# CDP iyo LLDP — Deriska garasho (Neighbor Discovery)

> **Qaybta:** 05-device-management · **Xaaladda:** 📝 Draft — waa la saxayaa (qoraalka waa qabyo, lab-ku waa diyaar)
> **Labs la xiriira:** [Lab 12 — CDP iyo LLDP](../labs/12-cdp-lldp/README.md)

## Topics we'll address

1. Maxay yihiin, maxaa loogu baahday
2. CDP vs LLDP
3. Configuration — shid, dami, timers
4. Verification — sida topology-ga aan la garanayn lagu sawiro
5. Amniga

---

## 1. Maxaa loogu baahday?

Waxaad shaqo cusub ka bilowday shirkad; 30 switch iyo 5 router ayaa jira, **khariidad ma jirto**. Sidee ku ogaanaysaa switch-kee port-kee ku xiran yahay router-kee? Waxaad ku wareegi kartaa kabalka oo dhan… ama waxaad isticmaali kartaa **CDP/LLDP**.

Labaduba waa **Layer 2 discovery protocols**: qalab walba 60 ilbiriqsi kasta wuxuu interface walba ka diraa fariin (multicast) ku qoran "anigu waxaan ahay R1, model 2911, port-kan waa G0/0, IP-gaygu waa …". Derisku wuu kaydiyaa, **ma sii gudbiyo** (hal hop keliya). Sidaas ayaad `show cdp neighbors` qalab walba ku ogaanaysaa cidda toos ugu xiran — hop hop ayaadna topology-ga oo dhan ku sawiraysaa.

IP looma baahna — Layer 2 ayuu ka shaqeeyaa. Lab 12 qalabku IP ma laha, weliba deriska way is-arkaan.

---

## 2. CDP vs LLDP

| | CDP | LLDP |
|---|---|---|
| Magaca | Cisco Discovery Protocol | Link Layer Discovery Protocol |
| Cidda leh | Cisco (proprietary) | IEEE 802.1AB (open standard) |
| Qalabka | Cisco keliya (+ qaar ka mid ah IP phones) | Qalab kasta: Cisco, HP, Juniper, Linux, servers |
| Caadi ahaan | **Shidan** (global + interfaces) | **Damman** — waa in la shido |
| Timer / holdtime | 60s / 180s | 30s / 120s |
| Multicast MAC | 0100.0CCC.CCCC | 0180.C200.000E |
| Macluumaad dheeraad | VTP domain, native VLAN, duplex, PoE (IP phones) | Capabilities, management address |

Marka la isticmaalo: shabakad Cisco keliya → CDP ku filan. Shabakad isku dhafan → LLDP shid. Labada isku mar way shaqayn karaan.

---

## 3. Configuration

### CDP

```
! Global — caadi ahaan wuu shidan yahay
R1(config)# cdp run
R1(config)# no cdp run                    ← qalabka oo dhan dami

! Interface keliya
R1(config)# interface g0/1
R1(config-if)# no cdp enable              ← interface-kan keliya dami (ISP-ga u socda)
R1(config-if)# cdp enable

! Timers
R1(config)# cdp timer 60                  ← inta jeer la diro
R1(config)# cdp holdtime 180              ← inta la hayo deris aan la maqlin
```

### LLDP (Lab 12)

```
! Global — waa in la shido
R1(config)# lldp run
R1(config)# no lldp run

! Interface: dir iyo hel si gooni ah
R1(config)# interface g0/1
R1(config-if)# no lldp transmit           ← ha dirin
R1(config-if)# no lldp receive            ← ha aqbalin

! Timers
R1(config)# lldp timer 30
R1(config)# lldp holdtime 120
```

---

## 4. Verification

### `show cdp neighbors`

```
R2# show cdp neighbors
Device ID    Local Intrfce   Holdtme   Capability   Platform   Port ID
R1           Gig 0/0         157       R            C2911      Gig 0/1
Switch       Gig 0/1         142       S            2960       Fas 0/1
```

Akhriskiisa (sadarka 1aad): "Port-kayga **G0/0** (Local Intrfce) waxaa ku xiran qalab magaciisu yahay **R1**, model **2911**, isaguna port-kiisa **G0/1** (Port ID) ayuu igu xiran yahay." Capability: R = router, S = switch, T = phone, B = bridge, H = host.

> ⚠️ Khaladka imtixaanka: *Local Interface* = port-**kaaga**, *Port ID* = port-ka **deriska**. Ha isku qaldin.

### `show cdp neighbors detail`

Wuxuu ku daraa: **IP-ga deriska**, IOS version, VTP domain, native VLAN, duplex. Sidaas ayaad IP-ga qalab aadan aqoon ku helaysaa si aad SSH ugu gasho.

```
R2# show cdp neighbors detail
Device ID: R1
Entry address(es):
  IP address : 192.168.10.1
Platform: cisco C2911, Capabilities: Router
Interface: GigabitEthernet0/0, Port ID (outgoing port): GigabitEthernet0/1
...
```

### Amarrada kale

| Amar | Waxa uu tusayo |
|---|---|
| `show cdp` | CDP shidan? timers |
| `show cdp interface` | Interface walba CDP ma ka shidan yahay |
| `show cdp entry R1` | Hal deris faahfaahin |
| `show cdp traffic` | Tirada fariimaha la diray/helay |
| `show lldp neighbors` | Isla qaabka CDP (Port ID, capability) |
| `show lldp neighbors detail` | IP-ga (management address), system description |
| `show lldp` / `show lldp interface` | Xaaladda LLDP |
| `clear cdp table` | Miiska tirtir |

### Topology sawir — tallaabo-tallaabo

1. Qalab kasta oo aad gasho: `show cdp neighbors` (ama `lldp`).
2. Qor: *aniga port X* ⟷ *deris Y port Z*.
3. `show cdp neighbors detail` → IP-ga derisku, SSH ugu gal, ku celi.
4. Lab 12: R2 ka bilow → R1 iyo Switch → R1 ka `MultSwitch` iyo `Router` → MultSwitch ka IP Phone iyo Server. Laptop-ku **ma** muuqdo (PC-yadu CDP/LLDP ma hadlaan).

---

## 5. Amniga

CDP/LLDP waxay **shaaciyaan**: model-ka, IOS version-ka (vulnerabilities loo raadin karo), IP-yada, VTP domain. Qof interface ku soo xidhma (ama qalab dibadda ah sida ISP-ga) wuu arki karaa. Sidaas darteed:

- Interface-yada **dibadda** (ISP, WAN, guest): `no cdp enable`, `no lldp transmit`.
- Interface-yada **user-ka** (access ports): CDP badanaa waa loo daayaa IP phones-ka (PoE iyo voice VLAN ayay ku helaan), laakiin qalab kale la isticmaali karaa `no cdp enable`.
- Interface-yada **switch ↔ switch / router** (gudaha): ha shidnaadaan — waa faa'iido.

> 💡 CDP-gu wuxuu ku digaa **Native VLAN mismatch** trunk-ka — waa mid ka mid ah sababaha loo daayo.

---

## Koobid

```
CDP  ──►  Cisco keliya, shidan (default), 60/180s
LLDP ──►  standard, qalab kasta, waa in la shido: lldp run, 30/120s
Hal hop ──►  deriska toos kuu xiran keliya; lama sii gudbiyo
show cdp neighbors [detail] ──►  Local Intrfce = adiga, Port ID = deriska, detail = IP
Amni ──►  no cdp enable / no lldp transmit interface-yada dibadda
```

---
_Qayb ka mid ah [CCNA Learning Journal — Af-Soomaali](../README.md). Khalad ama hagaajin: fur Issue ama Pull Request._
