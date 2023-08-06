"""Module with provide command for upload data to database."""

import json
from os.path import dirname, join

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Model


class Command(BaseCommand):
    """Command for upload data budget classification in database."""

    help: str = 'Command for upload data to database' # noqa

    def handle(self, *args, **options) -> None:
        """Invoke command."""
        model: Model = apps.get_model('devind_dictionaries', 'BudgetClassification')
        dir_name: str = dirname(dirname(__file__))
        file: str = join(
            dir_name,
            'seed',
            '001.devind_dictionaries',
            '001.BudgetClassification.json'
        )
        with open(file) as f:
            data = json.load(f)
        with transaction.atomic():
            for bcc in data:
                model.objects.get_or_create(code=bcc['code'], defaults={
                    'name': bcc['name']
                })
        self.stdout.write('Budget classification upload success.')
