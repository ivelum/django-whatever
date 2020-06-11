.. _models_creation:

Models creation
===============

You can get model instance saved in database without secifying any model fields

Given you have a simple polls model from django tutorial::

    #models.py
    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')

You can create random poll instance not having to provide question text or pub_date,
if they're not relevant for your test case::

    #tests.py
    from django_any import any_model
    user = any_model(Poll)

It will create a poll instance with both fields filled with meaningless but valid data::

    'question': 'KStKMESUXDjnlDNcJLsAiLcZQGnVXhORIKxWYtPwiqgVXgFvgpmMajwbGFRkoCo'
    'pub_date': datetime.datetime(2002, 10, 1, 6, 1, 16)


django-any will fill all required foreign keys and create related model instances as well.

Specifying values
~~~~~~~~~~~~~~~~~

If you need an instance with specific values you can provide them this way::

    user = any_model(Poll, question='To be or not ot be?')

Note, that ``pub_date`` will still be generated randomly for you.::

    'question': 'To be or not ot be?'
    'pub_date': datetime.datetime(2004, 5, 11, 16, 48, 35)


Constraints
~~~~~~~~~~~

``django-whatever`` will preserve all field constraints, such as max_length,
and choices when filling models with random data.
It also tries to honor model custom validation by making model instances until
``full_clean()`` returns ``True``.

Relations
~~~~~~~~~

``django-whatever`` supports Django ORM-like `double-underscore` syntax
for setting values for related instances::

    #models.py
    class Choice(models.Model):
        poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
        choice = models.CharField(max_length=200)
        votes = models.IntegerField()

    #tests.py
    order = any_model(Choice, poll__pub_date = datetime.now())


Fixtures
~~~~~~~~

In case you need data from fixtures for creation of your models you can use ``Q`` objects
to select values for fields from db::

     order = any_model(Order, customer__location=Q(country='US'))

It will create an order for existing customer, whose country is US.


Custom model fields
~~~~~~~~~~~~~~~~~~~

It's quite common to create custom model fields to store data. To let ``django-whatever`` know how to
generate random data for this filed you should register it explicitly::

    @any_field.register(model_utils.field.AutoCreatedField)
    def any_auto_created_field(field, **kwargs):
        return datetime.datetime.now()

.. note::  When project defines a lot of custom fields, it can be a hassle to
           register all of them manually. Quite often the registered sample data for the field the custom field
           was inherited from will work just as well, so django-whatever tries to use parent generator
           if no function is registered for a custom field.
