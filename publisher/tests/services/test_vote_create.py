from unittest import mock
from types import SimpleNamespace

import pytest

from config.di import get_di_test_container
from services.votes import Vote
from schemas import VoteSchema
from utils.test import ServiceTestMixin
from utils.exceptions import Custom404Exception


container = get_di_test_container()


class TestVote(ServiceTestMixin):
    def setup_method(self):
        self.schema = VoteSchema(believed=True)

        self.vote = SimpleNamespace(**{"id": 1})
        self.publication = SimpleNamespace(**{"id": 1})

        self.repo = mock.Mock()
        self.repo.get.return_value = None

        self.publication_repo = mock.Mock()
        self.publication_repo.get_by_id.return_value = self.publication

        self.context = container.create_vote.override(
            Vote(repo=self.repo, publication_repo=self.publication_repo)
        )

    def test_create(self):
        with self.context:
            assert (
                container.create_vote()(self.user.id, self.publication.id, self.schema)
                is None
            )

            self.repo.create.assert_called_once_with(
                self.user.id, self.publication.id, self.schema.believed
            )
            self.repo.update.assert_not_called()

    def test_create_bad_publication_id(self):
        self.publication_repo.get_by_id.return_value = None
        with self.context, pytest.raises(Custom404Exception):
            container.create_vote()(self.user.id, self.publication.id, self.schema)

            self.repo.create.assert_not_called()
            self.repo.update.assert_not_called()

    def test_update(self):
        self.repo.get.return_value = self.vote
        with self.context:
            assert (
                container.create_vote()(self.user.id, self.publication.id, self.schema)
                is None
            )

            self.repo.create.assert_not_called()
            self.repo.update.assert_called_once_with(self.vote.id, self.schema.believed)

    def test_update_bad_publication_id(self):
        self.publication_repo.get_by_id.return_value = None
        with self.context, pytest.raises(Custom404Exception):
            container.create_vote()(self.user.id, self.publication.id, self.schema)

            self.repo.create.assert_not_called()
            self.repo.update.assert_not_called()
