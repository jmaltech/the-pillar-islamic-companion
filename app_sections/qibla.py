# ---------- Jamaal's Portion of Final Project ----------
# Qibla Finder Module
# Course: High-Level Language - Python Group Project
# Description: Finds a user's coordinates from a city/state or ZIP code and
#              calculates the Qibla direction toward the Kaaba in Makkah.

import math
from geopy.geocoders import Nominatim

KAABA_LATITUDE = 21.4225
KAABA_LONGITUDE = 39.8262


def get_coordinates(location):
    """Convert a city/state or ZIP code into latitude and longitude."""
    location = location.strip()

    if not location:
        return None, "Please enter a city and state or a ZIP code."

    if not location.isdigit() and "," not in location:
        return None, (
            "Incomplete location. Please enter both city and state "
            "(for example, Nashville, TN) or a ZIP code."
        )

    geolocator = Nominatim(user_agent="the-pillar-qibla-finder")

    try:
        result = geolocator.geocode(f"{location}, USA", addressdetails=True)
    except Exception:
        return None, "Error connecting to the location service. Please try again."

    if not result:
        return None, (
            "The location could not be found. Please check the spelling and try again."
        )

    address = result.raw.get("address", {})
    city_keys = ["city", "town", "village", "municipality", "suburb", "county"]
    city = next((address[key] for key in city_keys if key in address), None)
    state = address.get("state")

    if city and state:
        formatted_location = f"{city}, {state}"
    else:
        formatted_location = result.address

    return (result.latitude, result.longitude, formatted_location), None


def validate_coordinates(latitude, longitude):
    """Check that latitude and longitude are valid numeric values."""
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return None, "Latitude and longitude must be numbers."

    if not -90 <= latitude <= 90:
        return None, "Latitude must be between -90 and 90 degrees."

    if not -180 <= longitude <= 180:
        return None, "Longitude must be between -180 and 180 degrees."

    return (latitude, longitude), None


def calculate_qibla_bearing(latitude, longitude):
    """Calculate the Qibla bearing clockwise from true north."""
    coordinates, error = validate_coordinates(latitude, longitude)
    if error:
        raise ValueError(error)

    latitude, longitude = coordinates

    user_latitude = math.radians(latitude)
    kaaba_latitude = math.radians(KAABA_LATITUDE)
    longitude_difference = math.radians(KAABA_LONGITUDE - longitude)

    x_value = math.sin(longitude_difference)
    y_value = (
        math.cos(user_latitude) * math.tan(kaaba_latitude)
        - math.sin(user_latitude) * math.cos(longitude_difference)
    )

    bearing = math.degrees(math.atan2(x_value, y_value))
    return round((bearing + 360) % 360, 1)


def get_compass_direction(bearing):
    """Convert a numeric bearing into one of eight compass directions."""
    directions = [
        "North", "Northeast", "East", "Southeast",
        "South", "Southwest", "West", "Northwest"
    ]
    index = int((float(bearing) + 22.5) // 45) % 8
    return directions[index]


def get_qibla_from_coordinates(latitude, longitude, location="Current Location"):
    """Return Qibla information when coordinates are already available."""
    coordinates, error = validate_coordinates(latitude, longitude)

    if error:
        return {"success": False, "error": error}

    latitude, longitude = coordinates
    bearing = calculate_qibla_bearing(latitude, longitude)

    return {
        "success": True,
        "location": location,
        "latitude": round(latitude, 4),
        "longitude": round(longitude, 4),
        "qibla_degrees": bearing,
        "qibla_direction": get_compass_direction(bearing),
        "error": None
    }


def get_qibla_data(location):
    """Find a location and return all Qibla information in a dictionary."""
    coordinate_info, error = get_coordinates(location)

    if error:
        return {"success": False, "error": error}

    latitude, longitude, formatted_location = coordinate_info
    return get_qibla_from_coordinates(latitude, longitude, formatted_location)


def run_qibla_finder_cli():
    """Run a small terminal version for testing the module by itself."""
    print("\n              QIBLA FINDER              ")
    location = input("Enter a city, state, or ZIP code: ").strip()
    result = get_qibla_data(location)

    if not result["success"]:
        print(f"\nError: {result['error']}")
        return

    print("\n              QIBLA RESULT              ")
    print(f"Location          : {result['location']}")
    print(f"Coordinates       : {result['latitude']}, {result['longitude']}")
    print(f"Qibla Bearing     : {result['qibla_degrees']} degrees")
    print(f"Compass Direction : {result['qibla_direction']}")
    print(
        f"\nFace approximately {result['qibla_degrees']} degrees clockwise "
        "from true north.\n"
    )


if __name__ == "__main__":
    run_qibla_finder_cli()
