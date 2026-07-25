"""Az ellenorzo.py determinisztikus viselkedésének bizonyítása.

A mérce az examples/GROUND-TRUTH.md kézzel rögzített igazsága: a szkriptnek
fillérre ugyanazt kell adnia, a szándékos tervtúllépést és a duplikátumot
jeleznie kell, a tiszta esetben pedig nullával kell kilépnie.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ellenorzo.py"
KIVONAT = ROOT / "examples" / "minta-kivonat.csv"
TERV = ROOT / "examples" / "minta-terv-2026-07.csv"


def futtat(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=ROOT,
    )


class GroundTruthTeszt(unittest.TestCase):
    def test_osszegek_fillerre_egyeznek(self):
        r = futtat(str(KIVONAT), "--honap", "2026-07")
        self.assertIn("620000", r.stdout, "bevétel")
        self.assertIn("-234030", r.stdout, "fogyasztási kiadás")
        self.assertIn("-100000", r.stdout, "átvezetés")
        self.assertIn("285970", r.stdout, "egyenleg-változás")
        self.assertIn("-99450", r.stdout, "élelmiszer kategória")
        self.assertIn("-35390", r.stdout, "rezsi kategória")

    def test_terv_teny_tullepes_jelzese(self):
        r = futtat(str(KIVONAT), "--terv", str(TERV), "--honap", "2026-07")
        self.assertIn("TÚLLÉPÉS 5000", r.stdout,
                      "a szabadidő 5000 Ft-os túllépését jeleznie kell")
        self.assertEqual(r.returncode, 1,
                         "túllépésnél nem-nulla kilépési kód kell")

    def test_tiszta_honap_nullaval_lep_ki(self):
        with tempfile.TemporaryDirectory() as td:
            terv = Path(td) / "terv.csv"
            # ugyanaz a terv, de a szabadidő keretét a tényre emeljük
            sorok = TERV.read_text().replace("szabadido;10000", "szabadido;15000")
            terv.write_text(sorok)
            r = futtat(str(KIVONAT), "--terv", str(terv), "--honap", "2026-07")
            self.assertNotIn("TÚLLÉPÉS", r.stdout)
            self.assertEqual(r.returncode, 0, "tiszta esetben exit 0 kell")

    def test_duplikatum_gyanu_jelzese(self):
        with tempfile.TemporaryDirectory() as td:
            kassza = Path(td) / "kassza.csv"
            sorok = KIVONAT.read_text().rstrip("\n").splitlines()
            sorok.append(sorok[6])  # a LIDL-sor még egyszer
            kassza.write_text("\n".join(sorok) + "\n")
            r = futtat(str(kassza))
            self.assertIn("FIGYELEM", r.stdout)
            self.assertIn("LIDL", r.stdout)
            self.assertEqual(r.returncode, 1)

    def test_honap_szures_ures_honapra(self):
        r = futtat(str(KIVONAT), "--honap", "2026-06")
        self.assertIn("Nincs adat", r.stdout)
        self.assertEqual(r.returncode, 1)

    def test_hibas_osszeg_hibat_ad(self):
        with tempfile.TemporaryDirectory() as td:
            kassza = Path(td) / "kassza.csv"
            kassza.write_text(
                "datum;leiras;osszeg;kategoria;forras\n"
                "2026-07-01;ROSSZ SOR;nem-szam;egyeb;teszt\n"
            )
            r = futtat(str(kassza))
            self.assertEqual(r.returncode, 2)
            self.assertIn("HIBA", r.stdout)

    def test_determinisztikus_ket_futas_azonos(self):
        r1 = futtat(str(KIVONAT), "--terv", str(TERV))
        r2 = futtat(str(KIVONAT), "--terv", str(TERV))
        self.assertEqual(r1.stdout, r2.stdout,
                         "két futásnak bitre azonos kimenetet kell adnia")


if __name__ == "__main__":
    unittest.main()
