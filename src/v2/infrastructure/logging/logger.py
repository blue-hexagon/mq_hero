import logging
import sys
from threading import Lock
from typing import Optional

_lock = Lock()
_configured = False


# -------------------------
# Context injection
# -------------------------

class ContextFilter(logging.Filter):
    """
    Injects contextual fields into every log record.
    Missing fields are filled with 'NA'.
    """

    DEFAULTS = {
        "tenant": "NA",
        "farm": "NA",
        "device": "NA",
        "device_class": "NA",
        "message_class": "NA",
        "direction": "NA",
        "client_id": "NA",
    }

    def filter(self, record: logging.LogRecord) -> bool:
        for key, default in self.DEFAULTS.items():
            if not hasattr(record, key):
                setattr(record, key, default)
        return True


# -------------------------
# Formatter with truncated logger name
# -------------------------

class TruncatingFormatter(logging.Formatter):
    """
    Formatter that exposes `shortname`:
    last N segments of the logger name.
    """

    def __init__(self, *args, max_parts: int = 2, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_parts = max_parts

    def format(self, record: logging.LogRecord) -> str:
        parts = record.name.split(".")
        record.shortname = ".".join(parts[-self.max_parts:])
        return super().format(record)


# -------------------------
# Singleton setup
# -------------------------

def setup_logging(
        *,
        level: int = logging.INFO,
        app_name: str = "iot-hero",  # noqa
        enable_debug_modules: Optional[list[str]] = None,
) -> None:
    """
    Global, idempotent logging configuration.
    Safe to call multiple times.
    """
    global _configured

    if _configured:
        return

    with _lock:
        if _configured:
            return

        root = logging.getLogger()
        root.setLevel(level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        formatter = TruncatingFormatter(
            fmt=(
                "%(asctime)s | %(levelname)-4s | %(shortname)s | "
                "tenant=%(tenant)s farm=%(farm)s device=%(device)s "
                "d_class=%(device_class)s m_class=%(message_class)s "
                "dir=%(direction)s | %(message)s"
            ),
            datefmt="%H:%M:%S",
            max_parts=2,
        )

        handler.setFormatter(formatter)
        handler.addFilter(ContextFilter())

        root.handlers.clear()
        root.addHandler(handler)

        # Optional per-module debug enabling
        if enable_debug_modules:
            for module in enable_debug_modules:
                logging.getLogger(module).setLevel(logging.DEBUG)

        _configured = True
