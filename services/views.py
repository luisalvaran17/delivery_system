from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import ServiceRequest
from .serializers import ServiceRequestSerializer
from services.service_request_management import (
    create_pickup_address, assign_driver_to_service, 
    create_service_request, update_driver_availability,
    update_service_driver
)


class ServiceRequestListCreateView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    
    def create(self, request, *args, **kwargs):
        pickup_address_data = request.data.get('pickup_address')

        if not pickup_address_data:
            return Response({'error': 'pickup_address is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the pickup address
        try:
            pickup_address = create_pickup_address(pickup_address_data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Find an available driver and choose the closest one
        try:
            available_nearest_driver, estimated_time = assign_driver_to_service(pickup_address)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Create the service request
        try:
            client = request.user
            service_request = create_service_request(client, pickup_address, available_nearest_driver, estimated_time)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Update the driver status to unavailable
        try:
            update_driver_availability(available_nearest_driver)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the service request and return the response
        serializer = self.get_serializer(service_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ServiceRequestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer


class CompleteServiceView(generics.UpdateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

    def update(self, request, *args, **kwargs):
        # Ensure the service exists
        try:
            service = self.get_object()
        except ServiceRequest.DoesNotExist:
            raise ValidationError(detail="Service not found.")  # 404 Not Found

        # Ensure that the user is a driver
        user_profile = request.user.userprofile
        print('user_profile', user_profile)
        if not user_profile.is_driver:
            return Response({'error': 'Only drivers can complete a service.'}, status=status.HTTP_403_FORBIDDEN)

        status_service = request.data.get('status', '')
        if status_service != 'completed':
            raise ValidationError(detail="Invalid status. Only 'completed' is allowed.")  # 400 Bad Request

        # Mark the service as completed
        try:
            update_service_driver(service, status_service)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Return response with updated service
        return Response(self.serializer_class(service).data, status=status.HTTP_200_OK)
