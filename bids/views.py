from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

# Create your views here.
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from bids.models import Auction
from bids.serializers import AuctionSerializer
from properties.models import Property
from properties.permissions import IsBuyer


class CreateBidAPI(APIView):
    permission_classes = [IsBuyer]

    class InputSerializer(serializers.Serializer):
        property = serializers.IntegerField()
        amount = serializers.IntegerField()

    def create(self, request):
        if not request.user.is_authenticated:
            return redirect("user-login")
        serializer = self.InputSerializer(data=request.POST)
        if not serializer.is_valid():
            messages.error(request, f"{serializer.errors}")
            return redirect("list-running-auctions")
        validated_data = serializer.validated_data
        current_time = now()
        try:
            property = Property.objects.get(
                is_active=True,
                id=validated_data["property"],
                start_date__lte=current_time,
                closing_date__gte=current_time,
            )
        except Property.DoesNotExist:
            messages.error(request, "Property not found")
            return redirect("list-running-auctions")

        max_bid = (
            property.auction_set.filter(is_active=True).order_by("-amount").first()
        )
        if max_bid and validated_data["amount"] <= max_bid.amount:
            messages.error(
                request, f"Maximum bid is {max_bid.amount}, enter the greater amount..."
            )
            return redirect("list-running-auctions")

        bid = Auction(
            property=property, buyer=request.user, amount=validated_data["amount"]
        )
        try:
            bid.save()
        except ValidationError as error:
            messages.error(request, str(error))
            return redirect("list-running-auctions")

        return redirect("list-running-auctions")
