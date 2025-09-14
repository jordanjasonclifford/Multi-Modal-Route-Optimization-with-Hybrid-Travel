import pandas as pd
import requests
import json
import time

def getTravelMetrics(A, B, m):
    """
    Calls Google Maps Distance Matrix API to get duration (s) and distance (m)
    A, B: tuples of (lat, lon)
    m: mode of transport (driving, walking, bicycling, transit)
    Returns: (duration_in_seconds, distance_in_meters)
    """
    API_KEY = ""
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": f"{A[0]},{A[1]}",
        "destinations": f"{B[0]},{B[1]}",
        "mode": m,
        "units": "metric",
        "key": API_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            element = data["rows"][0]["elements"][0]
            if element["status"] == "OK":
                duration = element["duration"]["value"]
                distance = element["distance"]["value"]
                return duration, distance
    except Exception as e:
        print(f"API error for {A} to {B} via {m}: {e}")

    return None, None


# Load prepared CSV
df = pd.read_csv("amazonhq_routes.csv")

# Add placeholders
durations = []
distances = []

# Loop through each row and call the API
for i, row in df.iterrows():
    origin = (row["origin_lat"], row["origin_lng"])
    destination = (row["destination_lat"], row["destination_lng"])
    mode = row["mode"]

    duration, distance = getTravelMetrics(origin, destination, mode)
    durations.append(duration)
    distances.append(distance)

    print(f"{i+1}/{len(df)}: {mode} from {row['origin_place']} to {row['destination_place']} → {duration}s, {distance}m")
    time.sleep(1)  # polite delay for rate limiting

# Add results to DataFrame
df["duration_sec"] = durations
df["distance_m"] = distances

# Save the enriched data
df.to_csv("06seattleroutes_amazonhq.csv", index=False)
print("Data saved to 06seattleroutes_amazonhq.csv")
