"""
Auto-create foreingkey referencies
"""
from django.test import TestCase

from django_any.models import any_model
from testapp.models import BaseModel, RelatedModel, SelfReferencingModel


class ForeignKeyCreation(TestCase):
    def test_fk_relation_autocreate(self):
        result = any_model(BaseModel)

        self.assertEqual(type(result), BaseModel)

        self.assertEqual(type(result.related), RelatedModel)
        self.assertTrue(result.related.name is not None)

    def test_nested_models_specification(self):
        result = any_model(BaseModel, related__name='test')
        self.assertEqual(result.related.name, 'test')

    def test_fk_referencing_self(self):
        self_referencing = any_model(SelfReferencingModel)
        self.assertTrue(self_referencing.parent is None)

        root = any_model(SelfReferencingModel)
        child = any_model(SelfReferencingModel, parent=root)
        self.assertEqual(type(child.parent), SelfReferencingModel)
