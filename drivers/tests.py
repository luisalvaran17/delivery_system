from django.test import TestCase
from django.contrib.auth.models import User
from addresses.models import Address
from drivers.models import Driver

class DriverModelTest(TestCase):
    """Test the Driver model."""

    def setUp(self):
        """Set up test data."""
        # Create an address instance for the driver
        self.address = Address.objects.create(
            street="Calle 123", city="Bogotá", latitude=4.60971, longitude=-74.08175
        )

    def test_create_driver(self):
        """Test creating a driver."""
        # Create a user for the driver
        user = User.objects.create_user(
            username="carlos_perez",
            password="password",
            email="carlos@example.com"
        )

        # Create the driver and associate it with the user
        driver = Driver.objects.create(
            user=user,
            current_address=self.address,
            is_available=True,
        )

        # Verify that the driver was created successfully in the database
        self.assertEqual(Driver.objects.count(), 1)
        self.assertEqual(driver.user.username, "carlos_perez")  # Check the user related to the driver
        self.assertEqual(driver.current_address, self.address)
        self.assertEqual(driver.is_available, True)

    def test_driver_str_method(self):
        """Test the __str__ method for driver."""
        user = User.objects.create_user(
            username="ana_garcia",
            password="password",
            email="ana@example.com"
        )
        driver = Driver.objects.create(
            user=user,
            current_address=self.address,
            is_available=True,
        )

        # Verify that the string representation of the driver matches the user's username or full name
        self.assertEqual(str(driver), "ana_garcia")  # Here we use the username of the user

    def test_driver_is_available(self):
        """Test changing the availability of the driver."""
        user = User.objects.create_user(
            username="jorge_lopez",
            password="password",
            email="jorge@example.com"
        )
        driver = Driver.objects.create(
            user=user,
            current_address=self.address,
            is_available=True,
        )
        self.assertTrue(driver.is_available)
        
        driver.is_available = False
        driver.save()
        
        # Reload the object from the database
        driver.refresh_from_db()
        
        self.assertFalse(driver.is_available)

class DriverSerializerTest(TestCase):
    """Test the Driver serializer."""

    def setUp(self):
        """Set up test data for serialization."""
        self.address = Address.objects.create(
            street="Carrera 45", city="Medellín", latitude=6.2442, longitude=-75.5812
        )

        # Create a user for the driver
        self.user = User.objects.create_user(username="maria", password="testpass")

        # Valid data for the driver, including the user ID
        self.driver_data = {
            "user": self.user.id,
            "current_address": {
                "street": "Carrera 45",
                "city": "Medellín",
                "latitude": 6.2442,
                "longitude": -75.5812,
            },
            "is_available": True,
        }

    def test_driver_serializer_valid(self):
        """Test the driver serializer with valid data."""
        from drivers.serializers import DriverSerializer
        print('self.driver_data', self.driver_data)
        serializer = DriverSerializer(data=self.driver_data)

        self.assertTrue(serializer.is_valid())  # Verify that the serializer is valid
        driver = serializer.save()

        # Verify that the driver's user matches the provided user
        self.assertEqual(driver.user.username, self.user.username)

        # Verify that the driver's availability matches the provided data
        self.assertEqual(driver.is_available, self.driver_data['is_available'])
