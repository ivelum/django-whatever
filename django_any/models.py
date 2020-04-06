"""
Values generators for common Django Fields
"""
from __future__ import division
import random
import re
import os
from decimal import Decimal
from datetime import date, datetime, time
from string import ascii_letters, digits, hexdigits

from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address, \
    validate_ipv6_address, validate_ipv46_address
from django.contrib.contenttypes.models import ContentType
from django.db import models, IntegrityError, transaction
from django.db.models import Q
from django.db.models.fields.files import FieldFile
from django.utils import six
from django.utils.lorem_ipsum import paragraphs

from django_any import xunit
from django_any.functions import valid_choices, split_model_kwargs, ExtensionMethod

any_field = ExtensionMethod()
any_model = ExtensionMethod(by_instance=True)


@any_field.decorator
def any_field_blank(function):
    """
    Sometimes return empty value if field could be blank
    """
    def wrapper(field, **kwargs):
        # any_model(Entry, pub_date__isnull=True)
        if kwargs.get('isnull', False):
            return None

        if field.blank and random.random() < 0.1:
            if field.null:
                return None
            else:
                try:
                    return field.to_python('')
                except ValidationError:  # bool, int, etc.
                    pass

        return function(field, **kwargs)
    return wrapper


@any_field.decorator
def any_field_choices(function):
    """
    Selection from field.choices

    >>> CHOICES = [('YNG', 'Child'), ('OLD', 'Parent')]
    >>> result = any_field(models.CharField(max_length=3, choices=CHOICES))
    >>> result in ['YNG', 'OLD']
    True
    """
    def wrapper(field, **kwargs):
        if field.choices:
            return random.choice(list(valid_choices(field.choices)))
        return function(field, **kwargs)

    return wrapper


@any_field.register(models.BigIntegerField)
def any_biginteger_field(field, **kwargs):
    """
    Return random value for BigIntegerField

    >>> result = any_field(models.BigIntegerField())
    >>> type(result)
    <type 'long'>
    """
    min_value = kwargs.get('min_value', 1)
    max_value = kwargs.get('max_value', 10**10)
    if six.PY3:
        long_type = int
    else:
        long_type = long  # noqa
    return long_type(xunit.any_int(min_value=min_value, max_value=max_value))


@any_field.register(models.BooleanField)
def any_boolean_field(field, **kwargs):
    """
    Return random value for BooleanField

    >>> result = any_field(models.BooleanField())
    >>> type(result)
    <type 'bool'>
    """
    return xunit.any_boolean()


@any_field.register(models.PositiveIntegerField)
def any_positiveinteger_field(field, **kwargs):
    """
    An positive integer

    >>> result = any_field(models.PositiveIntegerField())
    >>> type(result)
    <type 'int'>
    >>> result > 0
    True
    """
    min_value = kwargs.get('min_value', 1)
    max_value = kwargs.get('max_value', 9999)
    return xunit.any_int(min_value=min_value, max_value=max_value)


@any_field.register(models.CharField)
def any_char_field(field, **kwargs):
    """
    Return random value for CharField

    >>> result = any_field(models.CharField(max_length=10))
    >>> type(result)
    <type 'str'>
    """
    if validators.validate_comma_separated_integer_list in field.validators:
        return any_commaseparatedinteger_field(field, **kwargs)

    min_length = kwargs.get('min_length', 1)
    max_length = kwargs.get('max_length', field.max_length)
    return xunit.any_string(min_length=min_length, max_length=max_length)


@any_field.register(models.CommaSeparatedIntegerField)
def any_commaseparatedinteger_field(field, **kwargs):
    """
    Return random value for CharField

    >>> result = any_field(models.CommaSeparatedIntegerField(max_length=10))
    >>> type(result)
    <type 'str'>
    >>> [int(num) for num in result.split(',')] and 'OK'
    'OK'
    """
    nums_count = field.max_length // 2
    nums = [str(xunit.any_int(min_value=0, max_value=9)) for _ in six.moves.range(0, nums_count)]
    return ",".join(nums)


@any_field.register(models.DateField)
def any_date_field(field, **kwargs):
    """
    Return random value for DateField,
    skips auto_now and auto_now_add fields

    >>> result = any_field(models.DateField())
    >>> type(result)
    <type 'datetime.date'>
    """
    if field.auto_now or field.auto_now_add:
        return None
    from_date = kwargs.get('from_date', date(1990, 1, 1))
    to_date = kwargs.get('to_date', date.today())
    return xunit.any_date(from_date=from_date, to_date=to_date)


@any_field.register(models.DateTimeField)
def any_datetime_field(field, **kwargs):
    """
    Return random value for DateTimeField,
    skips auto_now and auto_now_add fields

    >>> result = any_field(models.DateTimeField())
    >>> type(result)
    <type 'datetime.datetime'>
    """
    USE_TZ = getattr(settings, 'USE_TZ', False)
    from_date = kwargs.get('from_date', datetime(1990, 1, 1))

    if USE_TZ:
        from django.utils.timezone import now, get_current_timezone, make_aware

        from_date = make_aware(from_date, get_current_timezone())
        to_date = kwargs.get('to_date', now())
    else:
        to_date = kwargs.get('to_date', datetime.today())

    return xunit.any_datetime(from_date=from_date, to_date=to_date)


@any_field.register(models.DecimalField)
def any_decimal_field(field, **kwargs):
    """
    Return random value for DecimalField

    >>> result = any_field(models.DecimalField(max_digits=5, decimal_places=2))
    >>> type(result)
    <class 'decimal.Decimal'>
    """
    min_value = kwargs.get('min_value', 0)
    max_value = kwargs.get('max_value',
                           Decimal('%s.%s' % ('9' * (field.max_digits - field.decimal_places),
                                              '9' * field.decimal_places)))
    decimal_places = kwargs.get('decimal_places', field.decimal_places)
    return xunit.any_decimal(min_value=min_value, max_value=max_value,
                             decimal_places=decimal_places)


@any_field.register(models.EmailField)
def any_email_field(field, **kwargs):
    """
    Return random value for EmailField

    >>> result = any_field(models.EmailField())
    >>> type(result)
    <type 'str'>
    >>> re.match(r"(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)", result, re.IGNORECASE) is not None  # noqa
    True
    """
    return xunit.any_email()


@any_field.register(models.FloatField)
def any_float_field(field, **kwargs):
    """
    Return random value for FloatField

    >>> result = any_field(models.FloatField())
    >>> type(result)
    <type 'float'>
    """
    min_value = kwargs.get('min_value', 1)
    max_value = kwargs.get('max_value', 100)
    precision = kwargs.get('precision', 3)
    return xunit.any_float(min_value=min_value, max_value=max_value, precision=precision)


@any_field.register(models.FileField)
@any_field.register(models.ImageField)
def any_file_field(field, **kwargs):
    """
    Lookup for nearest existing file

    """
    def get_some_file(path):
        subdirs, files = field.storage.listdir(path)

        if files:
            result_file = random.choice(files)
            instance = field.storage.open(os.path.join(path, result_file)).file
            return FieldFile(instance, field, result_file)

        for subdir in subdirs:
            result = get_some_file(os.path.join(path, subdir))
            if result:
                return result

    if callable(field.upload_to):
        generated_filepath = field.upload_to(None, xunit.any_string(ascii_letters, 10, 20))
        upload_to = os.path.dirname(generated_filepath)
    else:
        upload_to = field.upload_to
    if not field.storage.exists(upload_to):
        # make a directory, assuming it's on local file system
        os.makedirs(field.storage.path(upload_to))
    result = get_some_file(upload_to)

    if result is None and not field.blank:
        raise TypeError("Can't found file in %s for non nullable FileField" % field.upload_to)
    return result


@any_field.register(models.FilePathField)
def any_filepath_field(field, **kwargs):
    """
    Lookup for nearest existing file

    """
    def get_some_file(path):
        subdirs, files = [], []
        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                subdirs.append(entry_path)
            else:
                if not field.match or re.match(field.match, entry):
                    files.append(entry_path)

        if files:
            return random.choice(files)

        if field.recursive:
            for subdir in subdirs:
                result = get_some_file(subdir)
                if result:
                    return result

    result = get_some_file(field.path)
    if result is None and not field.null:
        raise TypeError("Can't found file in %s for non nullable FilePathField" % field.path)
    return result


@any_field.register(models.UUIDField)
def any_uuid_field(field, **kwargs):
    """
    Return random value for UUIDField
    >>> result = any_field(models.UUIDField())
    >>> type(result)
    <class 'uuid.UUID'>
    """
    import uuid
    return uuid.uuid4()


@any_field.register(models.GenericIPAddressField)
def any_genericipaddress_field(field, **kwargs):
    """
    Return random value for GenericIPAddressField
    >>> ipv4_address = any_field(models.GenericIPAddressField(protocol='ipv4'))
    >>> type(ipv4_address)
    <type 'str'>
    >>> from django.core.validators import URLValidator
    >>> re.match(URLValidator.ipv4_re, ipv4_address) is not None
    True
    >>> ipv6_address = any_field(models.GenericIPAddressField(protocol='ipv6'))
    >>> type(ipv6_address)
    <type 'str'>
    >>> from django.utils.ipv6 import is_valid_ipv6_address
    >>> is_valid_ipv6_address(ipv6_address) is True
    True
    >>> ipv46_address = any_field(models.GenericIPAddressField())
    >>> type(ipv46_address)
    <type 'str'>
    >>> from django.core.validators import validate_ipv46_address
    >>> validate_ipv46_address(ipv46_address) is True
    False
    """
    if field.default_validators == [validate_ipv46_address]:
        protocol = random.choice(('ipv4', 'ipv6'))
    elif field.default_validators == [validate_ipv4_address]:
        protocol = 'ipv4'
    elif field.default_validators == [validate_ipv6_address]:
        protocol = 'ipv6'
    else:
        raise Exception('Unexpected validators')

    if protocol == 'ipv4':
        return any_genericipaddress_field(field)
    if protocol == 'ipv6':
        nums = [str(xunit.any_string(hexdigits, min_length=4, max_length=4)) for _ in six.moves.range(0, 8)]
        return ":".join(nums)


@any_field.register(models.NullBooleanField)
def any_nullboolean_field(field, **kwargs):
    """
    Return random value for NullBooleanField
    >>> result = any_field(models.NullBooleanField())
    >>> result in [None, True, False]
    True
    """
    return random.choice([None, True, False])


@any_field.register(models.PositiveSmallIntegerField)
def any_positivesmallinteger_field(field, **kwargs):
    """
    Return random value for PositiveSmallIntegerField
    >>> result = any_field(models.PositiveSmallIntegerField())
    >>> type(result)
    <type 'int'>
    >>> result < 256, result > 0
    (True, True)
    """
    min_value = kwargs.get('min_value', 1)
    max_value = kwargs.get('max_value', 255)
    return xunit.any_int(min_value=min_value, max_value=max_value)


@any_field.register(models.SlugField)
def any_slug_field(field, **kwargs):
    """
    Return random value for SlugField
    >>> result = any_field(models.SlugField())
    >>> type(result)
    <type 'str'>
    >>> from django.core.validators import slug_re
    >>> re.match(slug_re, result) is not None
    True
    """
    letters = ascii_letters + digits + '_-'
    return xunit.any_string(letters=letters, max_length=field.max_length)


@any_field.register(models.SmallIntegerField)
def any_smallinteger_field(field, **kwargs):
    """
    Return random value for SmallIntegerValue
    >>> result = any_field(models.SmallIntegerField())
    >>> type(result)
    <type 'int'>
    >>> result > -256, result < 256
    (True, True)
    """
    min_value = kwargs.get('min_value', -255)
    max_value = kwargs.get('max_value', 255)
    return xunit.any_int(min_value=min_value, max_value=max_value)


@any_field.register(models.IntegerField)
def any_integer_field(field, **kwargs):
    """
    Return random value for IntegerField
    >>> result = any_field(models.IntegerField())
    >>> type(result)
    <type 'int'>
    """
    min_value = kwargs.get('min_value', -10000)
    max_value = kwargs.get('max_value', 10000)
    return xunit.any_int(min_value=min_value, max_value=max_value)


@any_field.register(models.TextField)
def any_text_field(field, **kwargs):
    """
    Return random 'lorem ipsum' Latin text
    >>> result = any_field(models.TextField())
    >>> type(result)
    <type 'str'>
    """
    return str("\n".join(paragraphs(10)))


@any_field.register(models.URLField)
def any_url_field(field, **kwargs):
    """
    Return random value for URLField
    >>> result = any_field(models.URLField())
    >>> from django.core.validators import URLValidator
    >>> re.match(URLValidator.regex, result) is not None
    True
    """
    url = kwargs.get('url')

    if not url:
        verified = [validator for validator in field.validators
                    if isinstance(validator, validators.URLValidator) and
                    getattr(validator, 'verify_exists', False)]
        if verified:
            url = random.choice(['http://news.yandex.ru/society.html',
                                 'http://video.google.com/?hl=en&tab=wv',
                                 'http://www.microsoft.com/en/us/default.aspx',
                                 'http://habrahabr.ru/company/opera/',
                                 'http://www.apple.com/support/hardware/',
                                 'http://ya.ru',
                                 'http://google.com',
                                 'http://fr.wikipedia.org/wiki/France'])
        else:
            url = "http://%s.%s/%s" % (
                xunit.any_string(max_length=10),
                xunit.any_string(min_length=2, max_length=3),
                xunit.any_string(max_length=20))

    return url


@any_field.register(models.TimeField)
def any_time_field(field, **kwargs):
    """
    Return random value for TimeField
    >>> result = any_field(models.TimeField())
    >>> type(result)
    <type 'datetime.time'>
    """
    return time(
        xunit.any_int(min_value=0, max_value=23),
        xunit.any_int(min_value=0, max_value=59),
        xunit.any_int(min_value=0, max_value=59))


@any_field.register(models.ForeignKey)
def any_foreignkey_field(field, **kwargs):
    return any_model(field.remote_field.model, **kwargs)


@any_field.register(models.OneToOneField)
def any_onetoone_field(field, **kwargs):
    return any_model(field.remote_field.model, **kwargs)


def _fill_model_fields(model, **kwargs):
    model_fields, fields_args = split_model_kwargs(kwargs)

    # fill virtual fields
    for field in model._meta.private_fields:
        if field.name in model_fields:
            object = kwargs[field.name]
            model_fields[field.ct_field] = kwargs[field.ct_field] = ContentType.objects.get_for_model(object)
            model_fields[field.fk_field] = kwargs[field.fk_field] = object.id
    # fill local fields
    for field in model._meta.fields:
        if field.name in model_fields:
            if isinstance(kwargs[field.name], Q):
                """
                Lookup ForeingKey field in db
                """
                key_field = model._meta.get_field(field.name)
                value = key_field.remote_field.model.objects.get(kwargs[field.name])
                setattr(model, field.name, value)
            else:
                # TODO support any_model call
                setattr(model, field.name, kwargs[field.name])
        elif isinstance(field, models.OneToOneField) and field.remote_field.parent_link:
            """
            skip link to parent instance
            """
        elif isinstance(field, models.fields.AutoField):
            """
            skip primary key field
            """
        elif isinstance(field, models.fields.related.ForeignKey) and field.model == field.remote_field.model:
            """
            skip self relations
            """
        else:
            setattr(model, field.name, any_field(field, **fields_args[field.name]))

    onetoone_fields = [
        (relation.name, relation)
        for relation in model._meta.get_fields()
        if relation.one_to_one and relation.auto_created
    ]
    for field_name, field in onetoone_fields:
        if field_name in model_fields:
            # TODO support any_model call
            setattr(model, field_name, kwargs[field_name])


@any_model.register_default
def any_model_default(model_cls, **kwargs):
    result = model_cls()

    attempts = 10
    while True:
        try:
            with transaction.atomic():
                _fill_model_fields(result, **kwargs)
                result.full_clean()
                result.save()
                return result
        except (IntegrityError, ValidationError):
            attempts -= 1
            if not attempts:
                raise
