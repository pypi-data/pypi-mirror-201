from typing import Dict, List
from urllib.parse import urlparse

import requests
from requests import RequestException

from powerschool_client.client_helper import raise_powerschool_down_error_if_page_unavailable
from powerschool_client.errors import PowerSchoolClientError, EntityNotFoundError
from powerschool_client.tokens import ITokenManager


class PowerSchoolClient:
    """
    Client for interacting with PowerSchool REST API
    """

    def __init__(self, token_manager: ITokenManager, expansions: Dict[str, List[str]] = None):
        self.token_manager = token_manager

        if expansions is not None:
            self.expansions = expansions
        else:
            self.expansions = {
                'STUDENTS': ['demographics', 'addresses', 'alerts', 'phones', 'school_enrollment', 'ethnicity_race',
                             'contact', 'contact_info', 'initial_enrollment', 'schedule_setup', 'fees', 'lunch'],
                'SECTIONS': ['term'],
                'TEACHERS': ['addresses', 'emails', 'phones', 'school_affiliations'],
            }

    def _headers(self, domain: str):
        access_token = self.token_manager.get_token(domain)

        return {
            'Authorization': f"Bearer {access_token}",
            'Accept': 'application/json'
        }

    def get(self, url, entity_type=None):
        if entity_type and entity_type in self.expansions:
            complete_url = url + '?expansions=' + \
                           ','.join(self.expansions[entity_type])
        else:
            complete_url = url

        domain = urlparse(url).hostname
        response = requests.get(complete_url, headers=self._headers(domain))

        try:
            response.raise_for_status()
        except RequestException as error:
            if error.response.status_code == 404:
                raise EntityNotFoundError(error)
            else:
                raise PowerSchoolClientError(error)

        raise_powerschool_down_error_if_page_unavailable(response)

        return response.json()

    def post(self, url, data, check_body_has_error=True):
        domain = urlparse(url).hostname
        response = requests.post(url, headers=self._headers(domain), json=data)

        try:
            response.raise_for_status()
        except RequestException as error:
            raise PowerSchoolClientError(error)

        raise_powerschool_down_error_if_page_unavailable(response)

        if response.text == "":
            return None

        response_body = response.json()

        # PowerSchool sends us a 200 message with a status == ERROR field,
        # handle that situation as well
        if check_body_has_error:

            # If there is only 1 result, PowerSchool will return an object. But if
            # there are more, the API will return a list. Ensure that we iterate
            # over a list
            if "results" in response_body and "result" in response_body["results"]:
                results = response_body['results']['result']
                results = results if isinstance(results, list) else [results]

                for result in results:
                    if result['status'] == 'ERROR':
                        raise PowerSchoolClientError(response_body)

        return response_body

    def put(self, url, data):
        domain = urlparse(url).hostname
        response = requests.put(url, headers=self._headers(domain), json=data)

        try:
            response.raise_for_status()
        except RequestException as error:
            raise PowerSchoolClientError(error)

        raise_powerschool_down_error_if_page_unavailable(response)

        if response.text == "":
            return None

        response_body = response.json()

        return response_body

    def power_query(self, url, data):
        domain = urlparse(url).hostname
        headers = self._headers(domain)
        headers["Content-Type"] = "application/json"

        response = requests.post(url, headers=headers, json=data)

        try:
            response.raise_for_status()
        except RequestException as error:
            raise PowerSchoolClientError(error)

        raise_powerschool_down_error_if_page_unavailable(response)

        response_body = response.json()

        if "record" not in response_body:
            response_body["record"] = []

        return response_body

    def delete(self, url):
        domain = urlparse(url).hostname
        response = requests.delete(url, headers=self._headers(domain))

        try:
            response.raise_for_status()
        except RequestException as error:
            if error.response.status_code != 404:
                raise PowerSchoolClientError(error)

        raise_powerschool_down_error_if_page_unavailable(response)

        return
