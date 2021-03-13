from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class EmailValidateMixin:
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('User with given email already exists'))
        return value
