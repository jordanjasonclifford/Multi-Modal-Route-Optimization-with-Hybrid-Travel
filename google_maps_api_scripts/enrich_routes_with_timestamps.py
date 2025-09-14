import pandas as pd
import requests
from time import sleep

# CONFIGURATION
API_KEY = ""
base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
SLEEP_SECONDS = 2

# Load files
routes_df = pd.read_csv("seattle_timed_test.csv")
timestamps_df = pd.read_csv("UNIX_Timestamps.csv")

# Use 'timestamp' column as list of UNIX timestamps
timestamps_df.columns = timestamps_df.columns.str.strip()
timestamps = timestamps_df["timestamp"].astype(int).tolist()

# All four modes
all_modes = ["driving", "transit", "walking", "bicycling"]

# API call function
def get_metrics(orig, dest, mode, departure_time):
    params = {
        "origins": f"{orig[0]},{orig[1]}",
        "destinations": f"{dest[0]},{dest[1]}",
        "mode": mode,
        "key": API_KEY
    }

    if mode in ["driving", "transit"] and departure_time is not None:
        params["departure_time"] = departure_time
        params["traffic_model"] = "best_guess"
    # if mode == "driving":
        # params["traffic_model"] = "best_guess"

    print(f"DEBUG: Calling API with departure_time = {departure_time} for mode={mode}")

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        element = data["rows"][0]["elements"][0]
        distance = element["distance"]["value"]
        duration = element["duration"]["value"]

        duration_traffic = (
            element.get("duration_in_traffic", {}).get("value", -1)
            if mode == "driving" else None
        )

        return distance, duration, duration_traffic
    except Exception as e:
        print(f"⚠️ API error [{mode}] {orig}→{dest} @ {departure_time}: {e}")
        return -1, -1, None

# Output results
results = []

# Static mode cache: {(origin, destination, mode): (distance, duration)}
static_cache = {}

# Get all unique OD pairs
unique_pairs = routes_df.drop_duplicates(
    subset=["origin_place", "origin_lat", "origin_lng", 
            "destination_place", "destination_lat", "destination_lng"]
)

# Main processing loop
for ts in timestamps:
    print(f"\n⏱ Processing timestamp: {ts}")

    for _, row in unique_pairs.iterrows():
        origin = (row["origin_lat"], row["origin_lng"])
        dest = (row["destination_lat"], row["destination_lng"])
        origin_name = row["origin_place"]
        dest_name = row["destination_place"]

        for mode in all_modes:
            ts_for_call = ts if mode in ["driving", "transit"] else None

            if mode in ["walking", "bicycling"]:
                pair_key = (origin, dest, mode)
                if pair_key in static_cache:
                    dist, dur = static_cache[pair_key]
                    dur_traffic = None
                else:
                    dist, dur, _ = get_metrics(origin, dest, mode, None)
                    static_cache[pair_key] = (dist, dur)
                    dur_traffic = None
            else:
                dist, dur, dur_traffic = get_metrics(origin, dest, mode, ts_for_call)

            print(f"📡 {origin_name} → {dest_name} @ {ts} [{mode}] = {dist}m, {dur}s (traffic: {dur_traffic})")

            results.append({
                "timestamp": ts,
                "origin_place": origin_name,
                "origin_lat": origin[0],
                "origin_lng": origin[1],
                "destination_place": dest_name,
                "destination_lat": dest[0],
                "destination_lng": dest[1],
                "mode": mode,
                "distance_meters": dist,
                "duration_seconds": dur,
                "duration_in_traffic": dur_traffic,
                "source": "api"
            })

            sleep(SLEEP_SECONDS)

# Save to CSV
out_df = pd.DataFrame(results)
out_df.to_csv("enriched_routes_by_timestamp_whs_to_mpc.csv", index=False)
print("\nAll done! Saved to enriched_routes_by_timestamp_whs_to_mpc.csv")
