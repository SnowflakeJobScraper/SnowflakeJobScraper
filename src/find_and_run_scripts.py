# pylint: disable=C0103,W1203,C0114

import os
import re
import subprocess

def find_and_run_scripts(directory):
    # Filename should start with 2 digits and underscore
    pattern = re.compile(r'^\d{2}_.*\.py$')

    # Get matching files
    all_files = os.listdir(directory)
    matched_files = [f for f in all_files if pattern.match(f)]

    # Sort files
    matched_files.sort()

    # Execute each file
    for script in matched_files:
        script_path = os.path.join(directory, script)
        try:
            subprocess.run(['python', script_path], check=True)
            print(f"Successfully ran {script}")
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {e}")

# Sample use
find_and_run_scripts('.')
