#!/usr/bin/env bash
# Az összes eval futtatása. Zölden kell futnia minden változtatás előtt.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m unittest discover -s evals -v
echo
echo "MINDEN EVAL ZÖLD ✔"
