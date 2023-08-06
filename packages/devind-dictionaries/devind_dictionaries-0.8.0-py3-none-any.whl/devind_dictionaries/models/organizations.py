"""Contains models dependence organizations."""

from django.conf import settings
from django.db import models

from .districts import Region


class Organization(models.Model):
    """Organizations model."""

    name = models.CharField(max_length=512, help_text='Name')
    present_name = models.CharField(max_length=512, help_text='Name for view')

    inn = models.CharField(max_length=16, null=True, help_text='Individual taxpayer number')
    kpp = models.CharField(max_length=16, null=True, help_text='Code of reason')
    kind = models.CharField(max_length=64, null=True, help_text='Type')

    rubpnubp = models.CharField(max_length=16, null=True, help_text='Rubpnubp code')
    kodbuhg = models.CharField(max_length=16, null=True, help_text='Accounting code')
    okpo = models.CharField(max_length=10, null=True, help_text='Russian classifier of enterprises and organizations')

    phone = models.CharField(max_length=128, null=True, help_text='Phone number')
    site = models.CharField(max_length=128, null=True, help_text='Site url')
    mail = models.EmailField(max_length=64, null=True, help_text='Email')
    address = models.TextField(null=True, help_text='Address')

    attributes = models.JSONField(help_text='Additional fields')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Created date')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated date')

    parent_id = models.PositiveIntegerField(null=True, default=None, help_text='Parent identifier')
    region = models.ForeignKey(Region, null=True, default=None, on_delete=models.SET_NULL, help_text='Region')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='organization',
        help_text='Director of organization'
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='organizations',
        help_text='Users in organization'
    )

    class Meta:
        """Metaclass for organizations."""

        ordering = ('id', 'name',)
        indexes = (
            models.Index(fields=['id']),
            models.Index(fields=['name']),
            models.Index(fields=['inn', 'kpp']),
        )
