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
    "enriched_routes_by_timestamp_bh_to_cts.csv",
    "enriched_routes_by_timestamp_cap_to_saq.csv",
    "enriched_routes_by_timestamp_cap_to_wfg.csv",
    "enriched_routes_by_timestamp_cg_to_bh.csv",
    "enriched_routes_by_timestamp_ppm_to_cap.csv",
    "enriched_routes_by_timestamp_sam_to_ss.csv",
    "enriched_routes_by_timestamp_sam_to_whs.csv",
    "enriched_routes_by_timestamp_sn_to_bh.csv",
    "enriched_routes_by_timestamp_whs_to_if.csv",
    "enriched_routes_by_timestamp_wp_to_idcts.csv",
    "enriched_routes_by_timestamp_wp_to_sft.csv",
    "enriched_routes_by_timestamp_wp_to_tmp.csv",
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
