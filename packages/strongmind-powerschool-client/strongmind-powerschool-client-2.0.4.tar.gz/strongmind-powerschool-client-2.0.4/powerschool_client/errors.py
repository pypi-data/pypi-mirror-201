from requests import RequestException

POWERSCHOOL_DEPENDENCY_NAME = 'PowerSchool'


class PowerSchoolClientError(Exception):
    """A generic error class when the PowerSchool API has returned an error."""
    dependency_name = POWERSCHOOL_DEPENDENCY_NAME

    def __init__(self, request_error: RequestException = None):
        if request_error:
            if hasattr(request_error, "request"):
                self.request = request_error.request
            if hasattr(request_error, "response"):
                self.response = request_error.response


class EntityNotFoundError(PowerSchoolClientError):
    """An Entity is not found in the PowerSchool API"""


class PowerSchoolDownError(PowerSchoolClientError):
    """An error when PowerSchool is down and returns an HTML payload"""
