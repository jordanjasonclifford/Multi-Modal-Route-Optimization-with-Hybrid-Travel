import requests
import json


def getTime(A, B, m):


    API_KEY = "AIzaSyBUsvoSqx1ru5MF5F9HCnYwOMgSVSdoBQo"
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"


    params = {
        "origins": f"{A[0]},{A[1]}",
        "destinations": f"{B[0]},{B[1]}",
        "mode": m,
        "units": "metric",  # Ensures time is returned in seconds
        "key": API_KEY,
    }


    response = requests.get(base_url, params=params)


    if response.status_code == 200:
        data = json.loads(response.text)
        if data["status"] == "OK":
            try:
                duration_seconds = data["rows"][0]["elements"][0]["duration"]["value"]
                return duration_seconds
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
international_fountain = (47.62250232314546, -122.35208589820942)
chinatown_gate = (47.59835834310235, -122.328023768465)
seattle_great_wheel = (47.606120881176786, -122.34252171878009)
u_village = (47.6616727246282, -122.29904419663022)
cap_hill = (47.619755979512334, -122.32061042657767)


print("  Driving distance:", getTime(cap_hill, B, "driving"), "seconds")
print("  Walking distance:", getTime(cap_hill, B, "walking"), "seconds")
print("  Bicycling distance:", getTime(cap_hill, B, "bicycling"), "seconds")
print("  Transit distance:", getTime(cap_hill, B, "transit"), "seconds\n")

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

""""
# AB
print(f"AB - {nameA} → {nameB}")
print("  Driving distance:", getTime(A, B, "driving"), "seconds")
print("  Walking distance:", getTime(A, B, "walking"), "seconds")
print("  Bicycling distance:", getTime(A, B, "bicycling"), "seconds")
print("  Transit distance:", getTime(A, B, "transit"), "seconds\n")

# BC
print(f"BC - {nameB} → {nameC}")
print("  Driving distance:", getTime(B, C, "driving"), "seconds")
print("  Walking distance:", getTime(B, C, "walking"), "seconds")
print("  Bicycling distance:", getTime(B, C, "bicycling"), "seconds")
print("  Transit distance:", getTime(B, C, "transit"), "seconds\n")

# CD
print(f"CD - {nameC} → {nameD}")
print("  Driving distance:", getTime(C, D, "driving"), "seconds")
print("  Walking distance:", getTime(C, D, "walking"), "seconds")
print("  Bicycling distance:", getTime(C, D, "bicycling"), "seconds")
print("  Transit distance:", getTime(C, D, "transit"), "seconds\n")

"""