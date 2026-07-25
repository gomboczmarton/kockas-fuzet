---
name: kivonat-konyvelo
description: >
  Banki kivonat (CSV/XLSX) feldolgozása a penzugy/kassza.csv főkönyvbe:
  normalizálás, kategorizálás a felhasználóval egyeztetve, duplikátum-védelem.
  Használd, ha a felhasználó kivonatot ad át, "könyveld le", "vezesd fel a
  költéseket" jellegű kérést mond, vagy új fájl jelenik meg a
  penzugy/kivonatok/ mappában.
---

# Kivonat-könyvelő

Cél: a kivonat sorai a `penzugy/kassza.csv`-be kerülnek
(`datum;leiras;osszeg;kategoria;forras`), a felhasználó minimális terhelésével.

## Eljárás

1. **Beolvasás**: nézd meg a kivonat formátumát. Dátum → ISO (ÉÉÉÉ-HH-NN),
   összeg → előjeles egész/tizedes (kiadás negatív). Ha ismeretlen az
   oszlopkiosztás, EGY kérdésben tisztázd, és jegyezd fel a `penzugy/naplo.md`-be,
   hogy legközelebb ne kelljen kérdezni.
2. **Duplikátum-védelem**: mielőtt bármit hozzáfűznél, ellenőrizd, hogy a
   (datum, leiras, osszeg) hármas szerepel-e már a kasszában. Ami szerepel,
   azt kihagyod, és a végén jelented: "N új tétel, M már megvolt".
3. **Kategorizálás**: a kassza korábbi soraiból tanulj (azonos partnernév →
   azonos kategória). Az ismeretlen partnereket GYŰJTSD össze, és egyszerre,
   táblázatban kérdezd meg (partner | összeg | javasolt kategória) — soha ne
   egyenként. A felhasználó válaszait a naplóba írd, szabályként.
4. **Írás**: fűzd a sorokat a kassza.csv-hez.
5. **ELLENŐRZÉS (kötelező záró lépés)**: futtasd
   `python3 scripts/ellenorzo.py penzugy/kassza.csv --honap <hónap>`
   — vagy kérd meg a `penzugyi-ellenor` subagentet. A kimenetét szó szerint
   mutasd meg. Ha duplikátum-gyanút jelez, azt a felhasználóval döntesd el.

## Hangnem-szabályok

- A kimaradt hónapok, kupacban érkező kivonatok: normális állapot, egyetlen
  szó megjegyzés nélkül dolgozod fel.
- Számot te nem mondasz ki fejből: minden összeg a szkript kimenetéből jön.
