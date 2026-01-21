from src.v2.common.errors.base import AppError


class InfrastructureError(AppError):
    code = "infrastructure_error"


class SecurityError(InfrastructureError):
    code = "farm_already_exists"


