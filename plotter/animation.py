import matplotlib.pyplot as plt
import pandas as pd

# Cargar el archivo CSV
file_path = "../DM/output.csv"  # Reemplaza con la ruta a tu archivo CSV
data = pd.read_csv(file_path)

# Mostrar las primeras filas del dataframe para verificar la carga
print(data.head())

n = 100

data = data[::5]
# Definir las posiciones de r0 a r99
r_columns = [f"r{i}" for i in range(n)]  # r0 a r99
x_positions = [0.001 * i for i in range(n)]  # Posiciones desde 0 hasta 0.099


min_y = data[r_columns].min().min()
max_y = data[r_columns].max().max()


for t in data["t"]:
    # Filtrar los datos para el valor actual de t
    data_t = data[data["t"] == t]
    y_values = data_t[r_columns].values.flatten()

    plt.figure(figsize=(12, 8))
    plt.errorbar(x_positions, y_values, fmt="o-")  # Ajusta el error como desees
    plt.title(
        f"t = {t:.4f} s", fontsize=20
    )  # Mostrar el tiempo en centésimas de segundo
    plt.xlabel("Posición en X(m)", fontsize=20)
    plt.ylabel("Posicion en Y(m)", fontsize=20)
    plt.xlim(-0.01, n * 0.001 + 0.01)  # Ajustar límites x según sea necesario
    plt.ylim(min_y - 0.01, max_y + 0.01)
    plt.tick_params(
        axis="both", which="major", labelsize=20
    )  # Ajustar límites y según sea necesario
    plt.savefig(
        f"blob3/grafico_t_{t:.4f}.png"
    )  # Guardar la figura con el tiempo en centésimas
    plt.close()  # Cerrar la figura para liberar memoria
