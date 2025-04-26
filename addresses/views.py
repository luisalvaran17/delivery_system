from rest_framework import generics
from .models import Address
from .serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated
 
# Vista para crear y listar direcciones
class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

# Vista para obtener, actualizar y eliminar una dirección especifica
class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
