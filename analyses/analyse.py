import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["font.family"] = "Helvetica Neue"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.labelcolor"] = "#444444"
plt.rcParams["xtick.labelsize"] = 11
plt.rcParams["ytick.labelsize"] = 11
plt.rcParams["axes.titlesize"] = 16

# Load the data
df = pd.read_csv("/Users/atharvapatharkar/Desktop/Projects/Biopharma-pipeline/data/pipeline_data.csv")

# Split into early and late stage
early = df[df["phase"].isin(["EARLY_PHASE1", "PHASE1", "PHASE2"])]
late = df[df["phase"].isin(["PHASE3", "PHASE4"])]

print("Early stage trials:", len(early))
print("Late stage trials:", len(late))
print()
print("Early stage sponsor breakdown:")
print(early["sponsor_class"].value_counts())
print()
print("Late stage sponsor breakdown:")
print(late["sponsor_class"].value_counts())
print("Trials per condition:")
print(df["condition"].value_counts())
print()

print("Early stage by condition:")
print(early["condition"].value_counts())
print()

print("Late stage by condition:")
print(late["condition"].value_counts())
print("Late stage by condition AND sponsor type:")
print(late.groupby(["condition", "sponsor_class"]).size())
print()

print("Early stage by condition AND sponsor type:")
print(early.groupby(["condition", "sponsor_class"]).size())

# Industry percentage by condition
print("Industry % by condition (all phases):")
total_by_condition = df.groupby(["condition", "sponsor_class"]).size().unstack(fill_value=0)
total_by_condition["total"] = total_by_condition.sum(axis=1)
total_by_condition["industry_%"] = (total_by_condition.get("INDUSTRY", 0) / total_by_condition["total"] * 100).round(1)
print(total_by_condition[["total", "industry_%"]])

print()

# Industry percentage by condition - LATE STAGE ONLY
print("Industry % by condition (late stage only):")
late_by_condition = late.groupby(["condition", "sponsor_class"]).size().unstack(fill_value=0)
late_by_condition["total"] = late_by_condition.sum(axis=1)
late_by_condition["industry_%"] = (late_by_condition.get("INDUSTRY", 0) / late_by_condition["total"] * 100).round(1)
print(late_by_condition[["total", "industry_%"]])

print("Industry % by condition (early stage only):")
early_by_condition = early.groupby(["condition", "sponsor_class"]).size().unstack(fill_value=0)
early_by_condition["total"] = early_by_condition.sum(axis=1)
early_by_condition["industry_%"] = (early_by_condition.get("INDUSTRY", 0) / early_by_condition["total"] * 100).round(1)
print(early_by_condition[["total", "industry_%"]])

# ── Chart 1: Total trials by condition (pie chart) ──
conditions = ["Anxiety", "Bipolar", "Depression/TRD", "PTSD", "Schizophrenia"]
total_trials = [29, 44, 48, 23, 47]

colors = ["#1B4F72", "#2E86C1", "#5DADE2", "#AED6F1", "#D6EAF8"]

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts = ax.pie(
    total_trials,
    colors=colors,
    startangle=90,
    pctdistance=0.75,
)

for text in texts:
    text.set_fontsize(12)

ax.set_title("CNS Pipeline: Trial Distribution by Condition", 
             fontsize=16, fontweight="bold", color="#1B4F72", pad=20)

plt.tight_layout()
plt.savefig("/Users/atharvapatharkar/Desktop/Projects/Biopharma-pipeline/data/chart1_total.png", dpi=300)
plt.close()
print("Saved chart1_total.png")