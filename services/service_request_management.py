# services/service_request_service.py
from addresses.models import Address
from .models import ServiceRequest
from services.helpers import find_nearest_driver
from rest_framework.exceptions import ValidationError


def create_pickup_address(pickup_address_data):
    """
    Creates the pickup address from the provided data.
    """
    try:
        pickup_address = Address.objects.create(**pickup_address_data)
        return pickup_address
    except Exception as e:
        raise ValidationError(f'Error creating pickup address: {str(e)}')


def assign_driver_to_service(pickup_address):
    """
    Assigns the nearest driver to the service request.
    """
    available_nearest_driver, _, estimated_time = find_nearest_driver(pickup_address)
    if not available_nearest_driver:
        raise ValidationError('No available drivers')
    if estimated_time is None:
        raise ValidationError('Unable to estimate time for the driver')
    return available_nearest_driver, estimated_time


def create_service_request(pickup_address, assigned_driver, estimated_time):
    """
    Creates a service request with the pickup address and the assigned driver.
    """
    try:
        service_request = ServiceRequest.objects.create(
            pickup_address=pickup_address,
            assigned_driver=assigned_driver,
            estimated_time_minutes=estimated_time,
            status='in progress'
        )
        return service_request
    except Exception as e:
        raise ValidationError(f'Error creating service request: {str(e)}')


def update_driver_availability(assigned_driver):
    """
    Updates the driver's availability to unavailable.
    """
    try:
        assigned_driver.is_available = False
        assigned_driver.save()
    except Exception as e:
        raise ValidationError(f'Error updating driver availability: {str(e)}')


def update_service_driver(service, status_service):
    """
    Updates the service status to the specified status and sets the driver's availability to False.
    """
    try:
        service.status = status_service
        assigned_driver = service.assigned_driver
        assigned_driver.is_available = True
        service.save()
        assigned_driver.save()
    except Exception as e:
        raise ValidationError(f'Error updating service status or driver availability: {str(e)}')
