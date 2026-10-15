from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#defining paths and .csv files
script_dir = Path(__file__).resolve().parent
path_demo = script_dir.parent / "data" / "synthetic_fibromyalgia_participant_demographics.csv" #demographics path
path_data = script_dir.parent / "data" / "synthetic_fibromyalgia_weekly_dataset.csv"           #dataset path
demo = pd.read_csv(path_demo)  #load demographics
data = pd.read_csv(path_data)  #load dataset

#Explore demographics
print(f"Age range: {demo['age_years'].min()}–{demo['age_years'].max()} years")
print("Distribution of education:", demo["education_level"].value_counts(dropna=False))

#Explore weekly results


#Plotting data (used to also find outliers)
#defining groups
fm = data[data["group"] == "FM"]
hc = data[data["group"] == "HC"]


#Plotting line plots
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

#for current pain
for ax, df, group_name in zip(
    axes,
    [fm, hc],
    ["Fibromyalgia (FM)", "Healthy controls (HC)"] 
):
    # one line per subject
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

#checks which participant(s) has impossible current pain score, as seen in plot
data[
    (data["current_pain_0_10"] > 10) |
    (data["current_pain_0_10"] < 0)
]

#removes participant FM012's erroneous current pain score on week 3
data.loc[
    (data["participant_id"] == "FM012") & (data["week"] == 3),
    "current_pain_0_10"
] = np.nan


#Plots continued: looks at stroop response time
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

#for stroop reaction times
for ax, df, group_name in zip(
    axes,
    [fm, hc],
    ["Fibromyalgia (FM)", "Healthy controls (HC)"] 
):
    # one line per subject
    for participant_id, participant in df.groupby("participant_id"):
        participant = participant.sort_values("week")

        ax.plot(
            participant["week"],
            participant["stroop_mean_rt_ms"],
            marker="o",
            alpha=0.5,
            label=participant_id
        )

    ax.set_title(group_name)
    ax.set_xlabel("Week")
    ax.set_xticks(range(1, 9))
    ax.grid(True, alpha=0.3)

axes[0].set_ylabel("Stroop mean reaction time (ms)")

plt.tight_layout()
plt.show()

#Checking which participant has an impossibly low stroop reaction time
data[data["stroop_mean_rt_ms"] < 200]

#Changing impossible score to nan
data.loc[
    (data["participant_id"] == "FM004") & (data["week"] == 6),
    "stroop_mean_rt_ms"
] = np.nan
