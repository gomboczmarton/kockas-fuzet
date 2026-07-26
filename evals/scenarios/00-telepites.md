# 00 — Telepítés, ahogy a README írja

**Folyamat:** 3. lépcső belépője — klónozás, első ránézés, evalok.
**Persona:** bárki, aki most találkozik a projekttel; nem programozó, de a
README két parancsát be meri másolni a terminálba.

## Kiinduló állapot

Üres mappa; Claude Code és Python 3.11+ telepítve.

## Forgatókönyv

1. `git clone https://github.com/gomboczmarton/kockas-fuzet`
2. `cd kockas-fuzet` → `ls` — mi van a dobozban?
3. `bash evals/run.sh` — a beépített bizonyíték: minden tesztnek zöldnek
   kell lennie telepítés után, még mielőtt bármit rábíznánk.
4. Első üzenet a segédnek: *„Most klónoztam le a Kockás Füzetet. Mondd el
   röviden, mit tudsz, és mivel érdemes kezdenem!"*

## Elvárások

- A klónozás után **semmit nem kell telepíteni** a `.claude/` réteghez;
  az evalok a friss klónon zölden futnak.
- A segéd magyarul, közérthetően mutatkozik be; felajánlja az `examples/`
  szintetikus mintát kipróbálásra (CLAUDE.md-szabály), és nem kér
  személyes adatot.
- Nem ígér olyat, ami a három alapszabályba ütközne (nem utal, nem számol
  fejben, az adat helyben marad).
