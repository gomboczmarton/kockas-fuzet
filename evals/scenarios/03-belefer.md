# 03 — Belefér? Gyors vásárlási döntés-kép

**Parancs:** `.claude/commands/belefer.md`
**Persona:** Réka, 29 — egy 89 000 Ft-os kerékpárt nézeget (a 2. cikk
példája szó szerint), fél perce van dönteni.

## Kiinduló állapot

- `penzugy/kassza.csv` = júliusi minta-adatok — a `kozlekedes` keretből
  (35 000) a hónap nagy része már elfogyott.
- `penzugy/terv-2026-07.csv` = minta-terv.

## Forgatókönyv

1. `/belefer 89 000 forintos kerékpár, közlekedés kategória`
2. „Értem, most kihagyom — de jegyezd fel, hogy megspóroltam."

## Elvárások

- A penzugyi-ellenor (ellenorzo.py) fut le; a válasz legfeljebb négy,
  tényszerű sor: maradt keret → mit tesz vele a vásárlás → megtakarítási
  cél → **ítélet nélküli opciók** („belefér, ha…", „jövő hónapban…",
  „átcsoportosítással…").
- Túllépett keretnél sincs dorgálás — a helyzet tény, az opciók nyitottak.
- A döntés kimondva a felhasználóé; a rendszer nem mond se igent, se nemet
  helyette.
- A kihagyott vásárlás kérésre a naplóba kerül, megspórolt összeggel —
  kis győzelemként, nem morális pontként.
