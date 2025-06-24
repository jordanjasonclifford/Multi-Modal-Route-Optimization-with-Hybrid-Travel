import requests
import json
from geopy.distance import geodesic  # For direct distance calculation


def getDistance(A, B, m):
    if m == "direct":
        return geodesic(A, B).meters


    API_KEY = "AIzaSyBUsvoSqx1ru5MF5F9HCnYwOMgSVSdoBQo"
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

fourDestinations = [
    ("Benaroya Hall", (47.60814199288301, -122.3368087995574)),
    ("Pike Place Market", (47.60939849082073, -122.3418399195103)),
    ("Westlake Center", (47.61204391377087, -122.33748668957276)),
    ("UW Station", (47.65027972126398, -122.30374414254722))
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
print("  Transit distance:", getDistance(A, B, "transit"), "meters")
print()

# BC
print(f"BC - {nameB} → {nameC}")
print("  Driving distance:", getDistance(B, C, "driving"), "meters")
print("  Walking distance:", getDistance(B, C, "walking"), "meters")
print("  Bicycling distance:", getDistance(B, C, "bicycling"), "meters")
print("  Transit distance:", getDistance(B, C, "transit"), "meters")
print()

# CD
print(f"CD - {nameC} → {nameD}")
print("  Driving distance:", getDistance(C, D, "driving"), "meters")
print("  Walking distance:", getDistance(C, D, "walking"), "meters")
print("  Bicycling distance:", getDistance(C, D, "bicycling"), "meters")
print("  Transit distance:", getDistance(C, D, "transit"), "meters")
print()

'''
driving_distance = getDistance(sculpture_park, spaceneedle, "driving")
walking_distance = getDistance(sculpture_park, spaceneedle, "walking")
bicycling_distance = getDistance(sculpture_park, spaceneedle, "bicycling")
transit_distance = getDistance(sculpture_park, spaceneedle, "transit")

driving_distance2 = getDistance(spaceneedle, pike_place, "driving")
walking_distance2 = getDistance(spaceneedle, pike_place, "walking")
bicycling_distance2 = getDistance(spaceneedle, pike_place, "bicycling")
transit_distance2 = getDistance(spaceneedle, pike_place, "transit")

driving_distance3 = getDistance(pike_place, uwub_station, "driving")
walking_distance3 = getDistance(pike_place, uwub_station, "walking")
bicycling_distance3 = getDistance(pike_place, uwub_station, "bicycling")
transit_distance3 = getDistance(pike_place, uwub_station, "transit")


print("AB - Sculpture Park to Space Needle ")
print("Driving distance:", driving_distance, "meters")
print("Walking distance:", walking_distance, "meters")
print("Bicycling distance:", bicycling_distance, "meters")
print("Transit distance:", transit_distance, "meters")


print("BC - Space Needle to Pike Place")
print("Driving distance:", driving_distance2, "meters")
print("Walking distance:", walking_distance2, "meters")
print("Bicycling distance:", bicycling_distance2, "meters")
print("Transit distance:", transit_distance2, "meters")

print("CD - Pike Place to UW Station")
print("Driving distance:", driving_distance3, "meters")
print("Walking distance:", walking_distance3, "meters")
print("Bicycling distance:", bicycling_distance3, "meters")
print("Transit distance:", transit_distance3, "meters")

# 1 A- D
# AB - Pop Cult to Space Needle 
# BC - Space Needle to seattle aquarium
# CD - Seattle aquarium to sculp park


# museum_pop_culture = (47.621470125609314, -122.3481282699205)
# spaceneedle = (47.620475865973454, -122.34922662355609)
# seattle_aquarium = (47.607381610552146, -122.34296367108706)
# sculpture_park = (47.616598558883176, -122.35531073027671)
'''