"""Test queries."""

from typing import Any

from django.test import TestCase
from example.schema import schema
from graphene.test import Client

from .test_services import get_test_organizations
from ..models import District, Organization, Region
from ..services import parse_organizations, update_entity


class TestQueries(TestCase):
    """Testing queries."""

    def setUp(self) -> None:
        """Set up data for testing."""
        content = get_test_organizations()
        districts, regions, organizations = parse_organizations(content)
        update_entity(District, districts)
        update_entity(Region, regions)
        update_entity(Organization, organizations)

        self.client: Client = Client(schema)

    def test_district(self) -> None:
        """Testing district query."""
        def query(district_id: int) -> Any:
            """Helpers for execute query."""
            return self.client.execute(
                """
                query ($districtId: Int!) {
                  district (districtId: $districtId) {
                    id
                    name
                    __typename
                  }
                }
                """,
                variables={'districtId': district_id}
            )
        find_district = query(1)
        self.assertIsNone(find_district.get('errors'))
        district = find_district['data']['district']
        self.assertEqual(district['__typename'], 'DistrictType')

    def test_districts(self) -> None:
        """Testing districts query."""
        districts_result = self.client.execute(
            """
            query {
              districts {
                id
                name
                __typename
              }
            }
            """
        )
        self.assertIsNone(districts_result.get('errors'))
        districts = districts_result['data']['districts']
        self.assertEqual(len(districts), District.objects.count())

    def tearDown(self) -> None:
        """Free seeder data."""
        Organization.objects.all().delete()
        Region.objects.all().delete()
        District.objects.all().delete()
