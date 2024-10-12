import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

base_path = "../simulation_runs/"


# Define the path where to search for folders
search_path = "../simulation_runs"  # Change this to your desired path

# Create an array of folders found in the given path
folders = [
    f for f in os.listdir(search_path) if os.path.isdir(os.path.join(search_path, f))
]

pattern = re.compile(r"^dt_([\d\.]+)_steps_(\d+)$")

values = []

mass = 70
gamma = 100
k = 10000
A = 1
analitical = (
    lambda t: A
    * np.exp(-gamma * t / (2 * mass))
    * np.cos(np.sqrt(k / mass - (gamma / (2 * mass)) ** 2) * t)
)
methods = ["Beeman", "Verlet", "Gear5"]
folders.sort()
print(folders)
for folder in folders:
    match = pattern.match(folder)
    if match:
        dt_value = float(match.group(1))  # Extract and convert dt_value to float
        steps_value = int(match.group(2))  # Extract and convert steps_value to int
        beeman = 0.0
        verlet = 0.0
        gear5 = 0.0
        for method in methods:
            with open(f"{base_path}{folder}/{method}_output.csv") as f:
                df = pd.read_csv(f)
                analitical_values = [analitical(t) for t in df["t"]]
                analitical_values = np.array(analitical_values)
                ecm = np.sum((df["r"] - analitical_values) ** 2) / steps_value
                print(steps_value)
                if method == "Beeman":
                    beeman = ecm
                elif method == "Verlet":
                    verlet = ecm
                else:
                    gear5 = ecm
        values.append((dt_value, beeman, verlet, gear5))
print(values)
fig, ax = plt.subplots(figsize=(10, 5))

ax.errorbar(
    [value[0] for value in values],
    [value[1] for value in values],
    label="Beeman",
    color="orange",
    linestyle="dashed",
    marker="o",
)
ax.errorbar(
    [value[0] for value in values],
    [value[2] for value in values],
    label="Verlet",
    color="red",
    linestyle="dashed",
    marker="o",
)
ax.errorbar(
    [value[0] for value in values],
    [value[3] for value in values],
    label="Gear5",
    color="green",
    linestyle="dashed",
    marker="o",
)

ax.set_xscale("log")

ax.set_xlabel("dt")
ax.set_ylabel("ECM")
ax.legend(shadow=True, fancybox=True, loc=(1.05, 0.7))
