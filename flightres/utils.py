import requests
import json
from math import radians, cos, sin, asin, sqrt


def reverseGeocode(query):
    try:
        geo_token = "4f7a333111ac5f"
        url = "https://us1.locationiq.com/v1/search.php"
        data = {
            'key': geo_token,
            'q': query,
            'format': 'json'
        }

        response = requests.get(url, params=data)
        obj = json.loads(response.text)

        return obj[0]['lat'], obj[0]['lon']
    except KeyError:
        return "Inavalid Address"


def is_near_senstive_area(lat, lon):
    sensitive_areas = [
        {'lat': 27.691163902, 'lon': 85.355331912, 'name': 'Tribhuvan International Airport', 'threshold_in_km': 1},
        {'lat': 27.7042, 'lon': 85.3067, 'name': 'Kathmandu Durbar Square', 'threshold_in_km': 1},
        {'lat': 27.6721, 'lon': 85.4281, 'name': 'Bhaktapur Durbar Square', 'threshold_in_km': 1},
        {'lat': 27.6727, 'lon': 85.3253, 'name': 'Patan Durbar Square', 'threshold_in_km': 1},
    ]

    distances = []
    for area in sensitive_areas:
        distances.append(haversine(area.get('lat'), area.get('lon'), lat, lon))

    nearest_poi_distance = min(distances)
    nearest_poi_name = sensitive_areas[distances.index(nearest_poi_distance)].get('name')
    if nearest_poi_distance < 1:
        return True, "This is in/near \"No Fly Zone\" {}. A special flight permission is required for this flight".format(
            nearest_poi_name)

    return False, ""


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def validate_lat_lon(lat_lon):
    valid = False

    try:
        lat, lon = lat_lon.split(",")
        lat = float(lat)
        lon = float(lon)
        valid_lat = -90.0 <= lat <= 90.0
        valid_lon = -180.0 <= lon <= 180.0
        valid = valid_lat and valid_lon
    except ValueError:
        lat = 0
        lon = 0
        return valid, lat, lon
