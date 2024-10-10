#!/bin/bash

# Define the range of k values (5 values between 100 and 10000)
k_values=(100 1000 2500 5000 10000)

# Path to the config file
config_file="../config.json"

# Create the target directory if it doesn't exist
mkdir -p 2_2

# Loop over the k values
for k in "${k_values[@]}"
do
  # Use jq to update the k value in config.json
  jq --arg k_value "$k" '.k = ($k_value | tonumber)' "$config_file" > temp_config.json && mv temp_config.json "$config_file"

  # Run the Java program with Maven
  mvn exec:java -Dexec.mainClass="ar.edu.itba.ss.CoupledOscillator"

  # Rename and move the output file
  mv output.csv "2_2/output_k_$k.csv"
done
