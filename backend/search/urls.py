# -*- coding: utf-8 -*-
from django.urls import path

from .views import EventSearchList


urlpatterns = [
    path('search/', EventSearchList.as_view(), name="search"),
]
