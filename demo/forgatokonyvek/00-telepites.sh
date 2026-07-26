# Forgatókönyv: telepítés pontosan úgy, ahogy a README írja.
# Spec: evals/scenarios/00-telepites.md
source "$REPO_ROOT/demo/kozos.sh"

CIM="Telepítés — klónozástól az első zöld evalig"
PERSONA="Bárki, aki most találkozik először a Kockás Füzettel"
NEV="Te"
MUNKA_DIR="$OTTHON"

setup() {
  rm -rf "$OTTHON/kockas-fuzet"
}

LEPESEK=(
  "git clone https://github.com/gomboczmarton/kockas-fuzet"
  "cd kockas-fuzet"
  "ls"
  "bash evals/run.sh"
)

TURNS=(
  "Szia! Most klónoztam le a Kockás Füzetet. Mondd el röviden, mit tudsz, és mivel érdemes kezdenem!"
)
