import pandas as pd
import time
import datetime
import requests
import json
from geopy.distance import geodesic

API_KEY = "AIzaSyBUsvoSqx1ru5MF5F9HCnYwOMgSVSdoBQo"   

def getTravelMetrics(A, B, m):
    if m == "direct":
        return geodesic(A, B).meters, 0

    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    # Set target time to 8:30 AM
    target_time = datetime.datetime.now().replace(hour=8, minute=30, second=0, microsecond=0)
    if target_time < datetime.datetime.now():
        target_time += datetime.timedelta(days=1)
    departure_timestamp = int(time.mktime(target_time.timetuple()))

    params = {
        "origins": f"{A[0]},{A[1]}",
        "destinations": f"{B[0]},{B[1]}",
        "mode": m,
        "units": "metric",
        "key": API_KEY,
    }

    # Add departure time for driving or transit
    if m in ["driving", "transit"]:
        params["departure_time"] = departure_timestamp

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = json.loads(response.text)
        if data["status"] == "OK":
            try:
                distance_meters = data["rows"][0]["elements"][0]["distance"]["value"]
                duration_seconds = data["rows"][0]["elements"][0]["duration"]["value"]
                return distance_meters, duration_seconds
            except (KeyError, IndexError):
                pass

    return None, None

def enrich_routes(csv_path, output_path):
    df = pd.read_csv(csv_path)
    enriched_data = []

    for idx, row in df.iterrows():
        origin = (row["origin_lat"], row["origin_lng"])
        destination = (row["destination_lat"], row["destination_lng"])
        mode = row["mode"]

        distance, duration = getTravelMetrics(origin, destination, mode)
        enriched_data.append({
            "dataset": row["dataset"],
            "origin_place": row["origin_place"],
            "destination_place": row["destination_place"],
            "origin_lat": origin[0],
            "origin_lng": origin[1],
            "destination_lat": destination[0],
            "destination_lng": destination[1],
            "mode": mode,
            "distance_m": distance,
            "duration_s": duration
        })

    enriched_df = pd.DataFrame(enriched_data)
    enriched_df.to_csv(output_path, index=False)
    print(f"Enriched data saved to {output_path}")

# Example usage:

enrich_routes("Prepared_Route_Cases.csv", "Enriched_Seattle_Routes_Two.csv")
