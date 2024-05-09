from sqlalchemy import select, update

from services.repo import IVoteRepo
from models.vote import Vote
from utils.types import VoteType
from utils.decorators import handle_orm_error


class VoteRepo(IVoteRepo):
    model = Vote

    @handle_orm_error
    async def get(self, user_id: int, publication_id: int) -> VoteType | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model).filter(
                    Vote.user_id == user_id, Vote.publication_id == publication_id
                )
            )
            return result.first()

    @handle_orm_error
    async def create(
        self, user_id: int, publication_id: int, believed: bool | None
    ) -> VoteType:
        vote = self.model(
            user_id=user_id, publication_id=publication_id, believed=believed
        )
        async with self.session_factory() as session:
            session.add(vote)
            await session.commit()
            await session.refresh(vote)
        return vote

    @handle_orm_error
    async def update(self, vote_id: int, believed: bool | None) -> None:
        async with self.session_factory() as session:
            await session.execute(
                update(self.model).filter(Vote.id == vote_id).values(believed=believed)
            )
            await session.commit()
