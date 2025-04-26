from rest_framework import generics
from .models import Driver
from .serializers import DriverSerializer
 
# View to create and list drivers
class DriverListCreateView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

# View to get, update, and delete a specific driver
class DriverRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
