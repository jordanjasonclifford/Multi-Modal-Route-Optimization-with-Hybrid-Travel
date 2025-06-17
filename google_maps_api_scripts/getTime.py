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
paradise_coords = (36.0968, -115.1703)
freemont_street_coords = (36.1699, -115.1398)

museum_of_flight = (47.5185223071121, -122.296854586384)
bellevue_square = (47.6157165377573, -122.203733607983)




driving_time = getTime(paradise_coords, freemont_street_coords, "driving")
walking_time = getTime(paradise_coords, freemont_street_coords, "walking")

driving_distance2 = getTime(museum_of_flight, bellevue_square, "driving")
walking_distance2 = getTime(museum_of_flight, bellevue_square, "walking")
bicycling_distance2 = getTime(museum_of_flight, bellevue_square, "bicycling")
transit_distance2 = getTime(museum_of_flight, bellevue_square, "transit")

print("Paradise to Freemont Driving time:", driving_time, "seconds")
print("Paradise to Freemont Walking time:", walking_time, "seconds")

print("Seattle case:")
print("Driving distance:", driving_distance2, "seconds")
print("Walking distance:", walking_distance2, "seconds")
print("Bicycling distance:", bicycling_distance2, "seconds")
print("Transit distance:", transit_distance2, "seconds")
