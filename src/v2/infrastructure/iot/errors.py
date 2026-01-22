from src.v2.infrastructure.errors import InfrastructureError


class IotError(InfrastructureError):
    code = "iot_error"


class SensorReadError(IotError):
    code = "sensor_error"
