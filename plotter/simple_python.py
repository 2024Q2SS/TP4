import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

base_path = "../simulation_runs/"
pattern = re.compile(r"^ecm_dt_(([\d\.]+)|([\d\.]+E-[\d]+))\.csv$")
# v_ecm = np.sum((df["v"] - df["a"]) ** 2) / len(df["v"])
# b_ecm = np.sum((df["b"] - df["a"]) ** 2) / len(df["b"])
# g_ecm = np.sum((df["g"] - df["a"]) ** 2) / len(df["g"])


# list of csv files in base_path
# files = [f for f in os.listdir(base_path) if f.endswith(".csv")]
# files.sort()
# values = []
# for file in files:
#     print(file)
#     match = pattern.match(file)
#     if match:
#         dt_value = float(match.group(1))
#         with open(f"{base_path}{file}") as f:
#             df = pd.read_csv(f)
#             v_ecm = np.sum(df["v"]) / len(df["v"])
#             b_ecm = np.sum(df["b"]) / len(df["b"])
#             g_ecm = np.sum(df["g"]) / len(df["g"])
#             values.append((dt_value, b_ecm, v_ecm, g_ecm))
#
# print(values)

values = [
    (1e-06, 6.894834055143456e-21, 4.939324628442577e-12, 6.254880500167978e-21),
    (5e-06, 2.497808589025838e-19, 1.2349466396576546e-10, 4.927719633423579e-22),
    (1e-05, 3.888563886035353e-18, 4.939667166884991e-10, 5.57229433899345e-23),
    (5e-05, 2.4409311643829224e-15, 1.2347175734929904e-08, 2.863552034190828e-24),
    (0.0001, 3.9056235025956353e-14, 4.937877470654522e-08, 1.4362931364989652e-24),
    (0.0005, 2.4412424283856885e-11, 1.232552118174259e-06, 3.732627553483389e-25),
    (0.001, 3.906417775735625e-10, 4.921306824156094e-06, 2.9992412325941357e-22),
    (0.005, 2.443773688842929e-07, 0.00012194591385902238, 3.349250723367167e-15),
    (0.01, 3.916382745118561e-06, 0.0004895291904116831, 4.056141286998137e-12),
    (0.05, 0.0026566144105224015, 0.023380031796746314, 0.00010669110895193562),
]
fig, ax = plt.subplots(figsize=(12, 8))
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
ax.set_yscale("log")

ax.set_xlabel("dt (s)", fontsize=20)
ax.set_ylabel("ECM", fontsize=20)
ax.legend(shadow=True, fancybox=True, loc=(1.05, 0.7), fontsize=20)
ax.tick_params(axis="both", which="major", labelsize=20)
