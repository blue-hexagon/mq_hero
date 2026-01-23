import logging
import sys
from threading import Lock
from typing import Optional

# =====================================================
# Global state (idempotent setup)
# =====================================================

_lock = Lock()
_configured = False

# =====================================================
# Context configuration
# =====================================================

_LOG_CONTEXT_KEYS = (
    "tenant",
    "farm",
    "device",
    "device_class",
    "message_class",
    "direction",
    "client_id",
)

_LOG_CONTEXT_DEFAULT = "NA"


# =====================================================
# Formatter with truncated logger name + optional context
# =====================================================

class TruncatingFormatter(logging.Formatter):
    """
    Formatter that:
    - exposes `shortname` (last N parts of logger name)
    - safely injects context defaults
    - conditionally renders context (no empty pipes)
    """

    def __init__(
            self,
            *args,
            max_parts: int = 2,
            show_empty_context: bool = False,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.max_parts = max_parts
        self.show_empty_context = show_empty_context

    def format(self, record: logging.LogRecord) -> str:
        # -------------------------------------------------
        # Ensure context keys always exist (formatter-safe)
        # -------------------------------------------------
        for key in _LOG_CONTEXT_KEYS:
            if not hasattr(record, key):
                setattr(record, key, _LOG_CONTEXT_DEFAULT)

        # -------------------------------------------------
        # Short logger name
        # -------------------------------------------------
        parts = record.name.split(".")
        record.shortname = ".".join(parts[-self.max_parts:])

        # -------------------------------------------------
        # Build conditional context block
        # -------------------------------------------------
        context_items = [
            f"{key}={getattr(record, key)}"
            for key in _LOG_CONTEXT_KEYS
            if getattr(record, key) != _LOG_CONTEXT_DEFAULT
        ]

        if context_items:
            record.context_block = " | " + " ".join(context_items)
        elif self.show_empty_context:
            record.context_block = " | context=NA"
        else:
            record.context_block = ""

        return super().format(record)


# =====================================================
# Logging setup (composition root)
# =====================================================

def setup_logging(
        *,
        level: int = logging.INFO,
        enable_debug_modules: Optional[list[str]] = None,
        show_empty_context: bool = False,
) -> None:
    """
    Global, idempotent logging configuration.

    Guarantees:
    - Safe to call multiple times
    - Per-module debug actually works
    - Context is optional and noise-free
    - Formatter never crashes on missing fields
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

        # -------------------------------------------------
        # Handler level MUST allow DEBUG if any module needs it
        # -------------------------------------------------
        effective_handler_level = level
        if enable_debug_modules:
            effective_handler_level = logging.DEBUG

        handler.setLevel(effective_handler_level)

        formatter = TruncatingFormatter(
            fmt=(
                "%(asctime)s | %(levelname)-4s | %(shortname)s"
                "%(context_block)s | %(message)s"
            ),
            datefmt="%H:%M:%S",
            max_parts=2,
            show_empty_context=show_empty_context,
        )

        handler.setFormatter(formatter)

        root.handlers.clear()
        root.addHandler(handler)

        # -------------------------------------------------
        # Enable DEBUG on specific module namespaces
        # -------------------------------------------------
        if enable_debug_modules:
            for module in enable_debug_modules:
                logging.getLogger(module).setLevel(logging.DEBUG)

        _configured = True

# =====================================================
# Example usage
# =====================================================
# setup_logging(
#     level=logging.INFO,
#     enable_debug_modules=[
#         "src.v2.application.runtime.context",
#         "src.v2.infrastructure.mqtt",
#     ],
# )
#
# log = logging.getLogger(__name__)
# log.debug("ROOT_ENV_KEY=%s", "ROLE")
# log.info("System initialized", extra={"tenant": "t1", "farm": "f1"})
