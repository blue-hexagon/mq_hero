class FarmAlreadyExistsWithId(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class DeviceAlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class CompanyAlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)
