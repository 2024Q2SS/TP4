#!/bin/bash

# Definición de los valores de k y omega correspondientes
k_values=(100 1000 2500 5000 9000)
w_values=(
    "8.5 9 9.5 9.75 10 10.5 11"
    "28 29 30 30.5 31 32 33"
    "48 49 49.5 50 50.5 51 52"
    "68 69 69.5 70 70.5 71 72"
    "92 93 93.5 94 94.5 95 96"
)

# Path to the config file
config_file="../config.json"

# Loop sobre los valores de k y omega
for i in "${!k_values[@]}"; do
  k="${k_values[$i]}"
  omega_set=(${w_values[$i]})  # Obtener el conjunto de valores de omega correspondientes a k

  # Loop sobre los valores de omega para el k actual
  for omega in "${omega_set[@]}"; do
    # Calcular dt como 1/(100*omega)
    dt=$(echo "1 / (100 * $omega)" | bc -l)

    # Calcular steps para que steps * dt = 5 segundos
    steps=$(echo "scale=0; 15 / $dt" | bc -l)

    # Usar jq para actualizar k, omega, dt, y steps en config.json
    jq --arg k_value "$k" '.k = ($k_value | tonumber)' "$config_file" > temp_config.json && mv temp_config.json "$config_file"
    jq --arg omega_value "$omega" '.omega = ($omega_value | tonumber)' "$config_file" > temp_config.json && mv temp_config.json "$config_file"
    jq --arg dt_value "$dt" '.dt = ($dt_value | tonumber)' "$config_file" > temp_config.json && mv temp_config.json "$config_file"
    jq --arg steps_value "$steps" '.steps = ($steps_value | tonumber)' "$config_file" > temp_config.json && mv temp_config.json "$config_file"

    # Crear la carpeta k_X si no existe
    mkdir -p "k_$k"

    # Ejecutar el programa
    mvn exec:java -Dexec.mainClass="ar.edu.itba.ss.CoupledOscillator"

    # Renombrar el archivo output.csv con el valor de omega y moverlo a la carpeta correspondiente
    mv output.csv "k_$k/output_$omega.csv"
  done
done


