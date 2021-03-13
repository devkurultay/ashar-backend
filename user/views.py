from allauth.account.adapter import get_adapter
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsOwnerOrReadOnly
from .serializers import (RegisterSerializer, LoginSerializer, ResendActivationSerializer,
                          LostPasswordSerializer, SocialLoginSerializer,
                          ChangePasswordSerializer)
from user.send_mail import send_confirmation_email

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActivationView(View):
    """
    Активация почты пользователя
    """
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.is_verified = True
            user.activation_code = ''
            user.save()
            return render(request, 'account/index.html', {})
        except User.DoesNotExist:
            return render(request, 'account/link_exp.html', {})


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class ResendActivationCodeView(APIView):
    def get(self, request):
        serializer = ResendActivationSerializer(request.query_params)
        if serializer.is_valid(raise_exception=True):
            serializer.send_activation()
            return Response({'status': 'success'})


class LostPasswordRequestView(APIView):
    def post(self, request):
        serializer = LostPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_activation()
            return Response({'status': 'success'})


class CreateNewPasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsOwnerOrReadOnly, )

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialLoginView(LoginView):
    serializer_class = SocialLoginSerializer

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)
