# Forgatókönyv: visszateres skill — két kihagyott hónap bepótlása.
# Spec: evals/scenarios/06-visszateres.md
source "$REPO_ROOT/demo/kozos.sh"

CIM="Visszatérés — két kihagyott hónap, szemrehányás nélkül"
PERSONA="Dóri, 36 — május vége óta nem nyitotta ki a füzetet"
NEV="Dóri"
MUNKA_DIR="$OTTHON/kockas-fuzet"

setup() {
  friss_klon
  penzugy_reset
  cp "$REPO_ROOT/demo/adatok/kassza-2026-05.csv" "$MUNKA_DIR/penzugy/kassza.csv"
  cp "$REPO_ROOT/demo/adatok/terv-2026-06.csv" "$MUNKA_DIR/penzugy/terv-2026-06.csv"
  cp "$REPO_ROOT/examples/minta-terv-2026-07.csv" "$MUNKA_DIR/penzugy/terv-2026-07.csv"
  cp "$REPO_ROOT/demo/adatok/kivonat-2026-06.csv" "$MUNKA_DIR/penzugy/kivonatok/"
  cp "$REPO_ROOT/demo/adatok/kivonat-2026-07.csv" "$MUNKA_DIR/penzugy/kivonatok/"
}

TURNS=(
  "Szia… májusban néztem rá utoljára, azóta csak gyűltek a kivonatok. Bepótolnám végre, ha nem gond."
  "A fogorvos menjen az egeszseg kategóriába, a Kifli az elelmiszer, a rendezvény pedig a szokásos havi klubestünk — az szabadido. Köszi, hogy nem csináltál belőle ügyet."
)
