#!/usr/bin/env bash
# PostToolUse hook: ha a módosított fájl a kasszát vagy egy tervet érint,
# futtasd le az ellenőrzőt. A hook stdin-en kapja a tool-hívás JSON-ját.
set -euo pipefail

INPUT=$(cat)
FILE=$(printf '%s' "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null || true)

case "$FILE" in
  *kassza.csv|*terv-*.csv)
    if [ -f penzugy/kassza.csv ]; then
      echo "[auto-ellenőrzés] ${FILE##*/} módosult — ellenorzo.py fut:"
      python3 scripts/ellenorzo.py penzugy/kassza.csv || {
        echo "[auto-ellenőrzés] FIGYELEM: az ellenőrző eltérést/duplikátumot jelzett — nézd át a fenti kimenetet, mielőtt továbblépsz."
      }
    fi
    ;;
esac
exit 0
