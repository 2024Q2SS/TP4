import glob
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Leer el número de osciladores desde el archivo config.json
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


# Lista de archivos CSV generados por los distintos valores de k
file_list = glob.glob("../DM/2_2/output_k_*.csv")

# Diccionario para almacenar las amplitudes máximas por k
k_amplitudes = {}

# Colores para las distintas curvas en el gráfico
colors = plt.cm.plasma(np.linspace(0, 1, len(file_list)))

# Graficar la evolución de la amplitud máxima en el tiempo para cada k
plt.figure(figsize=(10, 6))
for idx, filename in enumerate(sorted(file_list)):
    # Extraer el valor de k del nombre del archivo
    k_value = filename.split("_")[-1].split(".")[0]

    # Obtener los datos de tiempo, amplitud máxima en cada instante, y la amplitud máxima total
    t, max_amplitude_over_time, max_amplitude = get_amplitude_data(filename)

    # Guardar la amplitud máxima para el gráfico comparativo
    k_amplitudes[k_value] = max_amplitude

    # Graficar la evolución del módulo de la amplitud máxima en el tiempo
    plt.plot(t, max_amplitude_over_time, label=f"k = {k_value}", color=colors[idx])

plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud máxima |r| (m)")
plt.title("Evolución de la Amplitud Máxima en el Tiempo para Distintos k")
plt.legend()
plt.grid(True)
plt.show()

# Graficar la amplitud máxima para cada k
plt.figure(figsize=(8, 5))
ks = list(map(int, k_amplitudes.keys()))
amplitudes_max = list(k_amplitudes.values())
plt.plot(ks, amplitudes_max, marker="o")

plt.xlabel("Constante elástica k (kg/s^2)")
plt.ylabel("Amplitud máxima |r| (m)")
plt.title("Amplitud Máxima en Función de k")
plt.grid(True)
plt.show()
