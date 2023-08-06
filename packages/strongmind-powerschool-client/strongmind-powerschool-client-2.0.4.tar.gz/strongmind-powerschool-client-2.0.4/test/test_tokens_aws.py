import json
import os
import unittest

import boto3
import botocore
from botocore.client import BaseClient
from expects import expect, equal
from faker import Faker
from mockito import when, mock, verify, unstub

from powerschool_client.tokens_aws import TokenManagerAWS

fake = Faker()


class AWSSecretsManagerClientStub:
    def get_secret_value(self, SecretId=None): pass


class TestTokenManagerAWS(unittest.TestCase):
    def setUp(self):
        self.boto_client = mock(AWSSecretsManagerClientStub)
        when(boto3).client('secretsmanager').thenReturn(self.boto_client)
        self.token_manager = TokenManagerAWS()

    def tearDown(self):
        unstub()

    def test_creates_client_from_role_credentials(self):
        # Arrange
        when(boto3).client(...)
        role_credentials = {
            'AccessKeyId': fake.random_int(),
            'SecretAccessKey': fake.hexify('^' * 12),
            'SessionToken': fake.hexify('^' * 12)
        }

        # Act
        TokenManagerAWS(role_credentials)

        # Assert
        verify(boto3, times=1).client(
            'secretsmanager',
            aws_access_key_id=role_credentials['AccessKeyId'],
            aws_secret_access_key=role_credentials['SecretAccessKey'],
            aws_session_token=role_credentials['SessionToken'])

    def test_gets_token_from_aws_secrets_manager(self):
        subdomain = fake.domain_word()
        domain = f'{subdomain}.{fake.domain_name()}'
        environment = fake.word()
        expected_secret_name = f'powerschool_token_{subdomain}_{environment}'
        expected_token = fake.hexify('^' * 12)
        when(os).getenv('ENVIRONMENT', '').thenReturn(environment)
        when(self.boto_client).get_secret_value(...).thenReturn({
            'SecretString': json.dumps({
                'access_token': expected_token
            })
        })

        token = self.token_manager.get_token(domain)

        verify(self.boto_client, times=1).get_secret_value(SecretId=expected_secret_name)
        expect(token).to(equal(expected_token))

    def test_gets_secret_from_aws_secrets_manager(self):
        subdomain = fake.domain_word()
        domain = f'{subdomain}.{fake.domain_name()}'
        environment = fake.word()
        expected_secret_name = f'powerschool_token_{subdomain}_{environment}'
        expected_secret = {
            'client_id': fake.uuid4(),
            'client_secret': fake.uuid4(),
            'access_token': fake.uuid4(),
            'expires_at': fake.iso8601()
        }
        when(os).getenv('ENVIRONMENT', '').thenReturn(environment)
        when(self.boto_client).get_secret_value(...).thenReturn({
            'SecretString': json.dumps(expected_secret)
        })

        secret = self.token_manager.get_secret(domain)

        verify(self.boto_client, times=1).get_secret_value(SecretId=expected_secret_name)
        expect(secret).to(equal(expected_secret))
