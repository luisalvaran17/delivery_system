from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Meta:
        app_label = 'user'

    CLIENT = 'client'
    DRIVER = 'driver'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (DRIVER, 'Driver')
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENT)

    def __str__(self):
        return f"{self.username} - {self.role}"
