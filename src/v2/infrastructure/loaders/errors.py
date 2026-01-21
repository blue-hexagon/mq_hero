class ConfigError(Exception):
    """Base class for all configuration errors."""


class SchemaValidationError(ConfigError):
    pass


class ReferenceValidationError(ConfigError):
    pass


class DomainConstructionError(ConfigError):
    pass
