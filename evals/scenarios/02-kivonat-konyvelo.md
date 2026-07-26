# 02 — Kivonat-könyvelő: az új havi export lekönyvelése

**Skill:** `.claude/skills/kivonat-konyvelo`
**Persona:** Gábor, 41 — havonta egyszer néz rá a pénzügyekre; most
letöltötte az augusztusi kivonatot a bankból.

## Kiinduló állapot

- `penzugy/kassza.csv` = a júliusi minta-adatok (kategorizált előzmény).
- `penzugy/terv-2026-07.csv` = minta-terv.
- `penzugy/kivonatok/kivonat-2026-08.csv` = banki formátumú export
  (más fejléc, pontozott dátumok), benne:
  - ismert partnerek (ALDI, LIDL, NETFLIX… — a kasszából tanulható);
  - két ismeretlen partner (DM, WOLT);
  - egy júliusi sor, ami már szerepel a kasszában (TESCO 07-28) —
    duplikátum-csali.

## Forgatókönyv

1. „Megjött a bankból az augusztusi kivonat… légyszi könyveld le."
2. (A gyűjtött kérdésekre) „A DM haztartas, a Wolt elelmiszer; a Tesco-s
   sort hagyd ki."

## Elvárások

- Dátum- és formátum-normalizálás (2026.08.02. → 2026-08-02) kérdés nélkül.
- Az ismert partnerek kategóriáját a kasszából tanulja, **nem kérdezi**.
- A két ismeretlen partnert **egyetlen körben, táblázatban** kérdezi meg —
  nem egyenként.
- A TESCO-sort duplikátumként jelzi és a felhasználóval dönteti el.
- Könyvelés után lefut az `ellenorzo.py` (vagy a subagent), kimenete szó
  szerint látszik; zárásként „N új tétel, M már megvolt" összegzés.
- A tanult kategória-szabályok bekerülnek a `penzugy/naplo.md`-be.
- A kupacban érkező kivonatról egyetlen minősítő megjegyzés sincs.
