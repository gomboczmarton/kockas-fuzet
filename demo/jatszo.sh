#!/usr/bin/env bash
# Egy demó-forgatókönyv lejátszása ÉLŐ modellel (Claude Code kell hozzá).
#
# Használat:  bash demo/jatszo.sh demo/forgatokonyvek/03-belefer.sh
#
# A forgatókönyv-fájl adja: CIM, PERSONA, NEV, MUNKA_DIR, setup(),
# opcionálisan LEPESEK (shell-parancsok) és TURNS (persona-üzenetek).
# A számokat minden lejátszásban a scripts/ellenorzo.py adja — a
# felvételek valódi, vágatlan munkamenetek.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RENDER="$REPO_ROOT/demo/render_stream.py"
OTTHON="${DEMO_OTTHON:-$HOME/otthon}"
MODELL="${DEMO_MODELL:-claude-sonnet-5}"

# Csak azok az eszközök, amikre a skilleknek tényleg szükségük van.
ALLOWED="Bash(python3:*),Bash(ls:*),Bash(head:*),Bash(tail:*),Bash(cat:*),Bash(wc:*),Bash(date:*),Bash(echo:*),Bash(mkdir:*),Bash(cp:*),Bash(grep:*),Bash(sort:*),Bash(bash:*),Read,Write,Edit,MultiEdit,Glob,Grep,Task,TodoWrite,Skill"

LEPESEK=()
TURNS=()
NEV="Te"
PERSONA=""
OUTRO="— vége · minden összeg a scripts/ellenorzo.py kimenetéből származik —"
# shellcheck source=/dev/null
source "$1"

mkdir -p "$OTTHON"
setup >/dev/null 2>&1 || setup

SID="$(python3 -c 'import uuid; print(uuid.uuid4())')"

futtat_claude() {
  local prompt="$1" elso="$2"
  local extra=(--session-id "$SID")
  [ "$elso" = "nem" ] && extra=(--resume "$SID")
  (
    cd "$MUNKA_DIR"
    timeout 600 env -u CLAUDE_CODE_SESSION_ID -u CLAUDE_CODE_CHILD_SESSION \
      -u CLAUDE_PID -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD \
      -u CLAUDE_PROJECT_DIR -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT \
      -u CLAUDE_CODE_DEBUG \
      claude -p "$prompt" "${extra[@]}" --model "$MODELL" \
      --permission-mode acceptEdits --allowedTools "$ALLOWED" \
      --output-format stream-json --verbose 2>/dev/null
  ) | python3 "$RENDER" stream
}

clear
python3 "$RENDER" banner "$CIM" "$PERSONA"

CURDIR="$MUNKA_DIR"
for lepes in "${LEPESEK[@]:-}"; do
  [ -z "$lepes" ] && continue
  python3 "$RENDER" gepel "$lepes" --nev "\$"
  case "$lepes" in
    cd\ *) CURDIR="$CURDIR/${lepes#cd }" ;;
    *) (cd "$CURDIR" && eval "$lepes" 2>&1) || true ;;
  esac
  sleep 0.6
done
MUNKA_DIR="$CURDIR"

elso="igen"
for turn in "${TURNS[@]:-}"; do
  [ -z "$turn" ] && continue
  python3 "$RENDER" gepel "$turn" --nev "$NEV"
  futtat_claude "$turn" "$elso"
  elso="nem"
  sleep 0.8
done

printf '\033[2m%s\033[0m\n' "$OUTRO"
sleep 1.5
