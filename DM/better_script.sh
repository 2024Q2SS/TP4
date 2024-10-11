#!/bin/bash

# Valores de k entre 100 y 10000
k_values=(100 1000 2500 5000 10000)

# Omega será variado cerca de omega0 (que es ~ sqrt(k/m))
# Vamos a usar valores cercanos a omega0, pero no el valor exacto
# Por ejemplo, valores: 0.8*omega0, 0.9*omega0, 1.1*omega0, 1.2*omega0
m=0.001  # Masa según config.json
omega_ratios=(0.8 0.9 1.1 1.2)

# Calcular sin(pi/100) una vez para optimizar
sin_value=$(echo "s (3.141592653589793 / 100)" | bc -l)

# Path to the config file
config_file="../config.json"

# Loop sobre los valores de k
for k in "${k_values[@]}"
do
  # Calcular omega0 para este k con sin(pi/100)
  omega0=$(echo "sqrt($k / $m) * $sin_value" | bc -l)

  # Loop sobre los ratios para omega
  for ratio in "${omega_ratios[@]}"
  do
    # Calcular omega usando el ratio y omega0
    omega=$(echo "$omega0 * $ratio" | bc -l)

    # Use jq para actualizar k (entero) y omega (double) en config.json
    jq --arg k_value "$k" '.k = ($k_value | tonumber)' "$config_file" > temp_config.json && mv temp_config.json "$config_file"
    jq --arg omega_value "$omega" '.omega = ($omega_value | tonumber)' "$config_file" > temp_config.json && mv temp_config.json "$config_file"

    # Crear la carpeta k_X si no existe
    mkdir -p "k_$k"

    # Ejecutar el programa
    mvn exec:java -Dexec.mainClass="ar.edu.itba.ss.CoupledOscillator"

    # Renombrar el archivo output.csv con el valor de omega y moverlo a la carpeta correspondiente
    mv output.csv "k_$k/output_$omega.csv"
  done
done


