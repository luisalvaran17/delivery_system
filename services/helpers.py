import openrouteservice
from drivers.models import Driver
import os
import concurrent.futures
from math import radians, cos, sin, asin, sqrt

ORS_API_KEY = os.getenv("OPENROUTE_SERVICE_KEY")
client = openrouteservice.Client(key=ORS_API_KEY)


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


def find_nearest_driver(pickup_address, candidates_limit=10):
    """
    Finds the nearest available driver based on pickup address.
    First prefilters candidates using Haversine distance.
    Then gets real distance via OpenRouteService.
    """
    available_drivers = Driver.objects.filter(
        is_available=True, current_address__isnull=False
    )

    if not available_drivers.exists():
        raise Exception("No available drivers")

    pickup_lat = pickup_address.latitude
    pickup_lon = pickup_address.longitude

    # Prefilter: calculate Haversine distance
    driver_distances = []
    for driver in available_drivers:
        driver_lat = driver.current_address.latitude
        driver_lon = driver.current_address.longitude
        distance = haversine_distance(pickup_lat, pickup_lon, driver_lat, driver_lon)
        driver_distances.append((driver, distance))

    # Sort by distance and take only the N closest candidates
    driver_distances.sort(key=lambda x: x[1])
    candidates = [driver for driver, _ in driver_distances[:candidates_limit]]

    pickup_coords = (pickup_address.longitude, pickup_address.latitude)

    def get_driver_route(driver):
        try:
            driver_coords = (
                driver.current_address.longitude,
                driver.current_address.latitude,
            )
            route = client.directions(
                coordinates=[pickup_coords, driver_coords],
                profile="cycling-road",
                format="geojson",
            )
            route_summary = route["features"][0]["properties"]["summary"]
            if not route_summary:
                return None

            distance_km = route_summary["distance"] / 1000
            duration_minutes = int(route_summary["duration"] / 60)
            return (driver, distance_km, duration_minutes)
        except Exception as e:
            raise RuntimeError(
                f"Error calculating route for driver {driver.id if driver else 'unknown'}: {str(e)}"
            )

    nearest_driver = None
    min_distance = float("inf")
    estimated_time_minutes = None

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(get_driver_route, driver): driver for driver in candidates
        }

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                driver, distance_km, duration_minutes = result
                if (
                    estimated_time_minutes is None
                    or duration_minutes < estimated_time_minutes
                ):
                    nearest_driver = driver
                    min_distance = distance_km
                    estimated_time_minutes = duration_minutes

    if nearest_driver is None:
        raise Exception("No driver found with a valid route")

    return nearest_driver, min_distance, estimated_time_minutes
