from dataclasses import dataclass, field
from typing import Optional, List

from src.v2.domain.entities.device_class import DeviceClass
from src.v2.domain.entities.location import Location
from src.v2.domain.topics.topic_segment import TopicSegment
from src.v2.infrastructure.mqtt.message_contract import MqttMessageContract
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.v2.domain.entities.farm import Farm


@dataclass
class Device:
    id: str
    device_class: DeviceClass
    interval: int
    location: Location
    driver: str  # This defines the sensor model it'll use later
    _farm: Farm
    messages: List[MqttMessageContract] = field(default_factory=list)

    def get_topic_segment(self) -> TopicSegment:
        return TopicSegment(kind="device", token=self.id)

    def _add_message(self, contract: MqttMessageContract):
        self.messages.append(contract)

    @property
    def farm(self) -> Farm:
        return self._farm
    def __str__(self) -> str:
        return (f"Device(id={self.id}, class={self.device_class.id}, model={self.driver}, location={self.location}, "
                f"topic_segment={self.get_topic_segment()})")
