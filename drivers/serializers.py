from rest_framework import serializers
from .models import Driver
from addresses.models import Address
from addresses.serializers import AddressSerializer
from django.contrib.auth.models import User

class DriverSerializer(serializers.ModelSerializer):
    current_address = AddressSerializer()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Driver
        fields = ['id', 'user', 'current_address', 'is_available']

    def to_representation(self, instance):
        # Call the to_representation method of the base class to get the standard representation
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username if instance.user else None
        return representation

    def create(self, validated_data):
        """
        Creates a new Driver instance. Extracts the current address from the
        validated data, creates the Address instance, and assigns it to the Driver.
        """
        # Extract the address from the validated data set
        address_data = validated_data.pop('current_address')

        # Create the address
        address = Address.objects.create(**address_data)

        # Check if a Driver already exists for the user
        user = validated_data.get('user')
        driver = Driver.objects.filter(user=user).first()

        if driver:
            return driver
        else:
            # Create a new driver if none exists for the user
            driver = Driver.objects.create(current_address=address, **validated_data)
            return driver

    def validate_current_address(self, value):
        """
        Validates that the current address is a dictionary and contains valid data.
        """
        if not isinstance(value, dict):  # Ensure the address is a dictionary
            raise serializers.ValidationError("The address must be a dictionary with the necessary data.")
        return value

    def validate_is_available(self, value):
        """
        Validates that the availability is a boolean value (True or False).
        """
        if not isinstance(value, bool):
            raise serializers.ValidationError("Availability must be a boolean value (True or False).")
        return value
