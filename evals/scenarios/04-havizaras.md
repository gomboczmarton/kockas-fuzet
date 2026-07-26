# 04 — /havizaras: teljes havi zárás egyetlen paranccsal

**Parancs:** `.claude/commands/havizaras.md` (kivonat-konyvelo + havi-kor B
+ riport egyben).
**Persona:** Anna, 38 — a családi kassza gazdája; hónap végén egy
paranccsal akarja letudni a teljes zárást.

## Kiinduló állapot

- `penzugy/kassza.csv` = csak fejléc (üres főkönyv).
- `penzugy/terv-2026-07.csv` = minta-terv.
- `penzugy/kivonatok/kivonat-2026-07.csv` = banki formátumú júliusi export,
  benne egy ismeretlen partner (KIFLI.HU) és a szabadidő-túllépést okozó
  rendezvény-tétel.

## Forgatókönyv

1. `/havizaras 2026-07`
2. „A Kifli elelmiszer. A rendezvény egyszeri volt, a keret maradhat; az
   élelmiszer-keretet emeljük 110 ezerre. És kérek egy riportot is."

## Elvárások

- A parancs végigviszi a láncot: kivonat-könyvelés (az ismeretlen partner
  egy körben kérdezve) → penzugyi-ellenor futás → zárójelentés.
- A jelentés dramaturgiája kötött: **1 jó dolog → eltérések számokkal →
  legfeljebb 2 javaslat**; minden túllépésnél elhangzik az „egyszeri volt,
  vagy keretet igazítsunk?" kérdés.
- A túllépés kérdésként, nem vádként jelenik meg („sajnos/megint/csak" nem
  hangzik el).
- A döntések a `penzugy/naplo.md`-be kerülnek; a riport a
  `templates/riport-sablon.html` kitöltésével készül
  (`penzugy/riportok/riport-2026-07.html`), új elem kitalálása nélkül.
- Zárásként felajánlja a következő havi tervezést.
