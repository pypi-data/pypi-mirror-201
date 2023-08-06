"""Module define permission in dictionaries."""

from devind_helpers.permissions import ModelPermission


ChangeDistrict = ModelPermission('devind_dictionaries.change_district')
ChangeRegion = ModelPermission('devind_dictionaries.change_region')
ChangeOrganization = ModelPermission('devind_dictionaries.change_organization')
