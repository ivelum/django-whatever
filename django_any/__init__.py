__version__ = (0, 2, 4, 'final', 0)

try:
    from django_any.forms import any_form_field, any_form  # noqa: F401
    from django_any.models import any_field, any_model  # noqa: F401
except Exception:
    pass
