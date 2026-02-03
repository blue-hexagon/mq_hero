#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

source /app/shelldeps.sh

upload_ftpes() {
  local file="$1"

  lftp -u "$FTP_USER","$FTP_PASS" "$FTP_HOST" <<EOF
set ftp:ssl-force true
set ftp:ssl-protect-data true
set ssl:verify-certificate false
set net:limit-rate 1M
set net:max-retries 3
set net:timeout 20
cd "$FTP_REMOTE_DIR"
put "$file" -o "$(basename "$file").tmp"
mv "$(basename "$file").tmp" "$(basename "$file")"
bye
EOF
}


WATCH_DIR="/data/incoming"
OUT_DIR="/data/processed"
STATE_FILE="/state/imgproc.last"

mkdir -p "$OUT_DIR"

echo "[+] Watching $WATCH_DIR"

last_cleanup_hour=""

inotifywait -m -e close_write,moved_to --format '%f' "$WATCH_DIR" |
while IFS= read -r FILE; do

    case "$FILE" in
      *.jpg|*.jpeg|*.png|*.webp|*.bmp|*.tif|*.tiff) ;;
      *) continue ;;
    esac

    IN="$WATCH_DIR/$FILE"
    OUT="$OUT_DIR/processed_$FILE"

    now=$(date +%s)
    last=0
    [[ -f "$STATE_FILE" ]] && last=$(cat "$STATE_FILE")

    if (( now - last < 3600 )); then
        echo "[~] Rate limit active — skipping $FILE"
        continue
    fi

    echo "[*] Processing $FILE"

    if convert ... "$OUT"
    then
        echo "[✓] Saved $OUT"

        if upload_ftpes "$OUT"; then
            echo "[✓] Uploaded to FTPES"
        else
            echo "[✗] FTPES upload failed" >&2
            continue
        fi

        echo "$now" > "$STATE_FILE"
    else
        echo "[✗] Failed processing"
    fi
    current_hour=$(date +%H)
    if [[ "$current_hour" != "$last_cleanup_hour" ]]; then
        find "$OUT_DIR" -type f -mmin +1440 -delete
        last_cleanup_hour="$current_hour"
        echo "[*] Cleanup done"
    fi

done
