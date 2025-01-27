from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from config.i18n import _
from schemas import CreatePublicationSchema
from utils.types import PublicationType
from utils.domains import get_content_type
from utils.exceptions import Custom400Exception

from ..repo import IPublicationRepo
from .entries import CreatePublicationData, PublicationData


class ICreatePublication(ABC):
    @abstractmethod
    async def __call__(
        self, session: AsyncSession, user_id: int, schema: CreatePublicationSchema
    ) -> PublicationData: ...


class CreatePublication(ICreatePublication):
    def __init__(self, repo: IPublicationRepo) -> None:
        self.repo = repo

    async def __call__(
        self, session: AsyncSession, user_id: int, schema: CreatePublicationSchema
    ) -> PublicationData:
        schema = self._clean(schema)
        schema = self._to_entry(schema)
        publication = await self._create(session, user_id, schema)
        return self._to_schema(publication)

    def _clean(self, schema: CreatePublicationSchema) -> CreatePublicationSchema:
        schema.url = str(schema.url)
        return schema

    def _to_entry(self, schema: CreatePublicationSchema) -> CreatePublicationData:
        type = get_content_type(schema.url)
        if type is None:
            raise Custom400Exception(_("Platform is not supported."))
        return CreatePublicationData(url=schema.url, type=type)

    async def _create(
        self, session: AsyncSession, user_id: int, entry: CreatePublicationData
    ) -> PublicationType:
        return await self.repo.create(session, user_id, entry)

    def _to_schema(self, publication: PublicationType) -> PublicationData:
        return PublicationData(
            id=publication.id,
            url=publication.url,
            type=publication.type,
            believed_count=publication.believed_count,
            disbelieved_count=publication.disbelieved_count,
            created_at=str(publication.created_at),
        )
