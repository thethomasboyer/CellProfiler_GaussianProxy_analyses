# This file runs the CellProfiler pipeline in parallel on each group of images,
# where a group is defined by the Metadata_VideoID field in the images' metadata
# (so groups are videos). It's a bit clunky but it actually works well.
# TODO: maybe use CellProfiler's batch mode?

import shutil
import string
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from subprocess import CompletedProcess

from tqdm import tqdm


def run_pipeline(group: str, output_dir: Path, debug: bool):
    cmd = [
        "cellprofiler",
        "-c",
        "-r",
        "-p",
        "track_nuclei_measure_size_shape.cppipe",
        "-o",
        output_dir.as_posix(),
        "--file-list",
        "list_biotine_files.txt",
        "-g",
        f"Metadata_VideoID={group}",
    ]
    if debug:
        tqdm.write(f"Would run: '{' '.join(cmd)}'")
        return True
    else:
        tqdm.write(f"Running command on group {group}")
        stdout_file = output_dir / f"{group}_stdout.txt"
        stderr_file = output_dir / f"{group}_stderr.txt"
        with stdout_file.open("w") as stdout, stderr_file.open("w") as stderr:
            result = subprocess.run(
                cmd,
                stdout=stdout,
                stderr=stderr,
                capture_output=False,
            )
        return result


def main():
    # Script args
    debug = False
    output_dir = Path(
        "/workspaces/biocomp/tboyer/sources/CellProfiler_GaussianProxy_analyses/analyses/biotine/"
    )
    num_processes = 16

    # Groups to be processed in parallel (== videos!)
    all_rows = tuple(string.ascii_uppercase[0:15])  # A to O
    all_cols = (13, 14)
    all_fields = (1, 2, 3, 4)
    groups = [
        f"{row}_{col}_fld_{field}"
        for row in all_rows
        for col in all_cols
        for field in all_fields
    ]

    # Confirm run
    print(f"Debug mode: {debug}")
    print(f"Number of processes: {num_processes}")
    print(f"Output directory: {output_dir}")
    print(f"Will run pipeline on {len(groups)} groups: {groups}")
    confirm = input("Are you sure you want to proceed? (y/n): ")
    if confirm.lower() != "y":
        print("Operation cancelled.")
        return

    if output_dir.exists() and not debug:
        erase_confirm = input(
            f"Do you want to erase the existing outputs at {output_dir}? (y/n): "
        )
        if erase_confirm.lower() == "y":
            print(f"Erasing outputs in {output_dir}")
            shutil.rmtree(output_dir)
        else:
            print("Output directory exists and will not be erased. Exiting.")
            return
    output_dir.mkdir(parents=True)

    with ThreadPoolExecutor(max_workers=num_processes) as executor:
        future_to_group = {
            executor.submit(run_pipeline, group, output_dir, debug): group
            for group in groups
        }
        for future in tqdm(as_completed(future_to_group), total=len(groups)):
            group = future_to_group[future]
            try:
                result = future.result()
                if isinstance(result, CompletedProcess) and result.returncode != 0:
                    tqdm.write(
                        f"Processing failed for group {group} with return code {result.returncode}"
                    )
            except Exception as exc:
                tqdm.write(f"Group {group} generated an exception: {exc}")


if __name__ == "__main__":
    main()
