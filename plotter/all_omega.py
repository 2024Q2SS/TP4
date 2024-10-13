import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Definición de los valores de k y sus correspondientes valores de omega
k_values = [100, 1000, 2500, 5000, 9000]
w_values = [
    [8.5, 9, 9.5, 9.75, 10, 10.5, 11],
    [28, 29, 30, 30.5, 31, 32, 33],
    [48, 49, 49.5, 50, 50.5, 51, 52],
    [68, 69, 69.5, 70, 70.5, 71, 72],
    [92, 93, 93.5, 94, 94.5, 95, 96],
]

# Colores para cada conjunto de k
colors = plt.cm.plasma(np.linspace(0, 1, len(k_values)))

# Crear el gráfico
fig, ax = plt.subplots(figsize=(12, 8))

r_columns = [f"r{i}" for i in range(100)]

# Loop sobre los valores de k y omega
for i, k in enumerate(k_values):
    omegas = w_values[i]
    amplitudes_max = []

    # Loop sobre los valores de omega para el k actual
    for omega in omegas:
        # Leer el archivo correspondiente
        output_file = f"../DM/k_{k}/output_{omega}.csv"

        # Leer el CSV para obtener la amplitud máxima (última columna "a")
        try:
            data = pd.read_csv(output_file)
            amplitudes_max.append(
                np.abs(data[r_columns]).max().max()
            )  # Calcular la amplitud máxima
        except FileNotFoundError:
            print(f"Archivo no encontrado: {output_file}")
            continue

    # Graficar la amplitud máxima en función de omega, conectando los puntos
    ax.plot(omegas, amplitudes_max, marker="o", color=colors[i], label=f"k = {k}")

# Personalizar el gráfico
# plt.yscale("log")
plt.subplots_adjust(right=0.8)
ax.set_xlabel("Omega (rad/s)", fontsize=20)
ax.set_ylabel("Amplitud máxima |r| (m)", fontsize=20)
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
ax.tick_params(axis="both", which="major", labelsize=20)
ax.legend(
    shadow=True,
    fancybox=True,
    bbox_to_anchor=(1.5, 0.7),
    loc="upper left",
    fontsize=20,
)
ax.grid(True)
ax.legend(title="Valores de k")
plt.show()
