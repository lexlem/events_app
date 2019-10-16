from django.contrib import admin
from .models import Category, Event, EventPhoto, EventCalendar


class EventPhotoInline(admin.StackedInline):
    model = EventPhoto
    extra = 0


class EventAdmin(admin.ModelAdmin):
    model = Event
    inlines = [EventPhotoInline]
    list_display = ("id", "title", "status", 'author')
    list_filter = ("status", "created")
    list_editable = ("status",)


class EventCalendarAdmin(admin.ModelAdmin):
    model = EventCalendar

admin.site.register(Category)
admin.site.register(Event, EventAdmin)
admin.site.register(EventCalendar, EventCalendarAdmin)
