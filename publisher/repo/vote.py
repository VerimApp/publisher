from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.repo import IVoteRepo
from models.vote import Vote
from utils.types import VoteType
from utils.decorators import handle_orm_error, row_to_model


class VoteRepo(IVoteRepo):
    model = Vote

    @handle_orm_error
    @row_to_model()
    async def get(
        self, session: AsyncSession, user_id: int, publication_id: int
    ) -> VoteType | None:
        result = await session.execute(
            select(self.model).filter(
                Vote.user_id == user_id, Vote.publication_id == publication_id
            )
        )
        return result.first()

    @handle_orm_error
    async def create(
        self,
        session: AsyncSession,
        user_id: int,
        publication_id: int,
        believed: bool | None,
    ) -> VoteType:
        vote = self.model(
            user_id=user_id, publication_id=publication_id, believed=believed
        )
        session.add(vote)
        await session.flush([vote])
        await session.refresh(vote)
        return vote

    @handle_orm_error
    async def update(
        self, session: AsyncSession, vote_id: int, believed: bool | None
    ) -> None:
        await session.execute(
            update(self.model).filter(Vote.id == vote_id).values(believed=believed)
        )
