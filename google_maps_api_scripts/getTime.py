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
print("  Driving distance:", getTime(A, B, "driving"), "seconds")
print("  Walking distance:", getTime(A, B, "walking"), "seconds")
print("  Bicycling distance:", getTime(A, B, "bicycling"), "seconds")
print("  Transit distance:", getTime(A, B, "transit"), "seconds")
print()

# BC
print(f"BC - {nameB} → {nameC}")
print("  Driving distance:", getTime(B, C, "driving"), "seconds")
print("  Walking distance:", getTime(B, C, "walking"), "seconds")
print("  Bicycling distance:", getTime(B, C, "bicycling"), "seconds")
print("  Transit distance:", getTime(B, C, "transit"), "seconds")
print()

# CD
print(f"CD - {nameC} → {nameD}")
print("  Driving distance:", getTime(C, D, "driving"), "seconds")
print("  Walking distance:", getTime(C, D, "walking"), "seconds")
print("  Bicycling distance:", getTime(C, D, "bicycling"), "seconds")
print("  Transit distance:", getTime(C, D, "transit"), "seconds")
print()


'''
driving_distance = getTime(sculpture_park, spaceneedle, "driving")
walking_distance = getTime(sculpture_park, spaceneedle, "walking")
bicycling_distance = getTime(sculpture_park, spaceneedle, "bicycling")
transit_distance = getTime(sculpture_park, spaceneedle, "transit")

driving_distance2 = getTime(spaceneedle, pike_place, "driving")
walking_distance2 = getTime(spaceneedle, pike_place, "walking")
bicycling_distance2 = getTime(spaceneedle, pike_place, "bicycling")
transit_distance2 = getTime(spaceneedle, pike_place, "transit")

driving_distance3 = getTime(pike_place, uwub_station, "driving")
walking_distance3 = getTime(pike_place, uwub_station, "walking")
bicycling_distance3 = getTime(pike_place, uwub_station, "bicycling")
transit_distance3 = getTime(pike_place, uwub_station, "transit")


print("AB - Sculpture Park to Space Needle ")
print("Driving time:", driving_distance, "seconds")
print("Walking time:", walking_distance, "seconds")
print("Bicycling time:", bicycling_distance, "seconds")
print("Transit time:", transit_distance, "seconds")


print("BC - Space Needle to Pike Place")
print("Driving time:", driving_distance2, "seconds")
print("Walking time:", walking_distance2, "seconds")
print("Bicycling time:", bicycling_distance2, "seconds")
print("Transit time:", transit_distance2, "seconds")

print("CD - Pike Place to UW Station")
print("Driving time:", driving_distance3, "seconds")
print("Walking time:", walking_distance3, "seconds")
print("Bicycling time:", bicycling_distance3, "seconds")
print("Transit time:", transit_distance3, "seconds")

# 1 A- D
# AB - Pop Cult to Space Needle 
# BC - Space Needle to seattle aquarium
# CD - Seattle aquarium to sculp park

# 2 A - D 
# AB - Benaroya hall to art museum 
# BC - art museum to pike place
# CD - pike place to aquarium


# museum_pop_culture = (47.621470125609314, -122.3481282699205)
# spaceneedle = (47.620475865973454, -122.34922662355609)
# seattle_aquarium = (47.607381610552146, -122.34296367108706)
# sculpture_park = (47.616598558883176, -122.35531073027671)
'''