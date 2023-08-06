"""Contains information's about departments."""

from django.conf import settings
from django.db import models


class Department(models.Model):
    """Describe Department."""

    name = models.CharField(max_length=255, help_text='Department name')
    code = models.IntegerField(null=True, default=None, help_text='Code of department')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Created date')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated date')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='department',
        help_text='Director of department'
    )
    minister = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='minister',
        help_text='Responsible Minister'
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='departments',
        help_text='Users in departments'
    )
    organizations = models.ManyToManyField('devind_dictionaries.Organization', help_text='Related organizations')

    class Meta:
        """Metaclass for describe departments."""

        ordering = ('name',)
