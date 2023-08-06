"""Module for testing budget classification."""

from datetime import datetime, timedelta

from devind_dictionaries.models import BudgetClassification
from django.core.management import call_command
from django.test import TestCase
from django.utils.timezone import make_aware
from example.schema import schema
from graphene.test import Client


COUNT_BUDGET_CLASSIFICATION_CODE = 378
COUNT_CHANGE_CODES = 10

ACTIVE_BUDGET_CLASSIFICATIONS = """
    query {
      activeBudgetClassifications {
        totalCount
        pageInfo {
          hasNextPage
          hasPreviousPage
          startCursor
          endCursor
          __typename
        }
        edges {
          node {
            id
            __typename
          }
        }
      }
    }
"""


class TestBudgetClassification(TestCase):
    """Testing budget classification."""

    def setUp(self) -> None:
        """Setuping test settings."""
        call_command('load_budget_classification')
        self.client = Client(schema)

    def test_invoke_command(self) -> None:
        """Testing invoke command python manage.py load_budget_classification."""
        self.assertEqual(BudgetClassification.objects.count(), COUNT_BUDGET_CLASSIFICATION_CODE)

    def test_budget_classifications(self) -> None:
        """Test budget classification relay query."""
        query = """
        query {
          budgetClassifications {
            totalCount
            pageInfo {
              hasNextPage
              hasPreviousPage
              startCursor
              endCursor
              __typename
            }
            edges {
              node {
                id
                __typename
              }
            }
          }
        }
        """
        find_budget_classification = self.client.execute(query)
        self.assertIsNone(find_budget_classification.get('errors'))
        budget_classification = find_budget_classification['data']['budgetClassifications']
        self.assertEqual(budget_classification['totalCount'], COUNT_BUDGET_CLASSIFICATION_CODE)

    def test_active_budget_classifications(self) -> None:
        """Testing active budget classifications."""
        find_budget_classification = self.client.execute(ACTIVE_BUDGET_CLASSIFICATIONS)
        self.assertIsNone(find_budget_classification.get('errors'))
        budget_classification = find_budget_classification['data']['activeBudgetClassifications']
        self.assertEqual(budget_classification['totalCount'], COUNT_BUDGET_CLASSIFICATION_CODE)

    def test_active_budget_classification(self) -> None:
        """Testing active flag in budget classification."""
        budget_classifications_ids: list[int] = BudgetClassification.objects \
            .values_list('id', flat=True)[:COUNT_CHANGE_CODES]
        self.assertEqual(len(budget_classifications_ids), COUNT_CHANGE_CODES)
        BudgetClassification.objects.filter(pk__in=budget_classifications_ids).update(active=False)
        find_budget_classification = self.client.execute(ACTIVE_BUDGET_CLASSIFICATIONS)
        self.assertIsNone(find_budget_classification.get('errors'))
        budget_classification = find_budget_classification['data']['activeBudgetClassifications']
        self.assertEqual(budget_classification['totalCount'], COUNT_BUDGET_CLASSIFICATION_CODE - COUNT_CHANGE_CODES)

    def test_end_budget_classification_back(self) -> None:
        """Testing end date in budget classification."""
        end = datetime.now() - timedelta(days=2)
        budget_classifications_ids: list[int] = BudgetClassification.objects \
            .values_list('id', flat=True)[:COUNT_CHANGE_CODES]
        self.assertEqual(len(budget_classifications_ids), COUNT_CHANGE_CODES)
        BudgetClassification.objects.filter(pk__in=budget_classifications_ids).update(end=make_aware(end))
        find_budget_classification = self.client.execute(ACTIVE_BUDGET_CLASSIFICATIONS)
        self.assertIsNone(find_budget_classification.get('errors'))
        budget_classification = find_budget_classification['data']['activeBudgetClassifications']
        self.assertEqual(budget_classification['totalCount'], COUNT_BUDGET_CLASSIFICATION_CODE - COUNT_CHANGE_CODES)

    def tearDown(self) -> None:
        """Delete all budget classification code."""
        BudgetClassification.objects.all().delete()
