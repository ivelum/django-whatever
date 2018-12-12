# -*- coding: utf-8; -*-
import datetime
from decimal import Decimal

from django.db import models
from django.test import TestCase
from django.db.models.fields import NOT_PROVIDED

from django_any.contrib.default import any_model_with_defaults


class SimpleModelWithDefaults(models.Model):
    big_integer_field = models.BigIntegerField(default=8223372036854775807)
    char_field = models.CharField(max_length=5, default='USSR')
    boolean_field = models.BooleanField(default=True)
    date_field = models.DateField(default=datetime.date(2010, 12, 10))
    datetime_field = models.DateTimeField(datetime.datetime.now)
    decimal_field = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0.5'))
    email_field = models.EmailField(default='admin@dev.null')
    float_field = models.FloatField(default=0.7)
    integer_field = models.IntegerField(default=42)
    ip_field = models.GenericIPAddressField(default='127.0.0.1')
    null_boolead_field = models.NullBooleanField(default=None)
    positive_integer_field = models.PositiveIntegerField(default=4)
    small_integer = models.PositiveSmallIntegerField(default=1)
    slug_field = models.SlugField(default='any_model_default')
    text_field = models.TextField(default='Lorem ipsum')
    time_field = models.TimeField(default=datetime.time(hour=11, minute=14))
    url_field = models.URLField(default='http://yandex.ru')

    class Meta:
        app_label = 'django_any'


class TargetModel(models.Model):
    class Meta:
        app_label = 'django_any'


class RelationshipModelsWithDefaults(models.Model):
    fk = models.ForeignKey(TargetModel, on_delete=models.CASCADE, default=1, related_name='related_fk')
    o2o = models.OneToOneField(TargetModel, on_delete=models.CASCADE, default=1, related_name='related_o2o')

    class Meta:
        app_label = 'django_any'


class AnyModelWithDefaults(TestCase):
    sample_args = dict(
        big_integer_field = 1,
        char_field = 'USA',
        boolean_field = False,
        date_field = datetime.date(2012, 12, 10),
        datetime_field = datetime.datetime(1985, 12, 10),
        decimal_field = Decimal('1.5'),
        email_field = 'root@dev.null',
        float_field = 1.5,
        integer_field = 777,
        ip_field = '1.2.3.4',
        null_boolead_field = True,
        positive_integer_field = 777,
        small_integer = 12,
        slug_field = 'some_model',
        text_field = 'Here I come',
        time_field = datetime.time(hour=9, minute=10, second=11),
        url_field = 'http://google.com',
    )

    def test_default_provided_called_with_no_args(self):
        result = any_model_with_defaults(SimpleModelWithDefaults)

        self.assertEqual(type(result), SimpleModelWithDefaults)
        self.assertEqual(len(result._meta.fields), len(SimpleModelWithDefaults._meta.local_fields))

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
