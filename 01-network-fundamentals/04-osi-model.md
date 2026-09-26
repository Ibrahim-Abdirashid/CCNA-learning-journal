# OSI Model — 7-da Lakab

> **Qaybta:** 01-network-fundamentals · **Xaaladda:** ✅ Cashar dhammaystiran (laga soo guuriyay OneNote)
> **Labs la xiriira:** —


Si'ay laba computer u wada xidhiidhaan oo wax iskugu diraan waxaa jirta standards ay khasab tahay in la raaco si uu u dhaco wada xidhiidh-kaasi waxaana loo yaqaan OSI (Open System Model) , waxaana diyaariyay Organization-ka la yidhaahdo ISO

Tusaale: hadii aad heysato laba computer oo kala ah Hp iyo Dell iskuma xidhmeen haddii uusan jiri lahayn OSI Model-kan.

- Wuxuuna ka koobanyahay 7 layers, sidoo kalena waa standards-kii ugu horeeyay ee ay shirkaduhu isku raaceen in la hir galiyo si uu laba computer u wada xidhiidhaan, waxaa hadda jira oo la isticmaalaa ka la yidhaahdo TCP/IP Model

- 7 layers-kasi waxay suurta galinayaan inaad Muuqaal youtube-ka yaal aad daawan karto ama saxibka aad fariin u diri karto

- Marka aad rabto saxibka inaad warqad u dirto ama message u dirto waxay maraysa 7-layers-kan waxaana laga soo bilaabaa kor ilaa hoos ayay usocon:

Layer 7: Application Layer: waa marka aad dooneyso inaad la falgasho software tusaale: markaad rabto inaad website booqato oo aad tagto chrome-ka oo aad qorto [www.bbc.com](http://www.bbc.com) kaasaa wuxuu noqonayaa applicatioin layer.

- Wuxuuna isticmaalaa protocols-kan sida HTTP, HTTPS, SMTB(email), DNS, FTP, DHCP

- Sidoo kale xog hadaad dirto sida sawir oo kale application layer-ku wuxu xogti ka dhigaya wax loo yaqaan Encapsulation si'uu networku u fahmo isago isticmalaya protocols-ki kala duwana sida HTTP ama SMTP, sido kale layer walba marka wuxuu xogtii aad dirtay ku darayaa wax la yidhaahdo header.

- Taas cagsigeed markii xogtii la diray ay gaadho cidii loo diray, oo saxibka farinti kugu soo celiyo waxa ku dhacaysa xogtii wax loo yaqaan De-Encapsulation, oo xogtii la diray layer walba wuxu ka furayaa header-ki uu marki hore xogta ku daray xogtuna waxay noqon hoos iney ka soo bilabato oo kor uso kacdo layer physical to application layer.

- Header- nooca fariinta iyo protocol-ka la istimaalayo weeye waxa laga wado marka layer walba xogta intas buu ku dari.

Layer 6: Presentation Layer: isagu waa Translater, xogtii lasoo diray ayuu translate ku sameyn, qoraal baad iska soo dirtay oo saxibka u dirtay, markaa layer-kan ayaa xogtii ku sameyn translate oo format gaar ah oo uu receiver-ku ama cidii loo diray ay fahmi kareyso.

- Sida in xogtii encryption laga dhigo ama decryption
- Key protocols-ka uu isticmalo: SSL/TSL (security), JPEG, GIF

Layer 5: Session Layer: waxan dhihi karnaa shaqadiisu waa managing, inta badana saddexdan layer waxaa isticmaala qofka developer-ka ah,

- Session, wuxuu noqon karaa websites-ka qaar ee security-godu sareyo waxaa dhacda hadii adoo ku dhex jira muddo dhowr daqiiqo oo kale oo aadan wax action ahba sameyn inuu website-kasi is xidho oo uu login kuu diro.

Layer 4: Transport Layer: shaqadisa ugu weyn waa inuu labadi dhinac isku xidho, waa in data-dii lakala jajabiyo, xogti aad dirtay ayaa laga dhigayaa segments, taasoo fudeyd noqoneysa in xogta la diro meeshii loo direyna ay si fudud ku gaadho.

- Shaqada ugu muhimsan waxa weye uu layer-kani sameyn karo, inuu fuliyo in application fara badan ay isticmali karan hal connection, sida in hal computer aad hal mar shaqooyin badan ku wada qabsan kartid sida inaad dhowr application hal mar wada isticmaali kartid iyagoo aanan wax isku dhac ah aaney jirin wuxuuna siiyaa application walba wax loo yaqaan port numbers

- Protocols-ka uu isticmalana waxa ka mida: TCP iyo UPD

Layer 3: Network Layer: qalabkan shaqadisu waa Routing, oo ah in qalabyadii networks-ka kala duwan ku jiray in fariimaha loo kala qaado lana marriyo waddada ugu haboon ee ugu dhow.

- Qalab kastana wuxuu heystaa logical address sida IP address, looguna talo galay in la ogaado in qalab hebel networka xagee ayuu ka joogaa.
- Key devices-ka ugu muhiimsan ee lagu isticmaalo waxaa ka mid ah Router-ka.

Layer 2: Data Link Layer: wuxuu inoo suurto galinayaa iney wada xidhiidhaan qalabyada gaar ahaan kuwa isku network ku wada jira.

- Sido kale wuxu masuul ka yahay inuu fariimaha ka check gareeryo wixii cillad ah ee farimaha la socda

- Sidoo kale wuxu isticmaalaa address kaas oo la dhaho MAC adress, kaas oo ah ID unique ah oo uu qalab walba leeyahay.

- MAC Address magacyadisa kale ee loo yaqaan waxaa ka mida physical address , Burn-in address, layer 2 address

Layer 1: Physical Layer : layer-kan wuxuu masuul ka yahay inuu fariinta u diro iyadoo binary ah isagoo sii dhex marinaya hadba mediaha la isticmaalay sida copper, ama fiber obtic ama twisted pair

Created with OneNote.

---
_Qayb ka mid ah [CCNA Learning Journal — Af-Soomaali](../README.md). Khalad ama hagaajin: fur Issue ama Pull Request._
