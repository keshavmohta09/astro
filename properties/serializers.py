from rest_framework import serializers

from properties.models import Property, PropertyDocument, PropertyGallery


class PropertySerializer(serializers.ModelSerializer):
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
        )


class PropertyGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyGallery
        fields = ("id", "property", "file")


class PropertyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDocument
        fields = ("id", "property", "document")
