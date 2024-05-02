from unittest import mock
from types import SimpleNamespace
from datetime import datetime

import pytest
from pytest_mock import MockerFixture

from config.di import get_di_test_container
from services.publications import CreatePublication
from services.entries import ContentType
from services.publications.entries import PublicationData, CreatePublicationData
from schemas import CreatePublicationSchema
from utils.test import ServiceTestMixin
from utils.exceptions import Custom400Exception


container = get_di_test_container()


class TestCreatePublication(ServiceTestMixin):
    def setup_method(self, method):
        self.publication = SimpleNamespace(
            **{
                "id": 1,
                "url": "https://example.com",
                "type": ContentType.YOUTUBE,
                "believed_count": 0,
                "disbelieved_count": 0,
                "created_at": datetime(1, 1, 1),
            }
        )
        self.schema = CreatePublicationSchema(url=self.publication.url)

        self.repo = mock.Mock()
        self.repo.create.return_value = self.publication

        self.context = container.create_publication.override(
            CreatePublication(repo=self.repo)
        )

    def test_create(self, mocker: MockerFixture):
        get_content_type = mocker.patch("services.publications.create.get_content_type")
        get_content_type.return_value = ContentType.YOUTUBE
        with self.context:
            publication = container.create_publication()(
                user_id=self.user.id, schema=self.schema
            )

            assert isinstance(publication, PublicationData)
            assert isinstance(self.schema.url, str)
            assert publication.id == self.publication.id
            assert publication.url == self.publication.url
            assert publication.type == self.publication.type
            assert publication.believed_count == self.publication.believed_count
            assert publication.disbelieved_count == self.publication.disbelieved_count
            assert publication.created_at == str(self.publication.created_at)
            get_content_type.assert_called_once_with(self.schema.url)
            self.repo.create.assert_called_once_with(
                self.user.id,
                CreatePublicationData(url=self.schema.url, type=ContentType.YOUTUBE),
            )

    def test_create_bad_content_type(self, mocker: MockerFixture):
        get_content_type = mocker.patch("services.publications.create.get_content_type")
        get_content_type.return_value = None
        with self.context, pytest.raises(Custom400Exception):
            container.create_publication()(user_id=self.user.id, schema=self.schema)

            get_content_type.assert_called_once_with(self.schema.url)
            self.repo.create.assert_not_called()
