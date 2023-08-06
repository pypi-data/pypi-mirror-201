import json
import os

import boto3


class TokenManagerAWS:
    def __init__(self, role_credentials=None):
        """
        Role credentials can be found on assumed role.
            sts_client = boto3.client('sts')
            assumed_role = sts.client.assume_role(RoleArn='', RoleSessionName='')
            role_credentials = assumed_role['Credentials']
        """
        if role_credentials:
            self.client = boto3.client('secretsmanager',
                                       aws_access_key_id=role_credentials['AccessKeyId'],
                                       aws_secret_access_key=role_credentials['SecretAccessKey'],
                                       aws_session_token=role_credentials['SessionToken'])
        else:
            self.client = boto3.client('secretsmanager')

    def get_token(self, domain):
        powerschool_token_secret = self.get_secret(domain)
        return powerschool_token_secret.get('access_token')

    def get_secret(self, domain):
        subdomain = domain.split('.')[0]
        environment = os.getenv('ENVIRONMENT', '')
        powerschool_token_secret_name = f'powerschool_token_{subdomain}_{environment}'
        powerschool_token_secret_value = self.client.get_secret_value(SecretId=powerschool_token_secret_name)
        powerschool_token_secret = json.loads(powerschool_token_secret_value['SecretString'])
        print(json.dumps({
            'token_domain': domain,
            'source': 'Secret Manager',
            'message': f'PowerSchool token for {domain} retrieved from Secret Manager'
        }))
        return powerschool_token_secret
