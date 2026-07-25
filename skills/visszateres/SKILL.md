---
name: visszateres
description: >
  Kihagyott időszak (hetek-hónapok) utáni visszatérés: a lemaradás gyors,
  szemrehányás-mentes bepótlása. Használd, ha a felhasználó hosszabb kihagyás
  után jelentkezik, "rég nem néztem rá", "elmaradtam", "bepótolnám" jellegű
  mondatot mond, vagy a kassza.csv utolsó dátuma 30+ napra van a maitól.
---

# Visszatérés

**A győzelem az, hogy visszajött.** Ez a skill erre a mondatra épül.

## Eljárás

1. **Nyitás** (kötelező hangütés): egyetlen mondat arról, hogy a visszatérés
   a lényeg, és hogy a bepótlás rövid lesz. Semmilyen utalás a kihagyás
   hosszára, okára — kivéve ha ő maga hozza fel; akkor tényként kezeld.
2. **Helyzetkép 5 sorban**: mi az utolsó könyvelt dátum, hány hónap hiányzik,
   mely kivonatok kellenek hozzá. Kérd be őket egyszerre.
3. **Bepótlás**: a `kivonat-konyvelo` skill eljárása hónaponként, de a
   kérdéseket GYŰJTSD össze az összes hónapból egyetlen körre.
4. **Gyors-zárás**: a kihagyott hónapokra nem kell teljes havi-kör riport —
   hónaponként 2 sor (bevétel/kiadás + a legnagyobb eltérés), az
   ellenorzo.py számaiból.
5. **Friss start**: az aktuális hónapra ajánld fel a havi-kor tervezést.
   Zárd azzal, hogy a rendszer most naprakész.

## Tilalmak

- Tilos a hátralékot "sok"-nak minősíteni, listaként az arcába tolni, vagy
  "legközelebb ne hagyd ennyire" tanácsot adni.
- Ha háromnál több hónap hiányzik, akkor sem hosszabb a folyamat — csak több
  kivonatot kérsz be egyszerre.
