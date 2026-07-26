# Forgatókönyv: kivonat-konyvelo skill — augusztusi kivonat lekönyvelése.
# Spec: evals/scenarios/02-kivonat-konyvelo.md
source "$REPO_ROOT/demo/kozos.sh"

CIM="Kivonat-könyvelő — az új banki kivonat lekönyvelése"
PERSONA="Gábor, 41 — havonta egyszer néz rá; most jött meg a banki export"
NEV="Gábor"
MUNKA_DIR="$OTTHON/kockas-fuzet"

setup() {
  friss_klon
  penzugy_reset
  cp "$REPO_ROOT/examples/minta-kivonat.csv" "$MUNKA_DIR/penzugy/kassza.csv"
  cp "$REPO_ROOT/examples/minta-terv-2026-07.csv" "$MUNKA_DIR/penzugy/terv-2026-07.csv"
  cp "$REPO_ROOT/demo/adatok/kivonat-2026-08.csv" "$MUNKA_DIR/penzugy/kivonatok/"
}

TURNS=(
  "Megjött a bankból az augusztusi kivonat, betettem a penzugy/kivonatok mappába. Légyszi könyveld le."
  "A DM menjen haztartas kategóriába, a Wolt meg elelmiszer. A Tesco-s sort jól látod, az még a múltkori — azt hagyd ki."
)
