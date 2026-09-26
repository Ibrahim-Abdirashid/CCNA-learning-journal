# 🛠️ Tools — qalabka repo-gan lagu dhisay

Scripts-kan waxaa loo isticmaalay in casharrada OneNote iyo labs-ka Packet Tracer si toos ah loogu beddelo Markdown. Waxaad u isticmaali kartaa repo-gaaga.

```bash
pip install -r tools/requirements.txt
```

| Script | Waxa uu qabto |
|---|---|
| `pkt2xml.py` | Faylka `.pkt` / `.pka` (Packet Tracer 7–9) wuxuu u beddelaa XML cad. `python tools/pkt2xml.py lab.pkt lab.xml` |
| `pkt_extract.py` | XML-ka wuxuu ka soo saaraa: qalabka, IP-yada, VLAN/VTP, xiriirinta, `running-config` qalab walba, iyo sawir `topology.svg`. `python tools/pkt_extract.py lab.pkt out_dir/` |
| `build_labs.py` | Wuxuu dhisaa folder-ka `labs/` oo dhan (README Soomaali ah lab walba) isagoo isticmaalaya liiska `LABS` ee gudihiisa ku qoran. `python tools/build_labs.py "<folder .pkt-yada>" labs` |
| `mht2md.py` | Bogagga OneNote ee loo dhoofiyay `.mht` wuxuu u beddelaa Markdown + sawirro la cadaadiyay. |

## Sida OneNote looga dhoofiyo (Windows)

OneNote COM API ayaa lagu dhoofin karaa bog walba `.mht` ahaan (Windows PowerShell 5.1):

```powershell
$on = New-Object -ComObject OneNote.Application
$s = ""; $on.GetHierarchy("", 4, [ref]$s); [xml]$h = $s
# ... dooro bogga, kadib:
$on.Publish($pageId, "C:\out\01 - Cinwaan.mht", 2, "")   # 2 = pfMHTML
```

Kadib:

```bash
python tools/mht2md.py "C:\out" md_out img_out ../images
```

## Fiiro gaar ah

- `pkt2xml.py` wuxuu ku salaysan yahay hab-furista uu qoray mashruuca [pka2xml](https://github.com/mircodz/pka2xml) (Twofish-EAX + zlib).
- Maktabadda `twofish` ee PyPI waxay isticmaashaa `imp` oo Python 3.12+ laga saaray. Haddii ay diido, fayl `twofish.py` ee site-packages ku beddel `import imp` → `import importlib.util` iyo `imp.find_module('_twofish')[1]` → `importlib.util.find_spec('_twofish').origin`.
