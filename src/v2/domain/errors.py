from src.v2.common.errors.base import AppError


class DomainError(AppError):
    code = "domain_error"


class FarmAlreadyExistsWithId(DomainError):
    code = "farm_already_exists"


class DeviceAlreadyExists(DomainError):
    code = "device_already_exists"


class TenantAlreadyExists(DomainError):
    code = "tenant_already_exists"

class LocationAlreadyExists(DomainError):
    code = "location_already_exists"

class LocationDontExists(DomainError):
    code = "location_dont_exists"
