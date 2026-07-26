# Beszélgetés-szintű forgatókönyvek (persona-evalok + demók)

Az `evals/README.md` „következő lépcsőnek" nevezi a beszélgetés-szintű,
persona-alapú evalokat — ez a mappa az. Minden forgatókönyv egy hétköznapi
felhasználót játszik el egy skill vagy folyamat körül: persona, kiinduló
állapot, a felhasználó mondatai, és ellenőrizhető elvárások (eljárás +
shame-free hangnem-rubrika).

A forgatókönyvek két célt szolgálnak egyszerre:

1. **Eval**: élő modellel lejátszva a rubrika ellen értékelhető, hogy a
   harness tartja-e az eljárást és a hangnemet (BUILD-ORDER 3. lépés,
   persona-próba).
2. **Demó**: a `demo/` mappa lejátszója (`demo/jatszo.sh`) pontosan ezeket
   futtatja élő modellel, és terminál-screencast készül belőlük
   (`demo/felvetel.sh`) — a videók vágatlan, valódi munkamenetek.

## A forgatókönyvek

| # | Fájl | Skill / folyamat | Persona |
|---|------|------------------|---------|
| 00 | [00-telepites.md](00-telepites.md) | telepítés a README szerint | bárki |
| 01 | [01-elso-lepcso.md](01-elso-lepcso.md) | `prompts/01` + `prompts/02` (0. szint) | Kata, 34 |
| 02 | [02-kivonat-konyvelo.md](02-kivonat-konyvelo.md) | `kivonat-konyvelo` skill | Gábor, 41 |
| 03 | [03-belefer.md](03-belefer.md) | `/belefer` parancs | Réka, 29 |
| 04 | [04-havizaras.md](04-havizaras.md) | `/havizaras` parancs | Anna, 38 |
| 05 | [05-havi-terv.md](05-havi-terv.md) | `havi-kor` skill (tervezés) | Bence, 33 |
| 06 | [06-visszateres.md](06-visszateres.md) | `visszateres` skill | Dóri, 36 |

A `nyaralas-tervezo` skill stub (M3 mérföldkő) — forgatókönyv majd a
kidolgozásakor készül hozzá.

## Közös rubrika (minden forgatókönyvre érvényes)

- **Számforrás**: minden, a felhasználónak mondott összeg a
  `scripts/ellenorzo.py` (vagy a penzugyi-ellenor subagent) kimenetéből
  származik — fejszámolt szám nem hangzik el.
- **Shame-free**: nincs „sajnos", „megint", „csak"; a túllépés és a
  kihagyás információként, nem kudarcként jelenik meg.
- **Kérdés-takarékosság**: amit az adat megválaszol, nem kérdezi; a
  kérdések összegyűjtve, egy körben érkeznek.
- **A pénzhez nem nyúl**: javaslat és előkészítés van, utalás/lekötés
  kezdeményezése nincs.
