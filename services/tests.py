from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User

from addresses.models import Address
from drivers.models import Driver
from services.models import ServiceRequest

class CompleteServiceViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear usuarios
        self.client_user = User.objects.create_user(username='client', password='testpass')
        self.driver_user = User.objects.create_user(username='driver', password='testpass')
        profile = self.driver_user.userprofile
        profile.is_driver = True

        # Crear direcciones
        self.pickup_address = Address.objects.create(
            street='Cl. 68a #90a – 31',
            city='Bogotá',
            latitude=4.693408,
            longitude=-74.112279
        )

        self.driver_address = Address.objects.create(
            street='Cl. 70 #10-15',
            city='Bogotá',
            latitude=4.7110,
            longitude=-74.0721
        )

        # Crear Driver
        self.driver = Driver.objects.create(
            name='Driver Name',
            current_address=self.driver_address,
            is_available=True
        )

        # Crear solicitud de servicio
        self.service_request = ServiceRequest.objects.create(
            client=self.client_user,
            pickup_address=self.pickup_address,
            assigned_driver=self.driver,
            estimated_time_minutes=10,
            status=ServiceRequest.Status.IN_PROGRESS
        )

        self.url = reverse('complete-service', kwargs={'pk': self.service_request.pk})

    def test_driver_can_complete_service(self):
        """Un conductor puede completar un servicio"""
        self.client.force_authenticate(user=self.driver_user)
        response = self.client.patch(self.url, {'status': 'completed'}, format='json')

        self.assertEqual(response.status_code, 200)
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.status, 'completed')

    def test_client_cannot_complete_service(self):
        """Un cliente normal no puede completar un servicio"""
        self.client.force_authenticate(user=self.client_user)
        response = self.client.patch(self.url, {'status': 'completed'}, format='json')

        self.assertEqual(response.status_code, 403)
        self.assertIn('Only drivers can complete a service.', response.json()['error'])

    def test_driver_cannot_set_invalid_status(self):
        """Un conductor no puede poner un estado inválido"""
        self.client.force_authenticate(user=self.driver_user)
        response = self.client.patch(self.url, {'status': 'cancelled'}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid status', str(response.content))
