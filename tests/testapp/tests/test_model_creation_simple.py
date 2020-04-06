"""
Create models will all fields with simply to generate values
"""
from django.test import TestCase

from django_any.models import any_model
from testapp.models import SimpleModel


class SimpleCreation(TestCase):
    def test_model_creation_succeed(self):
        result = any_model(SimpleModel)

        self.assertEqual(type(result), SimpleModel)
        self.assertEqual(len(result._meta.fields), len(
            SimpleModel._meta.local_fields))

        for field, original_field in zip(
            result._meta.fields,
            SimpleModel._meta.local_fields,
        ):
            value = getattr(result, field.name)
            if field.name != 'null_boolead_field':
                self.assertTrue(
                    value is not None,
                    "%s is uninitialized" % field.name,
                )
            self.assertTrue(
                isinstance(field, original_field.__class__),
                "%s has correct field type" % field.name,
            )

    def test_partial_specification(self):
        result = any_model(SimpleModel, char_field='test')
        self.assertEqual(result.char_field, 'test')
