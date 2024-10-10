#!/bin/bash

# Define the range of omega values
omega_values=(300 600 1000 2000 3000)

# Path to the config file
config_file="../config.json"

# Create the target directory if it doesn't exist
mkdir -p 2_1

# Loop over the omega values
for omega in "${omega_values[@]}"
do
  # Use jq to update the omega value in config.json
  jq --arg omega_value "$omega" '.omega = ($omega_value | tonumber)' "$config_file" > temp_config.json && mv temp_config.json "$config_file"

  # Run the Java program with Maven
  mvn exec:java -Dexec.mainClass="ar.edu.itba.ss.CoupledOscillator"

  # Rename and move the output file
  mv output.csv "2_1/output_omega_$omega.csv"
done
