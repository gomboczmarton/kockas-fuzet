"""A Claude Code-szerkezet helyességének bizonyítása.

Azt ellenőrzi, hogy a harness komponensei ott vannak, ahol a Claude Code
keresi őket (.claude/ alatt), érvényes frontmatterrel, és hogy a README
linkjei nem mutatnak sehova.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def frontmatter(path):
    szoveg = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", szoveg, re.S)
    return m.group(1) if m else None


class SzerkezetTeszt(unittest.TestCase):
    def test_skillek_a_claude_alatt(self):
        for nev in ["kivonat-konyvelo", "havi-kor", "visszateres"]:
            p = ROOT / ".claude" / "skills" / nev / "SKILL.md"
            self.assertTrue(p.exists(), f"hiányzik: {p}")
            fm = frontmatter(p)
            self.assertIsNotNone(fm, f"{nev}: nincs frontmatter")
            self.assertIn(f"name: {nev}", fm)
            self.assertIn("description:", fm)

    def test_subagent_a_claude_alatt(self):
        p = ROOT / ".claude" / "agents" / "penzugyi-ellenor.md"
        self.assertTrue(p.exists())
        fm = frontmatter(p)
        self.assertIn("name: penzugyi-ellenor", fm)
        self.assertIn("tools:", fm)
        # a verifikátor nem kaphat írás-jogot
        self.assertNotIn("Write", fm)
        self.assertNotIn("Edit", fm)

    def test_parancsok_a_claude_alatt(self):
        for nev in ["havizaras", "belefer"]:
            p = ROOT / ".claude" / "commands" / f"{nev}.md"
            self.assertTrue(p.exists(), f"hiányzik: {p}")
            self.assertIn("description:", frontmatter(p) or "")

    def test_hook_bekotve_es_futtathato(self):
        beallitasok = json.loads((ROOT / ".claude" / "settings.json").read_text())
        hookok = beallitasok["hooks"]["PostToolUse"]
        parancsok = [h["command"] for blokk in hookok for h in blokk["hooks"]]
        self.assertIn(".claude/hooks/auto-ellenorzes.sh", parancsok)
        szkript = ROOT / ".claude" / "hooks" / "auto-ellenorzes.sh"
        self.assertTrue(szkript.exists())
        self.assertTrue(szkript.stat().st_mode & 0o111, "nem futtatható")

    def test_klaud_md_es_alapszabalyok(self):
        szoveg = (ROOT / "CLAUDE.md").read_text()
        for kulcs in ["A modell sosem számol", "penzugy/", "ellenorzo.py",
                      "Shame-free"]:
            self.assertIn(kulcs, szoveg, f"CLAUDE.md-ből hiányzik: {kulcs}")

    def test_readme_linkjei_elnek(self):
        szoveg = (ROOT / "README.md").read_text()
        for cel in re.findall(r"\]\((?!http)([^)#]+)\)", szoveg):
            self.assertTrue((ROOT / cel).exists(),
                            f"halott README-link: {cel}")

    def test_nincs_blog_hivatkozas(self):
        sajat = Path(__file__).resolve()
        for p in ROOT.rglob("*"):
            if p.resolve() == sajat:
                continue  # a minta önmagát találná meg
            if p.is_file() and ".git" not in p.parts and p.suffix in {
                    ".md", ".py", ".sh", ".json", ".csv"}:
                self.assertNotRegex(
                    p.read_text(errors="ignore"), r"(?i)kiszamolo|kiszámoló",
                    f"blog-hivatkozás maradt: {p}")


if __name__ == "__main__":
    unittest.main()
