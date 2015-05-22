from rest_framework import generics

from .mixins import CreateModelMixin, UpdateModelMixin, DeactivateModelMixin


class ListCreateAPIView(CreateModelMixin, generics.ListCreateAPIView):
    """Customized mixin for REST operations retrieve and create."""
    pass


class RetrieveUpdateDestroyAPIView(CreateModelMixin, UpdateModelMixin, DeactivateModelMixin,
                                   generics.RetrieveUpdateDestroyAPIView):
    """Customized mixin for REST operations retrieve, update and destroy."""
    pass
