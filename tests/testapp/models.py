import datetime
import os
from decimal import Decimal

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models


class CustomPermission(models.Model):
    name = models.CharField(max_length=5)


class SimpleModelWithDefaults(models.Model):
    big_integer_field = models.BigIntegerField(default=8223372036854775807)
    char_field = models.CharField(max_length=5, default='USSR')
    boolean_field = models.BooleanField(default=True)
    date_field = models.DateField(default=datetime.date(2010, 12, 10))
    datetime_field = models.DateTimeField(datetime.datetime.now)
    decimal_field = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0.5'))
    email_field = models.EmailField(default='admin@dev.null')
    float_field = models.FloatField(default=0.7)
    integer_field = models.IntegerField(default=42)
    ip_field = models.GenericIPAddressField(default='127.0.0.1')
    null_boolead_field = models.NullBooleanField(default=None)
    positive_integer_field = models.PositiveIntegerField(default=4)
    small_integer = models.PositiveSmallIntegerField(default=1)
    slug_field = models.SlugField(default='any_model_default')
    text_field = models.TextField(default='Lorem ipsum')
    time_field = models.TimeField(default=datetime.time(hour=11, minute=14))
    url_field = models.URLField(default='http://yandex.ru')


class TargetModel(models.Model):
    pass


class RelationshipModelsWithDefaults(models.Model):
    fk = models.ForeignKey(TargetModel, on_delete=models.CASCADE, default=1, related_name='related_fk')
    o2o = models.OneToOneField(TargetModel, on_delete=models.CASCADE, default=1, related_name='related_o2o')


class ModelWithConstraint(models.Model):
    """
    Validates that start_time is always before end_time
    """
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError('start_time could not be after end_time')


class ModelWithConstraintOnForeignKey(models.Model):
    timestamp = models.ForeignKey(ModelWithConstraint, on_delete=models.CASCADE)


class SimpleModel(models.Model):
    big_integer_field = models.BigIntegerField()
    char_field = models.CharField(max_length=5)
    boolean_field = models.BooleanField()
    date_field = models.DateField()
    datetime_field = models.DateTimeField()
    decimal_field = models.DecimalField(decimal_places=2, max_digits=10)
    email_field = models.EmailField()
    float_field = models.FloatField()
    integer_field = models.IntegerField()
    ip_field = models.GenericIPAddressField()
    null_boolead_field = models.NullBooleanField()
    positive_integer_field = models.PositiveIntegerField()
    small_integer = models.PositiveSmallIntegerField()
    slug_field = models.SlugField()
    text_field = models.TextField()
    time_field = models.TimeField()
    url_field = models.URLField()
    file_field = models.FileField(upload_to='sample_subdir')
    image_field = models.ImageField(upload_to='sample_subdir')


class MySlugField(models.SlugField):
    pass


class ModelWithCustomField(models.Model):
    slug = MySlugField()


class RelatedContentModel(models.Model):
    name = models.SlugField()


class ModelWithGenericRelation(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%s is not an even number' % value)


class ModelWithValidatedField(models.Model):
    even_field = models.PositiveIntegerField(validators=[validate_even])


class ModelUploadToString(models.Model):
    file_field = models.FileField(upload_to='sample_subdir')


def callable_upload_to(instance, filename):
    return os.path.join('sample_subdir', filename)


class ModelUploadToCallable(models.Model):
    file_field = models.FileField(upload_to=callable_upload_to)


class RelatedModel(models.Model):
    name = models.CharField(max_length=5)


class BaseModel(models.Model):
    related = models.ForeignKey(RelatedModel, on_delete=models.CASCADE)


class SelfReferencingModel(models.Model):
    name = models.CharField(max_length=5)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class OneToOneRelated(models.Model):
    name = models.CharField(max_length=5)


class ModelWithOneToOneField(models.Model):
    name = models.CharField(max_length=5)
    related = models.OneToOneField(OneToOneRelated, on_delete=models.CASCADE)


class QObjectRelated(models.Model):
    pass


class RelatedToQObject(models.Model):
    related = models.ForeignKey(QObjectRelated, on_delete=models.CASCADE)


class Redefined(models.Model):
    name = models.CharField(max_length=5)


class RelatedToRedefined(models.Model):
    related = models.ForeignKey(Redefined, on_delete=models.CASCADE)
