#!/usr/bin/env bash
# Terminál-screencast készítése egy (vagy minden) forgatókönyvről.
#
# Használat:
#   bash demo/felvetel.sh                              # minden forgatókönyv
#   bash demo/felvetel.sh demo/forgatokonyvek/03-belefer.sh
#
# Kimenet: demo/felvetelek/<nev>.cast + .gif + .mp4
# Kellékek: asciinema (pip), agg, ffmpeg — lásd demo/README.md.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KI="$REPO_ROOT/demo/felvetelek"
mkdir -p "$KI"

AGG="${AGG:-agg}"
FFMPEG="${FFMPEG:-ffmpeg}"

felvesz() {
  local f="$1" nev
  nev="$(basename "$f" .sh)"
  echo "=== Felvétel: $nev ==="
  asciinema rec --overwrite \
    -c "bash '$REPO_ROOT/demo/jatszo.sh' '$f'" \
    "$KI/$nev.cast" </dev/null

  # fejléc-méret rögzítése, hogy a videó mindig 104×30-as legyen
  python3 - "$KI/$nev.cast" <<'PY'
import json, sys
p = sys.argv[1]
sorok = open(p).read().splitlines()
fej = json.loads(sorok[0])
fej["width"], fej["height"] = 104, 30
open(p, "w").write("\n".join([json.dumps(fej)] + sorok[1:]) + "\n")
PY

  "$AGG" --font-family "DejaVu Sans Mono" --font-size 18 \
    --idle-time-limit 3 "$KI/$nev.cast" "$KI/$nev.gif"
  "$FFMPEG" -y -loglevel error -i "$KI/$nev.gif" \
    -movflags faststart -pix_fmt yuv420p \
    -vf "fps=24,scale=trunc(iw/2)*2:trunc(ih/2)*2" \
    "$KI/kockas-fuzet-demo-$nev.mp4"
  echo "=== Kész: $KI/kockas-fuzet-demo-$nev.mp4 ==="
}

if [ $# -gt 0 ]; then
  for f in "$@"; do felvesz "$f"; done
else
  for f in "$REPO_ROOT"/demo/forgatokonyvek/*.sh; do felvesz "$f"; done
fi
