import datetime
from typing import Dict, List
from dataclasses import dataclass
import requests
from requests.auth import HTTPBasicAuth


@dataclass
class TokenCredential:
    """
    Holds client credentials to be passed into the default token manager
    """
    domain: str
    client_id: str
    client_secret: str


@dataclass
class Token:
    """
    Holds oauth token and expiration information
    """
    access_token: str
    expires_at: datetime


class ITokenManager:
    def get_token(self, domain: str) -> str:
        raise NotImplementedError()


class TokenManager(ITokenManager):
    """
    Retrieves tokens from PowerSchool's API.
    A default in-memory implementation is provided, but may be replaced with something
    that implements one of various storage/caching strategies for the tokens.
    """

    def __init__(self, credentials: Dict[str, TokenCredential]):
        self.credentials = credentials
        self.tokens: Dict[str, Token] = {}

    def get_token(self, domain: str):
        """
        For a given powerschool instance domain name, return a valid token
        """
        domain_invalid = domain not in self.tokens

        expired = False
        if not domain_invalid:
            expired = self.tokens[domain].expires_at < datetime.datetime.now()

        # if no token, or token is expired, go get a new one from PowerSchool
        # NOTE: this implementation has been known to cause HTTP 429 response codes depending on how it is used
        if domain_invalid or expired:
            self.tokens[domain] = self._get_token_from_powerschool(domain)

        return self.tokens[domain].access_token

    def _get_token_from_powerschool(self, domain):
        basic_auth = HTTPBasicAuth(username=self.credentials[domain].client_id,
                                   password=self.credentials[domain].client_secret)
        response = requests.post(f"https://{domain}/oauth/access_token/", auth=basic_auth,
                                 data={'grant_type': 'client_credentials'})
        response.raise_for_status()
        token_dict = response.json()
        expires_in = datetime.timedelta(seconds=int(token_dict['expires_in']))
        expiry_time = datetime.datetime.utcnow() + expires_in
        token_dict["expires_at"] = expiry_time
        token_dict.pop("expires_in")
        return Token(**token_dict)
