from django.db import models

from .querysets import ActiveQuerySet


class ActiveManager(models.Manager.from_queryset(ActiveQuerySet)):
    """Manager for active/inactive records."""

    use_for_related_fields = True
