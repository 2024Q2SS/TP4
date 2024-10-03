import matplotlib.pyplot as plt
import pandas as pd

with open("../DM/Verlet_output.csv") as verlet_f:
    with open("../DM/Beeman_output.csv") as beeman_f:
        with open("../DM/Gear5_output.csv") as gear5_f:

            verlet_df = pd.read_csv(verlet_f)
            beeman_df = pd.read_csv(beeman_f)
            gear5_df = pd.read_csv(gear5_f)

            fig, ax = plt.subplots()

            ax.plot(verlet_df["t"], verlet_df["r"], label="Verlet")
            ax.plot(beeman_df["t"], beeman_df["r"], label="Beeman")
            ax.plot(gear5_df["t"], gear5_df["r"], label="Gear5")

            plt.show()
