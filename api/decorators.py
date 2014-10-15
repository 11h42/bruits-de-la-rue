from functools import wraps
import logging

from django.views.decorators.csrf import csrf_exempt

from api.errors import error_codes
from api.http_response import HttpBadRequest, HttpResponseUnauthorized


logger = logging.getLogger('api')


def catch_any_unexpected_exception(view_func):
    """
    Decorator which catches any unexpected exception.
    :param view_func: the view function to protect
    """

    def _wrapped_view(request, *args, **kwargs):
        try:
            logger.info("%s %s %s" % (request.user, request.method, request.path))
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.exception('catch unexpected error in %s api function' % view_func.__name__)
            return HttpBadRequest(10666, error_codes['10666'])

    return _wrapped_view


def b2rue_authenticated(view_func):
    """Decorator which ensures the credentials (user and api key) are corrects."""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request, "user") and request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        return HttpResponseUnauthorized()

    return _wrapped_view
