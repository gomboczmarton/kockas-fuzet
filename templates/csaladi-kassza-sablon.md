# Családi kassza sablon (Google Sheets / Excel specifikáció)

A 0–1. szint táblázata. (A tényleges .xlsx/Sheet-sablon az M1 mérföldkőnél
készül el ebből a specifikációból; az agent-oldali párja a `kassza.csv`.)

## Fülek és oszlopok

**1. fül — Kassza** (soronként egy tétel)
| Oszlop | Tartalom |
|---|---|
| A: Dátum | ÉÉÉÉ-HH-NN |
| B: Leírás | partner/megnevezés |
| C: Összeg | kiadás negatív, bevétel pozitív |
| D: Kategória | legördülő a Kategóriák fülről |
| E: Forrás | melyik bank/készpénz |

**2. fül — Terv** (havonta egy blokk)
| A: Kategória | B: Keret | C: Tény (képlet!) | D: Eltérés (képlet!) |

- C oszlop képlete (a lényeg — ez az ellenőr):
  `=-SUMIFS(Kassza!C:C; Kassza!D:D; A2; Kassza!A:A; ">="&$F$1; Kassza!A:A; "<="&$F$2)`
  (F1/F2: a hónap első/utolsó napja)
- D oszlop: `=B2-C2`, feltételes formázás: negatív → sárga (nem piros —
  hangnem!).

**3. fül — Kategóriák**: kategória-lista + havi tipikus összeg (a legördülőhöz
és az agent tanulásához).

**4. fül — Éves tételek**: tétel | esedékesség hónapja | összeg | naptárba
felvéve? — az emlekeztetok skill ebből dolgozik majd.

## Az ellenőrzési elv a táblázatban

A Tény és Eltérés oszlopokat SOHA nem az agent írja — képletek. Ha az agent
rögzített valamit rosszul, az eltérés-sorban látszik. A táblázat alja:
ellenőrző sor (`bevételek − kiadások − átvezetések = egyenleg-változás`),
aminek egyeznie kell a bankban látott változással — ez a felhasználó
végső, gépfüggetlen ellenőrzése.
