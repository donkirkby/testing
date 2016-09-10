# Tested with Django 1.9.2
import sys

import django
from django.apps import apps
from django.apps.config import AppConfig
from django.conf import settings
from django.db import connections, models, DEFAULT_DB_ALIAS
from django.db.models.base import ModelBase

NAME = 'udjango'


def main():
    setup()

    class City(models.Model):
        name = models.CharField(max_length=100)

    class Person(models.Model):
        name = models.CharField(max_length=50)
        city = models.ForeignKey(City, related_name='residents')

        def count_dependents(self):
            return self.children.count()

    class Child(models.Model):
        parent = models.ForeignKey(Person, related_name='children')
        name = models.CharField(max_length=255)

    syncdb(City)
    syncdb(Person)
    syncdb(Child)

    # A typical unit test would start here.
    # The set up is irrelevant to the test, but required by the database.
    city = City.objects.create(name='Vancouver')
    dad = Person.objects.create(name='Dad', city=city)
    dad.children.create(name='Bobby')
    dad.children.create(name='Suzy')

    # Actual test
    dependent_count = dad.count_dependents()

    # Validation
    assert dependent_count == 2, dependent_count

    # End of typical unit test.
    print('Done.')


def setup():
    DB_FILE = NAME + '.db'
    with open(DB_FILE, 'w'):
        pass  # wipe the database
    settings.configure(
        DEBUG=True,
        DATABASES={
            DEFAULT_DB_ALIAS: {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': DB_FILE}},
        LOGGING={'version': 1,
                 'disable_existing_loggers': False,
                 'formatters': {
                    'debug': {
                        'format': '%(asctime)s[%(levelname)s]'
                                  '%(name)s.%(funcName)s(): %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S'}},
                 'handlers': {
                    'console': {
                        'level': 'DEBUG',
                        'class': 'logging.StreamHandler',
                        'formatter': 'debug'}},
                 'root': {
                    'handlers': ['console'],
                    'level': 'WARN'},
                 'loggers': {
                    "django.db": {"level": "WARN"}}})
    app_config = AppConfig(NAME, sys.modules['__main__'])
    apps.populate([app_config])
    django.setup()
    original_new_func = ModelBase.__new__

    @staticmethod
    def patched_new(cls, name, bases, attrs):
        if 'Meta' not in attrs:
            class Meta:
                app_label = NAME
            attrs['Meta'] = Meta
        return original_new_func(cls, name, bases, attrs)
    ModelBase.__new__ = patched_new


def syncdb(model):
    """ Standard syncdb expects models to be in reliable locations.

    Based on https://github.com/django/django/blob/1.9.3
    /django/core/management/commands/migrate.py#L285
    """
    connection = connections[DEFAULT_DB_ALIAS]
    with connection.schema_editor() as editor:
        editor.create_model(model)

main()
