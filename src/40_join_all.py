# pylint: disable=C0103,W1203,C0114

import json
import logging
from pathlib import Path

import pandas as pd

from config import (
    ALL_JOBS_DETAILS_JSON,
    ALL_JOBS_JOINED_JSON,
    ALL_JOBS_JOINED_XLSX,
    ALL_SEARCH_JOBS_JSON,
    ENCODING,
    LOG_FORMAT,
    LOG_LEVEL,
)

# Logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(Path(__file__).name)


def main():
    """joins details"""

    all_search_jobs = json.load(open(ALL_SEARCH_JOBS_JSON, "r", encoding=ENCODING))
    all_jobs_details = json.load(open(ALL_JOBS_DETAILS_JSON, "r", encoding=ENCODING))

    all_search_jobs_look_up_table = {}
    for search_job in all_search_jobs:
        all_search_jobs_look_up_table[search_job["applyUrl"]] = search_job

    all_details_joined = []
    for job_detail in all_jobs_details:
        all_details_joined.append(
            # merge row: search_job + jobs_detail
            all_search_jobs_look_up_table[job_detail["applyUrl"]]
            | job_detail
        )

    # sort
    all_details_joined.sort(key=lambda x: x["applyUrl"])

    # save JSON
    logger.info(f"Saving file {ALL_JOBS_JOINED_JSON}...")
    json.dump(
        all_details_joined,
        open(ALL_JOBS_JOINED_JSON, "w", encoding=ENCODING),
        sort_keys=True,
        indent=4,
    )

    # save XLSX
    logger.info(f"Saving file {ALL_JOBS_JOINED_XLSX}...")
    df = pd.json_normalize(all_details_joined, sep="_")
    df.to_excel(ALL_JOBS_JOINED_XLSX)


if __name__ == "__main__":
    main()
