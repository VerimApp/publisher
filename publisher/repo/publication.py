from dataclasses import asdict

from sqlalchemy import and_
from sqlalchemy.orm import Query
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.default import Params

from config import settings
from models.publication import Publication
from models.vote import Vote
from services.repo import IPublicationRepo
from schemas.publication import PublicationSchema
from services.publications.entries import CreatePublicationData
from utils.repo import pagination_transformer
from utils.types import PublicationType
from utils.decorators import handle_orm_error


class PublicationRepo(IPublicationRepo):
    model = Publication

    @handle_orm_error
    def create(self, user_id: int, entry: CreatePublicationData) -> PublicationType:
        entry.type = entry.type.value
        publication = self.model(user_id=user_id, **asdict(entry))
        with self.session_factory() as session:
            session.add(publication)
            session.commit()
            session.refresh(publication)
        return publication

    @handle_orm_error
    def selection(
        self, user_id: int | None, size: int | None, page: int | None
    ) -> Query[Publication]:
        size = size or settings.PAGINATION_DEFAULT_PAGE_SIZE
        page = page or settings.PAGINATION_DEFAULT_PAGE
        with self.session_factory() as session:
            return paginate(
                session.query(
                    self.model.id,
                    self.model.url,
                    self.model.type,
                    self.model.believed_count,
                    self.model.disbelieved_count,
                    self.model.created_at,
                    Vote.believed,
                )
                .outerjoin(
                    Vote,
                    and_(Vote.publication_id == self.model.id, Vote.user_id == user_id),
                )
                .add_columns(Vote.believed)
                .order_by(Vote.believed.desc()),
                params=Params(page=page, size=size),
                transformer=pagination_transformer(PublicationSchema),
            )

    @handle_orm_error
    def get_by_id(self, publication_id: int) -> Publication | None:
        with self.session_factory() as session:
            return (
                session.query(self.model)
                .filter(self.model.id == publication_id)
                .first()
            )
