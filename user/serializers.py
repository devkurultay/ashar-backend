from django.http import HttpRequest
from django.contrib.auth import get_user_model, authenticate
from allauth.socialaccount.helpers import complete_social_login

from django.utils.translation import gettext_lazy as _
from requests import HTTPError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from user.mixins import EmailValidateMixin
from user.send_mail import send_activation_mail, send_confirmation_email

from allauth.account import app_settings as allauth_settings

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'is_verified')

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        return representation


class RegisterSerializer(EmailValidateMixin, serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ActivationSerializer(EmailValidateMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'activation_code', )


    def validate_activation_code(self, value):
        if not User.objects.filter(activation_code=value).exists():
            raise serializers.ValidationError(_('Wrong activation code'))
        return value

    def validate(self, validated_data):
        email = validated_data.get('email')
        activation_code = validated_data.get('activation_code')
        if not User.objects.filter(email=email, activation_code=activation_code).exists():
            raise serializers.ValidationError(_('User not found'))
        return validated_data

    def activate(self):
        email = self.validated_data.get('email')
        activation_code = self.validated_data.get('activation_code')
        user = User.objects.get(email=email, activation_code=activation_code)
        user.activate_with_code(activation_code)


class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, validated_data):
        email = validated_data.get('email')

        password = validated_data.pop('password', None)
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('User not found'))
        user = authenticate(username=email, password=password)
        if user and user.is_verified:
            refresh = self.get_token(user)
            validated_data['refresh'] = str(refresh)
            validated_data['access'] = str(refresh.access_token)
            validated_data['user'] = UserSerializer(instance=user).data
        return validated_data


class ResendActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', )

    def validate_email(self, email):
        if not User.objects.filter(email=email, is_active=False).exists():
            raise serializers.ValidationError(_('Account for activation not found'))
        return email

    def send_activation(self):
        email = self.validated_data.get('email')
        try:
            user = User.objects.get(email=email, is_active=False)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('User not found'))
        user.create_activation_code()
        send_activation_mail(user)


class LostPasswordSerializer(EmailValidateMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', )

    def send_activation(self):
        email = self.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('User not found'))
        user.create_activation_code()
        send_confirmation_email(user)


class CreateNewPasswordSerializer(EmailValidateMixin, serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, read_only=True, )
    password_confirmation = serializers.CharField(min_length=6, read_only=True, )

    class Meta:
        model = User
        fields = ('email', 'activation_code', 'password', 'password_confirmation')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirmation = validated_data.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError(_('Passwords don\'t match'))
        email = validated_data.get('email')
        activation_code = validated_data.get('activation_code')
        if not User.objects.filter(email=email, activation_code=activation_code).exists():
            raise serializers.ValidationError(_('User not found'))
        return validated_data

    def set_new_password(self):
        user = User.objects.get(email=self.validated_data.get('email'))
        user.activate_with_code(self.validated_data.get('activation_code'))
        user.set_password(self.validated_data.get('password'))


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, validated_data):
        new_password = validated_data.get('new_password')
        new_password_confirm = validated_data.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError(_('Passwords don\'t match'))
        return validated_data


class SocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def _get_request(self):
        request = self.context.get('request')
        if not isinstance(request, HttpRequest):
            request = request._request
        return request

    def get_social_login(self, adapter, app, token, response):
        request = self._get_request()
        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token
        return social_login

    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                _("View is not defined, pass it as a context variable")
            )

        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError(_("Define adapter_class in view"))

        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)
        if attrs.get('access_token'):
            access_token = attrs.get('access_token')
        elif attrs.get('code'):
            self.callback_url = getattr(view, 'callback_url', None)
            self.client_class = getattr(view, 'client_class', None)

            if not self.callback_url:
                raise serializers.ValidationError(
                    _("Define callback_url in view")
                )
            if not self.client_class:
                raise serializers.ValidationError(
                    _("Define client_class in view")
                )

            code = attrs.get('code')

            provider = adapter.get_provider()
            scope = provider.get_scope(request)
            client = self.client_class(
                request,
                app.client_id,
                app.secret,
                adapter.access_token_method,
                adapter.access_token_url,
                self.callback_url,
                scope
            )
            token = client.get_access_token(code)
            access_token = token['access_token']

        else:
            raise serializers.ValidationError(
                _("Incorrect input. access_token or code is required."))

        social_token = adapter.parse_token({'access_token': access_token})
        social_token.app = app

        try:
            login = self.get_social_login(adapter, app, social_token, access_token)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_("Incorrect value"))

        if not login.is_existing:
            if allauth_settings.UNIQUE_EMAIL:
                account_exists = get_user_model().objects.filter(
                    email=login.user.email,
                ).exists()
                if account_exists:
                    raise serializers.ValidationError(
                        _("User is already registered with this e-mail address.")
                    )

            login.lookup()
            login.save(request, connect=True)
        if login.account.user:
            login.account.user.is_verified = True
            login.account.user.is_active = True
            login.account.user.save()

        refresh = self.get_token(login.account.user)
        attrs['user'] = {
            "email": login.account.user.email,
            "first_name": login.account.user.first_name,
        }
        if login.account.user.is_verified:
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs
