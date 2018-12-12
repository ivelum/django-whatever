# -*- coding: utf-8 -*-
"""
Test model creation with custom fields
"""
from django.db import models
from django.test import TestCase
from django.utils import six
from django_any.models import any_model


class MySlugField(models.SlugField):
    pass


class ModelWithCustomField(models.Model):
    slug = MySlugField()

    class Meta:
        app_label = 'django_any'


class CustomFieldsTest(TestCase):

    def test_created_model_with_custom_field(self):
        model = any_model(ModelWithCustomField)

        self.assertEqual(type(model), ModelWithCustomField)
        self.assertEqual(len(model._meta.fields), len(ModelWithCustomField._meta.local_fields))

        self.assertTrue(model.slug)
        self.assertTrue(isinstance(model.slug, six.string_types))
