# 01 — Első lépcső: bemásolós recept, telepítés nélkül

**Folyamat:** `prompts/01-kivonat-elemzes.md`, majd `prompts/02-havi-terv.md`
(0. szintű, bármely AI-csevegőben működő réteg).
**Persona:** Kata, 34 — még sosem használt AI-t pénzügyre. A README 1.
lépcsőjét követi: recept + (itt: szintetikus minta-)kivonat bemásolása.

## Kiinduló állapot

Nincs telepítve semmi — üres csevegő. A bemenet a recept szövege és az
`examples/minta-kivonat.csv` tartalma, egyben bemásolva.

## Forgatókönyv

1. Kata bemásolja az 1. recept teljes szövegét, a helyére illesztve a
   minta-kivonatot.
2. Az elemzés után bemásolja a 2. receptet (havi terv).

## Elvárások

- Az elemzés kategória-táblázatot ad, a végén **újraszámolható képlettel**
  (SZUMHA/SUMIF) — a recept 1. szabálya szerint.
- A megtakarítás-átvezetés **nem** szerepel kiadásként (3. szabály);
  a top-3 kiadási kategória és az előfizetések listája megjelenik.
- Az összegek egyeznek az `examples/GROUND-TRUTH.md` értékeivel.
- A terv-recept keretjavaslatai mellett ott az evidencia; egyetlen
  kérdés hangzik el („mi lesz szokatlan?"); a megtakarítás a hónap
  **elejére** kerül; a kimenet Sheets-be másolható táblázat + SUMIFS.
- Hangnem: tényszerű, ítélkezés és túlzott lelkesítés nélkül.
