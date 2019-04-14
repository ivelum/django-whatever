# -*- coding: utf-8; mode: django -*-
from django.test import TestCase
from django_any.models import any_model
from testapp.models import Redefined, RelatedToRedefined


@any_model.register(Redefined)
def any_redefined_model(model_cls, **kwargs):
    kwargs['name'] = kwargs.get('name', 'test')  
    return any_model.default(model_cls, **kwargs)


class RedefinedCreation(TestCase):
    def test_redefined_creation(self):        
        result = any_model(Redefined)
        self.assertEqual(result.name, 'test')

    def test_redefined_creation_partial_specification(self):
        result = any_model(Redefined, name="test2")
        self.assertEqual(result.name, 'test2')

    # TODO Fix model factory registration
    def _test_create_related_redefied(self):
        result = any_model(RelatedToRedefined)
        self.assertEqual(result.related.name, 'test')
