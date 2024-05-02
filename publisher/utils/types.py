from typing import ClassVar, Dict, Protocol
from datetime import datetime

from services.entries import ContentType


class Dataclass(Protocol):
    __dataclass_fields__: ClassVar[Dict]


class PublicationType:
    id: int
    user_id: int
    url: str
    type: ContentType
    believed_count: int
    disbelieved_count: int
    created_at: datetime
    updated_at: datetime


class VoteType:
    id: int
    publication_id: int
    user_id: int
    believed: bool | None
