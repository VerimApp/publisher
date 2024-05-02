from abc import ABC, abstractmethod

from config.i18n import _
from schemas import VoteSchema
from services.repo import IVoteRepo, IPublicationRepo
from utils.types import VoteType
from utils.shortcuts import get_object_or_404


class IVote(ABC):
    @abstractmethod
    def __call__(
        self, user_id: int, publication_id: int, schema: VoteSchema
    ) -> None: ...


class Vote(IVote):
    def __init__(self, repo: IVoteRepo, publication_repo: IPublicationRepo) -> None:
        self.repo = repo
        self.publication_repo = publication_repo

    def __call__(self, user_id: int, publication_id: int, schema: VoteSchema) -> None:
        self._validate_publication_id(publication_id)
        vote = self._get(user_id, publication_id)
        if vote:
            self._update(vote, schema)
        else:
            self._create(user_id, publication_id, schema)

    def _validate_publication_id(self, publication_id: int) -> None:
        get_object_or_404(
            self.publication_repo.get_by_id(publication_id),
            msg=_("Publication not found."),
        )

    def _get(self, user_id: int, publication_id: int) -> VoteType | None:
        return self.repo.get(user_id, publication_id)

    def _create(
        self, user_id: int, publication_id: int, schema: VoteSchema
    ) -> VoteType:
        return self.repo.create(user_id, publication_id, schema.believed)

    def _update(self, vote: VoteType, schema: VoteSchema) -> None:
        self.repo.update(vote.id, schema.believed)
