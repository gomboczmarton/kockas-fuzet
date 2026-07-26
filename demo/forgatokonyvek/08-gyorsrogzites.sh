# Forgatókönyv: útközbeni gyors-rögzítés — "írd fel, légyszi"
# (az 1. cikk blokk-példája és a 2. cikk útközbeni rögzítés-képe).
# Spec: evals/scenarios/08-gyorsrogzites.md
source "$REPO_ROOT/demo/kozos.sh"

CIM="Írd fel! — készpénzes költés rögzítése menet közben"
PERSONA="Juli, 31 — a piacról hazafelé, egy blokk a zsebében"
NEV="Juli"
MUNKA_DIR="$OTTHON/kockas-fuzet"

setup() {
  friss_klon
  penzugy_reset
  cp "$REPO_ROOT/examples/minta-kivonat.csv" "$MUNKA_DIR/penzugy/kassza.csv"
  cp "$REPO_ROOT/examples/minta-terv-2026-07.csv" "$MUNKA_DIR/penzugy/terv-2026-07.csv"
}

TURNS=(
  "Ma a piacon 4 300 forintot költöttem készpénzből zöldségre. Írd fel, légyszi — és mostantól a készpénzes blokkjaimat is így szeretném bemondani."
  "Jó, vezesd úgy, ahogy javasoltad — és a szabályt írd be a naplóba, hogy legközelebb már ne kelljen megbeszélnünk."
)
