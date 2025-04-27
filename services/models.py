from django.db import models
from addresses.models import Address
from drivers.models import Driver
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    assigned_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_time_minutes = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    def __str__(self):
        return f"Service {self.id} - {self.status}"
