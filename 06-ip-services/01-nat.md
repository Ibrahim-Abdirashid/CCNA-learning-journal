# NAT — Network Address Translation

> **Qaybta:** 06-ip-services · **Xaaladda:** 📝 Draft — waa la saxayaa (qoraalka waa qabyo, labs-ku waa diyaar)
> **Labs la xiriira:** [Lab 17 — Static NAT](../labs/17-nat-static/README.md) · [Lab 18 — Dynamic NAT](../labs/18-nat-dynamic/README.md) · [Lab 19 — PAT / Overload](../labs/19-nat-pat-overload/README.md)

## Topics we'll address

1. Private iyo public IP — maxaa NAT loogu baahday
2. Erayada NAT: inside local, inside global, outside
3. Saddexda nooc: Static, Dynamic, PAT (overload)
4. Configuration mid walba
5. Verification iyo troubleshooting

---

## 1. Maxaa NAT loogu baahday?

IPv4 wuxuu leeyahay qiyaastii 4.3 bilyan cinwaan oo keliya — dunidu way ka badan tahay. Xalku wuxuu noqday: gurigaaga/shirkaddaada gudaheeda isticmaal **private IP** (bilaash, cid kastaa way isticmaali kartaa, internet-ka **laguma** gudbiyo), markaad internet-ka aadaysana router-ku ha kuu beddelo **public IP** (mid keliya oo ISP-gu ku siiyay).

Private IP-yada (RFC 1918):

| Class | Range | CIDR |
|---|---|---|
| A | 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 |
| B | 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 |
| C | 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 |

Tusaale: gurigaaga PC-gu wuxuu leeyahay 192.168.10.10, derisna 192.168.10.10 ayuu leeyahay — dhib ma jirto, maxaa yeelay labada router ee guryaha ayaa public IP kala duwan u beddelaya.

**NAT** (Network Address Translation) waa hawsha router-ku packet-ka **source IP**-giisa (marka uu baxayo) iyo **destination IP**-giisa (marka jawaabtu soo noqoto) ku beddelayo. Router-ku wuxuu hayaa **miis** (NAT table) uu ku xasuusto cidda uu wax u beddelay.

Faa'iidooyin: IP-yo ayuu badbaadiyaa, network-ka gudaha wuu qariyaa (dibadda lagama arko 192.168.x.x). Dhibaato: end-to-end connectivity wuu jebiyaa, qaar ka mid ah protocols-ka (VoIP, IPsec) dhib bay la kulmaan.

---

## 2. Erayada — waa in la kala fahmo

Ka fikir router-ka NAT: dhinac waa **inside** (network-kaaga), dhinaca kale waa **outside** (internet-ka).

| Eray | Micnaha | Tusaale (Lab 17) |
|---|---|---|
| **Inside local** | IP-ga PC-gaaga sida uu **gudaha** ku leeyahay (private) | 192.168.10.10 |
| **Inside global** | IP-ga PC-gaaga sida **dibaddu** u aragto (public, router-ku beddelay) | 203.0.113.100 |
| **Outside global** | IP-ga server-ka dibadda sida dhabta ah | 203.0.10.10 |
| **Outside local** | IP-ga server-ka dibadda sida gudaha loo arko (inta badan isku mid outside global) | 203.0.10.10 |

> 💡 Habka fudud: **local** = waxa gudaha la arko, **global** = waxa internet-ka la arko. **Inside** = qalabkaaga, **outside** = qalabka dibadda. Imtixaanka waxaa mar walba la weydiiyaa **inside local → inside global**.

Interface walba router-ka waa in loo sheegaa dhinaca uu ka tirsan yahay:

```
R1(config)# interface g0/0
R1(config-if)# ip nat inside       ← LAN-ka
R1(config)# interface g0/1
R1(config-if)# ip nat outside      ← internet / ISP
```

Haddii labadan la illoobo, **waxba ma shaqaynayaan** — khaladka ugu badan.

---

## 3. Saddexda nooc ee NAT

### a) Static NAT — 1 : 1 (Lab 17)

Hal IP gudaha ↔ hal IP dibadda, **joogto ah**. Waxaa loo isticmaalaa **server gudaha ah oo dibadda laga gaari karo** (web server, mail server), maxaa yeelay dadka dibaddu waa inay IP joogto ah yaqaannaan.

```
R1(config)# ip nat inside source static 192.168.10.10 203.0.113.100
```

Akhriskiisa: *inside* source-ka 192.168.10.10 → 203.0.113.100. Wuu labadhinac u shaqeeyaa: dibadda cid 203.0.113.100 wacda waxay gaaraysaa 192.168.10.10.

Dhibaato: IP walba oo public ah hal PC ayuu u baahan yahay — 50 PC = 50 public IP. Qaali.

### b) Dynamic NAT — pool (Lab 18)

Router-ku wuxuu hayaa **pool** IP-yo public ah (tusaale 209.165.201.10 – .20 = 11 IP). PC kasta oo baxa wuxuu **ku-meel-gaar** u qaataa mid ka mid ah, marka uu dhammeeyo (timeout) waa la soo celiyaa. **ACL** ayaa sheegaya cidda loo oggol yahay.

```
R1(config)# ip nat pool NAT-POOL 209.165.201.10 209.165.201.20 netmask 255.255.255.0
R1(config)# access-list 1 permit 192.168.10.0 0.0.0.255
R1(config)# ip nat inside source list 1 pool NAT-POOL
```

Dhibaato: pool-ku hadduu dhammaado (12-aad PC-ga) — internet ma helo ilaa mid soo celiyo. Weli IP badan ayuu u baahan yahay.

### c) PAT — Port Address Translation / Overload (Lab 19)

Waa kan **dhab ahaan** guryaha iyo shirkadaha isticmaalaan. **Hal** public IP (inta badan IP-ga interface-ka outside) ayaa PC-yada **oo dhan** loo isticmaalaa. Sidee router-ku u kala garanayaa jawaabaha? **Port numbers**:

| Inside local | Inside global | Outside |
|---|---|---|
| 192.168.10.10 **:1025** | 209.165.201.1 **:1025** | 209.165.201.200:80 |
| 192.168.10.11 **:1025** | 209.165.201.1 **:1026** ← port la beddelay | 209.165.201.200:80 |
| 192.168.10.12 **:3000** | 209.165.201.1 **:3000** | 209.165.201.200:80 |

Hal IP wuxuu qaadi karaa ~64,000 port — kumanaan PC. Configuration-ka waa mid fudud:

```
R1(config)# access-list 1 permit 192.168.10.0 0.0.0.255
R1(config)# ip nat inside source list 1 interface g0/1 overload
```

Ama pool iyo overload wadajir (shirkado waaweyn):

```
R1(config)# ip nat inside source list 1 pool NAT-POOL overload
```

Erayga **overload** = PAT. Ka fikir "hal IP ayaa la *overload* garaynayaa".

### Isbarbardhig

| | Static | Dynamic | PAT (overload) |
|---|---|---|---|
| Xiriirka | 1:1 joogto | 1:1 ku-meel-gaar (pool) | badan : 1 (ports) |
| Public IP loo baahan | PC walba mid | pool | 1 |
| Dibadda ma bilaabi kartaa? | ✅ haa | ❌ | ❌ |
| Isticmaalka | server | dhif | guryaha, shirkadaha |

---

## 4. Static NAT + PAT wadajir (xaalad dhab ah)

Shirkad: web server gudaha ah + 40 PC. Server-ka static, PC-yada PAT:

```
R1(config)# ip nat inside source static 192.168.10.10 203.0.113.100    ← server
R1(config)# access-list 1 deny host 192.168.10.10
R1(config)# access-list 1 permit 192.168.10.0 0.0.0.255
R1(config)# ip nat inside source list 1 interface g0/1 overload         ← PC-yada
```

**Port forwarding** (static PAT) — hal public IP laakiin port 80 keliya server-ka u gudbi:

```
R1(config)# ip nat inside source static tcp 192.168.10.10 80 209.165.201.1 80
```

---

## 5. Verification

```
R1# show ip nat translations
Pro  Inside global          Inside local          Outside local         Outside global
icmp 209.165.201.1:1        192.168.10.10:1       209.165.201.200:1     209.165.201.200:1
tcp  209.165.201.1:1025     192.168.10.11:1025    209.165.201.200:80    209.165.201.200:80
```

| Amar | Waxa uu tusayo |
|---|---|
| `show ip nat translations` | Miiska NAT: cidda loo beddelay cidda |
| `show ip nat statistics` | Tirada translations, interfaces inside/outside, pool-ka inta la isticmaalay, **misses** |
| `clear ip nat translation *` | Miiska tirtir (dynamic keliya; static waa joogto) |
| `debug ip nat` | Beddel walba oo dhacaya si toos ah u arag (lab keliya!) |

Packet Tracer **Simulation mode** waa hab fiican: packet-ka raac, marka uu router-ka ka baxo *Outbound PDU Details* ku eeg — source IP wuu beddelmay.

---

## 6. Troubleshooting

1. `show ip nat statistics` — *Inside interfaces* iyo *Outside interfaces* ma muuqdaan? Haddii kale `ip nat inside/outside` waa la illoobay.
2. ACL-ka ma saxan yahay? `show access-lists` — hits ma kordhayaan?
3. Routing — router-ku ma yaqaan waddada dibadda (default route)? NAT routing ma beddelo.
4. Dynamic: pool-ku ma dhammaaday? `show ip nat statistics` → *misses*.
5. Static: IP-ga global-ku ma isku network yahay interface-ka outside (ama route ma leeyahay)?

---

## Koobid

```
Private IP (10/8, 172.16/12, 192.168/16)  ──►  internet-ka laguma gudbiyo → NAT
ip nat inside / ip nat outside            ──►  interface walba (khasab)
Static   : ip nat inside source static A B             (server, 1:1)
Dynamic  : pool + access-list + ip nat inside source list 1 pool P
PAT      : access-list + ip nat inside source list 1 interface g0/1 overload
Xaqiiji  : show ip nat translations / statistics
```

---
_Qayb ka mid ah [CCNA Learning Journal — Af-Soomaali](../README.md). Khalad ama hagaajin: fur Issue ama Pull Request._
