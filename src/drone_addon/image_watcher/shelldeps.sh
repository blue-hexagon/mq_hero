#!/usr/bin/env bash

PKGS=("inotify-tools" "imagemagick")
MISSING=()

for pkg in "${PKGS[@]}"; do
  if ! dpkg-query -W -f='${Status}' "$pkg" 2>/dev/null | grep -q "install ok installed"; then
    MISSING+=("$pkg")
  fi
done

if (( ${#MISSING[@]} )); then
  echo "Installing missing packages: ${MISSING[*]}"

  if [[ $EUID -ne 0 ]]; then
    SUDO=sudo
  else
    SUDO=
  fi

  $SUDO apt-get update -qq
  $SUDO apt-get install -y --no-install-recommends "${MISSING[@]}"
else
  echo "All packages already installed."
fi

return 0 2>/dev/null || exit 0
