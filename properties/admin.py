from django.contrib import admin
from django.contrib.admin import ModelAdmin

from properties.models import Property, PropertyDocument, PropertyGallery


@admin.register(Property)
class PropertyAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "seller",
        "base_price",
        "start_date",
        "closing_date",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "seller__email", "location")


@admin.register(PropertyGallery)
class ProfileGalleryAdmin(ModelAdmin):
    list_display = ("id", "property", "file")
    search_fields = ("property__name", "property__location")


@admin.register(PropertyDocument)
class ProfileDocumentAdmin(ModelAdmin):
    list_display = ("id", "property", "document")
    search_fields = ("property__name", "property__location")
