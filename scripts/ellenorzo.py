#!/usr/bin/env python3
"""Determinisztikus ellenőrző: kategória-összegek, terv-tény, duplikátumok.

A harness alapelve: a modell sosem számol — ez a szkript számol helyette,
fillérre pontosan (Decimal). Az agent ennek a kimenetét értelmezi, felül
nem bírálhatja.

Használat:
  python3 ellenorzo.py <kassza.csv> [--terv <terv.csv>] [--honap 2026-07]

CSV formátum (pontosvesszős):
  kassza: datum;leiras;osszeg;kategoria;forras
  terv:   kategoria;keret
"""
import argparse
import csv
import sys
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation

BEVETEL_KAT = "bevetel"
ATVEZETES_KAT = {"megtakaritas", "atvezetes"}


def beolvas(path):
    sorok = []
    with open(path, newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f, delimiter=";"), start=2):
            try:
                osszeg = Decimal(row["osszeg"].replace(" ", ""))
            except (InvalidOperation, KeyError):
                print(f"HIBA: {path} {i}. sor: érvénytelen összeg: {row}")
                sys.exit(2)
            sorok.append({**row, "osszeg": osszeg, "_sor": i})
    return sorok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kassza")
    ap.add_argument("--terv")
    ap.add_argument("--honap", help="YYYY-MM szűrés")
    args = ap.parse_args()

    sorok = beolvas(args.kassza)
    if args.honap:
        sorok = [s for s in sorok if s["datum"].startswith(args.honap)]
    if not sorok:
        print("Nincs adat a megadott szűrésre.")
        sys.exit(1)

    # duplikátum-gyanú: azonos datum+leiras+osszeg
    kulcsok = Counter((s["datum"], s["leiras"], str(s["osszeg"])) for s in sorok)
    duplak = [k for k, n in kulcsok.items() if n > 1]

    kat = defaultdict(Decimal)
    for s in sorok:
        kat[s["kategoria"]] += s["osszeg"]

    bevetel = kat.get(BEVETEL_KAT, Decimal(0))
    atvezetes = sum(v for k, v in kat.items() if k in ATVEZETES_KAT)
    kiadas = sum(v for k, v in kat.items()
                 if k != BEVETEL_KAT and k not in ATVEZETES_KAT)

    print(f"Tételek: {len(sorok)}  ({args.honap or 'minden hónap'})")
    print(f"Bevétel:                      {bevetel:>12}")
    print(f"Fogyasztási kiadás:           {kiadas:>12}")
    print(f"Átvezetés (megtakarítás):     {atvezetes:>12}")
    print(f"Egyenleg-változás:            {bevetel + kiadas + atvezetes:>12}")
    print("\nKategóriánként:")
    for k in sorted(kat, key=lambda x: kat[x]):
        print(f"  {k:<16} {kat[k]:>12}")

    kilepes = 0
    if duplak:
        kilepes = 1
        print("\nFIGYELEM — duplikátum-gyanús tételek (kézi ellenőrzés kell):")
        for d in duplak:
            print(f"  {d[0]} | {d[1]} | {d[2]}")

    if args.terv:
        print("\nTerv–tény:")
        terv = {r["kategoria"]: Decimal(r["keret"])
                for r in csv.DictReader(open(args.terv, encoding="utf-8"),
                                        delimiter=";")}
        for k, keret in sorted(terv.items()):
            teny = -kat.get(k, Decimal(0))
            elteres = keret - teny
            jelzo = "OK" if elteres >= 0 else f"TÚLLÉPÉS {-elteres}"
            print(f"  {k:<16} keret {keret:>10}  tény {teny:>10}  {jelzo}")
            if elteres < 0:
                kilepes = 1
        hianyzo = set(kat) - set(terv) - {BEVETEL_KAT}
        if hianyzo:
            print(f"  Tervben nem szereplő kategóriák: {', '.join(sorted(hianyzo))}")

    sys.exit(kilepes)


if __name__ == "__main__":
    main()
