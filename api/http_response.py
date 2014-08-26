import json

from django.http import HttpResponse


class HttpCreated(HttpResponse):
    status_code = 201

    def __init__(self, *args, **kwargs):
        location = kwargs.pop('location', '')

        super(HttpCreated, self).__init__(*args, **kwargs)
        self['Location'] = location


class HttpNoContent(HttpResponse):
    status_code = 204


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class HttpMethodNotAllowed(HttpResponse):
    status_code = 405


class HttpBadRequest(HttpResponse):
    status_code = 400

    def __init__(self, error_code, error_message, extra=None):
        """Constructor for init HTTPBadRequest
        can add an extra dictionary to customise the json return"""
        super(HttpBadRequest, self).__init__(content_type="application/json")
        return_dict = {
            "code": error_code,
            "message": error_message,
        }
        if extra:
            return_dict.update(extra)

        self.content = json.dumps(return_dict)