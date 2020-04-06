from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from django_any.test import Client


def view(request):
    """
    Test view that returning form
    """
    from django import forms
    from django.http import HttpResponse
    from django.shortcuts import redirect
    from django.template import Context, Template

    class TestForm(forms.Form):
        name = forms.CharField()

    if request.POST:
        form = TestForm(request.POST)
        if form.is_valid():
            return redirect('/view/')
    else:
        form = TestForm()

    template = Template("{{ form }}")
    context = Context({'form': form})

    return HttpResponse(template.render(context))


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^view/', view),
]


@override_settings(ROOT_URLCONF='testapp.tests.test_client')
class DjangoAnyClient(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_as_super_user(self):
        # TODO make test page which will not require is_staff like /admin
        self.assertTrue(self.client.login_as(is_superuser=True, is_staff=True))

        response = self.client.get('/admin/')
        self.assertEqual(200, response.status_code)

    def test_login_as_custom_user(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.assertTrue(self.client.login_as(user=user))

    def test_login_as_failed(self):
        user = None
        self.assertRaises(AssertionError, self.client.login_as, user=user)

    def test_post_any_data(self):
        response = self.client.post_any_data('/view/')
        self.assertRedirects(response, '/view/')
