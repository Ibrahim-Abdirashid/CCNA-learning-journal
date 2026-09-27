# DHCP — Dynamic Host Configuration Protocol

> **Qaybta:** 06-ip-services · **Xaaladda:** 📝 Draft — waa la saxayaa (qoraalka waa qabyo, labs-ku waa diyaar)
> **Labs la xiriira:** [Lab 20 — CCNA2 Lab Activity 1 (DHCP 3 LAN)](../labs/20-lab-activity-1-vlsm-dhcp-ssh/README.md) · [Lab 23 — Capstone (DHCP + relay)](../labs/23-capstone-etherchannel-vlans-dhcp-ssh-static/README.md)

## Topics we'll address

1. Maxaa DHCP loogu baahday
2. Sida uu u shaqeeyo — DORA
3. Router-ka DHCP server ka dhig
4. DHCP relay (`ip helper-address`) — server-ku network kale hadduu ku yaal
5. Router-ka DHCP client ka dhig
6. Verification iyo troubleshooting

---

## 1. Maxaa DHCP loogu baahday?

Casharkii [IP Address Configuration](../02-ip-addressing/01-ip-address-configuration.md) PC walba gacanta ayaan IP ugu qornay: IP, subnet mask, default gateway, DNS. Dugsi 200 PC leh, ama xafiis dadku laptops la yimaadaan — gacanta lagama qori karo, khaladna waa badan yahay (laba PC oo isku IP = **IP conflict**).

**DHCP** wuxuu PC-ga u ogolaadaa inuu **isagu weydiisto** IP marka uu network-ka ku soo xidhmo. Server-ku (router ama server gaar ah) wuxuu siinayaa:

- IP address + subnet mask
- Default gateway (`default-router`)
- DNS server
- Lease time — muddada uu IP-ga haysan karo (caadi 1 maalin), kadib wuu cusboonaysiinayaa

---

## 2. Sida uu u shaqeeyo — DORA

Afar fariin, xusuuso erayga **DORA**:

| # | Fariin | Cidda dirta | Nooca | Micnaha |
|---|---|---|---|---|
| 1 | **D**iscover | PC | broadcast (255.255.255.255) | "Ma jiraa DHCP server? IP baan rabaa" |
| 2 | **O**ffer | Server | unicast/broadcast | "Waa kan 192.168.10.11, ma rabtaa?" |
| 3 | **R**equest | PC | broadcast | "Haa, 192.168.10.11 ayaan qaadanayaa" (broadcast si servers-ka kale ay u ogaadaan) |
| 4 | **A**ck | Server | unicast | "Waa adigaa leh, muddo 24 saac, gateway waa .1, DNS waa ..." |

> 💡 PC-gu marka uu bilaabo IP ma laha (0.0.0.0), sidaas darteed wuxuu isticmaalaa **broadcast** — waana sababta router-ku caadi ahaan DHCP-ga uusan u gudbin network kale (routers-ku broadcast ma gudbiyaan). Xalka: qaybta 4.

PC-ga Windows: `ipconfig /release` (IP-ga sii daa), `ipconfig /renew` (mar kale weydiiso). Packet Tracer PC: Desktop → IP Configuration → **DHCP**.

---

## 3. Router-ka DHCP server ka dhig

Cisco router kasta wuxuu noqon karaa DHCP server — waa ku filan shabakad yar. Lab 20 (R1, 3 LAN):

```
! 1) IP-yada aan la rabin in la bixiyo (gateway, switch, server) ka reeb — KA HOR pool-ka
R1(config)# ip dhcp excluded-address 192.168.10.49 192.168.10.50
R1(config)# ip dhcp excluded-address 192.168.10.1 192.168.10.2

! 2) Pool LAN walba
R1(config)# ip dhcp pool LAN1
R1(dhcp-config)# network 192.168.10.48 255.255.255.248
R1(dhcp-config)# default-router 192.168.10.49
R1(dhcp-config)# dns-server 8.8.8.8
R1(dhcp-config)# domain-name ccna.local
R1(dhcp-config)# lease 1            ← 1 maalin (optional)

R1(config)# ip dhcp pool LAN2
R1(dhcp-config)# network 192.168.10.0 255.255.255.224
R1(dhcp-config)# default-router 192.168.10.1
R1(dhcp-config)# dns-server 8.8.8.8
```

Sidee router-ku u garanayaa PC-gu pool-kee uu ka tirsan yahay? **Interface-ka** uu Discover-ku ka soo galay: haddii uu ka yimid g0/0 (192.168.10.49/29), pool-ka `network 192.168.10.48/29` ayuu isticmaalayaa. Sidaas darteed interface walba waa inuu IP leeyahay oo pool-kiisu **isku network** yihiin.

Qodobbo:

- `excluded-address` **ka hor** pool-ka qor; haddii kale router-ku gateway-ga ayuu PC siin karaa.
- Pool walba **magac** gaar ah (LAN1, VLAN10-POOL…).
- `network` wuxuu qaataa **subnet mask**, ma aha wildcard (OSPF ka duwan).
- `default-router` haddii la illoobo PC-gu IP wuu helayaa laakiin network kale ma gaarayo.

DHCP-ga dami haddii loo baahdo: `no service dhcp`.

---

## 4. DHCP relay — `ip helper-address`

Xaaladda dhabta ah: hal DHCP server oo HQ ku yaal, laanta (branch) waa router kale. PC-yada laanta Discover (broadcast) way diraan, laakiin router-ka laanta broadcast **ma gudbiyo** — waa halkaas ku dhammaanaysaa.

Xalka: interface-ka router-ka ee PC-yadu ku xiran yihiin u sheeg "broadcast-ka DHCP ee halkan ku soo dhaca **unicast** ahaan ugu gudbi server-kan":

```
b-R1(config)# interface g0/1.30
b-R1(config-subif)# ip helper-address 10.0.0.1     ← IP-ga DHCP server-ka (ama router-ka HQ)
```

Lab 23: HQ-R1 waa DHCP server VLAN 30-ka laanta (pool `VLAN30-POOL 20.0.0.0/29`). b-R1 wuxuu Discover-ka ku duubaa unicast, source-kiisana wuxuu ka dhigaa IP-ga interface-ka (20.0.0.1 = *giaddr*) — sidaas ayuu HQ-R1 ku garanayaa pool-ka 20.0.0.0/29 inuu isticmaalo, xitaa haddii uusan toos ugu xirnayn.

Sidaas darteed labada shay waa in la hubiyaa:

1. Router-ka relay-ga: `ip helper-address` interface-ka **PC-yada** (ma aha ka server-ka).
2. Server-ka: pool ku jira network-ka laanta + route ku noqoshada laanta (static/OSPF).

---

## 5. Router-ka DHCP client ka dhig

Router-ka guriga interface-kiisa ISP-ga ku xiran wuxuu IP ka qaataa ISP-ga:

```
R1(config)# interface g0/1
R1(config-if)# ip address dhcp
R1(config-if)# no shutdown
```

---

## 6. Verification

| Halka | Amar | Waxa uu tusayo |
|---|---|---|
| Router (server) | `show ip dhcp binding` | IP walba iyo MAC-ka PC-ga qaatay, lease |
| Router (server) | `show ip dhcp pool` | Pool walba: inta la bixiyay, inta hadhay |
| Router (server) | `show ip dhcp conflict` | IP-yada conflict la helay |
| Router (server) | `show ip dhcp server statistics` | Tirada Discover/Offer/Request/Ack |
| PC (Windows/PT) | `ipconfig /all` | IP, gateway, DNS, DHCP server-ka bixiyay |
| PC | `ipconfig /release` → `ipconfig /renew` | Mar kale weydiiso |
| Router (debug) | `debug ip dhcp server events` | DORA-da oo toos ah (lab keliya) |

Packet Tracer **Simulation mode** + filter DHCP: afarta fariin ee DORA si toos ah u arag.

---

## 7. Troubleshooting — PC-gu IP ma helo (169.254.x.x)

IP `169.254.x.x` (APIPA) = "DHCP server-kii ma helin". Hubi:

1. Xadhigga iyo port-ka switch-ka — VLAN saxda ah ma ku jiraa?
2. Interface-ka router-ka *up/up* ma yahay, IP-giisuna pool-ka ma waafaqsan yahay?
3. `show ip dhcp pool` — IP-yo ma hadhay? (pool /29 = 6 host keliya, excluded ka jar)
4. PC-gu network kale ma ku yaal? → `ip helper-address` ma jiraa?
5. `service dhcp` ma shidan yahay?
6. ACL ma xirtay UDP 67/68?

---

## Koobid

```
DHCP     ──►  PC-gu isagaa IP weydiista: IP, mask, gateway, DNS, lease
DORA     ──►  Discover (bcast) → Offer → Request (bcast) → Ack
Server   ──►  ip dhcp excluded-address …  KADIB  ip dhcp pool NAME / network / default-router / dns-server
Relay    ──►  ip helper-address <server>  interface-ka PC-yada (broadcast → unicast)
Client   ──►  ip address dhcp
Xaqiiji  ──►  show ip dhcp binding / pool ;  PC: ipconfig /all, /renew
```

---
_Qayb ka mid ah [CCNA Learning Journal — Af-Soomaali](../README.md). Khalad ama hagaajin: fur Issue ama Pull Request._
