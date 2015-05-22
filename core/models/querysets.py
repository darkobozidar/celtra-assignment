from django.db.models import QuerySet


class ActiveQuerySet(QuerySet):
    def active(self, **kwargs):
        """Filters active records."""

        return self.filter(is_active=True, **kwargs)

    def inactive(self, **kwargs):
        """Filters inactive records."""

        return self.filter(is_active=False, **kwargs)
