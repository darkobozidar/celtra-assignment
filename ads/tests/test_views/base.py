from django.utils.six import BytesIO

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class RestViewTestBase():
    """Base class for testing REST views."""

    def _json_to_dict(self, json_bytes):
        """Parses JSON bytes to dictionary."""

        return JSONParser().parse(BytesIO(json_bytes)) if json_bytes else {}

    def _response_to_dict(self, response):
        """Returns response object and response JSON content converted to JSON."""

        return response, self._json_to_dict(response.content)

    def _get_request(self, request_url):
        """Performs GET request and returns response object and response data in dictionary."""

        response = self.client.get(request_url)
        return self._response_to_dict(response)

    def _post_request(self, request_url, data=None):
        """Performs POST request and returns response object and response data in dictionary."""

        response = self.client.post(
            request_url, data=JSONRenderer().render(data) or {}, content_type='application/json'
        )
        return self._response_to_dict(response)

    def _put_request(self, request_url, data=None):
        """Performs PUT request and returns response object and response data in dictionary."""

        response = self.client.put(
            request_url, data=JSONRenderer().render(data) or {}, content_type='application/json'
        )
        return self._response_to_dict(response)

    def _patch_request(self, request_url, data=None):
        """Performs PATCH request and returns response object and response data in dictionary."""

        response = self.client.patch(
            request_url, data=JSONRenderer().render(data) or {}, content_type='application/json'
        )
        return self._response_to_dict(response)

    def _delete_request(self, request_url, data=None):
        """Performs DELETE request and returns response object and response data in dictionary."""

        response = self.client.delete(
            request_url, data=JSONRenderer().render(data) or {}, content_type='application/json'
        )
        return self._response_to_dict(response)

    def _folder_data_dict(self, data_dict=None):
        """Returns dictionary with default folder data merged with provided data."""

        default_dict = {'name': 'Test', 'parent': ''}
        default_dict.update(data_dict or {})
        return default_dict

    def _ad_data_dict(self, data_dict=None):
        """Returns dictionary with default ad data merged with provided data."""

        default_dict = {'name': 'Test', 'ad_url': 'http://www.celtra.com', 'folder': ''}
        default_dict.update(data_dict or {})
        return default_dict
