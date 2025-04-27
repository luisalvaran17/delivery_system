from django.urls import path
from .views import ServiceRequestListCreateView, ServiceRequestRetrieveUpdateDestroyView, CompleteServiceView

urlpatterns = [
    path('services/', ServiceRequestListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceRequestRetrieveUpdateDestroyView.as_view(), name='service-retrieve-update-destroy'),
    path('services/<int:pk>/complete/', CompleteServiceView.as_view(), name='complete-service'),
]
