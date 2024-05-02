from dataclasses import dataclass

from ..entries import ContentType


@dataclass
class CreatePublicationData:
    url: str
    type: ContentType


@dataclass
class PublicationData:
    id: int
    url: str
    type: ContentType
    believed_count: int
    disbelieved_count: int
    created_at: str
