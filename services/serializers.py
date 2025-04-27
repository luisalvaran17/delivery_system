from django.forms import ValidationError
from rest_framework import serializers
from .models import ServiceRequest
from addresses.serializers import AddressSerializer
from drivers.serializers import DriverSerializer

class ServiceRequestSerializer(serializers.ModelSerializer):
    pickup_address = AddressSerializer(read_only=True)
    assigned_driver = DriverSerializer(read_only=True)
    client = serializers.StringRelatedField()

    class Meta:
        model = ServiceRequest
        fields = ['id', 'client', 'pickup_address', 'assigned_driver', 'estimated_time_minutes', 'created_at', 'status']

        def validate_status(self, value):
            """
            Ensures that the service status is valid.
            """
            valid_statuses = ['in progress', 'completed', 'cancelled']
            if value not in valid_statuses:
                raise ValidationError(f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}.")
            return value
