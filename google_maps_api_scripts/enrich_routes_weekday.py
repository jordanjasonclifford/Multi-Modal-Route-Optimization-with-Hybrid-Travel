import pandas as pd
import requests
import json
import time
from datetime import datetime, timedelta
from geopy.distance import geodesic

# Your Google Maps API key
API_KEY = "AIzaSyBUsvoSqx1ru5MF5F9HCnYwOMgSVSdoBQo"

def is_drivable(A, B, min_distance_m=50):
    """Check if the origin and destination are far enough for a valid driving route"""
    return geodesic(A, B).meters > min_distance_m

def getTravelMetrics(A, B, m, departure_time=None):
    """
    Calls Google Maps Distance Matrix API to get duration (s) and distance (m)
    A, B: tuples of (lat, lon)
    m: mode of transport (driving, walking, bicycling, transit)
    departure_time: UNIX timestamp (optional)
    """
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": f"{A[0]},{A[1]}",
        "destinations": f"{B[0]},{B[1]}",
        "mode": m,
        "units": "metric",
        "key": API_KEY
    }

    if m in ["driving", "transit"] and departure_time:
        # Make sure departure_time is in the future
        now_ts = int(datetime.utcnow().timestamp())
        if departure_time <= now_ts:
            departure_time = now_ts + 300  # 5 minutes into the future

        params["departure_time"] = departure_time

    try:
        response = requests.get(base_url, params=params)
        print(f"→ Request URL: {response.url}")  # DEBUG

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK" and data["rows"]:
                elements = data["rows"][0].get("elements", [])
                if elements and elements[0]["status"] == "OK":
                    duration = elements[0]["duration"]["value"]
                    distance = elements[0]["distance"]["value"]
                    return duration, distance
                else:
                    print(f"Google API element status: {elements[0].get('status')}")
            else:
                print(f"Google API top-level status or missing rows: {data.get('status')}")
                print("→ Full response:\n", json.dumps(data, indent=2))
        else:
            print(f"HTTP error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"API exception for {A} to {B} via {m} at {departure_time}: {e}")

    return None, None


# Load the CSV file
df = pd.read_csv("seattle_timed_test.csv")
results = []

# Loop over each day of the week (0 = Monday, 6 = Sunday)
for day_offset in range(7):
    weekday_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=day_offset)
    weekday_name = weekday_date.strftime('%A')
    print(f"\n===== Processing {weekday_name} =====")

    for hour in range(6, 23):  # From 6 AM to 10 PM
        departure_time = weekday_date.replace(hour=hour)
        departure_timestamp = int(departure_time.timestamp())
        departure_iso = departure_time.isoformat()

        print(f"\n--- {weekday_name}, {hour}:00 ---")

        for i, row in df.iterrows():
            origin = (row["origin_lat"], row["origin_lng"])
            destination = (row["destination_lat"], row["destination_lng"])
            mode = row["mode"]

            # Skip invalid driving trips that are too short
            if mode == "driving" and not is_drivable(origin, destination):
                print(f"[{weekday_name} {hour}:00] {i+1}/{len(df)} - driving SKIPPED (too close) {row['origin_place']} → {row['destination_place']}")
                duration, distance = None, None
            else:
                duration, distance = getTravelMetrics(origin, destination, mode, departure_timestamp)

            print(f"[{weekday_name} {hour}:00] {i+1}/{len(df)} - {mode} {row['origin_place']} → {row['destination_place']} → {duration}s, {distance}m")

            results.append({
                "weekday": weekday_name,
                "departure_hour": hour,
                "departure_time_iso": departure_iso,
                "departure_timestamp": departure_timestamp,
                "origin_place": row["origin_place"],
                "origin_lat": row["origin_lat"],
                "origin_lng": row["origin_lng"],
                "destination_place": row["destination_place"],
                "destination_lat": row["destination_lat"],
                "destination_lng": row["destination_lng"],
                "mode": mode,
                "duration_sec": duration,
                "distance_m": distance
            })

            time.sleep(1)  # API rate limit

# Export to CSV
df_out = pd.DataFrame(results)
df_out.to_csv("seattleroutes_spaceneedle_timed.csv", index=False)
print("\nSaved to seattleroutes_spaceneedle_timed.csv")
