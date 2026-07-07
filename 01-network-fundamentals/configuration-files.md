# Faylasha Habaynta — Configuration Files

> **Xaaladda:** ✅ Dhammaystiran

---

Cisco devices sida routers, switches waxa jira files ay ugu keydsan yihiin amara kala duwan ee ka shaqeynaya devices-kas, amaradasi ha noqdaan kuwo adigu aad sameyneyso am kuwa shirkaddu soo siisayba.

Waxana jira laba feyl oo lagu kala keydiyo amaradaas oo kala ah:

---

## 1. Running Configuration (`running-config`)

File-ka **running-config** waxa ku keydsan amarada lagu shaqeynayo kuwaas oo ah kuwa markaas la qorayo. Hadii aan la save gareyn, ay amaradaasi lumi karaan hadii qalabkasi uu dumo ama wax kale dhacaan xogtaasi waa ku deysey.

**Si aad u chake gareyso file-kan running configuration-ka waxad qortaa adigoo jooga level-ki 2aad ee privilege mode-ka:**

```
ALS-1# show running-config
```

### Astaamaha Muhiimka ah (Key Characteristics)

| Astaame | Faahfaahin |
|---------|-----------|
| **Volatile** | Running config waxa lagu kaydiyaa RAM-ka device-ka, taas oo ka dhigaysa mid aan xasilloonayn. Waxay lumaan hadii device-ku dib u bilaabo ama la damiyaa. |
| **Dynamic** | Wax kasta oo lagu sameeyo habaynta device-ka isla markiiba ayay ku muuqdaan running config-ga. |
| **Temporary** | Isbeddelada running config-ga looguma keydiyo si joogto ah haddaan gaar ahaan loogu keydin startup config-ga. |

> 📝 **Xusuusnow:** Running config waxa ku jira amarada *hadda* shaqeynaya — waa "xaaladda nololeed" ee device-ka.

---

## 2. Startup Configuration (`startup-config`)

File-ka **startup-config** waxa inogu keydsan amarada sida **permanent**-ga ah — astaamihisuna waxay caksi ku yihiin kii running-ka.

- Markaad qalabka **is baddal amar** ah ku sameyso markiba laguma save gareyo startup-ka. Ee waxa lagu save gareyaa running-ka, kadib adaa u wareejinya startup-ka.
- **Si aad u chake gareysi file-ka startup-ka waxad qortaa:**

```
ALS-1# show startup-config
```

### Astaamaha Muhiimka ah (Key Characteristics)

| Astaame | Faahfaahin |
|---------|-----------|
| **Non-volatile** | Startup config waxa lagu kaydiyaa NVRAM, taas oo ilaalisa waxa ku jira xitaa markii device-ka la damiyaa. |
| **Static** | Waxa aan isbeddelin ilaa running config-ga si gaar ah loogu keydiyo. |

> 📝 **Xusuusnow:** Startup config waa "habayntii ugu dambaysay ee la keydinayay" — waa waxa device-ka raacaya marka dib loo bilaabo.

---

## Sida Loo Keydiyo Running-Config → Startup-Config

Marka aad dooneyso amaradii running-ka ku jiray in loo wareejiyo startup-ka waxaad sameynaysaa labadan amar midkood:

### Amarka 1aad — `copy`

```
ALS-1# copy running-config startup-config
```

### Amarka 2aad — `write memory`

```
ALS-1# write memory
```

> ⚠️ **Digniin:** Haddaadan keydinin (save gareyn) running-config-ga startup-config-ga, amaradaada oo dhan ayaa lumi doona markii device-ku dib u bilaabo!

---

## Koobid — Summary

```
Device RAM  ──►  running-config   (volatile  — lost on reboot)
Device NVRAM ──► startup-config   (non-volatile — kept on reboot)

copy running-config startup-config   ──►  saves changes permanently
write memory                         ──►  same effect (shortcut)
```

---

*Xog la soo daray: 2026-07-07 | Qayb: 01 - Network Fundamentals*
