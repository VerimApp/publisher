from unittest import mock

from services.validators import Validate
from services.validators.base import ValidationMode
from utils.test import ServiceTestMixin


class TestValidate(ServiceTestMixin):
    def setup_method(self):
        self.data = None

        self.validator1 = mock.Mock()
        self.validator1.is_valid.return_value = True

        self.validator2 = mock.Mock()
        self.validator2.is_valid.return_value = True

        self.validate = Validate(self.validator1, self.validator2)

    def test_and_mode_both_valid(self):
        assert self.validate(self.data, mode=ValidationMode.AND, raise_exception=False)
        self.validator1.is_valid.assert_called_once_with(self.data, False)
        self.validator2.is_valid.assert_called_once_with(self.data, False)

    def test_and_mode_first_valid(self):
        self.validator2.is_valid.return_value = False
        assert not self.validate(
            self.data, mode=ValidationMode.AND, raise_exception=False
        )
        self.validator1.is_valid.assert_called_once_with(self.data, False)
        self.validator2.is_valid.assert_called_once_with(self.data, False)

    def test_and_mode_second_valid(self):
        self.validator1.is_valid.return_value = False
        assert not self.validate(
            self.data, mode=ValidationMode.AND, raise_exception=False
        )
        self.validator1.is_valid.assert_called_once_with(self.data, False)
        self.validator2.is_valid.assert_not_called()

    def test_and_mode_both_not_valid(self):
        self.validator1.is_valid.return_value = False
        self.validator2.is_valid.return_value = False
        assert not self.validate(
            self.data, mode=ValidationMode.AND, raise_exception=False
        )
        self.validator1.is_valid.assert_called_once_with(self.data, False)
        self.validator2.is_valid.assert_not_called()

    def test_or_mode_both_valid(self):
        assert self.validate(self.data, mode=ValidationMode.OR, raise_exception=True)
        self.validator1.is_valid.assert_called_once_with(self.data, True)
        self.validator2.is_valid.assert_not_called()

    def test_or_mode_first_valid(self):
        self.validator2.is_valid.return_value = False
        assert self.validate(self.data, mode=ValidationMode.OR, raise_exception=True)
        self.validator1.is_valid.assert_called_once_with(self.data, True)
        self.validator2.is_valid.assert_not_called()

    def test_or_mode_second_valid(self):
        self.validator1.is_valid.return_value = False
        assert self.validate(self.data, mode=ValidationMode.OR, raise_exception=True)
        self.validator1.is_valid.assert_called_once_with(self.data, True)
        self.validator2.is_valid.assert_called_once_with(self.data, True)

    def test_or_mode_both_not_valid(self):
        self.validator1.is_valid.return_value = False
        self.validator2.is_valid.return_value = False
        assert not self.validate(
            self.data, mode=ValidationMode.OR, raise_exception=True
        )
        self.validator1.is_valid.assert_called_once_with(self.data, True)
        self.validator2.is_valid.assert_called_once_with(self.data, True)
