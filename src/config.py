# pylint: disable=C0103,W1203,C0114

from pathlib import Path

# Encoding
ENCODING = "UTF-8"


# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"


# Careers URL and User Agent
CAREERS_URL = "https://careers.snowflake.com/us/en/search-results?s=1&from="
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


# Request settings
REQUEST_TIMEOUT = 60
MAX_RETRIES = 3


# Directory structure
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
SEARCH_JOBS_PAGES_DIR = OUTPUT_DIR / "00_search_jobs_pages"
SEARCH_JOBS_JSON_DIR = OUTPUT_DIR / "00_search_jobs_json"
FETCH_JOB_PAGES_DIR = OUTPUT_DIR / "10_fetch_job_pages"
JOB_DETAILS_JSON_DIR = OUTPUT_DIR / "20_job_details_json"
JOB_DETAILS_DESC_TXT_DIR = OUTPUT_DIR / "20_job_details_desc_txt"


# Output files
ALL_SEARCH_JOBS_JSON = OUTPUT_DIR / "00_all_search_jobs.json"
ALL_SEARCH_JOBS_XLSX = OUTPUT_DIR / "00_all_search_jobs.xlsx"
ALL_JOBS_DETAILS_JSON = OUTPUT_DIR / "30_all_jobs_details.json"
ALL_JOBS_DETAILS_XLSX = OUTPUT_DIR / "30_all_jobs_details.xlsx"
ALL_JOBS_JOINED_JSON = OUTPUT_DIR / "40_all_jobs_joined.json"
ALL_JOBS_JOINED_XLSX = OUTPUT_DIR / "40_all_jobs_joined.xlsx"


# Processing settings
MAX_WORKERS = 10
