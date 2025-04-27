from faker import Faker
from django.core.management.base import BaseCommand
from addresses.models import Address
from drivers.models import Driver
from django.contrib.auth.models import User
from users.models import UserProfile
import random

class Command(BaseCommand):
    help = 'Create addresses and drivers with Faker'

    def handle(self, *args, **kwargs):
        calles_bogota = [
            "Calle 45", "Calle 68", "Carrera 10", "Avenida El Dorado", "Avenida Boyacá",
            "Calle 100", "Calle 13", "Calle 26", "Carrera 7", "Carrera 15", 
            "Avenida Suba", "Avenida Caracas", "Avenida Ciudad de Cali", "Calle 80",
            "Calle 53", "Calle 50", "Carrera 19", "Carrera 30", "Calle 170", 
            "Calle 182", "Avenida Boyacá", "Avenida NQS", "Calle 39", "Calle 23",
            "Calle 56", "Calle 92", "Calle 42", "Carrera 5", "Carrera 24"
        ]
        # Latitude and longitude range for Bogotá
        lat_min, lat_max = 4.5, 4.9
        lon_min, lon_max = -74.2, -74.1

        fake = Faker('es_CO')

        # Create 20 addresses
        for _ in range(20):
            street = f"{random.choice(calles_bogota)} {random.randint(1, 99)}"
            lat = round(random.uniform(lat_min, lat_max), 6)  # Generar latitud
            lon = round(random.uniform(lon_min, lon_max), 6)  # Generar longitud
            address = Address.objects.create(
                street=street,
                city='Bogotá',
                latitude=lat,
                longitude=lon
            )
            self.stdout.write(f"Address created: {address}")

        # Create 20 drivers
        for _ in range(20):
            # Create a random user
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password',
                email=fake.email()
            )

            # Create the user profile and mark as driver
            user_profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'is_driver': True}  # Mark this user as a driver
            )

            # Create a driver and link to a random address
            driver = Driver.objects.create(
                user=user,  # Assign the User object, not the UserProfile
                current_address=Address.objects.order_by('?').first(),  # Assign a random address
                is_available=True
            )

            self.stdout.write(f"Driver created: {driver.user.username} with user profile as driver")
            
