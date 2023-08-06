# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         8/04/23 7:32
# Project:      Django Plugins
# Module Name:  urls
# Description:
# ****************************************************************
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainSlidingView
from rest_framework_simplejwt.views import TokenRefreshSlidingView

urlpatterns = [
    path("login/", TokenObtainSlidingView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshSlidingView.as_view(), name="token_refresh")
]