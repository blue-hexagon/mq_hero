class AppError(Exception):
    """
    Root exception for all known, intentional failures.
    """
    code: str = "app_error"
    http_status: int | None = None
    retryable: bool = False

    def __init__(self, message: str, *, cause: Exception | None = None):
        super().__init__(message)
        self.cause = cause
