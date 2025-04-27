from rest_framework import serializers
from .models import ServiceRequest
from addresses.serializers import AddressSerializer
from drivers.serializers import DriverSerializer

class ServiceRequestSerializer(serializers.ModelSerializer):
    pickup_address = AddressSerializer()
    assigned_driver = DriverSerializer(read_only=True)

    class Meta:
        model = ServiceRequest
        fields = ['id', 'pickup_address', 'assigned_driver', 'estimated_time_minutes', 'created_at', 'status']
