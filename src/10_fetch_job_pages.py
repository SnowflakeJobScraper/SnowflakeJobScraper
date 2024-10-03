# pylint: disable=C0103,W1203,C0114
# pylint: disable=W0401,W0614

import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

from config import (
    ALL_SEARCH_JOBS_JSON,
    ENCODING,
    FETCH_JOB_PAGES_DIR,
    LOG_FORMAT,
    LOG_LEVEL,
    MAX_WORKERS,
    USER_AGENT,
)
from fetch_page import fetch_page
from sanitize_filename import sanitize_filename

# Logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(Path(__file__).name)


def fetch_page_and_save(session: requests.Session, job: dict) -> str:
    """Download the job page and save it to a file"""
    URL = job["applyUrl"]
    FILEPATH = FETCH_JOB_PAGES_DIR / f"{sanitize_filename(URL)}.html"

    page = fetch_page(session, URL)
    if page:
        with open(FILEPATH, "w", encoding=ENCODING) as outfile:
            outfile.write(page)
        return f"Downloaded and saved: {FILEPATH}"

    logger.error(f"Failed to download {URL}")
    return f"Failed to download {URL}"


def main():
    """Load jobs list, fetch details for each job and save"""
    # Create folders
    FETCH_JOB_PAGES_DIR.mkdir(parents=True, exist_ok=True)

    try:
        with open(ALL_SEARCH_JOBS_JSON, "r", encoding=ENCODING) as file:
            jobs = json.load(file)

        with requests.Session() as session:
            session.headers.update({"User-Agent": USER_AGENT})

            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = [
                    executor.submit(fetch_page_and_save, session, job) for job in jobs
                ]
                for future in as_completed(futures):
                    result = future.result()
                    logger.info(result)
    except FileNotFoundError as e:
        logger.error(f"Failed to open job file: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse job file: {e}")


if __name__ == "__main__":
    main()
