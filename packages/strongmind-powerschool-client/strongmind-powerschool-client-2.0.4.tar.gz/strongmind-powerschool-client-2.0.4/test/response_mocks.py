import base64
from urllib.parse import urlparse

import responses
from requests import Request


def add_authenticated_payload(responses_mock: responses.RequestsMock,
                              request_type: str,
                              url: str,
                              body: str,
                              auth,
                              status: int = 200):
    if type(auth) is dict:
        auth = base64.b64encode(f"{auth['user']}:{auth['password']}".encode()).decode()
        auth = f"Basic {auth}"

    def request_callback(request: Request):
        headers = {'content-type': 'application/json'}
        if 'Authorization' not in request.headers or request.headers['Authorization'] != auth:
            return 401, headers, "{}"
        else:
            return status, headers, body

    responses_mock.add_callback(
        request_type,
        url,
        callback=request_callback
    )


def add_powerschool_down_payload(responses_mock: responses.RequestsMock,
                                 request_type: str,
                                 url: str,
                                 auth,
                                 redirect_url: str = None):
    parsed_url = urlparse(url)
    if not redirect_url:
        redirect_url = f"https://message.powerschool.com/?server={parsed_url.hostname}"

    def redirect_callback(request: Request):
        headers = {
            'content-type': 'application/json',
            'location': redirect_url,
            'Authorization': auth
        }
        return 302, headers, ""

    responses_mock.add_callback(
        request_type,
        url,
        callback=redirect_callback
    )

    def down_callback(request: Request):
        headers = {
            'content-type': 'application/html'
        }
        return 200, headers, "<html>\r\n<head>\r\n<title>PowerSchool page unavailable</title>\r\n</head>\r\n<body></body>\r\n</html>"

    responses_mock.add_callback(
        'GET',
        redirect_url,
        callback=down_callback
    )
