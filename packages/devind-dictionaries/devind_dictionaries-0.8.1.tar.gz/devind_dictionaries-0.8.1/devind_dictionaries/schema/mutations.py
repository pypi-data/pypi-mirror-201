"""Dictionaries mutations.

Last change: Luferov
Time 2022-03-02
"""

from typing import Any

from devind_helpers.decorators import permission_classes
from devind_helpers.schema import BaseMutation
from graphql import ResolveInfo

from ..permissions import ChangeDistrict, ChangeOrganization, ChangeRegion
from ..tasks import update_organizations


class UpdateOrganizations(BaseMutation):
    """For start celery task which updated districts, regions and organizations."""

    @staticmethod
    @permission_classes((ChangeDistrict, ChangeOrganization, ChangeRegion,))
    def mutate_and_get_payload(root: Any, info: ResolveInfo) -> 'UpdateOrganizations':
        """Start celery task."""
        update_organizations.delay()
        return UpdateOrganizations()
