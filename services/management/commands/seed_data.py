from faker import Faker
from django.core.management.base import BaseCommand
from addresses.models import Address
from drivers.models import Driver
from django.contrib.auth.models import User
from users.models import UserProfile

class Command(BaseCommand):
    help = 'Create addresses and drivers with Faker'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create 20 addresses
        for _ in range(20):
            address = Address.objects.create(
                street=fake.street_address(),
                city=fake.city(),
                latitude=fake.latitude(),
                longitude=fake.longitude()
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
