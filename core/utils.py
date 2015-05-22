from django.core import exceptions as django_exc

from rest_framework import exceptions as rest_exc


def django_exc_to_rest_exc(fn):
    """
    Decorator which catches django ValidationError and converts it to REST ValidationError. In case
    of custom model validations Django ValidationError is raised. REST framework doesn't know how to
    handle this kind of exception, so it has to be converted.
    """

    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except django_exc.ValidationError as exc:
            raise rest_exc.ValidationError(dict(exc))

    return wrapper
