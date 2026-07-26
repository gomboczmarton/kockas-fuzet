# 06 — Visszatérés: két kihagyott hónap, szemrehányás nélkül

**Skill:** `.claude/skills/visszateres` — a BUILD-ORDER 3. lépésének
persona-próbája (hangnem-rubrikával) ezen a forgatókönyvön fut.
**Persona:** Dóri, 36 — május vége óta nem nyitotta ki a füzetet; kicsit
szabadkozva tér vissza.

## Kiinduló állapot

- `penzugy/kassza.csv` utolsó dátuma 2026-05-30 (≈2 hónap kihagyás).
- `penzugy/terv-2026-06.csv` és `terv-2026-07.csv` megvan.
- `penzugy/kivonatok/` = júniusi és júliusi banki export, bennük két
  ismeretlen partner (FOGORVOSI RENDELO, KIFLI.HU).

## Forgatókönyv

1. „Szia… májusban néztem rá utoljára, azóta csak gyűltek a kivonatok.
   Bepótolnám végre, ha nem gond."
2. „A fogorvos egeszseg, a Kifli elelmiszer."

## Elvárások (hangnem-rubrika — ez itt a fő mérce)

- **Az első mondat nem a hátralékról szól** — a visszatérés tényét
  ünnepli, és rövid bepótlást ígér.
- Tilos: a kihagyás minősítése („sok", „sajnos", „megint"), a hátralék
  listázása az arcába, „legközelebb ne hagyd ennyire" tanács.
- Helyzetkép legfeljebb 5 sorban (utolsó dátum, hiányzó hónapok, kellő
  kivonatok); a kérdések **mindkét hónapból egyetlen körbe** gyűjtve.
- Bepótlás a kivonat-konyvelo eljárással; hónaponként 2 soros gyors-zárás
  az ellenorzo.py számaiból (bevétel/kiadás + legnagyobb eltérés).
- Zárás: friss start — felajánlja az aktuális hónap tervezését, és
  kimondja, hogy a rendszer naprakész.
