from rest_framework import generics
from .models import Address
from .serializers import AddressSerializer
 
# Vista para crear y listar direcciones
class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

# Vista para obtener, actualizar y eliminar una dirección especifica
class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
