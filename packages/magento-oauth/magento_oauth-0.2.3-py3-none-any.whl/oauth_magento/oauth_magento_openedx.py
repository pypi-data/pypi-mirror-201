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
            'first_name': response.get('firstname', ''),
            'last_name': response.get('lastname', ''),
        }

    def user_data(self, access_token, access_token_secret, *args, **kwargs):
        """Load user data from the remote service."""
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
        }
        response = self.get_json(self.USER_DATA_URL, headers=headers)
        return response
