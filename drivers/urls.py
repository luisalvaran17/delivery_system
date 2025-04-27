from django.urls import path
from .views import DriverListCreateView, DriverRetrieveUpdateDestroyView

urlpatterns = [
    path('drivers/', DriverListCreateView.as_view(), name='driver-list-create'),
    path('drivers/<int:pk>/', DriverRetrieveUpdateDestroyView.as_view(), name='driver-retrieve-update-destroy'),
]
