import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

# === Load and combine data ===
df1 = pd.read_csv("enriched_routes_sn_to_wp_with_daytime.csv")
df2 = pd.read_csv("enriched_routes_wp_to_st_with_daytime.csv")
df = pd.concat([df1, df2], ignore_index=True)

# === Use 'duration_in_traffic' instead of 'duration_seconds' for driving ===
df.loc[df["mode"] == "driving", "duration_seconds"] = df.loc[df["mode"] == "driving", "duration_in_traffic"]

# Drop rows with missing or NaN durations
df = df.dropna(subset=["duration_seconds"])

# === Pivot data: each row is a full trip with all 4 modes ===
pivot = df.pivot_table(
    index=["day", "time", "timestamp", "origin_place", "origin_lat", "origin_lng",
           "destination_place", "destination_lat", "destination_lng"],
    columns="mode",
    values="duration_seconds"
).reset_index()

# Drop rows with any missing modes
pivot = pivot.dropna(subset=["driving", "transit", "walking", "bicycling"])

# === Create label column ===
pivot["best_mode"] = pivot[["driving", "transit", "walking", "bicycling"]].idxmin(axis=1)

# === Feature engineering ===
features = pivot[[
    "origin_lat", "origin_lng", "destination_lat", "destination_lng", "timestamp"
]]
labels = pivot["best_mode"]

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.25, random_state=42)

# === Train classifier ===
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# === Evaluate ===
y_pred = clf.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
