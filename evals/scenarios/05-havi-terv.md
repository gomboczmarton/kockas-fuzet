# 05 — Havi kör: augusztusi terv a saját számokból

**Skill:** `.claude/skills/havi-kor` (A: tervezés).
**Persona:** Bence, 33 — három hónapja vezeti a kasszát, most először
tervez előre a saját tényadataiból.

## Kiinduló állapot

- `penzugy/kassza.csv` = három teljes hónap (május–július) kategorizált
  adata (`demo/adatok/kassza-3honap.csv`).
- `penzugy/terv-2026-07.csv` = minta-terv.

## Forgatókönyv

1. „Tervezzük meg az augusztust!"
2. „Augusztus 20-án szülinapi buli (~30 ezer), és jön az éves
   lakásbiztosítás (24 ezer)."

## Elvárások

- A skill az előző 3 hónapra **külön-külön** lefuttatja az ellenorzo.py-t;
  a keretjavaslatok mellett ott az evidencia („élelmiszer: 3 havi átlag
  X → javaslat Y") — az átlagok a szkript számaiból, nem fejből.
- **Egyetlen** nyitott kérdés hangzik el: „mi lesz szokatlan?"
- A válaszok beépülnek (szülinap → szabadidő/egyéb keret, biztosítás →
  külön sor vagy megfelelő kategória), és elkészül a
  `penzugy/terv-2026-08.csv` (`kategoria;keret`).
- A terv-fájlra ellenőrzés fut (a hook vagy kézi futtatás révén), és a
  megtakarítás a hónap elejére tervezett tétel marad.
- Hangnem: javaslat és evidencia, nem előírás; a döntés a felhasználóé.
