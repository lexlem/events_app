from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from backend.events.models import Event
from backend.events.serializers import EventSerializer, EventPhotoSerializer


class EventSearchSerializer(serializers.ModelSerializer):
    photos = EventPhotoSerializer(many=True, read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Event
        fields = "__all__"

    def to_native(self, obj):
        if isinstance(obj, Event):
            serializer = EventSerializer(obj)
        else:
            raise Exception("Neither an Event nor User instance!")
        return serializer.data
