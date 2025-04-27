from django.db import models
from addresses.models import Address

class Driver(models.Model):
    name = models.CharField(max_length=100)
    current_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
