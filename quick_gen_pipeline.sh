#!/bin/bash
#
# This script runs the CellProfiler pipeline on generated videos.

# Array of field names to process
field_names=(
    "J_14_fld_2"
    "L_13_fld_2"
    "N_14_fld_1"
    "O_14_fld_4"
)

echo "Processing fields: ${field_names[@]}"
echo "-----------------------------------"

# Loop through each field name and run the CellProfiler command
for field_name in "${field_names[@]}"; do
    echo "Processing $field_name..."

    # Define the base directory
    base_dir="/projects/static2dynamic/Thomas/experiments/GaussianProxy/biotine_all_paired_new_jz_MANUAL_WEIGHTS_DOWNLOAD_FROM_JZ_11-02-2025_14h31/inferences/InvertedRegeneration_100_diffsteps_no_SNR_leading_${field_name}"

    # Run the CellProfiler command
    set -x
    cellprofiler -c -r -p gen_biotine.cppipe -o "$base_dir/trajectories_-1_1 raw/cp_analysis" -i "$base_dir/trajectories_-1_1 raw"
    set +x

    echo "Completed processing $field_name"
    echo "-----------------------------------"
done

echo "All fields processed successfully"
