"""Tasks for update dictionaries.

Last change: Luferov
Time: 2022-03-02
"""

from celery import shared_task

from ..models import District, Organization, Region
from ..services import get_content, parse_organizations, update_entity
from ..settings import dictionaries_settings


@shared_task
def update_organizations() -> str:
    """Task for updated District, Regions and Organizations to actual version."""
    try:
        content: str = get_content(dictionaries_settings.ORGANIZATIONS_LINK)
    except Exception as ex:
        return str(ex)
    districts, regions, organizations = parse_organizations(content)
    update_entity(District, districts)
    update_entity(Region, regions)
    update_entity(Organization, organizations)
    return f'Districts: {len(districts)}, Regions: {len(regions)}, Organizations: {len(organizations)}'
