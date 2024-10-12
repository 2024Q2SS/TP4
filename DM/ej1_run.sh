#!/bin/bash

# Define arrays for dt and steps
dt_values=(0.05 0.01 0.005 0.001 0.0005 0.0001 0.00005 0.00001 0.000005 0.000001)

steps_values=(100 500 1000 5000 10000 50000 100000 500000 1000000 5000000)


# Path to config.json
config_file_path="../config.json"
base_output_dir="../simulation_runs"

# Create the base output directory if it doesn't exist
mkdir -p "$base_output_dir"

# Check if the arrays have the same length
if [ ${#dt_values[@]} -ne ${#steps_values[@]} ]; then

    echo "Error: dt_values and steps_values must have the same length."

    exit 1
fi

# Iterate over combinations of dt and steps
for i in "${!dt_values[@]}"; do
    dt="${dt_values[$i]}"
    steps="${steps_values[$i]}"

    # Create a new folder with the format dt_steps
    folder_name="dt_${dt}_steps_${steps}"
    output_folder_path="$base_output_dir/$folder_name"

    mkdir -p "$output_folder_path"

    for method in "Verlet" "Beeman" "Gear5"; do
        # Update config.json with new dt and steps values
        jq --arg method "$method" --arg dt "$dt" --arg steps "$steps" \
        '.method = $method | .dt = ($dt | tonumber) | .steps = ($steps | tonumber)' \
        "$config_file_path" > tmp.$$.json && mv tmp.$$.json "$config_file_path"
       
        echo "Running simulation for dt=${dt}, steps=${steps}, mehotd=${method}..."

        # Run the Maven command
        MAVEN_OPTS="-Xmx8g" mvn exec:java -Dexec.mainClass="ar.edu.itba.ss.App"

        mv "${method}_output.csv" "$output_folder_path"

        echo "Simulation for dt=${dt}, steps=${steps} completed."
    done
done

