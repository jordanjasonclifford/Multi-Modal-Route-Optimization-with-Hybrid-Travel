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
paradise_coords = (36.0968, -115.1703)
freemont_street_coords = (36.1699, -115.1398)

museum_of_flight = (47.5185223071121, -122.296854586384)
bellevue_square = (47.6157165377573, -122.203733607983)


driving_distance = getDistance(paradise_coords, freemont_street_coords, "driving")
walking_distance = getDistance(paradise_coords, freemont_street_coords, "walking")
bicycling_distance = getDistance(paradise_coords, freemont_street_coords, "bicycling")
transit_distance = getDistance(paradise_coords, freemont_street_coords, "transit")

driving_distance2 = getDistance(museum_of_flight, bellevue_square, "driving")
walking_distance2 = getDistance(museum_of_flight, bellevue_square, "walking")
bicycling_distance2 = getDistance(museum_of_flight, bellevue_square, "bicycling")
transit_distance2 = getDistance(museum_of_flight, bellevue_square, "transit")


print("FROM PARADISE TO FREEMONT")
print("Driving distance:", driving_distance, "meters")
print("Walking distance:", walking_distance, "meters")
print("Bicycling distance:", bicycling_distance, "meters")
print("Transit distance:", transit_distance, "meters")


print("Seattle case:")
print("Driving distance:", driving_distance2, "meters")
print("Walking distance:", walking_distance2, "meters")
print("Bicycling distance:", bicycling_distance2, "meters")
print("Transit distance:", transit_distance2, "meters")