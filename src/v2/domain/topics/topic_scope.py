from enum import Enum


class TopicScope(str,Enum):
    SINGLE = "single"
    ALL = "all"
    ALL_RECURSIVE = "recursive"
