"""Module with settings."""

from typing import Dict, Optional

from django.conf import settings

USER_TYPE: str = getattr(settings, 'DEVIND_CORE_USER_TYPE', None)

assert USER_TYPE, 'UserType is not set: settings.DEVIND_CORE_USER_TYPE'

ORGANIZATIONS_LINK: str = getattr(
    settings,
    'DEVIND_DICTIONARIES_ORGANIZATIONS_LINK',
    'https://reestr.cbias.ru/org_list_xml'
)

ORGANIZATIONS_MAPPER: Dict[str, str] = {
    'id_parent': 'parent_id',
    'id_region': 'region_id',
    'name': 'name',
    'name_small': 'present_name',
    'inn': 'inn',
    'kpp': 'kpp',
    'type': 'kind',
    'id_rubpnubp': 'rubpnubp',
    'id_kodbuhg': 'kodbuhg',
    'okpo': 'okpo',
    'phone': 'phone',
    'site': 'site',
    'mail': 'mail',
    'address': 'address',
}

DEFAULTS = {
    'USER_TYPE': USER_TYPE,
    'ORGANIZATIONS_LINK': ORGANIZATIONS_LINK,
    'ORGANIZATIONS_MAPPER': ORGANIZATIONS_MAPPER
}


class DevindDictionariesSettings:
    """Settings devind dictionaries."""

    def __init__(self: 'DevindDictionariesSettings', defaults: Optional[Dict[str, str]] = None) -> None:
        """Initialize devind dictionaries settings."""
        self.defaults: Dict[str, str] = defaults or DEFAULTS

    def __getattr__(self: 'DevindDictionariesSettings', item: str) -> str:
        """Get settings attribute."""
        if item not in self.defaults:
            raise AttributeError(f'Invalid devind_dictionaries attribute: {item}')
        return self.defaults[item]


dictionaries_settings = DevindDictionariesSettings(DEFAULTS)
