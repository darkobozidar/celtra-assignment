from django.db import models

from .managers import ActiveManager
from .. import const


class Model(models.Model):
    """Base class for models."""

    def save(self, *args, **kwargs):
        """Django Model class isn't performing validations when data is saved."""

        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True

    def delete(self, using=None):
        """Prevents deletion from Django ORM."""

        raise Exception(const.MSG_RECORDS_CANT_DELETE)


class IsActiveModel(Model):
    """Base model for retrieving active or inactive records."""

    is_active = models.BooleanField(
        default=True, help_text='Denotes if entity is active or inactive.'
    )

    objects = ActiveManager()

    class Meta:
        abstract = True

    def activate(self):
        """Activates record."""

        self.is_active = True
        self.save()

    def deactivate(self):
        """Deactivates record."""

        self.is_active = False
        self.save()


class BaseTimeModel(Model):
    """Base model that provides self-updating 'time_created' and 'time_modified' fields"""

    time_created = models.DateTimeField(
        auto_now_add=True, help_text='Time when record was created.'
    )
    time_modified = models.DateTimeField(
        auto_now=True, help_text='Time when record was updated.'
    )

    class Meta:
        abstract = True
