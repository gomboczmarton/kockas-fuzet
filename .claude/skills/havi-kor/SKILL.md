---
name: havi-kor
description: >
  A havi pénzügyi kör két fele: hónap eleji terv készítése az előző hónapok
  tényadataiból, és hónap végi zárás (terv-tény összevetés, eltérések
  megbeszélése). Használd "tervezzük meg a hónapot", "havi terv", "zárjuk a
  hónapot", "hogy ment a hónap" kérésekre.
---

# Havi kör

## A) Tervezés (hónap elején)

1. Futtasd az ellenőrzőt az előző 3 hónapra külön-külön
   (`ellenorzo.py penzugy/kassza.csv --honap <H>`), és a kategória-átlagokból
   javasolj keretet. A javaslat mellé tedd oda az evidenciát:
   "élelmiszer: az elmúlt 3 hónap átlaga 98 400 → javaslat 100 000".
2. EGY nyitott kérdést tegyél fel: "Mi lesz szokatlan ebben a hónapban?"
   (utazás, születésnap, éves számla…). A válaszokat építsd a keretekbe.
3. Írd ki a `penzugy/terv-<ÉÉÉÉ-HH>.csv` fájlt (`kategoria;keret`), és
   ellenőrzésképp futtasd rá az ellenorzo.py-t --terv módban az aktuális
   (üres vagy részleges) hónapra — hibátlanul kell lefutnia.

## B) Zárás (hónap végén)

1. Ha van feldolgozatlan kivonat: előbb a `kivonat-konyvelo` skill.
2. Futtasd: `ellenorzo.py penzugy/kassza.csv --terv penzugy/terv-<H>.csv
   --honap <H>`. A számokat CSAK innen veheted.
3. A jelentés sorrendje kötött (shame-free dramaturgia):
   1. egy dolog, ami jól ment (kereten belüli kategória, teljesült
      megtakarítás);
   2. az eltérések, számokkal, ítélet nélkül — minden túllépésnél kérdezd
      meg: egyszeri volt, vagy a keretet kell igazítani?;
   3. legfeljebb KÉT javaslat a következő hónapra.
4. (Ha a felhasználó riportot kér) töltsd ki a
   `templates/riport-sablon.html` sablont a szkript számaival — a sablon
   {{...}} helyőrzőit cseréld, új elemet ne találj ki; a kimenet:
   `penzugy/riportok/riport-<ÉÉÉÉ-HH>.html`. A dramaturgia kötött: ami jól
   ment → eltérések → legfeljebb két javaslat.
5. A döntéseket (keret-módosítás, új szabály) írd a naplóba és a következő
   terv alapjába.

## Hangnem

A túllépés információ, nem kudarc. Tilos: "sajnos", "megint", "csak".
A hónap zárása mindig a visszatérés megünneplésével ér véget, akármi
volt a számokban.
