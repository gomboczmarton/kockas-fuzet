# A demó-videók esetleírásai

Kilenc rövid terminál-videó mutatja a Kockás Füzetet működés közben —
vágatlan, valódi munkamenetek, szintetikus mintaadatokkal, hétköznapi
personák szemével. A teljes lejátszási lista: **[Kockás Füzet — ami
visszaír, a YouTube-on](https://www.youtube.com/playlist?list=PLcXziGNgfisQ)**.

Ez a dokumentum esetenként (use-case-enként) halad: ki a szereplő, mi a
helyzete, mi történik a videóban, és mit bizonyít. A precíz elvárások és a
hangnem-rubrika forgatókönyvenként az [`evals/scenarios/`](../../evals/scenarios/)
mappában vannak; a videók lejátszó- és felvevő-eszközei a
[`demo/`](../../demo/) mappában.

---

## 1 · Telepítés — klónozástól az első zöld tesztig

**Ki és miért:** bárki, aki most találkozik a projekttel — nem programozó,
de a README két parancsát be meri másolni a terminálba.

**Mi történik:** letöltés (`git clone`), egy pillantás a mappára, majd a
beépített tesztek futtatása — mind zöld, még mielőtt bármit rábíznánk.
Végül az első beszélgetés a segéddel, aki bemutatkozik és felajánlja a
kipróbálást a szintetikus mintákkal.

**Mit bizonyít:** nincs telepítő, nincs regisztráció; a bizalom nem ígéret,
hanem lefuttatható teszt. *(Spec: [00-telepites](../../evals/scenarios/00-telepites.md) ·
[videó](https://youtu.be/xWI9hjcE8OI))*

## 2 · Első lépcső — bemásolós recept bármelyik AI-csevegőben

**Ki és miért:** Kata (34) még sosem használt AI-t pénzügyre; a 0. szintű,
telepítés nélküli utat próbálja ki.

**Mi történik:** Kata bemásol egy kész receptet és egy minta-kivonatot egy
csevegőbe → kategória-táblázat, top-3 kiadás, előfizetés-lista; majd a havi
terv-recepttel keretszámokat és SUMIFS-képletet kap, amit a saját
táblázatába illeszthet.

**Mit bizonyít:** a belépéshez elég 10 perc, és az ellenőrzés a
felhasználónál marad — a végösszeget a táblázat képlete adja, nem a csevegő
szövege. *(Spec: [01-elso-lepcso](../../evals/scenarios/01-elso-lepcso.md) ·
[videó](https://youtu.be/5O1Zu-_XRUA))*

## 3 · Kivonat-könyvelő — az új havi export lekönyvelése

**Ki és miért:** Gábor (41) havonta egyszer néz rá a pénzügyekre; most jött
meg az augusztusi banki export.

**Mi történik:** a segéd magától átalakítja a bank formátumát; a korábbi
hónapokból tanult kategóriákat nem kérdezi újra, a két ismeretlen partnert
egyetlen táblázatban kérdezi meg; egy júliusból ismétlődő sort
duplikátumként kiszűr; a végén az ellenőrző program számol újra, és a
tanult szabályok a naplóba kerülnek.

**Mit bizonyít:** a rendszer tanul, nem kérdez feleslegesen, és a
duplikátum-védelem miatt a kupacban érkező kivonat sem okoz kárt.
*(Spec: [02-kivonat-konyvelo](../../evals/scenarios/02-kivonat-konyvelo.md) ·
skill: `kivonat-konyvelo` · [videó](https://youtu.be/Kw6vG6kYpWQ))*

## 4 · Belefér? — gyors kép vásárlás előtt

**Ki és miért:** Réka (29) a boltban egy 89 000 forintos kerékpárt nézeget,
fél perce van dönteni.

**Mi történik:** a `/belefer` parancs az ellenőr számaiból tényszerű képet
ad — maradt keret, a vásárlás hatása, ítélet nélküli opciók. Réka kihagyja
a vásárlást; a megspórolt összeg kis győzelemként a naplóba kerül.

**Mit bizonyít:** a gép számol és felsorol, de nem mond se igent, se nemet
— a döntés végig a felhasználóé.
*(Spec: [03-belefer](../../evals/scenarios/03-belefer.md) · parancs:
`/belefer` · [videó](https://youtu.be/pRHHjknqvzc))*

## 5 · Havi zárás — az egész hónap egyetlen paranccsal

**Ki és miért:** Anna (38), a családi kassza gazdája, hónap végén egy
paranccsal akarja letudni a zárást.

**Mi történik:** a `/havizaras` lekönyveli a kivonatot, lefuttatja az
ellenőrt, majd kötött sorrendű zárást ad: egy jó dolog → eltérések
számokkal → legfeljebb két kérdés. A rendezvény-túllépésre rákérdez:
egyszeri volt? („Jubileum.") A döntések a naplóba kerülnek, és elkészül az
offline HTML-riport.

**Mit bizonyít:** a hónap végi szembenézés kép, nem ítélet — a túllépés
kérdés, sosem vád.
*(Spec: [04-havizaras](../../evals/scenarios/04-havizaras.md) · parancs:
`/havizaras` · [videó](https://youtu.be/njxDEUfezhI))*

## 6 · Havi terv — a következő hónap a saját számokból

**Ki és miért:** Bence (33) három hónapja vezeti a kasszát, most először
tervez előre.

**Mi történik:** a segéd hónaponként lefuttatja az ellenőrzőt, evidenciával
javasol kereteket, és egyetlen kérdést tesz fel: mi lesz szokatlan? A
szülinap és az éves biztosítás beépül, elkészül az augusztusi terv-fájl —
a megtakarítás a hónap elejére tervezve.

**Mit bizonyít:** a terv a felhasználó tényadataiból készül, nem sablonból,
és minden számról látszik, honnan jött.
*(Spec: [05-havi-terv](../../evals/scenarios/05-havi-terv.md) · skill:
`havi-kor` · [videó](https://youtu.be/kBSXCizUs9U))*

## 7 · Visszatérés — kihagyott hónapok, szemrehányás nélkül

**Ki és miért:** Dóri (36) május óta nem nyitotta ki a füzetet; kicsit
szabadkozva tér vissza.

**Mi történik:** az első mondat a visszatérést ünnepli, nem a hátralékról
szól. Helyzetkép öt sorban, két hónap kivonata egy menetben lekönyvelve, a
kérdések egyetlen körben, hónaponként kétsoros gyorszárás — a végén friss
start.

**Mit bizonyít:** a rendszerek jellemzően a kimaradás utáni rossz érzésnél
halnak el — itt a visszatérés győzelem, és a bepótlás rövid.
*(Spec: [06-visszateres](../../evals/scenarios/06-visszateres.md) · skill:
`visszateres` · [videó](https://youtu.be/PsBXVs3cRG4))*

## 8 · Előfizetés-vadászat — mire ment el a legtöbb?

**Ki és miért:** Péter (45) gyanítja, hogy fizet valamiért feleslegesen.

**Mi történik:** a segéd a három hónap adatából kimutatja az ismétlődő
előfizetéseket és a legnagyobb kiadásokat, hónaponként az ellenőrző
számaival; az éves megtakarítást ellenőrizhető számítás adja, aminek a
módja is látszik. A lemondás Péter dolga marad.

**Mit bizonyít:** „a robot ne fejszámoljon" szabály élesben — és az
elfelejtett előfizetés információ, nem hanyagság.
*(Spec: [07-elofizetesek](../../evals/scenarios/07-elofizetesek.md) ·
[videó](https://youtu.be/vHRjMtXgX9I))*

## 9 · Írd fel! — készpénzes költés rögzítése menet közben

**Ki és miért:** Juli (31) a piacról hazafelé, blokk a zsebében; nem akar
hazaérve gépelni.

**Mi történik:** egyetlen mondat („4 300 forint készpénzből, zöldség — írd
fel"), a tétel a kasszába kerül, az ellenőrzés automatikusan lefut, és az
új „bemondós blokk" szabály a naplóba kerül — legközelebb kérdés nélkül
megy. A készpénz-kettősség kérdését a rendszer megbeszéli, nem elmaszatolja.

**Mit bizonyít:** így tanul a rendszer új szokást programozás nélkül —
elmondod magyarul, és beépül.
*(Spec: [08-gyorsrogzites](../../evals/scenarios/08-gyorsrogzites.md) ·
[videó](https://youtu.be/IOrEgfLit98))*
