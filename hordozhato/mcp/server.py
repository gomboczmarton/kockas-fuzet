#!/usr/bin/env python3
"""A Kockás Füzet helyi MCP szervere, MCP App felülettel (Füzetlap).

Claude Desktopban (és minden MCP Apps-et rajzoló gazdában, amely helyi stdio
szervert futtat) a `fuzetlap` eszköz a hónap terv–tény lapját szalagokkal
mutatja. Csak a standard könyvtárat használja; a gépen marad: a kassza nem
megy fel sehova, csak az kerül a beszélgetésbe, amit az eszköz visszaad.

Egy forrás minden felületnek: a scripts/fuzetallapot.py kimenetét adja át
változtatás nélkül (structuredContent), és ugyanazokat a számokat szövegként
is (content) — az MCP Apps szabvány szerint az eszköznek felület nélkül is
értelmes szöveget kell adnia, és nem minden gazda adja tovább a modellnek a
structuredContent-et.

Beállítás (claude_desktop_config.json):
  "mcpServers": {"kockas-fuzet": {"command": "python3",
    "args": ["/ut/a/kockas-fuzet/hordozhato/mcp/server.py"],
    "env": {"KOCKAS_PENZUGY": "/ut/a/kockas-fuzet/penzugy"}}}
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIEW_URI = "ui://kockas-fuzet/fuzetlap.html"
MIME = "text/html;profile=mcp-app"
UI_EXT = "io.modelcontextprotocol/ui"
FORRAS = "Minden szám: scripts/ellenorzo.py · a felület nem számol"

TOOL = {
    "name": "fuzetlap",
    "title": "Füzetlap",
    "description": ("A hónap terv–tény lapja a Kockás Füzetből: kategóriánként tény és "
                    "keret, a döntést kérő tételek, összesítő. Minden számot a "
                    "determinisztikus ellenorzo.py ad; ne számolj belőle újat."),
    "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    # a hivatalos registerAppTool mindkét kulcsot kiírja (a lapos a régi gazdáknak)
    "_meta": {"ui": {"resourceUri": VIEW_URI}, "ui/resourceUri": VIEW_URI},
}


class NincsMetodus(Exception):
    pass


class RosszParameter(Exception):
    pass


def ft(s):
    """'-234030' -> '−234 030'. Csak formázás, mint a terminál-modban."""
    neg = s.startswith("-")
    egesz, _, tort = s.lstrip("+-").partition(".")
    tagolt = f"{int(egesz):,}".replace(",", " ")
    return ("−" if neg else "") + tagolt + (f",{tort}" if tort else "")


def elojeles(s):
    return ft(s) if s.startswith("-") else "+" + ft(s)


def allapot():
    penzugy = os.environ.get("KOCKAS_PENZUGY", str(ROOT / "penzugy"))
    argv = [sys.executable, str(ROOT / "scripts" / "fuzetallapot.py"), "--penzugy", penzugy]
    if os.environ.get("KOCKAS_MA"):
        argv += ["--ma", os.environ["KOCKAS_MA"]]
    r = subprocess.run(argv, capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
    return json.loads(r.stdout)


def szoveg(a):
    """Ugyanaz a lap markdownban — a szöveges gazdáknak és a modellnek."""
    n = a.get("nezet")
    if a["helyzet"] == "visszateres":
        return "Jó, hogy itt vagy. Ha szeretnéd, együtt rendbe tesszük a füzetet."
    if a["helyzet"] != "havi" or not n or n.get("allapot") == "hiba":
        return "A Füzetlap a könyvelt hónapot mutatja — még nincs mit."
    pecset = "✓ ellenőrizve" if n["allapot"] == "rendben" else "◆ döntést kér"
    sorok = [f"**Füzetlap · {n['honap']}** — {pecset}", "",
             "| kategória | tény | keret | |", "|---|---:|---:|---|"]
    for t in n.get("terv_teny", []):
        jel = f"+{ft(t['tullepes'])} · döntést kér" if t["allapot"] == "tullepes" else "keretben"
        sorok.append(f"| {t['kategoria']} | {ft(t['teny'])} | {ft(t['keret'])} | {jel} |")
    sorok += ["", f"Bevétel {ft(n['bevetel'])} · Kiadás {ft(n['kiadas'])} · "
              f"Megtakarítás {ft(n['atvezetes'])} · Egyenleg-változás {elojeles(n['egyenleg_valtozas'])}",
              "", f"_{FORRAS}_"]
    return "\n".join(sorok)


def valasz(uzenet, allapot_):
    m, p = uzenet.get("method"), uzenet.get("params") or {}
    if m == "initialize":
        ext = (p.get("capabilities") or {}).get("extensions") or {}
        allapot_["ui"] = UI_EXT in ext
        return {"protocolVersion": p.get("protocolVersion", "2025-11-25"),
                "capabilities": {"tools": {}, "resources": {}},
                "serverInfo": {"name": "kockas-fuzet", "version": "0.1.0"}}
    if m == "ping":
        return {}
    if m == "tools/list":
        return {"tools": [TOOL]}
    if m == "tools/call":
        if p.get("name") != "fuzetlap":
            raise RosszParameter(f"ismeretlen eszköz: {p.get('name')}")
        a = allapot()
        return {"content": [{"type": "text", "text": szoveg(a)}], "structuredContent": a,
                "isError": False}
    if m == "resources/list":
        return {"resources": [{"uri": VIEW_URI, "name": "Füzetlap", "mimeType": MIME}]}
    if m == "resources/read":
        if p.get("uri") != VIEW_URI:
            raise RosszParameter(f"ismeretlen erőforrás: {p.get('uri')}")
        html = (Path(__file__).with_name("fuzetlap.html")).read_text(encoding="utf-8")
        # csp nélkül a gazda a szigorú alapértelmezést adja: a nézet nem hálózatozik
        return {"contents": [{"uri": VIEW_URI, "mimeType": MIME, "text": html,
                              "_meta": {"ui": {"prefersBorder": True}}}]}
    raise NincsMetodus(m)


def main():
    allapot_ = {"ui": False}
    for sor in sys.stdin:
        if not sor.strip():
            continue
        uzenet = json.loads(sor)
        if "id" not in uzenet:
            continue  # értesítés (pl. notifications/initialized): nincs válasz
        try:
            ki = {"jsonrpc": "2.0", "id": uzenet["id"], "result": valasz(uzenet, allapot_)}
        except NincsMetodus as h:
            ki = {"jsonrpc": "2.0", "id": uzenet["id"],
                  "error": {"code": -32601, "message": f"nincs ilyen metódus: {h}"}}
        except (RosszParameter, ValueError, subprocess.SubprocessError) as h:
            ki = {"jsonrpc": "2.0", "id": uzenet["id"], "error": {"code": -32602, "message": str(h)}}
        sys.stdout.write(json.dumps(ki, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
