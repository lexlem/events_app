# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import get_user_model

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill
from taggit.managers import TaggableManager

from backend.geo.models import Address

UserModel = get_user_model()


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=400)
    position = models.SmallIntegerField(verbose_name="Позиция", default=0)

    def __str__(self):
        return "%s" % self.title

    @property
    def active_events_count(self):
        return self.events.filter(status="published").order_by("-id").count()


class Event(models.Model):
    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REJECTED = "rejected"
    DELETED = "deleted"

    STATUSES = (
        (DRAFT, "Черновик"),
        (PUBLISHED, "Опубликовано"),
        (ARCHIVED, "В архиве"),
        (REJECTED, "Отклонено"),
        (DELETED, "Удалено"),
    )

    FRIENDS = "friends"
    EVERYONE = "everyone"

    VISIBILITY_CHOICES = ((FRIENDS, "Только для друзей"), (EVERYONE, "Для всех"))

    author = models.ForeignKey(
        UserModel,
        verbose_name="Автор",
        related_name="events",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    author_name = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(verbose_name="Название", max_length=35)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="events",
        on_delete=models.DO_NOTHING,
    )
    status = models.CharField("Статус", max_length=30, choices=STATUSES, default=DRAFT)
    description = models.TextField("Описание", max_length=250, blank=True, null=True)
    start_datetime = models.DateTimeField("Дата и время начала", blank=True, null=True)
    end_datetime = models.DateTimeField("Дата и время окончания", blank=True, null=True)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    social_links = JSONField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    visibility = models.CharField(
        verbose_name="Отображение",
        max_length=30,
        choices=VISIBILITY_CHOICES,
        default=FRIENDS,
    )
    location = models.ForeignKey(
        Address, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    def __str__(self):
        return "%s" % self.title


class EventPhoto(models.Model):
    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    event = models.ForeignKey(
        Event,
        verbose_name="Событие",
        related_name="photos",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(verbose_name="Оригинал", upload_to=settings.UPLOAD_URL)
    thumbnail = ImageSpecField(
        source="image", processors=[ResizeToFit(105, 105)], options={"quality": 100}
    )
    img_512x512 = ImageSpecField(
        source="image", processors=[ResizeToFill(512, 512)], options={"quality": 70}
    )
    position = models.IntegerField(verbose_name="Позиция", default=1, blank=False)
    title = models.TextField(verbose_name="Заголовок", blank=True, null=True)

    def __str__(self):
        if self.image:
            return os.path.basename(self.image.url)
        else:
            return ""

class EventCalendar(models.Model):
    class Meta:
        verbose_name = "Календарь"
        verbose_name_plural = "Календари"

    author = models.OneToOneField(
        UserModel,
        verbose_name="Владелец",
        related_name="calendar",
        on_delete=models.DO_NOTHING
    )
    events = models.ManyToManyField(Event)

    def __str__(self):
        return "%s" % self.author
