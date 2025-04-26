from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'latitude', 'longitude']


    def validate_latitude(self, value):
        """
        Validates that the latitude is within the appropriate range (-90 to 90).
        """
        if value < -90 or value > 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90."
            )
        return value

    def validate_longitude(self, value):
        """
        Validates that the longitude is within the appropriate range (-180 to 180).
        """
        if value < -180 or value > 180:
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180."
            )
        return value

    def validate_street(self, value):
        """
        Validates that the street field is not empty.
        """
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Street cannot be empty.")
        return value

    def validate_city(self, value):
        """
        Validates that the city field is not empty.
        """
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("City cannot be empty.")
        return value
