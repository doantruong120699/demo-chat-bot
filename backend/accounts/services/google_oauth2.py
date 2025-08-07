"""
Google OpenId, OAuth2, OAuth1, Google+ Sign-in backends, docs at:
    https://python-social-auth.readthedocs.io/en/latest/backends/google.html
"""

import requests

from django.conf import settings


class GoogleOAuth2:
    def get_user_details(self, access_token):
        response = requests.get(
            settings.GOOGLE_OAUTH2_USER_INFO_URL,
            headers={
                "Authorization": "Bearer %s" % access_token,
            },
        )
        response = response.json()
        return response
