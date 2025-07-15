import pandas as pd
import matplotlib.pyplot as plt

# === Load the CSVs ===
summary_df = pd.read_csv("qlearning_all_policy_summary.csv")
freq_df = pd.read_csv("qlearning_all_mode_frequencies.csv")

# === Plot 1: Mode Frequency Over Hours ===
plt.figure(figsize=(12, 6))
for mode in ['driving', 'transit', 'bicycling', 'walking']:
    plt.plot(freq_df['hour_of_day'], freq_df[mode], marker='o', label=mode)

plt.title("Q-Learning Mode Frequency per Hour (Ideal Routes)")
plt.xlabel("Hour of Day")
plt.ylabel("Frequency Across 10 Runs")
plt.legend()
plt.grid(True)
plt.xticks(range(24))
plt.tight_layout()
plt.show()

# === Plot 2: Final Mode by Hour (Majority Vote) ===
plt.figure(figsize=(12, 4))
colors = {
    'driving': '#1f77b4',
    'transit': '#2ca02c',
    'bicycling': '#ff7f0e',
    'walking': '#d62728'
}
bar_colors = summary_df['final_mode'].map(colors)

plt.bar(summary_df['hour_of_day'], [1]*len(summary_df), color=bar_colors)
plt.title("Final Chosen Mode per Hour (Majority Vote)")
plt.xlabel("Hour of Day")
plt.yticks([])
plt.xticks(range(24))
plt.grid(axis='x')
for i, mode in enumerate(summary_df['final_mode']):
    plt.text(i, 0.5, mode, ha='center', va='center', fontsize=8, color='white')
plt.tight_layout()
plt.show()

# === Plot 3: Agreement Score ===
plt.figure(figsize=(12, 5))
plt.plot(summary_df['hour_of_day'], summary_df['agreement'], color='black', marker='o')
plt.title("Agreement Score per Hour (How Many Runs Agreed with Majority)")
plt.xlabel("Hour of Day")
plt.ylabel("Agreement (out of 10)")
plt.grid(True)
plt.xticks(range(24))
plt.tight_layout()
plt.show()
