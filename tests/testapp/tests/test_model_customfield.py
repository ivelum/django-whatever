"""
Test model creation with custom fields
"""
from django.test import TestCase

from django_any.models import any_model
from testapp.models import ModelWithCustomField


class CustomFieldsTest(TestCase):

    def test_created_model_with_custom_field(self):
        model = any_model(ModelWithCustomField)

        self.assertEqual(type(model), ModelWithCustomField)
        self.assertEqual(len(model._meta.fields), len(
            ModelWithCustomField._meta.local_fields))

        self.assertTrue(model.slug)
        self.assertTrue(isinstance(model.slug, str))
