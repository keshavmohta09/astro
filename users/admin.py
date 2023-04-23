from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import Profile, User


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("id", "email", "is_seller", "is_buyer")
    list_filter = ("is_seller", "is_buyer")
    search_fields = ("email", "first_name", "last_name")


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("id", "user", "pan_card", "aadhar_card")
    list_filter = ("user__is_seller", "user__is_buyer")
    search_fields = ("user__email", "aadhar_card", "pan_card", "address")
