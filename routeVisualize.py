import requests
import polyline
import folium

API_KEY = "AIzaSyBUsvoSqx1ru5MF5F9HCnYwOMgSVSdoBQo"  # Replace with your real key

routes = [
    {
        "origin": "King Street Station, Seattle, WA",
        "destination": "Tukwila Station, WA",
        "mode": "transit",
        "color": "blue"
    },
    {
        "origin": "SeaTac Airport, WA",
        "destination": "Capitol Hill Station, Seattle, WA",
        "mode": "bicycling",
        "color": "green"
    },
    {
        "origin": "Fremont, Seattle, WA",
        "destination": "Bellevue, WA",
        "mode": "driving",
        "color": "red"
    }
]

# Create a base map centered around Seattle
seattle_map = folium.Map(location=[47.6062, -122.3321], zoom_start=11)

for route in routes:
    response = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json",
        params={
            "origin": route["origin"],
            "destination": route["destination"],
            "mode": route["mode"],
            "key": API_KEY
        }
    ).json()
    
    if response["status"] == "OK":
        points = response["routes"][0]["overview_polyline"]["points"]
        coords = polyline.decode(points)
        folium.PolyLine(
            coords,
            color=route["color"],
            weight=5,
            opacity=0.8,
            tooltip=f"{route['mode'].capitalize()} Route"
        ).add_to(seattle_map)

# Save to file
seattle_map.save("seattle_routes_map.html")
print("Map saved as seattle_routes_map.html — open it in your browser.")
