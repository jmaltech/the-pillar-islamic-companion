#  ---------- Zheer's Portion of Final Project ----------
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from hijridate import Gregorian
from islamic_times.islamic_times import ITLocation

HIJRI_MONTHS = [
    "Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani",
    "Jumada al-awwal", "Jumada al-thani", "Rajab", "Sha'ban",
    "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"
]


def get_location():
    return input("Enter (city, state) or zipcode: ").strip()


def get_coordinates(location):
    if not location.isdigit() and "," not in location:
        return None, "Incomplete location. Please enter both city and state (e.g., Nashville, TN) or a zipcode."

    geolocator = Nominatim(user_agent="the-pillar-app")

    try:
        result = geolocator.geocode(f"{location}, USA", addressdetails=True)
    except Exception:
        return None, "Error connecting to location service. Please try again."

    if not result:
        return None, "Location does not exist or could not be found. Please check your spelling and try again."

    address = result.raw.get("address", {})
    city_keys = ["city", "town", "village", "municipality", "suburb"]
    city = next((address[k] for k in city_keys if k in address), None)
    state = address.get("state")

    if not city or not state:
        return None, "Could not determine both city and state for that location. Please try entering (city, state) or a zipcode."

    return (result.latitude, result.longitude, f"{city}, {state}"), None


def get_prayer_times(latitude, longitude, date=None, method="ISNA"):
    date = date or datetime.now()

    try:
        it_location = ITLocation(
            latitude=latitude,
            longitude=longitude,
            date=date,
            method=method,
            find_local_tz=True
        )
        return it_location.prayer_times()
    except Exception as e:
        print(f"Error calculating prayer times: {e}")
        return None


def format_prayer_list(prayer_times_obj):
    prayer_list = []

    for line in str(prayer_times_obj).splitlines():
        if ":" not in line:
            continue

        label, _, rest = line.partition(":")
        label, rest = label.strip(), rest.strip()

        if label.lower() == "sunset" or not rest:
            continue

        try:
            time_obj = datetime.strptime(rest.split()[0], "%H:%M:%S")
            prayer_list.append({"name": label, "time": time_obj.strftime("%I:%M %p").lstrip("0")})
        except ValueError:
            continue

    return prayer_list


def get_hijri_date(date=None):
    date = date or datetime.now()
    hijri = Gregorian(date.year, date.month, date.day).to_hijri()
    return f"{hijri.day} {HIJRI_MONTHS[hijri.month - 1]} {hijri.year} AH"


def format_full_date(date=None):
    date = date or datetime.now()
    return f"{date.strftime('%A, %B')} {date.day}, {date.year}"


def shift_date(date, days):
    return date + timedelta(days=days)


def test_print(location=None, prayer_times=None, date=None):
    date = date or datetime.now()

    print(f"{format_full_date(date)}  |  {get_hijri_date(date)}")

    if prayer_times:
        print(f"Prayer times in ({location}):" if location else "Prayer Times:")
        for prayer in format_prayer_list(prayer_times):
            print(f"  {prayer['name'] + ':' :<10} {prayer['time']:>8}")


if __name__ == "__main__":
    location = get_location()
    coords_info, error = get_coordinates(location)

    if error:
        print(f"Error: {error}")
    else:
        latitude, longitude, city_state = coords_info
        prayers = get_prayer_times(latitude, longitude)
        test_print(city_state, prayers)
