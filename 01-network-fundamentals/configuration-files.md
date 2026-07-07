# Faylasha Habaynta Cisco IOS  
### Configuration Files

> **Xaaladda:** ✅ Dhammaystiran

Cisco routers iyo switches waxay leeyihiin faylal lagu kaydiyo amarrada iyo dejimaha qalabka (**configuration**).

Marka aad qalabka configure-garayso, amarrada aad geliso waxay ku kaydsamaan mid ka mid ah laba fayl:

1. **Running Configuration — `running-config`**
2. **Startup Configuration — `startup-config`**

Labadan fayl shaqooyin kala duwan ayay qabtaan, waana muhiim in la fahmo farqiga u dhexeeya.

---

## 1. Running Configuration — `running-config`

`running-config` waa configuration-ka qalabku **hadda isticmaalayo**.

Marka aad amar ku qorto Cisco IOS, isbeddelkaasi isla markiiba wuxuu galayaa `running-config`, qalabkuna wuxuu bilaabayaa inuu ku shaqeeyo.

Tusaale ahaan:

```cisco
hostname SW1
```

Markaad amarkan geliso, magaca switch-ku isla markiiba wuxuu isu beddelayaa `SW1`.

### Sida loola socdo ama loo ogaado meesha ay wax marayaan iyo shaqooyin kaad qabatay

Waxaad `running-config` ku arki kartaa amarkan:

```cisco
show running-config
```

Ama qaabka loo soo gaabiyo:

```cisco
show run
```

### Halkee lagu kaydiyaa?

`running-config` waxaa lagu kaydiyaa **RAM**.

RAM-ku waa xasuus ku-meel-gaar ah. Marka qalabka la damiyo ama dib loo daaro oo la reload gareeyo, xogta ku jirta RAM way ku deysay.

### Astaamaha muhiimka ah

| Astaanta | Sharaxaadda |
|---|---|
| **Active** | Waa configuration-ka uu qalabku hadda ku shaqaynayo |
| **Dynamic** | Isbeddel kasta oo aad samayso isla markiiba ayuu ku muuqdaa |
| **Volatile** | Wuxuu tirmayaa marka qalabka la damiyo ama dib loo soo kiciyo |
| **Temporary** | Isbeddelladu joogto ma noqdaan ilaa la kaydiyo |

> **Xusuusnow:** `running-config` waa xaaladda uu qalabku hadda ku sugan yahay.

---

## 2. Startup Configuration — `startup-config`

`startup-config` waa configuration-ka la kaydiyey ee qalabku isticmaalo marka uu shidmayo ama dib loo bilaabayo.

Waxaa lagu kaydiyaa **NVRAM**.

NVRAM waa xasuus aan xogteedu lumin marka qalabka la damiyo.

### Side u arki kartaa shaqadi aad fulisay 

```cisco
show startup-config
```

Ama:

```cisco
show start
```

### Astaamaha muhiimka ah

| Astaanta | Sharaxaadda |
|---|---|
| **Saved** | Waxa ku jira configuration-kii ugu dambeeyey ee la kaydiyey |
| **Non-volatile** | Xogtu ma tirmayso marka qalabka la damiyo |
| **Boot configuration** | Qalabku wuxuu akhriyaa marka uu shidmayo |
| **Persistent** | Wuxuu sii jirayaa ilaa si ula kac ah loo beddelo ama loo tirtiro |

> **Xusuusnow:** `startup-config` waa configuration-ka qalabku ku bilaabanayo marka uu mar kale shidmo.

---

# Farqiga u dhexeeya labada fayl

| Qodobka | `running-config` | `startup-config` |
|---|---|---|
| Waxa uu matalo | Configuration-ka hadda shaqaynaya | Configuration-ka la kaydiyey |
| Halka lagu kaydiyo | RAM | NVRAM |
| Marka qalabka la damiyo | Wuu tirmayaa | Wuu sii jirayaa |
| Isbeddelku goorma ayuu galaa? | Isla markiiba | Marka la kaydiyo |
| Amarka/command-ga aad kula socon karto | `show running-config` | `show startup-config` |

---

# Sida loo kaydiyo Running-Config

Marka aad configuration cusub samayso, wuxuu marka hore galayaa `running-config`.

Si isbeddelladaasi u sii jiraan marka qalabka dib loo damiyo oo loo daaro, waa inaad u kaydisaa `startup-config`.

Waxaa jira laba amar oo caadi ahaan loo isticmaalo.

## Habka 1: `copy running-config startup-config`

```cisco
copy running-config startup-config
```

Qaabka gaaban:

```cisco
copy run start
```

Marka lagu weydiiyo magaca faylka destination-ka:

```text
Destination filename [startup-config]?
```

Riix **Enter**.

Amarkani wuxuu nuqul ka sameeyaa `running-config`, wuxuuna ku kaydiyaa `startup-config`.

---

## Habka 2: `write memory`

```cisco
write memory
```

Qaabka gaaban:

```cisco
wr
```

Amarkani wuxuu qabtaa shaqo la mid ah:

```cisco
copy running-config startup-config
```

> **Fiiro gaar ah:** `copy running-config startup-config` ayaa ah amarka rasmi ahaan loo doorbido. `write memory` waa amar hore oo weli ka shaqeeya qalab badan oo Cisco ah.

---

# Maxaa dhacaya haddii aan la kaydin?

Tusaale ahaan, waxaad samaysay:

```cisco
hostname SW1
interface gigabitEthernet 0/1
 no shutdown
```

Qalabku isla markiiba wuu ku shaqaynayaa dejimahaas, sababtoo ah waxay ku jiraan `running-config`.

Laakiin haddii aad dib udamiso oo u daarto   adigoon kaydin:

```cisco
reload
```

isbeddelladaas way luminayaan.

Sababtu waa:

```text
running-config → RAM → wuu tirmayaa marka qalabka dib loo soo kiciyo
```

Si aanay u lumin, kaydi:

```cisco
copy running-config startup-config
```

---

# Tusaale tallaabo-tallaabo ah

## 1. Samee configuration

```cisco
enable
configure terminal
hostname SW1
interface gigabitEthernet 0/1
 description Link-to-Router
 no shutdown
end
```

## 2. Hubi configuration-ka shaqaynaya

```cisco
show running-config
```

## 3. Kaydi isbeddellada

```cisco
copy running-config startup-config
```

## 4. Hubi configuration-ka la kaydiyey

```cisco
show startup-config
```

Hadda, xitaa haddii switch-ka inta la damiyo haddana  dib loo daaro, configuration-ku wuu sii jiri doonaa.

---

# Khaladaadka caadiga ah

## 1. Configuration la sameeyo laakiin aan la kaydin

Tani waa khaladka ugu badan.

Qalabku wuu shaqaynayaa, laakiin marka la sameeyo `reload`, dhammaan isbeddellada cusub way luminayaan.

Xalka:

```cisco
copy running-config startup-config
```

---

## 2. In la moodo in `running-config` si joogto ah u kaydsan yahay

`running-config` wuxuu ku jiraa RAM oo keliya.

```text
RAM = xasuus ku-meel-gaar ah
```

Sidaas darteed, si joogto ah uma sii jirayo marka qalabka la damiyo.

---

## 3. In la isku khaldo amarrada `show run` iyo `show start`

```cisco
show running-config
```

Wuxuu ku tusayaa configuration-ka hadda shaqaynaya.

```cisco
show startup-config
```

Wuxuu ku tusayaa configuration-ka ugu dambeeyey ee la kaydiyey.

Labada fayl mararka qaarkood way kala duwanaan karaan haddii isbeddello cusub aan weli la kaydin.

---

# Sida loo ogaado in isbeddellada la kaydiyey

Waxaad isbarbardhigi kartaa:

```cisco
show running-config
```

iyo:

```cisco
show startup-config
```

Haddii ay kala duwan yihiin, waxay ka dhigan tahay in `running-config` uu leeyahay isbeddello aan weli loo kaydin `startup-config`.

Markaas isticmaal:

```cisco
copy running-config startup-config
```

---

# Koobid

```text
RAM
└── running-config
    ├── Waa configuration-ka hadda shaqaynaya
    ├── Isbeddelladu isla markiiba ayay galaan
    └── Wuu tirmayaa marka qalabka dib loo bilaabo

NVRAM
└── startup-config
    ├── Waa configuration-ka la kaydiyey
    ├── Waxaa la akhriyaa marka qalabku shidmayo
    └── Ma tirmayo marka qalabka la damiyo
```

Si aad configuration-ka u kaydiso:

```cisco
copy running-config startup-config
```

Ama:

```cisco
write memory
```

---

# Qodobbada muhiimka ah

- `running-config` waa configuration-ka qalabku hadda isticmaalayo.
- `running-config` waxaa lagu kaydiyaa RAM.
- `startup-config` waa configuration-ka qalabku ku bilaabanayo.
- `startup-config` waxaa lagu kaydiyaa NVRAM.
- Isbeddellada cusub marka hore waxay galaan `running-config`.
- Isbeddelladu ma sii jiri doonaan ilaa loo kaydiyo `startup-config`.
- Amarka ugu muhiimsan ee kaydintu waa:

```cisco
copy running-config startup-config
```

---

# Su’aalo dib-u-eegis ah

1. Waa maxay `running-config`?
2. Waa maxay `startup-config`?
3. Halkee lagu kaydiyaa `running-config`?
4. Halkee lagu kaydiyaa `startup-config`?
5. Maxaa ku dhacaya `running-config` marka qalabka dib loo bilaabo?
6. Amarkee ayaa lagu daawadaa configuration-ka hadda shaqaynaya?
7. Amarkee ayaa lagu daawadaa configuration-ka la kaydiyey?
8. Sidee `running-config` loogu kaydiyaa `startup-config`?
9. Maxay ku kala duwan yihiin RAM iyo NVRAM?
10. Maxaa dhici kara haddii configuration-ka aan la kaydin?

---

*update: 2026-07-07 | Qaybta 01 — Network Fundamentals*
