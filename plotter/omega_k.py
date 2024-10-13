import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# Definición de los valores de k y sus correspondientes valores de omega
k_values = [100, 1000, 2500, 5000, 9000]
w_values = [
    [8.5, 9, 9.5, 9.75, 10, 10.5, 11],
    [28, 29, 30, 30.5, 31, 32, 33],
    [48, 49, 49.5, 50, 50.5, 51, 52],
    [68, 69, 69.5, 70, 70.5, 71, 72],
    [92, 93, 93.5, 94, 94.5, 95, 96],
]

# Listas para almacenar los resultados
omega0_values = []  # Amplitud máxima
k_results = []  # Valores de k correspondientes
r_columns = [f"r{i}" for i in range(100)]
# Loop sobre los valores de k
for i, k in enumerate(k_values):
    omegas = w_values[i]
    max_amplitude = 0
    best_omega = 0

    # Loop sobre los valores de omega para el k actual
    for omega in omegas:
        # Leer el archivo correspondiente
        output_file = (
            f"../DM/k_{k}/output_{omega}.csv"  # Actualizado para buscar en ../DM/k_{k}
        )

        # Leer el CSV para obtener la amplitud máxima (última columna "a")
        try:
            data = pd.read_csv(output_file)
            amplitude = np.abs(data[r_columns]).max().max()
        except FileNotFoundError:
            print(f"Archivo no encontrado: {output_file}")
            continue

        # Comprobar si esta amplitud es la máxima encontrada
        if amplitude > max_amplitude:
            max_amplitude = amplitude
            best_omega = omega  # Guardar el omega que da la amplitud máxima

    # Almacenar los resultados
    omega0_values.append(best_omega)
    k_results.append(k)


x_data = k_values
y_data = omega0_values


# Definir la función de regresión (raíz cuadrada)
def sqrt_function(x, c):
    return c * np.sqrt(x)


# Realizar el ajuste (regresión) con la función de raíz cuadrada
params, covariance = curve_fit(sqrt_function, x_data, y_data)

# Valor óptimo de la constante
optimal_c = params[0]
print(optimal_c)

# Predicciones usando el valor óptimo
y_pred = sqrt_function(x_data, optimal_c)

# Generar valores de x más densos para graficar la curva ajustada suavemente
x_smooth = np.linspace(
    min(x_data), max(x_data), 500
)  # 500 puntos entre el mínimo y máximo de x
y_smooth = sqrt_function(
    x_smooth, optimal_c
)  # Valores ajustados de y para la curva suave

plt.figure(figsize=(12, 8))
# Gráfico de los datos y la curva ajustada
plt.scatter(x_data, y_data, label="Datos")
plt.plot(
    x_smooth,
    y_smooth,
    color="red",
    label=rf"Ajuste por $f(x) = c \cdot \sqrt{{x}}$ (c={optimal_c:.4f})",
)  # Curva suave
plt.xlabel("Valores de k (kg/s²)", fontsize=20)
plt.ylabel("Omega0 (rad/s)", fontsize=20)
plt.xticks(x_data)
plt.yticks(y_data)
plt.tick_params(axis="both", which="major", labelsize=20)
plt.legend(fancybox=True, shadow=True, loc=(1.05, 0.7), fontsize=20)
plt.grid(True)
plt.show()


# Paso 4: Cálculo del error cuadrático medio (ECM)
def calculate_error(c):
    return np.sum((y_data - sqrt_function(x_data, c)) ** 2)


# Valores de la constante c para probar
c_values = np.linspace(0.1, 2 * optimal_c, 100)
errors = [calculate_error(c) for c in c_values]
plt.figure(figsize=(12, 8))
# Graficar el error en función de c
plt.plot(c_values, errors, label="Error del ajuste")
plt.axvline(
    x=optimal_c, color="red", linestyle="--", label=f"Mínimo en c={optimal_c:.4f}"
)
plt.xlabel("Valor de c", fontsize=20)
plt.ylabel("Error(c)", fontsize=20)
plt.tick_params(axis="both", which="major", labelsize=20)
plt.legend(fancybox=True, shadow=True, loc=(1.05, 0.7), fontsize=20)
plt.grid(True)
plt.show()
