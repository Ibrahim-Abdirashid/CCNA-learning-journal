"""
build_labs.py - Build the labs/ folder of the repo from the Packet Tracer files.

For every lab in LABS it:
  - copies the .pkt file (with a clean name)
  - extracts topology.svg, configs/*.txt and summary.json (via pkt_extract.py)
  - writes a Somali README.md with the IP table, cabling, key commands and steps

Usage:  python build_labs.py "<folder with the original .pkt files>" labs
"""
import sys, os, re, json, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------------------
# Lab catalogue (order = learning order)
# --------------------------------------------------------------------------------------
LABS = [
 dict(slug='01-telnet', src='Telnet Configuration.pkt', title='Telnet — Remote Access-ka Switch-ka',
      level='Bilow', lessons=['05-device-management/01-telnet-and-ssh.md'],
      objective="Switch-ka waxaa la siinayaa IP (interface VLAN 1), kadibna waxaa lagu furayaa Telnet si PC-gu meel fog uga maamulo. Telnet xogtu waa *clear text* (lama qarin), sidaas darteed labs-ka xiga waxaan u gudbaynaa SSH.",
      steps=[
        ("Sii switch-ka IP management ah (SVI VLAN 1)", "Switch(config)# hostname TelnetSwitch\nTelnetSwitch(config)# interface vlan 1\nTelnetSwitch(config-if)# ip address 192.168.1.1 255.255.255.0\nTelnetSwitch(config-if)# no shutdown"),
        ("Dhig enable secret si privileged mode loo ilaaliyo", "TelnetSwitch(config)# enable secret cisco"),
        ("Fur Telnet line-yada VTY", "TelnetSwitch(config)# line vty 0 4\nTelnetSwitch(config-line)# password cisco\nTelnetSwitch(config-line)# login\nTelnetSwitch(config-line)# transport input telnet"),
        ("PC0 sii IP 192.168.1.10/24, kadibna Command Prompt ka qor", "C:\\> telnet 192.168.1.1"),
      ],
      verify=["`show ip interface brief` — VLAN1 waa inuu *up/up* yahay", "`show running-config | section line vty`", "PC0 → `ping 192.168.1.1` kadib `telnet 192.168.1.1`"],
      notes=["Telnet password-ka iyo xogta oo dhan waxay maraan network-ka iyagoo aan la qarin (plain text). Shabakad dhab ah **ha ku isticmaalin** — SSH isticmaal (Lab 02)."]),

 dict(slug='02-ssh', src='SSH configuration.pkt', title='SSH — Remote Access ammaan ah',
      level='Bilow', lessons=['05-device-management/02-ssh.md', '05-device-management/01-telnet-and-ssh.md'],
      objective="Router-ka waxaa lagu habaynayaa SSH version 2 si PC-gu meel fog uga soo galo isagoo xogtu sirran tahay (encrypted). Waxaa loo baahan yahay: hostname, domain-name, RSA key, username/password, iyo VTY oo SSH keliya aqbala.",
      steps=[
        ("Hostname iyo domain name (RSA key-gu wuu u baahan yahay labadaba)", "Router(config)# hostname SSH\nSSH(config)# ip domain-name cisco"),
        ("Samee RSA key (1024 ama ka badan) oo shid SSH v2", "SSH(config)# crypto key generate rsa\nHow many bits in the modulus [512]: 1024\nSSH(config)# ip ssh version 2"),
        ("Samee user local ah iyo enable secret", "SSH(config)# username admin secret cisco\nSSH(config)# enable secret cisco"),
        ("VTY: isticmaal user-ka local-ka oo SSH keliya ogolow", "SSH(config)# line vty 0 15\nSSH(config-line)# login local\nSSH(config-line)# transport input ssh"),
        ("Interface-ka LAN-ka sii IP oo shid", "SSH(config)# interface g0/0\nSSH(config-if)# ip address 192.168.10.1 255.255.255.0\nSSH(config-if)# no shutdown"),
        ("PC0 (192.168.10.2) ka tijaabi", "C:\\> ssh -l admin 192.168.10.1"),
      ],
      verify=["`show ip ssh` — version 2 waa inuu muuqdaa", "`show ssh` — sessions-ka furan", "PC0 → `ssh -l admin 192.168.10.1`; Telnet waa inuu diidaa (`transport input ssh`)"],
      notes=["Haddii `crypto key generate rsa` uu diido, hubi in hostname iyo ip domain-name la dhigay.", "`login local` waxay ka dhigan tahay in username/password-ka local-ka la isticmaalayo, ma aha password-ka line-ka."]),

 dict(slug='03-vlan-access-ports', src='VLAN Access configuration.pkt', title='VLAN-yada iyo Access Ports',
      level='Bilow', lessons=['03-switching/02-vlan-introduction.md', '03-switching/03-vlans.md'],
      objective="Hal switch ayaa loo qaybinayaa 3 VLAN (CCST, CCNA, CCNP). PC walba waxaa lagu xirayaa port *access* ah oo VLAN gaar ah ka tirsan. Natiijadu: PC-yada isku VLAN ah ayaa is-ping-i kara, kuwa VLAN kala duwan ma kala gaari karaan (router/L3 la'aan).",
      steps=[
        ("Abuur VLAN-yada oo magac sii", "Switch(config)# vlan 10\nSwitch(config-vlan)# name CCST\nSwitch(config-vlan)# vlan 20\nSwitch(config-vlan)# name CCNA\nSwitch(config-vlan)# vlan 30\nSwitch(config-vlan)# name CCNP"),
        ("Ports-ka PC-yada ka dhig access oo VLAN u qoondee (range isticmaal)", "Switch(config)# interface range fa0/1-2\nSwitch(config-if-range)# switchport mode access\nSwitch(config-if-range)# switchport access vlan 10\nSwitch(config)# interface range fa0/3-7\nSwitch(config-if-range)# switchport mode access\nSwitch(config-if-range)# switchport access vlan 20\nSwitch(config)# interface range fa0/8-10\nSwitch(config-if-range)# switchport mode access\nSwitch(config-if-range)# switchport access vlan 30"),
        ("PC-yada IP sii: VLAN10 = 192.168.10.x, VLAN20 = 192.168.20.x, VLAN30 = 192.168.30.x", ""),
      ],
      verify=["`show vlan brief` — port walba VLAN-kiisa", "`show interfaces fa0/1 switchport`", "PC0 → ping PC1 (isku VLAN) ✅ ; PC0 → ping PC2 (VLAN kale) ❌"],
      notes=["Laptop0 waxa ku xiran console cable (RS-232) — waa habka lagu maamulo switch-ka Terminal-ka Packet Tracer."]),

 dict(slug='04-vlan-trunk', src='VLAN Trunk Configuration.pkt', title='VLAN Trunk (802.1Q) — Switch L2 iyo L3',
      level='Bilow', lessons=['03-switching/04-vlan-trunking.md', '03-switching/05-vlan-trunk-layer3-switch.md'],
      objective="Laba switch (2960 iyo 3560 multilayer) ayaa isku xiran hal xadhig — *trunk*. Trunk-gu wuxuu qaadaa VLAN-yada oo dhan (11, 12, 13) isagoo tag 802.1Q ku daraya frame walba. Native VLAN-ka waxaa loo beddelay 999 (amni). PC-yada isku VLAN ah ee labada switch ku kala jira waa inay is-gaaraan.",
      steps=[
        ("Labada switch abuur VLAN-yada isku midka ah", "Switch(config)# vlan 11\nSwitch(config-vlan)# name CCNA\nSwitch(config-vlan)# vlan 12\nSwitch(config-vlan)# name CCNP\nSwitch(config-vlan)# vlan 13\nSwitch(config-vlan)# name CCIE"),
        ("Switch L2 (2960): port-ka isku xira ka dhig trunk", "Switch-1(config)# interface g0/1\nSwitch-1(config-if)# switchport mode trunk\nSwitch-1(config-if)# switchport trunk native vlan 999"),
        ("Switch L3 (3560): marka hore encapsulation dot1q sheeg, kadib trunk", "MultLayerSwitch(config)# interface g0/1\nMultLayerSwitch(config-if)# switchport trunk encapsulation dot1q\nMultLayerSwitch(config-if)# switchport mode trunk\nMultLayerSwitch(config-if)# switchport trunk native vlan 999"),
        ("Access ports-ka PC-yada VLAN u qoondee (fa0/1→11, fa0/2→12, fa0/3→13 labada switch)", ""),
      ],
      verify=["`show interfaces trunk` — g0/1 waa inuu trunk yahay, native 999", "`show vlan brief`", "PC-1 (VLAN11, 192.168.11.1) → ping PC-6 (VLAN11, 192.168.11.2) ✅"],
      notes=["Switch-yada 3560/3650 **waa khasab** `switchport trunk encapsulation dot1q` ka hor `switchport mode trunk`, haddii kale waa diidayaa.", "Native VLAN-ku waa inuu isku mid ka ahaadaa labada dhinac, haddii kale CDP waxay ku digi doontaa *Native VLAN mismatch*."]),

 dict(slug='05-vtp-server-client', src='VTP Protocol server and client Practice 1.pkt', title='VTP — Server iyo Client',
      level='Dhexe', lessons=['03-switching/06-vtp.md'],
      objective="VTP (VLAN Trunking Protocol) wuxuu VLAN-yada ka faafiyaa switch-ka *server* una gudbiyaa switch-yada *client* isaga oo maraya trunk link. Halkan SW-1 (server) ayaa abuuray VLAN 10 (CCNA) iyo 20 (CCNP); SW-2 (client) si toos ah ayuu u helay.",
      steps=[
        ("Link-ka labada switch ka dhig trunk (VTP trunk keliya ayuu maraa!)", "SW-1(config)# interface g0/1\nSW-1(config-if)# switchport mode trunk"),
        ("SW-1: VTP server, domain, password, version 2", "SW-1(config)# vtp mode server\nSW-1(config)# vtp domain cisco.com\nSW-1(config)# vtp password cisco123\nSW-1(config)# vtp version 2"),
        ("SW-2: VTP client oo isku domain/password ah", "SW-2(config)# vtp mode client\nSW-2(config)# vtp domain cisco.com\nSW-2(config)# vtp password cisco123\nSW-2(config)# vtp version 2"),
        ("SW-1 keliya ku abuur VLAN-yada — SW-2 iskiis buu u helayaa", "SW-1(config)# vlan 10\nSW-1(config-vlan)# name CCNA\nSW-1(config-vlan)# vlan 20\nSW-1(config-vlan)# name CCNP"),
      ],
      verify=["`show vtp status` labada switch — domain, mode, iyo *Configuration Revision* waa inay isku mid yihiin", "`show vlan brief` SW-2 — VLAN 10 iyo 20 waa inay muuqdaan iyadoo aan halkaas lagu qorin", "`show vtp password`"],
      notes=["Amarrada `vtp ...` kuma muuqdaan `show running-config`; waxay ku kaydsan yihiin `vlan.dat`. Isticmaal `show vtp status`.", "Client-ku VLAN ma abuuri karo (`vlan 30` wuu diidayaa)."]),

 dict(slug='06-vtp-transparent', src='VTP Protocol server and client and Transparent Practice 2.pkt', title='VTP — Server, Client iyo Transparent',
      level='Dhexe', lessons=['03-switching/06-vtp.md'],
      objective="Afar switch: SW-1 server, SW-2 *transparent* (dhexda), SW-3 iyo SW-4 clients. Transparent-ku VLAN-yada VTP-ga **ma qaato** oo uma isticmaalo naftiisa, laakiin wuu **sii gudbiyaa** (forward) fariimaha VTP si clients-ka ka dambeeya ay u helaan. Domain: CISCO, VLAN 100 (STUDENTS) iyo 200 (TEACHERS).",
      steps=[
        ("Dhammaan links-ka switch-yada ka dhig trunk", "SW-2(config)# interface range fa0/1-3\nSW-2(config-if-range)# switchport mode trunk"),
        ("SW-1 server", "SW-1(config)# vtp mode server\nSW-1(config)# vtp domain CISCO\nSW-1(config)# vtp password ccna\nSW-1(config)# vtp version 2"),
        ("SW-2 transparent (isku domain iyo password)", "SW-2(config)# vtp mode transparent\nSW-2(config)# vtp domain CISCO\nSW-2(config)# vtp password ccna\nSW-2(config)# vtp version 2"),
        ("SW-3 iyo SW-4 clients", "SW-3(config)# vtp mode client\nSW-3(config)# vtp domain CISCO\nSW-3(config)# vtp password ccna\nSW-3(config)# vtp version 2"),
        ("SW-1 ku abuur VLAN 100 iyo 200", "SW-1(config)# vlan 100\nSW-1(config-vlan)# name STUDENTS\nSW-1(config-vlan)# vlan 200\nSW-1(config-vlan)# name TEACHERS"),
      ],
      verify=["`show vtp status` afarta switch", "`show vlan brief` SW-3 iyo SW-4 — VLAN 100/200 waa inay yimaadaan", "`show vlan brief` SW-2 — **ma** laha VLAN 100/200 (transparent)"],
      notes=["Mode transparent-ka kaliya ayaa ku muuqda running-config (`vtp mode transparent`).", "Faylka casharka: *WAXAA KHASAB AH INAAD MAR WALBA ISKA HUBISO IN LINK-YADA SWITCH-YADA U DHAXEEYA AY TRUNK YIHIIN*."]),

 dict(slug='07-intervlan-layer3-switch', src='InterVlan routing using layer 3 Switch.pkt', title='Inter-VLAN Routing — Layer 3 Switch (SVI)',
      level='Dhexe', lessons=['03-switching/09-intervlan-layer3-switch.md', '03-switching/07-intervlan-routing-overview.md'],
      objective="Multilayer switch (3650) ayaa VLAN-yada SALES(10), IT(20), HR(30) u kala gudbinaya iyadoo interface VLAN (SVI) walba loo dhigay IP gateway ah. Switch L2-ka (SW-1) wuxuu PC-yada ku hayaa access ports, hal trunk ayuuna ku xiran yahay L3 switch-ka.",
      steps=[
        ("SW-1 (L2): VLAN-yada, access ports, iyo trunk-ka u socda L3", "Switch(config)# vlan 10\nSwitch(config-vlan)# name SALES\nSwitch(config-vlan)# vlan 20\nSwitch(config-vlan)# name IT\nSwitch(config-vlan)# vlan 30\nSwitch(config-vlan)# name HR\nSwitch(config)# interface range fa0/1-2\nSwitch(config-if-range)# switchport access vlan 10\nSwitch(config)# interface fa0/3\nSwitch(config-if)# switchport access vlan 20\nSwitch(config)# interface fa0/4\nSwitch(config-if)# switchport access vlan 30\nSwitch(config)# interface fa0/5\nSwitch(config-if)# switchport mode trunk"),
        ("L3 switch: isla VLAN-yada abuur, trunk-ka, kadib SVI walba IP sii", "MultSwitch(config)# interface g1/0/1\nMultSwitch(config-if)# switchport mode trunk\nMultSwitch(config)# interface vlan 10\nMultSwitch(config-if)# ip address 192.168.10.1 255.255.255.0\nMultSwitch(config-if)# no shutdown\nMultSwitch(config)# interface vlan 20\nMultSwitch(config-if)# ip address 192.168.20.1 255.255.255.0\nMultSwitch(config)# interface vlan 30\nMultSwitch(config-if)# ip address 192.168.30.1 255.255.255.0"),
        ("Shid routing-ka L3 switch-ka (**qodobka ugu muhiimsan**)", "MultSwitch(config)# ip routing"),
        ("PC walba gateway u dhig IP-ga SVI-ga VLAN-kiisa", ""),
      ],
      verify=["`show ip interface brief` L3 switch — Vlan10/20/30 up/up", "`show ip route` — 3 network oo *C* (connected) ah", "PC1 (VLAN10) → ping PC3 (VLAN20) ✅"],
      notes=["Haddii `ip routing` la illoobo, SVI-yadu way shaqaynayaan laakiin VLAN-yadu isma gaaraan.", "SVI-gu wuxuu *up* noqonayaa keliya haddii VLAN-kaasi jiro oo ugu yaraan hal port uu VLAN-kaas ku *up* yahay."]),

 dict(slug='08-intervlan-layer3-switch-practice-2', src='practice 2 InterVlan routing using layer 3 Switch.pkt', title='Inter-VLAN Routing L3 Switch — Practice 2 (laba switch L2)',
      level='Dhexe', lessons=['03-switching/09-intervlan-layer3-switch.md'],
      objective="Isla fikradda Lab 07, laakiin VLAN walba wuxuu ku yaal switch L2 gaar ah (SW-1 = VLAN 100 CCNA, SW-2 = VLAN 200 CCNP), labaduba trunk ayay ku xiran yihiin 3560 multilayer switch-ka oo SVI-yadu yihiin 10.100.0.1 iyo 11.200.0.1.",
      steps=[
        ("SW-1 iyo SW-2: VLAN, access port PC-ga, trunk-ka L3", "SW-1(config)# vlan 100\nSW-1(config-vlan)# name CCNA\nSW-1(config)# interface fa0/1\nSW-1(config-if)# switchport access vlan 100\nSW-1(config)# interface g0/1\nSW-1(config-if)# switchport mode trunk"),
        ("3560: trunks (dot1q) iyo SVI-yada", "MultSwitch(config)# interface range g0/1-2\nMultSwitch(config-if-range)# switchport trunk encapsulation dot1q\nMultSwitch(config-if-range)# switchport mode trunk\nMultSwitch(config)# vlan 100\nMultSwitch(config)# vlan 200\nMultSwitch(config)# interface vlan 100\nMultSwitch(config-if)# ip address 10.100.0.1 255.0.0.0\nMultSwitch(config)# interface vlan 200\nMultSwitch(config-if)# ip address 11.200.0.1 255.0.0.0\nMultSwitch(config)# ip routing"),
      ],
      verify=["`show interfaces trunk` 3560", "`show ip route`", "PC1 (10.100.0.2) → ping PC0 (11.200.0.2) ✅"],
      notes=["Subnet mask-ka /8 (255.0.0.0) waa tijaabo keliya; xaqiiqda /24 ama ka yar ayaa la isticmaalaa."]),

 dict(slug='09-etherchannel-static', src='etherchannel using Static EtherChannel Protocol.pkt', title='EtherChannel — Static (mode on)',
      level='Dhexe', lessons=['03-switching/11-etherchannel.md'],
      extra_src=[('etherchannel.pkt', 'etherchannel-starter.pkt', 'Faylka bilowga ah: 4 xadhig oo aan weli la habayn (ku tababaro adigu)')],
      objective="Afar xadhig oo isku xira SW-1 iyo SW-2 ayaa loo isku daraa hal link macquul ah (Port-channel 1). Habka *static* (`mode on`) ma sameeyo negotiation — labada dhinacba waa in gacanta lagu dhigaa `on`. Faa'iidada: bandwidth isku daran + redundancy, STP-na hal link buu u arkaa (ma xiro 3 xadhig).",
      steps=[
        ("Labada switch: ports-ka 4-ta ah isku dar channel-group 1 mode on", "SW-1(config)# interface range fa0/1-4\nSW-1(config-if-range)# channel-group 1 mode on\nSW-1(config-if-range)# switchport mode trunk"),
        ("Port-channel interface-ka ka dhig trunk", "SW-1(config)# interface port-channel 1\nSW-1(config-if)# switchport mode trunk"),
        ("Isla amarradan ku celi SW-2", ""),
      ],
      verify=["`show etherchannel summary` — `Po1(SU)` iyo ports `(P)`", "`show interfaces port-channel 1`", "`show spanning-tree` — Po1 keliya, ma jiraan ports *blocking*"],
      notes=["Ka hor intaadan bilaabin, `etherchannel-starter.pkt` waxaa ku jira 4 xadhig oo 3 ka mid ah STP ayaa xiray (orange). Kadib habaynta dhammaantood cagaar ayay noqonayaan.", "`mode on` hal dhinac + `desirable`/`active` dhinaca kale **ma shaqeeyo**."]),

 dict(slug='10-etherchannel-pagp', src='etherchannel using PAgP Protocol waxa gaar u leh CISCO.pkt', title='EtherChannel — PAgP (desirable / auto)',
      level='Dhexe', lessons=['03-switching/11-etherchannel.md'],
      objective="PAgP (Port Aggregation Protocol) waa protocol Cisco u gaar ah oo si otomaatig ah EtherChannel u sameeya. SW-1 = `desirable` (wuu codsadaa), SW-2 = `auto` (wuu aqbalaa laakiin ma codsado). Isku-darka shaqeeya: desirable+desirable, desirable+auto. auto+auto **ma** shaqeeyo.",
      steps=[
        ("SW-1: desirable", "SW-1(config)# interface range fa0/1-4\nSW-1(config-if-range)# channel-group 1 mode desirable\nSW-1(config-if-range)# switchport mode trunk\nSW-1(config)# interface port-channel 1\nSW-1(config-if)# switchport mode trunk"),
        ("SW-2: auto", "SW-2(config)# interface range fa0/1-4\nSW-2(config-if-range)# channel-group 1 mode auto\nSW-2(config-if-range)# switchport mode trunk\nSW-2(config)# interface port-channel 1\nSW-2(config-if)# switchport mode trunk"),
      ],
      verify=["`show etherchannel summary` — Protocol: **PAgP**", "`show pagp neighbor`", "`show interfaces trunk`"],
      notes=["PAgP waxaa loo isticmaalaa keliya switch Cisco ↔ Cisco. Qalab kale (HP, Juniper…) LACP isticmaal (Lab 11)."]),

 dict(slug='11-etherchannel-lacp', src='etherchannel using LACP Protocol Standard.pkt', title='EtherChannel — LACP (active / passive)',
      level='Dhexe', lessons=['03-switching/11-etherchannel.md'],
      objective="LACP (IEEE 802.3ad) waa heerka caalamiga ah ee EtherChannel — wuxuu la shaqeeyaa qalab kasta. SW-1 = `active` (wuu codsadaa), SW-2 = `passive` (wuu aqbalaa). Isku-darka shaqeeya: active+active, active+passive. passive+passive **ma** shaqeeyo. Laba PC ayaa lagu daray si ping loo tijaabiyo.",
      steps=[
        ("SW-1: active", "SW-1(config)# interface range fa0/1-4\nSW-1(config-if-range)# channel-group 1 mode active\nSW-1(config-if-range)# switchport mode trunk\nSW-1(config)# interface port-channel 1\nSW-1(config-if)# switchport mode trunk"),
        ("SW-2: passive", "SW-2(config)# interface range fa0/1-4\nSW-2(config-if-range)# channel-group 1 mode passive\nSW-2(config-if-range)# switchport mode trunk\nSW-2(config)# interface port-channel 1\nSW-2(config-if)# switchport mode trunk"),
        ("PC0 (192.168.1.1) → ping PC1 (192.168.1.2); kadib jar hal xadhig — ping-gu waa inuu sii socdaa", ""),
      ],
      verify=["`show etherchannel summary` — Protocol: **LACP**", "`show lacp neighbor`", "Xadhig ka saar (delete) topology-ga: Po1 wuu sii shaqaynayaa (redundancy)"],
      notes=["Tilmaan: *active/passive* = LACP, *desirable/auto* = PAgP, *on* = static. Ha isku qasin labada protocol hal channel."]),

 dict(slug='12-cdp-lldp', src='CDP and LLDP Protocols pratical.pkt', title='CDP iyo LLDP — Deriska garasho (Neighbor Discovery)',
      level='Bilow', lessons=['05-device-management/03-cdp-lldp.md'],
      objective="CDP (Cisco Discovery Protocol, Cisco keliya) iyo LLDP (IEEE 802.1AB, qalab kasta) waxay qalabka u ogolaadaan inuu ogaado qalabka toos ugu xiran: magaca, port-ka, model-ka, IP-ga. Topology-gan (3 router, switch L2, switch L3, IP phone, laptop, server) LLDP ayaa laga shiday dhammaan qalabka Cisco-ga si loo barbardhigo CDP.",
      steps=[
        ("CDP caadi ahaan wuu shidan yahay. Hubi:", "R1# show cdp neighbors\nR1# show cdp neighbors detail"),
        ("LLDP caadi ahaan wuu damman yahay — shid qalab walba", "R1(config)# lldp run"),
        ("Eeg deriska LLDP", "R1# show lldp neighbors\nR1# show lldp neighbors detail"),
        ("Amni: interface-yada u socda dibadda (ISP) ka dami CDP", "R1(config)# interface g0/1\nR1(config-if)# no cdp enable"),
      ],
      verify=["`show cdp neighbors` R2 — waa inuu arkaa R1 iyo Switch", "`show lldp neighbors` MultSwitch — Laptop-ka **ma** muuqdo (PC-yadu LLDP/CDP ma hadlaan), IP Phone-ku wuu muuqdaa", "`show cdp interface`"],
      notes=["Faylkan IP lagama dhigin qalabka — ujeeddadu waa garashada deriska oo keliya (Layer 2).", "CDP wuxuu shaacin karaa macluumaad xasaasi ah, sidaas darteed `no cdp run` ama `no cdp enable` interface-yada dibadda."]),

 dict(slug='13-ipv6-addressing', src='IBRAHIM ABDIRASHID IPV6 LAB CONFIGURATION.pkt', title='IPv6 Addressing — Router iyo laba LAN',
      level='Dhexe', lessons=['02-ip-addressing/05-ipv6-addressing.md'],
      objective="Router ISR4331 ayaa laba LAN u kala qaybinaya IPv6: 2001:DB8:1::/64 iyo 2001:DB8:2::/64. `ipv6 unicast-routing` waa khasab si router-ku IPv6 u gudbiyo uuna PC-yada u diro Router Advertisement (SLAAC).",
      steps=[
        ("Shid IPv6 routing", "R1(config)# ipv6 unicast-routing"),
        ("Interface walba IPv6 sii oo shid", "R1(config)# interface g0/0/0\nR1(config-if)# ipv6 address 2001:DB8:1::1/64\nR1(config-if)# no shutdown\nR1(config)# interface g0/0/1\nR1(config-if)# ipv6 address 2001:DB8:2::1/64\nR1(config-if)# no shutdown"),
        ("PC-yada: Desktop → IP Configuration → IPv6 *Automatic* (SLAAC) ama gacanta ku qor tusaale 2001:DB8:1::10/64, gateway 2001:DB8:1::1", ""),
      ],
      verify=["`show ipv6 interface brief` — cinwaanka *link-local* (FE80::) iyo global", "`show ipv6 route` — laba *C* iyo laba *L*", "PC (LAN1) → `ping 2001:DB8:2::1` iyo PC LAN2"],
      notes=["Faylkan PC-yadu IPv6 gacanta laguma qorin — SLAAC ku tijaabi ama adigu geli.", "Link-local (FE80::/10) interface walba si toos ah ayuu u helaa marka IPv6 la shido."]),

 dict(slug='14-static-routing-ipv4-ipv6', src='Static Routing using ipv4 and ipv6.pkt', title='Static Routing — IPv4 iyo IPv6 (3 router)',
      level='Dhexe', lessons=['04-routing/02-static-routing.md', '02-ip-addressing/05-ipv6-addressing.md'],
      objective="Saddex router (R-LAN1, R-LAN2, R-LAN3) oo xadhig isku xiran, mid walbana LAN gaar ah leeyahay (192.168.1.0, .2.0, .3.0 /24). Router walba waxaa gacanta lagu tusayaa (static route) networks-ka uusan toos ugu xirnayn. Labada qaab ayaa la isticmaalay: *next-hop* iyo *exit-interface + next-hop*.",
      steps=[
        ("Interface-yada IP sii (IPv4 + IPv6) oo shid — tusaale R-LAN1", "R-LAN1(config)# interface g0/0\nR-LAN1(config-if)# ip address 192.168.1.1 255.255.255.0\nR-LAN1(config-if)# ipv6 address 2000:ABC:1::1/64\nR-LAN1(config-if)# no shutdown\nR-LAN1(config)# interface g0/1\nR-LAN1(config-if)# ip address 1.0.0.1 255.255.255.252\nR-LAN1(config-if)# ipv6 address 200:1::1/64\nR-LAN1(config-if)# no shutdown"),
        ("R-LAN1: laba network oo fog", "R-LAN1(config)# ip route 192.168.2.0 255.255.255.0 g0/1 1.0.0.2\nR-LAN1(config)# ip route 192.168.3.0 255.255.255.0 1.0.0.2"),
        ("R-LAN2 (dhexe): LAN1 iyo LAN3", "R-LAN2(config)# ip route 192.168.1.0 255.255.255.0 g0/0 1.0.0.1\nR-LAN2(config)# ip route 192.168.3.0 255.255.255.0 g0/2 2.0.0.2"),
        ("R-LAN3: LAN1 iyo LAN2 (labaduba R-LAN2 ayay maraan)", "R-LAN3(config)# ip route 192.168.1.0 255.255.255.0 g0/0 2.0.0.1\nR-LAN3(config)# ip route 192.168.2.0 255.255.255.0 g0/0 2.0.0.1"),
        ("IPv6 static routes (isla fikradda) — tusaale R-LAN1", "R-LAN1(config)# ipv6 unicast-routing\nR-LAN1(config)# ipv6 route 2000:ABC:2::/64 200:1::2\nR-LAN1(config)# ipv6 route 2000:ABC:3::/64 200:1::2"),
      ],
      verify=["`show ip route` — networks-ka fog waa inay *S* (static) ku muuqdaan", "`show ipv6 route`", "PC0 (192.168.1.2) → ping PC4 (192.168.3.2) ✅ — waa inuu maraa R1→R2→R3"],
      notes=["Faylka hadda ku jira: IPv4 static routes-ka waa dhammaystiran yihiin; IPv6 static routes-ka weli lagama qorin router-rada — tallaabada 5 ku dhammaystir.", "Link-yada router-rada /30 (255.255.255.252) ayaa loo isticmaalay: 2 host keliya ayaa loo baahan yahay."]),

 dict(slug='15-ospf-single-area', src='OSPF Single area 0 configuration.pkt', title='OSPF Single Area (Area 0) — 3 router serial',
      level='Dhexe', lessons=['04-routing/03-ospf.md'],
      objective="OSPF (Open Shortest Path First) waa dynamic routing protocol: router-radu iyagaa isku sheega networks-ka. Saddex router oo serial isku xiran, dhammaan area 0 (backbone). Router walba router-id gaar ah (1.1.1.1, 2.2.2.2, 3.3.3.3). Process ID-gu (10, 20, 30) waa mid gudaha router-ka ah, isku mid ma ahaan karo — laakiin **area**-du waa inay isku mid noqotaa.",
      steps=[
        ("Interface-yada IP sii (serial-ka DCE-ga `clock rate` u baahan karaa)", "R1(config)# interface s0/0/0\nR1(config-if)# ip address 192.168.10.1 255.255.255.0\nR1(config-if)# clock rate 64000\nR1(config-if)# no shutdown"),
        ("R1: OSPF, router-id, networks-ka toos ugu xiran", "R1(config)# router ospf 10\nR1(config-router)# router-id 1.1.1.1\nR1(config-router)# network 192.168.1.0 0.0.0.255 area 0\nR1(config-router)# network 192.168.10.0 0.0.0.255 area 0"),
        ("R2 (dhexe): 3 network", "R2(config)# router ospf 20\nR2(config-router)# router-id 2.2.2.2\nR2(config-router)# network 192.168.2.0 0.0.0.255 area 0\nR2(config-router)# network 192.168.10.0 0.0.0.255 area 0\nR2(config-router)# network 192.168.20.0 0.0.0.255 area 0"),
        ("R3", "R3(config)# router ospf 30\nR3(config-router)# router-id 3.3.3.3\nR3(config-router)# network 192.168.3.0 0.0.0.255 area 0\nR3(config-router)# network 192.168.20.0 0.0.0.255 area 0"),
        ("Interface-yada LAN-ka ka dhig passive (hello lagama diro PC-yada)", "R1(config-router)# passive-interface g0/0"),
      ],
      verify=["`show ip ospf neighbor` — R2 waa inuu 2 deris FULL leeyahay", "`show ip route ospf` — networks-ka *O*", "`show ip protocols`", "PC0 (192.168.1.2) → ping 192.168.3.2 ✅"],
      notes=["Wildcard mask = 255.255.255.255 − subnet mask (0.0.0.255 = /24).", "Haddii deris (neighbor) uusan soo bixin: hubi area, subnet isku mid, interface *up*, iyo hello/dead timers."]),

 dict(slug='16-ospf-multi-area-somaliland', src='OSPF practice.pkt', title='OSPF Multi-Area — Hargeysa, Boorama, Burco, Berbera',
      level='Sare', lessons=['04-routing/03-ospf.md'],
      objective="Shabakad shirkadeed oo 4 magaalo ah: HQ Hargeysa (R1, area 0 + server 172.16.1.2), Boorama (R2, area 1), Burco (R3, area 2), Berbera (R4, area 3). Afarta router waxay isku yimaadaan L3 switch (192.168.1.0/24 = area 0 backbone). Router walba oo magaalo ah waa ABR (Area Border Router) — hal lug area 0, lugta kale area-diisa. TELESOM-ISP waa router bannaan oo loogu talagalay default route mustaqbalka.",
      steps=[
        ("R1-Hargaisa (HQ, area 0 keliya)", "R1-Hargaisa(config)# router ospf 1\nR1-Hargaisa(config-router)# router-id 1.1.1.1\nR1-Hargaisa(config-router)# network 192.168.1.0 0.0.0.255 area 0\nR1-Hargaisa(config-router)# network 172.16.0.0 0.0.255.255 area 0"),
        ("R2-Borama (ABR: area 0 + area 1)", "R2-Borama(config)# router ospf 1\nR2-Borama(config-router)# router-id 2.2.2.2\nR2-Borama(config-router)# network 192.168.1.0 0.0.0.255 area 0\nR2-Borama(config-router)# network 10.0.0.0 0.255.255.255 area 1"),
        ("R3-Burco (ABR: area 0 + area 2)", "R3-Burco(config)# router ospf 1\nR3-Burco(config-router)# router-id 3.3.3.3\nR3-Burco(config-router)# network 192.168.1.0 0.0.0.255 area 0\nR3-Burco(config-router)# network 20.0.0.0 0.255.255.255 area 2"),
        ("R4-Berbera (ABR: area 0 + area 3)", "R4-Berbera(config)# router ospf 1\nR4-Berbera(config-router)# router-id 4.4.4.4\nR4-Berbera(config-router)# network 192.168.1.0 0.0.0.255 area 0\nR4-Berbera(config-router)# network 30.0.0.0 0.255.255.255 area 3"),
      ],
      verify=["`show ip ospf neighbor` R1 — 3 deris (R2, R3, R4) oo FULL ah (mid DR/BDR)", "`show ip route` R2 — networks-ka area kale *O IA* (inter-area) ayay ku muuqdaan", "`show ip ospf` — *It is an area border router*", "cashier-1 (Boorama) → ping 172.16.1.2 (server HQ) ✅ iyo cashier-5 (Berbera)"],
      notes=["Area walba waa inuu area 0 taabtaa (ama virtual-link). Halkan ABR walba si toos ah ayuu area 0 ugu xiran yahay.", "Network-ga L3 switch-ku waa *broadcast multi-access*: DR/BDR ayaa la doortaa (router-id-ga ugu sarreeya = DR haddii priority isku mid yahay).", "Server-ka HQ IP-giisu waa 172.16.1.2/16 halka router-ku /8 leeyahay — mismatch yar; labadaba /16 ka dhig.", "TELESOM-ISP weli lama habayn — tababar: `ip route 0.0.0.0 0.0.0.0 <ISP>` R1 ku dar iyo `default-information originate`."]),

 dict(slug='17-nat-static', src='NAT using Static NAT.pkt', title='NAT — Static NAT (1:1)',
      level='Dhexe', lessons=['06-ip-services/01-nat.md'],
      objective="Static NAT wuxuu si joogto ah isugu beddelaa hal IP gudaha ah (192.168.10.10 = PC1) iyo hal IP dibadda ah (203.0.113.100). Waxaa loo isticmaalaa server gudaha ah oo dibadda laga gaari karo. Interface-ka LAN = `inside`, interface-ka internet-ka = `outside`.",
      steps=[
        ("Interface-yada IP sii oo calaamadee inside/outside", "Router(config)# interface g0/0\nRouter(config-if)# ip address 192.168.10.1 255.255.255.0\nRouter(config-if)# ip nat inside\nRouter(config)# interface g0/1\nRouter(config-if)# ip address 203.0.10.1 255.255.255.0\nRouter(config-if)# ip nat outside"),
        ("Static NAT mapping", "Router(config)# ip nat inside source static 192.168.10.10 203.0.113.100"),
        ("PC1 → ping FILE SERVER (203.0.10.10), kadib eeg miiska NAT", "Router# show ip nat translations"),
      ],
      verify=["`show ip nat translations` — *Inside local* 192.168.10.10 ↔ *Inside global* 203.0.113.100", "`show ip nat statistics`", "Simulation mode: eeg packet-ka marka uu router-ka ka baxo — source IP wuu beddelmay"],
      notes=["IP-ga global-ka (203.0.113.100) ma aha inuu interface-ka outside ku yaal — router-ku wuu ka jawaabayaa ARP-ka (proxy).", "Faylkan server-ka waxaa loo baahan yahay route ku noqoshada 203.0.113.0 — Packet Tracer wuu ka gudbaa maadaama server-ku gateway 203.0.10.1 leeyahay."]),

 dict(slug='18-nat-dynamic', src='NAT using Dynamic Nat.pkt', title='NAT — Dynamic NAT (pool)',
      level='Dhexe', lessons=['06-ip-services/01-nat.md'],
      objective="Dynamic NAT wuxuu PC-yada gudaha (192.168.10.0/24) si ku-meel-gaar ah u siiyaa IP ka mid ah *pool* dibadda ah (209.165.201.10 – .20). ACL ayaa sheegaya cidda loo oggol yahay in la tarjumo. Marka pool-ku dhammaado, PC-yada intiisa kale internet ma helaan — sababtaas ayaa PAT loo isticmaalaa (Lab 19).",
      steps=[
        ("Inside / outside", "R1(config)# interface g0/0\nR1(config-if)# ip nat inside\nR1(config)# interface g0/1\nR1(config-if)# ip nat outside"),
        ("Pool-ka IP-yada dibadda", "R1(config)# ip nat pool NAT-POOL 209.165.201.10 209.165.201.20 netmask 255.255.255.0"),
        ("ACL: cidda la tarjumayo", "R1(config)# access-list 1 permit 192.168.10.0 0.0.0.255"),
        ("Isku xir ACL-ka iyo pool-ka", "R1(config)# ip nat inside source list 1 pool NAT-POOL"),
        ("PC0, PC1, PC2 → ping Server 209.165.201.200", ""),
      ],
      verify=["`show ip nat translations` — PC walba IP pool ka helay", "`show ip nat statistics` — *Total translations*, *Misses*", "`clear ip nat translation *` si aad mar kale u aragto"],
      notes=["Pool-ka 11 IP ayuu leeyahay: haddii 12 PC isku mar isticmaalaan, kan 12aad wuu fashilmayaa (`show ip nat statistics` → misses).", "Translations-ku waqti ayay ku dhacaan (timeout) haddii aan la isticmaalin."]),

 dict(slug='19-nat-pat-overload', src='NAT PAT ama Overload.pkt', title='NAT — PAT / Overload (hal IP, PC badan)',
      level='Dhexe', lessons=['06-ip-services/01-nat.md'],
      objective="PAT (Port Address Translation, *overload*) wuxuu dhammaan PC-yada gudaha ku tarjumaa **hal** IP dibadda ah (IP-ga interface g0/1 = 209.165.201.1) isagoo kala saara *port numbers*. Waa habka guryaha iyo shirkadaha yaryar ku galaan internet-ka.",
      steps=[
        ("Inside / outside", "R1(config)# interface g0/0\nR1(config-if)# ip nat inside\nR1(config)# interface g0/1\nR1(config-if)# ip nat outside"),
        ("ACL-ka LAN-ka", "R1(config)# access-list 1 permit 192.168.10.0 0.0.0.255"),
        ("PAT: interface-ka outside isticmaal (overload)", "R1(config)# ip nat inside source list 1 interface g0/1 overload"),
        ("PC0, PC1, PC2 → ping Server 209.165.201.200 isku mar", ""),
      ],
      verify=["`show ip nat translations` — dhammaan *Inside global* = 209.165.201.1 laakiin port-yo kala duwan (tusaale :1024, :1025)", "`show ip nat statistics` — *Dynamic mappings ... overload*"],
      notes=["⚠️ **Faylkan `.pkt` NAT weli laguma habayn** — waxaa ku jira topology-ga iyo IP-yada oo keliya (router-ka `router rip` bannaan ayaa ku jira). Tallaabooyinka kore adigu ku dhammaystir, kadib faylka kaydi.", "Halkii interface, pool-na waa loo isticmaali karaa: `ip nat inside source list 1 pool NAT-POOL overload`."]),

 dict(slug='20-lab-activity-1-vlsm-dhcp-ssh', src='CCNA2-LABACTIVITY 1.pkt', title='CCNA2 Lab Activity 1 — VLSM, DHCP, SSH, IPv6 (3 LAN)',
      level='Sare', lessons=['02-ip-addressing/03-subnetting.md', '02-ip-addressing/04-subnetting-part-2.md', '06-ip-services/02-dhcp.md', '05-device-management/02-ssh.md', '02-ip-addressing/05-ipv6-addressing.md'],
      report='Ibrahim Abdirashid_CCNA2_Lab1_Report.pdf',
      objective="Lab rasmi ah oo koorsada CCNA2. Hal router (R1, 2911) iyo 3 switch, LAN walba subnet cabbir gaar ah (VLSM): LAN2 /27 (30 host), LAN3 /28 (14 host), LAN1 /29 (6 host). R1 waa DHCP server saddexda LAN, dhammaan qalabku SSH ayay leeyihiin, interface walbana IPv6 dual-stack (2001:DB8:ACAD:x::1/64). Warbixinta buuxda: PDF-ka hoose.",
      steps=[
        ("Qorshaha VLSM ee 192.168.10.0/24", "LAN2: 192.168.10.0/27   (.1 – .30)   gateway .1\nLAN3: 192.168.10.32/28  (.33 – .46)  gateway .33\nLAN1: 192.168.10.48/29  (.49 – .54)  gateway .49"),
        ("R1: interfaces IPv4 + IPv6", "R1(config)# ipv6 unicast-routing\nR1(config)# interface g0/0\nR1(config-if)# description LAN_TO_SW1\nR1(config-if)# ip address 192.168.10.49 255.255.255.248\nR1(config-if)# ipv6 address 2001:DB8:ACAD:1::1/64\nR1(config-if)# no shutdown"),
        ("R1: DHCP pools (IP-yada gateway/switch ka reeb)", "R1(config)# ip dhcp excluded-address 192.168.10.49 192.168.10.50\nR1(config)# ip dhcp pool LAN1\nR1(dhcp-config)# network 192.168.10.48 255.255.255.248\nR1(dhcp-config)# default-router 192.168.10.49"),
        ("Switch walba: SVI, default-gateway, SSH", "SW1(config)# interface vlan 1\nSW1(config-if)# ip address 192.168.10.50 255.255.255.248\nSW1(config)# ip default-gateway 192.168.10.49\nSW1(config)# ip domain-name ccna.local\nSW1(config)# crypto key generate rsa\nSW1(config)# username admin secret cisco\nSW1(config)# line vty 0 15\nSW1(config-line)# login local\nSW1(config-line)# transport input ssh"),
        ("Amni asaasi ah: enable secret, banner, console password, service password-encryption", "R1(config)# enable secret class\nR1(config)# service password-encryption\nR1(config)# banner motd #fadlan xog sax ah ku soo gal#"),
      ],
      verify=["PC walba: `ipconfig /renew` — IP DHCP ka helay subnet-kiisa", "`show ip dhcp binding` R1", "`show ip interface brief` iyo `show ipv6 interface brief`", "PC → `ssh -l admin 192.168.10.49`", "PC LAN1 → ping PC LAN3 ✅"],
      notes=["Waa lab la qiimeeyay — PDF-ka waxaa ku jira topology-ga, jadwalka IP-yada iyo screenshots-ka.", "Qaar ka mid ah PC-yada (kuwa 'dhcp' aan lahayn) IP weli ma haystaan — DHCP ka codsii."]),

 dict(slug='21-lab-activity-2-vlans-trunk-vtp', src='CCNA2-LAB ACTIVITY 2.pkt', title='CCNA2 Lab Activity 2 — VLANs, Trunk, VTP, Port Security (3 switch, 38 PC)',
      level='Sare', lessons=['03-switching/03-vlans.md', '03-switching/04-vlan-trunking.md', '03-switching/06-vtp.md'],
      report='CCNA2-LAB ACTIVITY 2.pdf',
      objective="Shabakad dugsi: S1 (VTP server, core) iyo S2/S3 (VTP clients, access) oo trunk isku xiran (native VLAN 99, allowed 10,20,30,40,99). VLAN-yada: 10 STUDENTS (192.168.10.0/26), 20 STAFF (.64/26), 30 ADMIN (.128/26), 40 GUESTS (.192/26). Switch walba SVI VLAN 30 (management) ayuu leeyahay, SSH iyo banner ayaa la dhigay. Warbixinta buuxda: PDF-ka hoose.",
      steps=[
        ("S1: VTP server + VLAN-yada", "S1(config)# vtp mode server\nS1(config)# vtp domain cisco\nS1(config)# vlan 10\nS1(config-vlan)# name STUDENTS\nS1(config-vlan)# vlan 20\nS1(config-vlan)# name STAFF\nS1(config-vlan)# vlan 30\nS1(config-vlan)# name ADMIN\nS1(config-vlan)# vlan 40\nS1(config-vlan)# name GUESTS\nS1(config-vlan)# vlan 99\nS1(config-vlan)# name NATIVE"),
        ("S1: trunks u socda S2 iyo S3", "S1(config)# interface range g0/1-2\nS1(config-if-range)# switchport mode trunk\nS1(config-if-range)# switchport trunk native vlan 99\nS1(config-if-range)# switchport trunk allowed vlan 10,20,30,40,99"),
        ("S2/S3: VTP client, access ports (fa0/1-10 → 10, fa0/11-15 → 20, fa0/16 → 30, fa0/17-24 → 40)", "S2(config)# vtp mode client\nS2(config)# vtp domain cisco\nS2(config)# interface range fa0/1-10\nS2(config-if-range)# switchport mode access\nS2(config-if-range)# switchport access vlan 10"),
        ("Management SVI + SSH switch walba", "S2(config)# interface vlan 30\nS2(config-if)# ip address 192.168.10.132 255.255.255.192\nS2(config)# ip domain-name cisco.com\nS2(config)# crypto key generate rsa\nS2(config)# username admin secret cisco\nS2(config)# ip ssh version 2"),
      ],
      verify=["`show vtp status` S2 — mode Client, VLAN-yada 4 ayaa yimid", "`show interfaces trunk` S1 — native 99, allowed 10,20,30,40,99", "`show vlan brief` S2 — ports-ka VLAN-kooda", "ST-1 → ping ST-1(1) (isku VLAN, switch kale) ✅ ; ST-1 → ping Staf-1 ❌"],
      notes=["PC-yada gateway lama siin maadaama router/L3 aan jirin — VLAN-yadu isma gaaraan (ujeeddo).", "Staf-2(1) iyo Staf-3(1) mask-koodu waa /24 halkii /26 — khalad yar oo la saxi karo."]),

 dict(slug='22-lab-activity-3-intervlan-mls', src='CCNA2-LAB ACTIVITY 3.pkt', title='CCNA2 Lab Activity 3 — Inter-VLAN Routing Multilayer Switch',
      level='Sare', lessons=['03-switching/09-intervlan-layer3-switch.md'],
      report='CCNA2-LAB ACTIVITY 3.pdf',
      objective="Sii-wadista Lab Activity 2: hadda MLS1 (multilayer switch) ayaa gateway u ah VLAN 10/20/30 (SVI: 192.168.10.1, .65, .129) si ardayda, shaqaalaha iyo maamulku isu gaaraan. S1 iyo S2 waa access switches oo trunk ku xiran MLS1. Warbixinta buuxda: PDF-ka hoose.",
      steps=[
        ("MLS1: VLAN-yada + trunks", "MLS1(config)# vlan 10\nMLS1(config-vlan)# name STUDENTS\nMLS1(config-vlan)# vlan 20\nMLS1(config-vlan)# name STAFF\nMLS1(config-vlan)# vlan 30\nMLS1(config-vlan)# name ADMIN\nMLS1(config)# interface range g0/1-2\nMLS1(config-if-range)# switchport trunk encapsulation dot1q\nMLS1(config-if-range)# switchport mode trunk"),
        ("MLS1: SVI-yada + ip routing", "MLS1(config)# interface vlan 10\nMLS1(config-if)# ip address 192.168.10.1 255.255.255.192\nMLS1(config)# interface vlan 20\nMLS1(config-if)# ip address 192.168.10.65 255.255.255.192\nMLS1(config)# interface vlan 30\nMLS1(config-if)# ip address 192.168.10.129 255.255.255.192\nMLS1(config)# ip routing"),
        ("S1/S2: access ports iyo trunk-ka MLS1", "S1(config)# interface range fa0/1-2\nS1(config-if-range)# switchport access vlan 10\nS1(config)# interface g0/1\nS1(config-if)# switchport mode trunk"),
        ("PC walba gateway = SVI VLAN-kiisa", ""),
      ],
      verify=["`show ip route` MLS1 — 3 connected", "`show interfaces trunk`", "ST-1 (VLAN10) → ping ADM-1 (VLAN30) ✅"],
      notes=["/26 subnet: host-yada 62 VLAN walba (.1–.62, .65–.126, .129–.190)."]),

 dict(slug='23-capstone-etherchannel-vlans-dhcp-ssh-static', src='LAB EtherChannel-Vlans-Trunking-interVlan-DHCP-SSH-StaticRouting.pkt', title='Lab Guud (Capstone) — EtherChannel, VLANs, ROAS, DHCP, SSH, Static Routing',
      level='Sare', lessons=['03-switching/08-router-on-a-stick.md', '03-switching/11-etherchannel.md', '06-ip-services/02-dhcp.md', '04-routing/02-static-routing.md', '05-device-management/02-ssh.md'],
      objective="Isku-dar dhammaan casharrada: Xarunta (HQ) laba switch oo EtherChannel LACP (fa0/8-9) isku xiran, VLAN 10 CCNA (10.0.1.0/29) iyo 20 CCNP (10.0.2.0/28), router HQ-R1 oo *router-on-a-stick* (g0/0.10, g0/0.20) iyo DHCP server ah. Laan (branch) leh VLAN 30 CCIE (20.0.0.0/29) oo router b-R1 ku xiran; DHCP-ga laanta wuxuu maraa `ip helper-address` una socdaa HQ. Labada router waxay ku xiran yihiin 10.0.0.0/30, static routes ayaana isku xira. HQ-S1 SSH ayaa lagu maamulaa.",
      steps=[
        ("HQ-S1 ↔ HQ-S2: EtherChannel LACP + trunk", "HQ-S1(config)# interface range fa0/8-9\nHQ-S1(config-if-range)# channel-group 1 mode active\nHQ-S1(config-if-range)# switchport mode trunk\nHQ-S1(config)# interface port-channel 1\nHQ-S1(config-if)# switchport mode trunk"),
        ("HQ-R1: ROAS sub-interfaces", "HQ-R1(config)# interface g0/0\nHQ-R1(config-if)# no shutdown\nHQ-R1(config)# interface g0/0.10\nHQ-R1(config-subif)# encapsulation dot1Q 10\nHQ-R1(config-subif)# ip address 10.0.1.1 255.255.255.248\nHQ-R1(config)# interface g0/0.20\nHQ-R1(config-subif)# encapsulation dot1Q 20\nHQ-R1(config-subif)# ip address 10.0.2.1 255.255.255.240"),
        ("HQ-R1: DHCP pools 3-da VLAN (VLAN30-ka laanta oo ay ku jirto)", "HQ-R1(config)# ip dhcp excluded-address 10.0.1.1\nHQ-R1(config)# ip dhcp pool VLAN10-POOL\nHQ-R1(dhcp-config)# network 10.0.1.0 255.255.255.248\nHQ-R1(dhcp-config)# default-router 10.0.1.1\nHQ-R1(config)# ip dhcp pool VLAN30-POOL\nHQ-R1(dhcp-config)# network 20.0.0.0 255.255.255.248\nHQ-R1(dhcp-config)# default-router 20.0.0.1"),
        ("b-R1: sub-interface VLAN 30 + DHCP relay", "b-R1(config)# interface g0/1.30\nb-R1(config-subif)# encapsulation dot1Q 30\nb-R1(config-subif)# ip address 20.0.0.1 255.255.255.248\nb-R1(config-subif)# ip helper-address 10.0.0.1"),
        ("WAN link + static routes", "HQ-R1(config)# interface g0/2\nHQ-R1(config-if)# ip address 10.0.0.1 255.255.255.252\nHQ-R1(config)# ip route 20.0.0.0 255.255.255.248 10.0.0.2\nb-R1(config)# ip route 10.0.0.0 255.0.0.0 10.0.0.1"),
        ("HQ-S1: SSH (username ibrahim, domain ahsan)", "HQ-S1(config)# ip domain-name ahsan\nHQ-S1(config)# crypto key generate rsa\nHQ-S1(config)# username ibrahim secret cisco\nHQ-S1(config)# line vty 0 4\nHQ-S1(config-line)# login local\nHQ-S1(config-line)# transport input ssh"),
      ],
      verify=["`show etherchannel summary` HQ-S1 — Po1(SU)", "`show ip dhcp binding` HQ-R1 — PC-yada laanta (20.0.0.x) sidoo kale way ku jiraan (relay wuu shaqeeyay)", "`show ip route` labada router", "PC0 (HQ VLAN10) → ping PC10 (laanta VLAN30) ✅", "PC → `ssh -l ibrahim 10.0.1.1`"],
      notes=["HQ-S1 SVI VLAN10 = 10.0.1.1/24 — isku mid IP-ga router-ka g0/0.10! Waa khalad (IP conflict): u beddel 10.0.1.2/29.", "PC6, PC7, PC8 weli DHCP looma dhigin — Desktop → IP Configuration → DHCP.", "Route-ka b-R1 `10.0.0.0/8` waa summary ballaaran; ku filan laakiin /29 iyo /28 gaar ah ayaa ka sax badan."]),
 dict(slug='24-ip-configuration-basics', src='Day 10- IP Address Configuration on Network Devices.pkt', src_dir=r'C:\Users\hp\Documents\CCNA',
      title='IP Address Configuration — Router, Switch iyo PC (Day 10)',
      level='Bilow', lessons=['02-ip-addressing/01-ip-address-configuration.md', '02-ip-addressing/02-configuring-ip-addresses.md'],
      objective="Lab-ka casharka *IP Address Configuration on Network Devices*. Shirkad yar: EdgeRouter oo laba LAN leh (192.168.1.0/24 — maamulka, 172.16.0.0/16 — IT iyo Data Server), laba switch (branch1, branch2). Ujeeddadu waa: interface-yada router-ka IP sii oo shid, PC-yada IP + gateway sii, switch-yada hostname iyo user sii. Qaar ka mid ah PC-yada (Finance Manager, HR Manager) iyo gateway-ga IT Manager **ula kac ayaa looga tagay** — adigu dhammaystir.",
      steps=[
        ("Router: hostname iyo interface-yada", "Router(config)# hostname EdgeRouter\nEdgeRouter(config)# interface g0/0\nEdgeRouter(config-if)# ip address 192.168.1.254 255.255.255.0\nEdgeRouter(config-if)# no shutdown\nEdgeRouter(config)# interface g0/1\nEdgeRouter(config-if)# ip address 172.16.1.254 255.255.0.0\nEdgeRouter(config-if)# no shutdown"),
        ("Switch-yada: hostname iyo user local ah", "Switch(config)# hostname branch1\nbranch1(config)# username ccna secret cisco"),
        ("PC walba: Desktop → IP Configuration → Static: IP, mask, gateway = IP-ga router-ka ee LAN-kaas", "CEO-PC        192.168.1.2  /24  gw 192.168.1.254\nFinance Mgr   192.168.1.3  /24  gw 192.168.1.254   <- adigu geli\nHR Manager    192.168.1.4  /24  gw 192.168.1.254   <- adigu geli\nIT Manager    172.16.1.4   /16  gw 172.16.1.254    <- gateway ka maqan\nData Server   172.16.1.5   /16  gw 172.16.1.254"),
      ],
      verify=["`show ip interface brief` — g0/0 iyo g0/1 *up/up*", "CEO-PC → ping 192.168.1.254 (gateway) ✅, kadib ping 172.16.1.5 (Data Server) ✅", "IT Manager gateway la'aan → ping 192.168.1.2 ❌ (sababta: gateway ma laha!)"],
      notes=["Tani waa lab-ka ugu horreeya — haddii ping-gu shaqayn waayo, mar walba hubi: (1) `no shutdown`, (2) mask-ka, (3) gateway-ga PC-ga.", "Switch-yadu IP uma baahna si ay frames u gudbiyaan; IP waxaa loo siiyaa keliya management (Lab 01/02)."]),

 dict(slug='25-routing-directly-connected', src='Day 12 Routing PART 1.pkt', src_dir=r'C:\Users\hp\Documents\CCNA',
      title='Routing Part 1 — Directly Connected Networks (Day 12)',
      level='Bilow', lessons=['04-routing/01-routing-introduction.md'],
      objective="Lab-ka casharka *Routing — Hordhac*. Laba router oo isku xiran (192.168.168.0/24), Router1 laba LAN leeyahay (192.168.1.0, 192.168.2.0), Router_2 hal LAN (192.168.3.0). Ujeeddadu waa in la arko **directly connected networks** (`C` iyo `L`) routing table-ka, iyo in la fahmo sababta Cashier 1 uu Cashier 3 u gaarayo (isku router) laakiin Cashier 4 **uusan** u gaarin (router kale, route ma jirto) — taasi waa halka static routing (Lab 14) ka bilaabmayso.",
      steps=[
        ("Interface-yada IP sii oo shid (labada router)", "Router1(config)# interface g0/0\nRouter1(config-if)# ip address 192.168.1.1 255.255.255.0\nRouter1(config-if)# no shutdown\nRouter1(config)# interface g0/1\nRouter1(config-if)# ip address 192.168.2.1 255.255.255.0\nRouter1(config-if)# no shutdown\nRouter1(config)# interface g0/2\nRouter1(config-if)# ip address 192.168.168.1 255.255.255.0\nRouter1(config-if)# no shutdown"),
        ("Eeg routing table-ka — network walba oo interface *up* ah si toos ah ayuu u galaa", "Router1# show ip route\nC    192.168.1.0/24 is directly connected, GigabitEthernet0/0\nL    192.168.1.1/32 is directly connected, GigabitEthernet0/0\nC    192.168.2.0/24 ...\nC    192.168.168.0/24 ..."),
        ("Tijaabi: Cashier 1 → Cashier 3 (labaduba Router1) ✅ ; Cashier 1 → Cashier 4 (Router_2) ❌", ""),
        ("Su'aal: Router1 ma yaqaan 192.168.3.0? `show ip route` — maya. Xalka: static route (Lab 14) ama OSPF (Lab 15)", "Router1(config)# ip route 192.168.3.0 255.255.255.0 192.168.168.2\nRouter_2(config)# ip route 192.168.1.0 255.255.255.0 192.168.168.1\nRouter_2(config)# ip route 192.168.2.0 255.255.255.0 192.168.168.1"),
      ],
      verify=["`show ip route` labada router — `C` iyo `L` keliya (ka hor static-ka)", "`show ip interface brief`", "Cashier 2 iyo Cashier 4 gateway ma laha — geli, kadib ping"],
      notes=["`L` (local) = IP-ga interface-ka laftiisa /32; `C` (connected) = network-ka oo dhan.", "Router-ku wuxuu gudbiyaa keliya packets-ka network-kooda uu routing table ku hayo — haddii kale wuu tuuraa (ICMP *destination unreachable*)."]),

 dict(slug='26-network-design-static-routing', src='networkd design then configuration min bilow ila routing-ki 3 June 2026.pkt', src_dir=r'C:\Users\hp\Documents\CCNA',
      title='Network Design — HQ, Server Room, Burco + Static Routing',
      level='Dhexe', lessons=['04-routing/02-static-routing.md', '02-ip-addressing/01-ip-address-configuration.md'],
      objective="Mashruuc: shabakad shirkadeed bilow ilaa routing. HQ (CEO, Project Manager — 192.168.3.0/24), qolka server-rada (192.168.2.0/24), laanta Burco (192.168.1.0/24) iyo router Telesom oo internet-ka u taagan. Saddexda router waxaa isku xira links /8 (12.0.0.0, 23.0.0.0), static routes ayaana network walba isku xira. HQ-R1 wuxuu tusayaa **laba qaab** oo isku route ah: exit-interface keliya (`g0/2`) iyo next-hop (`12.0.0.2`) — kan labaad ayaa la doorbidaa Ethernet.",
      steps=[
        ("Qorshaha IP (design)", "HQ LAN       192.168.3.0/24   gw 192.168.3.1  (HQ-R1 g0/0)\nServers LAN  192.168.2.0/24   gw 192.168.2.1  (R2_server g0/0)\nBurco LAN    192.168.1.0/24   gw 192.168.1.1  (R3_brco g0/0)\nHQ <-> R2    12.0.0.0/8       12.0.0.1 <-> 12.0.0.2\nR2 <-> Burco 23.0.0.0/8       23.0.0.2 <-> 23.0.0.1"),
        ("HQ-R1: static route u socda servers-ka (next-hop)", "HQ-R1(config)# ip route 192.168.2.0 255.255.255.0 12.0.0.2\nHQ-R1(config)# ip route 192.168.1.0 255.255.255.0 12.0.0.2      <- Burco (ku dar!)"),
        ("R2_server (dhexe): labada dhinac", "R2_server(config)# ip route 192.168.3.0 255.255.255.0 12.0.0.1\nR2_server(config)# ip route 192.168.1.0 255.255.255.0 23.0.0.1"),
        ("R3_brco: servers + HQ (labaduba R2 ayay maraan)", "R3_brco(config)# ip route 192.168.2.0 255.255.255.0 23.0.0.2\nR3_brco(config)# ip route 192.168.3.0 255.255.255.0 23.0.0.2      <- HQ (ku dar!)"),
        ("Telesom_Router iyo Internet_Server weli lama habayn — tababar: default route HQ-R1 ku dar", "HQ-R1(config)# ip route 0.0.0.0 0.0.0.0 <IP Telesom>"),
      ],
      verify=["`show ip route` router walba — 3-da LAN oo dhan waa inay muuqdaan (`C` ama `S`)", "CEO → ping Server0 (192.168.2.2) ✅", "CEO → ping branch_manager (192.168.1.2) — ✅ keliya marka routes-ka maqan la daro"],
      notes=["Faylkan HQ-R1 iyo R3_brco route-ka ay isu leeyihiin **ma laha** — HQ iyo Burco isma gaaraan ilaa aad tallaabada 2 iyo 4 ku darto. Waa tababar fiican.", "Link-yada router-rada /8 ayaa loo isticmaalay; /30 ayaa sax ah (laba host keliya).", "IT_support laptop iyo Internet_Server IP ma laha."]),

 dict(slug='27-eigrp-daheeye-university', src='Daheeye Network Universty Using EIGRP GROUP 2.pkt', src_dir=r'C:\Users\hp\Desktop',
      title='Mashruuc Guud — Daheeye University: EIGRP, ROAS, DHCP, EtherChannel, SSH (4 campus)',
      level='Sare', lessons=['03-switching/08-router-on-a-stick.md', '03-switching/11-etherchannel.md', '06-ip-services/02-dhcp.md', '05-device-management/02-ssh.md', '04-routing/03-ospf.md'],
      extra_src=[('EIGRP Configuration.pkt', 'eigrp-daheeye-starter.pkt', 'Faylka bilowga ah: topology-ga oo aan la habayn (ku tababaro adigu)')],
      objective="Mashruuc koox (Group 2): jaamacad 4 campus leh — HQ Hargeysa, Boorama, Burco, Berbera. Campus walba: router ROAS oo 5 VLAN leh (10 ADMIN, 20 FACULTY, 30 STUDENTS, 40 SERVERS, 99 MGMT), switch dhexe + 2 access switch oo EtherChannel LACP isku xiran, DHCP router-ka, SSH management VLAN 99. Afarta router waxaa isku xira serial links /30 (10.255.0.0/27) iyo **EIGRP 100** (dynamic routing Cisco). HQ waa xiriirka internet-ka: default route → TELESOM-ISP, ISP-guna static routes 4-ta campus. Qorshaha IP: `10.<campus>.<vlan>.0/24` (10 HQ, 20 Boorama, 30 Burco, 40 Berbera).",
      steps=[
        ("Router walba: ROAS — sub-interface VLAN walba (tusaale R-HQ)", "R-HQ(config)# interface g0/1\nR-HQ(config-if)# no shutdown\nR-HQ(config)# interface g0/1.10\nR-HQ(config-subif)# encapsulation dot1Q 10\nR-HQ(config-subif)# ip address 10.10.10.1 255.255.255.0\nR-HQ(config)# interface g0/1.20\nR-HQ(config-subif)# encapsulation dot1Q 20\nR-HQ(config-subif)# ip address 10.10.20.1 255.255.255.0\n... (30, 40, 99 sidoo kale)"),
        ("Router walba: DHCP pools VLAN 10/20/30 (.1–.20 ka reeb)", "R-HQ(config)# ip dhcp excluded-address 10.10.10.1 10.10.10.20\nR-HQ(config)# ip dhcp pool HQ-ADMIN\nR-HQ(dhcp-config)# network 10.10.10.0 255.255.255.0\nR-HQ(dhcp-config)# default-router 10.10.10.1"),
        ("EIGRP 100 router walba — router-id, passive default, serials keliya fur, networks", "R-HQ(config)# router eigrp 100\nR-HQ(config-router)# eigrp router-id 1.1.1.1\nR-HQ(config-router)# passive-interface default\nR-HQ(config-router)# no passive-interface s0/0/0\nR-HQ(config-router)# no passive-interface s0/0/1\nR-HQ(config-router)# no passive-interface s0/1/0\nR-HQ(config-router)# network 10.10.0.0 0.0.255.255\nR-HQ(config-router)# network 10.255.0.0 0.0.0.31\nR-HQ(config-router)# no auto-summary"),
        ("HQ: default route → ISP oo EIGRP ku faafi; ISP: routes 4-ta campus", "R-HQ(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.1\nR-HQ(config)# router eigrp 100\nR-HQ(config-router)# redistribute static\nTELESOM-ISP(config)# ip route 10.10.0.0 255.255.0.0 203.0.113.2\nTELESOM-ISP(config)# ip route 10.20.0.0 255.255.0.0 203.0.113.2  (30, 40 sidoo kale)"),
        ("Switch dhexe campus walba: EtherChannel LACP 2 access switch, trunk native 999, allowed VLANs, SVI VLAN 99 + gateway", "MAIN-SWITCH(config)# interface range fa0/1-2\nMAIN-SWITCH(config-if-range)# channel-group 1 mode active\nMAIN-SWITCH(config)# interface port-channel 1\nMAIN-SWITCH(config-if)# switchport mode trunk\nMAIN-SWITCH(config-if)# switchport trunk native vlan 999\nMAIN-SWITCH(config-if)# switchport trunk allowed vlan 10,20,30,40,99,999\nMAIN-SWITCH(config)# interface vlan 99\nMAIN-SWITCH(config-if)# ip address 10.10.99.2 255.255.255.0\nMAIN-SWITCH(config)# ip default-gateway 10.10.99.1"),
        ("SSH switch-ka dhexe iyo router-ka (domain daheeye.local, user admin)", "MAIN-SWITCH(config)# ip domain-name daheeye.local\nMAIN-SWITCH(config)# crypto key generate rsa\nMAIN-SWITCH(config)# username admin secret cisco\nMAIN-SWITCH(config)# ip ssh version 2\nMAIN-SWITCH(config)# line vty 0 15\nMAIN-SWITCH(config-line)# login local\nMAIN-SWITCH(config-line)# transport input ssh"),
      ],
      verify=["`show ip eigrp neighbors` R-HQ — 3 deris (Boorama, Burco, Berbera)", "`show ip route eigrp` — networks-ka campus-yada kale `D`, default `D*EX`", "`show ip eigrp topology` — successor iyo feasible successor", "`show etherchannel summary` switch walba — Po1/Po2 (SU)", "`show ip dhcp binding` router walba", "PC HQ VLAN 30 → ping server Berbera 10.40.40.10 ✅", "PC → `ssh -l admin 10.10.99.2`"],
      notes=["EIGRP waa protocol Cisco (hadda open RFC 7868): AD 90, metric bandwidth+delay, DUAL algorithm, neighbors Hello sida OSPF laakiin area ma laha — **AS number** (100) waa inuu isku mid noqdaa router walba.", "`passive-interface default` + `no passive-interface s0/x` = LAN-yada oo dhan passive, serial-yada keliya Hello — hab wanaagsan.", "Faylka starter-ka (`eigrp-daheeye-starter.pkt`) waa isla topology-ga iyadoo aan waxba lagu qorin — ku tababaro bilow ilaa dhammaad.", "Cashar EIGRP weli lama qorin; casharka OSPF wuxuu sharxayaa fikradaha guud ee dynamic routing."]),
]

REPORTS_ONLY = [('DONE Ibrahim Abdirashid CCNA 2 — LAB ACTIVITY 4.pdf', 'lab-activity-4-report.pdf',
                 'CCNA2 Lab Activity 4 — warbixin (faylka .pkt ma jiro)')]

TYPE_SO = {'Router': 'Router', 'Switch': 'Switch (L2)', 'MultiLayerSwitch': 'Switch (L3)', 'Pc': 'PC',
           'Laptop': 'Laptop', 'Server': 'Server', 'IpPhone': 'IP Phone', 'Printer': 'Printer', 'Cloud': 'Cloud'}
LESSON_TITLES = {}  # filled from disk if available


def sh(iface):
    return iface


def build_readme(lab, S, files):
    d = S['devices']
    n = {}
    for x in d:
        n[x['type']] = n.get(x['type'], 0) + 1
    counts = ', '.join(f"{v} {TYPE_SO.get(k, k)}" for k, v in n.items())
    L = []
    L.append(f"# Lab {lab['slug'][:2]} — {lab['title']}\n")
    lessons = ' · '.join(f"[{os.path.basename(p).split('.')[0]}](../../{p})" for p in lab['lessons']) or '_(cashar weli lama qorin — waa mid soo socda)_'
    L.append("| | |\n|---|---|")
    L.append(f"| **Faylka Packet Tracer** | [`{lab['slug']}.pkt`]({lab['slug']}.pkt) |")
    L.append(f"| **Heerka** | {lab['level']} |")
    L.append(f"| **Casharka la xiriira** | {lessons} |")
    L.append(f"| **Qalabka** | {counts} |")
    if lab.get('report'):
        L.append(f"| **Warbixinta (PDF)** | [{lab['report']}]({files['report']}) |")
    L.append("")
    L.append("## 🎯 Ujeeddada\n")
    L.append(lab['objective'] + "\n")
    L.append("## 🗺️ Topology\n")
    L.append("![Topology](topology.svg)\n")
    L.append("_Sawirkan si toos ah ayaa faylka `.pkt` looga soo saaray; fur faylka Packet Tracer si aad u aragto qaabka rasmiga ah._\n")
    # IP table
    L.append("## 🔢 Jadwalka IP-yada (IP Addressing Table)\n")
    rows = []
    for x in d:
        label = x['name'] if x['name'] == x['hostname'] else f"{x['name']} (`{x['hostname']}`)"
        if x['has_config']:
            for i in x['interfaces']:
                if i['mask'] == 'ipv6':
                    rows.append((label, TYPE_SO.get(x['type'], x['type']), i['iface'], i['ip'], 'IPv6', '—'))
                else:
                    rows.append((label, TYPE_SO.get(x['type'], x['type']), i['iface'], i['ip'], i['mask'], '—'))
        else:
            for h in x['host_ips']:
                if h['ip'] == 'dhcp':
                    rows.append((label, TYPE_SO.get(x['type'], x['type']), 'NIC', 'DHCP', '—', '—'))
                else:
                    rows.append((label, TYPE_SO.get(x['type'], x['type']), 'NIC', h['ip'], h['mask'], h['gateway'] or '—'))
    if rows:
        L.append("| Qalab | Nooc | Interface | IP Address | Subnet Mask | Default Gateway |\n|---|---|---|---|---|---|")
        for r in rows:
            L.append('| ' + ' | '.join(r) + ' |')
        L.append("")
    else:
        L.append("_Faylkan IP laguma dhigin qalabka (lab Layer 2 ah)._\n")
    noip = [x['name'] for x in d if x['type'] in ('Pc', 'Laptop', 'Server') and not x['host_ips']]
    if noip and rows:
        L.append(f"_IP la'aan: {', '.join(noip)}._\n")
    # VLAN table
    vl = [(x['name'], x['vlans'], x['vtp']) for x in d if x['type'] in ('Switch', 'MultiLayerSwitch') and (x['vlans'] or (x['vtp'] and x['vtp']['domain']))]
    if vl:
        L.append("## 🏷️ VLAN-yada iyo VTP\n")
        L.append("| Switch | VLAN-yada | VTP mode | VTP domain | VTP version | Password |\n|---|---|---|---|---|---|")
        for name, vlans, vtp in vl:
            vs = ', '.join(f"{v['id']} {v['name']}" for v in vlans) or '—'
            if vtp:
                L.append(f"| {name} | {vs} | {vtp['mode']} | {vtp['domain'] or '—'} | {vtp['version']} | {vtp['password'] or '—'} |")
            else:
                L.append(f"| {name} | {vs} | — | — | — | — |")
        L.append("")
    # cabling
    L.append("## 🔌 Xiriirinta (Cabling)\n")
    L.append("| Qalab A | Port | ⟷ | Qalab B | Port |\n|---|---|---|---|---|")
    for l in S['links']:
        L.append(f"| {l['a']} | {l['a_port']} | ⟷ | {l['b']} | {l['b_port']} |")
    L.append("")
    # steps
    L.append("## ⚙️ Tallaabooyinka Configuration-ka\n")
    for k, (txt, cmd) in enumerate(lab['steps'], 1):
        L.append(f"**{k}. {txt}**\n")
        if cmd:
            L.append("```\n" + cmd + "\n```\n")
    # verify
    L.append("## ✅ Sida loo xaqiijiyo (Verification)\n")
    for v in lab['verify']:
        L.append(f"- {v}")
    L.append("")
    # notes
    if lab.get('notes'):
        L.append("## 📝 Fiiro gaar ah\n")
        for v in lab['notes']:
            L.append(f"- {v}")
        L.append("")
    # highlights
    hl = [x for x in d if x['has_config'] and len(x['highlights']) > 3]
    if hl:
        L.append("## 🧾 Amarrada muhiimka ah ee ku jira faylka\n")
        L.append("_Waxaa laga soo saaray `running-config`-ga qalab walba (waxaa laga saaray sadarrada caadiga ah). Config-ga oo dhammaystiran: folder-ka [`configs/`](configs/)._\n")
        for x in hl:
            title = x['name'] if x['name'] == x['hostname'] else f"{x['name']} — hostname `{x['hostname']}`"
            L.append(f"<details><summary><b>{title}</b> ({x['model']})</summary>\n\n```\n" + '\n'.join(x['highlights']) + "\n```\n\n</details>\n")
    # files
    L.append("## 📂 Faylasha\n")
    for f, desc in files['list']:
        L.append(f"- [`{f}`]({f}) — {desc}")
    L.append("")
    L.append("---\n_Qayb ka mid ah [CCNA Learning Journal — Af-Soomaali](../../README.md). Su'aal ama sax: fur Issue._\n")
    return '\n'.join(L)


def main(src_dir, out_root):
    os.makedirs(out_root, exist_ok=True)
    index = []
    for lab in LABS:
        out = os.path.join(out_root, lab['slug'])
        if os.path.isdir(out):
            shutil.rmtree(out)
        os.makedirs(out)
        pkt_dst = os.path.join(out, lab['slug'] + '.pkt')
        sdir = lab.get('src_dir', src_dir)
        shutil.copy2(os.path.join(sdir, lab['src']), pkt_dst)
        subprocess.run([sys.executable, os.path.join(HERE, "pkt_extract.py"), pkt_dst, out], check=True, capture_output=True)
        S = json.load(open(os.path.join(out, 'summary.json'), encoding='utf-8'))
        files = {'list': [(lab['slug'] + '.pkt', 'faylka Packet Tracer (fur PT 8.2+ / 9)'),
                          ('topology.svg', 'sawirka topology-ga'),
                          ('configs/', 'running-config qalab walba (.txt)')]}
        for src, dst, desc in lab.get('extra_src', []):
            shutil.copy2(os.path.join(sdir, src), os.path.join(out, dst))
            files['list'].append((dst, desc))
        if lab.get('report'):
            rep = re.sub(r'[^A-Za-z0-9._-]+', '-', lab['report']).strip('-').lower()
            shutil.copy2(os.path.join(src_dir, lab['report']), os.path.join(out, rep))
            files['report'] = rep
            files['list'].append((rep, 'warbixinta lab-ka (PDF)'))
        os.remove(os.path.join(out, 'summary.json'))
        with open(os.path.join(out, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(build_readme(lab, S, files))
        nd = len(S['devices'])
        index.append((lab['slug'], lab['title'], lab['level'], nd, lab['lessons']))
        print('built', lab['slug'])
    rep_dir = os.path.join(out_root, 'reports')
    os.makedirs(rep_dir, exist_ok=True)
    for src, dst, desc in REPORTS_ONLY:
        shutil.copy2(os.path.join(src_dir, src), os.path.join(rep_dir, dst))
    with open(os.path.join(out_root, 'README.md'), 'w', encoding='utf-8') as f:
        f.write("# 🧪 Labs — Packet Tracer (Af-Soomaali)\n\n")
        f.write("Lab walba wuxuu leeyahay: faylka `.pkt`, sawirka topology-ga, jadwalka IP-yada, tallaabooyinka configuration-ka oo Soomaali ah, amarrada xaqiijinta, iyo `running-config`-ga qalab walba.\n\n")
        f.write("**Sida loo isticmaalo:** akhri casharka la xiriira → fur `.pkt`-ga Packet Tracer → raac tallaabooyinka README-ga → xaqiiji `show` commands-ka.\n\n")
        f.write("| # | Lab | Heerka | Qalab | Casharka |\n|---|---|---|---|---|\n")
        for slug, title, level, nd, lessons in index:
            ls = ', '.join(f"[{os.path.basename(p).split('.')[0]}](../{p})" for p in lessons) or '—'
            f.write(f"| {slug[:2]} | [{title}]({slug}/README.md) | {level} | {nd} | {ls} |\n")
        f.write("\n## Warbixinno (Reports)\n\n")
        for src, dst, desc in REPORTS_ONLY:
            f.write(f"- [{desc}](reports/{dst})\n")
        f.write("\n## Qalabka loo isticmaalay\n\n- Cisco Packet Tracer 9.0 (faylasha waxaa lagu furi karaa 8.2 iyo ka sare)\n- `pkt_extract.py` (folder-ka `tools/`) — wuxuu `.pkt`-ga ka soo saaraa topology-ga, IP-yada iyo configs-ka\n")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
