from django.contrib import admin

from .models import Address, City


class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ("raw", "importance_index")
    list_filter = ("importance_index",)
    list_editable = ("importance_index",)


admin.site.register(Address)
admin.site.register(City, CityAdmin)
