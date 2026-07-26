# 03 — Belefér? Gyors vásárlási döntés-kép

**Parancs:** `.claude/commands/belefer.md`
**Persona:** Réka, 29 — a boltban áll egy 8 990 Ft-os társasjátékkal,
fél perce van dönteni.

## Kiinduló állapot

- `penzugy/kassza.csv` = júliusi minta-adatok — a `szabadido` keret
  (10 000) a rendezvény (15 000) miatt már túl van lépve.
- `penzugy/terv-2026-07.csv` = minta-terv.

## Forgatókönyv

1. `/belefer 8990 forintos társasjáték, szabadidő kategória`
2. „Igazad van, most kihagyom — de jegyezd fel, hogy megspóroltam."

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
