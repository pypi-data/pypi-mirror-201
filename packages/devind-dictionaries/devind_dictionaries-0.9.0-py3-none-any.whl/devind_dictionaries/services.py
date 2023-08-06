"""Services which uses in dictionaries.

Last change: Luferov
Time: 2022-03-2
"""

import xml.etree.ElementTree as ETree
from collections import defaultdict
from typing import Dict, Tuple, Type, Union

import requests
from devind_helpers.utils import convert_str_to_int
from django.db import transaction
from django.db.models import QuerySet

from .models import District, Organization, Region
from .settings import dictionaries_settings as settings


def parse_organizations(content: str) -> Tuple[Dict, Dict, Dict]:
    """Parse xml file to three structures: District, Regions, Organizations."""
    districts: Dict[int, Dict] = {}
    regions: Dict[int, Dict] = {}
    organizations: Dict[int, Dict] = defaultdict(dict)
    tree: ETree.Element = ETree.fromstring(content) # noqa
    for org in tree.iter('org'):
        district_id: int = convert_str_to_int(org.attrib.get('id_fedokrug'))
        region_id: int = convert_str_to_int(org.attrib.get('id_region'))
        org_id: int = convert_str_to_int(org.attrib.get('idlistedu')) # noqa
        if not all((district_id, region_id, org_id)):
            continue
        if district_id not in districts:
            districts[district_id] = {'name': org.attrib.get('name_fedokrug')}
        if region_id not in regions:
            regions[region_id] = {
                'common_id': region_id,
                'name': org.attrib.get('region'),
                'district_id': district_id
            }
        org_fields: Dict[str, str] = {}
        org_attributes: Dict[str, str] = {}
        for attribute, value in org.attrib.items():
            if attribute in settings.ORGANIZATIONS_MAPPER and value:
                org_fields[settings.ORGANIZATIONS_MAPPER[attribute]] = value
            else:
                org_attributes[attribute] = value
        if convert_str_to_int(org_fields['parent_id']) == org_id:
            del org_fields['parent_id']
        organizations[org_id] = {
            **org_fields,
            'attributes': org_attributes
        }
    return districts, regions, organizations


def update_entity(model: Type[Union[District, Region, Organization]], entities: Dict[int, Dict[str, str]]) -> None:
    """Update Districts, Regions or Organizations in database."""
    identifiers: QuerySet[int] = model.objects.values_list('pk', flat=True)
    with transaction.atomic():
        for pk, defaults in entities.items():
            model.objects.filter(pk=pk).update(**defaults) \
                if pk in identifiers \
                else model.objects.create(id=pk, **defaults)


def get_content(url: str) -> str:
    """Get content from url."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f'The requested content is not available: {url}')
    response.encoding = 'utf-8'
    return response.text
