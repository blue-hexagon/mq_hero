#!/usr/bin/env bash

WATCH_DIR="/srv/ftp/images/incoming"
OUT_DIR="/srv/ftp/images/processed"

mkdir -p "$OUT_DIR"

echo "[+] Watching $WATCH_DIR"

inotifywait -m -e close_write --format '%f' "$WATCH_DIR" | while read FILE
do
    IN="$WATCH_DIR/$FILE"
    OUT="$OUT_DIR/processed_$FILE"

    echo "[*] Processing $FILE"

    convert "$IN" \
        -resize 1920x1920\> \
        -contrast-stretch 0.5%x0.5% \
        -sharpen 0x0.7 \
        -modulate 100,110,100 \
        "$OUT"

    echo "[✓] Saved $OUT"
done
