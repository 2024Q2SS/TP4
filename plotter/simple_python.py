import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file_path = "../DM/ecm_dt_1.0E-6.csv"

df = pd.read_csv(file_path)

# v_ecm = np.sum((df["v"] - df["a"]) ** 2) / len(df["v"])
# b_ecm = np.sum((df["b"] - df["a"]) ** 2) / len(df["b"])
# g_ecm = np.sum((df["g"] - df["a"]) ** 2) / len(df["g"])

v_ecm = np.sum(df["v"]) / len(df["v"])
b_ecm = np.sum(df["b"]) / len(df["b"])
g_ecm = np.sum(df["g"]) / len(df["g"])

print(f"ECM for Verlet: {v_ecm}")
print(f"ECM for Beeman: {b_ecm}")
print(f"ECM for Gear5: {g_ecm}")
