# Cikk → demó térkép

A két cikkvázlat (a personal-finances-and-ai-agents repóban:
`article/drafts/2026-07-23-ai-csaladi-koltsegvetes-kiszamolo-stilus.md` és
`article/drafts/2026-07-23-csevegotol-az-ugynokig-kiszamolo-stilus.md`)
jelenetei és a demó-forgatókönyvek megfelelése. A cél: minden cikkbeli
állítás mögé odatehető legyen egy vágatlan videó.

## 1. cikk — „Rendbe rakja-e az AI a pénzügyeidet?"

| Cikk-jelenet | Demó | Megjegyzés |
|---|---|---|
| Nyitó anekdota: havi zárásnál a gép rákérdez a 15 ezres rendezvényre; „jubileum, egyszeri" | **04-havizaras** | a demó kelléke szándékosan ugyanez a tétel (HAVI RENDEZVENY 15 000, keret 10 000) és ugyanez a párbeszéd |
| Blokkfotó → kategorizálva a költségvetésbe | **08-gyorsrogzites** | terminál-demóban bemondott blokk; a fotós út a csevegős 1. lépcső |
| Havi büdzsé összerakása a saját számokból | **05-havi-terv** | |
| Nyaralás-költségterv oda-vissza | — | a `nyaralas-tervezo` skill M3-as stub; demó a kidolgozásakor készül |
| Kivonat-elemzés: mire ment a legtöbb, elfelejtett előfizetések | **01-elso-lepcso** (0. szint) és **07-elofizetesek** (harness-szint) | |
| 1. lépcső: kivonat bemásolva, 10 perc | **01-elso-lepcso** | |
| 2. lépcső: havi rutin (terv + zárás) | **05-havi-terv** + **04-havizaras** | |
| 3. lépcső: nyílt, letölthető rendszer a saját gépen | **00-telepites** (és az összes 02–08) | |
| „a robot ne fejszámoljon" szabály | minden demó | minden összeg az `ellenorzo.py`-ból; a 07-ben kimondott próba is |

## 2. cikk — „Amikor a robot már a naptáradba ír"

| Cikk-jelenet | Demó | Megjegyzés |
|---|---|---|
| Attila: PDF-összehasonlítás + naptárba írt emlékeztető | — | connector-függő (naptár/Drive-összekötés a csevegőben) — kívül esik a repo terminál-demóin; a cikk 2. lépcsős jelenete |
| Havi kör: terv az elmúlt 3 hónapból; zárásnál csak az eltérések | **05-havi-terv**, **04-havizaras** | |
| „Belefér-e egy 89 ezres kerékpár?" | **03-belefer** | a demó szó szerint a cikk példáját játssza |
| Éves tételek (biztosítás, matrica) beépítése | **05-havi-terv** | a 2. körben épül be az éves lakásbiztosítás |
| Visszatérés kihagyás után, szemrehányás nélkül | **06-visszateres** | |
| Nyaralás-tervező („írd a nyaralás-fülre: 68 euró") | **08-gyorsrogzites** (a rögzítés-minta) | maga a skill M3-as stub |
| „elmondod magyarul, és beépül" (készpénzes blokk példa) | **08-gyorsrogzites** | a szabály a naplóba kerül — a demó a recept-tanulás útját mutatja |
| „a pénzedhez nem nyúl" határ | minden demó | a 03/07-ben explicit: a rendszer nem dönt és nem intézkedik |

## Nyelvi követelmény

Minden demó-interakció **magyarul** zajlik (persona-üzenetek és válaszok
egyaránt) — ez a forgatókönyvek közös, kötelező eleme.
