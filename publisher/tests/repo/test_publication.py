from config.di import get_di_test_container
from models.publication import Publication
from models.vote import Vote
from services.repo import IPublicationRepo
from services.publications.entries import CreatePublicationData, ContentType
from schemas import PublicationSchema
from utils.test import RepoTestMixin


container = get_di_test_container()


class TestPublicationRepo(RepoTestMixin):
    repo: IPublicationRepo = container.publication_repo()

    def setup_method(self):
        self.entry = CreatePublicationData(
            url="https://example.com", type=ContentType.YOUTUBE
        )
        self.user_id = 1

        self.publication = self._create()

    def _create(self) -> Publication:
        return self.repo.create(self.user_id, self.entry)

    def test_create(self):
        assert isinstance(self.publication, Publication)
        assert self.publication.user_id == self.user_id
        assert self.publication.url == self.entry.url
        assert self.publication.type == self.entry.type

    def test_selection_no_vote(self):
        selection = self.repo.selection(self.user_id, size=100, page=1)
        for publication in selection.items:
            assert isinstance(publication, PublicationSchema)

        publication = list(
            filter(lambda item: item.id == self.publication.id, selection.items)
        )[0]
        assert publication.id == self.publication.id
        assert publication.url == self.publication.url
        assert publication.type == self.publication.type
        assert publication.believed_count == self.publication.believed_count
        assert publication.disbelieved_count == self.publication.disbelieved_count
        assert publication.created_at == self.publication.created_at
        assert publication.believed is None

    def test_selection_no_vote_no_user(self):
        selection = self.repo.selection(None, size=100, page=1)
        for publication in selection.items:
            assert isinstance(publication, PublicationSchema)

        publication = list(
            filter(lambda item: item.id == self.publication.id, selection.items)
        )[0]
        assert publication.id == self.publication.id
        assert publication.url == self.publication.url
        assert publication.type == self.publication.type
        assert publication.believed_count == self.publication.believed_count
        assert publication.disbelieved_count == self.publication.disbelieved_count
        assert publication.created_at == self.publication.created_at
        assert publication.believed is None

    def test_selection_believed(self):
        with container.db().session() as session:
            vote = Vote(
                user_id=self.user_id, publication_id=self.publication.id, believed=True
            )
            session.add(vote)
            session.commit()
            session.refresh(vote)

        # voted user
        selection = self.repo.selection(self.user_id, size=100, page=1)
        for publication in selection.items:
            assert isinstance(publication, PublicationSchema)

        publication = list(
            filter(lambda item: item.id == self.publication.id, selection.items)
        )[0]
        assert publication.id == self.publication.id
        assert publication.url == self.publication.url
        assert publication.type == self.publication.type
        assert publication.believed_count == self.publication.believed_count
        assert publication.disbelieved_count == self.publication.disbelieved_count
        assert publication.created_at == self.publication.created_at
        assert publication.believed

        # other user
        selection = self.repo.selection(self.user_id + 1, size=100, page=1)
        for publication in selection.items:
            assert isinstance(publication, PublicationSchema)

        publication = list(
            filter(lambda item: item.id == self.publication.id, selection.items)
        )[0]
        assert publication.id == self.publication.id
        assert publication.url == self.publication.url
        assert publication.type == self.publication.type
        assert publication.believed_count == self.publication.believed_count
        assert publication.disbelieved_count == self.publication.disbelieved_count
        assert publication.created_at == self.publication.created_at
        assert publication.believed is None

        with container.db().session() as session:
            session.delete(vote)

    def test_selection_believed_no_user(self):
        with container.db().session() as session:
            vote = Vote(
                user_id=self.user_id, publication_id=self.publication.id, believed=True
            )
            session.add(vote)
            session.commit()
            session.refresh(vote)

        selection = self.repo.selection(None, size=100, page=1)
        for publication in selection.items:
            assert isinstance(publication, PublicationSchema)

        publication = list(
            filter(lambda item: item.id == self.publication.id, selection.items)
        )[0]
        assert publication.id == self.publication.id
        assert publication.url == self.publication.url
        assert publication.type == self.publication.type
        assert publication.believed_count == self.publication.believed_count
        assert publication.disbelieved_count == self.publication.disbelieved_count
        assert publication.created_at == self.publication.created_at
        assert publication.believed is None

        with container.db().session() as session:
            session.delete(vote)

    def test_selection_disbelieved(self):
        with container.db().session() as session:
            vote = Vote(
                user_id=self.user_id, publication_id=self.publication.id, believed=False
            )
            session.add(vote)
            session.commit()
            session.refresh(vote)

        # voted user
        selection = self.repo.selection(self.user_id, size=100, page=1)
        for publication in selection.items:
            assert isinstance(publication, PublicationSchema)

        publication = list(
            filter(lambda item: item.id == self.publication.id, selection.items)
        )[0]
        assert publication.id == self.publication.id
        assert publication.url == self.publication.url
        assert publication.type == self.publication.type
        assert publication.believed_count == self.publication.believed_count
        assert publication.disbelieved_count == self.publication.disbelieved_count
        assert publication.created_at == self.publication.created_at
        assert not publication.believed

        # other user
        selection = self.repo.selection(self.user_id + 1, size=100, page=1)
        for publication in selection.items:
            assert isinstance(publication, PublicationSchema)

        publication = list(
            filter(lambda item: item.id == self.publication.id, selection.items)
        )[0]
        assert publication.id == self.publication.id
        assert publication.url == self.publication.url
        assert publication.type == self.publication.type
        assert publication.believed_count == self.publication.believed_count
        assert publication.disbelieved_count == self.publication.disbelieved_count
        assert publication.created_at == self.publication.created_at
        assert publication.believed is None

        with container.db().session() as session:
            session.delete(vote)

    def test_selection_disbelieved_no_user(self):
        with container.db().session() as session:
            vote = Vote(
                user_id=self.user_id, publication_id=self.publication.id, believed=False
            )
            session.add(vote)
            session.commit()
            session.refresh(vote)

        selection = self.repo.selection(None, size=100, page=1)
        for publication in selection.items:
            assert isinstance(publication, PublicationSchema)

        publication = list(
            filter(lambda item: item.id == self.publication.id, selection.items)
        )[0]
        assert publication.id == self.publication.id
        assert publication.url == self.publication.url
        assert publication.type == self.publication.type
        assert publication.believed_count == self.publication.believed_count
        assert publication.disbelieved_count == self.publication.disbelieved_count
        assert publication.created_at == self.publication.created_at
        assert publication.believed is None

        with container.db().session() as session:
            session.delete(vote)

    def test_get_by_id(self):
        publication = self.repo.get_by_id(self.publication.id)

        assert isinstance(publication, Publication)
        assert publication.id == self.publication.id

    def test_get_by_id_not_found(self):
        assert self.repo.get_by_id(self.publication.id + 1) is None
