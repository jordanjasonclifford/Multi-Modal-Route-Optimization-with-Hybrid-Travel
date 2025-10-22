import requests
import json
from geopy.distance import geodesic  # For direct distance calculation


def getDistance(A, B, m):
    if m == "direct":
        return geodesic(A, B).meters


    API_KEY = ""
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"


    params = {
        "origins": f"{A[0]},{A[1]}",
        "destinations": f"{B[0]},{B[1]}",
        "mode": m,
        "units": "metric",
        "key": API_KEY,
    }


    response = requests.get(base_url, params=params)


    if response.status_code == 200:
        data = json.loads(response.text)
        if data["status"] == "OK":
            try:
                distance_meters = data["rows"][0]["elements"][0]["distance"]["value"]
                return distance_meters
            except (KeyError, IndexError):
                pass  # Handle missing data in the API response
   
    # Return None if API call failed or data was invalid
    return None


# Example Usage:
benaroya_hall = (47.60814199288301, -122.3368087995574)
museum_pop_culture = (47.621470125609314, -122.3481282699205)
spaceneedle = (47.620475865973454, -122.34922662355609)
seattle_aquarium = (47.607381610552146, -122.34296367108706)
sculpture_park = (47.616598558883176, -122.35531073027671)
pike_place = (47.60939849082073, -122.3418399195103)
art_museum = (47.60751482550527, -122.33796002616279)
westlake_center = (47.61204391377087, -122.33748668957276)
uwub_station = (47.65027972126398, -122.30374414254722)
westlake_station = (47.61175694210985, -122.3365386185384)
u_district_station = (47.6599735494618, -122.31407798225337)
henry_art_gallery = (47.656270488379, -122.31172287699964)
fremont_troll = (47.65105594466806, -122.34750074191479)
sodo_station = (47.581165192600594, -122.32736238031688)
mohai = (47.62757702542345, -122.33690614596017)
cap_hill_station = (47.619755979512334, -122.32061042657767)


fourDestinations = [
    ("The Seattle Great Wheel", (47.606120881176786, -122.34252171878009)),       # A
    ("SODO Station", (47.581165192600594, -122.32736238031688)),                  # B
    ("International Fountain", (47.62250232314546, -122.35208589820942)),         # C
    ("Historic Chinatown Gate", (47.59835834310235, -122.328023768465))         # D
]


# Unpack them for manual use
nameA, A = fourDestinations[0]
nameB, B = fourDestinations[1]
nameC, C = fourDestinations[2]
nameD, D = fourDestinations[3]

# AB
print(f"AB - {nameA} → {nameB}")
print("  Driving distance:", getDistance(A, B, "driving"), "meters")
print("  Walking distance:", getDistance(A, B, "walking"), "meters")
print("  Bicycling distance:", getDistance(A, B, "bicycling"), "meters")
print("  Transit distance:", getDistance(A, B, "transit"), "meters\n")

# BC
print(f"BC - {nameB} → {nameC}")
print("  Driving distance:", getDistance(B, C, "driving"), "meters")
print("  Walking distance:", getDistance(B, C, "walking"), "meters")
print("  Bicycling distance:", getDistance(B, C, "bicycling"), "meters")
print("  Transit distance:", getDistance(B, C, "transit"), "meters\n")

# CD
print(f"CD - {nameC} → {nameD}")
print("  Driving distance:", getDistance(C, D, "driving"), "meters")
print("  Walking distance:", getDistance(C, D, "walking"), "meters")
print("  Bicycling distance:", getDistance(C, D, "bicycling"), "meters")
print("  Transit distance:", getDistance(C, D, "transit"), "meters\n")
