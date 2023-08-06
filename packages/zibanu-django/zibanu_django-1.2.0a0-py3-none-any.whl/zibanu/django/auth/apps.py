# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         8/04/23 7:18
# Project:      Django Plugins
# Module Name:  apps
# Description:
# ****************************************************************
from datetime import timedelta
from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ZbDjangoLogging(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "zibanu.django.auth"
    verbose_name = _("Zibanu Auth for Django")
    label = "zb_auth"

    def ready(self):
        # Set default settings for Simple JWT Module
        jwt_default_settings: dict = {
            "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
            "REFRESH_TOKEN_LIFETIME": timedelta(hours=1),
            "ROTATE_REFRESH_TOKEN": False,
            "UPDATE_LAST_LOGIN": False,

            "ALGORITHM": "HS512",
            "SIGNING_KEY": settings.SECRET_KEY,
            "VERIFYING_KEY": "",
            "AUTH_HEADER_TYPES": ("JWT",),

            "USER_ID_FIELD": "id",
            "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.SlidingToken",),

            "SLIDING_TOKEN_OBTAIN_SERIALIZER": "zibanu.django.auth.api.serializers.TokenObtainSlidingSerializer"
        }
        settings.SIMPLE_JWT = getattr(settings, "SIMPLE_JWT", jwt_default_settings)
        settings.ZB_AUTH_INCLUDE_GROUPS = getattr(settings, "ZB_AUTH_INCLUDE_GROUPS", True)
        settings.ZB_AUTH_INCLUDE_PERMISSIONS = getattr(settings, "ZB_AUTH_INCLUDE_PERMISSIONS", False)
