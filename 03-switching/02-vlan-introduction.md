# VLAN-yada — waxa ay tahay inaad fahanto

> **Qaybta:** 03-switching · **Xaaladda:** ✅ Cashar dhammaystiran (laga soo guuriyay OneNote)
> **Labs la xiriira:** [Lab 03 — VLAN-yada iyo Access Ports](../labs/03-vlan-access-ports/README.md)


- Godka Switch-ka waxaan ka dhigi karnaa 4 xaaladood midkood:

- Access : oo micnihiisu Switch-ka god-kisa waxaa kaga soo xidhmaya qalab VLAN ka tirsan , oo ah end device

- Trunk : waa god aan wax VLANs ah ka tirsaneyn

- Dynamic trunk port : Wuxu ka jawaabaya su'ashan ah port-gani ma Access ayuu noqon mise Trunk

- Dynamic auto: lakin hadda godka xadhigisa laga dhigo dynamic auto, waxay ka dhigan tahay godkani waxa uu sugaya in computer-ka ku xidhani u soo sheego waxa uu noqon doono.

- Dynamic desirable : negotiation ayuu sameyn port-ga ku yaal switchka ee laga dhigay dynamic desirable , wuxu message u diri qalabka god-kas kaga soo xidhma, wuxuna weydiin war ma trunk baad noqon oo igula dhaqmi, qalab aanan ka tirsaneyn wax VLANs ah, mise mid kale  VLAN baad ka tirsantahayo Access baan ka dhignaa, Godka ayaana fariinta diraya oo diveces-ka kusoo xidhmaya negotition la sameynaya.

- VTP mode

- Access : wixi end device ahba waa access, waxa laga wadaa hadii aad ogtahay port hebel, in lagu xidhi doono ama uu ku soo xidhmi doono qalabyadi end devices-ka ahaa sida PC ama Server iwm godkaasi waa access.

- Dynamic Trunking Protocol : Wuxu ka jawaabaya su'ashan ah port-gani ma Access ayuu noqon mise Trunk

Tusale: laba switch oo kala ah Switch A iyo Switch B, oo midna yahay dynamic desrible ka kalena Dynamic auto hadi la isku xidho , markiba Switch A wuxu bilaabi negotition oo wuxu leyahy Switch B-yow aan Trunk noqono, Switch B, isna wuxu leyahay waa amarkaga, kadib natijadu waxay noqon Trunk formed

Switch A Switch B

Dynamic Desirable ← DTP → Dynamic Auto

Dynamic Trunking Protocol : waxaa jira 5 mode/hab/xaalad uu port-gu ku shaqeynayo :

1. Access : Port-ku wuxuu noqonayaa access port. Waxaa lagu isticmaalaa port-ka PC-ga.

Switch(config-if)# switchport mode access

PC → Access Port → VLAN 10

1. Trunk : Port-ku wuxuu noqonayaa trunk, xitaa haddii dhinaca kale aanu negotiation sameyn. Waxaa lagu isticmaalaa switch-to-switch links, switch to Router.

Switch(config-if)# switchport mode trunk

1. Dynamic Auto :Waa passive. Isagu trunk ma codsnayo, laakiin haddii dhinaca kale codsado wuu aqbalaya, fariintuna waxay ka imaan dhanka qalabka ee godka ku soo xidhmaya,

Switch(config-if)# switchport mode dynamic auto

1. Dynamic Desirable : Waa active. Wuxuu isku dayayaa inuu dhinaca kale la sameeyo trunk., farintuna waxay ka imaan dhanka port-ga ee laga dhigay dynamic desirable, wuxuna u diraya farin qalabka kuso xidhmaya fariintas oo loo yaqaan VTP(VLAN Trunk Protocol), wuxuna dhihi war ma end device ayad tahay oo VLAN ka tirsan oo waxan godka ka dhigaa Access, mise waxaad tahay qalab aan VLAN ka tirsaneyn oo godka Trunk ayan ka dhigaa

Switch(config-if)# switchport mode dynamic desirable

1. Nonegotiate : Wuxuu joojinayaa dirista DTP messages , Waxaa la isticmaalaa marka aad trunk ama access si manual ah u dejisay oo aadan rabin negotiation.

Switch(config-if)# switchport nonegotiate

- Xeerka muhiimka ah

Si trunk automatic ah u samaysmo, ugu yaraan hal dhinac waa inuu noqdaa:

- trunk, ama
- dynamic desirable

- Sidee baan u kala xulun, goormaanse waxan kala isticmalayaa

Access

- Hadii aad sii ogtahay qalabka god-kaas ku soo xidhmaya inuu end device yahay, waa inaad godkaas Access ka dhigtaa, maadama qalab-yadasi VLANs ka tirsanaan doonaan godkasi waa inuu ACCESS noqdaa.

Trunk

- Sido kale hadii aad sii ogsoontahay, god-kasi inuusan end device kuso xidhmeyn oo uusan VLAN ka tirsaneyn wa inaad Trunk ka dhigtaa

Dynamic diserible

- Hadi shirkadaad u shaqeyso ku dhahdo enginere god-kas configuration noogu same, adiguna ma ogid, god-kaas qalab noocee ah baa ku soo xidhmaya, marka adaa u kala doraya ma dynamic desirable baan ka dhigi mise Dynamic Auto

Created with OneNote.

---
_Qayb ka mid ah [CCNA Learning Journal — Af-Soomaali](../README.md). Khalad ama hagaajin: fur Issue ama Pull Request._
