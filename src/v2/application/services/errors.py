from src.v2.common.errors.base import AppError


class ServiceError(AppError):
    code = "service_error"
class TopicDuplicationError(ServiceError):
    code = "topic_duplication_error"
