# -*- coding: utf-8; mode: django -*-
from django.db import models
from django.test import TestCase
from django_any.models import any_field
from django_any.test import WithTestDataSeed, with_seed, without_random_seed


# Skip until #4 is fixed

#class CustomSeed(TestCase):
#    __metaclass__ = WithTestDataSeed
#
#    @without_random_seed
#    @with_seed(1)
#    def test_deterministic_string(self):
#        media = models.CharField(max_length=25)
#        result = any_field(media)
#        self.assertEqual('SNnz', result)
