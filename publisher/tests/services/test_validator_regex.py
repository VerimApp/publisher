from unittest import mock

import pytest
from pytest_mock import MockerFixture

from services.validators.regex import RegexValidator
from utils.test import ServiceTestMixin
from utils.exceptions import Custom400Exception


class TestRegexValidator(ServiceTestMixin):
    def setup_method(self):
        self.pattern = r"pattern"
        self.data = None

        self.validator = RegexValidator(pattern=self.pattern)

    def test_valid(self, mocker: MockerFixture):
        re = mocker.patch("services.validators.regex.re")
        re.match.return_value = True

        assert self.validator.is_valid(self.data, raise_exception=False)
        re.match.assert_called_once_with(self.pattern, self.data)

    def test_valid_raise_exc(self, mocker: MockerFixture):
        re = mocker.patch("services.validators.regex.re")
        re.match.return_value = True

        assert self.validator.is_valid(self.data, raise_exception=True)
        re.match.assert_called_once_with(self.pattern, self.data)

    def test_not_valid(self, mocker: MockerFixture):
        re = mocker.patch("services.validators.regex.re")
        re.match.return_value = None

        assert not self.validator.is_valid(self.data, raise_exception=False)
        re.match.assert_called_once_with(self.pattern, self.data)

    def test_not_valid_raise_exc(self, mocker: MockerFixture):
        re = mocker.patch("services.validators.regex.re")
        re.match.return_value = None

        with pytest.raises(Custom400Exception):
            self.validator.is_valid(self.data, raise_exception=True)
            re.match.assert_called_once_with(self.pattern, self.data)
