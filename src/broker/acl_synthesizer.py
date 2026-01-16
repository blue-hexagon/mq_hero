from src.business.company import Company
from src.business.farm import Farm
from src.data.device import Device


def generate_device_acl(company: Company, farm: Farm, device: Device) -> list[str]:
    root = device_topic(company, farm, device)

    if device.type == "sensor":
        return [
            f"topic write {root}/state/#",
            f"topic write {root}/events/#",
            f"topic write {root}/metrics/#",
            f"topic write {root}/logs/#",
        ]

    if device.type == "actuator":
        return [
            f"topic read  {root}/cmd/#",
            f"topic write {root}/state/#",
            f"topic write {root}/metrics/#",
            f"topic write {root}/logs/#",
        ]

    if device.type == "drone":
        return [
            f"topic read  {root}/cmd/#",
            f"topic write {root}/state/#",
            f"topic write {root}/events/#",
            f"topic write {root}/metrics/#",
            f"topic write {root}/logs/#",
        ]

    raise ValueError("Unknown device type")
