from django.core.exceptions import ValidationError
from django.shortcuts import render

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

    def get(self, request):
        serializer = self.InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=400)
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
            return Response(data="Property not found", status=404)

        max_bid = (
            property.auction_set.filter(is_active=True).order_by("-amount").first()
        )
        if max_bid and validated_data["amount"] <= max_bid.amount:
            return Response(
                data=f"Maximum bid is {max_bid.amount}, enter the greater amount...",
                status=400,
            )

        bid = Auction(
            property=property, buyer=request.user, amount=validated_data["amount"]
        )
        try:
            bid.save()
        except ValidationError as error:
            return Response(data=error, status=400)

        return Response(
            data=AuctionSerializer(instance=bid).data,
            status=201,
        )
