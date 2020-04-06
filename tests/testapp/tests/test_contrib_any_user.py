from django.contrib.auth.models import User
from django.test import TestCase

from django_any.contrib.auth import any_user
from django_any.models import any_model


class AnyUser(TestCase):
    def test_raw_user_creation(self):
        result = any_model(User)
        self.assertEqual(type(result), User)

    def test_create_superuser(self):
        user = any_user(is_superuser=True)
        self.assertTrue(user.is_superuser)

    def test_create_with_permissions(self):
        user = any_user(permissions=['testapp.add_custompermission',
                                     'testapp.delete_custompermission'])

        self.assertTrue(user.has_perm('testapp.add_custompermission'))
        self.assertTrue(user.has_perm('testapp.delete_custompermission'))
        self.assertFalse(user.has_perm('testapp.change_custompermission'))
