# Kockás Füzet Claude Code nélkül

A Kockás Füzet Claude Code-ra készült, de a tudása hordozható. Ebben a
mappában két belépő van azoknak, akik nem fejlesztők: egy **skill-csomag**
a chat-felületekre, és egy **helyi MCP szerver** a Claude Desktophoz, amely
a havi lapot képként (szalagokkal) is megmutatja.

## Melyiket válaszd?

| Felület | Mit kapsz | Hol van az adat | Mi tartatja be a szabályokat |
|---|---|---|---|
| **Claude.ai / ChatGPT / Gemini** — skill-csomag | könyvelés, terv–tény, „belefér?”, visszatérés beszélgetésben; a számokat a mellékelt `ellenorzo.py` adja | a szolgáltató szerverein (feltöltés + futtatás); a beszélgetés végén nem marad meg — a frissített `kassza.csv`-t letöltöd, legközelebb újra feltöltöd | csak a skill utasítása: **nincs hook**, ami minden módosítás után kikényszerítené az ellenőrzést |
| **Claude Desktop + helyi MCP** — Füzetlap-app | a fentiek, plusz a `fuzetlap` eszköz: terv–tény szalagok a beszélgetésben | a saját gépeden (`penzugy/`); csak az eszköz válasza kerül a beszélgetésbe | a szkript a gépeden fut; az ellenőrzés kikényszerítése itt sincs |
| **Claude Code** (a teljes rendszer) | minden, plusz terminál-felület és automatikus ellenőrzés | a saját gépeden | PostToolUse hook: minden kassza-módosítás után lefut az ellenőrző |

Bármelyik felületen: a modell elé kerülő szöveg a modell szolgáltatójához
megy. A „saját gépen marad” a fájlokra igaz, nem a beszélgetésre.

## 1. Skill-csomag (Claude.ai, ChatGPT, Gemini)

```bash
python3 hordozhato/build_skill.py      # -> hordozhato/dist/kockas-fuzet.zip
```

- **Claude.ai**: Customize → Skills → „+” → Upload a skill → a zip. Kell hozzá
  a „Code execution and file creation” beállítás (Settings → Capabilities).
- **ChatGPT**: Plugins → Skills → Create → Upload (a csomag az Agent Skills
  szabványt követi; fogyasztói csomagokban ez 2026 októberében béta).
- **Gemini app**: Skills → feltöltés (a szkriptek ott internet nélkül futnak —
  az `ellenorzo.py`-nak nem is kell).

A csomag a repó egyetlen forrásából épül (szkriptek, a `.claude/skills/`
leírásai referenciaként), így nem tud elcsúszni a Claude Code-os változattól.

## 2. Füzetlap-app (Claude Desktop, helyi MCP)

A `mcp/server.py` csak a Python standard könyvtárát használja. A Claude
Desktop beállításaiba (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "kockas-fuzet": {
      "command": "python3",
      "args": ["/ut/a/kockas-fuzet/hordozhato/mcp/server.py"],
      "env": { "KOCKAS_PENZUGY": "/ut/a/kockas-fuzet/penzugy" }
    }
  }
}
```

Utána a beszélgetésben: „mutasd a füzetlapot”. A Claude engedélyt kér a
megjelenítéshez; a lap az MCP Apps szabvány szerint rajzolódik (sandboxolt
keretben, külső erőforrás nélkül). Ahol a gazda nem tud rajzolni, ugyanaz a
lap markdown-táblaként érkezik — ugyanazokkal a számokkal.

A claude.ai webes és mobil felülete csak *távoli* MCP szervert ér el: ahhoz a
füzetet egy interneten elérhető szerverre kellene tenni. Ezt a Kockás Füzet
nem ajánlja (lásd a második alapszabályt).

## Ami mindenhol ugyanaz

Egy nézet-modell, sok felület: a `scripts/fuzetallapot.py` kimenetéből rajzol
a terminál-mod, a státuszsor, a markdown-tartalék és a Füzetlap-app. Egyik sem
számol; az `evals/test_hordozhato.py` ellenőrzi, hogy a képernyőn minden szám
betű szerint ebből jön, és hogy a nézet minden üzenete megfelel a hivatalos
MCP Apps sémának (`@modelcontextprotocol/ext-apps` 2.0.3):

```bash
KOCKAS_MCP_APPS_SEMA=<…/ext-apps/dist/src/generated/schema.json> bash evals/run.sh
```
