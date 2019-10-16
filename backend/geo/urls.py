# -*- coding: utf-8 -*-
from django.urls import path, include

from .views import CityList


urlpatterns = [
    path('cities/', CityList.as_view(), name='cities-list'),
]
