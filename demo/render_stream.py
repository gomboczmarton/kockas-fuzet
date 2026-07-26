#!/usr/bin/env python3
"""A demó-lejátszó megjelenítője.

Három al-parancs:
  banner <cím> <persona>   — nyitókártya a felvétel elejére
  gepel <szöveg> [--nev N] — a persona üzenetének "gépelt" kiírása
  stream                   — a `claude -p --output-format stream-json`
                             kimenetének élő, olvasható megjelenítése
                             (szöveg, eszközhívások, ellenőrző-kimenet)

Csak szabványkönyvtárat használ.
"""
import json
import shutil
import sys
import textwrap
import time

SZELES = 100

DIM = "\033[2m"
BOLD = "\033[1m"
SARGA = "\033[1;33m"
ZOLD = "\033[32m"
CIAN = "\033[36m"
RESET = "\033[0m"


def _ki(s, delay=0.0):
    for ch in s:
        sys.stdout.write(ch)
        sys.stdout.flush()
        if delay:
            time.sleep(delay)


def banner(cim, persona):
    vonal = "─" * SZELES
    print(f"{DIM}{vonal}{RESET}")
    print(f"  {BOLD}KOCKÁS FÜZET · DEMÓ{RESET}")
    print(f"  {BOLD}{cim}{RESET}")
    if persona:
        print(f"  {DIM}{persona}{RESET}")
    print(f"{DIM}{vonal}{RESET}")
    print()
    time.sleep(1.2)


def gepel(szoveg, nev="Te"):
    print()
    _ki(f"{SARGA}{nev} ▸{RESET} ")
    # hosszú beillesztett szövegnél gyorsabban "gépelünk"
    delay = min(0.028, max(0.001, 4.0 / max(len(szoveg), 1)))
    sorok = szoveg.splitlines() or [""]
    for i, sor in enumerate(sorok):
        if i > 0:
            sys.stdout.write(f"\n{SARGA}  │{RESET} ")
        _ki(sor, delay)
    print()
    print()
    time.sleep(0.4)


def _eszkoz_sor(nev, inp):
    if nev == "Bash":
        resz = (inp.get("command") or "").replace("\n", " ")
    elif nev in ("Read", "Write", "Edit", "MultiEdit", "NotebookEdit"):
        resz = inp.get("file_path", "")
    elif nev in ("Task", "Agent"):
        resz = (inp.get("description", "") or inp.get("subagent_type", "")
                or inp.get("prompt", ""))
    elif nev == "Skill":
        resz = inp.get("skill", "") or inp.get("command", "")
    elif nev in ("Glob", "Grep"):
        resz = inp.get("pattern", "")
    else:
        resz = ""
    if len(resz) > 84:
        resz = resz[:81] + "…"
    return f"{DIM}{CIAN}  » {nev}{RESET}{DIM}  {resz}{RESET}"


def _szoveg_ki(szoveg):
    delay = min(0.004, max(0.0005, 6.0 / max(len(szoveg), 1)))
    for sor in szoveg.splitlines():
        if len(sor) > SZELES:
            sor = "\n".join(textwrap.wrap(sor, SZELES, drop_whitespace=False))
        _ki(sor + "\n", delay)


def stream():
    fontos_eredmeny = {}  # tool_use_id -> True, ha a kimenetét mutatjuk
    print(f"{ZOLD}Kockás Füzet ▸{RESET}")
    for nyers in sys.stdin:
        nyers = nyers.strip()
        if not nyers:
            continue
        try:
            uzenet = json.loads(nyers)
        except json.JSONDecodeError:
            continue
        tipus = uzenet.get("type")
        if tipus == "assistant":
            for blokk in uzenet.get("message", {}).get("content", []):
                bt = blokk.get("type")
                if bt == "text" and blokk.get("text", "").strip():
                    _szoveg_ki(blokk["text"].rstrip())
                    print()
                elif bt == "tool_use":
                    print(_eszkoz_sor(blokk.get("name", "?"),
                                      blokk.get("input", {}) or {}))
                    cmd = (blokk.get("input", {}) or {}).get("command", "")
                    if "ellenorzo.py" in cmd or "evals/run.sh" in cmd:
                        fontos_eredmeny[blokk.get("id")] = True
        elif tipus == "user":
            tartalom = uzenet.get("message", {}).get("content", [])
            if not isinstance(tartalom, list):
                continue
            for blokk in tartalom:
                if blokk.get("type") != "tool_result":
                    continue
                if not fontos_eredmeny.pop(blokk.get("tool_use_id"), False):
                    continue
                resz = blokk.get("content")
                if isinstance(resz, list):
                    resz = "\n".join(b.get("text", "") for b in resz
                                     if isinstance(b, dict))
                if not isinstance(resz, str):
                    continue
                sorok = resz.strip().splitlines()[:22]
                for s in sorok:
                    print(f"{DIM}    {s[:SZELES - 4]}{RESET}")
                    time.sleep(0.02)
    print()


if __name__ == "__main__":
    mod = sys.argv[1] if len(sys.argv) > 1 else "stream"
    if mod == "banner":
        banner(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
    elif mod == "gepel":
        nev = "Te"
        argv = sys.argv[2:]
        if "--nev" in argv:
            i = argv.index("--nev")
            nev = argv[i + 1]
            argv = argv[:i] + argv[i + 2:]
        gepel(argv[0] if argv else "", nev)
    else:
        stream()
