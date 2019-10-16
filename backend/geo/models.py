# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models


class AddressManager(models.Manager):
    def create_from_dict(self, data):
        addr, _ = self.get_or_create(
            raw=data.get("raw"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude")
        )
        return addr


class Address(models.Model):
    raw = models.CharField(max_length=300, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    objects = AddressManager()

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return "-".join([str(self.id), self.raw])


class City(models.Model):
    raw = models.CharField(max_length=300, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    importance_index = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.raw
