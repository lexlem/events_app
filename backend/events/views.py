import json
from collections import defaultdict
from django.db.models.signals import pre_delete
from rest_framework import mixins, generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from taggit.models import Tag

from backend.permissions import IsOwnerOrReadOnly, IsOwner
from .models import Event, EventPhoto, Category, EventCalendar
from .serializers import (
    EventSerializer,
    EventPhotoSerializer,
    CategorySerializer,
    TagSerializer,
    EventCalendarSerializer,
)


class TagList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.filter(status=Event.PUBLISHED).order_by("-start_datetime")
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def paginate_queryset(self, queryset):
        if (
            self.paginator
            and self.request.query_params.get(self.paginator.page_query_param, None)
            is None
        ):
            return None
        return super().paginate_queryset(queryset)


class EventsCalendarDetail(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    serializer_class = EventCalendarSerializer
    pagination_class = None
    permission_classes = (IsOwner,)

    def get_object(self):
        user = self.request.user
        if not user.is_anonymous:
            return EventCalendar.objects.get(author=user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        user = self.request.user
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        if not user.is_anonymous:
            current_calendar = EventCalendar.objects.get(author=user)
            added_event = Event.objects.get(id=body.get("event"))
            if body.get("type") == "add":
                current_calendar.events.add(added_event)
            else:
                current_calendar.events.remove(added_event)
            current_calendar.save()
        return Response(status=200)


class EventDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Event.DELETED
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventPhotoViewSet(ModelViewSet):
    queryset = EventPhoto.objects.all()
    serializer_class = EventPhotoSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(image=self.request.data.get("image"))
