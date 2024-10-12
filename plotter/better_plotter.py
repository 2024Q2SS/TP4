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


# Función para leer el CSV y obtener la amplitud máxima en cada instante de tiempo
def get_amplitude_data(filename):
    # Leer el archivo CSV sin redondeos o conversiones
    data = pd.read_csv(filename)

    # Extraer la columna de tiempo (t) asegurando que no hay pérdida de precisión
    t = data["t"].unique()

    # Inicializar una lista para las amplitudes máximas por instante de tiempo
    max_amplitudes = []

    # Calcular la amplitud máxima para cada instante de tiempo sin redondeos
    for i in range(len(t)):
        # Obtener las posiciones (r) de los N osciladores en el instante i sin perder precisión
        positions = data["r"].iloc[i * N : (i + 1) * N]

        # Calcular el módulo de la amplitud para cada oscilador sin redondear
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
    closest_omegas = sorted(sorted_omegas, key=lambda x: abs(x - max_omega))[1:3]

    # Unir la omega máxima con las dos más cercanas sin redondeos
    omegas_to_plot = [max_omega] + closest_omegas

    # Graficar la evolución de la amplitud máxima en el tiempo para las tres omegas seleccionadas
    plt.figure(figsize=(10, 6))
    for idx, omega in enumerate(sorted(omegas_to_plot)):
        t, max_amplitude_over_time = all_data[omega]
        plt.plot(
            t, max_amplitude_over_time, label=f"Omega = {omega:.3f}", color=colors[idx]
        )  # Sin redondear

    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud máxima |r| (m)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Graficar la amplitud máxima para cada omega
    plt.figure(figsize=(8, 5))
    omegas = list(omega_amplitudes.keys())
    amplitudes_max = list(omega_amplitudes.values())
    plt.plot(omegas, amplitudes_max, marker="o", linestyle="None")

    plt.xticks(omegas)
    plt.ylim(bottom=0)

    plt.xlabel("Omega (rad/s)")
    plt.ylabel("Amplitud máxima |r| (m)")
    plt.grid(True)
    plt.show()
