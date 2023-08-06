"""Description schema for dictionaries.

Last change: Luferov
Time: 2022-03-2
"""

from typing import Any, Iterable

import graphene
from devind_helpers.orm_utils import get_object_or_404
from graphene_django import DjangoListField
from graphene_django_filter import AdvancedDjangoFilterConnectionField
from graphql import ResolveInfo

from .mutations import UpdateOrganizations
from .types import BudgetClassificationType, DepartmentType, DistrictType, OrganizationType, RegionType
from ..models import BudgetClassification, Department, District, Organization, Region


class Query(graphene.ObjectType):
    """List of queries for dictionaries."""

    budget_classifications = AdvancedDjangoFilterConnectionField(BudgetClassificationType)
    active_budget_classifications = AdvancedDjangoFilterConnectionField(
        BudgetClassificationType,
        filter_input_type_prefix='ActiveBudgetClassification'
    )

    department = graphene.Field(DepartmentType, department_id=graphene.Int(required=True, description='Department ID'))
    departments = DjangoListField(DepartmentType)

    district = graphene.Field(DistrictType, district_id=graphene.Int(required=True, description='District ID'))
    districts = DjangoListField(DistrictType)

    region = graphene.Field(RegionType, region_id=graphene.Int(required=True, description='Region ID'))
    regions = DjangoListField(RegionType)

    organization = graphene.Field(
        OrganizationType,
        organization_id=graphene.Int(required=True, description='Organization ID')
    )
    organizations = AdvancedDjangoFilterConnectionField(OrganizationType)

    @staticmethod
    def resolve_active_budget_classifications(
            root: Any,
            info: ResolveInfo,
            *args,
            **kwargs
    ) -> Iterable[BudgetClassification]:
        """Resolve active budget classification for now."""
        return BudgetClassification.objects.active_now()

    @staticmethod
    def resolve_department(root: Any, info: ResolveInfo, department_id: int) -> Department:
        """Resolve function for get department entity."""

    @staticmethod
    def resolve_district(root: Any, info: ResolveInfo, district_id: int) -> District:
        """Resolve function for get district entity."""
        return get_object_or_404(District, pk=district_id)

    @staticmethod
    def resolve_region(root: Any, info: ResolveInfo, region_id: int) -> Region:
        """Resolve function for get region entity."""
        return get_object_or_404(Region, pk=region_id)

    @staticmethod
    def resolve_organization(root: Any, info: ResolveInfo, organization_id: int) -> Organization:
        """Resolve function for get organizations entity."""
        return get_object_or_404(Organization, pk=organization_id)


class Mutation(graphene.ObjectType):
    """List of mutations for dictionaries."""

    update_organizations = UpdateOrganizations.Field(description='Update district, regions and organizations.')
