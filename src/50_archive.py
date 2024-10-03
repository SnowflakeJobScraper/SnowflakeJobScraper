# pylint: disable=C0103,W1203,C0114

import logging
import os
from datetime import datetime
from pathlib import Path

from config import LOG_FORMAT, LOG_LEVEL, OUTPUT_DIR

# Logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(Path(__file__).name)


def main():
    """Rename output folder to output with timestamp"""

    # Get current timestamp and names
    current_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    old_folder_name = OUTPUT_DIR
    new_folder_name = f"{old_folder_name}-{current_timestamp}"

    # Rename folder
    try:
        os.rename(old_folder_name, new_folder_name)
        logger.info(f"Folder renamed from '{old_folder_name}' to '{new_folder_name}'")
    except OSError as e:
        logger.error(f"Failure: {e}")

if __name__ == "__main__":
    main()
