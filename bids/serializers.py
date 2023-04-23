from rest_framework import serializers

from bids.models import Auction


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ("id", "buyer", "property", "amount", "date_created")
