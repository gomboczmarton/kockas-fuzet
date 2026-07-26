# Közös setup-segédek a forgatókönyvekhez. A jatszo.sh tölti be,
# $OTTHON és $REPO_ROOT már definiálva van.

friss_klon() {
  # A demók abban a klónban játszódnak, amit egy felhasználó is kapna.
  if [ ! -d "$OTTHON/kockas-fuzet/.claude" ]; then
    rm -rf "$OTTHON/kockas-fuzet"
    (cd "$OTTHON" && git clone --quiet https://github.com/gomboczmarton/kockas-fuzet)
  fi
}

penzugy_reset() {
  # Üres penzugy/ munkaterület — minden forgatókönyv tiszta lappal indul.
  rm -rf "$OTTHON/kockas-fuzet/penzugy"
  mkdir -p "$OTTHON/kockas-fuzet/penzugy/kivonatok"
}
