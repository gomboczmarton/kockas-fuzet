# 08 — Írd fel! Készpénzes költés rögzítése menet közben

**Folyamat:** kézi gyors-rögzítés a kasszába + új szabály tanulása a
naplóba — az 1. cikk blokk-példájának és a 2. cikk útközbeni („írd fel:
ma 68 euró") képének harness-szintű párja.
**Persona:** Juli, 31 — a piacról hazafelé, blokk a zsebében; nem akar
hazaérve gépelni.

## Kiinduló állapot

- `penzugy/kassza.csv` = júliusi minta-adatok (benne készpénzfelvét,
  `keszpenz` kategória).
- `penzugy/terv-2026-07.csv` = minta-terv.

## Forgatókönyv

1. „Ma a piacon 4 300 forintot költöttem készpénzből zöldségre. Írd fel,
   légyszi — és mostantól a készpénzes blokkjaimat is így szeretném
   bemondani."
2. „Vezesd úgy, ahogy javasoltad — és a szabályt írd a naplóba."

## Elvárások

- A tétel a kasszába kerül (append; ISO dátum, negatív összeg, forrás
  jelzi a készpénzes eredetet); írás után lefut az ellenőrzés (hook vagy
  kézi futtatás).
- A rendszer észreveszi és **megbeszéli** a készpénz-kettősség kérdését
  (a felvett készpénz már szerepel `keszpenz` kategóriaként — a blokkos
  részletezés hogyan ne duplázzon), és a felhasználóval közösen választott
  megoldást rögzíti.
- Az új „bemondós blokk" szabály a `penzugy/naplo.md`-be kerül, hogy
  legközelebb kérdés nélkül működjön.
- Kérdés-takarékosság: egy körben, tömören; a válaszok rövidek — ez egy
  útközbeni interakció.
- A beszélgetés végig magyarul zajlik.
