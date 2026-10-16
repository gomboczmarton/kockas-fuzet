#!/usr/bin/env python3
"""A hordozható skill összerakása feltöltéshez (Claude.ai, ChatGPT, Gemini).

Használat:
  python3 hordozhato/build_skill.py [--ki hordozhato/dist]

Kimenet: <ki>/kockas-fuzet.zip, benne a skill mappája a legfelső szinten
(kockas-fuzet/SKILL.md — a Claude.ai a zip gyökerében álló SKILL.md-t nem
ismeri fel). A szkriptek és a referenciák a repó egyetlen forrásából
másolódnak, így a hordozható változat nem tud elcsúszni a Claude Code-ostól.
"""
import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEV = "kockas-fuzet"
TARTALOM = {
    "SKILL.md": ROOT / "hordozhato" / "skill" / "SKILL.md",
    "scripts/ellenorzo.py": ROOT / "scripts" / "ellenorzo.py",
    "scripts/fuzetallapot.py": ROOT / "scripts" / "fuzetallapot.py",
    "references/kivonat-konyvelo.md": ROOT / ".claude" / "skills" / "kivonat-konyvelo" / "SKILL.md",
    "references/havi-kor.md": ROOT / ".claude" / "skills" / "havi-kor" / "SKILL.md",
    "references/visszateres.md": ROOT / ".claude" / "skills" / "visszateres" / "SKILL.md",
    "references/belefer.md": ROOT / ".claude" / "commands" / "belefer.md",
}


def epit(ki: Path) -> Path:
    ki.mkdir(parents=True, exist_ok=True)
    cel = ki / f"{NEV}.zip"
    with zipfile.ZipFile(cel, "w", zipfile.ZIP_DEFLATED) as zf:
        for belso, forras in TARTALOM.items():
            zf.write(forras, f"{NEV}/{belso}")
    return cel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ki", default=str(ROOT / "hordozhato" / "dist"))
    cel = epit(Path(ap.parse_args().ki))
    print(cel)


if __name__ == "__main__":
    sys.exit(main())
