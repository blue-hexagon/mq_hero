from datetime import datetime, timezone


class TimeStamp:
    @classmethod
    def get_utc_isof(cls) -> str:
        return datetime.now(timezone.utc).isoformat()
