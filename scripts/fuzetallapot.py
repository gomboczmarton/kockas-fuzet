#!/usr/bin/env python3
"""A füzet állapota a megjelenítőknek (nézet-modell + helyzet).

Egy forrás minden felületnek: a terminál-mod (füzetsor, Füzetlap) és a
státuszsor is ebből rajzol, és egyik sem számol. A számok az ellenorzo.py
szamol() függvényéből jönnek; ez a szkript csak eldönti, melyik hónapot és
milyen helyzetet mutassunk:

  ures         nincs kassza, vagy nincs benne tétel
  visszateres  sem ebben, sem az előző hónapban nincs tétel — a felület
               ilyenkor köszönt, és nem mutatja a kihagyott hónapokat
  havi         a mostani hónap, vagy ha még üres, a legutóbbi könyvelt

Használat:
  python3 scripts/fuzetallapot.py [--penzugy penzugy] [--ma 2026-07] [--sor]

--sor: egyetlen sor a Claude Code státuszsorába (statusLine), ANSI-színnel.
Kilépési kód mindig 0: a megjelenítés sosem kapu.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ellenorzo  # noqa: E402

SEMA = "kockas-allapot/1"
ZOLD, SARGA, HALK, VEG = "\033[38;2;143;179;156m", "\033[38;2;232;199;106m", "\033[2m", "\033[0m"


def elozo(honap):
    ev, ho = map(int, honap.split("-"))
    return f"{ev - 1}-12" if ho == 1 else f"{ev}-{ho - 1:02d}"


def allapot(penzugy, ma):
    kassza = penzugy / "kassza.csv"
    ki = {"sema": SEMA, "ma": ma, "helyzet": "ures", "nezet": None,
          "frissitve": datetime.datetime.now().strftime("%H:%M")}
    if not kassza.exists():
        return ki

    def nezet(honap):
        terv = penzugy / f"terv-{honap}.csv"
        e = ellenorzo.szamol(str(kassza), str(terv) if terv.exists() else None, honap)
        return json.loads(ellenorzo.json_szoveg(e))

    n = nezet(ma)
    honapok = list(n.get("honapok", {}))
    if n["allapot"] == "nincs_adat" and honapok:
        utolso = honapok[-1]
        if utolso < elozo(ma):
            ki["helyzet"] = "visszateres"
            return ki
        n = nezet(utolso)
    if n["allapot"] != "nincs_adat":
        ki["helyzet"] = "havi"
        ki["nezet"] = n
    return ki


def sor(a):
    fej = f"{ZOLD}▦ Kockás Füzet{VEG}"
    if a["helyzet"] == "visszateres":
        return f"{fej} {HALK}· jó, hogy itt vagy{VEG}"
    if a["helyzet"] == "ures":
        return f"{fej} {HALK}· a füzet még üres{VEG}"
    n = a["nezet"]
    if n["allapot"] == "rendben":
        return f"{fej} · {n['honap']} · {ZOLD}✓ ellenőrizve{VEG}"
    return f"{fej} · {n['honap']} · {SARGA}◆ döntést kér{VEG}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--penzugy", default="penzugy")
    ap.add_argument("--ma", help="ÉÉÉÉ-HH (alapból a mai hónap)")
    ap.add_argument("--sor", action="store_true", help="státuszsor-szöveg")
    args = ap.parse_args()
    ma = args.ma or datetime.date.today().strftime("%Y-%m")
    try:
        a = allapot(Path(args.penzugy), ma)
    except (ellenorzo.Hiba, OSError, ValueError) as h:
        a = {"sema": SEMA, "ma": ma, "helyzet": "havi", "frissitve": None,
             "nezet": {"allapot": "hiba", "honap": ma, "uzenet": str(h)}}
    if args.sor:
        print(sor(a) if a["nezet"] is None or a["nezet"]["allapot"] != "hiba"
              else f"{ZOLD}▦ Kockás Füzet{VEG} · {SARGA}◆ nézzük meg együtt{VEG}")
    else:
        print(json.dumps(a, ensure_ascii=False))


if __name__ == "__main__":
    main()
