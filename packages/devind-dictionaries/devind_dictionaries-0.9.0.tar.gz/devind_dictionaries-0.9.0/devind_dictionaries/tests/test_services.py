"""Test services."""

from dataclasses import dataclass
from functools import lru_cache
from os.path import join
from typing import Callable, Optional
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from ..models import District, Organization, Region
from ..services import get_content, parse_organizations, update_entity
from ..settings import dictionaries_settings


@lru_cache
def get_test_organizations() -> str:
    """Get testing organizations."""
    data_file: str = join(settings.BASE_DIR, 'devind_dictionaries', 'tests', 'data', 'organizations.xml')
    with open(data_file, encoding='utf8') as file:
        content: str = file.read()
    return content


@dataclass
class MockRequestResponse:
    """Mock response instead of request.get."""

    status_code: int
    text: Optional[str] = None
    encoding: str = 'urf-8'


def mock_request_get(url: str, *args, **kwargs) -> MockRequestResponse:
    """Mock request get."""
    if url == dictionaries_settings.ORGANIZATIONS_LINK:
        return MockRequestResponse(status_code=200, text=get_test_organizations())
    return MockRequestResponse(status_code=500)


class TestServices(TestCase):
    """Testing services."""

    def setUp(self) -> None:
        """Set up response."""
        self.content = get_test_organizations()

    @patch('requests.get', side_effect=mock_request_get)
    def test_get_content(self, mock_get: Callable[[str], str]) -> None:
        """Testing available content organizations."""
        self.assertEqual(get_content(dictionaries_settings.ORGANIZATIONS_LINK), self.content)
        with self.assertRaises(Exception):
            get_content('https://devind.ru')

    def test_parse_organization(self) -> None:
        """Testing parse organizations."""
        districts, regions, organizations = parse_organizations(self.content)
        update_entity(District, districts)
        update_entity(Region, regions)
        update_entity(Organization, organizations)
        self.assertEqual(len(districts), District.objects.count())
        self.assertEqual(len(regions), Region.objects.count())
        self.assertEqual(len(organizations), Organization.objects.count())

    def tearDown(self) -> None:
        """Free seeder data."""
        Organization.objects.all().delete()
        Region.objects.all().delete()
        District.objects.all().delete()
