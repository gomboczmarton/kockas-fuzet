"""A megjelenítő réteg bizonyítása.

Három réteg, egy forrás: az ellenorzo.py számol, a fuzetallapot.py eldönti a
helyzetet, a státuszsor és a terminál-mod csak rajzol. Ezek a tesztek azt
mutatják, hogy a gépi kimenet (--json) fillérre a GROUND-TRUTH.md értékeit
adja, a helyzet-döntés a hangnem-szabályt követi (visszatéréskor nincs
hátralék), és a mod saját tesztjei is zöldek, ha a gépen van Claude Code.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ELLENORZO = ROOT / "scripts" / "ellenorzo.py"
ALLAPOT = ROOT / "scripts" / "fuzetallapot.py"
KIVONAT = ROOT / "examples" / "minta-kivonat.csv"
TERV = ROOT / "examples" / "minta-terv-2026-07.csv"
MOD = ROOT / ".claude" / "skills" / "kockas-felulet"
TILTOTT = ("sajnos", "megint", " csak ", "kudarc", "hátralék", "lemarad", "elmarad")


def futtat(*args):
    return subprocess.run([sys.executable, *map(str, args)], stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, cwd=ROOT, timeout=60)


class GepiKimenetTeszt(unittest.TestCase):
    def test_json_a_ground_truth_szamait_adja(self):
        r = futtat(ELLENORZO, KIVONAT, "--terv", TERV, "--honap", "2026-07", "--json")
        n = json.loads(r.stdout)
        self.assertEqual((n["bevetel"], n["kiadas"], n["atvezetes"], n["egyenleg_valtozas"]),
                         ("620000", "-234030", "-100000", "285970"))
        kat = {k["kategoria"]: k["osszeg"] for k in n["kategoriak"]}
        self.assertEqual(kat["elelmiszer"], "-99450")
        tullep = [t for t in n["terv_teny"] if t["allapot"] == "tullepes"]
        self.assertEqual([(t["kategoria"], t["tullepes"]) for t in tullep], [("szabadido", "5000")])
        self.assertEqual(n["allapot"], "dontest_ker")

    def test_json_es_szoveg_kilepesi_kodja_azonos(self):
        for extra in ([], ["--honap", "2026-06"], ["--terv", TERV, "--honap", "2026-07"]):
            szoveg = futtat(ELLENORZO, KIVONAT, *extra)
            gepi = futtat(ELLENORZO, KIVONAT, *extra, "--json")
            self.assertEqual(szoveg.returncode, gepi.returncode, extra)
            self.assertEqual(json.loads(gepi.stdout)["kilepes"], gepi.returncode)

    def test_json_hibas_sornal_hiba_allapot(self):
        with tempfile.TemporaryDirectory() as td:
            kassza = Path(td) / "kassza.csv"
            kassza.write_text("datum;leiras;osszeg;kategoria;forras\n"
                              "2026-07-01;ROSSZ SOR;nem-szam;egyeb;teszt\n")
            r = futtat(ELLENORZO, kassza, "--json")
            self.assertEqual(r.returncode, 2)
            self.assertEqual(json.loads(r.stdout)["allapot"], "hiba")


class HelyzetTeszt(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.penzugy = Path(self.td.name) / "penzugy"
        self.penzugy.mkdir()
        shutil.copy(KIVONAT, self.penzugy / "kassza.csv")
        shutil.copy(TERV, self.penzugy / "terv-2026-07.csv")

    def tearDown(self):
        self.td.cleanup()

    def allapot(self, ma, *extra):
        r = futtat(ALLAPOT, "--penzugy", self.penzugy, "--ma", ma, *extra)
        self.assertEqual(r.returncode, 0, "a megjelenítés sosem kapu: mindig 0")
        return r.stdout if extra else json.loads(r.stdout)

    def test_havi_lap_a_mostani_honapra(self):
        a = self.allapot("2026-07")
        self.assertEqual((a["helyzet"], a["nezet"]["honap"]), ("havi", "2026-07"))

    def test_ures_honap_elejen_a_legutobbi_konyvelt(self):
        a = self.allapot("2026-08")
        self.assertEqual((a["helyzet"], a["nezet"]["honap"]), ("havi", "2026-07"))

    def test_visszatereskor_nincs_honap_es_nincs_szam(self):
        a = self.allapot("2026-10")
        self.assertEqual(a["helyzet"], "visszateres")
        self.assertIsNone(a["nezet"], "visszatéréskor a lemaradás nem kerül elő")
        sor = self.allapot("2026-10", "--sor")
        self.assertIn("jó, hogy itt vagy", sor)
        tiszta = re.sub(r"\x1b\[[0-9;]*m", "", sor)
        self.assertFalse(any(c.isdigit() for c in tiszta), tiszta)

    def test_ures_fuzet(self):
        (self.penzugy / "kassza.csv").unlink()
        self.assertEqual(self.allapot("2026-07")["helyzet"], "ures")

    def test_statusz_sor_hangnem(self):
        for ma in ("2026-07", "2026-08", "2026-10"):
            sor = self.allapot(ma, "--sor").lower()
            for szo in TILTOTT:
                self.assertNotIn(szo, sor, (ma, szo))


class BeallitasTeszt(unittest.TestCase):
    def test_stabil_reteg_a_settingsben(self):
        b = json.loads((ROOT / ".claude" / "settings.json").read_text())
        self.assertIn("fuzetallapot.py --sor", b["statusLine"]["command"])
        self.assertEqual(b["spinnerVerbs"]["mode"], "replace")
        for tipp in b["spinnerTipsOverride"]["tips"]:
            for szo in TILTOTT:
                self.assertNotIn(szo, tipp.lower())

    def test_mod_a_helyen(self):
        manifest = json.loads((MOD / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "kockas-felulet")
        self.assertTrue((MOD / "hooks" / "register.tsx").exists())
        self.assertTrue(list((MOD / "tests").glob("*.test.tsx")))

    @unittest.skipUnless(shutil.which("claude"), "Claude Code nincs telepítve")
    def test_mod_validalva_es_tesztjei_zoldek(self):
        v = subprocess.run(["claude", "plugin", "validate", str(MOD)],
                           capture_output=True, text=True, timeout=120)
        self.assertEqual(v.returncode, 0, v.stdout + v.stderr)
        t = subprocess.run(["claude", "plugin", "test", str(MOD)],
                           capture_output=True, text=True, timeout=300)
        self.assertEqual(t.returncode, 0, t.stdout + t.stderr)


if __name__ == "__main__":
    unittest.main()
