# Evalok — mi bizonyítja, hogy a harness működik?

Futtatás (a repo gyökeréből): `bash evals/run.sh` — minden változtatás előtt
zölden kell futnia. Csak a Python szabványkönyvtárat használja.

## Rétegek

1. **`test_ellenorzo.py` — a számoló mag** (a harness 1. alapszabálya).
   A `scripts/ellenorzo.py`-t az `examples/GROUND-TRUTH.md` kézzel rögzített
   igazsága ellen méri: fillérre pontos összegek, a szándékos tervtúllépés
   és a duplikátum jelzése, tiszta esetben exit 0, hibás adatnál értelmes
   hiba, és két futás bitre azonos kimenete (determinizmus).
2. **`test_szerkezet.py` — a Claude Code-szerkezet.** A skillek, a
   verifikátor subagent és a parancsok a `.claude/` alatt vannak, érvényes
   frontmatterrel; a verifikátornak nincs írás-joga; a hook be van kötve a
   `.claude/settings.json`-ba és futtatható; a CLAUDE.md tartalmazza az
   alapszabályokat; a README linkjei élnek; és sehol nincs blog-hivatkozás.
3. **`test_hook.py` — a biztonsági öv.** Szimulált munkaterületen
   bizonyítja, hogy kassza-írás után a hook tényleg lefuttatja az
   ellenőrzőt, más fájloknál csendben marad, és hibás bemenettől sem
   omlik össze.

## Amit ez az eval-szint NEM fed le (következő lépcső)

- **Beszélgetés-szintű evalok**: a skillek hangneme (shame-free rubrika) és
  eljárás-követése persona-alapú tesztet igényel élő modellel — terv:
  szintetikus personák + rubrika, a BUILD-ORDER 3. lépésének
  kész-kritériuma szerint.
- A Google Sheets-oldali képletek (templates/) helyessége — ott a
  táblázat maga az ellenőr.
