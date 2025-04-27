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
        driver = Driver.objects.create(
            name="Carlos Pérez",
            current_address=self.address,
            is_available=True,
        )

        # Verify that the driver was created successfully in the database
        self.assertEqual(Driver.objects.count(), 1)
        self.assertEqual(driver.name, "Carlos Pérez")
        self.assertEqual(driver.current_address, self.address)
        self.assertEqual(driver.is_available, True)

    def test_driver_str_method(self):
        """Test the __str__ method for driver."""
        driver = Driver.objects.create(
            name="Ana García",
            current_address=self.address,
            is_available=True,
        )
        # Verify that the string representation of the driver matches the expected name
        self.assertEqual(str(driver), "Ana García")

    def test_driver_is_available(self):
        """Test changing the availability of the driver."""
        driver = Driver.objects.create(
            name="Jorge López",
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

        self.driver_data = {
            "name": "María Fernández",
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
        serializer = DriverSerializer(data=self.driver_data)
        
        self.assertTrue(serializer.is_valid())
        driver = serializer.save()

        # Verify that the driver's name matches the input data
        self.assertEqual(driver.name, self.driver_data['name'])
        
        # Verify that the driver's availability matches the input data
        self.assertEqual(driver.is_available, self.driver_data['is_available'])

    def test_driver_serializer_invalid(self):
        """Test the driver serializer with invalid data."""
        
        from drivers.serializers import DriverSerializer
        invalid_data = self.driver_data.copy()
        invalid_data['name'] = ""  # Nombre inválido

        serializer = DriverSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())  # The serializer should be invalid due to the empty name
        self.assertIn('name', serializer.errors)  # Verify that the error is in the 'name' field
