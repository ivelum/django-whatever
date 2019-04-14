# -*- coding: utf-8; mode: django -*-
"""
Test model creation with custom field validation
"""
from django.test import TestCase
from django_any.models import any_model
from testapp.models import ModelWithValidatedField, validate_even


class PassFieldValidation(TestCase):
    def test_created_value_pass_validation(self):
        result = any_model(ModelWithValidatedField)
        validate_even(result.even_field)
