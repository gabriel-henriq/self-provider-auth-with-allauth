import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2LoginView,
    OAuth2CallbackView,
)
from .provider import CustomProvider
from django.conf import settings


class CustomAdapter(OAuth2Adapter):
    provider_id = CustomProvider.id

    access_token_url = f"{settings.OAUTH_SERVER_BASEURL}/api/oauthtoken"
    profile_url = f"{settings.OAUTH_SERVER_BASEURL}/api/useraccount/"

    authorize_url = f"{settings.OAUTH_SERVER_BASEURL}/authorization"

    def complete_login(self, request, app, token, **kwargs):
        headers = {
            "Authorization": f"Bearer {token.token}",
            "Accept": "application/json",
        }
        useremail = kwargs["response"]["useremail"]
        resp = requests.get(
            self.profile_url + f"{useremail}?type=email", headers=headers
        )
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(CustomAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CustomAdapter)
