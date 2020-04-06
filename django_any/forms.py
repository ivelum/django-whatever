"""
Django forms data generators

"""
from __future__ import division
import random
from datetime import date, datetime, time
from string import hexdigits

from django import forms
from django.core.validators import validate_ipv4_address, \
    validate_ipv6_address, validate_ipv46_address
from django.utils import formats, six

from django_any import xunit
from django_any.functions import valid_choices, split_model_kwargs, \
    ExtensionMethod

any_form = ExtensionMethod()
any_form_field = ExtensionMethod()


@any_form.register_default
def any_form_default(form_cls, **kwargs):
    """
    Returns tuple with form data and files
    """
    form_data = {}
    form_files = {}

    form_fields, fields_args = split_model_kwargs(kwargs)

    for name, field in six.iteritems(form_cls.base_fields):
        if name in form_fields:
            form_data[name] = kwargs[name]
        else:
            try:
                form_field_data = any_form_field(field, **fields_args[name])
            except Exception:
                if field.required:
                    raise
            else:
                form_data[name] = form_field_data

    return form_data, form_files


@any_form_field.decorator
def field_required_attribute(function):
    """
    Sometimes return None if field is not required

    >>> result = any_form_field(forms.BooleanField(required=False))
    >>> result in ['', 'True', 'False']
    True
    """
    def _wrapper(field, **kwargs):
        if not field.required and random.random < 0.1:
            return None
        return function(field, **kwargs)
    return _wrapper


@any_form_field.decorator
def field_choices_attibute(function):
    """
    Selection from field.choices
    """
    def _wrapper(field, **kwargs):
        if hasattr(field.widget, 'choices'):
            valid_only = list(valid_choices(field.widget.choices))
            if valid_only:
                return random.choice(valid_only)
        return function(field, **kwargs)

    return _wrapper


@any_form_field.register(forms.BooleanField)
def boolean_field_data(field, **kwargs):
    """
    Return random value for BooleanField

    >>> result = any_form_field(forms.BooleanField())
    >>> type(result)
    <type 'str'>
    """
    return str(xunit.any_boolean())


@any_form_field.register(forms.CharField)
def char_field_data(field, **kwargs):
    """
    Return random value for CharField
    >>> result = any_form_field(forms.CharField(min_length=3, max_length=10))
    >>> type(result)
    <type 'str'>
    """
    min_length = kwargs.get('min_length', 1)
    max_length = kwargs.get('max_length', field.max_length or 255)
    return xunit.any_string(min_length=field.min_length or min_length,
                            max_length=field.max_length or max_length)


@any_form_field.register(forms.DecimalField)
def decimal_field_data(field, **kwargs):
    """
    Return random value for DecimalField

    >>> result = any_form_field(forms.DecimalField(max_value=100, min_value=11, max_digits=4, decimal_places = 2))
    >>> type(result)
    <type 'str'>
    >>> from decimal import Decimal
    >>> Decimal(result) >= 11, Decimal(result) <= Decimal('99.99')
    (True, True)
    """
    min_value = 0
    max_value = 10
    from django.core.validators import MinValueValidator, MaxValueValidator
    for elem in field.validators:
        if isinstance(elem, MinValueValidator):
            min_value = elem.limit_value
        if isinstance(elem, MaxValueValidator):
            max_value = elem.limit_value
    if (field.max_digits and field.decimal_places):
        from decimal import Decimal
        max_value = min(max_value,
                        Decimal('%s.%s' % ('9' * (field.max_digits - field.decimal_places),
                                           '9' * field.decimal_places)))

    min_value = kwargs.get('min_value') or min_value
    max_value = kwargs.get('max_value') or max_value

    return str(xunit.any_decimal(min_value=min_value,
                                 max_value=max_value,
                                 decimal_places=field.decimal_places or 2))


@any_form_field.register(forms.EmailField)
def email_field_data(field, **kwargs):
    """
    Return random value for EmailField

    >>> result = any_form_field(forms.EmailField(min_length=10, max_length=30))
    >>> type(result)
    <type 'str'>
    >>> len(result) <= 30, len(result) >= 10
    (True, True)
    """
    max_length = 10
    if field.max_length:
        max_length = (field.max_length - 5) // 2
    min_length = 10
    if field.min_length:
        min_length = (field.min_length - 4) // 2
    return "%s@%s.%s" % (
        xunit.any_string(min_length=min_length, max_length=max_length),
        xunit.any_string(min_length=min_length, max_length=max_length),
        xunit.any_string(min_length=2, max_length=3))


@any_form_field.register(forms.DateField)
def date_field_data(field, **kwargs):
    """
    Return random value for DateField

    >>> result = any_form_field(forms.DateField())
    >>> type(result)
    <type 'str'>
    """
    from_date = kwargs.get('from_date', date(1990, 1, 1))
    to_date = kwargs.get('to_date', date.today())

    date_format = random.choice(field.input_formats or formats.get_format('DATE_INPUT_FORMATS'))

    return xunit.any_date(from_date=from_date, to_date=to_date).strftime(date_format)


@any_form_field.register(forms.DateTimeField)
def datetime_field_data(field, **kwargs):
    """
    Return random value for DateTimeField

    >>> result = any_form_field(forms.DateTimeField())
    >>> type(result)
    <type 'str'>
    """
    from_date = kwargs.get('from_date', datetime(1990, 1, 1))
    to_date = kwargs.get('to_date', datetime.today())
    date_format = random.choice(field.input_formats or formats.get_format('DATETIME_INPUT_FORMATS'))
    return xunit.any_datetime(from_date=from_date, to_date=to_date).strftime(date_format)


@any_form_field.register(forms.FloatField)
def float_field_data(field, **kwargs):
    """
    Return random value for FloatField

    >>> result = any_form_field(forms.FloatField(max_value=200, min_value=100))
    >>> type(result)
    <type 'str'>
    >>> float(result) >=100, float(result) <=200
    (True, True)
    """
    min_value = 0
    max_value = 100
    from django.core.validators import MinValueValidator, MaxValueValidator
    for elem in field.validators:
        if isinstance(elem, MinValueValidator):
            min_value = elem.limit_value
        if isinstance(elem, MaxValueValidator):
            max_value = elem.limit_value

    min_value = kwargs.get('min_value', min_value)
    max_value = kwargs.get('max_value', max_value)
    precision = kwargs.get('precision', 3)

    return str(xunit.any_float(min_value=min_value, max_value=max_value, precision=precision))


@any_form_field.register(forms.IntegerField)
def integer_field_data(field, **kwargs):
    """
    Return random value for IntegerField

    >>> result = any_form_field(forms.IntegerField(max_value=200, min_value=100))
    >>> type(result)
    <type 'str'>
    >>> int(result) >=100, int(result) <=200
    (True, True)
    """
    min_value = 0
    max_value = 100
    from django.core.validators import MinValueValidator, MaxValueValidator
    for elem in field.validators:
        if isinstance(elem, MinValueValidator):
            min_value = elem.limit_value
        if isinstance(elem, MaxValueValidator):
            max_value = elem.limit_value

    min_value = kwargs.get('min_value', min_value)
    max_value = kwargs.get('max_value', max_value)

    return str(xunit.any_int(min_value=min_value, max_value=max_value))


@any_form_field.register(forms.GenericIPAddressField)
def generic_ipaddress_field_data(field, **kwargs):
    """
    Return random value for GenericIPAddressField

    >>> ipv4_address = any_form_field(forms.GenericIPAddressField(protocol='ipv4'))
    >>> type(ipv4_address)
    <type 'str'>
    >>> from django.core.validators import URLValidator
    >>> import re
    >>> re.match(URLValidator.ipv4_re, ipv4_address) is not None
    True
    >>> ipv6_address = any_form_field(forms.GenericIPAddressField(protocol='ipv6'))
    >>> type(ipv6_address)
    <type 'str'>
    >>> from django.utils.ipv6 import is_valid_ipv6_address
    >>> is_valid_ipv6_address(ipv6_address) is True
    True
    >>> ipv46_address = any_form_field(forms.GenericIPAddressField())
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
        return generic_ipaddress_field_data(field)
    if protocol == 'ipv6':
        nums = [str(xunit.any_string(hexdigits, min_length=4, max_length=4)) for _ in six.moves.range(0, 8)]
        return ":".join(nums)


@any_form_field.register(forms.NullBooleanField)
def null_boolean_field_data(field, **kwargs):
    """
    Return random value for NullBooleanField

    >>> result = any_form_field(forms.NullBooleanField())
    >>> type(result)
    <type 'unicode'>
    >>> result in [u'1', u'2', u'3']
    True
    """
    return random.choice(['None', 'True', 'False'])


@any_form_field.register(forms.SlugField)
def slug_field_data(field, **kwargs):
    """
    Return random value for SlugField

    >>> result = any_form_field(forms.SlugField())
    >>> type(result)
    <type 'str'>
    >>> from django.core.validators import slug_re
    >>> import re
    >>> re.match(slug_re, result) is not None
    True
    """
    min_length = kwargs.get('min_length', 1)
    max_length = kwargs.get('max_length', field.max_length or 20)

    from string import ascii_letters, digits
    letters = ascii_letters + digits + '_-'
    return xunit.any_string(letters=letters, min_length=min_length, max_length=max_length)


@any_form_field.register(forms.URLField)
def url_field_data(field, **kwargs):
    """
    Return random value for URLField

    >>> result = any_form_field(forms.URLField())
    >>> from django.core.validators import URLValidator
    >>> import re
    >>> re.match(URLValidator.regex, result) is not None
    True
    """
    urls = kwargs.get('choices',
                      ['http://news.yandex.ru/society.html',
                       'http://video.google.com/?hl=en&tab=wv',
                       'http://www.microsoft.com/en/us/default.aspx',
                       'http://habrahabr.ru/company/opera/',
                       'http://www.apple.com/support/hardware/',
                       'http://localhost/',
                       'http://72.14.221.99',
                       'http://fr.wikipedia.org/wiki/France'])

    return random.choice(urls)


@any_form_field.register(forms.TimeField)
def time_field_data(field, **kwargs):
    """
    Return random value for TimeField

    >>> result = any_form_field(forms.TimeField())
    >>> type(result)
    <type 'str'>
    """
    time_format = random.choice(field.input_formats or formats.get_format('TIME_INPUT_FORMATS'))

    return time(xunit.any_int(min_value=0, max_value=23),
                xunit.any_int(min_value=0, max_value=59),
                xunit.any_int(min_value=0, max_value=59)).strftime(time_format)


@any_form_field.register(forms.TypedChoiceField)
@any_form_field.register(forms.ChoiceField)
def choice_field_data(field, **kwargs):
    """
    Return random value for ChoiceField

    >>> CHOICES = [('YNG', 'Child'), ('OLD', 'Parent')]
    >>> result = any_form_field(forms.ChoiceField(choices=CHOICES))
    >>> type(result)
    <type 'str'>
    >>> result in ['YNG', 'OLD']
    True
    >>> typed_result = any_form_field(forms.TypedChoiceField(choices=CHOICES))
    >>> typed_result in ['YNG', 'OLD']
    True
    """
    if field.choices:
        return str(random.choice(list(valid_choices(field.choices))))
    return 'None'


@any_form_field.register(forms.MultipleChoiceField)
def multiple_choice_field_data(field, **kwargs):
    """
    Return random value for MultipleChoiceField

    >>> CHOICES = [('YNG', 'Child'), ('MIDDLE', 'Parent') ,('OLD', 'GrandParent')]
    >>> result = any_form_field(forms.MultipleChoiceField(choices=CHOICES))
    >>> type(result)
    <type 'str'>
    """
    if field.choices:
        from django_any.functions import valid_choices
        valid_choices_list = list(valid_choices(field.choices))
        random.shuffle(valid_choices_list)
        choices = []
        count = xunit.any_int(min_value=1, max_value=len(field.choices))
        for i in six.moves.range(0, count):
            choices.append(valid_choices_list[i])
        return ' '.join(choices)
    return 'None'


@any_form_field.register(forms.models.ModelChoiceField)
def model_choice_field_data(field, **kwargs):
    """
    Return one of first ten items for field queryset
    """
    data = list(field.queryset[:10])
    if data:
        return random.choice(data)
    else:
        raise TypeError('No %s available in queryset' % field.queryset.model)
