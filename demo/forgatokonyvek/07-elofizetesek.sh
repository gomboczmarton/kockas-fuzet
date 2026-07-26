# Forgatókönyv: elfelejtett előfizetések + "mire ment el a legtöbb?"
# (az 1. cikk 4. valós példája, harness-szinten). Spec: evals/scenarios/07-elofizetesek.md
source "$REPO_ROOT/demo/kozos.sh"

CIM="Mire ment el a legtöbb? — előfizetés-vadászat"
PERSONA="Péter, 45 — három hónap adata van; gyanítja, hogy fizet valamiért feleslegesen"
NEV="Péter"
MUNKA_DIR="$OTTHON/kockas-fuzet"

setup() {
  friss_klon
  penzugy_reset
  cp "$REPO_ROOT/demo/adatok/kassza-3honap.csv" "$MUNKA_DIR/penzugy/kassza.csv"
  cp "$REPO_ROOT/examples/minta-terv-2026-07.csv" "$MUNKA_DIR/penzugy/terv-2026-07.csv"
}

TURNS=(
  "Nézd át az elmúlt három hónapot: mire ment el a legtöbb, és milyen ismétlődő előfizetéseim vannak? Az az érzésem, valamiről el is feledkeztem."
  "A Netflixet tényleg fél éve nem nézzük. Mennyit spórolnék évente, ha lemondanám? De rendesen számold ki, ne fejből!"
)
