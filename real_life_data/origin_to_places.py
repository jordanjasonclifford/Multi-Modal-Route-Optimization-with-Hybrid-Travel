import pandas as pd

# Load the Seattle POI data
df = pd.read_csv("SeattlePOI.csv")

# Split Coordinates into lat/lng columns
df[['lat', 'lng']] = df['Coordinates'].str.split(',', expand=True)
df['lat'] = df['lat'].astype(float)
df['lng'] = df['lng'].astype(float)

# Define origin
origin = df[df['Place'] == 'Cal Anderson Park'].iloc[0]

# Destination: All except origin
destinations = df[df['Place'] != 'Cal Anderson Park']

# Modes
modes = ['driving', 'walking', 'bicycling', 'transit']

# Generate rows
rows = []
for _, dest in destinations.iterrows():
    for mode in modes:
        rows.append({
            'origin_place': origin['Place'],
            'origin_lat': origin['lat'],
            'origin_lng': origin['lng'],
            'destination_place': dest['Place'],
            'destination_lat': dest['lat'],
            'destination_lng': dest['lng'],
            'mode': mode
        })

# Save output
output_df = pd.DataFrame(rows)
output_df.to_csv("cal_anderson_park_routes.csv", index=False)
print("Saved to space_needle_routes.csv")
