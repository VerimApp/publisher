from datetime import datetime
from enum import Enum

from pydantic.dataclasses import dataclass
from pydantic import HttpUrl


class ContentType(str, Enum):
    YOUTUBE = "YOUTUBE"
    VK = "VK"
    TIKTOK = "TIKTOK"
    TWITCH = "TWITCH"


@dataclass
class CreatePublicationSchema:
    url: HttpUrl


@dataclass
class PublicationSchema:
    id: int
    url: str
    type: ContentType
    believed_count: int
    disbelieved_count: int
    created_at: datetime
    believed: bool | None
