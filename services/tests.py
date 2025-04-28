from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User

from addresses.models import Address
from drivers.models import Driver
from services.models import ServiceRequest

from unittest.mock import patch, MagicMock
from .helpers import haversine_distance, find_nearest_driver
from geopy.distance import geodesic


class CompleteServiceViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.client_user = User.objects.create_user(
            username="client", password="testpass"
        )
        self.driver_user = User.objects.create_user(
            username="driver", password="testpass"
        )

        profile = self.driver_user.userprofile
        profile.is_driver = True
        profile.save()

        # Create addresses
        self.pickup_address = Address.objects.create(
            street="Cl. 68a #90a – 31",
            city="Bogotá",
            latitude=4.693408,
            longitude=-74.112279,
        )

        self.driver_address = Address.objects.create(
            street="Cl. 70 #10-15", city="Bogotá", latitude=4.7110, longitude=-74.0721
        )

        # create Driver
        self.driver = Driver.objects.create(
            user=self.driver_user,  # Associate the driver with the user
            current_address=self.driver_address,
            is_available=True,
        )

        # create servic request
        self.service_request = ServiceRequest.objects.create(
            client=self.client_user,
            pickup_address=self.pickup_address,
            assigned_driver=self.driver,
            estimated_time_minutes=10,
            status=ServiceRequest.Status.IN_PROGRESS,
        )

        self.url = reverse("complete-service", kwargs={"pk": self.service_request.pk})

    def test_driver_can_complete_service(self):
        """A driver can complete a service"""
        self.client.force_authenticate(user=self.driver_user)
        response = self.client.patch(self.url, {"status": "completed"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.status, "completed")

    def test_client_cannot_complete_service(self):
        """A regular client cannot complete a service"""
        self.client.force_authenticate(user=self.client_user)
        response = self.client.patch(self.url, {"status": "completed"}, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Only drivers can complete a service.", response.json()["error"])

    def test_driver_cannot_set_invalid_status(self):
        """A driver cannot set an invalid status"""
        self.client.force_authenticate(user=self.driver_user)
        response = self.client.patch(self.url, {"status": "cancelled"}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid status", str(response.content))


class DriverTests(TestCase):

    @patch("services.helpers.openrouteservice.Client.directions")
    @patch("services.helpers.Driver.objects.filter")
    def test_find_nearest_driver(self, mock_filter, mock_directions):
        # Create mock Address instances
        address_1 = Address.objects.create(
            street="Street 1", city="City 1", latitude=10.0, longitude=20.0
        )
        address_2 = Address.objects.create(
            street="Street 2", city="City 2", latitude=15.0, longitude=25.0
        )

        # Create a mock user (this is necessary to avoid the ForeignKey error)
        user_1 = User.objects.create(username="user1", password="password")
        user_2 = User.objects.create(username="user2", password="password")

        # Create drivers with the associated user and address
        driver_1 = Driver.objects.create(
            user=user_1,  # Assigning the created user
            current_address=address_1,
            is_available=True,
        )
        driver_2 = Driver.objects.create(
            user=user_2,  # Assigning the created user
            current_address=address_2,
            is_available=True,
        )

        # Mock the response from OpenRouteService for both drivers
        mock_route_1 = {
            "features": [
                {
                    "properties": {
                        "summary": {
                            "distance": 1000,  # in meters
                            "duration": 600,  # in seconds
                        }
                    }
                }
            ]
        }

        mock_route_2 = {
            "features": [
                {
                    "properties": {
                        "summary": {
                            "distance": 2000,  # in meters
                            "duration": 1200,  # in seconds
                        }
                    }
                }
            ]
        }

        # Configure the mock responses
        mock_directions.side_effect = [mock_route_1, mock_route_2]
        mock_filter.return_value = [driver_1, driver_2]

        # Create a mock pickup address with latitude and longitude
        pickup_address = MagicMock()
        pickup_address.latitude = 12.0
        pickup_address.longitude = 22.0

        # Call the function to find the nearest driver
        nearest_driver, min_distance, estimated_time_minutes = find_nearest_driver(
            pickup_address
        )

        # Assert that the nearest driver is driver_1
        self.assertEqual(nearest_driver, driver_1)
        self.assertEqual(min_distance, 1.0)  # in kilometers
        self.assertEqual(estimated_time_minutes, 10)  # in minutes

    def test_haversine_distance(self):
        # Test Haversine distance calculation
        lat1, lon1 = 10.0, 20.0
        lat2, lon2 = 15.0, 25.0
        result = haversine_distance(lat1, lon1, lat2, lon2)

        # Use geopy to calculate the actual distance as a reference
        expected_distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers

        # Assert that the result is approximately equal to the expected value
        self.assertAlmostEqual(result, expected_distance, delta=0.5)
