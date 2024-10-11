import glob

# Leer el número de osciladores desde el archivo config.json
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

with open("../config.json") as f:
    config = json.load(f)
N = config["N"]  # Número de osciladores


# Función para leer el CSV y obtener la amplitud máxima en cada instante de tiempo
def get_amplitude_data(filename):
    # Leer el archivo CSV
    data = pd.read_csv(filename)

    # Extraer la columna de tiempo (t)
    t = data["t"].unique()

    # Inicializar una lista para las amplitudes máximas por instante de tiempo
    max_amplitudes = []

    # Calcular la amplitud máxima para cada instante de tiempo
    for i in range(len(t)):
        # Obtener las posiciones (r) de los N osciladores en el instante i
        positions = data["r"].iloc[i * N : (i + 1) * N]

        # Calcular el módulo de la amplitud para cada oscilador
        amplitudes = np.abs(positions)

        # Guardar la amplitud máxima de los osciladores en este instante
        max_amplitudes.append(np.max(amplitudes))

    return t, np.array(max_amplitudes), np.max(max_amplitudes)


# Lista de carpetas que contienen los resultados para cada k dentro de ../DM/
folders = glob.glob("../DM/k_*")

# Graficar la evolución de la amplitud máxima en el tiempo para cada k y cada omega
for folder in sorted(folders):
    k_value = folder.split("_")[1]
    file_list = glob.glob(f"{folder}/output_*.csv")

    # Diccionario para almacenar las amplitudes máximas por omega
    omega_amplitudes = {}

    # Colores para las distintas curvas en el gráfico
    colors = plt.cm.plasma(np.linspace(0, 1, len(file_list)))

    # Graficar la evolución de la amplitud máxima en el tiempo para cada omega en esta carpeta
    plt.figure(figsize=(10, 6))
    for idx, filename in enumerate(sorted(file_list)):
        # Extraer el valor de omega del nombre del archivo
        omega_value = filename.split("_")[-1].split(".")[0]

        # Obtener los datos de tiempo, amplitud máxima en cada instante, y la amplitud máxima total
        t, max_amplitude_over_time, max_amplitude = get_amplitude_data(filename)

        # Guardar la amplitud máxima para el gráfico comparativo
        omega_amplitudes[omega_value] = max_amplitude

        # Graficar la evolución del módulo de la amplitud máxima en el tiempo
        plt.plot(
            t,
            max_amplitude_over_time,
            label=f"Omega = {float(omega_value):.3g}",
            color=colors[idx],
        )

    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud máxima |r| (m)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Graficar la amplitud máxima para cada omega
    plt.figure(figsize=(8, 5))
    omegas = list(map(float, omega_amplitudes.keys()))
    amplitudes_max = list(omega_amplitudes.values())
    plt.plot(omegas, amplitudes_max, marker="o", linestyle="None")

    plt.xlim(left=0)
    plt.ylim(bottom=0)

    plt.xlabel("Omega (rad/s)")
    plt.ylabel("Amplitud máxima |r| (m)")
    plt.grid(True)
    plt.show()
