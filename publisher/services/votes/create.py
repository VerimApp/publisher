from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from config.i18n import _
from schemas import VoteSchema
from services.repo import IVoteRepo, IPublicationRepo
from utils.types import VoteType
from utils.shortcuts import get_object_or_404


class IVote(ABC):
    @abstractmethod
    async def __call__(
        self,
        session: AsyncSession,
        user_id: int,
        publication_id: int,
        schema: VoteSchema,
    ) -> None: ...


class Vote(IVote):
    def __init__(self, repo: IVoteRepo, publication_repo: IPublicationRepo) -> None:
        self.repo = repo
        self.publication_repo = publication_repo

    async def __call__(
        self,
        session: AsyncSession,
        user_id: int,
        publication_id: int,
        schema: VoteSchema,
    ) -> None:
        await self._validate_publication_id(session, publication_id)
        vote = await self._get(session, user_id, publication_id)
        if vote:
            await self._update(session, vote, schema)
        else:
            await self._create(session, user_id, publication_id, schema)

    async def _validate_publication_id(
        self, session: AsyncSession, publication_id: int
    ) -> None:
        get_object_or_404(
            await self.publication_repo.get_by_id(session, publication_id),
            msg=_("Publication not found."),
        )

    async def _get(
        self, session: AsyncSession, user_id: int, publication_id: int
    ) -> VoteType | None:
        return await self.repo.get(session, user_id, publication_id)

    async def _create(
        self,
        session: AsyncSession,
        user_id: int,
        publication_id: int,
        schema: VoteSchema,
    ) -> VoteType:
        return await self.repo.create(session, user_id, publication_id, schema.believed)

    async def _update(
        self, session: AsyncSession, vote: VoteType, schema: VoteSchema
    ) -> None:
        await self.repo.update(session, vote.id, schema.believed)
