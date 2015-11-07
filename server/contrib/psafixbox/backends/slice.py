"""
Slice OAuth2 backend, docs at:
    http://python-social-auth.readthedocs.org/en/latest/backends/implementation.html
"""
import base64

from social.backends.oauth import BaseOAuth2


class SliceOAuth2(BaseOAuth2):
    name = 'slice'
    ID_KEY = 'id'
    AUTHORIZATION_URL = 'https://api.slice.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://api.slice.com/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REFRESH_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token'),
    ]

    def auth_headers(self):
        auth_str = '{0}:{1}'.format(*self.get_key_and_secret())
        b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
        return {
            'Authorization': 'Basic {0}'.format(b64_auth_str)
        }

    def get_user_details(self, response):
        """Return user details from Slice account"""
        fullname, first_name, last_name = self.get_user_names(
            response.get('display_name')
        )
        return {'username': response.get('id'),
                'email': response.get('email'),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://api.slice.com/api/v1/users/self',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        )

    def refresh_token_params(self, token, redirect_uri=None, *args, **kwargs):
        params = super(SliceOAuth2, self).refresh_token_params(token)
        return params
