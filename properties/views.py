from django.shortcuts import render
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView

from properties.models import Property
from properties.serializers import (
    PropertyDocumentSerializer,
    PropertyGallerySerializer,
    PropertySerializer,
)
from users.serializers import UserSerializer


class ListRunningAuctionsAPI(APIView):
    class OutputSerializer(PropertySerializer):
        seller = UserSerializer()
        gallery = PropertyGallerySerializer(source="propertygallery_set", many=True)
        documents = PropertyDocumentSerializer(source="propertydocument_set", many=True)

        class Meta:
            model = Property
            fields = (
                "id",
                "name",
                "seller",
                "location",
                "base_price",
                "start_date",
                "closing_date",
                "gallery",
                "documents",
            )

    def get(self, request):
        current_time = now()
        properties = (
            Property.objects.filter(
                is_active=True,
                start_date__lte=current_time,
                closing_date__gte=current_time,
            )
            .select_related("seller")
            .prefetch_related("propertygallery_set", "propertydocument_set")
        )
        serializer = self.OutputSerializer(properties, many=True)
        return render(request, "property.html", serializer.data)
