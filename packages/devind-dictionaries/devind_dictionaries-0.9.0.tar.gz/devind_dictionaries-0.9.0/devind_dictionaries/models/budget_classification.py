"""Contains information's about budget classification codes."""

from django.db import models

from ..managers import BudgetClassificationManager


class BudgetClassification(models.Model):
    """Budget classification codes."""

    code = models.CharField(max_length=40, unique=True, help_text='Code')
    name = models.CharField(max_length=1024, help_text='Name')

    active = models.BooleanField(default=True, help_text='Active')
    start = models.DateTimeField(auto_now_add=True, help_text='Date of start activity')
    end = models.DateTimeField(null=True, help_text='Date of end activity')

    created_at = models.DateTimeField(auto_now_add=True, help_text='Created date')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated date')

    objects = BudgetClassificationManager()

    class Meta:
        """Metaclass of budget classification codes."""

        ordering = ('code',)
