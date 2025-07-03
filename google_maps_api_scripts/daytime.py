import pandas as pd
from datetime import datetime

# === Load and Convert Timestamps ===
timestamps_df = pd.read_csv("UNIX_Timestamps.csv")
timestamps_df.columns = timestamps_df.columns.str.strip()
timestamps_df["readable_time"] = timestamps_df["timestamp"].apply(
    lambda x: datetime.utcfromtimestamp(int(x)).strftime('%A %Y-%m-%d %H:%M:%S')
)

# === Load Enriched Route Files ===
sn_to_wp_df = pd.read_csv("enriched_routes_by_timestamp_sn_to_wp.csv")
wp_to_st_df = pd.read_csv("enriched_routes_by_timestamp_wp_to_st.csv")

# === Merge to Add 'day_time' ===
sn_to_wp_merged = pd.merge(timestamps_df, sn_to_wp_df, on="timestamp", how="right")
wp_to_st_merged = pd.merge(timestamps_df, wp_to_st_df, on="timestamp", how="right")

sn_to_wp_merged.rename(columns={"readable_time": "day_time"}, inplace=True)
wp_to_st_merged.rename(columns={"readable_time": "day_time"}, inplace=True)

# === Reorder Columns to Put 'day_time' First ===
sn_to_wp_cols = ["day_time"] + [col for col in sn_to_wp_merged.columns if col != "day_time"]
wp_to_st_cols = ["day_time"] + [col for col in wp_to_st_merged.columns if col != "day_time"]

sn_to_wp_final = sn_to_wp_merged[sn_to_wp_cols]
wp_to_st_final = wp_to_st_merged[wp_to_st_cols]

# === Save Final CSVs ===
sn_to_wp_final.to_csv("enriched_routes_sn_to_wp_with_daytime.csv", index=False)
wp_to_st_final.to_csv("enriched_routes_wp_to_st_with_daytime.csv", index=False)
