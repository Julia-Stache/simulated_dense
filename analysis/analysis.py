from pathlib import Path
import numpy as np
import pandas as pd
import os  
from collections import Counter
import seaborn as sns

#loading paths to data
script_dir = Path(__file__).resolve().parent
path_demo = script_dir.parent / "data" / "synthetic_fibromyalgia_participant_demographics.csv" #demographics path
path_data = script_dir.parent / "data" / "synthetic_fibromyalgia_weekly_dataset.csv"           #dataset path
demo = pd.read_csv(path_demo)  #load demographics
data = pd.read_csv(path_data)  #load dataset


#Explore demographics
print(f"Age range: {demo['age_years'].min()}–{demo['age_years'].max()} years")
print("Distribution of education:", demo["education_level"].value_counts(dropna=False))

#Explore weekly results - starting with current pain
# Separate the two groups
fm = data[data["group"] == "FM"]
hc = data[data["group"] == "HC"]

# Create two plots side by side
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

for ax, df, group_name in zip(
    axes,
    [fm, hc],
    ["Fibromyalgia (FM)", "Healthy controls (HC)"]
):
    # Plot one line per participant
    for participant_id, participant in df.groupby("participant_id"):
        participant = participant.sort_values("week")

        ax.plot(
            participant["week"],
            participant["current_pain_0_10"],
            marker="o",
            alpha=0.5,
            label=participant_id
        )

    ax.set_title(group_name)
    ax.set_xlabel("Week")
    ax.set_xticks(range(1, 9))
    ax.set_ylim(0, 10)
    ax.grid(True, alpha=0.3)

axes[0].set_ylabel("Current pain (0–10)")

plt.tight_layout()
plt.show()

##try and convert code key to .json
