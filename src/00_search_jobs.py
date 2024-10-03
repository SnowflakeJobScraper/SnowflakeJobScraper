# pylint: disable=C0103,W1203,C0114

import json
import logging
import re
from pathlib import Path

import pandas as pd
import requests

from config import (
    ALL_SEARCH_JOBS_JSON,
    ALL_SEARCH_JOBS_XLSX,
    CAREERS_URL,
    ENCODING,
    LOG_FORMAT,
    LOG_LEVEL,
    SEARCH_JOBS_JSON_DIR,
    SEARCH_JOBS_PAGES_DIR,
    USER_AGENT,
)
from fetch_page import fetch_page

# Logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(Path(__file__).name)


def save_to_file(
    content: str, file_path: Path, mode: str = "w", encoding: str = ENCODING
) -> None:
    """Save content to a file."""
    with open(file_path, mode, encoding=encoding) as f:
        f.write(content)


def extract_jobs_from_page(page_text: str) -> dict:
    """Extract job data from a page's text using regex."""

    # JSON assignment in JS script
    JOBS_REGEXP = r"""phApp\.ddo =(.*?); phApp\."""

    match = re.search(JOBS_REGEXP, page_text, flags=re.DOTALL)
    if match:
        # magic, below keys are not quoted, but it works!
        return json.loads(match.group(1))
    return None


def main():
    """Main function to fetch job listings and save them to files."""

    # Create folders
    SEARCH_JOBS_PAGES_DIR.mkdir(parents=True, exist_ok=True)
    SEARCH_JOBS_JSON_DIR.mkdir(parents=True, exist_ok=True)

    with requests.Session() as session:
        session.headers.update({"User-Agent": USER_AGENT})
        all_jobs = []
        start_num = 0

        while True:
            url = f"{CAREERS_URL}{start_num}"
            logger.info(f"Fetching URL: {url}")

            page_text = fetch_page(session, url)
            if not page_text:
                break

            # save jobs HTML version
            save_to_file(
                page_text, SEARCH_JOBS_PAGES_DIR / f"search-results_{start_num}.html"
            )

            # extract job data from HTML to object (dict)
            job_data = extract_jobs_from_page(page_text)

            # checks
            if not job_data:
                logger.info("No pattern match!?")
                break

            if "eagerLoadRefineSearch" not in job_data:
                logger.info(""""eagerLoadRefineSearch" key not found""")
                break

            job_data = job_data["eagerLoadRefineSearch"]
            if job_data["hits"] == 0:
                logger.info("No more jobs found.")
                break

            # checks OK
            # save job from listing - JSON version
            save_to_file(
                json.dumps(job_data, indent=4),
                SEARCH_JOBS_JSON_DIR / f"search-results_{start_num}.json",
            )
            all_jobs += job_data["data"]["jobs"]
            start_num += 10

        # print summary
        logger.info(f"Total jobs: {len(all_jobs)}")

        # sort list by object "applyUrl" field
        all_jobs.sort(key=lambda x: x["applyUrl"])

        # save as JSON
        logger.info(f"Saving file {ALL_SEARCH_JOBS_JSON}...")
        save_to_file(
            json.dumps(all_jobs, indent=4, sort_keys=True), ALL_SEARCH_JOBS_JSON
        )

        # save as XLS
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html
        logger.info(f"Saving file {ALL_SEARCH_JOBS_XLSX}...")
        df = pd.json_normalize(all_jobs, sep="_")
        df.to_excel(ALL_SEARCH_JOBS_XLSX)


if __name__ == "__main__":
    main()
