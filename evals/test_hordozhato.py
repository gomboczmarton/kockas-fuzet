"""A hordozható réteg bizonyítása (hordozhato/).

1. Skill-csomag: a zip a Claude.ai által elvárt szerkezetű, a szkriptek és a
   referenciák betűre azonosak a repóbelivel (nem csúszhat el), a kicsomagolt
   ellenorzo.py önállóan a GROUND-TRUTH számait adja, és a SKILL.md kimondja a
   három szabályt, a hook pótlását és az adatkezelési különbséget.
2. MCP szerver (stdio): kézfogás, az eszköz és a nézet metaadata a
   szabvány szerint, a szöveges tartalék ugyanazokat a számokat hordja, mint a
   structuredContent, és az a fuzetallapot.py kimenete.
3. MCP App nézet böngészőben (ha van node + playwright + a hivatalos séma):
   minden üzenet mindkét irányban megfelel a @modelcontextprotocol/ext-apps
   sémájának, és a rajzolt szöveg minden száma a nézet-modellből jön.
   KOCKAS_MCP_APPS_SEMA=<.../ext-apps/dist/src/generated/schema.json>
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HORD = ROOT / "hordozhato"
KIVONAT = ROOT / "examples" / "minta-kivonat.csv"
TERV = ROOT / "examples" / "minta-terv-2026-07.csv"
SZAM = re.compile(r"\d[\d ]*(?:,\d+)?")


def szamok(szoveg):
    tiszta = re.sub(r"\d{4}-\d{2}(-\d{2})?|\d{1,2}:\d{2}", " ", szoveg)
    return [s.replace(" ", "").replace(",", ".") for s in SZAM.findall(tiszta)]


def engedett(obj):
    ki = set()

    def jar(v):
        if isinstance(v, str) and re.fullmatch(r"-?\d+(\.\d+)?", v):
            ki.add(v.lstrip("-"))
        elif isinstance(v, list):
            for x in v:
                jar(x)
        elif isinstance(v, dict):
            for x in v.values():
                jar(x)
    jar(obj)
    return ki


def penzugy_mappa(td):
    p = Path(td) / "penzugy"
    p.mkdir()
    shutil.copy(KIVONAT, p / "kassza.csv")
    shutil.copy(TERV, p / "terv-2026-07.csv")
    return p


def mcp(uzenetek, penzugy):
    env = {**os.environ, "KOCKAS_PENZUGY": str(penzugy), "KOCKAS_MA": "2026-07"}
    r = subprocess.run([sys.executable, str(HORD / "mcp" / "server.py")],
                       input="".join(json.dumps(u) + "\n" for u in uzenetek),
                       capture_output=True, text=True, env=env, timeout=60)
    return {v["id"]: v for v in map(json.loads, r.stdout.splitlines())}


INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-11-25", "clientInfo": {"name": "teszt", "version": "0"},
                   "capabilities": {"extensions": {"io.modelcontextprotocol/ui":
                                                   {"mimeTypes": ["text/html;profile=mcp-app"]}}}}}
HIVAS = {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "fuzetlap", "arguments": {}}}


class SkillCsomagTeszt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.td = tempfile.TemporaryDirectory()
        r = subprocess.run([sys.executable, str(HORD / "build_skill.py"), "--ki", cls.td.name],
                           capture_output=True, text=True, timeout=60)
        cls.zip = Path(r.stdout.strip())

    @classmethod
    def tearDownClass(cls):
        cls.td.cleanup()

    def test_szerkezet_a_claude_ai_szerint(self):
        with zipfile.ZipFile(self.zip) as z:
            nevek = z.namelist()
        self.assertEqual({n.split("/")[0] for n in nevek}, {"kockas-fuzet"},
                         "a zip legfelső szintjén a skill mappája álljon")
        self.assertIn("kockas-fuzet/SKILL.md", nevek)

    def test_frontmatter_hordozhato(self):
        with zipfile.ZipFile(self.zip) as z:
            skill = z.read("kockas-fuzet/SKILL.md").decode()
        fm = re.match(r"^---\n(.*?)\n---\n", skill, re.S).group(1)
        nev = re.search(r"^name: (.+)$", fm, re.M).group(1).strip()
        self.assertEqual(nev, "kockas-fuzet")
        self.assertRegex(nev, r"^[a-z0-9-]{1,64}$", "ASCII kötőjeles név minden felületen")
        leiras = " ".join(fm.split("description:", 1)[1].replace(">", "").split())
        self.assertLessEqual(len(leiras), 1024)
        self.assertLess(skill.count("\n"), 500)

    def test_a_szabalyok_es_a_potlasok_ki_vannak_mondva(self):
        with zipfile.ZipFile(self.zip) as z:
            skill = z.read("kockas-fuzet/SKILL.md").decode()
        for kell in ("A modell sosem számol", "scripts/ellenorzo.py", "--json",
                     "nincs hook", "szerverein", "letöltésre", "A pénzhez csak a felhasználó nyúl",
                     "A visszatérés ünnep"):
            self.assertIn(kell, skill)

    def test_szkriptek_es_referenciak_betura_azonosak(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("build_skill", HORD / "build_skill.py")
        build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)
        with zipfile.ZipFile(self.zip) as z:
            for belso, forras in build.TARTALOM.items():
                self.assertEqual(z.read(f"kockas-fuzet/{belso}"), forras.read_bytes(), belso)

    def test_kicsomagolva_onalloan_szamol(self):
        with tempfile.TemporaryDirectory() as td:
            with zipfile.ZipFile(self.zip) as z:
                z.extractall(td)
            r = subprocess.run([sys.executable, f"{td}/kockas-fuzet/scripts/ellenorzo.py", str(KIVONAT),
                                "--terv", str(TERV), "--honap", "2026-07", "--json"],
                               capture_output=True, text=True, timeout=60)
            n = json.loads(r.stdout)
            self.assertEqual((n["bevetel"], n["kiadas"], n["egyenleg_valtozas"]),
                             ("620000", "-234030", "285970"))


class McpSzerverTeszt(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.penzugy = penzugy_mappa(self.td.name)

    def tearDown(self):
        self.td.cleanup()

    def test_kezfogas_eszkoz_es_nezet_a_szabvany_szerint(self):
        v = mcp([INIT, {"jsonrpc": "2.0", "method": "notifications/initialized"},
                 {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                 {"jsonrpc": "2.0", "id": 4, "method": "resources/read",
                  "params": {"uri": "ui://kockas-fuzet/fuzetlap.html"}}], self.penzugy)
        self.assertEqual(v[1]["result"]["serverInfo"]["name"], "kockas-fuzet")
        meta = v[2]["result"]["tools"][0]["_meta"]
        self.assertEqual(meta["ui"]["resourceUri"], "ui://kockas-fuzet/fuzetlap.html")
        self.assertEqual(meta["ui/resourceUri"], meta["ui"]["resourceUri"], "régi gazdáknak is")
        tart = v[4]["result"]["contents"][0]
        self.assertEqual(tart["mimeType"], "text/html;profile=mcp-app")
        self.assertNotRegex(tart["text"], r"(src|href)=[\"']https?:",
                            "a nézet nem tölt külső erőforrást (szigorú CSP)")

    def test_szoveges_tartalek_ugyanazokat_a_szamokat_hordja(self):
        e = mcp([INIT, HIVAS], self.penzugy)[3]["result"]
        szoveg = e["content"][0]["text"]
        lathato = szamok(szoveg)
        self.assertGreater(len(lathato), 15)
        self.assertTrue(set(lathato) <= engedett(e["structuredContent"]),
                        set(lathato) - engedett(e["structuredContent"]))
        self.assertIn("| szabadido | 15 000 | 10 000 | +5 000 · döntést kér |", szoveg)

    def test_structured_content_a_fuzetallapot_kimenete(self):
        e = mcp([INIT, HIVAS], self.penzugy)[3]["result"]["structuredContent"]
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "fuzetallapot.py"),
                            "--penzugy", str(self.penzugy), "--ma", "2026-07"],
                           capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
        vart = json.loads(r.stdout)
        e.pop("frissitve"), vart.pop("frissitve")
        self.assertEqual(e, vart)

    def test_hibak_jsonrpc_kodokkal(self):
        v = mcp([INIT, {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "nincs"}},
                 {"jsonrpc": "2.0", "id": 6, "method": "nincs/ilyen"}], self.penzugy)
        self.assertEqual(v[5]["error"]["code"], -32602)
        self.assertEqual(v[6]["error"]["code"], -32601)


SEMA = os.environ.get("KOCKAS_MCP_APPS_SEMA", "")
NODE_MODULES = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip() \
    if shutil.which("npm") else ""


@unittest.skipUnless(Path(SEMA).is_file() and NODE_MODULES and (Path(NODE_MODULES) / "playwright").is_dir(),
                     "böngészős próba: KOCKAS_MCP_APPS_SEMA + node playwright kell")
class McpNezetBongeszobenTeszt(unittest.TestCase):
    def test_uzenetek_a_hivatalos_semanak_felelnek_meg_es_a_szamok_eredetiek(self):
        import jsonschema
        defs = json.loads(Path(SEMA).read_text())["$defs"]

        def ervenyes(nev, obj):
            jsonschema.Draft202012Validator({"$defs": defs, "$ref": f"#/$defs/{nev}"}).validate(obj)

        with tempfile.TemporaryDirectory() as td:
            e = mcp([INIT, HIVAS], penzugy_mappa(td))[3]["result"]
            (Path(td) / "eredmeny.json").write_text(json.dumps(e))
            r = subprocess.run(["node", str(HORD / "mcp" / "proba" / "gazda_proba.cjs"),
                                str(HORD / "mcp" / "fuzetlap.html"), f"{td}/eredmeny.json", td],
                               capture_output=True, text=True, timeout=180,
                               env={**os.environ, "NODE_PATH": NODE_MODULES})
            self.assertEqual(r.returncode, 0, r.stderr)
            uzenetek = json.loads((Path(td) / "uzenetek.json").read_text())
            semak = {"ui/initialize": "McpUiInitializeRequest",
                     "ui/notifications/initialized": "McpUiInitializedNotification",
                     "ui/notifications/size-changed": "McpUiSizeChangedNotification",
                     "ui/notifications/tool-result": "McpUiToolResultNotification"}
            latott = set()
            for u in uzenetek:
                m = u["m"]
                if "method" in m:
                    ervenyes(semak[m["method"]], {k: m[k] for k in m if k not in ("jsonrpc", "id")})
                    latott.add(m["method"])
                else:
                    ervenyes("McpUiInitializeResult", m["result"])
            self.assertEqual(latott, set(semak), "a teljes kézfogás lefutott")
            # a séma-ellenőrzés harap: protocolVersion nélküli kérés elbukik
            with self.assertRaises(jsonschema.ValidationError):
                ervenyes("McpUiInitializeRequest", {"method": "ui/initialize",
                                                    "params": {"appInfo": {"name": "x", "version": "0"},
                                                               "appCapabilities": {}}})
            for tema in ("light", "dark"):
                lathato = szamok((Path(td) / f"szoveg-{tema}.txt").read_text())
                self.assertGreater(len(lathato), 15)
                self.assertTrue(set(lathato) <= engedett(e["structuredContent"]))


if __name__ == "__main__":
    unittest.main()
