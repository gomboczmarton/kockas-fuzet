# Forgatókönyv: havi-kor skill A) fele — következő havi terv tényadatokból.
# Spec: evals/scenarios/05-havi-terv.md
source "$REPO_ROOT/demo/kozos.sh"

CIM="Havi kör — augusztusi terv a saját számokból"
PERSONA="Bence, 33 — három hónapnyi adat után először tervez előre"
NEV="Bence"
MUNKA_DIR="$OTTHON/kockas-fuzet"

setup() {
  friss_klon
  penzugy_reset
  cp "$REPO_ROOT/demo/adatok/kassza-3honap.csv" "$MUNKA_DIR/penzugy/kassza.csv"
  cp "$REPO_ROOT/examples/minta-terv-2026-07.csv" "$MUNKA_DIR/penzugy/terv-2026-07.csv"
}

TURNS=(
  "Tervezzük meg az augusztust!"
  "Augusztus 20-án szülinapi bulit tartunk, az kb. 30 ezer plusz, és akkor jön az éves lakásbiztosítás is, 24 ezer. Más extra nem lesz."
)
