from rest_framework import serializers
from .models import Driver
from addresses.models import Address
from addresses.serializers import AddressSerializer

class DriverSerializer(serializers.ModelSerializer):
    current_address = AddressSerializer()

    class Meta:
        model = Driver
        fields = ['id', 'name', 'current_address', 'is_available']

    def create(self, validated_data):
        """
        Creates a new Driver instance. Extracts the current address from the 
        validated data, creates the Address instance, and assigns it to the Driver.
        """
        # Extract the address from the validated data set
        address_data = validated_data.pop('current_address')
        
        # Create the address
        address = Address.objects.create(**address_data)

        # Create the driver and assign the created address
        driver = Driver.objects.create(current_address=address, **validated_data)

        return driver

    def validate_name(self, value):
        """
        Validates that the name contains only letters and spaces.
        """
        if not value.isalpha() and ' ' not in value:
            raise serializers.ValidationError("The name can only contain letters and spaces.")
        return value

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
