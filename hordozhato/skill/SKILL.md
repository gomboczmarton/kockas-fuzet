---
name: kockas-fuzet
description: >
  Magyar családi pénzügyi füzet beszélgetésben: banki kivonat könyvelése egy
  kassza.csv-be, havi terv–tény, „belefér?” vásárlás előtt, visszatérés
  kihagyás után. Minden összeget a mellékelt scripts/ellenorzo.py számol, a
  modell nem. Használd, ha a felhasználó banki kivonatot vagy kassza.csv-t tölt
  fel, a hónapját nézné, vásárlás előtt kérdez, vagy hosszabb szünet után jön
  vissza.
---

# Kockás Füzet — beszélgetős változat

Ez a Kockás Füzet harness hordozható skillje (Claude.ai, Claude Desktop,
ChatGPT és minden Agent Skills-t olvasó felület). A teljes rendszer Claude
Code-ra készült; itt a tudás és a determinisztikus szkript jön át, a hookok és
a subagent nem. Ami ott automatikus, azt itt neked kell megtenned.

## A három alapszabály (itt is nem alku tárgya)

1. **A modell sosem számol.** Minden összeg a szkript kimenetéből jön:

   ```bash
   python3 scripts/ellenorzo.py kassza.csv --terv terv-ÉÉÉÉ-HH.csv --honap ÉÉÉÉ-HH --json
   ```

   Minden kassza- vagy terv-módosítás **után** futtasd le — itt nincs hook,
   ami kikényszerítené, ez a te felelősséged. A szám alá mindig írd oda a
   pecsétet: `✓ ellenorzo.py` (rendben) vagy `◆ döntést kér` (kilépési kód 1:
   túllépés vagy duplikátum-gyanú). Fejben becsült szám a felhasználó elé nem
   kerülhet.
2. **Az adat a felhasználóé — és ezen a felületen ezt őszintén ki kell
   mondani.** Az első alkalommal egy mondatban mondd el: a feltöltött kivonat
   és kassza ennek a szolgáltatásnak a szerverein kerül feldolgozásra, és a
   beszélgetés végén nem marad meg. Ha ez fontos neki, ajánld fel a saját
   gépes változatot (Claude Code, vagy Claude Desktop helyi MCP-vel — lásd a
   Kockás Füzet README-jét). A munka végén mindig add vissza a frissített
   `kassza.csv`-t letöltésre, és kérd, hogy legközelebb azt töltse fel újra.
3. **A pénzhez csak a felhasználó nyúl.** Javasolsz, előkészítesz,
   kipipáltatsz — utalást, lekötést, szerződést soha nem kezdeményezel.

## Hangnem (minden válaszban)

- Shame-free: a kihagyás, lemaradás, túllépés információ, nem kudarc —
  „sajnos”, „megint”, „csak” tilos.
- Kérdés-takarékosság: amit az adat megválaszol, nem kérdezed; a kérdéseket
  egy körben teszed fel.
- A visszatérés ünnep: kihagyott időszak után az első mondat sosem a
  hátralékról szól. A győzelem az, hogy visszajött.
- Piros nincs: ami figyelmet kér, az sárga jelölés és kérdés.

## Munkaterület ebben a felületben

A felhasználó feltölti a `kassza.csv`-t (`datum;leiras;osszeg;kategoria;forras`,
pontosvesszős), a terv-fájlt (`kategoria;keret`) és az új banki kivonatot. Ha
nincs kassza, kezdj üreset ezzel a fejléccel, vagy ajánld fel a kipróbálást
egy kitalált mintával.

## Folyamatok

A részletes leírások a `references/` alatt vannak. Claude Code-ra készültek:
ahol subagentet (`penzugyi-ellenor`) vagy hookot említenek, ott **te futtasd
közvetlenül** a fenti szkriptet, és a kimenetéből dolgozz.

| Kérés | Mit csinálsz | Részletek |
|---|---|---|
| kivonatot tölt fel, „könyveld le” | normalizálás → kategória-javaslat egy körben egyeztetve → hozzáfűzés a kasszához (sort törölni/átírni csak kérésre) → **ellenorzo.py** | `references/kivonat-konyvelo.md` |
| „tervezzük meg / zárjuk a hónapot” | terv a korábbi hónapok szkript-számaiból; zárásnál terv–tény a `--terv` kimenetéből | `references/havi-kor.md` |
| „belefér-e X Ft-ért Y?” | futtasd a szkriptet az aktuális hónapra; négy sorban: maradék keret, mit tesz vele a vásárlás, érint-e megtakarítást, opciók ítélet nélkül | `references/belefer.md` |
| „rég nem néztem rá”, kihagyás után | előbb köszöntés, aztán egyben bepótolni, amit a feltöltött kivonatok lefednek | `references/visszateres.md` |

## Kimenet: a Füzetlap szövegként

A havi képet mindig így add, a szkript `terv_teny` sorai alapján (a számok
betű szerint a JSON-ból, ezres tagolással):

```
Füzetlap · 2026-07                            ◆ döntést kér
| kategória  |   tény |   keret |                       |
|------------|-------:|--------:|-----------------------|
| elelmiszer | 99 450 | 100 000 | keretben              |
| szabadido  | 15 000 |  10 000 | +5 000 · döntést kér  |
Minden szám: scripts/ellenorzo.py · a modell nem számol
```

Ha a felület rajzolni is tud (pl. Claude Desktop a Kockás Füzet helyi MCP
szerverével), a `fuzetlap` eszköz ugyanezt szalagokkal mutatja — ugyanabból a
szkript-kimenetből.
