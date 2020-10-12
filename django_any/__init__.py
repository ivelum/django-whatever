__version__ = (0, 3, 0, 'final', 0)

try:
    from django_any.forms import any_form, any_form_field  # noqa: F401
    from django_any.models import any_field, any_model  # noqa: F401
except Exception:
    pass
