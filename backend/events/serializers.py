from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from taggit.models import Tag

from backend.events.models import (
    Category,
    Event,
    EventPhoto,
    EventCalendar,
)
from backend.geo.models import Address
from backend.geo.serializers import AddressSerializer


class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPhoto
        fields = ("event", "image")


class EventSerializer(TaggitSerializer, serializers.ModelSerializer):
    photos = EventPhotoSerializer(many=True, read_only=True)
    location = AddressSerializer()
    tags = TagListSerializerField()

    class Meta:
        model = Event
        fields = "__all__"

    def create(self, validated_data):
        location = validated_data.pop("location")
        validated_data["location"] = Address.objects.create_from_dict(
            data={
                "raw": location.get("raw", ""),
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
            }
        )
        to_be_tagged, validated_data = self._pop_tags(validated_data)
        tag_object = super(TaggitSerializer, self).create(validated_data)
        return self._save_tags(tag_object, to_be_tagged)

    def update(self, instance, validated_data):
        to_be_tagged, validated_data = self._pop_tags(validated_data)
        tag_object = super(TaggitSerializer, self).update(instance, validated_data)
        return self._save_tags(tag_object, to_be_tagged)

    def _save_tags(self, tag_object, tags):
        for key in tags.keys():
            tag_values = tags.get(key)
            getattr(tag_object, key).set(*tag_values)
        return tag_object

    def _pop_tags(self, validated_data):
        to_be_tagged = {}
        for key in self.fields.keys():
            field = self.fields[key]
            if isinstance(field, TagListSerializerField):
                if key in validated_data:
                    to_be_tagged[key] = validated_data.pop(key)
        return (to_be_tagged, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "active_events_count")
        read_only_fields = ("title",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("slug", "name")
        read_only_fields = ("name",)


class EventCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCalendar
        fields = ("author", "events")
    events = EventSerializer(many=True)
