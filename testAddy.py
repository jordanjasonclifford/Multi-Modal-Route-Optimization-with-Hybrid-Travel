import requests
import time


api_key = "AIzaSyBUsvoSqx1ru5MF5F9HCnYwOMgSVSdoBQo"
origin = "10788+Rivendell+Ave+Las+Vegas+NV+89135"
destination = "11330+Westbrook+Mill+Ln+Fairfax+VA+22030"
departure_time = int(time.time()) + 3600  # Current time + 1 hour (in seconds)


url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&departure_time={departure_time}&key={api_key}"


response = requests.get(url)


if response.status_code == 200:
    data = response.json()
    routes = data.get("routes", [])  # Handle cases where "routes" might be missing
    if routes:
        legs = routes[0].get("legs", [])  # Handle cases where "legs" might be missing
        if legs:
            distance = legs[0]["distance"]["text"]
            duration = legs[0]["duration"]["text"]  # Get the duration as well
            print("Distance:", distance, "\nDuration:", duration)
        else:
            print("No legs found in the route.")
    else:
        print("No routes found for the given parameters.")
else:
    print("Error:", response.status_code, response.json().get("error_message", "Unknown error"))  # More detailed error info



