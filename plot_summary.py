import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the enriched dataset
df = pd.read_csv("Enriched_Seattle_Routes.csv")

# Drop any rows with missing values
df = df.dropna(subset=["duration_sec", "distance_m"])

# Convert seconds to minutes and meters to kilometers
df["duration_min"] = df["duration_sec"] / 60
df["distance_km"] = df["distance_m"] / 1000

# Set visual style
sns.set(style="whitegrid")

# Plot 1: Average Travel Duration by Mode
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="mode", y="duration_min", ci=None, estimator=np.mean)
plt.title("Average Travel Duration by Mode")
plt.ylabel("Duration (minutes)")
plt.xlabel("Mode of Transport")
plt.tight_layout()
plt.savefig("avg_duration_by_mode.png")
plt.close()

# Plot 2: Average Travel Distance by Mode
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="mode", y="distance_km", ci=None, estimator=np.mean)
plt.title("Average Travel Distance by Mode")
plt.ylabel("Distance (km)")
plt.xlabel("Mode of Transport")
plt.tight_layout()
plt.savefig("avg_distance_by_mode.png")
plt.close()

# Plot 3: Duration Distribution by Mode (Boxplot)
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="mode", y="duration_min")
plt.title("Travel Duration Distribution by Mode")
plt.ylabel("Duration (minutes)")
plt.xlabel("Mode of Transport")
plt.tight_layout()
plt.savefig("duration_distribution_by_mode.png")
plt.close()

print("Plots saved: avg_duration_by_mode.png, avg_distance_by_mode.png, duration_distribution_by_mode.png")
