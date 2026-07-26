# Forgatókönyv: 1. lépcső — bemásolós recept, telepítés nélkül.
# Spec: evals/scenarios/01-elso-lepcso.md
source "$REPO_ROOT/demo/kozos.sh"

CIM="1. lépcső — bemásolós recept bármelyik AI-csevegőben"
PERSONA="Kata, 34 — még sosem használt AI-t pénzügyre; a receptet és a minta-kivonatot másolja be"
NEV="Kata"
MUNKA_DIR="$OTTHON/csevego"

setup() {
  rm -rf "$MUNKA_DIR"
  mkdir -p "$MUNKA_DIR"
}

RECEPT1="$(sed -n '/^Az alábbi banki/,/^\[IDE MÁSOLD A KIVONATOT\]$/p' "$REPO_ROOT/prompts/01-kivonat-elemzes.md")"
KIVONAT="$(cat "$REPO_ROOT/examples/minta-kivonat.csv")"
RECEPT2="$(sed -n '/^Készítsünk havi/,/tényszerűen\.$/p' "$REPO_ROOT/prompts/02-havi-terv.md")"

TURNS=(
  "${RECEPT1/\[IDE MÁSOLD A KIVONATOT\]/$KIVONAT}"
  "$RECEPT2"
)

OUTRO="— vége · 0. szint: az ellenőrzés a tiéd — a kapott képlet a saját táblázatodban számol —"
