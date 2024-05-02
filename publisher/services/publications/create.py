from abc import ABC, abstractmethod

from config.i18n import _
from schemas import CreatePublicationSchema
from utils.types import PublicationType
from utils.domains import get_content_type
from utils.exceptions import Custom400Exception

from ..repo import IPublicationRepo
from .entries import CreatePublicationData, PublicationData


class ICreatePublication(ABC):
    @abstractmethod
    def __call__(
        self, user_id: int, schema: CreatePublicationSchema
    ) -> PublicationData: ...


class CreatePublication(ICreatePublication):
    def __init__(self, repo: IPublicationRepo) -> None:
        self.repo = repo

    def __call__(
        self, user_id: int, schema: CreatePublicationSchema
    ) -> PublicationData:
        schema = self._clean(schema)
        schema = self._to_entry(schema)
        publication = self._create(user_id, schema)
        return self._to_schema(publication)

    def _clean(self, schema: CreatePublicationSchema) -> CreatePublicationSchema:
        schema.url = str(schema.url)
        return schema

    def _to_entry(self, schema: CreatePublicationSchema) -> CreatePublicationData:
        type = get_content_type(schema.url)
        if type is None:
            raise Custom400Exception(_("Platform is not supported."))
        return CreatePublicationData(url=schema.url, type=type)

    def _create(self, user_id: int, entry: CreatePublicationData) -> PublicationType:
        return self.repo.create(user_id, entry)

    def _to_schema(self, publication: PublicationType) -> PublicationData:
        return PublicationData(
            id=publication.id,
            url=publication.url,
            type=publication.type,
            believed_count=publication.believed_count,
            disbelieved_count=publication.disbelieved_count,
            created_at=str(publication.created_at),
        )
