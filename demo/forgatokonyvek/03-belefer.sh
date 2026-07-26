# Forgatókönyv: /belefer parancs — gyors vásárlási döntés-kép.
# Spec: evals/scenarios/03-belefer.md
source "$REPO_ROOT/demo/kozos.sh"

CIM="Belefér? — gyors kép vásárlás előtt"
PERSONA="Réka, 29 — a boltban áll, harminc másodperce van dönteni"
NEV="Réka"
MUNKA_DIR="$OTTHON/kockas-fuzet"

setup() {
  friss_klon
  penzugy_reset
  cp "$REPO_ROOT/examples/minta-kivonat.csv" "$MUNKA_DIR/penzugy/kassza.csv"
  cp "$REPO_ROOT/examples/minta-terv-2026-07.csv" "$MUNKA_DIR/penzugy/terv-2026-07.csv"
}

TURNS=(
  "/belefer 8990 forintos társasjáték, szabadidő kategória"
  "Igazad van, most kihagyom — de jegyezd fel, hogy ez megvolt bennem, és megspóroltam."
)
