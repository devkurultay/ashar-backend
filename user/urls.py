from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .social_views import GoogleLogin, FacebookLogin
from .views import (RegisterView, ActivationView, LoginView, ResendActivationCodeView,
                                          CreateNewPasswordView)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view(), name='activate_account'),
    path('login/', LoginView.as_view()),
    path('refresh_token/', TokenRefreshView.as_view()),
    path('resend_activation/', ResendActivationCodeView.as_view()),
    path('forgot_password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('change_password/', CreateNewPasswordView.as_view(), name='change_password'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('facebook/', FacebookLogin.as_view(), name='facebook_login'),
]
