from django.db.models.fields import NOT_PROVIDED
from django.db.models.fields.related import ForeignKey, OneToOneField

from django_any.models import any_model


def any_model_with_defaults(cls, **attrs):
    """Use model-provided defaults"""

    for field in cls._meta.fields:
        default = field.default
        if default is not NOT_PROVIDED:
            if callable(default):
                # for stuff like default=datetime.now
                default = default()
            if isinstance(field, (ForeignKey, OneToOneField)):
                Model = field.remote_field.model
                if not isinstance(default, Model):
                    try:
                        default = Model.objects.get(pk=default)
                    except Model.DoesNotExist:
                        pass
            attrs.setdefault(field.name, default)

    return any_model(cls, **attrs)
