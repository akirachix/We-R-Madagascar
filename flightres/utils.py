import requests
import json


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
