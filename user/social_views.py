from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from user.views import SocialLoginView


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

