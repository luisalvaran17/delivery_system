import openrouteservice
from drivers.models import Driver
from addresses.models import Address
import os

ORS_API_KEY = os.getenv('OPENROUTE_SERVICE_KEY')
client = openrouteservice.Client(key=ORS_API_KEY)

import openrouteservice
from drivers.models import Driver
from addresses.models import Address
import os

ORS_API_KEY = os.getenv('OPENROUTE_SERVICE_KEY')
client = openrouteservice.Client(key=ORS_API_KEY)

def find_nearest_driver(pickup_address):
    """
    Finds the nearest available driver based on the pickup address,
    using OpenRouteService to calculate real distance and estimated time.
    """
    available_drivers = Driver.objects.filter(is_available=True)

    if not available_drivers.exists():
        raise Exception('No available drivers')

    nearest_driver = None
    min_distance = float('inf')
    estimated_time_minutes = None

    pickup_coords = (pickup_address.longitude, pickup_address.latitude)

    for driver in available_drivers:
        if driver.current_address:
            driver_coords = (driver.current_address.longitude, driver.current_address.latitude)

            try:
                # Request route calculation from OpenRouteService
                route = client.directions(
                    coordinates=[pickup_coords, driver_coords],
                    profile='cycling-road',
                    format='geojson'
                )

                route_summary = route['features'][0]['properties']['summary']
                if not route_summary:
                    continue
                distance_km = route_summary['distance'] / 1000  # Convert meters to kilometers
                duration_minutes = route_summary['duration'] / 60  # Convert seconds to minutes

                # Check if this driver is closer than the current nearest
                if distance_km < min_distance:
                    min_distance = distance_km
                    nearest_driver = driver
                    estimated_time_minutes = int(duration_minutes)

            except openrouteservice.exceptions.ApiError as e:
                continue

    if nearest_driver is None:
        raise Exception('No driver found with a valid route')

    return nearest_driver, min_distance, estimated_time_minutes
