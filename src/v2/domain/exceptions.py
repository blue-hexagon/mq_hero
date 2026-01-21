class FarmAlreadyExistsWithId(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class DeviceAlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TenantAlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)
