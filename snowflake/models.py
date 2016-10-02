from pydoc import locate
import uuid

from django.db import models
from django.db.models.fields import UUIDField
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


class SnowflakeManager(models.Manager):

    def get(self, *args, **kwargs):
        flake = models.Manager.get(self, *args, **kwargs)
        klass = locate(flake.model_class)
        return klass.objects.get(pk=flake.id)


class Snowflake(models.Model):

    id = UUIDField(primary_key=True)
    model_class = models.CharField(max_length=255)

    @classmethod
    def add_lookup(cls, obj):
        if not hasattr(obj, 'pk'):
            raise TypeError("Lookups must have a primary key")
        if not isinstance(obj.pk, uuid.UUID):
            raise TypeError("Lookups primary key must be of type uuid.UUID")
        lookup, created = Snowflake.objects.get_or_create(id=obj.pk)
        lookup.model_class = "%s.%s" % (obj.__class__.__module__, obj.__class__.__name__)
        lookup.save()

    objects = SnowflakeManager()

    def __str__(self):
        return "%s: %s" % (self.model_class)


class SnowflakeAbstractModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


@receiver(post_save, dispatch_uid="snowflake_updater")
def update_snowflake(sender, instance, **kwargs):
    if issubclass(instance.__class__, SnowflakeAbstractModel):
        Snowflake.add_lookup(instance)

