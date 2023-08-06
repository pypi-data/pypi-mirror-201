# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         8/04/23 9:58
# Project:      Django Plugins
# Module Name:  serializers
# Description:
# ****************************************************************
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import SlidingToken
from typing import Dict, Any


class EmailTokenObtainSerializer(serializers.TokenObtainSerializer):
    username_field = get_user_model().EMAIL_FIELD
    include_groups = settings.ZB_AUTH_INCLUDE_GROUPS
    include_permissions = settings.ZB_AUTH_INCLUDE_PERMISSIONS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        user = get_user_model().objects.filter(email__iexact=attrs.get(self.username_field)).first()

        if user is None:
            raise AuthenticationFailed(self.error_messages["no_active_account"], "no_active_account")

        authenticate_kwargs = {
            get_user_model().USERNAME_FIELD: user.get_username(),
            "password": attrs.get("password")
        }
        self.user = authenticate(**authenticate_kwargs)
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        return {}


class TokenObtainSlidingSerializer(EmailTokenObtainSerializer):
    token_class = SlidingToken

    @classmethod
    def get_token(cls, user):
        lst_user_roles = list()
        lst_user_permissions = list()
        token = super().get_token(user)
        # Include Groups/Roles
        if cls.include_groups:
            for user_group in user.groups.all():
                lst_user_roles.append(user_group.name)
        else:
            lst_user_roles.append("guest")

        # Include User Permissions
        if cls.include_permissions:
            for user_permission in user.permissions.all():
                lst_user_permissions.append(user_permission.codename)
            token["permissions"] = lst_user_permissions
        token["roles"] = lst_user_roles
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        data = super().validate(attrs)
        token = self.get_token(self.user)
        data["token"] = str(token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data
