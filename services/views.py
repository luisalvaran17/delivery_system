from rest_framework import generics, status
from rest_framework.response import Response

from addresses.models import Address
from .models import ServiceRequest
from .serializers import ServiceRequestSerializer
from services.helpers import find_nearest_driver


class ServiceRequestListCreateView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    
    def create(self, request, *args, **kwargs):
        print('heeree')
        pickup_address_data = request.data.get('pickup_address')

        if not pickup_address_data:
            return Response({'error': 'pickup_address is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the pickup address
        pickup_address = Address.objects.create(**pickup_address_data)

        # Find an available driver and choose the closest one
        available_nearest_driver, _, estimated_time = find_nearest_driver(pickup_address)

        if not available_nearest_driver:
            return Response({'error': 'No available drivers'}, status=status.HTTP_404_NOT_FOUND)

        service_request = ServiceRequest.objects.create(
            pickup_address=pickup_address,
            assigned_driver=available_nearest_driver,
            estimated_time_minutes=estimated_time,
            status='in progress'
        )

        available_nearest_driver.is_available = False
        available_nearest_driver.save()

        serializer = self.get_serializer(service_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ServiceRequestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
