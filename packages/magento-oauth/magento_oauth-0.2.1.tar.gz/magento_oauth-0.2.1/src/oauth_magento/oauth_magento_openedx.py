from social_core.backends.oauth import BaseOAuth2

class MagentoOAuth2(BaseOAuth2):
    name = 'magento'
    ID_KEY = 'id'
    AUTHORIZATION_URL = 'https://docentedigital.app/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://docentedigital.app/oauth/token'
    USER_DATA_URL = 'https://docentedigital.app/oauth/userinfo'

    def get_user_details(self, response):
        """Extract user details from the response object."""
        return {
            'email': response.get('email', ''),
            'first_name': response.get('first_name', ''),
            'last_name': response.get('last_name', ''),
        }

    def user_data(self, access_token, *args, **kwargs):
        """Load user data from the remote service."""
        headers = {'Authorization': 'Bearer ' + access_token}
        response = self.get_json(self.USER_DATA_URL, headers=headers)
        return response