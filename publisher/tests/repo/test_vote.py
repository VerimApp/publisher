from config.di import get_di_test_container
from models.publication import Publication
from models.vote import Vote
from services.repo import IVoteRepo
from services.publications.entries import CreatePublicationData, ContentType
from schemas import PublicationSchema
from utils.test import RepoTestMixin


container = get_di_test_container()


class TestVoteRepo(RepoTestMixin):
    repo: IVoteRepo = container._vote_repo()

    def setup_method(self):
        self.entry = CreatePublicationData(
            url="https://example.com", type=ContentType.YOUTUBE
        )
        self.user_id = 1

        self.publication = self._create_publication()
        self.vote = self._create()

    def _create(self, believed: bool | None = None):
        return self.repo.create(
            user_id=self.user_id, publication_id=self.publication.id, believed=believed
        )

    def _create_publication(self):
        return container.publication_repo().create(
            user_id=self.user_id, entry=self.entry
        )

    def test_get(self):
        vote = self.repo.get(self.user_id, self.publication.id)

        assert isinstance(vote, Vote)
        assert vote.id == self.vote.id

    def test_get_not_found(self):
        assert self.repo.get(self.user_id + 1, self.publication.id) is None

    def test_create(self):
        vote = self._create()

        assert isinstance(vote, Vote)
        assert vote.user_id == self.user_id
        assert vote.publication_id == self.publication.id
        assert vote.believed is None

        vote = self._create(believed=True)

        assert isinstance(vote, Vote)
        assert vote.user_id == self.user_id
        assert vote.publication_id == self.publication.id
        assert vote.believed

        vote = self._create(believed=False)

        assert isinstance(vote, Vote)
        assert vote.user_id == self.user_id
        assert vote.publication_id == self.publication.id
        assert not vote.believed

    def test_update(self):
        vote = self._create()

        assert vote.believed is None

        self.repo.update(vote.id, believed=True)
        with container.db().session() as session:
            vote = session.query(Vote).filter(Vote.id == vote.id).first()
            assert vote.believed

        self.repo.update(vote.id, believed=False)
        with container.db().session() as session:
            vote = session.query(Vote).filter(Vote.id == vote.id).first()
            assert not vote.believed
