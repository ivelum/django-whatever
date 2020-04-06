"""
Test model creation with FileField
"""
from django.test import TestCase

from django_any.models import any_model
from testapp.models import ModelUploadToCallable, ModelUploadToString


class FileFiledUploadTo(TestCase):

    def test_created_model_with_filefield_string_upload_to(self):
        model = any_model(ModelUploadToString)
        self.assertEqual(model.file_field, 'sample_file.txt')

    def test_created_model_with_filefield_callable_upload_to(self):
        model = any_model(ModelUploadToCallable)
        self.assertEqual(model.file_field, 'sample_file.txt')
