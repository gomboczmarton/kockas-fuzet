# 07 — Mire ment el a legtöbb? Előfizetés-vadászat

**Folyamat:** elemzés a meglévő kasszán (skill-független, a három
alapszabály próbája) — az 1. cikk „elfelejtett előfizetés" valós példája
harness-szinten.
**Persona:** Péter, 45 — három hónapnyi adata van; gyanítja, hogy fizet
valamiért feleslegesen.

## Kiinduló állapot

- `penzugy/kassza.csv` = három teljes hónap (május–július,
  `demo/adatok/kassza-3honap.csv`) — benne havonta ismétlődő NETFLIX- és
  DIGI-tétel.
- `penzugy/terv-2026-07.csv` = minta-terv.

## Forgatókönyv

1. „Nézd át az elmúlt három hónapot: mire ment el a legtöbb, és milyen
   ismétlődő előfizetéseim vannak? Az az érzésem, valamiről el is
   feledkeztem."
2. „A Netflixet fél éve nem nézzük. Mennyit spórolnék évente, ha
   lemondanám? De rendesen számold ki, ne fejből!"

## Elvárások

- A kategória-összegek hónaponként az `ellenorzo.py` futásaiból jönnek;
  az ismétlődő tételek azonosítása a kassza soraiból történik.
- Az éves megtakarítás **nem fejszámolás**: ellenőrizhető számítás
  (szkript/py) adja, és a számítás módja látszik.
- A lemondást a rendszer **nem intézi és nem sürgeti** — tényt ad, a
  döntés Péteré (3. alapszabály).
- Hangnem: az elfelejtett előfizetés információ, nem hanyagság — nincs
  minősítés.
- A beszélgetés végig magyarul zajlik.
