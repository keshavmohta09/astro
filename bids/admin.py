from django.contrib import admin
from django.contrib.admin import ModelAdmin

from bids.models import Auction


@admin.register(Auction)
class AuctionAdmin(ModelAdmin):
    list_display = ("id", "property", "buyer", "amount", "is_active", "date_created")
    list_filter = ("is_active",)
    search_fields = ("property__name", "buyer__email", "amount")
