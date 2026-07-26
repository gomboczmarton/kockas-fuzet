# Forgatókönyv: /havizaras parancs — teljes havi zárás egyben.
# Spec: evals/scenarios/04-havizaras.md
source "$REPO_ROOT/demo/kozos.sh"

CIM="/havizaras — teljes havi zárás egyetlen paranccsal"
PERSONA="Anna, 38 — a családi kassza gazdája; hónap végi zárás"
NEV="Anna"
MUNKA_DIR="$OTTHON/kockas-fuzet"

setup() {
  friss_klon
  penzugy_reset
  printf 'datum;leiras;osszeg;kategoria;forras\n' > "$MUNKA_DIR/penzugy/kassza.csv"
  cp "$REPO_ROOT/examples/minta-terv-2026-07.csv" "$MUNKA_DIR/penzugy/terv-2026-07.csv"
  cp "$REPO_ROOT/demo/adatok/kivonat-2026-07.csv" "$MUNKA_DIR/penzugy/kivonatok/"
}

TURNS=(
  "/havizaras 2026-07"
  "A Kifli az elelmiszer. A rendezvény egyszeri volt — jubileum —, ott a keret maradhat; az élelmiszer-keretet viszont emeljük 110 ezerre a jövő hónaptól. És kérek egy riportot is."
)
