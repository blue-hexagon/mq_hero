from src.v2.domain.entities.company import Company
from src.v2.domain.entities.message_contract import MessageClass, MessageContract, MqttDirection
from src.v2.domain.topics.topic_builder import TopicBuilder
from src.v2.domain.topics.topic_scope import TopicScope


class TopicGenerationService:
    @staticmethod
    def generate_topics(company_lst: list[Company]) -> list[str]:
        topics = []

        for company in company_lst:
            for farm in company.farms:
                for device in farm.devices.values():
                    for msg_type in MessageClass:
                        contract = MessageContract(
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
    # MARKER;:
    # def make_subscriptions(self):
    #     TopicBuilder() \
    #         .add(TopicScope.SINGLE, company) \
    #         .add(TopicScope.ALL, farm) \
    #         .add(TopicScope.ALL, device_class) \
    #         .add(TopicScope.ALL, device) \
    #         .add(TopicScope.ALL_RECURSIVE, contract) \
    #         .build()
