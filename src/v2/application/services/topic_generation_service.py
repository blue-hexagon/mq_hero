from src.v2.domain.entities.tenant import Tenant
from src.v2.domain.entities.mqtt_message_contract import MessageClass
from src.v2.domain.topics.topic_builder import TopicBuilder
from src.v2.domain.topics.topic_scope import TopicScope
from src.v2.infrastructure.mqtt.message_contract import MqttMessageContract
from src.v2.infrastructure.mqtt.types import MqttDirection


class TopicGenerationService:
    @staticmethod
    def generate_topics(company_lst: list[Tenant]) -> list[str]:
        topics = []

        for company in company_lst:
            for farm in company.farms:
                for device in farm.devices.values():
                    for msg_type in MessageClass:
                        contract = MqttMessageContract(
                            msg_type=msg_type,  # noqa: IDE quirk (not a str)
                            direction=MqttDirection.PUB,
                        )

                        topic = (
                            TopicBuilder()
                            .add(TopicScope.SINGLE, company)
                            .add(TopicScope.SINGLE, farm)
                            .add(TopicScope.SINGLE, device.device_class)  # see note below
                            .add(TopicScope.SINGLE, device)
                            .add(TopicScope.SINGLE, contract)
                            .build()
                        )

                        topics.append(topic)

        return topics

