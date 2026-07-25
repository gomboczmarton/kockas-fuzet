# Vizuális nyelv (DESIGN.md)

A Kockás Füzet ábráinak, riportjainak és slide-jainak közös szabályrendszere.
Cél: a grafika ugyanazt mondja, amit a hangnem-szabályok — **a szám
ellenőrizhető, a hiba nem szégyen, a döntés a felhasználóé.**

## Szín-paletta

| Név | Hex | Mire |
|---|---|---|
| papír | `#FBF9F1` | füzetlap-felületek, kártyák belseje |
| lap | `#FDFCF8` | ábra-háttér (README-ben világos módban) |
| tábla | `#F2EFE6` | oldal-háttér (deck, riport) |
| keret | `#CFC8B5` / `#DCD7C8` | vonalak, kártya-szegély |
| rács | `#E3EBF0` | a kockás papír vonalhálója (24 px) |
| tinta | `#23231F` | főszöveg |
| halk tinta | `#4A4740` / `#6B675E` | másodlagos szöveg, mono feliratok |
| jelölés | `#A09A89` | sorszámok, apró címkék |
| zöld | `#3F6B52` | rendben / ellenőrizve / akcentus |
| világoszöld | `#8FB39C` | kereten belüli érték, kitöltött hónap |
| sárga | `#E8C76A` (`#C9A642`) | túllépés, eldöntésre váró tétel |
| semleges rúd | `#C9C2AE` | „régi módszer" adatsor |

**Piros nincs a palettában.** Ez nem esztétikai, hanem hangnem-döntés: a
túllépés információ, nem kudarc (lásd `skills/havi-kor/SKILL.md`). Ha valami
figyelmet kér, sárga és kérdés formájában kér.

## Betűk

- Címek, mondatok: `Georgia, 'Times New Roman', serif` — a füzetbe írt kéz
  nyugalma, és minden gépen ott van (a README-SVG-k nem tölthetnek le fontot).
- Számok, fájlnevek, technikai címkék: `ui-monospace, 'SF Mono', Menlo,
  Consolas, monospace` — ami gépből jön, monospace-ben jelenik meg.

Egyszerű szabály: **amit a gép számolt, az mono; amit ember mond, az serif.**

## Motívumok

1. **Kockás rács** — 24 px-es háló, csak ott, ahol „papírt" mutatunk
   (banner, füzetlap-nézet). Nem dekoráció: ez a márka.
2. **Négyzet = egy hónap.** Kitöltött = könyvelt, szaggatott = kihagyott,
   sötétzöld pipával = most bepótolt.
3. **Szalag = keret.** Világoszöld a tény, sárga a túllépés, világos alap a
   maradék keret.
4. **Pecsét = eredet.** Minden generált szám alatt ott a forrás
   (`ellenorzo.py`, dátum). Két állapot van: ellenőrizve, illetve döntést kér.
5. **Nincs ikonkészlet, nincs illusztráció, nincs emoji.** Négyszög, kör,
   vonal, szöveg — ennyi.

## Fájlok

```
assets/
  banner.svg / banner-dark.svg   README-fejléc (<picture>-rel váltakozik)
  harom-szabaly.svg              a három alapszabály
  harom-lepcso.svg               belépési térkép (10 perc → saját gép)
  hogolyo.svg                    miért bukik el a követés
  terv-teny.svg                  havi terv–tény szalag (sárga túllépés)
  ellenor-pecset.svg             ellenőrizve / döntést kér
  fuzetlap.svg                   a kassza mint füzetlap, képlet-sorral
  belefer-kartya.svg             /belefer parancs kimenete kártyán
  visszateres-naptar.svg         kihagyott hónapok bepótolva
  deck-layoutok.svg              a négy slide-sablon
  riport-anatomia.svg            a generált havi riport szerkezete
templates/riport-sablon.html     kitöltendő, offline havi riport
docs/oktatas/oktato-deck.html    egyfájlos oktató bemutató
```

## Ha új ábrát készítesz

- Statikus SVG, **script és külső font nélkül** (a GitHub kiszűri őket).
- Saját háttér-négyszög minden ábrán (`#FDFCF8`), hogy sötét GitHub-témában
  is olvasható legyen; sötét változat csak a bannernek van.
- `role="img"` + `aria-label` a teljes állításról — a képnek szövegként is
  el kell mondania a lényeget.
- Szélesség 1200 px (kártyáknál 900–1000), a magasság a tartalomtól.
- A számok a `examples/GROUND-TRUTH.md` minta-adatából jöjjenek, ne
  kitaláltak legyenek — így az ábra és az eval ugyanazt mutatja.

## A négy slide-layout

1. **Cím-lap** — nagy serif cím, zöld alávonás, semmi más.
2. **Anekdota-lap** — egy konkrét eset, folyó szöveg, dőlt bevezetővel.
3. **Szabály-lap** — az egyetlen színes (világoszöld hátterű) layout: egy
   mondat, nagyban. Legfeljebb 3–4 ilyen egy bemutatóban.
4. **Ábra-lap** — egy `assets/` ábra, egy mondat alatta.

Minimum betűméret 1920×1080-on: 28 px (mono címke), 40 px (szöveg).
