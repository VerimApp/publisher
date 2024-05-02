from pydantic.dataclasses import dataclass


@dataclass
class VoteSchema:
    believed: bool | None
