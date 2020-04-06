from os import path
import codecs
import os
from setuptools import setup

os.environ['DJANGO_SETTINGS_MODULE'] = "testproject.settings"

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

setup(
    name='django-whatever',
    version=":versiontools:django_any:",
    description='Unobtrusive test models creation for django.',
    long_description=read(path.join(path.dirname(__file__), 'README.rst')),
    author='Sergey Fursov',
    author_email='geyser85@gmail.com',
    url='http://github.com/ivelum/django-whatever',
    packages=['django_any', 'django_any.contrib'],
    include_package_data=True,
    test_suite="tests.manage",
    zip_safe=False,
    setup_requires=[
        'versiontools >= 1.8',
    ],
    license='MIT License',
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Topic :: Software Development :: Testing :: Mocking',
    ]
)
