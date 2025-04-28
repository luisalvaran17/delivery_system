from rest_framework import generics
from .models import Driver
from .serializers import DriverSerializer
from rest_framework.permissions import IsAuthenticated


# View to create and list drivers
class DriverListCreateView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


# View to get, update, and delete a specific driver
class DriverRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
