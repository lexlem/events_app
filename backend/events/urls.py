# -*- coding: utf-8 -*-
from django.urls import path, include

from .views import (
    TagList,
    CategoryList,
    EventDetail,
    EventList,
    EventPhotoViewSet,
    EventsCalendarDetail,
)

urlpatterns = [
    path("categories/", CategoryList.as_view(), name="categories-list"),
    path("tags/", TagList.as_view(), name="tags-list"),
    path("events/", EventList.as_view(), name="event-list"),
    path("events/<int:pk>", EventDetail.as_view(), name="event-detail"),
    path(
        "calendar-events/",
        EventsCalendarDetail.as_view(),
        name="events-calendar-detail",
    ),
    path(
        "events/photos/",
        EventPhotoViewSet.as_view({"get": "list", "post": "create"}),
        name="photo-list",
    ),
    path(
        "events/photos/<int:pk>",
        EventPhotoViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="photo-detail",
    ),
]
