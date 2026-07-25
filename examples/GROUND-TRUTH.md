# Minta-adat ground truth (az eval mércéje)

A `minta-kivonat.csv` ismert, kézzel rögzített igazsága — az
`ellenorzo.py`-nak és minden skillnek pontosan ezt kell kihoznia:

- Bevétel: **620 000**
- Fogyasztási kiadás (megtakarítás-átvezetés nélkül): **–234 030**;
  megtakarítással együtt: **–334 030**
- Kategóriánként: elelmiszer –99 450 · rezsi –35 390 · kozlekedes –30 950 ·
  elofizetes –4 490 · egeszseg –8 750 · szabadido –15 000 · keszpenz –40 000 ·
  megtakaritas –100 000 *(a megtakarítás átvezetés, nem fogyasztás — a
  riportban külön sorban kezelendő)*
- Hó végi egyenleg-változás: **+285 970**
- Terv–tény eltérések (minta-terv-2026-07.csv ellen): szabadido **+5 000
  túllépés** (15 000 vs. 10 000 keret; a "jubileumi rendezvény" eset) —
  minden más kategória kereten belül.
- Duplikátum: nincs. (Dedup-teszthez másold be kétszer a 07-08-i LIDL sort —
  az ellenorzo.py-nak jeleznie kell.)
