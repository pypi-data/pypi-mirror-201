import random
import string
from social_core.backends.oauth import BaseOAuth1

class MagentoOAuth1(BaseOAuth1):
    name = 'magento'
    ID_KEY = 'id'
    REQUEST_TOKEN_URL = 'https://docentedigital.app/oauth/token/request'
    AUTHORIZATION_URL = 'https://docentedigital.app/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://docentedigital.app/oauth/token/access'
    USER_DATA_URL = 'https://docentedigital.app/rest/V1/customers/me'

    def get_user_details(self, response):
        """Extract user details from the response object."""
        return {
            'email': response.get('email', ''),
            'first_name': response.get('first_name', ''),
            'last_name': response.get('last_name', ''),
        }

    def user_data(self, access_token, *args, **kwargs):
        """Load user data from the remote service."""
        headers = {
            'oauth_consumer_key': self.setting('KEY'),
            'oauth_nonce': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32)),
            'oauth_signature_method': 'HMAC-SHA1',
        }
        response = self.get_json(self.USER_DATA_URL, headers=headers, auth=self.oauth_auth(access_token))
        return response
