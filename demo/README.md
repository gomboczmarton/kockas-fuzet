# Demók — a forgatókönyvek lejátszása és felvétele

Ez a mappa játssza le az `evals/scenarios/` persona-forgatókönyveit **élő
modellel**, és készít róluk terminál-screencastot (YouTube-ra feltölthető
MP4-et). A felvételek vágatlan, valódi munkamenetek: minden összeg a
`scripts/ellenorzo.py`-ból jön, a válaszokat tényleg a modell adja.

## Fájlok

- `jatszo.sh` — egy forgatókönyv lejátszása a terminálban
  (persona-üzenet „gépelve", majd a segéd válasza élőben).
- `render_stream.py` — a Claude Code stream-json kimenetének olvasható
  megjelenítése (szöveg, eszközhívások, ellenőrző-kimenet).
- `felvetel.sh` — asciinema-felvétel + GIF (agg) + MP4 (ffmpeg).
- `forgatokonyvek/` — a lejátszható forgatókönyv-konfigok (persona,
  kiinduló állapot, üzenetek); a leírásuk az `evals/scenarios/`-ban.
- `adatok/` — szintetikus kellék-adatok (banki formátumú kivonatok,
  több-havi kassza) — minden adat kitalált.
- `kozos.sh` — közös setup-segédek (friss klón, üres munkaterület).

## Lejátszás

Kell hozzá: [Claude Code](https://claude.com/claude-code) (bejelentkezve)
és Python 3.11+.

```bash
bash demo/jatszo.sh demo/forgatokonyvek/03-belefer.sh
```

A lejátszó a `$HOME/otthon/kockas-fuzet` friss klónban dolgozik (a
`DEMO_OTTHON` környezeti változóval átirányítható), a modell alapból
`claude-sonnet-5` (`DEMO_MODELL`-lel cserélhető). Minden futás tiszta
`penzugy/` munkaterülettel indul, a forgatókönyv setupja szerint.

## Felvétel

Kellékek: `pip install asciinema`, az [agg](https://github.com/asciinema/agg)
bináris és `ffmpeg`.

```bash
bash demo/felvetel.sh                                # mind a hét
bash demo/felvetel.sh demo/forgatokonyvek/06-visszateres.sh
```

Kimenet: `demo/felvetelek/kockas-fuzet-demo-<nev>.mp4` (+ a köztes `.cast`
és `.gif`). A `.cast` fájlok szövegesek és kicsik — ezek a felvételek
„forráskódjai"; a videók YouTube-ra kerülnek, a repóba nem.

## Fontos

A demók szintetikus adatokkal futnak (`examples/` + `demo/adatok/`) —
személyes pénzügyi adat a felvételekbe nem kerül.
