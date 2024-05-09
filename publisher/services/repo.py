from abc import abstractmethod

from sqlalchemy.orm import Query

from models.publication import Publication
from utils.repo import IRepo
from utils.types import PublicationType, VoteType

from .publications.entries import CreatePublicationData


class IPublicationRepo(IRepo):
    @abstractmethod
    async def create(self, user_id: int, entry: CreatePublicationData) -> PublicationType: ...

    @abstractmethod
    async def selection(
        self, user_id: int | None, size: int | None, page: int | None
    ) -> Query[Publication]: ...

    @abstractmethod
    async def get_by_id(self, publication_id: int) -> Publication | None: ...


class IVoteRepo(IRepo):
    @abstractmethod
    async def get(self, user_id: int, publication_id: int) -> VoteType | None: ...

    @abstractmethod
    async def create(
        self, user_id: int, publication_id: int, believed: bool | None
    ) -> VoteType: ...

    @abstractmethod
    async def update(self, vote_id: int, believed: bool | None) -> None: ...
