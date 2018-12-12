# -*- coding: utf-8; mode: django -*-
"""
Create models will all fields with simply to generate values
"""
from django.db import models
from django.test import TestCase

from django_any.models import any_model


class SimpleModel(models.Model):
    big_integer_field = models.BigIntegerField()
    char_field = models.CharField(max_length=5)
    boolean_field = models.BooleanField()
    date_field = models.DateField()
    datetime_field = models.DateTimeField()
    decimal_field = models.DecimalField(decimal_places=2, max_digits=10)
    email_field = models.EmailField()
    float_field = models.FloatField()
    integer_field = models.IntegerField()
    ip_field = models.GenericIPAddressField()
    null_boolead_field = models.NullBooleanField()
    positive_integer_field = models.PositiveIntegerField()
    small_integer = models.PositiveSmallIntegerField()
    slug_field = models.SlugField()
    text_field = models.TextField()
    time_field = models.TimeField()
    url_field = models.URLField()
    file_field = models.FileField(upload_to='sample_subdir')
    image_field = models.ImageField(upload_to='sample_subdir')

    class Meta:
        app_label = 'django_any'


class SimpleCreation(TestCase):
    def test_model_creation_succeed(self):
        result = any_model(SimpleModel)

        self.assertEqual(type(result), SimpleModel)
        self.assertEqual(len(result._meta.fields), len(SimpleModel._meta.local_fields))

        for field, original_field in zip(result._meta.fields, SimpleModel._meta.local_fields):
            value = getattr(result, field.name)
            if field.name != 'null_boolead_field':
                self.assertTrue(value is not None, "%s is uninitialized" % field.name)
            self.assertTrue(isinstance(field, original_field.__class__), "%s has correct field type" % field.name)

    def test_partial_specification(self):
        result = any_model(SimpleModel, char_field='test')
        self.assertEqual(result.char_field, 'test')

