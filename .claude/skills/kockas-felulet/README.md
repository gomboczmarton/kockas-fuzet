# kockas-felulet — a Kockás Füzet terminál-modja

Claude Code mod (függvény-hook plugin). A projekt `.claude/skills/` mappájából
magától töltődik be, amint a munkaterületet megbízhatónak jelölted; külön
telepítés nem kell. Fejlesztéshez: `claude --plugin-dir .claude/skills/kockas-felulet`.

## Mit rajzol

| Hely | Mit mutat | Felület |
|---|---|---|
| prompt fölött (`AbovePrompt`) | ▦ Kockás Füzet · hónap · 12 hónap négyzete · pecsét; alatta a döntést kérő kategóriák | terminál, asztali app |
| `/fuzetlap` panel (`Pane`) | terv–tény szalagok kategóriánként, összesítő, forrás-sor | terminálon szöveg-szalag, asztali/mobil appban SVG |
| nyugta (`$.ui.toast`) | „Ellenőrizve · rendben” / „… döntést kér: szabadido” a kassza vagy egy terv módosítása után | minden felület |
| kör vége (`TurnDuration`) | „▦ 3 mp” az angol „Baked for 3s” helyett | terminál |
| prompt alatt (`PromptHint`) | `· /fuzetlap · /belefer` tipp üres promptnál | terminál |

Ahol a panel nem jelenhet meg (nincs rajzoló felület), a `/fuzetlap` ugyanazt
markdown-táblaként adja vissza. Akkor is, ha telefonról vagy a claude.ai-ról,
Remote Controlon kérdezed: a mod ott nem rajzol, a panel a gép termináljában
nyílna meg, ezért a táblázat a válaszban érkezik.

## Szabályok, amiket a tesztek őriznek

1. **A geometria számolható, a kiírt szám nem.** A szalag hossza arány; minden
   számjegy a képernyőn betű szerint a `scripts/fuzetallapot.py` kimenetéből
   jön (szám-eredet teszt; egy kiszámolt százalékra elbukik).
2. **Hangnem.** Piros nincs (DESIGN.md), minősítő szó nincs, visszatéréskor a
   kihagyott hónapok nem jelennek meg.
3. **Nem kapu.** A mod nem tilt és nem dönt; az ellenőrzést a
   `.claude/settings.json` PostToolUse hookja kényszeríti, a mod csak mutatja.

```bash
claude plugin validate .claude/skills/kockas-felulet
claude plugin test .claude/skills/kockas-felulet
```

A típusok forrása a futó Claude Code saját deklarációja (a mod mellé a motor
írja, `.claude-plugin/types/`); az API korai hozzáférésű, kiadásonként
változhat — frissítés után futtasd újra a teszteket.
