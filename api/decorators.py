from api.errors import error_codes
from api.http_response import HttpBadRequest


def catch_any_unexpected_exception(view_func):
    """
    Decorator which catches any unexpected exception.
    :param view_func: the view function to protect
    """

    def _wrapped_view(request, *args, **kwargs):
        try:
            # todo add logger
            # logger.info("%s %s %s" % (request.user, request.method, request.path))
            return view_func(request, *args, **kwargs)
        except Exception:
            # todo add logger
            # logger.exception('catch unexpected error in %s api function' % view_func.__name__)
            return HttpBadRequest(10666, error_codes['10666'])

    return _wrapped_view
