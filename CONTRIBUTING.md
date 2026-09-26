# 🤝 Sida wax loogu daro (Contributing)

Repo-gan waxaa loogu talagalay dhalinyarada Soomaaliyeed ee baranaysa CCNA. Kaalmo kasta waa la soo dhawaynayaa: sax af, sax farsamo, cashar cusub, lab cusub, ama tarjumaad.

## Waxaad samayn karto

| Nooca | Sida |
|---|---|
| **Khalad aad aragtay** (af, IP, command) | Fur **Issue** oo sheeg faylka iyo sadarka, ama toos u sax oo Pull Request soo dir. |
| **Cashar cusub** | Ku qor Markdown qaabka faylasha jira (eeg hoos). Sawirrada gali `images/<qaybta>-<magaca-casharka>/`. |
| **Lab cusub** | Ku dar liiska `LABS` ee `tools/build_labs.py` (magac, ujeeddo, tallaabooyin, xaqiijin), faylka `.pkt` gali, kadib `python tools/build_labs.py <folder> labs`. |
| **Su'aal** | Fur Issue oo cinwaan u dhig `Su'aal: ...`. |

## Qaabka casharka (Markdown)

```markdown
# Cinwaanka casharka

> **Qaybta:** 03-switching · **Xaaladda:** ✅ Dhammaystiran
> **Labs la xiriira:** [Lab 05 — VTP](../labs/05-vtp-server-client/README.md)

Sharaxaad Soomaali ah. Erayada farsamada (VLAN, trunk, subnet…) Ingiriisi ku hay.

## Cinwaan-hoosaad
- Qodob
- Qodob

Amarrada mar walba code block geli:

​```
Switch(config)# vlan 10
​```
```

## Xeerarka qoraalka

1. **Soomaali cad** — sida aad saaxiibkaa ugu sharxi lahayd, ma aha tarjumaad eray-eray ah.
2. **Erayada farsamada Ingiriisi ku hay** (router, subnet mask, trunk) si ardaygu imtixaanka u fahmo.
3. **Command walba code block** ku qor, prompt-ka la socda (`R1(config)#`).
4. **Tusaale IP** isticmaal kuwa loogu talagalay waxbarashada: `192.168.x.x`, `10.x.x.x`, `2001:DB8::/32`.
5. **Ha soo gelin** faylasha Cisco NetAcad (PDF-yada modules-ka, `.pka` la qiimeeyo) — waa copyright Cisco.

## Git

```bash
git checkout -b cashar-ospf        # branch cusub
git add .
git commit -m "Ku dar casharka OSPF (Af-Soomaali)"
git push origin cashar-ospf        # kadib fur Pull Request
```

Mahadsanid! 🙏
