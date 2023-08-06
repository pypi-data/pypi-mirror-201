from requests import RequestException, Response

from powerschool_client.errors import PowerSchoolDownError


def raise_powerschool_down_error_if_page_unavailable(response: Response):
    if 'powerschool page unavailable' in response.text.lower():
        request_error = RequestException(request=response.request, response=response)
        raise PowerSchoolDownError(request_error)
