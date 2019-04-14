# -*- coding: utf-8; mode: django -*-
"""
Models that have custom validation checks
"""
from django.db import models
from django.test import TestCase
from django_any.models import any_model
from testapp.models import ModelWithConstraint, \
    ModelWithConstraintOnForeignKey


class PassModelValidation(TestCase):
    def test_model_creation_succeed(self):
        result = any_model(ModelWithConstraint)
        self.assertTrue(result.start_time <= result.end_time)

    def test_foreignkey_constraint_succeed(self):
        result = any_model(ModelWithConstraintOnForeignKey, on_delete=models.CASCADE)
        self.assertTrue(result.timestamp.start_time <= result.timestamp.end_time)

