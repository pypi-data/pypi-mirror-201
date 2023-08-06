"""Manager for extend default managers."""

from django.db import models
from django.db.models import Q, QuerySet
from django.utils import timezone


class BudgetClassificationManager(models.Manager):
    """Extend default managers."""

    def active_now(self) -> QuerySet:
        """Get active budget classifications."""
        now = timezone.now()
        return self.filter(
            Q(active=True, start__lt=now) & Q(Q(end__gt=now) | Q(end__isnull=True))
        )
