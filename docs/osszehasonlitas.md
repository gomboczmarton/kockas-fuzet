# Kockás Füzet vagy Belay?

Két nyílt forrású pénzügyi asszisztens Claude Code-ra. Ugyanaz az alap, két különböző élethelyzet.

![Kockás Füzet és Belay összehasonlítása, mindkét oldalon a tipikus felhasználói kérdéssel](../assets/kockas-fuzet-vs-belay.svg)

## Közös alap

- A gép nem számol fejben
- Az adatod a tiéd
- A pénzhez csak te nyúlsz
- Kihagyás után nincs szégyen

## Részletesen

|  | Kockás Füzet | A kérdés, amire válaszol | Belay | A kérdés, amire válaszol |
|---|---|---|---|---|
| **Kinek szól** | Magyar családoknak és magánszemélyeknek, nem programozóknak. | *„Hogyan tartsam kézben a család pénzét esti táblázatozás nélkül?”* | ADHD-s felnőtteknek, akiknél a pénzügyi rutin rendre elakad. | *„Hogyan legyen rálátásom a pénzemre, ha az agyam nem viszi a rutint?”* |
| **Szemlélet** | Havi keret kategóriánként. A túllépés sárga kérdés, nem kudarc. | *„Mennyi maradt még ebben a hónapban élelmiszerre?”* | Előbb láthatóság, keret csak ha kell. A célszám referencia, nem limit. | *„Hová tűnik el a pénzem — újabb feladott költségvetés nélkül?”* |
| **Indulás** | 10 perc, telepítés nélkül: bemásolós recept bármelyik AI-csevegőbe. | *„Kipróbálhatom most rögtön, telepítés nélkül?”* | Egyszeri onboarding 12–24 hónapnyi banki exporttal, bármikor folytatható. | *„Rendet tesz két év kivonatában anélkül, hogy bármit válogatnék?”* |
| **Banki adatok** | A havi kivonat bekerül a kasszába, duplikátum-védelemmel. | *„Mire ment el a pénz ebben a hónapban, kategóriánként?”* | Több bank és számla, automatikus felismeréssel (Revolut, Wise, OTP…). | *„Miért számolja költésnek, amikor a hitelkártyámat töltöm fel?”* |
| **Vásárlás előtt** | /belefer: négy sorban a maradék keret és a lehetőségek, ítélet nélkül. | *„Belefér ebben a hónapban egy 25 000 forintos cipő?”* | /purchase-check: fél perc alatt tényszerű kép a hatásról. A döntés a tiéd. | *„Megvegyem, vagy felborítja az egész hónapot?”* |
| **Kihagyás után** | A kihagyott hetek bepótlása; az első mondat sosem a hátralékról szól. | *„Két hónapja nem néztem rá. Hogyan kezdjem újra?”* | Welcome back: az egész kihagyás öt sorban, aztán tiszta lap. | *„Három hónapra eltűntem. Most mindent pótolnom kell?”* |
| **Hosszú távon** | Havi kör: terv a saját számaidból, zárás terv–tény összevetéssel. | *„Mire lesz elég a fizetés a következő hónapban?”* | Coach: mintázatok, kis visszafordítható kísérletek; /extend: új folyamatok. | *„Segít szokást építeni, nem csak riportot adni?”* |
| **Az adataid** | Egy CSV főkönyv a saját mappádban; a táblázat egyben az ellenőr is. | *„Hol vannak az adataim, és ki látja őket?”* | Bővülő eseménynapló és olvasható állapotfájlok a saját repódban. | *„Visszanézhetem, mi változott és miért?”* |

## Melyiket válaszd?

- **Kockás Füzet**, ha magyarul, családban gondolkodsz, egy táblázatból indulnál, és még ma kipróbálnád telepítés nélkül.
- **Belay**, ha ADHD-val élsz (vagy egyszerűen a rutin a nehéz), több bankszámlád van, és előbb látni szeretnéd, hová megy a pénz, mielőtt bármit tervezel.

## Hol találod

- Kockás Füzet — [github.com/gomboczmarton/kockas-fuzet](https://github.com/gomboczmarton/kockas-fuzet) · *a kockás füzet, ami visszaír*
- Belay — [github.com/gomboczmarton/adhd-personal-finance-belay](https://github.com/gomboczmarton/adhd-personal-finance-belay) · *You climb. It holds the rope.*

Mindkettő Claude Code-dal működik. Minden összeget determinisztikus szkript számol, nem a modell.

*A tartalom a két repó `main` ágát írja le (2026. október). Az ábra forrása ugyanez a táblázat: [`assets/kockas-fuzet-vs-belay.svg`](../assets/kockas-fuzet-vs-belay.svg).*
