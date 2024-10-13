import glob
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Leer el número de osciladores desde el archivo config.json
with open("../config.json") as f:
    config = json.load(f)
N = config["N"]  # Número de osciladores

r_columns = [f"r{i}" for i in range(N)]


# Función para leer el CSV y obtener la amplitud máxima en cada instante de tiempo
def get_amplitude_data(filename):
    # Leer el archivo CSV sin redondeos o conversiones
    df = pd.read_csv(filename)

    # Inicializar una lista para las amplitudes máximas por instante de tiempo
    # Calcular el valor absoluto máximo entre r0, r1, ..., r99 para cada tiempo
    posiciones = df.loc[:, 'r0':'r99']
    max_amplitude_over_time = posiciones.abs().max(axis=1)

    # Calcular la amplitud máxima global
    max_amplitude_global = max_amplitude_over_time.max()
    t = df["t"]
    return np.array(t), np.array(max_amplitude_over_time), np.array(max_amplitude_global)
# Lista de carpetas que contienen los resultados para cada k dentro de ../DM/
folders = glob.glob("../DM/k_*")

# Graficar la evolución de la amplitud máxima en el tiempo para cada k y cada omega
for folder in sorted(folders):
    k_value = folder.split("_")[1]
    file_list = glob.glob(f"{folder}/output_*.csv")

    # Diccionario para almacenar las amplitudes máximas por omega
    omega_amplitudes = {}
    all_data = (
        {}
    )  # Diccionario para almacenar los tiempos y amplitudes máximas por omega

    # Colores para las distintas curvas en el gráfico
    colors = ["red", "green", "blue"]

    # Recopilar la amplitud máxima en el tiempo para cada omega
    for idx, filename in enumerate(sorted(file_list)):
        # Extraer el valor de omega del nombre del archivo, capturando todos los decimales
        omega_value = filename.split("_")[-1].replace(".csv", "")

        # Convertir el valor de omega a float directamente sin redondeo
        omega_float = float(omega_value)

        # **Imprimir el valor de omega extraído del archivo**
        print(f"Omega extraído: {omega_value}")

        # Obtener los datos de tiempo, amplitud máxima en cada instante, y la amplitud máxima total
        t, max_amplitude_over_time, max_amplitude = get_amplitude_data(filename)

        # Guardar la amplitud máxima en el diccionario
        omega_amplitudes[omega_float] = max_amplitude

        # **Imprimir el valor de omega después de guardarlo en el diccionario**
        print(f"Omega guardado en el diccionario: {omega_float}")

        # Guardar también los datos de tiempo y la evolución de amplitudes para graficar después
        all_data[omega_float] = (t, max_amplitude_over_time)

    # Ordenar las omegas por su amplitud máxima sin perder precisión
    sorted_omegas = sorted(
        omega_amplitudes.keys(), key=lambda x: omega_amplitudes[x], reverse=True
    )

    # Obtener la omega con la amplitud máxima más grande sin redondear
    max_omega = sorted_omegas[0]

    # Encontrar las dos omegas más cercanas (una mayor y otra menor) sin perder precisión
    closest_omegas = sorted(sorted_omegas, key=lambda x: abs(x - max_omega))[1:4]

    # Unir la omega máxima con las dos más cercanas sin redondeos
    omegas_to_plot = closest_omegas

    # Graficar la evolución de la amplitud máxima en el tiempo para las tres omegas seleccionadas
    plt.figure(figsize=(12, 8))
    for idx, omega in enumerate(sorted(omegas_to_plot)):
        t, max_amplitude_over_time = all_data[omega]
        plt.plot(
            t, max_amplitude_over_time, label=f"Omega = {omega:.3f}", color=colors[idx]
        )  # Sin redondear

    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.xlabel("Tiempo (s)", fontsize=20)
    plt.ylabel("Amplitud máxima |r| (m)", fontsize=20)
    plt.tick_params(axis="both", which="major", labelsize=20)
    plt.legend(fancybox=True, shadow=True, loc=(1.05, 0.7), fontsize=20)
    plt.grid(True)
    plt.show()

    # Graficar la evolución de la amplitud máxima en el tiempo para las tres omegas seleccionadas
    plt.figure(figsize=(12, 8))
    for idx, omega in enumerate(sorted(omegas_to_plot)):
        t, max_amplitude_over_time = all_data[omega]
    
        # Zoom in on the last 20 seconds
        #zoom_start = mint(t) - 40  # Determine the start of the zoom (last 20 seconds)
        plt.plot(
            t, max_amplitude_over_time, label=f"Omega = {omega:.3f}", color=colors[idx]
        )

    # Set xlim to zoom in on the last 20 seconds
    plt.xlim(left=0, right=15)  # Left boundary is last 20 seconds, right is max time
    plt.ylim(bottom=0)
    plt.xlabel("Tiempo (s)", fontsize=20)
    plt.ylabel("Amplitud máxima |r| (m)", fontsize=20)
    plt.tick_params(axis="both", which="major", labelsize=20)
    plt.legend(fancybox=True, shadow=True, loc=(1.05, 0.7), fontsize=20)
    plt.grid(True)
    plt.show()
    # Graficar la amplitud máxima para cada omega
    plt.figure(figsize=(12, 8))
    omegas = list(omega_amplitudes.keys())
    amplitudes_max = list(omega_amplitudes.values())
    plt.plot(omegas, amplitudes_max, marker="o", linestyle="None")

    plt.xticks(omegas)
    plt.ylim(bottom=0)
    plt.tick_params(axis="both", which="major", labelsize=20)
    plt.xlabel("Omega (rad/s)", fontsize = 20)
    plt.ylabel("Amplitud máxima |r| (m)", fontsize = 20)
    plt.grid(True)
    plt.show()
