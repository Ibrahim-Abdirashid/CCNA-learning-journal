# Heerarka Amarrada Cisco IOS  
### Cisco IOS Command Hierarchy

## Ujeeddada

Marka aad maamulayso Cisco switch ama router, amarrada oo dhan hal meel lagama wada fuliyo. Cisco IOS wuxuu amarrada u kala saaraa **heerar kala duwan (command modes)**.

Heer kasta:

- Wuxuu leeyahay calaamad u gaar ah oo loo yaqaan **prompt**
- Wuxuu kuu oggolaanayaa amarro gaar ah
- Wuxuu leeyahay awood ka duwan heerarka kale

Sidaas darteed, amar wuxuu shaqayn karaa marka aad joogto heer gaar ah, laakiin wuu diidi karaa haddii aad ku qorto heer aan ku habboonayn.

---

## Waa maxay heerarka Cisco IOS CLI?

**Cisco IOS CLI (Command-Line Interface)** waa goobta qoraalka ah ee lagu maamulo Cisco routers iyo switches.

Cisco IOS wuxuu leeyahay heerar badan, laakiin lixdan ayaa ah kuwa inta badan la isticmaalo:

| Prompt | Magaca heerka | Waxa lagu qabto |
|---|---|---|
| `Switch>` | User EXEC Mode | Daawashada macluumaad kooban iyo tijaabooyin fudud |
| `Switch#` | Privileged EXEC Mode | Fulinta amarro awood badan iyo gelitaanka configuration-ka |
| `Switch(config)#` | Global Configuration Mode | Dejinta guud ee qalabka |
| `Switch(config-if)#` | Interface Configuration Mode | Dejinta interface gaar ah |
| `Router(config-router)#` | Router Configuration Mode | Dejinta routing protocol |
| `Switch(config-line)#` | Line Configuration Mode | Dejinta console, VTY ama AUX lines |

> **Fiiro gaar ah:** Calaamadda prompt-ku waxay kuu sheegaysaa heerka aad hadda ku sugan tahay.

---

# Sidee ayay heerarku u shaqeeyaan?

## Heerka 1: User EXEC Mode

### Calaamadda

```text
Switch>
```

Kani waa heerka ugu horreeya ee aad gasho marka aad qalabka furto ama aad CLI-ga ku xiranto.

Heerkan waxaad ku:

- Daawan kartaa macluumaad kooban
- Fulisaa amarro tijaabo ah sida `ping`
- Eegi kartaa qaar ka mid ah xogta qalabka
- Baran kartaa amarrada kuu bannaan adigoo adeegsanaya `?`

Laakiin heerkan kama beddeli kartid configuration-ka qalabka.

Tusaale:

```text
Switch> ?
Switch> ping 192.168.1.1
Switch> show clock
```

Si aad uga gudubto User EXEC Mode una gasho heerka xiga, isticmaal:

```cisco
enable
```

```text
Switch> enable
Switch#
```

---

## Heerka 2: Privileged EXEC Mode

### Calaamadda

```text
Switch#
```

Kani waa heer awood badan leh. Waxaa sidoo kale loo yaqaan **Enable Mode**.

Heerkan waxaad ku:

- Fulisaa amarro badan oo `show` ah
- Eegi kartaa running configuration-ka
- Kaydin kartaa configuration-ka
- Dib u shidi kartaa qalabka
- Geli kartaa Global Configuration Mode
- Fulisaa amarro troubleshooting ah

Tusaalooyin:

```cisco
show running-config
show startup-config
show interfaces
show ip interface brief
copy running-config startup-config
```

Si aad u aragto amarrada heerkan kuu bannaan:

```text
Switch# ?
```

Si aad u gasho Global Configuration Mode:

```cisco
configure terminal
```

Ama si kooban:

```cisco
conf t
```

```text
Switch# configure terminal
Switch(config)#
```

---

## Heerka 3: Global Configuration Mode

### Calaamadda

```text
Switch(config)#
```

Kani waa heerka ugu weyn ee lagu dejiyo configuration-ka qalabka.

Heerkan waxaad ku:

- Beddeli kartaa magaca qalabka
- Samayn kartaa VLANs
- Dejisaa passwords
- Daaraysaa adeegyo kala duwan
- U gudbi kartaa heerarka hoose ee configuration-ka

Isbeddellada aad halkan ku samayso waxay galaan:

```text
running-config
```

Tusaalooyin:

```cisco
hostname SW1
enable secret class
service password-encryption
banner motd #Authorized users only#
```

Tusaale dhammaystiran:

```text
Switch# configure terminal
Switch(config)# hostname SW1
SW1(config)#
```

---

# Heerarka hoose ee Configuration Mode

Marka aad joogto Global Configuration Mode, waxaad u gudbi kartaa heerar hoose oo lagu dejiyo qayb gaar ah.

## Interface Configuration Mode

Waxaa loo isticmaalaa dejinta interface ama port gaar ah.

```cisco
interface gigabitEthernet 0/1
```

```text
SW1(config)# interface gigabitEthernet 0/1
SW1(config-if)#
```

Heerkan waxaad ku samayn kartaa:

```cisco
description Link-to-SW2
switchport mode trunk
ip address 192.168.1.1 255.255.255.0
no shutdown
```

---

## Router Configuration Mode

Waxaa loo isticmaalaa dejinta routing protocol sida OSPF, RIP ama EIGRP.

```cisco
router ospf 1
```

```text
Router(config)# router ospf 1
Router(config-router)#
```

Tusaale:

```cisco
network 192.168.1.0 0.0.0.255 area 0
```

---

## Line Configuration Mode

Waxaa loo isticmaalaa dejinta hababka qalabka lagu geli karo, sida:

- Console
- VTY — Telnet ama SSH
- AUX

Tusaale VTY:

```cisco
line vty 0 4
```

```text
SW1(config)# line vty 0 4
SW1(config-line)#
```

Tusaale configuration:

```cisco
password cisco
login
transport input ssh
```

Tusaale Console:

```cisco
line console 0
```

```text
SW1(config-line)#
```

---

# Sidee looga baxaa heerarka?

## Amarka `exit`

Amarka `exit` wuxuu kaa saarayaa heerka aad hadda joogto, wuxuuna kuu celinayaa hal heer oo kaa sarreeya.

```text
SW1(config-if)# exit
SW1(config)#
```

Tusaale kale:

```text
SW1(config-line)# exit
SW1(config)#
```

---

## Amarka `end`

Amarka `end` wuxuu kaa saarayaa heer kasta oo configuration ah, wuxuuna si toos ah kuugu celinayaa Privileged EXEC Mode.

```text
SW1(config-if)# end
SW1#
```

Waxa kale oo la isticmaali karaa:

```text
Ctrl + Z
```

---

## Amarka `disable`

Amarka `disable` wuxuu kaa celinayaa Privileged EXEC Mode una celinayaa User EXEC Mode.

```text
SW1# disable
SW1>
```

---

## Soo koobidda amarrada bixitaanka

| Amarka | Waxa uu sameeyo |
|---|---|
| `exit` | Wuxuu dib kuugu celinayaa hal heer |
| `end` | Wuxuu si toos ah kuugu celinayaa Privileged EXEC Mode |
| `Ctrl + Z` | Wuxuu qabtaa shaqada `end` |
| `disable` | Wuxuu Privileged EXEC Mode kaaga celinayaa User EXEC Mode |
| `logout` | Wuxuu xirayaa CLI session-ka |

---

# Qaab-dhismeedka heerarka Cisco IOS

```text
Switch>
   │
   └── enable
         │
         ▼
Switch#
   │
   └── configure terminal
         │
         ▼
Switch(config)#
   │
   ├── interface gigabitEthernet 0/1
   │      └── Switch(config-if)#
   │
   ├── router ospf 1
   │      └── Router(config-router)#
   │
   └── line vty 0 4
          └── Switch(config-line)#
```

Qaabkan wuxuu muujinayaa in Cisco IOS uu leeyahay nidaam heerar kala sarreeya. Si aad u gaarto heer hoose, waa inaad marka hore martaa heerarka ka sarreeya.

---

# Khaladaadka caadiga ah

## 1. Amar lagu qoray heer khaldan

Haddii amar lagu qoro heer uusan ka shaqaynayn, waxaa laga yaabaa inaad aragto:

```text
% Invalid input detected at '^' marker.
```

Tusaale ahaan:

```text
Switch> show running-config
```

Amarkan User EXEC Mode kama shaqaynayo. Marka hore waa inaad gashaa Privileged EXEC Mode:

```text
Switch> enable
Switch# show running-config
```

---

## 2. Prompt-ka oo aan la fiirin

Mar kasta eeg calaamadda prompt-ka:

```text
>          User EXEC Mode
#          Privileged EXEC Mode
(config)#  Global Configuration Mode
(config-if)# Interface Configuration Mode
```

Prompt-ku wuxuu kuu sheegayaa meesha aad joogto iyo nooca amarrada aad fulin karto.

---

## 3. `configure terminal` oo heer khaldan lagu qoray

Amarkan wuxuu ka shaqeeyaa Privileged EXEC Mode:

```text
Switch# configure terminal
```

Kama shaqaynayo User EXEC Mode:

```text
Switch> configure terminal
```

Marka hore isticmaal:

```cisco
enable
```

---

## 4. `exit` iyo `end` oo la isku khaldo

`exit` wuxuu dib kuu celinayaa hal heer:

```text
Switch(config-if)# exit
Switch(config)#
```

`end` wuxuu toos kuu geynayaa Privileged EXEC Mode:

```text
Switch(config-if)# end
Switch#
```

---

# Qodobbada muhiimka ah

- Cisco IOS wuxuu isticmaalaa nidaam heerar kala sarreeya.
- Heer kasta wuxuu leeyahay amarro iyo awood u gaar ah.
- Calaamadda `>` waxay muujinaysaa User EXEC Mode.
- Calaamadda `#` waxay muujinaysaa Privileged EXEC Mode.
- Calaamadda `(config)#` waxay muujinaysaa Global Configuration Mode.
- `enable` wuxuu kuu gudbinayaa Privileged EXEC Mode.
- `configure terminal` wuxuu kuu gudbinayaa Global Configuration Mode.
- `exit` wuxuu dib kuu celinayaa hal heer.
- `end` ama `Ctrl + Z` waxay kuu celinayaan Privileged EXEC Mode.
- Calaamadda `?` waxay ku tusaysaa amarrada ka shaqaynaya heerka aad joogto.

---

# Su’aalo dib-u-eegis ah

1. Maxaa loola jeedaa Cisco IOS command hierarchy?
2. Waa maxay farqiga u dhexeeya User EXEC Mode iyo Privileged EXEC Mode?
3. Amarkee ayaa lagu galaa Privileged EXEC Mode?
4. Amarkee ayaa lagu galaa Global Configuration Mode?
5. Maxay calaamadaha `>`, `#`, iyo `(config)#` kala tilmaamayaan?
6. Waa maxay shaqada amarka `exit`?
7. Waa maxay farqiga u dhexeeya `exit` iyo `end`?
8. Interface Configuration Mode maxaa lagu qabtaa?
9. Sidee loo ogaadaa amarrada ka shaqaynaya heerka aad joogto?
10. Maxaa sababa fariinta `% Invalid input detected`?
