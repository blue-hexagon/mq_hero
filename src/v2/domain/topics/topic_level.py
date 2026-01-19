from enum import Enum


class TopicLevel(Enum):
    MSP = "msp_id"
    COMPANY = "company_id"
    FARM = "farm_id"
    DEVICE_CLASS = "device_class"
    DEVICE = "device_id"
    MESSAGE_TYPE = "message_type"
