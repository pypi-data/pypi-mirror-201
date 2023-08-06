"""Contains a description of models of regions and districts."""

from django.db import models


class District(models.Model):
    """Describe district."""

    name = models.CharField(max_length=255, help_text='District name')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created date')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated date')

    class Meta:
        """Metaclass for describe district."""

        ordering = ('name',)
        indexes = (
            models.Index(fields=['name']),
        )


class Region(models.Model):
    """Describe regions.

    If district is None, then region out the Russia.
    """

    name = models.CharField(max_length=255, help_text='Region name')
    common_id = models.PositiveIntegerField(null=True, help_text='Real code of region')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created date')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated date')

    district = models.ForeignKey(District, null=True, on_delete=models.SET_NULL)

    class Meta:
        """Metaclass for describe region."""

        ordering = ('common_id', 'name',)
        indexes = (
            models.Index(fields=['common_id']),
            models.Index(fields=['name']),
        )
