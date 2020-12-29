import requests
import json
from math import radians, cos, sin, asin, sqrt
from shapely.geometry import Point, Polygon
from zipfile import ZipFile




def reverseGeocode(query):
    try:
        geo_token = "4f7a333111ac5f"
        url = "https://us1.locationiq.com/v1/search.php"
        data = {
            'key': geo_token,
            'q': query,
            'format': 'json',
            'countrycodes': 'np',
        }

        response = requests.get(url, params=data)
        obj = json.loads(response.text)

        return obj[0]['lat'], obj[0]['lon']
    except KeyError:
        return "Inavalid Address"


def is_near_senstive_area(lat, lon, shp_names):
    sensitive_areas = []
    points = Point(lat, lon)
   
    for x in shp_names:
        with open('/usr/src/app/uploads/shp_files/' + x) as f:
            data = json.load(f)
            for feature in data['features']:
                for y in feature['geometry']['coordinates']:
                    areas = []
                    for z in y:
                        areas.append([z[1], z[0]])
                    polyg = Polygon(areas)
                    sensitive_areas.append(polyg)
        f.close()
        
    for pol in sensitive_areas:
        if pol.contains(points) or points.touches(pol):
            return True, "This is inside the \"No Fly Zone\" {}. A special flight permission is required for this flight".format(
            'No-fly zone')
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
