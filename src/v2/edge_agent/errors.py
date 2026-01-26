from src.v2.common.errors.base import AppError


class EdgeAgentError(AppError):
    code = "edgeagent_error"


class MissingModuleError(AppError):
    code = "missing_module_error"

