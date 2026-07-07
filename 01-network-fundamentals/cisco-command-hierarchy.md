# Habraaca Amarka Cisco IOS — Cisco Command Hierarchy

## Ujeeddada

Cisco IOS waxay leedahay **levels kala sareeya** (command hierarchy) oo marba aad mid ka gashid adigoo qalabka maamuleysa. Heer kasta wuxuu leeyahay awoodiisa (permissions) gaarka ah — taa oo macnaheedu yahay in amarrada qaarkood ay ka shaqeynayaan oo keliya heer gaar ah, ee kale ma shaqeeyaan.

---

## Waa maxay Cisco IOS CLI Levels?

Cisco IOS CLI (Command Line Interface) waxay leedahay **6 heer (levels)** oo muhiim ah. Saddexda koowaad ayaa ugu badan la isticmaalaa maalinlaha:

| Prompt | Magaca Heerka | Sharaxaad |
|---|---|---|
| `Hostname>` | User EXEC Mode | Heerka ugu hooseeya — awood xaddidan |
| `Hostname#` | Privileged EXEC Mode (Enable Mode) | Heerka labaad — show commands iyo wax badan |
| `Hostname(config)#` | Global Configuration Mode | Heerka 3aad — meesha configuration-ka laga sameeyo |
| `Hostname(config-if)#` | Interface Configuration Mode | Heerka interface-ka gaar ah |
| `Hostname(config-router)#` | Router Configuration Mode | Heerka routing protocol-ka |
| `Hostname(config-line)#` | Line Configuration Mode | Heerka VTY, TTY, iyo async lines |

---

## Sidee Levels-ku u Shaqeeyaan?

### Heer 1 — User EXEC Mode

> **Calaamadda:** `Switch>`

Kani waa **heerka ugu hooseeya** ee aad gashid marka aad qalabka Cisco (switch ama router) u xidato. Heerkan:

- Waxaad fulin kartaa **amarrada kooban** oo aan qalabka beddelin waxba.
- Awood baadan **ma lihid** — si tusaale ah, ma arki kartid configuration-ka dhammaystiran.
- Lagu gartaa **magaca qalabka oo `>` ku xiga** (tusaale: `Switch>`).

**Si aad u ogaato amarrada aad fulin karto heerkan**, ku dhufo calaamadda su'aasha:

```cisco
Switch> ?
```

---

### Heer 2 — Privileged EXEC Mode (Enable Mode)

> **Calaamadda:** `Switch#`

Kani waa **heerka 2aad**. Si aad uga gudubto User EXEC Mode, waxaad qortaa amarka `enable`:

```cisco
Switch> enable
Switch#
```

Heerkan waxaad awoodaa:

- Fulinта **show commands** si aad u aragto xaaladda qalabka.
- Seegidda diiwaannada (logs) iyo dib-u-dejinta (reload).
- Galitaanka Global Configuration Mode.

**Si aad u ogaato amarrada aad fulin karto**, ku dhufo `?` kadibna riix Enter:

```cisco
Switch# ?
```

---

### Heer 3 — Global Configuration Mode

> **Calaamadda:** `Switch(config)#`

Kani waa **heerka 3aad** — halka ugu muhiimsan ee **configuration-ka laga sameeyo**. Si aad uga gudubto Privileged EXEC Mode, waxaad isticmashaa:

```cisco
Switch# configure terminal
Switch(config)#
```

Heerkan:

- Waxaad awoodaa **badbaadinta** (saving) iyo **beddel** qalabka oo dhan.
- Waana **halka ugu badan** ee amarrada configuration-ka lagu fuliyaa.
- Lagu gartaa in magaca qalabka oo `(config)#` ku xiga.

---

### Heerarka Hooseeya ee Configuration Mode

Ka dib marka aad Global Configuration Mode gasho, waxaad u gudbi kartaa heerarka hooseeya ee gaar ah:

**Interface Configuration Mode** — si aad u habaynto interface gaar ah:

```cisco
Switch(config)# interface GigabitEthernet 0/1
Switch(config-if)#
```

**Router Configuration Mode** — si aad u habaynto routing protocol:

```cisco
Router(config)# router ospf 1
Router(config-router)#
```

**Line Configuration Mode** — si aad u habaynto VTY ama console lines:

```cisco
Switch(config)# line vty 0 4
Switch(config-line)#
```

---

## Sidee Levels-ka Loo Baxo?

| Amarka | Waxuu Samaynaa |
|---|---|
| `exit` | Heer hoose ayuu ku noqdaa (mid) |
| `end` ama `Ctrl+Z` | Toos ayuu ugu noqdaa Privileged EXEC Mode |
| `disable` | Ka baxaa Privileged EXEC Mode oo User EXEC Mode ku noqdaa |

```cisco
Switch(config-if)# exit
Switch(config)# exit
Switch#
```

ama si degdeg ah:

```cisco
Switch(config-if)# end
Switch#
```

---

## Koobaynta Levels-ka (Sawirka Qaab-dhismeedka)

```text
Switch>                        ← User EXEC Mode        (Heer 1)
  └─ enable
Switch#                        ← Privileged EXEC Mode   (Heer 2)
  └─ configure terminal
Switch(config)#                ← Global Config Mode     (Heer 3)
  ├─ interface ...
  │   └─ Switch(config-if)#     ← Interface Mode
  ├─ router ...
  │   └─ Switch(config-router)# ← Router Mode
  └─ line ...
      └─ Switch(config-line)#   ← Line Mode
```

<!-- TODO: Add the original OneNote image here — save as: images/cisco-command-hierarchy-table.png -->

---

## Khaladaadka Caadiga ah

- **"Invalid input detected"** — Badanaa macnaheedu waa inaad heerka khaldan joogatid. Tusaale ahaan, aad `show running-config` ku dooneyso User EXEC Mode — waa inay ka shaqeysaa Privileged EXEC Mode keliya.
- **Inaad ilawdo heerka aad joogtid** — Fiiri prompt-ka si joogta ah: `>` waa User EXEC, `#` waa Privileged EXEC, `(config)#` waa Global Configuration.
- **`configure terminal` halkii `conf t`** — Labaduba waa sax. `conf t` waa gaaban (shorthand).

---

## Qodobbada Muhiimka ah

- Cisco IOS waxay isticmaashaa **hierarchical mode system** — si amarro kala sareeya heerarka kala duwan la siiyo.
- **`>`** = User EXEC | **`#`** = Privileged EXEC | **`(config)#`** = Global Configuration.
- Calaamadda **`?`** waa aalad caawinta — waqti kasta waad isticmaali kartaa si aad u ogaato amarrada heerka aad jooogtid.
- Heerka aad ka shaqeyso waa lagu gartaa **calaamadda (prompt)** ee ka horeysa meesha aad ku qortid.

---

## Su'aalo Dib-u-eegis ah

1. Cisco IOS levels-ka kala sareeya waa maxay, oo midkood midkood ka faraq waa maxay?
2. Sideed uga gudbi kartaa User EXEC Mode si toos ah Global Configuration Mode?
3. Heerka `Switch(config-if)#` waa maxay, oo goorma ayaad u baahan tahay?
4. Calaamadaha `>` iyo `#` xagee loo adeegsan karaa si loo garto heerka qofku joogaa?
5. Amarka `end` iyo `exit` farqigood waa maxay?
