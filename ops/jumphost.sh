#!/usr/bin/env bash
set -euo pipefail

# =========================
# CONFIG
# =========================
trap '' SIGINT SIGTERM SIGQUIT SIGTSTP

SOURCE_IP="172.16.20.10"

# format: "name|user@host|port(optional)"
TARGETS=(
  "rpi01|toor@172.16.30.10|22"
  "rpi02|toor@172.16.30.11|22"
  "observability-stack01|toor@172.16.20.224|22"
  "drone-sim01|toor@172.16.20.225|22"
  "ftpes01|toor@172.16.20.192|22"
  "proxmox|root@10.60.60.11|22"
  "dc01|administrator@172.16.20.2|22"
  "dc02|administrator@172.16.20.3|22"
  "coresw01|admin@172.16.10.2|22"
  "coresw02|admin@172.16.10.3|22"
  "wg-cpe01|admin@172.16.20.1|22"
  "wg-rorendegaard|admin@10.60.1.200|22"
  "wg-tagensgaard|admin@10.60.1.201|22"
  "prtg01|administrator@172.16.20.7|22"
)

# =========================
# FUNCTIONS
# =========================

print_menu() {
  clear
  echo
  echo "Jump Host Selector (source IP: $SOURCE_IP)"
  echo "-------------------------------------------"
  for i in "${!TARGETS[@]}"; do
    IFS='|' read -r name conn port <<< "${TARGETS[$i]}"
    printf " [%d] %s (%s)\n" "$i" "$name" "$conn"
  done
  echo
}

validate_source_ip() {
  if ! ip addr show | grep -q "$SOURCE_IP"; then
    echo "Source IP $SOURCE_IP not present on this host"
    exit 1
  fi
}

jump() {
  local entry="$1"
  IFS='|' read -r name conn port <<< "$entry"

  echo "Jumping to $name ($conn) from $SOURCE_IP"

  ssh \
    -b "$SOURCE_IP" \
    -p "$port" \
    -o ExitOnForwardFailure=yes \
    -o ServerAliveInterval=120 \
    -o ConnectTimeout=5 \
    -o ServerAliveCountMax=5 \
    "$conn"
}

# =========================
# MAIN
# =========================

while :
do
  validate_source_ip
  print_menu

  read -rp "Select target number: " choice

  if [[ "$choice" == "KOde12345!!?" ]]; then
    exit
  elif [[ ! "$choice" =~ ^[0-9]+$ ]] || [[ "$choice" -ge "${#TARGETS[@]}" ]]; then
    echo "Invalid selection"
    sleep 2
    continue
  fi
  jump "${TARGETS[$choice]}" || continue

done
