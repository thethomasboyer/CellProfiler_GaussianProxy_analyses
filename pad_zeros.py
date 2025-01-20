# This script pads zeros to the time number in the filename of some directory
# because CellProfiler does not allow a custom ordering of files...

import os
import re

# Define the directory containing your files
directory = "/projects/static2dynamic/datasets/biotine/3_channels_min_99_perc_normalized_rgb_stacks_png"
debug_mode = False  # Set to True for debug mode, False for actual renaming

if not debug_mode:
    inpt = input(f"WARNING: will rename files at {directory}. Continue? (y/[n])")
    if inpt.lower() != "y":
        print("Exiting without renaming files")
        exit(0)

# Regular expression to match "time_<x>"
pattern = re.compile(r"_time_([1-9]|1[0-9]).png$")

for filename in os.listdir(directory):
    match = pattern.search(filename)
    if match:
        num = int(match.group(1))
        if num < 10:  # Single digit
            new_filename = pattern.sub(f"_time_{num:02d}.png", filename)
            if debug_mode:
                print(f"Would rename: {filename} -> {new_filename}")
            else:
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
    else:
        print(f"WARNING: filename {filename} did not match pattern; skipping")
