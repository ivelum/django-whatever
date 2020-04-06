import datetime
from decimal import Decimal

from django.test import TestCase
from django.db.models.fields import NOT_PROVIDED

from django_any.contrib.default import any_model_with_defaults
from testapp.models import SimpleModelWithDefaults, TargetModel, \
    RelationshipModelsWithDefaults


class AnyModelWithDefaults(TestCase):
    sample_args = dict(
        big_integer_field=1,
        char_field='USA',
        boolean_field=False,
        date_field=datetime.date(2012, 12, 10),
        datetime_field=datetime.datetime(1985, 12, 10),
        decimal_field=Decimal('1.5'),
        email_field='root@dev.null',
        float_field=1.5,
        integer_field=777,
        ip_field='1.2.3.4',
        null_boolead_field=True,
        positive_integer_field=777,
        small_integer=12,
        slug_field='some_model',
        text_field='Here I come',
        time_field=datetime.time(hour=9, minute=10, second=11),
        url_field='http://google.com',
    )

    def test_default_provided_called_with_no_args(self):
        result = any_model_with_defaults(SimpleModelWithDefaults)

        self.assertEqual(type(result), SimpleModelWithDefaults)
        self.assertEqual(len(result._meta.fields), len(
            SimpleModelWithDefaults._meta.local_fields))

        for field, original_field in zip(result._meta.fields, SimpleModelWithDefaults._meta.local_fields):
            value = getattr(result, field.name)
            if field.name != 'null_boolead_field':
                self.assertTrue(value is not None, "%s is uninitialized" % field.name)
            self.assertTrue(isinstance(field, original_field.__class__), "%s has correct field type" % field.name)
            if original_field.default is not NOT_PROVIDED:
                self.assertEqual(original_field.default, value)

    def test_default_provided_called_with_args(self):
        result = any_model_with_defaults(SimpleModelWithDefaults, **self.sample_args)

        for field, original_field in zip(result._meta.fields, SimpleModelWithDefaults._meta.local_fields):
            self.assertNotEqual(original_field.default, getattr(result, field.name))

    def test_related_fields_instances(self):
        default_target = TargetModel.objects.create()

        standard = RelationshipModelsWithDefaults.objects.create()
        self.assertEqual(standard.fk, default_target)
        self.assertEqual(standard.o2o, default_target)
        standard.delete()  # release o2o field

        try:
            test = any_model_with_defaults(RelationshipModelsWithDefaults)
            self.assertEqual(test.fk, default_target)
            self.assertEqual(test.o2o, default_target)
        except ValueError:
            raise AssertionError(
                '`any_model_with_defaults` must provide models instances '
                'instead of raw values for related fields with defaults.')
