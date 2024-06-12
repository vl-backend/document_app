from enum import Enum, auto


class DocumentStatus(Enum):
    PUBLISHED = auto()
    ARCHIVED = auto()
    DRAFT = auto()
