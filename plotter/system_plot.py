import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

config = json.load(open("../config.json"))

steps = config["steps"]
dt = config["dt"]
t0 = config["t0"]
gamma = config["gamma"]
mass = config["mass"]
k = config["k"]
r0 = config["r0"]
print(
    "Steps: ", steps, "dt: ", dt, "t0: ", t0, "gamma: ", gamma, "mass: ", mass, "k: ", k
)

analitical = (
    lambda t: r0
    * np.exp(-gamma * t / (2 * mass))
    * np.cos(np.sqrt(k / mass - (gamma / (4 * mass)) ** 2) * t)
)

analitical_values = [analitical(t0 + i * dt) for i in range(steps)]
analitical_steps = [t0 + i * dt for i in range(steps)]


def format_sci_notation(value):
    exponent = int("{:e}".format(value).split("e")[1])
    base = float("{:e}".format(value).split("e")[0])
    return r"${:.2f} \times 10^{{{}}}$".format(base, exponent)


with open("../DM/Verlet_output.csv") as verlet_f:
    with open("../DM/Beeman_output.csv") as beeman_f:
        with open("../DM/Gear5_output.csv") as gear5_f:

            verlet_df = pd.read_csv(verlet_f)
            beeman_df = pd.read_csv(beeman_f)
            gear5_df = pd.read_csv(gear5_f)
            # calculo ECM para cada metodo

            verlet_ecm = np.sum((verlet_df["r"] - analitical_values) ** 2) / steps
            beeman_ecm = np.sum((beeman_df["r"] - analitical_values) ** 2) / steps
            gear5_ecm = np.sum((gear5_df["r"] - analitical_values) ** 2) / steps
            fig, ax = plt.subplots(figsize=(12, 8))

            ax.plot(
                verlet_df["t"],
                verlet_df["r"],
                label=rf"Verlet ECM={format_sci_notation(verlet_ecm)}",
                color="red",
                linestyle="dashed",
            )
            ax.plot(
                beeman_df["t"],
                beeman_df["r"],
                label=rf"Beeman ECM={format_sci_notation(beeman_ecm)}",
                color="black",
                linestyle="dashed",
            )
            ax.plot(
                gear5_df["t"],
                gear5_df["r"],
                label=rf"Gear5 ECM={format_sci_notation(gear5_ecm)}",
                color="green",
                linestyle="dashed",
            )
            ax.plot(
                analitical_steps,
                analitical_values,
                label="Analitical",
                color="blue",
                linestyle="dashed",
            )
            ax.tick_params(axis="both", which="major", labelsize=20)
            ax.legend(shadow=True, fancybox=True, loc=(1.05, 0.7), fontsize=20)
            ax.set_ylabel("posición (m)", fontsize=20)
            ax.set_xlabel("t (s)", fontsize=20)
            # ax.set_title("Comparacion de metodos")

            plt.show()
            plt.savefig("comparacion_metodos.png")
            plt.close()

            # Create zoomed-in plot
            t_min = 3.99  # Define the minimum t for zoom
            t_max = 4.01  # Define the maximum t for zoom

            # Filter data for zoom
            zoom_mask = (verlet_df["t"] >= t_min) & (verlet_df["t"] <= t_max)

            # Filter the analytical values
            analitical_zoom_steps = [t for t in analitical_steps if t_min < t <= t_max]
            analitical_zoom_values = [analitical(t) for t in analitical_zoom_steps]

            fig, ax_zoom = plt.subplots(figsize=(12, 8))
            ax_zoom.plot(
                verlet_df["t"][zoom_mask],
                verlet_df["r"][zoom_mask],
                label=rf"Verlet ECM={format_sci_notation(verlet_ecm)}",
                color="red",
            )
            ax_zoom.plot(
                beeman_df["t"][zoom_mask],
                beeman_df["r"][zoom_mask],
                label=rf"Beeman ECM={format_sci_notation(beeman_ecm)}",
                color="black",
            )
            ax_zoom.plot(
                gear5_df["t"][zoom_mask],
                gear5_df["r"][zoom_mask],
                label=rf"Gear5 ECM={format_sci_notation(gear5_ecm)}",
                color="green",
                linestyle="dashed",
            )
            ax_zoom.plot(
                analitical_zoom_steps,
                analitical_zoom_values,
                label="Analitical",
                color="blue",
            )
            ax_zoom.legend(shadow=True, fancybox=True, loc=(1.05, 0.7), fontsize=20)
            ax_zoom.set_ylabel("posición (m)", fontsize=20)
            ax_zoom.set_xlabel("t (s)", fontsize=20)
            ax_zoom.set_xticks(verlet_df["t"][zoom_mask])
            ax_zoom.tick_params(axis="both", which="major", labelsize=20)
            plt.show()
            plt.savefig("comparacion_metodos_zoom.png")
            plt.close()
