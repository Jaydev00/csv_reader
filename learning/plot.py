import matplotlib.pyplot as plt
import numpy as np

# data from https://allisonhorst.github.io/palmerpenguins/
#    "63.33_nightly_n",

barTitles = (
    "63.33_nightly_q",
    "63.33_nightly_n",
)
weight_counts = {
    "Pass": np.array([129, 77]),
    "Fail": np.array([39, 19]),
}
percentages = np.zeros(2)
passArray = weight_counts["Pass"]
failArray = weight_counts["Fail"]
for i in range(len(barTitles)):
    percentages[i] = 100 * np.round(passArray[i] / (passArray[i]+failArray[i]), 3)
percentages_labels = []
for entry in percentages:
    percentages_labels.append(str(entry) + "% ")
    
    
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(2)

customGreen = (0.166,
               0.720,
               0.193,
               1)

for category, weight_count in weight_counts.items():
    if category == "Pass":
        p = ax.bar(barTitles, weight_count, width, label=category, bottom=bottom, color=customGreen ,linewidth=10)
        ax.bar_label(p, label_type='center', labels=percentages_labels)
    if category == "Fail":
        p = ax.bar(barTitles, weight_count, width, label=category, bottom=bottom, color="red",linewidth=10)
    bottom += weight_count
    print(bottom)

ax.set_title("Number of penguins with above average body mass")
ax.legend(loc="upper right", reverse=True)

plt.show()