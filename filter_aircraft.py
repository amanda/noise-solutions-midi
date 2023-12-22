import json
import requests
from math import atan2, degrees, radians, sin, cos, sqrt

API_URL = "https://api.adsb.lol/api/0/routeset"
data = "json/aircraft.json"
latitude = 40.7038776
longitude = -73.8876282

def fetch_routes(callsigns):
    data = {"planes": [{"callsign": callsign.strip(), "lat": 0, "lng": 0} for callsign in callsigns]}
    r = requests.post(API_URL, json=data)
    r.raise_for_status()
    return {rec.get("callsign"):rec.get('_airport_codes_iata') for rec in r.json()}

def haversine_distance(lat1, lon1, lat2=latitude, lon2=longitude):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of the Earth in miles (you can change this to kilometers if needed)
    R = 3958.8

    # Calculate the distance
    distance = R * c

    return distance

def compass_bearing(lat2, lon2, lat1=latitude, lon1=longitude):
    """
    Calculate the initial compass bearing in degrees from the source
    coordinate pair to the target coordinate pair.
    """
    lat1, lon1 = radians(lat1), radians(lon1)
    lat2, lon2 = radians(lat2), radians(lon2)

    dlon = lon2 - lon1

    x = atan2(
        sin(dlon) * cos(lat2),
        cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(dlon))
    )

    # Convert bearing from radians to degrees
    initial_bearing = (degrees(x) + 360) % 360

    return initial_bearing

def calculate_relative_bearing(lat, lon, bearing, buffer_angle=40):
    """
    Check if the target object is heading toward the source location
    within a configurable buffer angle.
    """
    # Calculate the initial compass bearing from source to target
    target_bearing = compass_bearing(lat, lon)

    # Calculate the relative bearing (difference between source and target bearings)
    relative_bearing = (target_bearing - bearing + 360) % 360

    # Check if the relative bearing is within the buffer angle
    return relative_bearing

# open the json file and calculate distance in miles between the aircrafts and the given location
# with open(data, "r") as f:
#     data = json.load(f).get("aircraft")
#     callsigns = [i.get("flight") for i in data if "flight" in i]
#     routes = fetch_routes(callsigns)
#     for i in data:
#         if "lat" not in i or "lon" not in i:
#             continue
#         lat = i.get("lat")
#         lon = i.get("lon")
#         i["distance"] = haversine_distance(lat, lon)
#         if "track" in i and i["distance"] < 20:
#             callsign = i.get("flight", "").strip()
#             print(callsign, i.get("squawk"), i["distance"], i["track"], routes.get(callsign))
