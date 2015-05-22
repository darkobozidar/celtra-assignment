from rest_framework import mixins

from ..utils import django_exc_to_rest_exc


class CreateModelMixin(mixins.CreateModelMixin):
    """Custom read model mixin for REST."""

    @django_exc_to_rest_exc
    def perform_create(self, serializer):
        """Decorator converts django ValidationError to REST ValidationError."""

        super().perform_create(serializer)


class UpdateModelMixin(mixins.UpdateModelMixin):
    """Custom update model mixin for REST."""

    @django_exc_to_rest_exc
    def perform_update(self, serializer):
        """Decorator converts django ValidationError to REST ValidationError."""

        super().perform_update(serializer)


class DeactivateModelMixin(mixins.DestroyModelMixin):
    """Custom delete model mixin for REST."""

    @django_exc_to_rest_exc
    def perform_destroy(self, instance):
        """
        Instead of deleting instance it deactivates it. Decorator converts django ValidationError
        to REST ValidationError.
        """

        instance.deactivate()
