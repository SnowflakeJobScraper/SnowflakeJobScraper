# pylint: disable=C0103,W1203,C0114

import json
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from config import (
    ENCODING,
    FETCH_JOB_PAGES_DIR,
    JOB_DETAILS_DESC_TXT_DIR,
    JOB_DETAILS_JSON_DIR,
    LOG_FORMAT,
    LOG_LEVEL,
    MAX_WORKERS,
)
from sanitize_filename import sanitize_filename

# Logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(Path(__file__).name)

pattern = re.compile(r""","jobDetail":(.*?),"flashParams""", re.DOTALL)


def process_file(filepath):
    """Process a single HTML file and extract job information."""
    try:
        with open(filepath, "r", encoding=ENCODING) as file:
            content = file.read()
            match = pattern.search(content)
            if match:
                g1 = match.group(1)
                parsed = json.loads(g1)
                title = sanitize_filename(
                    parsed["data"]["job"]["structureData"]["title"]
                )
                job_id = parsed["data"]["job"]["cmsJobId"]

                # Save parsed JSON
                json_filename = (
                    JOB_DETAILS_JSON_DIR / f"job_desc_json_[{title}]_{job_id}.json"
                )
                with open(json_filename, "w", encoding=ENCODING) as json_file:
                    json.dump(parsed, json_file, indent=4, sort_keys=True)

                # Clean and save job description
                desc = parsed["data"]["job"]["structureData"]["description"]
                desc = re.sub(r"<h3>", "\n", desc)
                desc = re.sub(r"<p>", "\n", desc)
                desc = re.sub(r"<li.*?>", "\n    - ", desc)
                desc = re.sub(r"<.*?>", "", desc)
                desc = re.sub(r"&nbsp;", "", desc)
                desc = re.sub(r"&amp", "&", desc)

                text_filename = (
                    JOB_DETAILS_DESC_TXT_DIR / f"job_desc_txt_[{title}]_{job_id}.txt"
                )
                with open(text_filename, "w", encoding=ENCODING) as text_file:
                    text_file.write(desc)

                return f"Processed: {filepath}"

            return f"No match found in: {filepath}"
    except OSError as e:
        logger.error(f"Failed to process {filepath}: {e}")
        return f"Failed: {filepath}"


def main(files: list):
    """Main function to process multiple files concurrently."""

    # Create folders
    JOB_DETAILS_JSON_DIR.mkdir(parents=True, exist_ok=True)
    JOB_DETAILS_DESC_TXT_DIR.mkdir(parents=True, exist_ok=True)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_file, file) for file in files]
        for future in as_completed(futures):
            logger.info(future.result())


if __name__ == "__main__":
    main(FETCH_JOB_PAGES_DIR.glob("*.html"))
