#!/usr/bin/env python3
"""Determinisztikus ellenőrző: kategória-összegek, terv-tény, duplikátumok.

A harness alapelve: a modell sosem számol — ez a szkript számol helyette,
fillérre pontosan (Decimal). Az agent ennek a kimenetét értelmezi, felül
nem bírálhatja.

Használat:
  python3 ellenorzo.py <kassza.csv> [--terv <terv.csv>] [--honap 2026-07] [--json]

A --json kimenet ugyanazokat a számokat adja gépi formában (nézet-modell):
ebből rajzol a terminál-felület (felulet/) és minden más megjelenítő. A
megjelenítő nem számol — minden kiírt szám innen jön, szövegként, hogy a
Decimal pontossága ne vesszen el. Kilépési kód mindkét módban azonos.

CSV formátum (pontosvesszős):
  kassza: datum;leiras;osszeg;kategoria;forras
  terv:   kategoria;keret
"""
import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation

BEVETEL_KAT = "bevetel"
ATVEZETES_KAT = {"megtakaritas", "atvezetes"}
SEMA = "kockas-ellenorzo/1"


class Hiba(Exception):
    pass


def beolvas(path):
    sorok = []
    with open(path, newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f, delimiter=";"), start=2):
            try:
                osszeg = Decimal(row["osszeg"].replace(" ", ""))
            except (InvalidOperation, KeyError):
                raise Hiba(f"HIBA: {path} {i}. sor: érvénytelen összeg: {row}")
            sorok.append({**row, "osszeg": osszeg, "_sor": i})
    return sorok


def szamol(kassza, terv_path=None, honap=None):
    """Minden szám itt születik; a két kiíró csak formáz."""
    osszes = beolvas(kassza)
    honapok = Counter(s["datum"][:7] for s in osszes)
    sorok = [s for s in osszes if s["datum"].startswith(honap)] if honap else osszes
    e = {"honap": honap, "honapok": dict(sorted(honapok.items())),
         "tetelek": len(sorok), "kilepes": 0}
    if not sorok:
        e["kilepes"] = 1
        return e

    # duplikátum-gyanú: azonos datum+leiras+osszeg
    kulcsok = Counter((s["datum"], s["leiras"], str(s["osszeg"])) for s in sorok)
    e["duplak"] = [k for k, n in kulcsok.items() if n > 1]

    kat = defaultdict(Decimal)
    for s in sorok:
        kat[s["kategoria"]] += s["osszeg"]
    e["kat"] = kat
    e["bevetel"] = kat.get(BEVETEL_KAT, Decimal(0))
    e["atvezetes"] = sum(v for k, v in kat.items() if k in ATVEZETES_KAT)
    e["kiadas"] = sum(v for k, v in kat.items()
                      if k != BEVETEL_KAT and k not in ATVEZETES_KAT)
    e["egyenleg"] = e["bevetel"] + e["kiadas"] + e["atvezetes"]
    if e["duplak"]:
        e["kilepes"] = 1

    if terv_path:
        with open(terv_path, encoding="utf-8") as f:
            terv = {r["kategoria"]: Decimal(r["keret"])
                    for r in csv.DictReader(f, delimiter=";")}
        e["terv_teny"] = []
        for k, keret in sorted(terv.items()):
            teny = -kat.get(k, Decimal(0))
            elteres = keret - teny
            e["terv_teny"].append((k, keret, teny, elteres))
            if elteres < 0:
                e["kilepes"] = 1
        e["terven_kivul"] = sorted(set(kat) - set(terv) - {BEVETEL_KAT})
    return e


def kiir_szoveg(e):
    if not e["tetelek"]:
        print("Nincs adat a megadott szűrésre.")
        return
    kat = e["kat"]
    print(f"Tételek: {e['tetelek']}  ({e['honap'] or 'minden hónap'})")
    print(f"Bevétel:                      {e['bevetel']:>12}")
    print(f"Fogyasztási kiadás:           {e['kiadas']:>12}")
    print(f"Átvezetés (megtakarítás):     {e['atvezetes']:>12}")
    print(f"Egyenleg-változás:            {e['egyenleg']:>12}")
    print("\nKategóriánként:")
    for k in sorted(kat, key=lambda x: kat[x]):
        print(f"  {k:<16} {kat[k]:>12}")

    if e["duplak"]:
        print("\nFIGYELEM — duplikátum-gyanús tételek (kézi ellenőrzés kell):")
        for d in e["duplak"]:
            print(f"  {d[0]} | {d[1]} | {d[2]}")

    if "terv_teny" in e:
        print("\nTerv–tény:")
        for k, keret, teny, elteres in e["terv_teny"]:
            jelzo = "OK" if elteres >= 0 else f"TÚLLÉPÉS {-elteres}"
            print(f"  {k:<16} keret {keret:>10}  tény {teny:>10}  {jelzo}")
        if e["terven_kivul"]:
            print(f"  Tervben nem szereplő kategóriák: {', '.join(e['terven_kivul'])}")


def json_szoveg(e):
    """Nézet-modell: minden összeg szövegként, ahogy a Decimal kiírja."""
    ki = {"sema": SEMA, "forras": "ellenorzo.py", "honap": e["honap"],
          "tetelek": e["tetelek"], "honapok": e["honapok"],
          "allapot": "nincs_adat" if not e["tetelek"]
          else ("dontest_ker" if e["kilepes"] else "rendben"),
          "kilepes": e["kilepes"]}
    if e["tetelek"]:
        kat = e["kat"]
        ki.update({
            "bevetel": str(e["bevetel"]),
            "kiadas": str(e["kiadas"]),
            "atvezetes": str(e["atvezetes"]),
            "egyenleg_valtozas": str(e["egyenleg"]),
            "kategoriak": [{"kategoria": k, "osszeg": str(kat[k])}
                           for k in sorted(kat, key=lambda x: kat[x])],
            "duplikatum_gyanu": [{"datum": d[0], "leiras": d[1], "osszeg": d[2]}
                                 for d in e["duplak"]],
        })
        if "terv_teny" in e:
            ki["terv_teny"] = [
                {"kategoria": k, "keret": str(keret), "teny": str(teny),
                 "elteres": str(elteres),
                 # túllépés: a keret feletti rész, pozitív számként (a szöveges
                 # kimenet "TÚLLÉPÉS N" értéke)
                 "tullepes": str(-elteres) if elteres < 0 else None,
                 "allapot": "keretben" if elteres >= 0 else "tullepes"}
                for k, keret, teny, elteres in e["terv_teny"]]
            ki["terven_kivul"] = e["terven_kivul"]
    return json.dumps(ki, ensure_ascii=False)


def kiir_json(e):
    print(json_szoveg(e))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kassza")
    ap.add_argument("--terv")
    ap.add_argument("--honap", help="YYYY-MM szűrés")
    ap.add_argument("--json", action="store_true",
                    help="gépi kimenet (nézet-modell) a megjelenítőknek")
    args = ap.parse_args()

    try:
        e = szamol(args.kassza, args.terv, args.honap)
    except Hiba as h:
        if args.json:
            print(json.dumps({"sema": SEMA, "forras": "ellenorzo.py",
                              "allapot": "hiba", "uzenet": str(h),
                              "kilepes": 2}, ensure_ascii=False))
        else:
            print(h)
        sys.exit(2)

    (kiir_json if args.json else kiir_szoveg)(e)
    sys.exit(e["kilepes"])


if __name__ == "__main__":
    main()
