=====
Snowflake
=====

Snowflake is a silly little app that enables models with a UUIDField primary key to be retrieved solely via the PK, without knowing the type. Cause every instance is a special, unique snowflake... get it? Har har.

Quick start
-----------

1. Add "snowflake" to INSTALLED_APPS::

    INSTALLED_APPS = [
        ...
        'snowflake',
    ]

2. Extend SnowflakeAbstractModel in your own model::

    class MyModel(SnowflakeAbstractModel):
        name = models.CharField(max_length=255)

3. Run `python manage.py makemigrations` and `python manage.py migrate` normally.

4. You now have a generic lookup that will return your model instance from only a uuid::

    >>> Snowflake.objects.get(id=SOMEUUID)
    <MyModel: MyModel object>

