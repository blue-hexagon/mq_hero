FROM debian:stable-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        inotify-tools \
        imagemagick \
        lftp \
        ca-certificates \
        bash && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY watcher.sh shelldeps.sh ./
RUN chmod +x watcher.sh shelldeps.sh

RUN mkdir -p /state

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD pgrep -f inotifywait || exit 1

STOPSIGNAL SIGTERM

ENTRYPOINT ["/app/watcher.sh"]
