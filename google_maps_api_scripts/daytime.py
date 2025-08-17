import pandas as pd
from datetime import datetime
import os

# === Load and Convert Timestamps ===
timestamps_df = pd.read_csv("UNIX_Timestamps.csv")
timestamps_df.columns = timestamps_df.columns.str.strip()
timestamps_df["readable_time"] = timestamps_df["timestamp"].apply(
    lambda x: datetime.utcfromtimestamp(int(x)).strftime('%A %Y-%m-%d %H:%M:%S')
)

# === List of CSVs to Process ===
route_files = [
    "new_train_combined_routes.csv"

]

# === Process Each File ===
for file in route_files:
    df = pd.read_csv(file)
    merged = pd.merge(timestamps_df, df, on="timestamp", how="right")
    merged.rename(columns={"readable_time": "day_time"}, inplace=True)

    # Reorder to put 'day_time' first
    ordered_cols = ["day_time"] + [col for col in merged.columns if col != "day_time"]
    final_df = merged[ordered_cols]

    # Save new file
    out_filename = file.replace(".csv", "_with_daytime.csv")
    final_df.to_csv(out_filename, index=False)
    print(f"✅ Saved: {out_filename}")
