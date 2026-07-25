"""Az automatikus ellenőrző hook végponttól végpontig tesztje.

Szimulált munkaterületen bizonyítja, hogy a hook (1) kassza-írásnál
ténylegesen lefuttatja az ellenőrzőt, (2) más fájloknál csendben marad,
(3) hibás bemenettől nem omlik össze.
"""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "auto-ellenorzes.sh"


def hook_futtat(munkaterulet, bemenet):
    return subprocess.run(
        ["bash", str(HOOK)], input=bemenet, capture_output=True,
        text=True, cwd=munkaterulet,
    )


def munkaterulet():
    td = tempfile.mkdtemp()
    (Path(td) / "penzugy").mkdir()
    shutil.copy(ROOT / "examples" / "minta-kivonat.csv",
                Path(td) / "penzugy" / "kassza.csv")
    (Path(td) / "scripts").mkdir()
    shutil.copy(ROOT / "scripts" / "ellenorzo.py",
                Path(td) / "scripts" / "ellenorzo.py")
    return td


class HookTeszt(unittest.TestCase):
    def test_kassza_irasnal_ellenoriz(self):
        td = munkaterulet()
        r = hook_futtat(td, '{"tool_input":{"file_path":"penzugy/kassza.csv"}}')
        self.assertEqual(r.returncode, 0)
        self.assertIn("[auto-ellenőrzés]", r.stdout)
        self.assertIn("620000", r.stdout, "az ellenőrző tényleg lefutott")

    def test_mas_fajlnal_csendben_marad(self):
        td = munkaterulet()
        r = hook_futtat(td, '{"tool_input":{"file_path":"README.md"}}')
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "")

    def test_hibas_bemenettol_nem_omlik_ossze(self):
        td = munkaterulet()
        for rossz in ["", "nem json", "{}"]:
            r = hook_futtat(td, rossz)
            self.assertEqual(r.returncode, 0,
                             f"hibás bemenetnél is exit 0 kell: {rossz!r}")


if __name__ == "__main__":
    unittest.main()
