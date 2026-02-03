#!/usr/bin/env bash

PKGS=("inotify-tools" "imagemagick")
MISSING=()

for pkg in "${PKGS[@]}"; do
  if ! dpkg -s "$pkg" >/dev/null 2>&1; then
    MISSING+=("$pkg")
  fi
done

if [ ${#MISSING[@]} -ne 0 ]; then
  echo "Installing missing packages: ${MISSING[*]}"
  sudo apt update
  sudo apt install -y --no-install-recommends "${MISSING[@]}"
else
  echo "All packages already installed."
fi

return 0 2>/dev/null || exit 0
