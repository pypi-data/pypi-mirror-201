"""Testing settings."""

from django.test import TestCase

from ..settings import dictionaries_settings


class TestSettings(TestCase):
    """Testing settings."""

    def test_field_exists(self) -> None:
        """Testing exist url value."""
        self.assertIsNotNone(dictionaries_settings.ORGANIZATIONS_LINK)
        self.assertIsNotNone(dictionaries_settings.USER_TYPE)
