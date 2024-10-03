# pylint: disable=C0103,W1203,C0114

import json
import logging
from pathlib import Path

import pandas as pd

from config import (
    ALL_JOBS_DETAILS_JSON,
    ALL_JOBS_DETAILS_XLSX,
    ENCODING,
    JOB_DETAILS_JSON_DIR,
    LOG_FORMAT,
    LOG_LEVEL,
)

# Logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(Path(__file__).name)


def main(json_files: list):
    """Main function to process multiple files concurrently."""
    all_job_details = []
    for file in json_files:
        with open(file, "r", encoding=ENCODING) as f:
            all_job_details.append(json.load(f)["data"]["job"])

    # sort
    all_job_details.sort(key=lambda x: x["applyUrl"])

    # save JSON
    logger.info(f"Saving file {ALL_JOBS_DETAILS_JSON}...")
    json.dump(
        all_job_details,
        open(ALL_JOBS_DETAILS_JSON, "w", encoding=ENCODING),
        indent=4,
        sort_keys=True,
    )

    # save XLSX
    logger.info(f"Saving file {ALL_JOBS_DETAILS_XLSX}...")
    df = pd.json_normalize(all_job_details, sep="_")
    df.to_excel(ALL_JOBS_DETAILS_XLSX)


if __name__ == "__main__":
    main(JOB_DETAILS_JSON_DIR.glob("*.json"))
