from enum import Enum


class TopicLevel(str, Enum):
    MSP = "msp_id"
    TENANT = "tenant_id"
    FARM = "farm_id"
    DEVICE_CLASS = "device_class"
    DEVICE = "device_id"
    MESSAGE_CLASS = "message_class"
