import os
import random
import string
from calendar import timegm
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from graphql_jwt.settings import jwt_settings
from graphql_jwt.utils import exceptions, get_payload

from editions.exceptions import GraphQLError


def jwt_payload(user, context=None):
    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA,
        "token_type": "access",
        "token_class": "AccessToken"
    }
    if jwt_settings.JWT_ALLOW_REFRESH:
        payload["origIat"] = timegm(datetime.utcnow().utctimetuple())

    if jwt_settings.JWT_AUDIENCE is not None:
        payload["aud"] = jwt_settings.JWT_AUDIENCE

    if jwt_settings.JWT_ISSUER is not None:
        payload["iss"] = jwt_settings.JWT_ISSUER

    return payload


def get_user_by_token(token, context=None):
    payload = get_payload(token, context)
    return get_user_by_payload(payload)


def get_user_by_payload(payload):
    user_id = payload.get('user_id')
    if not user_id:
        raise exceptions.JSONWebTokenError(_('Invalid payload'))

    user = get_user_by_id(user_id)
    if user is not None and not user.is_active:
        raise exceptions.JSONWebTokenError(_('User is disabled'))
    return user


def get_user_by_id(user_id):
    User = get_user_model()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
