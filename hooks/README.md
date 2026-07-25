# Hookok

A hook a harness "biztonsági öve": determinisztikusan, az agent szándékától
függetlenül fut le. Itt egyetlen hook van (a vázlat-szinten ennyi kell):

- **auto-ellenorzes** (`PostToolUse`, Edit|Write): ha az agent a
  `kassza.csv`-t vagy egy `terv-*.csv`-t módosított, automatikusan lefut az
  `ellenorzo.py`, és a kimenete visszakerül az agent kontextusába. Így a
  "minden írás után ellenőrzés" szabály nem az agent fegyelmén múlik —
  a rendszer kényszeríti ki.

Telepítés a felhasználó pénzügyi repójában:
1. `settings-example.json` tartalma → `.claude/settings.json` (vagy
   összefésülve a meglévővel);
2. `chmod +x hooks/auto-ellenorzes.sh`.

Későbbi hook-jelöltek (M4): Stop-hook a hónap-zárás teljességi
ellenőrzésére ("maradt-e kategorizálatlan tétel?"), PreToolUse-guard a
kassza.csv törlése/átírása ellen.
