.. _changelog:

Changelog
=========

dev
~~~

* automated tests in Travis CI

0.3.0
~~~~~

* dropped Django 1.1, 2.0, 2.2 and Python 2.7, 3.4 support
* added Django 3.0 and Python 3.8 suport
* added automated codestyle checks

0.2.4
~~~~~

* A bunch of maintenance updates that happened during the "unmaintained" mode.
* The last version with Django 1.11, 2.0, and 2.1 support

0.2.3
~~~~~

* Values for custom fields are created with their parent generator if the field is not registered (#22)

0.2.2
~~~~~

* Fixed pip installation
* Added ability to login_as arbitrary user

0.2.1
~~~~~

* Added xunit reference docs
* Fixed ``any_text_field`` return value
* Updated setup.py to use versiontools
* Minor updates and bugfixes in docs and LICENCE

0.2.0
~~~~~

* Fixed ``ImportError: cannot import name _strclass`` for python 2.7
* Added ``any_model_with_defaults`` function to generate models with default values where acceptible
* Fixed tests for django 1.4 compatibility
* Added support for GenericIPAddressField in both model and forms (django 1.4 and above)
* Multiple minor updates and bugfixes in docs

0.1.0
~~~~~

* Forked django-any and renamed to django-whatever
* Created complete documentation for package
* Models with ``GenericForeignKey`` can be created with ``any_model(MyModel, content_object=object)``
* Self-referencing models no longer produce ``"RuntimeError: maximum recursion depth exceeded"``
* ``ImageField`` and naive callable ``upload_to`` support.


django-any changelog
~~~~~~~~~~~~~~~~~~~~

Not maintained
