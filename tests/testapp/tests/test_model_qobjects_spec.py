"""
Allow partial specifications with q objects
"""
from django.db.models import Q
from django.test import TestCase
from django_any.models import any_model
from testapp.models import QObjectRelated, RelatedToQObject


class QObjectsSupport(TestCase):
    def setUp(self):
        self.related = any_model(QObjectRelated)

    def test_qobject_specification(self):
        result = any_model(RelatedToQObject, related=Q(pk=self.related.pk))
        self.assertEqual(self.related, result.related)
