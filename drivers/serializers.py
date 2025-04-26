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
        # Extract the address from the validated data set
        address_data = validated_data.pop('current_address')
        
        # Create the address
        address = Address.objects.create(**address_data)

        # Create the driver and assign the created address
        driver = Driver.objects.create(current_address=address, **validated_data)

        return driver
