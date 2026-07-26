#!/usr/bin/env bash
# Feltöltésre kész formátumok a natív felvételekből:
#   - YouTube:  1920×1080 (letterbox, a terminál saját háttérszínével)
#   - LinkedIn: 1080×1080 négyzet (ugyanígy)
#
# Használat: bash demo/formatumok.sh          # minden natív mp4-re
# Kellék: ffmpeg (FFMPEG env-változóval cserélhető).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KI="$REPO_ROOT/demo/felvetelek"
FFMPEG="${FFMPEG:-ffmpeg}"
HATTER="272a35"   # az agg által renderelt terminál háttérszíne

mkdir -p "$KI/youtube" "$KI/linkedin"

for mp4 in "$KI"/kockas-fuzet-demo-*.mp4; do
  [ -e "$mp4" ] || continue
  nev="$(basename "$mp4")"
  "$FFMPEG" -y -loglevel error -i "$mp4" \
    -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x$HATTER" \
    -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -movflags faststart \
    "$KI/youtube/$nev"
  "$FFMPEG" -y -loglevel error -i "$mp4" \
    -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:color=0x$HATTER" \
    -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -movflags faststart \
    "$KI/linkedin/$nev"
  echo "kész: $nev (youtube + linkedin)"
done
